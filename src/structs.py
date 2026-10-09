from dataclasses import dataclass, field
from queue import Queue

from pygame import Vector2
from pygame.key import ScancodeWrapper

from components import *
from consts import EntityType


@dataclass(slots=True)
class Entity:
    type:       EntityType
    collision:  ICollidable
    movement:   IMovable
    interact:   IInteractable
    render:     IRenderable
    id:         int

@dataclass(slots=True)
class InitialTicks:
    enter:     int = field(default=0)
    click:     int = field(default=0)
    interact:  int = field(default=0)
    inventory: int = field(default=0)

@dataclass(slots=True)
class BorderRadius:
    upperLeft:  int = field(default=0)
    upperRight: int = field(default=0)
    lowerLeft:  int = field(default=0)
    lowerRight: int = field(default=0)
    def __init__(self, *args):
        match len(args):
            case 1:
                self.upperLeft  = args[0]
                self.lowerRight = args[0]
                self.upperRight = args[0]
                self.lowerLeft  = args[0]
            case 2:
                self.upperLeft  = args[0]
                self.lowerRight = args[0]
                self.upperRight = args[1]
                self.lowerLeft  = args[1]
            case 4:
                self.upperLeft  = args[0]
                self.lowerRight = args[1]
                self.upperRight = args[2]
                self.lowerLeft  = args[3]

@dataclass(slots=True)
class PlayerData:
    walkingDirection : int            = field(default_factory=int)
    walkingFrame     : int            = field(default_factory=int)
    interactionPoint : Vector2        = field(default_factory=Vector2)
    deltaPosition    : Vector2        = field(default_factory=Vector2)
    positions        : Queue[Vector2] = field(default_factory=Queue)
    stop             : bool           = field(default=False)

@dataclass(slots=True)
class Overlays:
    uiKeys: list[str]
    overlays: dict[str, UI]
    keys: list[str]

    def __init__(self, overlays: dict[str, UI]):
        self.uiKeys   = list(overlays.keys())
        self.overlays = overlays
        self.keys     = self.uiKeys

    def update(self) -> None:
        # self.overlays.update(self.active)
        self.keys.sort(key=lambda x: self.overlays[x].z)

    def add(self, overlays: dict[str, UI]) -> None:
        self.keys = list(
            set(
                self.keys 
                + list(overlays.keys())
            )
        )
        self.overlays.update(overlays)
        self.update()

    def clear(self):
        for key in self.keys:
            if key not in self.uiKeys:
                del self.overlays[key]

        self.keys = list(self.uiKeys)

    # def clear(self) -> None:
    #     print("before")
    #     print(self.overlays)
    #     self.overlays = self.active
    #     print("after")
    #     print(self.overlays)
    #     print("--------------")

@dataclass(slots=True)
class World:
    showInventory: bool
    commandIndex:  int
    initialTicks:  InitialTicks
    playerData:    PlayerData
    overlays:      Overlays
    animator:      list[Callable[[World], bool]]
    clicked:       bool
    levels:        list[list[Entity]]
    level:         int
    mouse:         type
    keys:          ScancodeWrapper
    tick:          int
