from dataclasses import dataclass, field

from pygame import *

from consts import CollisionType, EntityType

# from classes import *
from interfaces import Movement


@dataclass(slots=True)
class Imovable(Movement):
    position: Vector2 = field(default_factory=Vector2)

    def onMove(self, world) -> tuple[int, int]:
        return self.position

@dataclass(slots=True)
class PlayerMovement(Movement):
    position: Vector2 = field(default_factory=Vector2)

    def __init__(self, position: Vector2, speed: int):
        self.position: Vector2 = position
        self.speed:    int     = speed

    def onMove(self, world) -> tuple[int, int]:
        walking_direction = world.playerData.walkingDirection
        walking_frame     = 0

        keys  = world.keys
        speed = self.speed << keys[K_LSHIFT]
        world.playerData.deltaPosition = Vector2(
            (
                keys[K_d]
                - keys[K_a]
                + keys[K_RIGHT]
                - keys[K_LEFT]
            ),
            (
                keys[K_s]
                - keys[K_w]
                + keys[K_DOWN]
                - keys[K_UP]
            ),
        )

        if (
            # and not mouse.get_visible()
            world.playerData.deltaPosition.length_squared()
        ):
            walking_frame = (world.tick * 2) // speed % 4
            match world.playerData.deltaPosition.x, world.playerData.deltaPosition.y:
                case (1, _):
                    world.playerData.walkingDirection = 0
                case (_, 1):
                    world.playerData.walkingDirection = 1
                case (_, -1):
                    world.playerData.walkingDirection = 2
                case (-1, _):
                    world.playerData.walkingDirection = 3

            world.playerData.deltaPosition *= speed
            if not world.playerData.stop:
                final_position = Vector2(
                    math.clamp(
                        self.position.x
                        + (world.playerData.deltaPosition.x),
                        0,
                        1279
                    ), 
                    math.clamp(
                        self.position.y
                        + (world.playerData.deltaPosition.y),
                        0,
                        719
                    ),
                )

                if not any(
                    entity.collision.onCollide(final_position) & CollisionType.OBSTACLE
                    for entity in world.levels[world.level]
                    if entity.type != EntityType.PLAYER
                ):
                    self.position = final_position

                world.playerData.interactionPoint = final_position

                if world.playerData.positions.full():
                    world.playerData.positions.get()
                else:
                    world.playerData.positions.put(self.position)

        return walking_frame, world.playerData.walkingDirection

@dataclass(slots=True)
class Chaser(Movement):
    t = 0
    position: Vector2 = field(default_factory=Vector2)
    targetEntity = None

    def __init__(
        self,
        position,
        speed,
        shock,
        enemies,
        id,
    ):
        self.position: Vector2 = Vector2(position)
        self.initial_position: Vector2 = Vector2(position)
        self.speed = speed
        self.shock = shock
        self.id = id
        # self.rect = Rect(self.current_position, (self.width, self.height))

    def onMove(self, world) -> tuple[int, int]:
        if not self.targetEntity:
            self.targetEntity = next( x for x in world.levels[world.level] if x.id == self.id )
        if world.tick - world.initialTicks.enter > self.shock * 6:
            self.t = min(self.t + (
                0.1 * self.speed 
                # / fps
            ), 1)
            self.position = Vector2.lerp(
                self.position,
                self.targetEntity.movement.position,
                self.t
            )
        else:
            self.t = 0
            self.position = self.initial_position
            # print(abs(sawman.x - self.x))
            # if (
            #     math.Vector2.length_squared(player_vars.current_position - self.current_position) < self.width * self.width * scale
            # ):
            #     if not (battle.enemies or player_vars.inenem):
            #         music.stop()
            #         battle.xp = self.enemies[2]
            #         battle.enemies = self.enemies.copy()
            #         battle.aa = tick
            #         battle.attac = self.speed
            #         battle.eloc = self.current_position
            #         if self.speed:
            #             self.enemies = ()
            # else:
            #     player_vars.inenem = False

@dataclass(slots=True)
class RoomMovement(Movement):
    position: Vector2   = field(default_factory=Vector2)
    bounds: Rect        = field(default_factory=Rect)
    def __init__(self, position: Vector2, rect: Rect):
        self.position = position
        xMax          = rect.w - 1280
        yMax          = rect.h - 720
        self.bounds   = Rect((0, 0), (xMax + 1, yMax + 1))

    def onMove(self, world) -> tuple[int, int]:
        if self.bounds.collidepoint(world.playerData.deltaPosition-self.position):
            for entity in world.levels[world.level]:
                entity.movement.position -= world.playerData.deltaPosition
                entity.collision.rect.topleft -= world.playerData.deltaPosition
