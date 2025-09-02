import pygame
from os import getcwd
from datetime import datetime
from pygame.image import save
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
    adddict,
    pullup,
    shadow,
    glow,
)
from recipies import recipies
from settings import fps, fontaliased, sfxvol, debug_mode
from json import load

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

fontmed = pygame.font.Font(f"{cwd}/ui/Soilad.otf", 48)
fontmin = pygame.font.Font(f"{cwd}/ui/Soilad.otf", 24)


class Chara:
    collision = in_object = False
    zhealth = shealth = 100
    dx, dy = 0, 0
    frame = money = dir = dindex = rindex = 0
    scale = 1
    stop = inenem = False
    mtogg = True
    mask = pygame.mask.Mask((50, 50), fill=True)
    group = {}

    def __init__(self, pos, sprite):
        self.spritesheet1 = pygame.image.load(sprite).convert_alpha()
        self.xi, self.yi = self.xf, self.yf = self.x, self.y = pos

    def lock(self):
        self.x, self.y = 640, 360

    def save(self):
        return (
            self.rindex,
            self.dindex,
            self.x,
            self.y,
            self.money,
            self.zhealth,
            self.shealth,
        )

    def load(self, a):
        (
            self.rindex,
            self.dindex,
            self.x,
            self.y,
            self.money,
            self.zhealth,
            self.shealth,
        ) = a

    def move(self, room, keys, tick, wall, entertime, ysort, offset):
        y_offset = 400
        speed = 12 << keys[pygame.K_LSHIFT]
        if debug_mode:
            self.dindex += keys[pygame.K_LCTRL]
        self.xi, self.yi = self.x, self.y
        self.dx, self.dy = (
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
        if (self.dx or self.dy) and not self.stop and not pygame.mouse.get_visible():
            self.dindex = 0
            self.group = dict()
            match (self.dx, self.dy):
                case (1, _):
                    self.dir = 0
                case (-1, _):
                    self.dir = 3
                case (_, 1):
                    self.dir = 1
                case (_, -1):
                    self.dir = 2
            self.frame = (tick * 2) // speed % 4
            self.xf, self.yf = (
                clamp(self.x + (self.dx * speed * self.scale), 0, room.w - 100),
                clamp(self.y + (self.dy * speed * self.scale), 0, room.h - 239),
            )

            # for i in ysort:
            #     pygame.draw.rect(
            #         screen, (0, 0, 0), i.sprite.get_rect(topleft=(i.x, i.y))
            #     )

            self.in_object = reduce(
                lambda x, y: x or y,
                [
                    rect.sprite.get_rect(topleft=(rect.x, rect.y)).collidepoint(
                        (self.xf + 50, self.yf + y_offset - (239 * self.scale))
                    )
                    and rect.collision
                    for rect in ysort
                ],
            )
            # print(in_object)
            print(self.xf)
            if sawman.mask.overlap(wall, (-self.xf, -self.yf - 188)) or self.in_object:
                for adj in (
                    (1, 1),
                    (-1, 1),
                    (1, -1),
                    (-1, -1),
                ):
                    pygame.draw.rect(
                        screen,
                        (255, 0, 0),
                        pygame.Rect(
                            5,
                            5,
                            -self.xf + (adj[0] * self.scale * speed),
                            -self.yf - 188 + (adj[1] * self.scale * speed),
                        ),
                    )
                    self.in_object = reduce(
                        lambda x, y: x or y,
                        [
                            rect.sprite.get_rect(topleft=(rect.x, rect.y)).collidepoint(
                                (
                                    self.xf + 50 + (adj[0] * self.scale * speed),
                                    self.yf
                                    + y_offset
                                    - (239 * self.scale)
                                    + (adj[0] * self.scale * speed),
                                )
                            )
                            and rect.collision
                            for rect in ysort
                        ],
                    )
                    if (
                        not sawman.mask.overlap(
                            wall,
                            (
                                -self.xf + (adj[0] * self.scale * speed),
                                -self.yf - 188 + (adj[1] * self.scale * speed),
                            ),
                        )
                        or self.in_object
                    ):
                        self.x, self.y = (
                            self.xf - (adj[0] * self.scale * speed),
                            self.yf - (adj[1] * self.scale * speed),
                        )

            else:
                if not self.in_object:
                    self.x, self.y = self.xf, self.yf

            # if sawman.mask.overlap(wall, (-self.x, -self.y - 188)):
            #     self.x = (self.x + int(datetime_ist.strftime("%I%M")[:1:])) % 1280
            #     self.y = (self.y + int(datetime_ist.strftime("%I%M")[:1:-1])) % 720
        else:
            self.frame = 0
        self.scale = self.y / 360 if room.outside else 1
        self.sprite = pygame.transform.scale(
            clip(self.spritesheet1, 100 * self.frame, 239 * self.dir),
            (100 * self.scale, 239 * self.scale),
        )
        screen.blit(
            self.sprite,
            (self.x + offset[0], self.y + offset[1] + (239 - 239 * self.scale)),
        )
        # pygame.draw.circle(
        #     screen,
        #     (255, 0, 0),
        #     (self.xf + 50, self.yf + y_offset - (239 * self.scale)),
        #     10,
        # )


class Zweistein:
    collision = False

    def __init__(self, xy, sprite):
        self.spritesheet2 = pygame.image.load(sprite).convert_alpha()
        self.poss = [xy]
        self.x, self.y = xy

    def save(self):
        return self.poss, self.x, self.y

    def load(self, a):
        self.poss, self.x, self.y = a

    def move(self, room, keys, tick, wall, entertime, ysort, offset):
        if self.poss[-1] != (sawman.x, sawman.y):
            self.poss.append((sawman.x, sawman.y))
            if len(self.poss) > 16:
                self.poss = self.poss[1::]
        self.x, self.y = self.poss[0]
        self.scale = self.y / 360 if room.outside else 1
        self.sprite = pygame.transform.scale(
            clip(self.spritesheet2, 100 * sawman.frame, 239 * sawman.dir),
            (100 * self.scale, 239 * self.scale),
        )
        screen.blit(
            self.sprite,
            (self.x + offset[0], self.y + offset[1] + (239 - 239 * self.scale)),
        )


class Inventory:
    info = result = ""
    tubes = []
    zhands = ""
    shands = ""
    tubetext1 = tubetext2 = fontmed.render("", fontaliased, (255, 0, 0))
    a = 0
    ymov = -720
    middlemouse = True
    invshow = False

    def __init__(self, item):
        self.invbox = item
        self.invnames = [x[0] for x in self.invbox]
        self.renderbox = {
            k: fontmed.render(f"{v}: {k[0]}", fontaliased, (255, 255, 255))
            for k, v in self.invbox.items()
        }

    def save(self):
        return self.invbox, self.zhands, self.shands

    def load(self, a):
        self.invbox, self.zhands, self.shands = a

    def update(self):
        self.renderbox = {
            k: fontmed.render(f"{v}: {k[0]}", fontaliased, (255, 255, 255))
            for k, v in self.invbox.items()
        }
        print(self.invbox)

    def open(self, sawman, mscroll, tick):
        self.ymov = round(
            lerp(self.ymov, (not self.invshow) * -720, (tick - self.a) / 45)
        )
        if self.ymov > -600:
            self.invnames = [x[0] for x in self.invbox]
            mpos = pygame.mouse.get_pos()
            mouses = pygame.mouse.get_pressed() if self.invshow else (0, 0, 0)

            screen.blit(invui, (0, 0 + self.ymov))
            screen.blit(
                fontmin.render(
                    f"Health: {int(sawman.shealth)}", fontaliased, (255, 255, 255)
                ),
                (180, 145 + self.ymov),
            )
            screen.blit(
                fontmin.render(
                    f"Health: {int(sawman.zhealth)}", fontaliased, (255, 255, 255)
                ),
                (180, 575 + self.ymov),
            )
            if self.zhands:
                screen.blit(
                    glow(
                        fontmin.render(self.zhands[0], fontaliased, (255, 0, 127)),
                        5,
                        (255, 0, 127),
                    ),
                    (100, 625 + self.ymov),
                )
            if self.shands:
                screen.blit(
                    glow(
                        fontmin.render(self.shands[0], fontaliased, (255, 127, 0)),
                        5,
                        (255, 127, 0),
                    ),
                    (100, 215 + self.ymov),
                )
            screen.blit(
                fontmin.render(
                    datetime_ist.strftime("%I:%M %p"), fontaliased, (255, 255, 255)
                ),
                (60, 300 + self.ymov),
            )
            screen.blit(
                fontmin.render(f"௹:{sawman.money}", fontaliased, (255, 255, 255)),
                (60, 375 + self.ymov),
            )
            itemdex = 0
            for k, v in list(self.invbox.copy().items())[
                mscroll : min(len(self.invbox.copy()), 11 + mscroll)
            ]:
                if k in self.renderbox:
                    itemtext = self.renderbox[k]
                else:
                    continue

                if (
                    itemtext.get_rect(topleft=(420, 75 + (50 * itemdex))).collidepoint(
                        mpos
                    )
                    and sawman.mtogg
                ):
                    match mouses:
                        case _, _, 1:
                            match k[1]:
                                case -1:
                                    self.info = "if i eat this ill 110% die"
                                case 0:
                                    self.info = "not gonna softlock myself"
                                case _:
                                    if mouses[0]:
                                        sawman.shealth += k[1] / 2
                                        sawman.zhealth += k[1] / 2
                                        if v == 1:
                                            del self.invbox[k]
                                        else:
                                            self.invbox[k] -= 1
                                        sawman.mtogg = False
                                    self.info = "yim yum"
                        case _, 1, _:
                            if sawman.mtogg:
                                if k[1] < -1:
                                    if self.zhands:
                                        self.invbox[self.zhands] = (
                                            1
                                            if self.zhands not in self.invbox
                                            else self.invbox[self.zhands] + 1
                                        )
                                    if self.invbox[k] == 1:
                                        del self.invbox[k]
                                    else:
                                        self.invbox[k] -= 1
                                    self.zhands = k
                                    self.update()
                                if k[1] > 0:
                                    if self.shands:
                                        self.invbox[self.shands] = (
                                            1
                                            if self.shands not in self.invbox
                                            else self.invbox[self.shands] + 1
                                        )
                                    if self.invbox[k] == 1:
                                        del self.invbox[k]
                                    else:
                                        self.invbox[k] -= 1
                                    self.shands = k
                                    self.update()
                                sawman.mtogg = False
                        case 1, _, _:
                            if len(self.tubes) < 2:
                                if k not in self.tubes:
                                    self.tubes.append(k)
                                self.tubes.sort()
                                self.tubetext1 = glow(
                                    pygame.transform.rotate(
                                        fontmin.render(
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
                                        fontmin.render(
                                            f"{self.tubes[-1][0]}",
                                            fontaliased,
                                            (255, 0, 0),
                                        ),
                                        90,
                                    ),
                                    0.3,
                                    (255, 0, 0),
                                )
                                if tuple(self.tubes) in recipies.keys():
                                    for x in self.tubes:
                                        if self.invbox[x] == 1:
                                            del self.invbox[x]
                                        else:
                                            self.invbox[x] -= 1
                                    if isinstance(recipies[tuple(self.tubes)], tuple):
                                        self.invbox[recipies[tuple(self.tubes)]] = (
                                            1
                                            if recipies[tuple(self.tubes)]
                                            not in self.invbox
                                            else self.invbox[
                                                recipies[tuple(self.tubes)]
                                            ]
                                            + 1
                                        )
                                        self.result = recipies[tuple(self.tubes)][0]
                                    else:
                                        self.result = ""
                                        for x in recipies[tuple(self.tubes)]:
                                            self.invbox[x] = (
                                                1
                                                if x not in self.invbox
                                                else self.invbox[x] + 1
                                            )
                                            self.result = f"{self.result}+{x[0]}"  # ono
                                        self.result = self.result[1::]
                                    sawman.mtogg = False
                                    self.tubes = []
                                    self.update()
                            else:
                                self.tubes = []
                    itemtext = glow(
                        fontmed.render(f"{v}: {k[0]}", fontaliased, (255, 0, 0)),
                        5,
                        (255, 0, 0),
                    )
                if v < 0:
                    self.invbox.pop(k)
                screen.blit(itemtext, (420, 75 + (50 * itemdex) + self.ymov))
                itemdex += 1
                screen.blit(self.tubetext1, (1042, 220 + self.ymov))
                screen.blit(self.tubetext2, (1082, 220 + self.ymov))
                i = 0
                for r in self.result.split("+"):
                    screen.blit(
                        glow(
                            fontmin.render(r, fontaliased, (255, 0, 0)),
                            0.2,
                            (0, 0, 255),
                        ),
                        (1020, 490 + i + self.ymov),
                    )
                    i += 30

            screen.blit(
                fontmin.render(self.info, fontaliased, (255, 255, 255)),
                (60, 250 + self.ymov),
            )

            # FUCKING ZOO WEE MAMA ITEMS ARENT REAL THEYE A TUPLE
            # 0 is important
            # -1 is a chemical
            # anything else is food


class Obj:
    def __init__(self, sprite, loc, items, dialogs, collision=True):
        self.x, self.y = loc
        self.collision = collision
        self.sprite = shadow(pygame.image.load(sprite).convert_alpha(), 5, (0, 0, 0))
        self.dialogs = dialogs
        self.dialog = dialogs[0]
        self.dialen = len(self.dialog)
        self.diarender = [scroll(x) for x in [putlines(x[1]) for x in self.dialog]]
        for i in self.diarender:
            idex = self.diarender.index(i)
            for j in i:
                jdex = i.index(j)
                self.diarender[idex][jdex] = [
                    fontmed.render(k, fontaliased, (255, 255, 255))
                    for k in self.diarender[idex][jdex].split("\n")
                ]
        # print(self.diarender)
        self.items = [*items, 0]
        self.rect = pygame.Rect((self.x, self.y), self.sprite.get_size())

    def save(self):
        return (
            self.dialog,
            self.items,
            True,
        )

    def load(self, a):
        self.dialog, self.items, _ = a
        self.dialen = len(self.dialog)
        self.diarender = [scroll(x) for x in [putlines(x[1]) for x in self.dialog]]
        for i in self.diarender:
            idex = self.diarender.index(i)
            for j in i:
                jdex = i.index(j)
                self.diarender[idex][jdex] = [
                    fontmed.render(k, fontaliased, (255, 255, 255))
                    for k in self.diarender[idex][jdex].split("\n")
                ]

    def move(self, room, keys, tick, wall, entertime, ysort, offset):
        screen.blit(self.sprite, (self.x + offset[0], self.y + offset[1]))

    def textbox(self, sawman, inventory, i, ymov):
        if sawman.dindex > self.dialen:
            sawman.group = dict()
            sawman.dindex = 0
            # adddict(inventory.invbox, self.items[0])
            if not self.items[0] or inventory.invbox != adddict(
                inventory.invbox, self.items[0]
            ):
                music.unpause()
                self.dialogs = (
                    self.dialogs[1::] if len(self.dialogs) > 1 else self.dialogs
                )
                self.dialog = self.dialogs[0]
                self.dialen = len(self.dialog)
                self.diarender = [
                    scroll(x) for x in [putlines(x[1]) for x in self.dialog]
                ]
                for i in self.diarender:
                    idex = self.diarender.index(i)
                    for j in i:
                        jdex = i.index(j)
                        self.diarender[idex][jdex] = [
                            fontmed.render(k, fontaliased, (255, 255, 255))
                            for k in self.diarender[idex][jdex].split("\n")
                        ]
                if self.items[0]:
                    inventory.invbox = adddict(inventory.invbox, self.items[0])
                self.items = self.items[1::] if len(self.items) > 1 else self.items
        else:
            if self.dialog[sawman.dindex - 1][0]:
                sawman.group[self.dialog[sawman.dindex - 1][0][0]] = self.dialog[
                    sawman.dindex - 1
                ][0][1]
            for f in sorted(sawman.group.keys()):
                screen.blit(
                    pygame.image.load(
                        f"{cwd}/sprites/faces/{f}/{sawman.group[f]}.png"
                    ).convert_alpha(),
                    (0, 0),
                )
            if "cutscene" in sawman.group.keys():
                music.pause()
            screen.blit(box, (0, 480 + ymov))
            if self.dialog[sawman.dindex - 1][0]:
                match self.dialog[sawman.dindex - 1][0][0]:
                    case "sawman":
                        x_offset = 200
                    case "zweistein":
                        x_offset = 850
                    case _:
                        x_offset = 625
                text = fontmed.render(
                    self.dialog[sawman.dindex - 1][0][0].capitalize(),
                    False,
                    (255, 255, 255),
                )
                pygame.draw.rect(
                    screen,
                    (0, 0, 0, 127),
                    pygame.Rect(
                        (x_offset - 30, 440 + ymov), (text.get_width() + 60, 60)
                    ),
                    border_radius=50,
                )
                pygame.draw.rect(
                    screen,
                    (255, 0, 0),
                    pygame.Rect(
                        (x_offset - 30, 440 + ymov), (text.get_width() + 60, 60)
                    ),
                    border_radius=50,
                    width=5,
                )
                screen.blit(
                    text,
                    (x_offset, 440 + ymov),
                )
            for line in self.diarender[sawman.dindex - 1][
                min(i, len(self.diarender[sawman.dindex - 1]) - 1)
            ]:
                screen.blit(
                    line,
                    (
                        250,
                        500
                        + ymov
                        + (
                            50
                            * self.diarender[sawman.dindex - 1][
                                min(i, len(self.diarender[sawman.dindex - 1]) - 1)
                            ].index(line)
                        ),
                    ),
                )


class Chaser:
    t = 0
    collision = False

    def __init__(self, sprite, pos, speed, shock, enemies):
        self.x, self.y = self.xi, self.yi = pos
        self.speed = speed
        self.shock = shock
        self.enemies = enemies
        self.sprite, self.w, self.h = enemclip(
            shadow(pygame.image.load(sprite).convert_alpha(), 5, (0, 0, 0)), (0, 0)
        )
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def save(self):
        return (
            self.enemies,
            False,
            False,
        )

    def load(self, a):
        self.enemies, _, _ = a

    def move(self, room, keys, tick, wall, entertime, ysort, offset):
        scale = self.y / 360 if room.outside else 1
        if self.enemies:
            if tick - entertime > self.shock * 6:
                self.t = min(self.t + (0.1 * scale * self.speed / fps), 1)
                self.x, self.y = (
                    lerp(self.x, sawman.x, self.t),
                    lerp(self.y, sawman.y, self.t),
                )
            else:
                self.t = 0
                self.x, self.y = self.xi, self.yi
            print(abs(sawman.x - self.x))
            if (
                abs(sawman.x - self.x) < self.w * scale
                and not battle.enemies
                and not sawman.inenem
            ):
                music.stop()
                battle.xp = self.enemies[1]
                battle.enemies = self.enemies.copy()
                battle.aa = tick
                battle.attac = self.speed
                battle.eloc = [self.x, self.y]
                if self.speed:
                    self.enemies = ()
            if abs(sawman.x - self.x) > self.w * scale:
                sawman.inenem = False
            screen.blit(
                pygame.transform.scale(self.sprite, (self.w * scale, self.h * scale)),
                (
                    self.x + offset[0],
                    self.y + offset[1] + (self.h - self.h * scale) - 120 * scale,
                ),
            )

    def textbox(self, b, c, d, e):
        pass
        # self0enemies[1] -= 30


class Battle:
    sstate = zstate = "idle"
    oindex = opass = 0
    a = 1
    aa = 1
    attac = 0
    sawtime = zweitime = 0
    zfocus = 1
    strat = ["", ""]
    exec = False
    xp = 0
    zsked = ssked = False
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
            fontmin.render(" ".join(feederr.split()[:2:]), fontaliased, (0, 0, 0)),
            fontmin.render(" ".join(feederr.split()[3::]), fontaliased, (0, 0, 0)),
        )
        self.feederrfg = (
            fontmin.render(" ".join(feederr.split()[:2:]), fontaliased, (255, 127, 0)),
            fontmin.render(" ".join(feederr.split()[3::]), fontaliased, (255, 127, 0)),
        )
        self.shooterrbg = (
            fontmin.render(" ".join(shooterr.split()[:2:]), fontaliased, (0, 0, 0)),
            fontmin.render(" ".join(shooterr.split()[3::]), fontaliased, (0, 0, 0)),
        )
        self.shooterrfg = (
            fontmin.render(" ".join(shooterr.split()[:2:]), fontaliased, (255, 0, 255)),
            fontmin.render(" ".join(shooterr.split()[3::]), fontaliased, (255, 0, 255)),
        )
        self.locktextbg = fontmin.render(locktext, fontaliased, (0, 0, 0))
        self.locktextfg = fontmin.render(locktext, fontaliased, (255, 0, 255))

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

    def render(self, sawman, tick, keys, bgm, inventory):
        z = 0

        enemsprite, w, h = enemclip(
            pygame.image.load(
                f"{cwd}/battle/enemies/{self.enemies[0]}.png"
            ).convert_alpha(),
            self.enemstate,
        )

        self.eloc = (
            [
                lerp(self.eloc[0], 640 - (w / 2), (tick - self.aa) / 40),
                lerp(self.eloc[1], 360 - (h / 2), (tick - self.aa) / 40),
            ]
            if (tick - self.aa) < 20
            else [640 - (w / 2), 360 - (h / 2)]
        )
        self.szloc = lerp(self.szloc, 0, (tick - self.aa - 4) / 40)

        self.barloc = lerp(self.barloc, 670, (tick - self.aa - 8) / 40)

        swood = lognt(sawman.zhealth)
        zwood = lognt(sawman.zhealth)
        wood = lognt(self.enemies[1] - 1)

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

        bar(
            screen,
            int(22 * wood),
            (640, 148 + abs(((tick * wood / 10) % 10) - 5)),
            coler(self.enemies[1] + abs((tick % 50) - 25))[::-1],
        )
        bar(
            screen,
            int(22 * wood),
            (640, 150),
            coler(self.enemies[1] + abs((tick % 50) - 25)),
        )

        if (not tick % (600 >> (4 * self.exec))) and self.attac:
            self.exec = (
                0
                if (
                    self.strat == ["", ""]
                    or self.strat == ["", " skedaddle"]
                    or self.strat == [" skedaddle", ""]
                )
                else 1
            )
            self.a = tick
            self.enemstate[1] = 0
            if sawman.shealth > sawman.zhealth and not self.ssked:
                sawman.shealth -= (
                    20 * self.attac / (1 + 0.5 * (self.strat[0] == " defend"))
                )
                self.sstate = "defense"
                self.sawtime = tick
                if self.strat[0] != " skedaddle":
                    self.strat[0] = ""
            else:
                sawman.zhealth -= (
                    20 * self.attac / (1 + 0.5 * (self.strat[1] == " defend"))
                )
                self.zstate = "defense"
                self.zweitime = tick
                if self.strat[1] != " skedaddle":
                    self.strat[1] = ""
            self.enemies[1] -= (
                5
                * (self.strat[1] == " defend" or self.strat[0] == " defend")
                / (tick % 10 + 1)
            )
            if sawman.shealth < 0:
                sawman.shealth = 0
                self.sstate = "rip"
            if sawman.zhealth < 0:
                sawman.zhealth = 0
                self.zstate = "rip"

        if int((tick / self.a - 1) * 20) > 2:
            self.enemstate = [0, 0]
        else:
            self.enemstate[0] = int((tick / self.a - 1) * 10) + 1

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

        if self.exec and sawman.shealth > 0:
            match self.strat[0]:
                case " attac":
                    if self.sstate != "defense":
                        if not sfx1.get_busy():
                            sfx1.set_volume(sfxvol)
                            sfx1.play(self.sawin)
                        self.enemies[1] -= (1 + abs(swood)) / 27
                        self.enemstate[1] = 1
                        self.sstate = "offense"
                    else:
                        sfx1.set_volume(0)
                        sfx1.stop()
                        self.strat[0] = ""
                case " defend":
                    self.sstate = "defense"
                case " feed":
                    if self.sstate != "defense" and inventory.shands:
                        self.enemies[1] += inventory.shands[1]
                        self.enemstate[1] = 0
                        self.sstate = "offense"
                        if tick - self.a > 4:
                            inventory.shands = ""
                            self.strat[0] = ""
                    if not inventory.shands:
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
                        if tick - self.a > 30:
                            self.strat[0] = ""
                case " skedaddle":
                    self.ssked = True

        if not self.ssked:
            screen.blit(
                self.sawman[self.sstate],
                (-self.szloc + (((tick * int(sawman.shealth)) / 1024) % 2 - 1), 0),
            )

            bar(
                screen,
                int(12 * lognt(sawman.shealth - 1)),
                (146, self.barloc + 4),
                radius=15,
            )
            bar(
                screen,
                int(12 * lognt(sawman.shealth - 1)),
                (150, self.barloc),
                (255, 127, 0),
                15,
            )
        else:
            self.opass = 1

        if self.exec and sawman.zhealth > 0:
            match self.strat[1]:
                case " shoot":
                    if self.zstate != "defense" and inventory.zhands:
                        self.enemies[1] += (
                            inventory.zhands[1] * self.zfocus + (zwood)
                        ) / 9
                        self.enemstate[1] = 0
                        if not sfx2.get_busy():
                            sfx2.set_volume(sfxvol)
                            sfx2.play(self.bang)
                        self.zstate = "offense"
                        if tick - self.a > 4:
                            inventory.zhands = ""
                            self.strat[1] = ""
                    if not inventory.zhands:
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
                        if tick - self.a > 30:
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
                (self.szloc + (((tick * int(sawman.zhealth)) / 1024) % 2 - 1), 0),
            )
            bar(
                screen,
                int(12 * lognt(sawman.zhealth - 1)),
                (1124, self.barloc + 4),
                radius=15,
            )
            bar(
                screen,
                int(12 * lognt(sawman.zhealth - 1)),
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
            fontmed.render(
                f"{self.strat[0]}{'+' * self.exec}{'   ' * (not self.exec)}{self.strat[1]}",
                fontaliased,
                (255 * (self.exec), 0, 0),
            ),
            (584 - 24 * len(self.strat[0]), 560),
        )
        screen.blit(
            fontmed.render(
                f"{self.strat[0]}{'+' * self.exec}{'   ' * (not self.exec)}{self.strat[1]}",
                fontaliased,
                (255 * (not self.exec), 0, 0),
            ),
            (586 - 24 * len(self.strat[0]), 558),
        )

        if tick - self.a > 10:
            pullup(fontaliased, fontmin, screen, self.enemytheme[self.enemies[0]], 0)
        for o in self.options:
            if not self.ssked:
                screen.blit(
                    fontmed.render(o[0], fontaliased, (0, 0, 0)),
                    (50 - self.szloc, 360 + z),
                )
            if not self.zsked:
                screen.blit(
                    fontmed.render(o[-1], fontaliased, (0, 0, 0)),
                    (980 + self.szloc, 360 + z),
                )
            z += 50
        screen.blit(
            fontmed.render(
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
            self.enemies[1] < 5
            or self.enemies[1] - self.xp > 20
            or (self.strat == [" skedaddle", " skedaddle"] and self.exec)
        ):
            sfx1.set_volume(0)
            sfx2.set_volume(0)
            music.stop()
            self.enemstate = [0, 1]
            music.play(pygame.mixer.Sound(f"{cwd}/music/{bgm}.mp3"), -1)
            sawman.shealth += int(battle.xp) / 2
            sawman.zhealth += int(battle.xp) / 2
            sawman.money += self.moneygivers[self.enemies[0]]
            sawman.inenem = True
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
        self.intersrect = [x.sprite.get_rect(topleft=(x.x, x.y)) for x in inters]
        self.bgm = bgm if bgm else 0
        self.wall = pygame.image.load(f"{cwd}/rooms/{room}/wall.png").convert_alpha()
        self.floor = pygame.image.load(f"{cwd}/rooms/{room}/floor.png").convert_alpha()
        self.w, self.h = self.wall.get_size()
        self.mask = pygame.mask.from_surface(self.wall)
        self.portals = portals
        self.dialog = dialog
        self.dialen = len(self.dialog)
        self.diarender = [scroll(x) for x in [putlines(x[1]) for x in self.dialog]]
        for i in self.diarender:
            idex = self.diarender.index(i)
            for j in i:
                jdex = i.index(j)
                self.diarender[idex][jdex] = [
                    fontmed.render(k, fontaliased, (255, 255, 255))
                    for k in self.diarender[idex][jdex].split("\n")
                ]

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
            self.dialen = len(self.dialog)
            self.diarender = [scroll(x) for x in [putlines(x[1]) for x in self.dialog]]
            for i in self.diarender:
                idex = self.diarender.index(i)
                for j in i:
                    jdex = i.index(j)
                    self.diarender[idex][jdex] = [
                        fontmed.render(k, fontaliased, (255, 255, 255))
                        for k in self.diarender[idex][jdex].split("\n")
                    ]

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

    def textbox(self, i, ymov):
        if sawman.dindex > self.dialen:
            self.dialen = self.dialog = sawman.dindex = 0
        else:
            if self.dialog[sawman.dindex - 1][0]:
                sawman.group[self.dialog[sawman.dindex - 1][0][0]] = self.dialog[
                    sawman.dindex - 1
                ][0][1]
            for f in sorted(sawman.group.keys()):
                screen.blit(
                    pygame.image.load(
                        f"{cwd}/sprites/faces/{f}/{sawman.group[f]}.png"
                    ).convert_alpha(),
                    (0, 0 + ymov),
                )
            screen.blit(box, (0, 480 + ymov))
            if self.dialog[sawman.dindex - 1][0]:
                match self.dialog[sawman.dindex - 1][0][0]:
                    case "sawman":
                        x_offset = 200
                    case "zweistein":
                        x_offset = 850
                    case _:
                        x_offset = 625
                text = fontmed.render(
                    self.dialog[sawman.dindex - 1][0][0].capitalize(),
                    False,
                    (255, 255, 255),
                )
                pygame.draw.rect(
                    screen,
                    (0, 0, 0, 127),
                    pygame.Rect(
                        (x_offset - 30, 440 + ymov), (text.get_width() + 60, 60)
                    ),
                    border_radius=50,
                )
                pygame.draw.rect(
                    screen,
                    (255, 0, 0),
                    pygame.Rect(
                        (x_offset - 30, 440 + ymov), (text.get_width() + 60, 60)
                    ),
                    border_radius=50,
                    width=5,
                )
                screen.blit(
                    text,
                    (x_offset, 440 + ymov),
                )
            for line in self.diarender[sawman.dindex - 1][
                min(i, len(self.diarender[sawman.dindex - 1]) - 1)
            ]:
                screen.blit(
                    line,
                    (
                        250,
                        500
                        + ymov
                        + (
                            50
                            * self.diarender[sawman.dindex - 1][
                                min(i, len(self.diarender[sawman.dindex - 1]) - 1)
                            ].index(line)
                        ),
                    ),
                )


class Portal:
    def __init__(self, pos, dim, rindex, nloc):
        self.door = pygame.Rect(
            (pos[0] - (dim[0] / 2), pos[1] - (dim[0] / 2)), (dim[0], dim[1])
        )
        self.rindex = rindex
        self.nloc = (nloc[0], nloc[1])

    def changeroom(self):
        sawman.x, sawman.y = self.nloc
        zwei.poss = [self.nloc]
        return self.rindex


class Trader:
    collision = True
    diarender = ("", "")

    def __init__(self, sprite, loc, shopman, menu):
        self.x, self.y = loc
        self.sprite = pygame.image.load(sprite).convert_alpha()
        self.rect = pygame.Rect((self.x, self.y), self.sprite.get_size())
        self.shopui = pygame.image.load("ui/shop.png").convert_alpha()
        self.shopman = pygame.image.load(shopman).convert()
        self.menu = menu

    def textbox(self, sawman, inventory, i, ymov):
        screen.blit(self.shopman, (0, 0))
        screen.blit(self.shopui, (0, ymov * 1.2))
        itemdex = 0
        mpos = pygame.mouse.get_pos()
        if sawman.dindex == 2:
            sawman.dindex = 0
            pygame.mouse.set_visible(False)
            mouses = 0, 0, 0
        else:
            pygame.mouse.set_visible(True)
            mouses = pygame.mouse.get_pressed()
            for k, v in self.menu.items():
                itemtext = fontmed.render(f"{k[0]}: ௹{v}", fontaliased, (255, 255, 255))
                if (
                    itemtext.get_rect(topleft=(750, 50 + (60 * itemdex))).collidepoint(
                        mpos
                    )
                    and sawman.mtogg
                ):
                    itemtext = glow(
                        fontmed.render(
                            f"{k[0]}: ௹{v} ({inventory.invbox[k] if k in inventory.invbox else 0})",
                            fontaliased,
                            (255, 0, 0),
                        ),
                        5,
                        (255, 0, 0),
                    )
                    match mouses:
                        case (1, _, _):
                            if k in inventory.invbox:
                                inventory.invbox[k] += 1
                                sawman.money -= v
                            else:
                                inventory.invbox[k] = 1
                            sawman.mtogg = False
                        case (_, _, 1):
                            if k in inventory.invbox:
                                if inventory.invbox[k] == 1:
                                    del inventory.invbox[k]
                                else:
                                    inventory.invbox[k] -= 1
                                    sawman.money += v * 0.9
                            sawman.mtogg = False

                screen.blit(itemtext, (750, 50 + (60 * itemdex) + ymov))
                itemdex += 1

    def load(a, aa):
        pass

    def save(a):
        pass

    def move(self, room, keys, tick, wall, entertime, ysort, offset):
        screen.blit(self.sprite, (self.x + offset[0], self.y + offset[0]))


class Button:
    def __init__(self, id, pos, dim, thicc):
        self.id = id
        self.pos = pos
        self.dim = dim
        self.thicc = thicc
        self.brect = pygame.Rect(
            self.pos[0] - (self.dim[0] * uiscale / 2),
            self.pos[1],
            self.dim[0] * uiscale,
            self.dim[1] * uiscale,
        )

    def draw(self, screen, mpos, mtogg, tab, settings_json):
        if pygame.Rect.collidepoint(self.brect, mpos):
            pygame.draw.rect(
                screen,
                (255, 0, 0),
                pygame.Rect(
                    self.pos[0] - (self.dim[0] * uiscale / 2),
                    self.pos[1] - (self.thicc * uiscale),
                    self.dim[0] * uiscale,
                    self.dim[1] * uiscale + (self.thicc * uiscale * 2),
                ),
            )
            pygame.draw.circle(
                screen,
                (255, 0, 0),
                (
                    self.pos[0] - (self.dim[0] * uiscale / 2),
                    self.pos[1] + (self.dim[1] * uiscale / 2),
                ),
                (self.dim[1] * uiscale / 2) + self.thicc * uiscale,
            )
            pygame.draw.circle(
                screen,
                (255, 0, 0),
                (
                    self.pos[0] + (self.dim[0] * uiscale / 2),
                    self.pos[1] + (self.dim[1] * uiscale / 2),
                ),
                (self.dim[1] * uiscale / 2) + self.thicc * uiscale,
            )

        pygame.draw.rect(
            screen,
            (0, 0, 0),
            self.brect,
        )
        pygame.draw.circle(
            screen,
            (0, 0, 0),
            (
                self.pos[0] - (self.dim[0] * uiscale / 2),
                self.pos[1] + (self.dim[1] * uiscale / 2),
            ),
            (self.dim[1] * uiscale / 2),
        )
        pygame.draw.circle(
            screen,
            (0, 0, 0),
            (
                self.pos[0] + (self.dim[0] * uiscale / 2),
                self.pos[1] + (self.dim[1] * uiscale / 2),
            ),
            (self.dim[1] * uiscale / 2),
        )

        text = (
            f"{self.id}: {settings_json[self.id]}"
            if self.id in settings_json
            else self.id
        )
        font_render = fontmin.render(
            text,
            fontaliased,
            (255, 0, 0)
            if pygame.Rect.collidepoint(self.brect, mpos) and mtogg
            else (255, 255, 255),
        )
        screen.blit(
            font_render,
            (
                self.pos[0] - (font_render.get_width() / 2),
                self.pos[1] + (self.thicc * uiscale),
            ),
        )

        if pygame.Rect.collidepoint(self.brect, mpos) and mtogg:
            return self.id


x = 1280
y = 720
keys = pygame.key.get_pressed()
sawman = Chara((x, y), f"{cwd}/sprites/sawman.png")
zwei = Zweistein((x, y), f"{cwd}/sprites/zweistein.png")
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
