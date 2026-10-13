from collections.abc import Callable
from dataclasses import dataclass, field

import pygame

from consts import CollisionType, EntityType
from Interfaces import IMovable
from structs import Entity


@dataclass(slots=True)
class Immovable(IMovable):

    def onMove(self, world) -> tuple[int, int]:
        return (0, 0)


@dataclass(slots=True)
class PlayerMovement(IMovable):
    speed: int = field(default=10)

    def onMove(self, world) -> tuple[int, int]:
        walking_direction = world.playerData.walkingDirection
        walking_frame = 0

        keys = world.keys
        speed = self.speed << keys[pygame.K_LSHIFT]
        world.playerData.deltaPosition = pygame.Vector2(
            (keys[pygame.K_d] - keys[pygame.K_a] + keys[pygame.K_RIGHT] -
             keys[pygame.K_LEFT]),
            (keys[pygame.K_s] - keys[pygame.K_w] + keys[pygame.K_DOWN] -
             keys[pygame.K_UP]),
        )

        if (
                # and not mouse.get_visible()
                world.playerData.deltaPosition.length_squared()):
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
                final_position = pygame.Vector2(
                    pygame.math.clamp(
                        self.position.x + (world.playerData.deltaPosition.x),
                        0, 1279),
                    pygame.math.clamp(
                        self.position.y + (world.playerData.deltaPosition.y),
                        0, 719),
                )

                if not any(
                        entity.collision.onCollide(final_position)
                        & CollisionType.OBSTACLE
                        for entity in world.levels[world.level]
                        if entity.type != EntityType.PLAYER):
                    self.position = final_position

                world.playerData.interactionPoint = final_position

                if world.playerData.positions.full():
                    world.playerData.positions.get()
                else:
                    world.playerData.positions.put(self.position)
            else:
                world.commandIndex = 0

        return walking_frame, walking_direction


@dataclass(slots=True)
class Chaser(IMovable):
    speed: float
    shock: int
    targetFilter: Callable[[Entity], bool]
    initial_position: pygame.Vector2
    t: float = field(default=0)
    _targetEntity: Entity | None = field(default=None)

    def __post_init__(self):
        self.position = self.initial_position

    def onMove(self, world) -> tuple[int, int]:
        if not self._targetEntity:
            print([x.id for x in world.levels[world.level]])
            self._targetEntity = next(x for x in world.levels[world.level]
                                      if self.targetFilter(x))
        if world.tick - world.initialTicks.enterLevel > self.shock * 6:
            self.t = min(
                self.t + (
                    0.1 * self.speed
                    # / fps
                ),
                1)
            self.position = pygame.Vector2.lerp(
                self.position, self._targetEntity.movement.position, self.t)
        else:
            self.t = 0
            self.position = self.initial_position
        return (0, 0)  # TODO: make chasers animated with Spritesheets


@dataclass(slots=True)
class RoomMovement(IMovable):
    bounds: pygame.Rect = field(default_factory=pygame.Rect)

    def __init__(self, position: pygame.Vector2, rect: pygame.Rect):
        self.position = position
        xMax = rect.w - 1280
        yMax = rect.h - 720
        self.bounds = pygame.Rect((0, 0), (xMax + 1, yMax + 1))

    def onMove(self, world) -> tuple[int, int]:
        if self.bounds.collidepoint(world.playerData.deltaPosition -
                                    self.position):
            for entity in world.levels[world.level]:
                entity.movement.position -= world.playerData.deltaPosition
                entity.collision.rect.topleft -= world.playerData.deltaPosition
        return (0, 0)
