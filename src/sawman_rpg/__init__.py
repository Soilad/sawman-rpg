import pygame

from levels import *


def main() -> None:
    run = True
    show_hitboxes = False
    entityIDs = [ i for i, x in enumerate(world.levels[world.level]) ]
    transparentScreen = pygame.Surface(
        (1280, 720),
        pygame.SRCALPHA
    )
    while run:
        world.mouse = pygame.mouse
        world.keys  = pygame.key.get_pressed()

        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    run = False
                # case pygame.KEYDOWN:
                case pygame.KEYUP:
                    match event.key:
                        case pygame.K_RETURN | pygame.K_z:
                            world.initialTicks.enter = world.tick
                            world.commandIndex += 1
                        case pygame.K_F3:
                            show_hitboxes = not show_hitboxes
                        case pygame.K_TAB:
                            # world.initialTicks.inventory = world.tick
                            world.showInventory = not world.showInventory
                            world.animator.extend(
                                [
                                    UIanimation(
                                        world.overlays.overlays["inventory"],
                                        ["rect", "y"],
                                        (20 if world.showInventory else -720)
                                    ),
                                    UIanimation(
                                        world.overlays.overlays["stats"],
                                        ["rect", "y"],
                                        (20 if world.showInventory else -720)
                                    )
                                ]
                            )
                case pygame.MOUSEBUTTONDOWN:
                    world.clicked = True

        for id in entityIDs:
            entity = world.levels[world.level][id]
            entityIDs.sort(key = lambda x: world.levels[world.level][x].movement.position.y)
            position = entity.movement.position
            if hasattr(entity.collision, "rect"):
                entity.collision.rect.center = position
            sprite_pos = entity.movement.onMove(world)

            if entity.collision.onCollide(world.playerData.interactionPoint) == CollisionType.INTERACT:
                entity.interact.onInteract(world)
            entity.render.onRender(transparentScreen, position, sprite_pos)

            for key in world.overlays.keys:
                overlay = world.overlays.overlays[key]
                overlay.draw(transparentScreen)

                hovered = overlay.onHover(world)
                if hovered and world.clicked:
                    world.clicked = False
                    if hasattr(overlay, "onClick"):
                        overlay.onClick(world)

            # print(world.overlays.passive.values())
            # for overlay in world.overlays.passive.values():
            #     overlay.draw(transparentScreen)


        # if world.commandIndex:
        #     world.overlays.overlays["textbox"].rect.y = lerp(
        #         world.overlays.overlays["textbox"].rect.y,
        #         440
        #     )
        # run every animation, keep only the ones that haven't finished
        world.animator = [
            animation for animation in world.animator
            if not animation(world)
        ]

        # world.overlays.overlays["inventory"].rect.y = lerp(
        #     world.overlays.overlays["inventory"].rect.y,
        #     20 if world.showInventory else -720
        # )
        # world.overlays.overlays["stats"].rect.y = lerp(
        #     world.overlays.overlays["stats"].rect.y,
        #     20 if world.showInventory else -720
        # )
        # world.overlays.overlays["stats"].update()
        # world.overlays.overlays["inventory"].update()
        # world.overlays.overlays["textbox"].update()
        # print(world.overlays.overlays["inventory"].rect.y,)


        if show_hitboxes:
            for entity in world.levels[world.level]:
                rect = getattr(entity.collision, "rect", None)
                if rect is not None:
                    color = (
                        (0, 255, 0)
                        if getattr(entity.collision, "collideReturn", None) == CollisionType.INTERACT
                        else (255, 0, 0)
                    )
                    pygame.draw.rect(transparentScreen, color, rect, 2)
            pygame.draw.circle(transparentScreen, (255, 255, 0), world.playerData.interactionPoint, 4)

        screen.blit(transparentScreen, (0, 0))
        world.tick += 1
        # pygame.time.Clock().tick(20)
        pygame.display.update()
