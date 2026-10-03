from pygame import Rect, Vector2, image, mask


class Uncollidable:
    def onCollide(self, point: Vector2):
        return False

class Obstacle:
    rect = None

    def __init__(self, x, y, width, height):
        self.rect = Rect(x, y, width, height)

    def onCollide(self, point: Vector2):
        return bool(self.rect.collidepoint(point))

class Wall:
    collisionMask = None
    def __init__(self, room):
        self.collisionMask = mask.from_surface(
            image.load(f"./rooms/{room}/wall.png").convert_alpha()
        )

    def onCollide(self, point: Vector2):
        return bool(self.collisionMask.get_at(point))

class Portal:
    rect = None

    def __init__(self, x, y, width, height, target_room):
        self.rect = Rect(x, y, width, height)
        self.target_room = target_room

    def onCollide(self, point: Vector2):
        return bool(self.rect.collidepoint(point))
