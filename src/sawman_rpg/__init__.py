import pygame

from func import UIanimation
from levels import *


def main() -> None:
    run = True
    entered = False
    transparentScreen = pygame.Surface((1280, 720), pygame.SRCALPHA)
    while run:
        world.mouse = pygame.mouse
        world.keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    run = False
                case pygame.KEYUP:
                    match event.key:
                        case pygame.K_RETURN | pygame.K_z:
                            world.initialTicks.enter = world.tick
                            entered = True
                            # world.commandIndex += 1
                        case pygame.K_TAB:
                            world.showInventory = not world.showInventory
                            UIanimation(world, "inventory", ["rect", "y"],
                                        20 if world.showInventory else -720)
                            UIanimation(world, "stats", ["rect", "y"],
                                        20 if world.showInventory else -720)
                            world.ui.overlays["inventory"].children = [
                                ButtonUI(
                                    COLOR_TERTIARY,
                                    COLOR_SECONDARY,
                                    (1, 4),
                                    BorderRadius(10, 50, 50, 10),
                                    x.onUse,
                                    children=[
                                        SurfaceOverlay(
                                            font_medium.render(
                                                f" {x.quantity}: {x.name}",
                                                FONT_ALIASED,
                                                COLOR_PRIMARY,
                                            ),
                                            align=(AlignUI.START,
                                                   AlignUI.START),
                                        ),
                                    ],
                                    rect=Rect((0, 0), (1280, 80)),
                                ) for x in world.playerData.items.values()
                            ]
                case pygame.MOUSEBUTTONDOWN:
                    world.clicked = True
                case pygame.MOUSEWHEEL:
                    world.scrollDirection = Vector2(event.x, event.y)

        if world.nextLevel is not None:
            playerID = next(
                entity for entity in world.entityIDs
                if world.levels[world.level][entity].type == EntityType.PLAYER)
            playerEntity = world.levels[world.level].pop(playerID)
            world.level = world.nextLevel
            world.nextLevel = None
            world.levels[world.level].append(playerEntity)
        world.updateEntities()

        entityCount = len(world.entityIDs)
        collideAny = False
        for id in world.entityIDs:
            if entityCount != len(world.levels[world.level]):
                break
            # NOTE(soi): this is a bad idea and should probably change rooms outside the loop
            entity = world.levels[world.level][id]
            position = entity.movement.position
            if hasattr(entity.collision, "rect"):
                entity.collision.rect.center = position
            sprite_pos = entity.movement.onMove(world)

            if entity.collision.onCollide(world.playerData.interactionPoint
                                          ) == CollisionType.INTERACT:
                collideAny = True
                # print(world.inDoor)
                # input()
                entity.interact.onInteract(world)
                if entered:
                    world.commandIndex += 1
                    entered = False
            entity.render.onRender(transparentScreen, position, sprite_pos)
        if not collideAny:
            world.inDoor = False
            # pygame.draw.rect(transparentScreen, COLOR_PRIMARY,
            #                  entity.collision.rect)

        for key in world.ui.keys:
            element = world.ui.overlays[key]
            element.draw(transparentScreen)

            hovered = element.onHover(world)
            if hovered and world.clicked:
                world.clicked = False
                if hasattr(element, "onClick"):
                    element.onClick(world)

        for animation_id in list(world.animator.keys()):
            animation = world.animator[animation_id]
            if animation(world):
                del world.animator[animation_id]

        screen.blit(transparentScreen, (0, 0))
        world.tick += 1
        # pygame.time.Clock().tick(60)
        pygame.display.update()
