// DDJ-SB2 NauticMixxx RX3 menu navigation.
// Transport, mixer, jogs, pads and effects stay in the stock Mixxx SB2 mapper
// (Pioneer-DDJ-SB2-scripts.js). This file only drives the RX3 browser,
// SOURCE, SHORTCUT and UTILITY screens through the shared encoder contract.
//
//   BROWSE turn              move the selected item (context aware)
//   BROWSE press             enter; 2 s hold = BACK in BROWSE, GRID in PERFORMANCE
//   SHIFT + BROWSE turn      step through the header: SOURCE, BROWSE, TAG LIST,
//                            PLAYLIST, SEARCH, MENU (UTILITY)
//   SHIFT + BROWSE press     BACK; 2 s hold = open/close SHORTCUT
//   LOAD 1 / LOAD 2          load the selected track (RX3 rules: PERFORMANCE
//                            only selects the deck)
//   SHIFT + LOAD 1           SOURCE (closes SHORTCUT first when it is open)
//   SHIFT + LOAD 2           toggle BROWSE <-> PERFORMANCE
var NauticSB2Browser = {};

NauticSB2Browser.sections = ["source", "browse", "tag_list", "playlist", "search", "utility", "track_tools"];
NauticSB2Browser.section = -1;
NauticSB2Browser.menuOpen = false;
// Shift+turn arrives in bursts; one detent per two ticks avoids skipping sections.
NauticSB2Browser.accumulated = 0;

NauticSB2Browser.pulse = function(group, key, value) {
    engine.setValue(group, key, value);
    engine.setValue(group, key, 0);
};

NauticSB2Browser.nativeBrowser = function() {
    return engine.getValue("[RX3Browser]", "enabled") > 0;
};

NauticSB2Browser.isOpen = function() {
    if (Math.round(engine.getValue("[Tab]", "current")) === 1) { return true; }
    // Stock Mixxx skins do not have NauticMixxx's [Tab] page.
    return !NauticSB2Browser.nativeBrowser() &&
        engine.getValue("[Skin]", "show_maximized_library") > 0;
};

NauticSB2Browser.open = function() {
    if (NauticSB2Browser.isOpen()) { return false; }
    engine.setValue("[XDJ_RX3]", "search_active", 0);
    engine.setValue("[Tab]", "library", 1);
    engine.setValue("[Skin]", "show_maximized_library", 1);
    if (NauticSB2Browser.nativeBrowser()) {
        NauticSB2Browser.pulse("[RX3Browser]", "open", 1);
    } else {
        engine.setValue("[Library]", "focused_widget", 2);
    }
    return true;
};

NauticSB2Browser.shortcutVisible = function() {
    return engine.getValue("[RX3Shortcut]", "visible") > 0;
};

NauticSB2Browser.view = function(_channel, _control, value) {
    if (!value) { return; }
    NauticSB2Browser.section = -1;
    if (NauticSB2Browser.shortcutVisible()) { NauticSB2Browser.pulse("[RX3Shortcut]", "toggle", 1); }
    if (NauticSB2Browser.open()) { return; }
    engine.setValue("[Skin]", "show_maximized_library", 0);
    // Page triggers are latched; the stack clears the previous page itself.
    // Resetting overview to zero would hide PERFORMANCE and reopen BROWSER.
    engine.setValue("[Tab]", "overview", 1);
};

NauticSB2Browser.source = function(_channel, _control, value) {
    if (!value) { return; }
    if (NauticSB2Browser.shortcutVisible()) {
        NauticSB2Browser.pulse("[RX3Shortcut]", "toggle", 1);
        return;
    }
    NauticSB2Browser.section = 0;
    NauticSB2Browser.open();
    if (NauticSB2Browser.nativeBrowser()) {
        NauticSB2Browser.pulse("[RX3Browser]", "source", 1);
    } else {
        engine.setValue("[Library]", "focused_widget", 2);
    }
};

NauticSB2Browser.turn = function(_channel, _control, value) {
    if (!value || !NauticSB2Browser.isOpen()) { return; }
    var direction = value > 0x3f ? -1 : 1;
    if (NauticSB2Browser.nativeBrowser()) {
        NauticSB2Browser.pulse("[RX3Browser]", "move", direction);
    } else {
        NauticSB2Browser.pulse("[Library]", direction < 0 ? "MoveUp" : "MoveDown", 1);
    }
};

NauticSB2Browser.enter = function(_channel, _control, value) {
    if (!value || NauticSB2Browser.open()) { return; }
    if (NauticSB2Browser.nativeBrowser()) {
        NauticSB2Browser.pulse("[RX3Browser]", "enter", 1);
    } else {
        NauticSB2Browser.pulse("[Library]", "GoToItem", 1);
    }
};

NauticSB2Browser.back = function(_channel, _control, value) {
    if (!value || NauticSB2Browser.open()) { return; }
    if (NauticSB2Browser.nativeBrowser()) {
        NauticSB2Browser.pulse("[RX3Browser]", "back", 1);
    } else {
        NauticSB2Browser.pulse("[Library]", "MoveLeft", 1);
    }
};

// Step the BROWSE header (SOURCE ... MENU, TRACK TOOLS) with SHIFT + BROWSE turn.
NauticSB2Browser.stepSection = function(direction) {
    if (!NauticSB2Browser.nativeBrowser() || NauticSB2Browser.shortcutVisible() ||
            engine.getValue("[RX3Info]", "visible") > 0) {
        return;
    }
    var wasClosed = NauticSB2Browser.open();
    var count = NauticSB2Browser.sections.length;
    var next = wasClosed ? 0 :
        (NauticSB2Browser.section < 0 ? 1 : NauticSB2Browser.section + direction);
    next = Math.max(0, Math.min(count - 1, next));
    if (next === NauticSB2Browser.section && !wasClosed) { return; }
    // MENU (UTILITY) and TRACK TOOLS are stacked pages; close them before moving on.
    if (NauticSB2Browser.menuOpen && next !== NauticSB2Browser.section) {
        NauticSB2Browser.pulse("[RX3Browser]", "close_tools", 1);
        NauticSB2Browser.menuOpen = false;
    }
    NauticSB2Browser.section = next;
    var name = NauticSB2Browser.sections[next];
    if (name === "utility" || name === "track_tools") { NauticSB2Browser.menuOpen = true; }
    NauticSB2Browser.pulse("[RX3Browser]", name, 1);
};

NauticSB2Browser.shiftTurn = function(_channel, _control, value) {
    if (!value) { return; }
    NauticSB2Browser.accumulated += value > 0x3f ? -1 : 1;
    if (Math.abs(NauticSB2Browser.accumulated) < 2) { return; }
    var direction = NauticSB2Browser.accumulated < 0 ? -1 : 1;
    NauticSB2Browser.accumulated = 0;
    NauticSB2Browser.stepSection(direction);
};

// Context-aware press is completed on release, after the hold is classified.
NauticSB2Browser.shortPress = NauticSB2Browser.enter;
NauticSB2Browser.originalTurn = NauticSB2Browser.turn;
NauticSB2Browser.enter = function(channel, control, value, status, group) {
    NauticRX3Encoder.press(NauticSB2Browser, value, status || 0x90, false);
};
NauticSB2Browser.shortcut = function(channel, control, value, status, group) {
    NauticRX3Encoder.press(NauticSB2Browser, value, status || 0x90, true);
    // After the release of a short shifted press (no 2 s hold, no turn): BACK.
    var down = value > 0 && ((status || 0x90) & 0xF0) !== 0x80;
    if (!down && !NauticRX3Encoder.pressed && !NauticRX3Encoder.consumed &&
            !NauticRX3Encoder.moved && NauticSB2Browser.isOpen() &&
            !NauticSB2Browser.shortcutVisible() &&
            engine.getValue("[RX3Info]", "visible") <= 0) {
        NauticSB2Browser.back(0, 0, 127);
    }
};
NauticSB2Browser.turn = function(channel, control, value, status, group) {
    NauticRX3Encoder.turn(NauticSB2Browser, channel, control, value, status, group);
};
