import pygame

# from classes import *
from interfaces import Movement


class Imovable(Movement):
    position = pygame.math.Vector2(0, 0)
    def onMove(self, *_) -> tuple[int, int]:
        return self.position

class PlayerMovement(Movement):
    def __init__(
        self,
        position: pygame.Vector2,
        speed:    int,
        keys:     pygame.key.ScancodeWrapper
    ):
        self.position: pygame.Vector2 = position
        self.speed:    int            = speed

    def onMove(self, world, entities, keys) -> tuple[int, int]:
        walking_direction = 0
        walking_frame = 0

        speed = self.speed << keys[pygame.K_LSHIFT]
        delta_position = pygame.math.Vector2(
            (
                keys[pygame.K_d]
                - keys[pygame.K_a]
                + keys[pygame.K_RIGHT]
                - keys[pygame.K_LEFT]
            ),
            (
                keys[pygame.K_s]
                - keys[pygame.K_w]
                + keys[pygame.K_DOWN]
                - keys[pygame.K_UP]
            ),
        )
        if (
            delta_position.length_squared()
            # and not self.stop
            # and not pygame.mouse.get_visible()
        ):
            walking_frame = (world.tick * 2) // speed % 4
            match delta_position.x, delta_position.y:
                case (1, _):
                    walking_direction = 0
                case (_, 1):
                    walking_direction = 1
                case (_, -1):
                    walking_direction = 2
                case (-1, _):
                    walking_direction = 3

        delta_position *= speed
        final_position = self.position + delta_position
        # final_position = pygame.Vector2(
        #     pygame.math.clamp(
        #         self.position.x
        #         + (delta_position.x),
        #         0,
        #         # room.w -
        #         100
        #     ), 
        #     pygame.math.clamp(
        #         self.position.y
        #         + (delta_position.y),
        #         0,
        #         # room.h -
        #         # 239
        #     ),
        # )

        if not any(
            entities.collision.onCollide(final_position) 
            for entities in entities
            if entities.id != 0
        ):
            self.position = final_position
        return walking_frame, walking_direction

class Chaser(Movement):
    t = 0
    position = pygame.math.Vector2(0, 0)
    targetEntity = None

    def __init__(self, position, speed, shock, enemies, id):
        self.position: pygame.math.Vector2 = pygame.math.Vector2(position)
        self.initial_position: pygame.math.Vector2 = pygame.math.Vector2(position)
        self.speed = speed
        self.shock = shock
        self.id = id
        # self.rect = pygame.Rect(self.current_position, (self.width, self.height))

    def onMove(self, world, entities, keys) -> tuple[int, int]:
        if not self.targetEntity:
            self.targetEntity = next( x for x in entities if x.id == self.id )
        if world.tick - world.enterTime > self.shock * 6:
            self.t = min(self.t + (
                0.1 * self.speed 
                # / fps
            ), 1)
            self.position = pygame.math.Vector2.lerp(
                self.position,
                self.targetEntity.movement.position,
                self.t
            )
        else:
            self.t = 0
            self.position = self.initial_position
            # print(abs(sawman.x - self.x))
            # if (
            #     pygame.math.Vector2.length_squared(player_vars.current_position - self.current_position) < self.width * self.width * scale
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
