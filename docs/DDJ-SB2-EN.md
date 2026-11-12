# DDJ-SB2 NauticMixxx RX3 mapping

`controllers/Pioneer_DDJ_SB2_RX3/` is the stock Mixxx **Pioneer DDJ-SB2** mapping (decks, mixer, jogs, pads, effects, 4-deck layers: unchanged) plus NauticMixxx RX3 menu navigation. Select **Pioneer DDJ-SB2 - NauticMixxx RX3** in Preferences > Controllers. Copy the folder's files into your Mixxx `controllers` folder first if your build does not install them (the Linux build installs them with the app).

## Menu navigation

The SB2 sends separate MIDI notes for SHIFT + BROWSE and SHIFT + LOAD, so no shift state is tracked.

| Control | PERFORMANCE | BROWSE / SOURCE | SHORTCUT / INFO |
| --- | --- | --- | --- |
| BROWSE turn | nothing | move the selected item | move row focus / change option |
| BROWSE press | open BROWSE | enter the item | edit / activate focused button |
| BROWSE 2 s hold | toggle GRID | BACK | no action |
| SHIFT + BROWSE turn | open BROWSE at SOURCE, then step the header | step the header | ignored |
| SHIFT + BROWSE press | nothing | BACK | no action |
| SHIFT + BROWSE 2 s hold | open SHORTCUT | open SHORTCUT | close SHORTCUT |
| LOAD 1 / 2 (3 / 4 on the deck-3/4 layer) | select that deck only | load the selected track | blocked |
| SHIFT + LOAD 1 | open SOURCE | open SOURCE | close SHORTCUT |
| SHIFT + LOAD 2 | open BROWSE | back to PERFORMANCE | close SHORTCUT, then toggle |

SHIFT + BROWSE turn steps the BROWSE header in order **SOURCE, BROWSE, TAG LIST, PLAYLIST, SEARCH, MENU (UTILITY), TRACK TOOLS**; two encoder ticks make one step so a quick flick does not skip sections. Leaving MENU or TRACK TOOLS closes it. TRACK TOOLS (crate, playlist, BPM, colour of the selected or deck track) and POWER (`[RX3Browser],power`) can also be bound to any other control. UTILITY and the settings are reached from SHORTCUT (SHIFT + BROWSE hold) or from the MENU header item.

PLAY on decks 1 and 2 uses the RX3 VINYL SPEED ADJUST gradual stop; SHIFT + PLAY keeps the stock reverse-play.

## MIDI used

| Control | Message |
| --- | --- |
| BROWSE turn / SHIFT + BROWSE turn | CC `0xB6 0x40` / `0xB6 0x64` |
| BROWSE press / SHIFT + BROWSE press | Note `0x96 0x41` / `0x96 0x42` |
| LOAD 1, 2, 3, 4 | Notes `0x96 0x46`, `0x47`, `0x48`, `0x49` |
| SHIFT + LOAD (left) / (right) | Notes `0x96 0x58`, `0x60` / `0x96 0x59`, `0x61` |

The stock SB2 mapping used the browse press for preview and SHIFT + LOAD for effect/sampler views; those assignments are replaced. Everything else in the original XML is unchanged.

## Status

`scripts/test-sb2-rx3-navigation.js` runs 15 gesture scenarios against a mock engine. The mapping has not been tried on a physical DDJ-SB2 or against the running RX3 UI; verify SHIFT + BROWSE hold timing, the header stepping and LED behavior before a live set. Based on the Mixxx DDJ-SB2 mapping by Be and Michael Stahl (DG3NEC), GPL.
