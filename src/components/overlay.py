from dataclasses import dataclass

from pygame import Color, Rect, Surface, Vector2, draw

from consts import AlignUI
from Interfaces import UI


class RectOverlay(UI):
    radius: int
    color:  Color
    # rect:   Rect


    def draw(self, screen):
        draw.rect(
            screen,
            self.color,
            self.rect,
            border_radius=self.radius,
        )

class SurfaceOverlay(UI):
    surface: Surface
    def __init__(
        self,
        position: Vector2,
        surface:  Surface,
        z: int,
        align:  tuple[AlignUI, AlignUI] = (AlignUI.START, AlignUI.START)
    ):
        self.surface  = surface
        # print(position)
        # print(surface.get_size())
        self.rect     = Rect(position, surface.get_size())
        self.z        = z
        self.align    = align


    def draw(self, screen):
        screen.blit(
            self.surface,
            self.rect.topleft
        )
        draw.circle(
            screen,
            (255, 0, 255),
            self.rect.topleft,
            10,
        )

