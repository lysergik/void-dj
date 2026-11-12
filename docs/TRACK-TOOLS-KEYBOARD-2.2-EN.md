# TRACK TOOLS, POWER and keyboard navigation (patch 0051)

## Where things are
The BROWSE header already ends with MENU (UTILITY). Rather than add buttons to crowded track rows, the track edits live in one overlay that uses the same encoder contract as every other tool page (turn selects, press executes, hold/BACK returns):

* TRACK TOOLS: UTILITY > BROWSER > TRACK TOOLS, the keyboard Ctrl+F4, controller control `[RX3Browser],track_tools`, or one SHIFT + BROWSE step after MENU on the SB2 preset.
  * TARGET row: press, then turn to choose SELECTED (track highlighted in BROWSE) / DECK 1 / DECK 2.
  * ADD TO CRATE: ● marks crates holding the track; press toggles. NEW CRATE: TAG LIST starts one.
  * ADD TO PLAYLIST: same, plus NEW PLAYLIST (ADD TRACK).
  * BPM: DOUBLE, HALVE, x2/3, x3/4, x4/3, x3/2, LOCK/UNLOCK BPM, UNDO LAST BPM / GRID CHANGE, RESET BEATGRID (asks twice). These are the same operations as the right-click menu of stock Mixxx.
  * COLOR: NO COLOR plus the track colour palette of Preferences, shown in its own tint.
  * USB tracks are read-only; use TAG LIST for them.
* POWER: SHORTCUT title row (between UTILITY and CLOSE), UTILITY > GENERAL > POWER, Ctrl+F10, `[RX3Browser],power`. EXIT closes NauticMixxx. On Linux SLEEP suspends the device (systemctl/loginctl suspend, which is what a single-app Xorg device wants) and SHUTDOWN exits and powers off. Each needs a second press within 4 seconds.

## Keyboard (main window only; dialogs and text fields keep their own keys)
The plain F-keys, Shift+Left/Right and Ctrl+1..4 stay with Mixxx's default keyboard mapping (pitch, load, View menu), so the RX3 layer uses Ctrl+F-keys and Alt+digits.

| Key | Action |
|---|---|
| Up / Down | BROWSE turn (also SHORTCUT, INFO, GRID nudge) |
| Return | BROWSE press (opens BROWSE if closed) |
| Backspace, Shift+Return | BACK |
| Esc | close SHORTCUT / GRID, else BACK |
| Ctrl+F1 | SOURCE |
| Ctrl+F2 | BROWSE <-> PERFORMANCE |
| Ctrl+F3 | SHORTCUT |
| Ctrl+F4 | TRACK TOOLS (from PERFORMANCE it targets the active deck, from BROWSE the highlighted track) |
| Ctrl+F5 | MENU (UTILITY) |
| Ctrl+F6 | GRID mode |
| Ctrl+F7 / F8 / F9 | TAG LIST / PLAYLIST / SEARCH |
| Ctrl+F10 | POWER |
| Shift+Up / Shift+Down | step the header SOURCE, BROWSE, TAG LIST, PLAYLIST, SEARCH, MENU, TRACK TOOLS |
| Alt+1..4 | load the selected track to deck 1..4 |

The keys work without a window manager (single-app Xorg). Other controller presets can bind `[RX3Browser],track_tools`, `power` and `close_tools` (leave a stacked tool page).

Other presets (FLX4, FLX6, Inpulse 500, Roland) reach TRACK TOOLS and POWER through MENU > BROWSER and the SHORTCUT button; bind the controls above for a direct gesture.

Colours appear as a row tint in every browser list, and as a bar on the highlighted row. BPM scaling, lock/undo, colour persistence and EXIT were checked in a real run; suspend and power-off were not executed in the test environment.
