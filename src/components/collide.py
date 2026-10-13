from dataclasses import dataclass, field

from pygame import Rect, Vector2, image
from pygame.mask import Mask, from_surface

from consts import CollisionType
from Interfaces import ICollidable


@dataclass(slots=True)
class Uncollidable(ICollidable):

    def onCollide(self, point: Vector2) -> CollisionType:
        return self.collideReturn


@dataclass(slots=True)
class Obstacle(ICollidable):

    def onCollide(self, point: Vector2) -> CollisionType:
        if self.rect.collidepoint(point):
            return self.collideReturn
        else:
            return CollisionType.NO_OBSTACLE


@dataclass(slots=True)
class Wall(ICollidable):
    collisionMask: Mask = field(default_factory=Mask)

    def __init__(
        self,
        room: str,
        collide_return: CollisionType = CollisionType.OBSTACLE,
    ):
        self.collideReturn = collide_return
        self.collisionMask = from_surface(
            image.load(f"./rooms/{room}/wall.png").convert_alpha())
        self.rect = Rect()

    def onCollide(self, point: Vector2):
        return self.collideReturn if self.collisionMask.get_at(
            point - self.rect.topleft) else CollisionType.NO_OBSTACLE


# if __name__ == "__main__":
