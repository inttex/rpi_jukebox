import enum


class COMMAND(enum.Enum):
    PAUSE_PLAY = enum.auto()
    VOL_INC = enum.auto()
    VOL_DEC = enum.auto()
    STOP_DEVICE = enum.auto()
    STOP_DEVICE_20_MIN = enum.auto()
    NEXT = enum.auto()
    PREV = enum.auto()
    STOP_VIEW = enum.auto()
