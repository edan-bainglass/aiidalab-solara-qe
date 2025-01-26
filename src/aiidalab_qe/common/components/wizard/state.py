from enum import Enum


class WizardState(Enum):
    FAIL = -1
    INIT = 0
    CONFIGURED = 1
    READY = 2
    ACTIVE = 3
    SUCCESS = 4


STATE_ICONS = {
    "INIT": "\u25cb",
    "READY": "\u25ce",
    "CONFIGURED": "\u25cf",
    "ACTIVE": "\u231b",
    "SUCCESS": "\u2713",
    "FAIL": "\u00d7",
}

BG_COLORS = {
    "INIT": "#eee",
    "READY": "#fcf8e3",
    "CONFIGURED": "#fcf8e3",
    "ACTIVE": "#d9edf7",
    "SUCCESS": "#dff0d8",
    "FAIL": "#f8d7da",
}
