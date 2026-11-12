# Display profiles, window mode and waveform styles

NauticMixxx ships five skins of the same RX3 workflow:

| Skin | Native size | Use |
|---|---|---|
| `XDJ_RX3_Mixxx` | 1280x800 | master design |
| `XDJ_RX3_Mixxx_800x600` | 800x600 | 4:3 touch panels |
| `XDJ_RX3_Mixxx_800x480` | 800x480 | 5" / 4.3" wide touch panels (e.g. Waveshare 800x480) |
| `XDJ_RX3_Mixxx_600x480` | 600x480 | small touch panels |
| `XDJ_RX3_Mixxx_480x320` | 480x320 | 3.5" / handheld screens |

All five are fill-window skins: at another window size they scale like the master.
Choose **SCREEN** in SHORTCUT or UTILITY > DISPLAY: the matching skin loads at once,
the window is fitted to it and the choice is the default at the next start.
The same choice can be made at start-up from the command line:

```
nauticmixxx --resolution 800x480
```

Accepted values: `1280x800`, `800x600`, `800x480`, `600x480`, `480x320`. The skin is selected
before the window opens and, like SCREEN, stays the default for the next start. An unknown value
is reported in the log and the configured skin is kept. Combine with `--fullscreen` for a kiosk.

**WINDOW** switches between windowed and fullscreen. **WAVEFORM STYLE** picks the
renderer (OpenGL styles first; SOFTWARE/QT styles for systems without shaders).

The smaller skins are generated: edit `tools/profiles.py` (per-skin scale factors and
QSS overrides) and run `python3 tools/make_skins.py`; do not edit the generated folders.

STORAGE overview thumbnails come from stored waveform summaries. Tracks loaded on a deck
are analysed automatically; UTILITY > BROWSER > ANALYZE WAVEFORMS (STORAGE) scans the rest.
