from pygame import Color, draw

from Interfaces import UI


class RectOverlay(UI):
    radius: int
    color: Color

    # rect:   Rect

    def draw(self, screen):
        draw.rect(
            screen,
            self.color,
            self.rect,
            border_radius=self.radius,
        )
