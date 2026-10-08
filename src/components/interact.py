from dataclasses import dataclass

from consts import FONT_ALIASED, CollisionType, Signal

# from func import give_items, glow
from interfaces import Command, Interact


@dataclass(slots=True)
class NoInteract(Interact):
    def onInteract(self, screen, surface, world, Inventory, b_togg, text_scroll, y_position):
        pass

@dataclass(slots=True)
class Commands(Interact):
    commands: list[Command]
    def __init__(self, commands: list[Command]):
        self.commands = commands
        self.len      = len(self.commands)
        # self.len, self.rendered_dialog = set_dialog(self.dialog, font_medium, FONT_ALIASED)

    def onInteract(self, world) -> None:
        if  world.commandIndex < self.len:
            command = self.commands[world.commandIndex]
            status  = command.emit(world)
            # print(status)
            match status:
                case Signal.CLEAR_COMMANDS:
                    self.commands = self.commands[world.commandIndex::]
                    self.len      = len(self.commands)
        else:
            world.commandIndex = 0
            for command in self.commands:
                command.reset()


class Shop:
    def __init__(self, sprite, dialog, font_small, FONT_ALIASED):
        self.shopui  = pygame.image.load("ui/shop.png").convert_alpha()
        self.shopman = pygame.image.load(shopman).convert()
        self.menu    = []
        for index in range(len(menu)):
            item, price = menu.items()[index]
            self.menu.append(
                Button(
                    f"{item[0]}: ௹{price}",
                    (750, 50 + (60 * index) + y_position),
                    (100, 10),
                    10
                )
            )


    def onInteract(self, screen, surface, font_medium, world, Inventory, b_togg, text_scroll, y_position):
        screen.blit(self.shopman, (0, 0))
        screen.blit(self.shopui, (0, y_position * 1.2))
        item_index = 0
        mpos = pygame.mouse.get_pos()
        if world.dialogueIndex == CollisionType.INTERACT:
            world.dialogueIndex = 0
            pygame.mouse.set_visible(False)
            mouses = 0, 0, 0
        else:
            pygame.mouse.set_visible(True)
            mouses = pygame.mouse.get_pressed()
            for k, v in self.menu.items():
                itemtext = font_medium.render(f"{k[0]}: ௹{v}", FONT_ALIASED, (255, 255, 255))
                if (
                    itemtext.get_rect(topleft=(750, 50 + (60 * item_index))).collidepoint(
                        mpos
                    )
                    and b_togg
                ):
                    itemtext = glow(
                        font_medium.render(
                            f"{k[0]}: ௹{v} ({Inventory.inventory_dict.get(k, 0)})",
                            FONT_ALIASED,
                            (255, 0, 0),
                        ),
                        5,
                        (255, 0, 0),
                    )
                    match mouses:
                        case (1, _, _):
                            give_items(Inventory.inventory_dict, {k: 1})
                            world.money -= v
                        case (_, _, 1):
                            if giveable(Inventory.inventory_dict, {k: -1}):
                                give_items(Inventory.inventory_dict, {k: -1})
                                world.money += v * 0.9
                    b_togg = False

                screen.blit(itemtext, (750, 50 + (60 * item_index) + y_position))
                item_index += 1

