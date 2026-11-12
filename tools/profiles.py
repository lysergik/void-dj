"""Design parameters of the derived NauticMixxx skins (see make_skins.py)."""
PROFILES = {
    "800x600": {
        "dir": "XDJ_RX3_Mixxx_800x600", "size": (800, 600),
        "kx": 0.66, "ky": 0.72, "kl": 0.70, "kf": 0.78, "font_floor": 9,
        "ui": 0.66, "topbar_wrap": 32,
        "sizes": {}, "hide": [], "setvars": {"ovh": 46, "ovwf": 42}, "qss": """#WaveformInfoSource { font-size: 15px; }
#RX3StatusTab { font-size: 12px; }
/* 2.2: timers and BPM readouts sized to their boxes (fits 100+ minute tracks) */
#RX3LibraryDeckTime { font-size: 18px; }
#RX3LibraryDeckBpm1, #RX3LibraryDeckBpm2 { font-size: 21px; }
#DeckTrackTime { font-size: 25px; }
#DeckHeaderBpmValue { font-size: 20px; }
""",
    },
    "600x480": {
        "dir": "XDJ_RX3_Mixxx_600x480", "size": (600, 480),
        "kx": 0.5, "ky": 0.58, "kl": 0.54, "kf": 0.66, "font_floor": 9,
        "ui": 0.5, "topbar_wrap": 28,
        "sizes": {}, "hide": [], "setvars": {"ovh": 38, "ovwf": 34}, "qss": """
/* readout row: text must fit its fixed slots */
#DeckTrackTime { font-size: 20px; }
#TrackTimeContainer { max-width: 76px; padding: 1px 1px 0 2px; }
#DeckTempoPercent, #BPMPercent { font-size: 12px; }
#DeckTempoCaption { font-size: 8px; min-width: 0; }
#TimeLabelRemain, #TimeLabelSlash, #TimeLabelTime { font-size: 8px; }
#DeckCueLabel, #DeckAutoCueLabel { font-size: 7px; }
#DeckHeaderBpmValue { font-size: 14px; }
#DeckHeaderBpmTitle { font-size: 7px; min-width: 14px; max-width: 14px; }
#TrackNoValue, #TrackNoQuantizeValue { font-size: 14px; }
#DeckTitle { font-size: 14px; }
#TrackNoCaption, #TrackNoPlayMode, #TrackNoQuantize { font-size: 7px; }
#BpmMaster { font-size: 6px; }
#DeckTrackTime { font-size: 19px; }
#TimeLabelRemain, #TimeLabelSlash, #TimeLabelTime { font-size: 7px; }
#DeckTempoCaption { font-size: 7px; }
#WaveformInfoSource { font-size: 11px; }
#RX3StatusTab { font-size: 8px; padding: 0; }
#RX3LibraryDeckTime { font-size: 14px; }
#RX3LibraryDeckBpm1, #RX3LibraryDeckBpm2 { font-size: 17px; }
""",
    },
    # 800x480 (Waveshare 4.3" class panels, 5" 800x480 DSI/HDMI screens).
    # Horizontal scale from 800x600 (same 800 px width), vertical scale, text
    # and native-widget density from 600x480 (same 480 px height): fixed widths
    # get the room of the wider 800 px canvas while every height, font size and
    # touch-row length stays exactly as proven on 480 px tall screens, so
    # nothing that fits 600x480 vertically can overflow here.
    "800x480": {
        "dir": "XDJ_RX3_Mixxx_800x480", "size": (800, 480),
        "kx": 0.66, "ky": 0.58, "kl": 0.54, "kf": 0.66, "font_floor": 9,
        "ui": 0.5, "topbar_wrap": 28,
        "sizes": {}, "hide": [], "setvars": {"ovh": 38, "ovwf": 34}, "qss": None,
    },
    "480x320": {
        "dir": "XDJ_RX3_Mixxx_480x320", "size": (480, 320),
        "kx": 0.375, "ky": 0.4, "kl": 0.39, "kf": 0.56, "font_floor": 9,
        "ui": 0.39, "topbar_wrap": 22,
        "sizes": {}, "hide": [], "setvars": {"ovh": 30, "ovwf": 26}, "qss": """
/* readout row: text must fit its fixed slots */
#DeckTrackTime { font-size: 15px; }
#TrackTimeContainer { max-width: 56px; padding: 1px 1px 0 2px; }
#DeckTempoPercent, #BPMPercent { font-size: 9px; }
#DeckTempoCaption { font-size: 8px; min-width: 0; }
#TimeLabelRemain, #TimeLabelSlash, #TimeLabelTime { font-size: 8px; }
#DeckCueLabel, #DeckAutoCueLabel { font-size: 7px; }
#DeckHeaderBpmValue { font-size: 11px; }
#DeckHeaderBpmTitle { font-size: 7px; min-width: 14px; max-width: 14px; }
#TrackNoValue, #TrackNoQuantizeValue { font-size: 11px; }
#DeckTitle { font-size: 11px; }
#TrackNoCaption, #TrackNoPlayMode, #TrackNoQuantize { font-size: 6px; }
#BpmMaster { font-size: 5px; }
#DeckTrackTime { font-size: 13px; }
#TimeLabelRemain, #TimeLabelSlash, #TimeLabelTime { font-size: 6px; }
#DeckTempoCaption { font-size: 6px; }
#DeckCueLabel, #DeckAutoCueLabel { font-size: 6px; }
#DeckHeaderBpmTitle { font-size: 6px; min-width: 13px; max-width: 13px; }
#DeckTempoCaption { font-size: 5px; }
#WaveformInfoSource { font-size: 8px; }
#RX3StatusTab { font-size: 6px; padding: 0; }
#RX3LibraryDeckTime { font-size: 11px; }
#RX3LibraryDeckBpmCaption, #RX3LibraryMaster { font-size: 6px; padding: 0 1px; }
#RX3LibraryDeckBpmCaption { min-width: 12px; max-width: 12px; }
#RX3LibraryDeckBpm1, #RX3LibraryDeckBpm2 { font-size: 13px; }
""",
    },
}

# 800x480 shares the 480 px-tall text/readout overrides of 600x480.
PROFILES["800x480"]["qss"] = PROFILES["600x480"]["qss"]
