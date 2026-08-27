from enum import Enum, auto

class AppState(Enum):
    INPUT_COLORS = auto()
    CHOOSE_MODE = auto()
    ROTATE = auto()
    GUIDE = auto()