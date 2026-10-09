from dataclasses import dataclass, field

from pygame import Rect, Vector2, image, mask

from consts import CollisionType
from Interfaces import ICollidable


@dataclass(slots=True)
class Uncollidable(ICollidable):
    def onCollide(self, point: Vector2) -> CollisionType:
        return CollisionType.NO_OBSTACLE

@dataclass(slots=True)
class Obstacle(ICollidable):
    def __init__(
        self,
        rect: Rect,
        collide_return: CollisionType = CollisionType.OBSTACLE,
    ):
        self.rect = rect
        self.collideReturn = collide_return

    def onCollide(self, point: Vector2) -> CollisionType:
        if self.rect.collidepoint(point):
            return self.collideReturn
        else:
            return CollisionType.NO_OBSTACLE

@dataclass(slots=True)
class Wall(ICollidable):
    collisionMask = None
    def __init__(
        self,
        room: str,
        collide_return: CollisionType = CollisionType.OBSTACLE
    ):
        self.collideReturn = collide_return
        self.collisionMask = mask.from_surface(
            image.load(f"./rooms/{room}/wall.png").convert_alpha()
        )
        self.rect = Rect()

    def onCollide(self, point: Vector2):
        return self.collideReturn if self.collisionMask.get_at(point - self.rect.topleft) else CollisionType.NO_OBSTACLE

class Portal:
    rect = None

    def __init__(self, x, y, width, height, target_room):
        self.rect = Rect(x, y, width, height)
        self.target_room = target_room

    def onCollide(self, point: Vector2):
        return bool(self.rect.collidepoint(point))
