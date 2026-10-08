from enum import Enum, Flag, auto

from pygame import font


class CollisionType(Flag):
    NO_OBSTACLE = auto()
    VOLUNTARY   = auto()
    OBSTACLE    = auto()
    INTERACT    = auto()

class EntityType(Flag):
    PLAYER    = auto()
    ROOM      = auto()
    ENTITY    = auto()

class Signal(Enum):
    CLEAR_COMMANDS = auto()
    OK             = auto()

class DirectionUI(Flag):
    HORIZONTAL = auto()
    VERTICAL   = auto()

class AlignUI(Flag):
    START  = auto()
    CENTER = auto()
    END    = auto()

font.init()
font_medium = font.Font("./ui/Soilad.ttf", 48)
FONT_ALIASED = True
X_OFFSETS = {
    "sawman":    200,
    "zweistein": 850
}
TICKS_PER_CHAR = 3
