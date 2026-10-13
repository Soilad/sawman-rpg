# from classes import *
from dataclasses import dataclass, field

from pygame import Surface, Vector2, image

from func import clip
from Interfaces import IRenderable


@dataclass(slots=True)
class Invisible(IRenderable):

    def onRender(*_):
        pass


@dataclass(slots=True)
class Spritesheet(IRenderable):
    spritesheet: dict[tuple[int, int], Surface]

    def __init__(self, sprite, width, height):
        self.spritesheet: dict[tuple[int, int], Surface] = clip(
            image.load(sprite).convert_alpha(), width, height)
        self.blitOffset = Vector2(width // 2, height)

    def onRender(self, screen, position, sprite_pos):
        screen.blit(self.spritesheet[sprite_pos], position - self.blitOffset)


@dataclass(slots=True)
class Sprite(IRenderable):
    sprite: Surface

    def __init__(self, sprite):
        self.sprite = image.load(sprite).convert_alpha()
        self.blitOffset = Vector2(self.sprite.get_width() // 2,
                                  self.sprite.get_height())

    def onRender(self, screen, position, sprite_pos) -> None:
        screen.blit(self.sprite, position - self.blitOffset)


@dataclass(slots=True)
class Room(IRenderable):
    wall: Surface
    floor: Surface

    def __init__(
        self,
        room,
    ):
        # self.bgm = bgm if bgm else 0
        print(f"./rooms/{room}/wall.png")
        self.wall = image.load(f"./rooms/{room}/wall.png").convert_alpha()
        self.floor = image.load(f"./rooms/{room}/floor.png").convert_alpha()
        self.blitOffset = Vector2(0, 0)

    def onRender(self, screen, position, sprite_pos) -> None:
        screen.blit(self.floor, position)
        screen.blit(self.wall, position)
