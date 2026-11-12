# MIXMAN sticks (patches 0056, 0057)

`mixman` (the Rust library manager/exporter for Mixxx) writes a stick with
`MIXMAN/library.sqlite`, `MIXMAN/analysis/<id>` and `MIXMAN/Contents/<Artist>/<file>`
(see mixman's `FORMAT.md`, format version 1). NauticMixxx handles such a stick in two ways.

## As a SOURCE

Plug the stick in (it appears under `/media/<user>/` like a Rekordbox USB). It shows in SOURCE
as `USB1`/`USB2` with `Type: MIXMAN`. The stick is projected into the same runtime catalog as a
Rekordbox USB, so ARTIST, ALBUM, TRACK, KEY, GENRE, PLAYLIST (mixman playlists, then the crates
listed as `name (crate)`), MATCHING, FOLDER and SEARCH work, and tracks load to the decks with
their tags, key, Mixxx beat grid (grid locked state included), hot cues/loops/main cue with
colours, and the stored waveform. The browser PREVIEW column draws the stored waveform summary.

Editing (patch 0057): beat grid, BPM lock, hot cues/loops, main cue, colour and rating can be
changed and are written back to `MIXMAN/library.sqlite` in one transaction. Use TRACK TOOLS >
BPM / COLOR (saved at once), the INFO panel's `SAVE CUES / LOOPS / GRID TO USB`, or UTILITY >
MEMORY CUES. Audio and tags are never touched. Not representable on a stick, so not saved:
extra memory cues beyond the main cue. Crates/playlists on the stick stay read-only (ADD TO
CRATE/PLAYLIST are refused for stick tracks). Edit the stick on a writable mount only.

## IMPORT TO STORAGE

* SOURCE: select the stick, then `IMPORT TO STORAGE` (the button replaces MY SETTINGS MENU).
* UTILITY > BROWSER > `IMPORT MIXMAN STICK TO STORAGE`.

Audio is copied to `~/Music/MIXMAN` (setting `[RX3Import] destination`) keeping the artist
folders; tags, rating, colour, key, beat grid, hot cues, loops, main cue, crates and
playlists are added to the STORAGE library, one track per event-loop turn so the audio engine
stays live. Existing tracks (same destination file) are left untouched, crates/playlists are
merged by name, so importing twice is harmless. New tracks are queued for waveform analysis.

Verified with a stick written by the real mixman 0.1.0: 5 tracks, 2 crates and 1 playlist
imported with identical BPM, key, beat grid bytes, cue positions/labels/colours.
