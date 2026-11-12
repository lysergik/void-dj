# NETWORK source and Serato drives (patch 0060)

## SOURCE > NETWORK
One row listing every library found on the LAN, each opening like a USB (ARTIST, ALBUM, TRACK, KEY, PLAYLIST, MATCHING, FOLDER, SEARCH). Everything is read-only; IMPORT TO STORAGE works.

* **NauticMixxx** - another NauticMixxx with `UTILITY > NETWORK > SHARE MY LIBRARY: ON`. TCP 48210 (HTTP, read-only) and UDP 48211 (announcements). The library snapshot arrives first, audio and per-track data on demand, cached under the settings folder (`network/`). Optional 4-digit PIN (same on both sides); stale or malformed requests and path traversal are rejected. Tested between two instances on one machine: PIN auth, snapshot, byte-identical audio.
* **Pioneer (Pro DJ Link)** - players announce themselves on UDP 50000; the NFS export of the player's USB/SD slot is read (portmap 111, mountd, NFSv2) and `PIONEER/rekordbox/export.pdb` is parsed like a normal USB. **Tested only against `tools/mock_prolink_player.py`, a simulated player written from the protocol as I understand it, not against real CDJ/XDJ hardware.** Expect adjustments on real devices.

## Serato drives
`_Serato_/database V2` and `_Serato_/Subcrates/*.crate` appear as a read-only USB source (tags, BPM, key, crates as playlists). Cue points and grids are read from the audio files' own tags when a track loads. Tested with a synthetic drive, not with a drive written by Serato DJ.

## Several USB sticks
Each mounted stick gets its own number (USB1, USB2, ...) in SOURCE.
