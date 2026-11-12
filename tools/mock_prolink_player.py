#!/usr/bin/env python3
"""Fake Pro DJ Link player for testing NauticMixxx's NETWORK > Pioneer reader.

Broadcasts keep-alive packets to UDP 50000 and serves a directory as the player's
USB slot over NFS v2 (portmapper 111, mountd, nfsd, all UDP). Read-only.
It checks the reader against this script, NOT against real CDJ/XDJ hardware.

  mock_prolink_player.py DIR [--ip 127.0.0.1] [--slot C]

DIR is laid out like a stick (PIONEER/rekordbox/export.pdb, Contents/...).
Needs root for port 111.
"""
import argparse, os, socket, struct, threading, time

def pack(*vals):
    return b"".join(struct.pack(">I", v) for v in vals)

def xdr_opaque(data):
    return pack(len(data)) + data + b"\0" * ((4 - len(data) % 4) % 4)

class Handles:
    def __init__(self, root):
        self.root = os.path.realpath(root)
        self.by_id = {}
        self.by_path = {}
    def handle(self, path):
        path = os.path.realpath(path)
        if not path.startswith(self.root):
            return None
        hid = self.by_path.get(path)
        if hid is None:
            hid = len(self.by_id) + 1
            self.by_id[hid] = path
            self.by_path[path] = hid
        return struct.pack(">I", hid) + b"\0" * 28
    def path(self, fh):
        return self.by_id.get(struct.unpack(">I", fh[:4])[0])

def fattr(path):
    st = os.stat(path)
    ftype = 2 if os.path.isdir(path) else 1
    return pack(ftype, st.st_mode & 0xFFFF, 1, 0, 0, st.st_size, 4096, 0, (st.st_size + 511) // 512,
                1, st.st_ino & 0xFFFFFFFF, int(st.st_atime), 0, int(st.st_mtime), 0, int(st.st_ctime), 0)

def reply(xid, body):
    return pack(xid, 1, 0, 0, 0, 0) + body  # REPLY, MSG_ACCEPTED, AUTH_NULL verifier, SUCCESS

def parse_call(data):
    xid, mtype, rpcvers, prog, vers, proc = struct.unpack(">6I", data[:24])
    pos = 24
    for _ in range(2):  # credential, verifier
        _, ln = struct.unpack(">II", data[pos:pos + 8])
        pos += 8 + ((ln + 3) & ~3)
    return xid, prog, vers, proc, data[pos:]

def serve(sock, handler):
    while True:
        data, addr = sock.recvfrom(65535)
        try:
            xid, prog, vers, proc, args = parse_call(data)
            sock.sendto(reply(xid, handler(prog, vers, proc, args)), addr)
        except Exception as exc:  # keep serving
            print("rpc error", exc)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--ip", default="127.0.0.1")
    ap.add_argument("--slot", default="C")
    ap.add_argument("--name", default="CDJ-MOCK")
    ap.add_argument("--number", type=int, default=1)
    a = ap.parse_args()
    handles = Handles(a.dir)
    socks = {n: socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for n in ("port", "mount", "nfs")}
    for s in socks.values():
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    socks["port"].bind((a.ip, 111)); socks["mount"].bind((a.ip, 0)); socks["nfs"].bind((a.ip, 0))
    ports = {"mount": socks["mount"].getsockname()[1], "nfs": socks["nfs"].getsockname()[1]}

    def portmap(prog, vers, proc, args):
        if proc == 3:
            p, v, proto, _ = struct.unpack(">4I", args[:16])
            return pack({100005: ports["mount"], 100003: ports["nfs"]}.get(p, 0))
        return pack(0)

    def mountd(prog, vers, proc, args):
        if proc == 1:
            ln = struct.unpack(">I", args[:4])[0]
            export = args[4:4 + ln].decode()
            if export.strip("/") != a.slot:
                return pack(13)  # EACCES
            return pack(0) + handles.handle(a.dir)
        return pack(0)

    def nfsd(prog, vers, proc, args):
        if proc == 4:  # LOOKUP
            fh = args[:32]
            ln = struct.unpack(">I", args[32:36])[0]
            name = args[36:36 + ln].decode()
            base = handles.path(fh)
            target = os.path.join(base, name) if base and "/" not in name and name not in ("..",) else None
            if not target or not os.path.exists(target):
                return pack(2)  # NFSERR_NOENT
            return pack(0) + handles.handle(target) + fattr(target)
        if proc == 6:  # READ
            fh = args[:32]
            offset, count, _ = struct.unpack(">3I", args[32:44])
            path = handles.path(fh)
            if not path or not os.path.isfile(path):
                return pack(2)
            with open(path, "rb") as f:
                f.seek(offset)
                data = f.read(min(count, 8192))
            return pack(0) + fattr(path) + xdr_opaque(data)
        return pack(0)

    for name, fn in (("port", portmap), ("mount", mountd), ("nfs", nfsd)):
        threading.Thread(target=serve, args=(socks[name], fn), daemon=True).start()

    beacon = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    packet = bytearray(0x36)
    packet[0:10] = b"Qspt1WmJOL"
    packet[0x0a] = 0x06
    packet[0x0c:0x0c + len(a.name)] = a.name.encode()
    packet[0x24] = a.number
    packet[0x26:0x2c] = bytes([0xde, 0xad, 0xbe, 0xef, 0, a.number])
    packet[0x2c:0x30] = bytes(int(x) for x in a.ip.split("."))
    print("mock player", a.name, "serving", a.dir, "as /%s/ on" % a.slot, a.ip, flush=True)
    while True:
        beacon.sendto(bytes(packet), (a.ip, 50000))
        time.sleep(1.5)

main()
