import pygame
from os import getcwd
from datetime import datetime
# from pygame.image import save
# from pygamevideo import Video
from pygame.math import lerp, clamp
import pytz
from functools import reduce
from func import (
    lognt,
    coler,
    bar,
    scroll,
    clip,
    enemclip,
    putlines,
    # adddict,
    giveable,
    set_dialog,
    give_items,
    pullup,
    shadow,
    glow,
)
from recipies import recipies
from settings import fps, fontaliased, sfxvol, debug_mode
from json import load
from collections.abc import Callable

with open("settings.json") as json_data:
    uiscale = int(load(json_data)["UI Size"] / 14)

datetime_ist = datetime.now(pytz.timezone("Asia/Bangkok"))
nighttime = datetime.now(pytz.timezone("Etc/GMT+1"))
cwd = getcwd()
# pygame.mixer.pre_init(22100, -16, 2, 64)
pygame.init()
pygame.font.init()
pygame.mixer.init(22050, -16, 2, 1024)

music = pygame.mixer.Channel(0)
sfx1 = pygame.mixer.Channel(1)
sfx2 = pygame.mixer.Channel(2)

screen = pygame.display.set_mode(
    (1280, 720), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.SCALED, vsync=1
)

pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONUP, pygame.KEYUP])
box = pygame.image.load(f"{cwd}/ui/textbox.png").convert_alpha()
invui = pygame.image.load(f"{cwd}/ui/inventory.png").convert_alpha()
invanim = range(0, 27)

font_medium = pygame.font.Font(f"{cwd}/ui/Soilad.ttf", 48)
font_small = pygame.font.Font(f"{cwd}/ui/Soilad.ttf", 24)

# @dataclass
class Player_Vars:
    z_health: int = 100
    s_health: int = 100
    walking_frame: int = 0 
    walking_direction: int = 0
    money: int = 0
    dialog_index: int = 0
    room_index: int = 0
    group: dict = {}
    inenem: bool = False
    current_position: pygame.math.Vector2 = pygame.math.Vector2(640, 360)


class Chara:
    collision: bool = False
    in_object: bool = False
    delta_position = pygame.math.Vector2()
    scale: int = 1
    stop: bool = False
    mask = pygame.mask.Mask((50, 50), fill=True)
    current_position: pygame.math.Vector2 = pygame.math.Vector2(640, 360)

    def __init__(self, pos, sprite):
        self.s_spritesheet: dict[tuple[int,int]:pygame.Surface] = clip(pygame.image.load(sprite).convert_alpha(), 100, 239)
        self.initial_position: pygame.math.Vector2 = pos
        self.final_position: pygame.math.Vector2 = pos
    def lock(self, player_vars):
        player_vars.current_position = self.current_position = pygame.math.Vector2(640, 360)

    def save(self):
        return (

            self.current_position,
            # self.room_index,
            # self.dialog_index,
            # self.money,
            # self.z_health,
            # self.s_health,
        )

    def load(self, a):
        (
            self.current_position,
            # self.room_index,
            # self.dialog_index,
            # self.money,
            # self.z_health,
            # self.s_health,
        ) = a

    def move(self, player_vars, room, keys, tick, wall, entertime, ysort, offset):
        # y_offset: int = 400
        self.current_position = player_vars.current_position
        speed: int = 12 << keys[pygame.K_LSHIFT]
        if debug_mode:
            player_vars.dialog_index += keys[pygame.K_LCTRL]
        self.initial_position = self.current_position
        self.delta_position = pygame.math.Vector2(
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
        if self.delta_position.length_squared() and not self.stop and not pygame.mouse.get_visible():
            player_vars.dialog_index = 0
            player_vars.group = {}
            match self.delta_position.x, self.delta_position.y:
                case (1, _):
                    player_vars.walking_direction = 0
                case (_, 1):
                    player_vars.walking_direction = 1
                case (_, -1):
                    player_vars.walking_direction = 2
                case (-1, _):
                    player_vars.walking_direction = 3
            player_vars.walking_frame = (tick * 2) // speed % 4
            self.final_position.x, self.final_position.y = (
                clamp(player_vars.current_position.x + (self.delta_position.x * speed * self.scale), 0, room.w - 100),
                clamp(player_vars.current_position.y + (self.delta_position.y * speed * self.scale), 0, room.h - 239),
            )
            self.final_position = player_vars.current_position + ( speed * self.scale * (self.delta_position))

            # for i in ysort:
            #     pygame.draw.rect(
            #         screen, (0, 0, 0), i.sprite.get_rect(topleft=(i.x, i.y))
            #     )

            self.in_object = reduce(
                lambda x, y: x or y,
                [
                    rect.sprite.get_rect(topleft=rect.current_position).collidepoint(
                        self.final_position + (50 * self.scale, 239 - (125 * self.scale))
                    )
                    and rect.collision
                    for rect in ysort
                ],
            )
            # print(in_object)
            # print(self.xf)
            if sawman.mask.overlap(wall, (0, -188) - self.final_position) or self.in_object:
                for adjacent in (
                    pygame.math.Vector2(1, 1),
                    pygame.math.Vector2(-1, 1),
                    pygame.math.Vector2(1, -1),
                    pygame.math.Vector2(-1, -1),
                ):
                    temp = adjacent * self.scale * speed + self.final_position + (50, -239)

                    self.in_object = reduce(
                        lambda x, y: x or y,
                        [
                            rect.sprite.get_rect(topleft=rect.current_position).collidepoint(
                                temp
                            )
                            and rect.collision
                            for rect in ysort
                        ],
                    )
            if (
                not self.mask.overlap(
                    wall,
                    -1 * self.final_position - (0, 188)
                    ,
                )
                or self.in_object
            ):
                player_vars.current_position = self.current_position = self.final_position
            # else:
            #     if not self.in_object:
            #         self.x, self.y = self.xf, self.yf

            # if sawman.mask.overlap(wall, (-self.x, -self.y - 188)):
            #     self.x = (self.x + int(datetime_ist.strftime("%I%M")[:1:])) % 1280
            #     self.y = (self.y + int(datetime_ist.strftime("%I%M")[:1:-1])) % 720
        else:
            player_vars.walking_frame = 0

        self.scale = player_vars.current_position.y / 360 if room.outside else 1
        self.sprite = pygame.transform.scale(self.s_spritesheet[(player_vars.walking_frame, player_vars.walking_direction)], (100 * self.scale, 239 * self.scale))
        screen.blit(
            self.sprite,
            player_vars.current_position + offset + (0, (239 - 239 * self.scale)),
        )
        # pygame.draw.circle(
        #     screen,
        #     (255, 0, 0),
        #     (self.xf + 50, self.yf + y_offset - (239 * self.scale)),
        #     10,
        # )


class Zweistein:
    collision = False

    def __init__(self, position, sprite):
        self.z_spritesheet: dict[tuple[int, int]: pygame.Surface] = clip(pygame.image.load(sprite).convert_alpha(),100,239)
        self.positions_list: list[pygame.math.Vector2] = [position]
        self.current_position: pygame.math.Vector2 = position

    def save(self):
        return self.positions_list, self.current_position

    def load(self, a):
        self.positions_list, self.current_position = a

    def move(self, player_vars, room, keys, tick, wall, entertime, ysort, offset):
        if self.positions_list[-1] != player_vars.current_position:
            self.positions_list.append(player_vars.current_position)
            if len(self.positions_list) > 8:
                self.current_position = self.positions_list.pop(0)
        self.scale = self.current_position.y / 360 if room.outside else 1

        self.sprite = pygame.transform.scale(self.z_spritesheet[(player_vars.walking_frame, player_vars.walking_direction)], (100 * self.scale, 239 * self.scale))
        screen.blit(
            self.sprite,
            self.current_position + offset + (0, (239 - 239 * self.scale)),
        )


class Inventory:
    info: str = ""
    result: str = ""
    tubes: list = []
    z_hands: str = ""
    s_hands: str = ""
    z_health_text: pygame.Surface = font_medium.render("", fontaliased, (0, 0, 0))
    s_health_text: pygame.Surface = font_medium.render("", fontaliased, (0, 0, 0))
    # wtf is up with the tube texts
    nonetext: pygame.Surface = font_medium.render("", fontaliased, (0, 0, 0))
    tubetext1 = tubetext2 = nonetext
    # wait its not even a tube its a beaker
    initial_open: int = 0 
    y_position: int = -720
    middlemouse: bool = True
    SHOW_INVENTORY: bool = False

    def __init__(self, inventory_dict):
        self.inventory_dict: dict[tuple[str,int]: int] = inventory_dict 
        # self.inventory_items = (x[0] for x in self.inventory_dict)
        self.inventory_text = {
            item_tuple: font_medium.render(f"{quantity}: {item_tuple[0]}", fontaliased, (255, 255, 255))
            for item_tuple, quantity in self.inventory_dict.items()
        }

    def save(self):
        return self.inventory_dict, self.z_hands, self.s_hands

    def load(self, save_inventory):
        self.inventory_dict, self.z_hands, self.s_hands = save_inventory

    def update_items(self):
        self.renderbox = {
            item_tuple: font_medium.render(f"{quantity}: {item_tuple[0]}", fontaliased, (255, 255, 255))
            for item_tuple, quantity in self.inventory_dict.items()
        }

    def update_health(self, player_vars):
        self.z_health_text = font_small.render(f"Health: {int(player_vars.z_health)}", fontaliased, (255, 255, 255))
        self.s_health_text = font_small.render(f"Health: {int(player_vars.s_health)}", fontaliased, (255, 255, 255))

    # def update_money(self):
    # make this a method

    def open(self, player_vars, mscroll, b_togg,  tick):
        # print(self.invbox)
        # print(self.renderbox)
        delta_open: int = tick - self.initial_open
        self.y_position = round(
            lerp(self.y_position, (not self.SHOW_INVENTORY) * -720, delta_open / 45)
        )
        if self.y_position > -600:
            # self.invnames = [x[0] for x in self.invbox]
            mpos = pygame.mouse.get_pos()
            mouses: tuple[int, int, int] = pygame.mouse.get_pressed() if self.SHOW_INVENTORY else (0, 0, 0)

            screen.blit(invui, (0, 0 + self.y_position))
            screen.blit(
                self.s_health_text,
                (180, 145 + self.y_position),
            )
            screen.blit(
                self.z_health_text,
                (180, 575 + self.y_position),
            )
            if self.z_hands:
                screen.blit(
                    glow(
                        font_small.render(self.z_hands[0], fontaliased, (255, 0, 127)),
                        5,
                        (255, 0, 127),
                    ),
                    (100, 625 + self.y_position),
                )
            if self.s_hands:
                screen.blit(
                    glow(
                        font_small.render(self.s_hands[0], fontaliased, (255, 127, 0)),
                        5,
                        (255, 127, 0),
                    ),
                    (100, 215 + self.y_position),
                )
            screen.blit(
                font_small.render(
                    datetime_ist.strftime("%I:%M %p"), fontaliased, (255, 255, 255)
                ),
                (60, 300 + self.y_position),
            )
            screen.blit(
                font_small.render(f"௹:{player_vars.money}", fontaliased, (255, 255, 255)),
                (60, 375 + self.y_position),
            )
            item_index: int = 0
            inventory_dict_copy: dict[tuple[str, int]: int] = self.inventory_dict.copy()
            for item, quantity in list(inventory_dict_copy.items())[
                mscroll : min(len(inventory_dict_copy), 11 + mscroll)
            ]:
                if item in self.renderbox:
                    itemtext: pygame.Surface = self.renderbox[item]
                else:
                    continue

                if (
                    itemtext.get_rect(topleft=(420, 75 + (50 * item_index))).collidepoint(
                        mpos
                    )
                ):
                    # lerp glow someday
                    itemtext: pygame.Surface = glow(
                        font_medium.render(f"{quantity}: {item[0]}", fontaliased, (255, 0, 0)),
                        5,
                        (255, 0, 0),
                    )
                    if b_togg:
                        itemtext: pygame.Surface = font_medium.render(f"{quantity}: {item[0]}", fontaliased, (255, 0, 0))
                        match mouses:
                            case _, _, 1:
                                match item[1]:
                                    case -1:
                                        self.info = "if i eat this ill 110% die"
                                    case 0:
                                        self.info = "not gonna softlock myself"
                                    case _:
                                        if mouses[0]:
                                            player_vars.s_health += item[1] / 2
                                            player_vars.z_health += item[1] / 2
                                            give_items(self.inventory_dict, {item: -1})
                                            self.update_items()
                                            self.update_health(player_vars)
                                        self.info = "yim yum"
                            case _, 1, _:
                                if item[1]:
                                    if item[1] < 0:
                                        if self.z_hands:
                                            give_items(self.inventory_dict, {self.z_hands: 1})
                                        give_items(self.inventory_dict, {item: -1})
                                        self.z_hands = item
                                    else:
                                        if self.s_hands:
                                            give_items(self.inventory_dict, {self.s_hands: 1})
                                        give_items(self.inventory_dict, {item: -1})
                                        self.s_hands = item
                                    self.update_items()
                            case 1, _, _:
                                if len(self.tubes) < 2:
                                    if item not in self.tubes:
                                        self.tubes.append(item)
                                    self.tubes.sort()
                                    self.tubetext1 = glow(
                                        pygame.transform.rotate(
                                            font_small.render(
                                                f"{self.tubes[0][0]}",
                                                fontaliased,
                                                (255, 0, 0),
                                            ),
                                            90,
                                        ),
                                        0.3,
                                        (255, 0, 0),
                                    )
                                    self.tubetext2 = glow(
                                        pygame.transform.rotate(
                                            font_small.render(
                                                f"{self.tubes[-1][0]}",
                                                fontaliased,
                                                (255, 0, 0),
                                            ),
                                            90,
                                        ),
                                        0.3,
                                        (255, 0, 0),
                                    )
                                    if tuple(self.tubes) in recipies.keys() and giveable(self.inventory_dict, recipies[tuple(self.tubes)]):
                                        give_items(self.inventory_dict, {tube_item: -1 for tube_item in self.tubes})
                                        give_items(self.inventory_dict, recipies[tuple(self.tubes)])
                                        self.tubes = []
                                        self.update_items()
                                else:
                                    self.tubes = []

                if quantity <= 0:
                    self.inventory_dict.pop(item)
                screen.blit(itemtext, (420, 75 + (50 * item_index) + self.y_position))
                item_index += 1
                screen.blit(self.tubetext1, (1042, 220 + self.y_position))
                screen.blit(self.tubetext2, (1082, 220 + self.y_position))
                for i, r in enumerate(self.result.split("+")):
                    screen.blit(
                        glow(
                            font_small.render(r, fontaliased, (255, 0, 0)),
                            0.2,
                            (0, 0, 255),
                        ),
                        (1020, 490 + (i * 30) + self.y_position),
                    )

            screen.blit(
                font_small.render(self.info, fontaliased, (255, 255, 255)),
                (60, 250 + self.y_position),
            )

            # FUCKING ZOO WEE MAMA ITEMS ARENT REAL THEYE A TUPLE
            # 0 is important
            # -1 is a chemical
            # anything else is food


class Obj:
    def __init__(self, sprite: pygame.Surface, position: pygame.math.Vector2, dialogs: list[tuple[tuple[tuple[str,str],str],Callable]], collision=True):
        self.current_position: pygame.math.Vector2 = pygame.math.Vector2(position)
        self.collision = collision
        self.sprite = shadow(pygame.image.load(sprite).convert_alpha(), 5, (0, 0, 0))
        self.dialogs = dialogs
        self.dialog, self.custom_funcs = self.dialogs.pop(0)
        # for i in self.dialog:
        #     if i[0]:
        #         if i[0][1].endswith(".mp4"):
        #             self.dialog[self.dialog.index(i)] = (
        #                 (
        #                     i[0][0],
        #                     Video(f"{cwd}/sprites/faces/{i[0][0]}/{i[0][1]}"),
        #                 ),
        #                 self.dialog[self.dialog.index(i)][1],
        #             )

        self.dialog_len, self.rendered_dialog = set_dialog(self.dialog, font_medium, fontaliased)
        # print(self.diarender)
        # self.item_batches = item_batches # shouldve been bitches smsmsh
        self.rect = pygame.Rect(self.current_position, self.sprite.get_size())

    def save(self):
        return (
            self.dialog,
            self.item_batches,
            True,
        )

    def load(self, a):
        self.dialog, self.item_batches, _ = a
        self.dialog_len, self.rendered_dialog = set_dialog(self.dialog, font_medium, fontaliased)
        

    def move(self, player_vars, room, keys, tick, wall, entertime, ysort, offset):
        screen.blit(self.sprite, self.current_position + offset)

            

    def textbox(self, textbox_surface: pygame.Surface, player_vars, inventory, b_togg, text_scroll, y_position):
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

            if "cutscene" in player_vars.group.keys():
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


class Chaser:
    t = 0
    collision = False

    def __init__(self, sprite, position, speed, shock, enemies):
        self.current_position: pygame.math.Vector2 = pygame.math.Vector2(position)
        self.initial_position: pygame.math.Vector2 = pygame.math.Vector2(position)
        self.speed = speed
        self.shock = shock
        self.enemies = [enemies[0], pygame.image.load(f"{cwd}/battle/enemies/{enemies[0]}.png").convert_alpha(), enemies[1]]
        # self.sprite, self.w, self.h = enemclip(
        #     , (0, 0)
        # )
        self.width, self.height = pygame.image.load(sprite).get_size()
        self.width //= 3
        self.height //= 2
        self.spritesheet = clip(shadow(pygame.image.load(sprite).convert_alpha(), 5, (0, 0, 0)), self.width, self.height)
        self.sprite = self.spritesheet[(0,0)]
        self.rect = pygame.Rect(self.current_position, (self.width, self.height))

    def save(self):
        return (
            self.enemies,
            False,
            False,
        )

    def load(self, a):
        self.enemies, _, _ = a

    def move(self, player_vars, room, keys, tick, wall, entertime, ysort, offset):
        scale = self.current_position.y / 360 if room.outside else 1
        if self.enemies:
            if tick - entertime > self.shock * 6:
                self.t = min(self.t + (0.1 * scale * self.speed / fps), 1)
                self.current_position = pygame.math.Vector2.lerp(
                    self.current_position, player_vars.current_position, self.t
                )
            else:
                self.t = 0
                self.current_position = self.initial_position
            # print(abs(sawman.x - self.x))
            if (
                pygame.math.Vector2.length_squared(player_vars.current_position - self.current_position) < self.width * self.width * scale
            ):
                if not (battle.enemies or player_vars.inenem):
                    music.stop()
                    battle.xp = self.enemies[2]
                    battle.enemies = self.enemies.copy()
                    battle.aa = tick
                    battle.attac = self.speed
                    battle.eloc = self.current_position
                    if self.speed:
                        self.enemies = ()
            else:
                player_vars.inenem = False
            screen.blit(
                pygame.transform.scale(self.sprite, (self.width * scale, self.height * scale)),
                self.current_position + offset + (0, (self.height - self.height * scale) - 120 * scale),
            )

    def textbox(*args):
        pass


class Battle:
    sstate = zstate = "idle"
    oindex = opass = 0
    initial_open: int = 1
    initial_enemy_position: int = 1
    attac = 0
    sawtime = zweitime = 0
    zfocus = 1
    xp = 0
    strat = ["", ""]
    exec: bool = False
    zsked: bool = False
    ssked: bool = False
    sawin = pygame.mixer.Sound(f"{cwd}/sfx/Sawin.ogg")
    focusin = pygame.mixer.Sound(f"{cwd}/sfx/Focusin.ogg")
    bang = pygame.mixer.Sound(f"{cwd}/sfx/Bang.ogg")
    enemstate = [0, 0]
    barloc = 720
    szloc = 640
    enemies = ()
    eloc = [0, 0]

    def __init__(
        self,
        bg,
        floor,
        sawman,
        zweistein,
        feederr,
        shooterr,
        locktext,
        enemytheme,
        moneygivers,
    ):
        self.bg = bg
        self.floor = floor
        self.sawman = {
            "offense": pygame.image.load(f"{sawman}/offense.png").convert_alpha(),
            "defense": pygame.image.load(f"{sawman}/defense.png").convert_alpha(),
            "idle": pygame.image.load(f"{sawman}/idle.png").convert_alpha(),
            "rip": pygame.image.load(f"{sawman}/rip.png").convert_alpha(),
        }
        self.zweistein = {
            "offense": pygame.image.load(f"{zweistein}/offense.png").convert_alpha(),
            "defense": pygame.image.load(f"{zweistein}/defense.png").convert_alpha(),
            "idle": pygame.image.load(f"{zweistein}/idle.png").convert_alpha(),
            "rip": pygame.image.load(f"{zweistein}/rip.png").convert_alpha(),
        }

        self.feederrbg = (
            font_small.render(" ".join(feederr.split()[:2:]), fontaliased, (0, 0, 0)),
            font_small.render(" ".join(feederr.split()[3::]), fontaliased, (0, 0, 0)),
        )
        self.feederrfg = (
            font_small.render(" ".join(feederr.split()[:2:]), fontaliased, (255, 127, 0)),
            font_small.render(" ".join(feederr.split()[3::]), fontaliased, (255, 127, 0)),
        )
        self.shooterrbg = (
            font_small.render(" ".join(shooterr.split()[:2:]), fontaliased, (0, 0, 0)),
            font_small.render(" ".join(shooterr.split()[3::]), fontaliased, (0, 0, 0)),
        )
        self.shooterrfg = (
            font_small.render(" ".join(shooterr.split()[:2:]), fontaliased, (255, 0, 255)),
            font_small.render(" ".join(shooterr.split()[3::]), fontaliased, (255, 0, 255)),
        )
        self.locktextbg = font_small.render(locktext, fontaliased, (0, 0, 0))
        self.locktextfg = font_small.render(locktext, fontaliased, (255, 0, 255))

        # this should change depending on enemy wood
        # options = (('call','shoot'),['defend'],('bribe','rob'),['skedaddle'])
        self.options = (
            (" attac", " shoot"),
            (" defend", " defend"),
            (" feed", " focus"),
            (" skedaddle", " skedaddle"),
        )

        self.enemytheme = enemytheme
        self.moneygivers = moneygivers

    def render(self, player_vars, tick, keys, bgm, inventory):
        z = 0

        delta_enemy_position: int = tick - self.initial_enemy_position
        delta_open = tick - self.initial_open
        # print(self.enemies)

        # this should be a dict or smthn
        enemsprite, w, h = enemclip(
            self.enemies[1],
            self.enemstate,
        )

        half_w = w/2
        half_h = h/2

        self.eloc = (
            [
                lerp(self.eloc[0], 640 - half_w, () / 40),
                lerp(self.eloc[1], 360 - half_h, (delta_enemy_position) / 40),
            ]
            if (delta_enemy_position) < 20
            else [640 - half_w, 360 - half_h]
        )
        self.szloc = lerp(self.szloc, 0, (delta_enemy_position - 4) / 40)

        self.barloc = lerp(self.barloc, 670, (delta_enemy_position - 8) / 40)

        swood = lognt(player_vars.s_health)
        zwood = lognt(player_vars.z_health)
        wood = lognt(self.enemies[2] - 1)

        screen.blit(self.bg, (0, 0))
        screen.blit(
            self.floor[int(tick / 3) % 3],
            (0, 0),
        )
        screen.blit(
            enemsprite,
            (
                self.eloc[0],
                self.eloc[1] + ((tick >> (3 - (self.sstate == "offense"))) % 2 - 1),
            ),
        )

        enemy_healthbar = int(22 * wood)
        enemy_healthbar_coler = coler(self.enemies[2] + abs((tick % 50) - 25))

        bar(
            screen,
            enemy_healthbar,
            (640, 148 + abs(((tick * wood / 10) % 10) - 5)),
            enemy_healthbar_coler[::-1],
        )
        bar(
            screen,
            enemy_healthbar,
            (640, 150),
            enemy_healthbar_coler,
        )

        time_limit = (600 >> (4 * self.exec))

        enemy_attack_timer = (tick % time_limit)
        bar(
            screen,
            (time_limit - enemy_attack_timer)//5,
            (640, 180),
            (255, 255, 255),
            radius=2
        )

        if (not enemy_attack_timer) and self.attac:
            self.exec = (
                0
                if (
                    self.strat == ["", ""]
                    or self.strat == ["", " skedaddle"]
                    or self.strat == [" skedaddle", ""]
                )
                else 1
            )
            self.initial_open = tick
            self.enemstate[1] = 0
            enemy_damage = 20 * self.attac / (1 + 0.5 * (self.strat[0] == " defend")) 
            if player_vars.s_health > player_vars.z_health and not self.ssked:
                player_vars.s_health -= enemy_damage
                self.sstate = "defense"
                self.sawtime = tick
                if self.strat[0] != " skedaddle":
                    self.strat[0] = ""
            else:
                player_vars.z_health -= enemy_damage
                self.zstate = "defense"
                self.zweitime = tick
                if self.strat[1] != " skedaddle":
                    self.strat[1] = ""
            self.enemies[2] -= (
                5
                * (self.strat[1] == " defend" or self.strat[0] == " defend")
                / (tick % 10 + 1)
            )
            if player_vars.s_health < 0:
                player_vars.s_health = 0
                self.sstate = "rip"
            if player_vars.z_health < 0:
                player_vars.z_health = 0
                self.zstate = "rip"

        if (delta_battle := int((tick / self.initial_open - 1) * 20)) > 2:
            self.enemstate = [0, 0]
        else:
            self.enemstate[0] = delta_battle + 1

        if (tick - self.sawtime) > 40 and self.sstate == "defense":
            sfx1.set_volume(0)
            sfx1.stop()
            self.sstate = "idle"

        if (tick - self.zweitime) > 40 and self.zstate == "defense":
            sfx2.set_volume(0)
            sfx2.stop()
            self.zstate = "idle"

        if keys[pygame.K_RETURN]:
            self.strat[self.opass] = self.options[self.oindex][-1 * self.opass]

        if self.exec and player_vars.s_health > 0:
            match self.strat[0]:
                case " attac":
                    if self.sstate != "defense":
                        if not sfx1.get_busy():
                            sfx1.set_volume(sfxvol)
                            sfx1.play(self.sawin)
                        self.enemies[2] -= (1 + abs(swood)) / 27
                        self.enemstate[1] = 1
                        self.sstate = "offense"
                    else:
                        sfx1.set_volume(0)
                        sfx1.stop()
                        self.strat[0] = ""
                case " defend":
                    self.sstate = "defense"
                case " feed":
                    if self.sstate != "defense" and inventory.s_hands:
                        self.enemies[2] += inventory.s_hands[1]
                        self.enemstate[1] = 0
                        self.sstate = "offense"
                        if delta_open > 4:
                            inventory.s_hands = ""
                            self.strat[0] = ""
                    if not inventory.s_hands:
                        screen.blit(
                            self.feederrbg[0],
                            (347, 283),
                        )
                        screen.blit(
                            self.feederrbg[1],
                            (347, 303),
                        )
                        screen.blit(
                            self.feederrfg[0],
                            (350, 280),
                        )
                        screen.blit(
                            self.feederrfg[1],
                            (350, 300),
                        )
                        if delta_open > 30:
                            self.strat[0] = ""
                case " skedaddle":
                    self.ssked = True

        if not self.ssked:
            screen.blit(
                self.sawman[self.sstate],
                (-self.szloc + (((tick * int(player_vars.s_health)) / 1024) % 2 - 1), 0),
            )

            s_bar = int(12 * lognt(player_vars.s_health - 1))

            bar(
                screen,
                s_bar,
                (146, self.barloc + 4),
                radius=15,
            )
            bar(
                screen,
                s_bar,
                (150, self.barloc),
                (255, 127, 0),
                15,
            )
        else:
            self.opass = 1

        if self.exec and player_vars.z_health > 0:
            match self.strat[1]:
                case " shoot":
                    if self.zstate != "defense" and inventory.z_hands:
                        self.enemies[2] += (
                            inventory.z_hands[1] * self.zfocus + (zwood)
                        ) / 9
                        self.enemstate[1] = 0
                        if not sfx2.get_busy():
                            sfx2.set_volume(sfxvol)
                            sfx2.play(self.bang)
                        self.zstate = "offense"
                        if delta_enemy_position > 4:
                            inventory.z_hands = ""
                            self.strat[1] = ""
                    if not inventory.z_hands:
                        screen.blit(
                            self.shooterrbg[0],
                            (757, 283),
                        )
                        screen.blit(
                            self.shooterrbg[1],
                            (757, 303),
                        )
                        screen.blit(
                            self.shooterrfg[0],
                            (760, 280),
                        )
                        screen.blit(
                            self.shooterrfg[1],
                            (760, 300),
                        )
                        if delta_enemy_position > 30:
                            self.strat[1] = ""
                case " defend":
                    self.zstate = "defense"

                case " focus":
                    if self.zstate != "defense" and self.zfocus < 30:
                        self.zfocus += 0.1
                        if not sfx2.get_busy():
                            sfx2.set_volume(sfxvol)
                            sfx2.play(self.focusin)
                        screen.blit(self.locktextbg, (757, 283))
                        screen.blit(self.locktextfg, (760, 280))
                    else:
                        sfx2.set_volume(0)
                        sfx2.stop()
                        self.strat[1] = ""
                case " skedaddle":
                    self.zsked = True

        if not self.zsked:
            screen.blit(
                self.zweistein[self.zstate],
                (self.szloc + (((tick * int(player_vars.z_health)) / 1024) % 2 - 1), 0),
            )
            z_bar = int(12 * lognt(player_vars.z_health - 1))
            bar(
                screen,
                z_bar,
                (1124, self.barloc + 4),
                radius=15,
            )
            bar(
                screen,
                z_bar,
                (1130, self.barloc),
                (255, 0, 127),
                15,
            )

        else:
            self.opass = 0

        if not music.get_busy():
            music.play(
                pygame.mixer.Sound(
                    f"{cwd}/music/{self.enemytheme[self.enemies[0]]}.mp3"
                ),
                -1,
            )
            if (
                self.strat == ["", ""]
                or (self.strat[0] == "" and self.zsked)
                or (self.strat[1] == "" and self.ssked)
            ):
                sfx1.stop()
                sfx2.stop()
                self.exec = False

        screen.blit(
            font_medium.render(
                f"{self.strat[0]}{'+' * self.exec}{'   ' * (not self.exec)}{self.strat[1]}",
                fontaliased,
                (255 * (self.exec), 0, 0),
            ),
            (584 - 24 * len(self.strat[0]), 560),
        )
        screen.blit(
            font_medium.render(
                f"{self.strat[0]}{'+' * self.exec}{'   ' * (not self.exec)}{self.strat[1]}",
                fontaliased,
                (255 * (not self.exec), 0, 0),
            ),
            (586 - 24 * len(self.strat[0]), 558),
        )

        if delta_enemy_position > 10:
            pullup(fontaliased, font_small, screen, self.enemytheme[self.enemies[0]], 0)
        for o in self.options:
            if not self.ssked:
                screen.blit(
                    font_medium.render(o[0], fontaliased, (0, 0, 0)),
                    (50 - self.szloc, 360 + z),
                )
            if not self.zsked:
                screen.blit(
                    font_medium.render(o[-1], fontaliased, (0, 0, 0)),
                    (980 + self.szloc, 360 + z),
                )
            z += 50
        screen.blit(
            font_medium.render(
                self.options[self.oindex][self.opass],
                fontaliased,
                (255, 127 * (-1 * (self.opass - 1)), 127 * self.opass),
            ),
            (
                53 + (930 * self.opass) + (self.opass * 2 - 1) * self.szloc,
                357 + 50 * self.oindex,
            ),
        )
        if (
            self.enemies[2] < 5
            or self.enemies[2] - self.xp > 20
            or (self.strat == [" skedaddle", " skedaddle"] and self.exec)
        ):
            sfx1.set_volume(0)
            sfx2.set_volume(0)
            music.stop()
            self.enemstate = [0, 1]
            music.play(pygame.mixer.Sound(f"{cwd}/music/{bgm}.mp3"), -1)
            player_vars.s_health += int(battle.xp) / 2
            player_vars.z_health += int(battle.xp) / 2
            player_vars.money += self.moneygivers[self.enemies[0]]
            player_vars.inenem = True
            self.xp = 0
            self.strat = ["", ""]
            self.zstate = "idle"
            self.sstate = "idle"
            self.enemies = ()
            self.ssked = False
            self.zsked = False
            self.barloc = 720
            self.szloc = 640


class Room:
    x, y = 0, 0

    def __init__(self, room, bgm, outside, inters, portals, dialog):
        self.outside = outside
        self.inters = inters
        self.intersrect = [x.sprite.get_rect(topleft=x.current_position) for x in inters]
        self.bgm = bgm if bgm else 0
        self.wall = pygame.image.load(f"{cwd}/rooms/{room}/wall.png").convert_alpha()
        self.floor = pygame.image.load(f"{cwd}/rooms/{room}/floor.png").convert_alpha()
        self.w, self.h = self.wall.get_size()
        self.mask = pygame.mask.from_surface(self.wall)
        self.portals = portals
        self.dialog = dialog
        self.dialog_len, self.rendered_dialog = set_dialog(self.dialog, font_medium, fontaliased)

    def save(self):
        return (
            [x.save() for x in self.inters],
            self.dialog,
        )

    def load(self, a):
        intersaves, cutscene = a
        for i in range(0, len(self.inters)):
            self.inters[i].load(intersaves[i])
        self.intersrect = [x.sprite.get_rect(topleft=(x.x, x.y)) for x in self.inters]
        self.dialog = cutscene
        if self.dialog:
            self.dialog_len, self.rendered_dialog = set_dialog(self.dialog, font_medium, fontaliased)


    def render(self, x, y):
        # speed = 12 << keys[pygame.K_LSHIFT]
        # if self.h != 720:
        #     dx, dy = (
        #         (
        #             keys[pygame.K_d]
        #             - keys[pygame.K_a]
        #             + keys[pygame.K_RIGHT]
        #             - keys[pygame.K_LEFT]
        #         ),
        #         (
        #             keys[pygame.K_s]
        #             - keys[pygame.K_w]
        #             + keys[pygame.K_DOWN]
        #             - keys[pygame.K_UP]
        #         ),
        #     )
        #     print(dx, dy)
        #     self.xf, self.yf = (
        #         clamp(self.x - (dx * speed), 0, 1180),
        #         clamp(self.y - (dy * speed), 0, 481),
        #     )
        #     self.x, self.y = self.xf, self.yf
        screen.blit(self.floor, (x, y))
        screen.blit(self.wall, (x, y))

    def textbox(self, player_vars, text_scroll, y_position):
        if player_vars.dialog_index > self.dialog_len:
            self.dialog_len = self.dialog = player_vars.dialog_index = 0
            player_vars.group = {}
        else:
            if self.dialog[player_vars.dialog_index - 1][0]:
                player_vars.group[self.dialog[player_vars.dialog_index - 1][0][0]] = pygame.image.load(
                    f"{cwd}/sprites/faces/{self.dialog[player_vars.dialog_index - 1][0][0]}/{self.dialog[player_vars.dialog_index - 1][0][1]}.png"
                ).convert_alpha()

            [screen.blit(face_sprite[1], (0, 0)) for face_sprite in sorted(player_vars.group.items(), key= lambda x: x[0])]

            screen.blit(box, (0, 480 + y_position))
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


# wow the portal class is useless huh
class Portal:
    def __init__(self, position, dim, room_index, new_position: pygame.math.Vector2):
        self.door = pygame.Rect(
            (position[0] - (dim[0] / 2), position[1] - (dim[0] / 2)), (dim[0], dim[1])
        )
        self.room_index = room_index
        self.new_position = pygame.math.Vector2(new_position)

class Trader:
    collision: bool = True
    rendered_dialog = ("", "")
    dialog = ((0, 1),(1, 1))

    def __init__(self, sprite, position, shopman, menu):
        self.current_position: pygame.math.Vector2 = pygame.math.Vector2(position)
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.rect = pygame.Rect(self.current_position, self.sprite.get_size())
        self.shopui = pygame.image.load("ui/shop.png").convert_alpha()
        self.shopman = pygame.image.load(shopman).convert()
        self.menu = menu

    def textbox(self, textbox_surface, player_vars, Inventory, b_togg, text_scroll, y_position):
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
                            f"{k[0]}: ௹{v} ({inventory.inventory_dict[k] if k in inventory.inventory_dict else 0})",
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

    def load(a, aa):
        pass

    def save(a):
        pass

    def move(self, player_vars, room, keys, tick, wall, entertime, ysort, offset):
        screen.blit(self.sprite, self.current_position + offset )


class Button:
    thicc = 0

    def __init__(self, id, pos, dim, thicc):
        self.id = id
        self.pos = pos
        self.dim = dim
        self.thiccmax = thicc
        self.brect = pygame.Rect(
            self.pos[0] - (self.dim[0] / 2),
            self.pos[1],
            self.dim[0],
            self.dim[1],
        )
        self.rect = pygame.Rect((0, 0), dim)
        # NOTE(soi): yea pygame already has a thing for centering rects, should read the documentation more smsmsmh
        self.rect.center = pos

    def draw(self, screen, mpos, b_togg, tab, settings_json):
        hovered = pygame.Rect.collidepoint(self.rect, mpos)

        if hovered:
            if self.thicc < self.thiccmax:
                self.thicc += 1
                # self.thicc = lerp(
                #     self.thicc,
                #     self.thiccmax,
                #     (tick - self.last_tick) / 5,
                # )
        else:
            self.thicc = max(self.thicc - 1, 0)
            # self.last_tick = tick

        scaled_thicc = self.thicc

        if scaled_thicc:
            pygame.draw.rect(
                screen,
                (255, 0, 0),
                pygame.Rect(
                    self.rect.x - scaled_thicc,
                    self.rect.y - scaled_thicc,
                    self.rect.width + scaled_thicc * 2,
                    self.rect.height + scaled_thicc * 2,
                ),
                border_radius=(self.rect.height * scaled_thicc // 2),
            )

        pygame.draw.rect(
            screen,
            (0, 0, 0),
            self.rect,
            border_radius=(self.rect.height // 2),
        )

        text = (
            f"{self.id}: {settings_json[self.id]}"
            if self.id in settings_json
            else self.id
        )
        self.text = text
        font_render = font_small.render(
            text,
            fontaliased,
            (255, 0, 0)
            if pygame.Rect.collidepoint(self.rect, mpos) and b_togg
            else (255, 255, 255),
        )
        screen.blit(
            font_render,
            (
                self.rect.centerx - font_render.get_width() / 2,
                self.rect.y + (self.thiccmax),
            ),
        )

        if pygame.Rect.collidepoint(self.rect, mpos) and b_togg:
            return self.id


x = 640
y = 360
keys = pygame.key.get_pressed()
player_vars = Player_Vars()
sawman = Chara(pygame.math.Vector2(x, y), f"{cwd}/sprites/sawman.png")
zwei = Zweistein(pygame.math.Vector2(x, y), f"{cwd}/sprites/zweistein.png")
print(nighttime.strftime("%d"))
battle = Battle(
    pygame.image.load(
        f"{cwd}/battle/battlebg{int(nighttime.strftime('%d')) % 8}.png"
    ).convert_alpha(),
    (
        pygame.image.load(f"{cwd}/battle/1.png").convert_alpha(),
        pygame.image.load(f"{cwd}/battle/2.png").convert_alpha(),
        pygame.image.load(f"{cwd}/battle/3.png").convert_alpha(),
    ),
    f"{cwd}/battle/sawman/",
    f"{cwd}/battle/zweistein/",
    "FUCK WHAT DO I FEED IT",
    "FUCK I FORGOT TO RELOAD",
    "Locking in",
    # {"Nitroglycerin": 200, "Oxyhydrogen Gas": 5},
    {"Amalgam Type C": "Sizeable_canines", "Shawarma": "Pakistani_nightcore_remix"},
    {"Amalgam Type C": 0, "Shawarma": 200},
)
inventory = Inventory(
    {
        ("Shawarma", 20): 5,
        ("Electrolysis Setup", 0): 2,
        ("Camera", 0): 1,
        ("Nitric Acid", -1): 3,
        ("Sulphuric Acid", -1): 1,
        ("Alcohol", -1): 1,
        ("Sodium Hydroxide", -1): 3,
        ("Oil", 1): 1,
        ("Silver", -1): 1,
        ("Water", 1): 3,
        ("Paper", -1): 1,
    }
)
