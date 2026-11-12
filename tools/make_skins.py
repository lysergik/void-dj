#!/usr/bin/env python3
"""Derive the small-screen NauticMixxx skins from the 1280x800 master skin.

The master skin (skins/XDJ_RX3_Mixxx) stays hand-maintained.  Each derived
skin has its own native reference size, so every pixel in its XML/QSS is a
real pixel of the target screen.  Per profile the generator:
  * rescales every fixed XML size (axis-aware, never below 1px),
  * rescales every QSS length, with a legibility floor for text,
  * applies design overrides (re-prioritised layout: some elements get
    different sizes, secondary readouts are dropped),
  * appends a per-profile QSS block (touch targets, tightened paddings).
Run:  python3 tools/make_skins.py   (from the repository root)
"""
import re, shutil, sys, os
import xml.etree.ElementTree as ET
from pathlib import Path
from profiles import PROFILES

ROOT = Path(__file__).resolve().parent.parent
MASTER = ROOT / "skins" / "XDJ_RX3_Mixxx"

TOKEN = re.compile(r"^(\d+)(me|mi|ma|min|max|e|i|f|p)?$")


def scale_token(tok, k):
    m = TOKEN.match(tok.strip())
    if not m:
        return tok
    num, kind = int(m.group(1)), m.group(2) or ""
    if kind in ("f", "me", "e", "min", "mi") and num > 0:
        num = max(1, round(num * k))
    return f"{num}{kind}"


def scale_size(text, kx, ky):
    parts = text.split(",")
    if len(parts) != 2:
        return text
    return f"{scale_token(parts[0], kx)},{scale_token(parts[1], ky)}"


def object_name(el):
    n = el.find("ObjectName")
    return n.text.strip() if n is not None and n.text else None


def transform_xml(path, prof, out):
    tree = ET.parse(path)
    root = tree.getroot()
    kx, ky = prof["kx"], prof["ky"]
    sizes = prof.get("sizes", {})
    hide = set(prof.get("hide", []))
    setvars = prof.get("setvars", {})

    def walk(parent):
        for child in list(parent):
            nm = object_name(child) if len(child) else None
            if nm in hide:
                parent.remove(child)
                continue
            walk(child)

    walk(root)
    for el in root.iter():
        if el.tag == "SetVariable" and el.get("name") in setvars:
            el.text = str(setvars[el.get("name")])
        if len(el) and el.find("Size") is not None:
            sz = el.find("Size")
            nm = object_name(el)
            if nm in sizes:
                sz.text = sizes[nm]
                for c in list(sz):
                    sz.remove(c)
            elif len(sz) == 0 and sz.text:
                sz.text = scale_size(sz.text, kx, ky)
    for el in root.iter():  # Size nodes outside ObjectName'd parents
        if el.tag == "Size" and len(el) == 0 and el.text and not el.get("_done"):
            pass
    out.parent.mkdir(parents=True, exist_ok=True)
    tree.write(out, encoding="utf-8", xml_declaration=False)


PX = re.compile(r"(-?\d+(?:\.\d+)?)px")


def transform_qss(text, prof):
    kl = prof["kl"]
    kf = prof["kf"]
    floor = prof["font_floor"]
    # text sizes: scale with floor; every other length: scale, keep >=1
    def font_sub(m):
        v = float(m.group(2))
        return f"{m.group(1)}{max(floor, round(v * kf))}px"
    text = re.sub(r"(font-size:\s*)(\d+(?:\.\d+)?)px", font_sub, text)

    def len_sub(m):
        # skip anything already rewritten as font-size by checking context
        v = float(m.group(1))
        if v == 0:
            return "0px"
        return f"{max(1, round(v * kl)) if abs(v) >= 1 else v}px"
    out, pos = [], 0
    for m in PX.finditer(text):
        start = m.start()
        line_start = text.rfind("\n", 0, start) + 1
        ctx = text[line_start:start]
        out.append(text[pos:start])
        if re.search(r"font-size:\s*$", ctx) and False:
            out.append(m.group(0))
        elif re.search(r"font-size:\s*\d*$", ctx) is not None and ctx.rstrip().endswith("font-size:"):
            out.append(m.group(0))
        else:
            out.append(len_sub(m))
        pos = m.end()
    out.append(text[pos:])
    return "".join(out)


def build(name, prof):
    dst = ROOT / "skins" / prof["dir"]
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(MASTER, dst, ignore=shutil.ignore_patterns("*.xml", "style.qss", "install*.sh"))
    for xml in MASTER.glob("*.xml"):
        if xml.name == "skin.xml":
            continue
        transform_xml(xml, prof, dst / xml.name)
    # skin.xml: own reference size, manifest, launch image
    s = (MASTER / "skin.xml").read_text(encoding="utf-8")
    w, h = prof["size"]
    s = s.replace("<title>NauticMixxx</title>", f"<title>NauticMixxx {w}x{h}</title>")
    s = s.replace("<MinimumSize>1280,800</MinimumSize>", f"<MinimumSize>{w},{h}</MinimumSize>")
    s = s.replace("<ReferenceSize>1280,800</ReferenceSize>", f"<ReferenceSize>{w},{h}</ReferenceSize>")
    s = s.replace("<Rx3DisplayState>true</Rx3DisplayState>",
                  f"<Rx3DisplayState>true</Rx3DisplayState>\n\t<Rx3UiScale>{prof['ui']}</Rx3UiScale>")
    s = s.replace("<Size>0me,48f</Size>", f"<Size>0me,{prof['topbar_wrap']}f</Size>")
    s = s.replace("1074px", f"{round(1074*prof['kx'])}px").replace("358px", f"{round(358*prof['kx'])}px")
    (dst / "skin.xml").write_text(s, encoding="utf-8")
    q = (MASTER / "style.qss").read_text(encoding="utf-8")
    q = transform_qss(q, prof)
    extra = prof.get("qss", "")
    (dst / "style.qss").write_text(q + "\n/* ---- " + name + " design overrides ---- */\n" + extra, encoding="utf-8")
    (dst / "README.md").write_text(
        f"# NauticMixxx {w}x{h}\n\nGenerated by tools/make_skins.py from XDJ_RX3_Mixxx.\n"
        "Edit tools/profiles.py, not these files.\n", encoding="utf-8")
    print("built", dst)


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent))
    only = sys.argv[1:] or list(PROFILES)
    for n in only:
        build(n, PROFILES[n])
