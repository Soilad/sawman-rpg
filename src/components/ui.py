from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pygame import Color, Rect, Surface, Vector2, draw, math

from consts import COLOR_PRIMARY, COLOR_SECONDARY, COLOR_TERTIARY, AlignUI, DirectionUI
from func import objectAnimation, lerp
from Interfaces import UI
from structs import BorderRadius

if TYPE_CHECKING:
    from structs import World


@dataclass(slots=True)
class ButtonUI(UI):
    color: Color
    outlineColor: Color
    borderRange: tuple[int, int]
    radius: BorderRadius
    onClick: Callable[[World], None] = field(default=lambda x: print("test"))
    _width: float = field(default=0)
    _transparency: float = field(default=0)

    def __post_init__(self):
        self._width = self.borderRange[0]
        # self.children = []
        self.update()

    def update(self):
        for surface in self.children:
            match surface.align[0]:
                case AlignUI.START:
                    surface.rect.left = self.rect.left
                case AlignUI.CENTER:
                    surface.rect.centerx = self.rect.centerx
                case AlignUI.END:
                    surface.rect.right = self.rect.right
            match surface.align[1]:
                case AlignUI.START:
                    surface.rect.top = self.rect.top
                case AlignUI.CENTER:
                    surface.rect.centery = self.rect.centery
                case AlignUI.END:
                    surface.rect.bottom = self.rect.bottom
            # surface.rect = surface.rect.clip(self.rect)
            # if hasattr(surface, "surface"):
            #     surface.surface.set_clip(surface.rect)

    def draw(self, screen):
        draw.rect(screen,
                  self.color,
                  self.rect,
                  border_top_left_radius=self.radius.upperLeft,
                  border_top_right_radius=self.radius.upperRight,
                  border_bottom_left_radius=self.radius.lowerLeft,
                  border_bottom_right_radius=self.radius.lowerRight)

        for surface in self.children:
            surface.draw(screen)

        _width = int(self._width)
        if _width:
            draw.rect(screen,
                      self.outlineColor,
                      self.rect,
                      border_top_left_radius=self.radius.upperLeft,
                      border_top_right_radius=self.radius.upperRight,
                      border_bottom_left_radius=self.radius.lowerLeft,
                      border_bottom_right_radius=self.radius.lowerRight,
                      width=_width)

    def onHover(
        self,
        world: World,
    ) -> bool:
        hovered = self.rect.collidepoint(world.mouse.get_pos())
        if self.id.int + hash("_width") not in world.animator:
            if hovered:
                objectAnimation(world, self, ["_width"],
                                self.borderRange[1] << world.clicked)
            else:
                objectAnimation(world, self, ["_width"],
                                self.borderRange[0] << world.clicked)
        return hovered

    # def onClick(self, world: World):
    #     print(world.mouse.get_pressed())


@dataclass(slots=True)
class BoxUI(UI):
    color: Color
    outlineColor: Color
    borderRange: tuple[int, int]
    radius: BorderRadius
    padding: Rect
    direction: DirectionUI

    _paddedRect: Rect = field(default_factory=Rect)
    _scrollOffset: Vector2 = field(default_factory=Vector2)
    _width: float = field(default=0)

    def __post_init__(self):
        self.update()

    def _in_bounds(self, rect: Rect) -> bool:
        clipped = rect.clip(self.rect)
        return (rect.h == clipped.h) and (rect.w == clipped.w)

    def update(self):
        self._paddedRect = Rect(
            self.rect.x + self.padding.x,
            self.rect.y + self.padding.y,
            self.rect.w - (self.padding.x << 1),
            self.rect.h - (self.padding.y << 1),
        )

        for i in range(len(self.children)):
            child = self.children[i]

            match self.direction:
                case DirectionUI.HORIZONTAL:
                    child.rect.x = self._paddedRect.x - self._scrollOffset.x
                    child.rect.y = self._paddedRect.y
                    child.rect.x += (self.padding.w + child.rect.w) * i
                    child.rect.h = self._paddedRect.h
                case DirectionUI.VERTICAL:
                    child.rect.x = self._paddedRect.x
                    child.rect.y = self._paddedRect.y - self._scrollOffset.y
                    child.rect.y += (self.padding.h + child.rect.h) * i
                    child.rect.w = self._paddedRect.w

            child.update()

    def draw(self, screen):
        draw.rect(
            screen,
            self.color,
            self.rect,
            border_top_left_radius=self.radius.upperLeft,
            border_top_right_radius=self.radius.upperRight,
            border_bottom_left_radius=self.radius.lowerLeft,
            border_bottom_right_radius=self.radius.lowerRight,
        )

        _width = int(self._width)
        if _width:
            draw.rect(screen,
                      self.outlineColor,
                      self.rect,
                      border_top_left_radius=self.radius.upperLeft,
                      border_top_right_radius=self.radius.upperRight,
                      border_bottom_left_radius=self.radius.lowerLeft,
                      border_bottom_right_radius=self.radius.lowerRight,
                      width=_width)
        for child in self.children:
            if self._in_bounds(child.rect):
                child.draw(screen)

    def onHover(
        self,
        world: World,
    ) -> bool:
        hovered = self.rect.collidepoint(world.mouse.get_pos())
        if hovered and world.scrollDirection != Vector2(0, 0):
            self._scrollOffset += 100 * world.scrollDirection
            self._scrollOffset.x = math.clamp(
                self._scrollOffset.x,
                -len(self.children) *
                (self.padding.h if self.direction == DirectionUI.VERTICAL else
                 self.padding.w),
                0,
            )
            self._scrollOffset.y = max(0, self._scrollOffset.y)
            world.scrollDirection = Vector2(0, 0)

        self.update()
        for child in self.children:
            # if not self.rect.collidepoint(child.rect.center):
            #     return False
            child_hovered = child.onHover(world)
            if child_hovered and world.clicked:
                world.clicked = False
                if self._in_bounds(child.rect) and hasattr(child, "onClick"):
                    child.onClick(world)
        return hovered

    # def onClick(self, world: World):
    #     print(world.mouse.get_pressed())


@dataclass(slots=True)
class SurfaceOverlay(UI):
    surface: Surface
    position: Vector2 = field(default_factory=Vector2)

    def __post_init__(self):
        self.children = []
        self.rect = Rect(self.position, self.surface.size)

    def draw(self, screen):
        screen.blit(self.surface, self.rect.topleft)


# if __name__ == "__main__":
