from levels import *


def main() -> None:
    run = True
    state_dirty = True
    while run:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    run = False
                case pygame.KEYDOWN:
                    state_dirty = True
                case pygame.K_UP:
                    state_dirty = False
        for entity in levels:
            if state_dirty:
                levels.sort(key=lambda x: x.movement.position.y)
                position = entity.movement.position
                sprite_pos = entity.movement.onMove(world, levels, keys)
            entity.render.onRender(screen, position, sprite_pos)
        world.tick += 1
        # pygame.time.Clock().tick(20)
        pygame.display.update()
