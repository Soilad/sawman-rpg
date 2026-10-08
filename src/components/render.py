# from classes import *
from dataclasses import dataclass

from pygame import Surface, Vector2, image

import func
from interfaces import Render


@dataclass(slots=True)
class Invisible:
    def onRender(*_):
        pass

@dataclass(slots=True)
class Spritesheet(Render):
    def __init__(self, sprite, width, height):
        self.spritesheet: dict[tuple[int, int]: Surface] = func.clip(
            image.load(sprite).convert_alpha(),
            width,
            height
        )
        self.blitOffset = Vector2(width // 2, height)

    def onRender(self, screen, position, sprite_pos):
        screen.blit(self.spritesheet[sprite_pos], position - self.blitOffset)

@dataclass(slots=True)
class Sprite(Render):
    def __init__(self, sprite):
        self.sprite = image.load(sprite).convert_alpha()
        self.blitOffset = Vector2(self.sprite.get_width() // 2, self.sprite.get_height())

    def onRender(self, screen, position, _):
        screen.blit(
            self.sprite,
            position 
            - self.blitOffset
        )

@dataclass(slots=True)
class Room(Render):
    def __init__(
        self,
        room,
    ):
        # self.bgm = bgm if bgm else 0
        self.wall  = image.load(f"./rooms/{room}/wall.png").convert_alpha()
        self.floor = image.load(f"./rooms/{room}/floor.png").convert_alpha()

    def onRender(self, screen, position, _):
        screen.blit(self.floor, position)
        screen.blit(self.wall,  position)
