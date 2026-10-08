from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pygame import Color, Rect, Vector2, image

from components.overlay import RectOverlay, SurfaceOverlay
from consts import TICKS_PER_CHAR, X_OFFSETS, Signal, font_medium
from func import lerp, set_dialog
from interfaces import Command

if TYPE_CHECKING:
    from structs import World


@dataclass(slots=True)
class DialogueCommand(Command):
    expression: str
    person:     str
    text:       str

    dialogue:   list[SurfaceOverlay]
    sprite:     SurfaceOverlay
    name:       SurfaceOverlay
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
        world.overlays.update()

    def refresh(self, world: World):
        world.overlays.overlays["textbox"].rect.y = lerp(
            world.overlays.overlays["textbox"].rect.y,
            440
        )
        frame = (world.tick - world.initialTicks.enter) // TICKS_PER_CHAR
        world.overlays.add(
            {
                "text": self.dialogue[min(frame, len(self.dialogue) - 1)],
            }
        )

@dataclass(slots=True)
class SignalCommand(Command):
    signal:  Signal
    emitted: bool = field(default=False)

    def init(self, world: World):
        world.overlays.clear()

    def refresh(self, world: World):
        world.overlays.overlays["textbox"].rect.y = (
            world.overlays.overlays["textbox"].rect.y + 720
        ) >> 1
