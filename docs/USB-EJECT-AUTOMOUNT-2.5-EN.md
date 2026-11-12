# USB EJECT and automount (patch 0062)

## EJECT

SOURCE lists the USB devices; select one and press **EJECT** (below MY SETTINGS MENU).
Controller mappings and the keyboard layer can call `[RX3Browser],usb_eject`.

1. If a deck has a track from that device loaded the button refuses ("DECK 1 HAS A TRACK FROM USB1 — EJECT THAT TRACK FIRST").
2. The device's library session is released, data is synced and the volume is unmounted (up to six attempts over three seconds, because a file may still be closing).
3. The result is shown under the button: `USB1 EJECTED — SAFE TO REMOVE`, `DEVICE BUSY — STOP THE DECKS USING IT`, `NO PERMISSION TO UNMOUNT (ROOT OR SUDO NEEDED)` or `UNMOUNT FAILED` (details in the log).

If `udisksctl` is installed (it is not part of stock DietPi) the port is also powered off once its last partition is unmounted.

## Automount at start-up (Linux)

A background thread runs when NauticMixxx starts:

1. `lsblk -J` lists disks and partitions.
2. A disk is a **system disk** and is left completely alone when any of its volumes is mounted at `/`, `/boot`, `/boot/firmware`, `/boot/efi`, `/usr`, `/var`, `/home`, `/opt`, `/tmp`, `/mnt/dietpi_userdata*`, `/media/root-ro|rw` or as swap, or when it holds the device `findmnt` reports for `/`, `/boot*`, `/usr`, `/var` or `/home`. Its unmounted spare partitions are ignored too.
3. On every other disk, each **unmounted** volume with a supported filesystem (vfat, exfat, ntfs, ext2/3/4, xfs, btrfs, hfsplus) is mounted at `/media/<label>` (label, else UUID, else device name; `-2`, `-3`… if taken). `/media` is already scanned by the USB discovery, so the stick appears in SOURCE within a couple of seconds.
4. Options: `nosuid,nodev,noexec,noatime`; FAT/exFAT/NTFS also get `uid`/`gid` of the user running NauticMixxx and `umask=0022` so exports, ratings and MY SETTINGS can be written. A read-only device, or a volume that refuses read-write (dirty NTFS, journaled HFS+), is mounted read-only.
5. At shutdown, once the decks and library are closed, the volumes **this module mounted** are unmounted and the `/media/<label>` directories it created are removed. Volumes mounted by anything else are left as they are.

Privileges: running as root, `mount`/`umount` are called directly; otherwise through `sudo -n` (stock DietPi gives the `dietpi` user passwordless sudo). Without either, the failure is logged and nothing else changes.

Only `lsblk`, `findmnt`, `mount`, `umount`, `sync`, `mkdir` and `rmdir` are needed. `NAUTICMIXXX_AUTOMOUNT=0` turns the automount off (EJECT keeps working).

The scan happens once, at start-up: a device plugged in later is not mounted by NauticMixxx.
