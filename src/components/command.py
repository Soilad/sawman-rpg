from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pygame import Vector2, image

from components.overlay import SurfaceOverlay
from consts import TICKS_PER_CHAR, X_OFFSETS, Signal, font_medium
from func import UIanimation, set_dialog
from Interfaces import UI, ICommandable

if TYPE_CHECKING:
    from structs import World


@dataclass(slots=True)
class DialogueCommand(ICommandable):
    expression: str
    person:     str
    text:       str

    dialogue:   list[UI]
    sprite:     UI
    name:       UI
    emitted:    bool = field(default=False)
    def __init__(
        self,
        expression,
        person,
        text,
        emitted = False,
    ):
        x_offset        = X_OFFSETS.get(person, 625)
        position        = Vector2(x_offset - 30, 440)

        self.expression = expression
        self.person     = person
        self.text       = text
        self.emitted    = emitted

        self.dialogue   = list(set_dialog(
            text,
            font_medium,
            Vector2(425, 440)
        ))
        self.sprite = SurfaceOverlay(
            surface = image.load(
                f"./sprites/faces/{self.person}/{self.expression}.png"
            ).convert_alpha(),
            position = Vector2(0, 0),
            z        = 1,
        )
        self.name = SurfaceOverlay(
            surface  = font_medium.render(self.person, False, (255, 255, 255,)),
            position = position,
            z        = 6,
        )

    def init(self, world: World):
        world.overlays.add(
            {
                self.person: self.sprite,
                "name": self.name,
            }
        )
        world.animator.append(
            UIanimation(
                world.overlays.overlays["textbox"],
                ["rect", "y"],
                540
            )
        )

    def refresh(self, world: World):
        frame = (world.tick - world.initialTicks.enter) // TICKS_PER_CHAR
        print(self.dialogue[min(frame, len(self.dialogue) - 1)])
        world.overlays.overlays["textbox"].children = self.dialogue[min(frame, len(self.dialogue) - 1)]
        world.overlays.overlays["textbox"].update()


@dataclass(slots=True)
class SignalCommand(ICommandable):
    signal:  Signal
    emitted: bool = field(default=False)

    def init(self, world: World):
        world.overlays.clear()

    def refresh(self, world: World):
        world.animator.append(
            UIanimation(
                world.overlays.overlays["textbox"],
                ["rect", "y"],
                720
            )
        )
