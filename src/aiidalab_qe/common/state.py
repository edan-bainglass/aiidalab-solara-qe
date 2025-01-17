from enum import Enum


class State(Enum):
    FAIL = -1
    INIT = 0
    CONFIGURED = 1
    READY = 2
    ACTIVE = 3
    SUCCESS = 4


STATE_ICONS = {
    State.INIT: "\u25cb",
    State.READY: "\u25ce",
    State.CONFIGURED: "\u25cf",
    State.ACTIVE: "\u231b",
    State.SUCCESS: "\u2713",
    State.FAIL: "\u00d7",
}

BG_COLORS = {
    State.INIT: "#eee",
    State.READY: "#fcf8e3",
    State.CONFIGURED: "#fcf8e3",
    State.ACTIVE: "#d9edf7",
    State.SUCCESS: "#dff0d8",
    State.FAIL: "#f8d7da",
}
