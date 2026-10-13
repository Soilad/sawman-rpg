from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pygame import Rect, Vector2, image

from components.ui import ButtonUI, SurfaceOverlay
from consts import (
    COLOR_PRIMARY,
    COLOR_SECONDARY,
    COLOR_TERTIARY,
    TICKS_PER_CHAR,
    X_OFFSETS,
    AlignUI,
    EntityType,
    Signal,
    font_medium,
)
from func import UIanimation, objectAnimation, set_dialog
from Interfaces import UI, ICommandable
from structs import BorderRadius

if TYPE_CHECKING:
    from structs import World


@dataclass(slots=True)
class DialogueCommand(ICommandable):
    expression: str
    person: str
    text: str

    _sprite: SurfaceOverlay = field(default=None)
    _name: SurfaceOverlay = field(default=None)
    _dialogue: list[list[SurfaceOverlay]] = field(default_factory=list)
    _nameAlignment: Vector2 = field(default_factory=Vector2)

    def __post_init__(self):

        self._dialogue = list(
            set_dialog(self.text, font_medium, Vector2(425, 440)))
        self._sprite = SurfaceOverlay(
            image.load(f"./sprites/faces/{self.person}/{self.expression}.png").
            convert_alpha(), )
        self._name = SurfaceOverlay(font_medium.render(self.person, False,
                                                       COLOR_PRIMARY),
                                    align=(AlignUI.CENTER, AlignUI.CENTER))
        self.signal = Signal.OK

    def init(self, world: World) -> bool:
        if not world.playerData.stop:
            world.playerData.stop = True

        world.ui.add({
            self.person: self._sprite,
        })
        world.ui.overlays["name"].children = [self._name]

        x_offset = X_OFFSETS.get(self.person, 625)
        objectAnimation(world, world.ui.overlays["textbox"], ["rect", "y"],
                        520)
        objectAnimation(world, world.ui.overlays["name"], ["rect", "y"], 480)
        objectAnimation(world, world.ui.overlays["name"], ["rect", "centerx"],
                        x_offset)
        return True

    def refresh(self, world: World):
        frame = (world.tick - world.initialTicks.enter) // TICKS_PER_CHAR
        world.ui.overlays["textbox"].children = self._dialogue[min(
            frame,
            len(self._dialogue) - 1)]
        world.ui.overlays["textbox"].update()


@dataclass(slots=True)
class MoveRoomCommand(ICommandable):
    levelID: int
    newPosition: Vector2

    def init(self, world: World) -> bool:
        if world.inDoor:
            return False
        playerID = next(
            entity for entity in world.entityIDs
            if world.levels[world.level][entity].type == EntityType.PLAYER)
        playerEntity = world.levels[world.level][playerID]
        playerEntity.movement.position = Vector2(self.newPosition)
        world.playerData.interactionPoint = Vector2(self.newPosition)
        world.nextLevel = self.levelID
        world.inDoor = True
        self.reset()

    def refresh(self, world: World):
        pass


@dataclass(slots=True)
class SignalCommand(ICommandable):

    def init(self, world: World):
        if world.playerData.stop:
            world.playerData.stop = False
        world.ui.clear()
        objectAnimation(world, world.ui.overlays["textbox"], ["rect", "y"],
                        720)
        objectAnimation(world, world.ui.overlays["name"], ["rect", "y"], 720)
        objectAnimation(world, world.ui.overlays["name"], ["rect", "centerx"],
                        640)
        return True

    def refresh(self, world: World):
        pass
