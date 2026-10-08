from dataclasses import dataclass

from pygame import Color, Rect, Surface, Vector2, draw

from interfaces import UI


@dataclass(slots=True)
class RectOverlay(UI):
    radius: int
    color:  Color
    rect:   Rect
    z:      int

    def draw(self, screen):
        draw.rect(
            screen,
            self.color,
            self.rect,
            border_radius=self.radius,
        )

@dataclass(slots=True)
class SurfaceOverlay(UI):
    surface: Surface
    rect:    Rect
    z:       int
    # position:  Vector2 # TODO: change this to rect

    def __init__(
        self,
        position: Vector2,
        surface:  Surface,
        z: int,
    ):
        self.surface  = surface
        # print(position)
        # print(surface.get_size())
        self.rect     = Rect(position, surface.get_size())
        self.z        = z


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

