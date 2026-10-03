import pygame

# from classes import *
from func import give_items, glow, set_dialog
from interfaces import Interact


class TextBox(Interact):
    def __init__(self, sprite, dialog, font_medium, fontaliased):
        self.sprite = sprite
        self.dialog = dialog
        self.dialog_len, self.rendered_dialog = set_dialog(self.dialog, font_medium, fontaliased)

    def onInteract(self, screen, surface, font_medium, player_vars, Inventory, b_togg, text_scroll, y_position):
        if player_vars.dialog_index > self.dialog_len:
            self.dialog_len = self.dialog = player_vars.dialog_index = 0
            player_vars.group = {}
        else:
            if self.dialog[player_vars.dialog_index - 1][0]:
                player_vars.group[self.dialog[player_vars.dialog_index - 1][0][0]] = pygame.image.load(
                    f"./sprites/faces/{self.dialog[player_vars.dialog_index - 1][0][0]}/{self.dialog[player_vars.dialog_index - 1][0][1]}.png"
                ).convert_alpha()

            [screen.blit(face_sprite[1], (0, 0,)) for face_sprite in sorted(player_vars.group.items(), key= lambda x: x[0])]

            screen.blit(surface, (0, 480 + y_position))
            if self.dialog[player_vars.dialog_index - 1][0]:
                match self.dialog[player_vars.dialog_index - 1][0][0]:
                    case "sawman":
                        x_offset = 200
                    case "zweistein":
                        x_offset = 850
                    case _:
                        x_offset = 625
                text = font_medium.render(
                    self.dialog[player_vars.dialog_index - 1][0][0].capitalize(),
                    False,
                    (255, 255, 255),
                )
                pygame.draw.rect(
                    screen,
                    (0, 0, 0, 127),
                    pygame.Rect(
                        (x_offset - 30, 440 + y_position), (text.get_width() + 60, 60)
                    ),
                    border_radius=50,
                )
                pygame.draw.rect(
                    screen,
                    (255, 0, 0),
                    pygame.Rect(
                        (x_offset - 30, 440 + y_position), (text.get_width() + 60, 60)
                    ),
                    border_radius = 50,
                    width=5,
                )
                screen.blit(
                    text,
                    (x_offset, 440 + y_position),
                )
            for line in self.rendered_dialog[player_vars.dialog_index - 1][
                min(
                    text_scroll,
                    len(self.rendered_dialog[player_vars.dialog_index - 1]) - 1
                )
            ]:
                screen.blit(
                    line,
                    (
                        250,
                        500
                        + y_position
                        + (
                            50
                            * self.rendered_dialog[player_vars.dialog_index - 1][
                                min(text_scroll, len(self.rendered_dialog[player_vars.dialog_index - 1]) - 1)
                            ].index(line)
                        ),
                    ),
                )

class Shop:
    def __init__(self, sprite, dialog, font_small, fontaliased):
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


    def onInteract(self, screen, surface, font_medium, player_vars, Inventory, b_togg, text_scroll, y_position):
        screen.blit(self.shopman, (0, 0))
        screen.blit(self.shopui, (0, y_position * 1.2))
        item_index = 0
        mpos = pygame.mouse.get_pos()
        if player_vars.dialog_index == 2:
            player_vars.dialog_index = 0
            pygame.mouse.set_visible(False)
            mouses = 0, 0, 0
        else:
            pygame.mouse.set_visible(True)
            mouses = pygame.mouse.get_pressed()
            for k, v in self.menu.items():
                itemtext = font_medium.render(f"{k[0]}: ௹{v}", fontaliased, (255, 255, 255))
                if (
                    itemtext.get_rect(topleft=(750, 50 + (60 * item_index))).collidepoint(
                        mpos
                    )
                    and b_togg
                ):
                    itemtext = glow(
                        font_medium.render(
                            f"{k[0]}: ௹{v} ({Inventory.inventory_dict.get(k, 0)})",
                            fontaliased,
                            (255, 0, 0),
                        ),
                        5,
                        (255, 0, 0),
                    )
                    match mouses:
                        case (1, _, _):
                            give_items(Inventory.inventory_dict, {k: 1})
                            player_vars.money -= v
                        case (_, _, 1):
                            if giveable(Inventory.inventory_dict, {k: -1}):
                                give_items(Inventory.inventory_dict, {k: -1})
                                player_vars.money += v * 0.9
                    b_togg = False

                screen.blit(itemtext, (750, 50 + (60 * item_index) + y_position))
                item_index += 1

class Dialogue:
    def __init__(
        self,
        dialogs: list[tuple[tuple[tuple[str,str],str],Callable]],
        collision=True,
    ):
        self.dialogs = dialogs
        self.dialog, self.custom_funcs = self.dialogs.pop(0)
        self.dialog_len, self.rendered_dialog = set_dialog(self.dialog, font_medium, fontaliased)

    def onInteract(self, textbox_surface: pygame.Surface, player_vars, inventory, b_togg, text_scroll, y_position):
        if (player_vars.dialog_index > self.dialog_len):
            player_vars.group = {}
            player_vars.dialog_index = 0
            # adddict(inventory.invbox, self.items[0])
            music.unpause()
            # print(self.dialogs[0])
            # print(giveable(inventory.inventory_dict, self.items))
            can_finish_dialog, run_after_dialog = self.custom_funcs
            if self.dialogs and can_finish_dialog(inventory.inventory_dict):
                print(self.custom_funcs)
                run_after_dialog(inventory.inventory_dict)
                inventory.update_items()
                self.dialog, self.custom_funcs = self.dialogs.pop(0)
                self.dialog_len, self.rendered_dialog = set_dialog(self.dialog, font_medium, fontaliased)


        else:
            if self.dialog[player_vars.dialog_index - 1][0]:
                player_vars.group[self.dialog[player_vars.dialog_index - 1][0][0]] = pygame.image.load(
                    f"{cwd}/sprites/faces/{self.dialog[player_vars.dialog_index - 1][0][0]}/{self.dialog[player_vars.dialog_index - 1][0][1]}.png"
                ).convert_alpha()

            #idfk man
            [screen.blit(face_sprite[1], (0, 0)) for face_sprite in sorted(player_vars.group.items(), key= lambda x: x[0])]

            if "cutscene" in player_vars.group:
                music.pause()
            screen.blit(textbox_surface, (0, 480 + y_position))
            if self.dialog[player_vars.dialog_index - 1][0]:
                match self.dialog[player_vars.dialog_index - 1][0][0]:
                    case "sawman":
                        x_offset = 200
                    case "zweistein":
                        x_offset = 850
                    case _:
                        x_offset = 625
                text = font_medium.render(
                    self.dialog[player_vars.dialog_index - 1][0][0].capitalize(),
                    False,
                    (255, 255, 255),
                )
                pygame.draw.rect(
                    screen,
                    (0, 0, 0, 127),
                    pygame.Rect(
                        (x_offset - 30, 440 + y_position), (text.get_width() + 60, 60)
                    ),
                    border_radius=50,
                )
                pygame.draw.rect(
                    screen,
                    (255, 0, 0),
                    pygame.Rect(
                        (x_offset - 30, 440 + y_position), (text.get_width() + 60, 60)
                    ),
                    border_radius=50,
                    width=5,
                )
                screen.blit(
                    text,
                    (x_offset, 440 + y_position),
                )
            for line in self.rendered_dialog[player_vars.dialog_index - 1][
                min(text_scroll, len(self.rendered_dialog[player_vars.dialog_index - 1]) - 1)
            ]:
                screen.blit(
                    line,
                    (
                        250,
                        500
                        + y_position
                        + (
                            50
                            * self.rendered_dialog[player_vars.dialog_index - 1][
                                min(text_scroll, len(self.rendered_dialog[player_vars.dialog_index - 1]) - 1)
                            ].index(line)
                        ),
                    ),
                )
