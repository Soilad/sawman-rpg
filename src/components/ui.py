from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from pygame import Color, Rect, Surface, draw

from consts import AlignUI, DirectionUI
from func import lerp
from Interfaces import UI
from structs import BorderRadius

if TYPE_CHECKING:
    from structs import World


class ButtonUI(UI):
    outlineColor: Color
    onClick:      Callable[[World], None]
    maxWidth:     int
    radius:       BorderRadius
    color:        Color
    rect:         Rect
    z:            int
    align:        tuple[AlignUI, AlignUI]
    _width:       float = 0

    def __init__(
        self,
        outlineColor: Color,
        onClick:      Callable[[World], None],
        maxWidth:     int,
        radius:       BorderRadius,
        color:        Color,
        rect:         Rect,
        z:            int,
        surfaces:     list[UI]|None           = None, # DEAR GOD DONT MODIFY THE SURFACES PARAM
        align:        tuple[AlignUI, AlignUI] = (AlignUI.START, AlignUI.CENTER),
        _width:       float                   = 0,
    ):
        if surfaces is None:
            surfaces = []
        self.outlineColor: Color               = outlineColor
        self.onClick:  Callable[[World], None] = onClick
        self.maxWidth: int                     = maxWidth
        self.surfaces: list[UI]                = surfaces
        self.radius:   BorderRadius            = radius
        self.color:    Color                   = color
        self.rect:     Rect                    = rect
        self.z:        int                     = z
        self.align:    tuple[AlignUI, AlignUI] = align
        self._width:   float                   = _width

        self.update()

    def update(self):
        for surface in self.surfaces:

            match surface.align[0]:
                case AlignUI.START:
                    surface.rect.left    = self.rect.left
                case AlignUI.CENTER:
                    surface.rect.centerx = self.rect.centerx
                case AlignUI.END:
                    surface.rect.right   = self.rect.right
            match surface.align[1]:
                case AlignUI.START:
                    surface.rect.top     = self.rect.top
                case AlignUI.CENTER:
                    surface.rect.centery = self.rect.centery
                case AlignUI.END:
                    surface.rect.bottom  = self.rect.bottom

            # self.surface.rect.x = self.rect.x + ((self.rect.w - self.surface.rect.w) >> 1)
            # self.surface.rect.y = self.rect.y + ((self.rect.h - self.surface.rect.h) >> 1)

    def draw(self, screen):
        draw.rect(
            screen,
            self.color,
            self.rect,
            border_top_left_radius     = self.radius.upperLeft,
            border_top_right_radius    = self.radius.upperRight,
            border_bottom_left_radius  = self.radius.lowerLeft, 
            border_bottom_right_radius = self.radius.lowerRight
        )

        for surface in self.surfaces:
            surface.draw(screen)

        _width = int(self._width)
        if _width:
            draw.rect(
                screen,
                self.outlineColor,
                self.rect,
                border_top_left_radius     = self.radius.upperLeft,
                border_top_right_radius    = self.radius.upperRight,
                border_bottom_left_radius  = self.radius.lowerLeft, 
                border_bottom_right_radius = self.radius.lowerRight,
                width=_width
            )


    def onHover(
        self,
        world: World,
    ) -> bool:
        hovered = self.rect.collidepoint(world.mouse.get_pos())
        self._width = lerp(
            self._width,
            (self.maxWidth << (world.clicked << 2) if hovered else 0)
        )
        return hovered

    # def onClick(self, world: World):
    #     print(world.mouse.get_pressed())

class BoxUI(UI):
    outlineColor : Color
    direction    : DirectionUI
    children     : list[UI]
    maxWidth     : int
    padding      : Rect
    radius       : BorderRadius
    color        : Color
    rect         : Rect
    z            : int

    _width       : float = 0

    def __init__(
        self,
        outlineColor : Color,
        children  : list[UI],
        direction : DirectionUI,
        maxWidth  : int,
        padding   : Rect,
        radius    : BorderRadius,
        color     : Color,
        rect      : Rect,
        z         : int,
    ):
        self.outlineColor = outlineColor
        self.maxWidth     = maxWidth
        self.radius       = radius  
        self.color        = color   
        self.rect         = rect    
        self.z            = z       

        self.direction = direction
        self.children  = children
        self.padding   = padding

        self.update()

    def update(self):
        for i in range(len(self.children)):
            child = self.children[i]
            child.rect.x = self.rect.x + self.padding.x
            child.rect.y = self.rect.y + self.padding.y

            match self.direction:
                case DirectionUI.HORIZONTAL:
                    child.rect.x += (self.padding.w + child.rect.w) * i
                    child.rect.h = self.rect.h - (self.padding.y << 1)
                case DirectionUI.VERTICAL:
                    child.rect.y += (self.padding.h + child.rect.h) * i
                    child.rect.w = self.rect.w - (self.padding.x << 1)
            child.update()

    def draw(self, screen):
        draw.rect(
            screen,
            self.color,
            self.rect,

            border_top_left_radius     = self.radius.upperLeft,
            border_top_right_radius    = self.radius.upperRight,
            border_bottom_left_radius  = self.radius.lowerLeft, 
            border_bottom_right_radius = self.radius.lowerRight,
        )

        _width = int(self._width)
        if _width:
            draw.rect(
                screen,
                self.outlineColor,
                self.rect,
                border_top_left_radius     = self.radius.upperLeft,
                border_top_right_radius    = self.radius.upperRight,
                border_bottom_left_radius  = self.radius.lowerLeft, 
                border_bottom_right_radius = self.radius.lowerRight,
                width=_width
            )
        for child in self.children:
            child.draw(screen)

    def onHover(
        self,
        world: World,
    ) -> bool:
        for child in self.children:
            child.onHover(world)
        return self.rect.collidepoint(world.mouse.get_pos())

    # def onClick(self, world: World):
    #     print(world.mouse.get_pressed())
