import pygame
from func import pullup, _apply_glow, _add_glitch_effect, _apply_flicker
from pygame.math import lerp
from PygameShader.shader import chromatic
from classes import (
    sawman,
    zwei,
    battle,
    inventory,
    Button,
    screen,
    cwd,
    music,
    nighttime,
)
from levels import levels
from settings import debug_mode, fps, mvol, fontaliased, scrollinvert
from json import load, dump


with open("settings.json") as json_data:
    settings_json = load(json_data)
    scrollinvert = settings_json["Scroll Invert"]


portaldimensions = [(0, 0)]
pw, ph = portaldimensions[0]


tbstart = 0
interymov = 600
roomymov = 600
print(nighttime.strftime("%H %m %p"))

box = pygame.image.load(f"{cwd}/ui/textbox.png").convert_alpha()
invui = pygame.image.load(f"{cwd}/ui/inventory.png").convert_alpha()
invanim = range(0, 27)

fontmed = pygame.font.Font(f"{cwd}/ui/Soilad.otf", 48)
fontmin = pygame.font.Font(f"{cwd}/ui/Soilad.otf", 24)

keys = pygame.key.get_pressed()

tick = mscroll = indoor = laterdays = 0


latertextbg = (
    fontmed.render("Later days.", fontaliased, (0, 0, 0)),
    fontmed.render("Later days..", fontaliased, (0, 0, 0)),
    fontmed.render("Later days...", fontaliased, (0, 0, 0)),
    fontmed.render("", fontaliased, (0, 0, 0)),
)
latertextfg = (
    fontmed.render("Later days.", fontaliased, (255, 255, 255)),
    fontmed.render("Later days..", fontaliased, (255, 255, 255)),
    fontmed.render("Later days...", fontaliased, (255, 255, 255)),
    fontmed.render("", fontaliased, (255, 255, 255)),
)
run = True
menu = True
settings = False
game = False
menubg = pygame.image.load(f"{cwd}/ui/menu.png")
tab = [1]

tick = mscroll = 0
mtogg = False

menubuttons = [
    Button("Start Game", (200, 200), (160, 40), 5),
    Button("Continue Game", (200, 250), (160, 40), 5),
    Button("Settings", (200, 300), (160, 40), 5),
    Button("Credits", (200, 350), (160, 40), 5),
    Button("Exit", (200, 400), (160, 40), 5),
]

settingsbuttons = [
    Button("UI Size", (200, 200), (160, 40), 5),
    Button("FPS", (200, 250), (160, 40), 5),
    Button("Sound Volume", (200, 300), (160, 40), 5),
    Button("Music Volume", (200, 350), (160, 40), 5),
    Button("Scroll Invert", (200, 400), (160, 40), 5),
    Button("Exit", (200, 450), (160, 40), 5),
]
night = pygame.image.load(f"{cwd}/ui/night.png").convert()

while run:
    while menu:
        if not run:
            break
        screen.blit(menubg, (0, 0))
        mpos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    run = False
                case pygame.KEYUP:
                    match event.key:
                        case pygame.K_F4:
                            pygame.display.toggle_fullscreen()
                case pygame.MOUSEWHEEL:
                    mscroll = -scrollinvert * event.y
                    mtogg = True
                case pygame.MOUSEBUTTONDOWN:
                    mscroll = 0
                    mtogg = True
                case pygame.MOUSEBUTTONUP:
                    mscroll = 0
                    mtogg = False

        for i in menubuttons:
            if i.draw(screen, mpos, mtogg, tab, settings_json):
                tab = i.draw(screen, mpos, mtogg, tab, settings_json)

        match tab:
            case "Start Game":
                game = True
                menu = False
                mtogg = False
                tab = 0
            case "Continue Game":
                game = True
                print(1)
                try:
                    with open(f"{cwd}/save.txt", "r") as save:
                        savedata = save.read()
                        if savedata:
                            savelevels = eval(savedata)
                            for i in range(0, len(levels)):
                                levels[i].load(savelevels[i])
                    with open(f"{cwd}/saveinventory.txt", "r") as save:
                        savedata = save.read()
                        if savedata:
                            inventory.load(eval(savedata))

                    with open(f"{cwd}/sawloc.txt", "r") as save:
                        savedata = save.read()
                        if savedata:
                            sawman.load(eval(savedata))
                    with open(f"{cwd}/zweiloc.txt", "r") as save:
                        savedata = save.read()
                        if savedata:
                            zwei.load(eval(savedata))
                except FileNotFoundError:
                    pass
                menu = False
                mtogg = False
                tab = 0

            case "Settings":
                settings = True
            case "Exit":
                run = False
        tab = 0
        if settings:
            for i in settingsbuttons:
                if i.draw(screen, mpos, mtogg, tab, settings_json):
                    tab = i.draw(screen, mpos, mtogg, tab, settings_json)
            match tab:
                case "Exit":
                    settings = False
                    menu = True
                case "UI Size":
                    settings_json["UI Size"] = max(
                        min(settings_json["UI Size"] + mscroll, 40), 14
                    )
                case "Scroll Invert":
                    settings_json["Scroll Invert"] = (
                        max(min(settings_json["Scroll Invert"] + mscroll, 1), 0) * -2
                        + 1
                    )
                case "Sound Volume":
                    settings_json["Sound Volume"] = max(
                        min(settings_json["Sound Volume"] + mscroll, 100), 0
                    )
                case "Music Volume":
                    settings_json["Music Volume"] = max(
                        min(settings_json["Music Volume"] + mscroll, 100), 0
                    )
                case "FPS":
                    settings_json["FPS"] = max(settings_json["FPS"] + mscroll, 12)
            with open("settings.json", "w") as json_data:
                dump(settings_json, json_data)

            mtogg = False
            tab = 0

        pygame.time.Clock().tick(settings_json["FPS"])
        pygame.display.update()

    pygame.mouse.set_visible(False)

    room = levels[sawman.rindex]
    portals = room.portals
    wall = room.mask
    aaa = list(
        dict.fromkeys(
            [
                y
                for y in [x.bgm for x in levels][: sawman.rindex :]
                if not isinstance(y, int)
            ]
        )
    )
    bgm = room.bgm if not isinstance(room.bgm, int) else aaa[-1]
    music.play(pygame.mixer.Sound(f"{cwd}/music/{bgm}.mp3"), -1)
    entertime = tick
    if tick - entertime < 10:
        pullup(fontaliased, fontmin, screen, bgm, tick - entertime)
    room.render()
    ysort = sorted(room.inters + [sawman, zwei], key=lambda r: r.y)
    pygame.display.update()

    music.set_volume(mvol)

    while game:
        if not run:
            break
        if not battle.enemies:
            room.render()
            for item in ysort:
                item.move(room, keys, tick, wall, entertime, ysort)
            if room.inters:
                for inter in room.inters:
                    # pygame.draw.rect(screen, (255,0,0),inter.rect)
                    ysort = sorted(room.inters + [sawman, zwei], key=lambda r: r.y)
                    if pygame.Rect.collidepoint(
                        inter.rect, (sawman.xf + 50, sawman.yf)
                    ):
                        if sawman.dindex:
                            sawman.stop = True
                            inter.textbox(
                                sawman,
                                inventory,
                                int((tick - tbstart) * 1.2),
                                interymov,
                            )
                            interymov = (
                                round(lerp(interymov, 300, (tick - tbstart) / 45))
                                if inter.diarender[sawman.dindex - 1] == "..."
                                else round(lerp(interymov, 0, (tick - tbstart) / 45))
                            )

                        else:
                            sawman.stop = False
                            interymov = round(
                                lerp(interymov, 300, (tick - tbstart) / 45)
                            )
            else:
                ysort = sorted([sawman, zwei], key=lambda r: r.y)

        else:
            # print(battle.enemies)
            battle.render(sawman, tick, keys, bgm, inventory)
            screen.blit(
                chromatic(
                    screen,
                    640,
                    360,
                    1 + (0.001 * (abs((tick % 65) - 32) / 8)),
                    fx=0.001 * (abs((tick % 65) - 32) / 4),
                ),
                (0, 0),
            )
            if not (sawman.shealth or sawman.zhealth):
                game = False
                pygame.mouse.set_visible(not pygame.mouse.get_visible())
                menu = True
        if room.dialog:
            sawman.dindex = 1 if not sawman.dindex else sawman.dindex
            sawman.stop = True
            roomymov = int(lerp(roomymov, 0, (tick - entertime) / 45))
            room.textbox(tick - tbstart, roomymov)
        elif not room.dialog:
            sawman.stop = False
            roomymov = 600
        if nighttime.strftime("%p") == "PM" and room.outside and not battle.enemies:
            screen.blit(night, (0, 0), special_flags=pygame.BLEND_SUB)
        inventory.open(sawman, mscroll, tick)
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            match event.type:
                case pygame.QUIT:
                    run = False
                case pygame.MOUSEBUTTONUP:
                    sawman.mtogg = True
                case pygame.MOUSEWHEEL:
                    mscroll = min(
                        max(mscroll - scrollinvert * event.y, 0),
                        len(inventory.invbox.copy()) - 1,
                    )
                case pygame.KEYUP:
                    match event.key:
                        case pygame.K_RETURN | pygame.K_z:
                            sawman.dindex += 1
                            tbstart = tick
                        case pygame.K_TAB | pygame.K_c:
                            inventory.update()
                            inventory.tubes = []
                            inventory.tubetext1 = inventory.tubetext2 = fontmin.render(
                                "", fontaliased, (225, 0, 0)
                            )
                            pygame.mouse.set_visible(not pygame.mouse.get_visible())
                            inventory.invshow = not inventory.invshow
                            music.set_volume(mvol / (1 + inventory.invshow))
                            inventory.a = tick

                        case pygame.K_F4:
                            pygame.display.toggle_fullscreen()
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_F5:
                            if not battle.enemies:
                                laterdays = tick
                                with open(f"{cwd}/save.txt", "w") as save:
                                    save.write(str([level.save() for level in levels]))
                                with open(f"{cwd}/saveinventory.txt", "w") as save:
                                    save.write(str(inventory.save()))
                                with open(f"{cwd}/sawloc.txt", "w") as save:
                                    save.write(str(sawman.save()))
                                with open(f"{cwd}/zweiloc.txt", "w") as save:
                                    save.write(str(zwei.save()))
                        case pygame.K_s | pygame.K_DOWN:
                            battle.oindex = (battle.oindex + 1) % 4
                        case pygame.K_w | pygame.K_UP:
                            battle.oindex = (battle.oindex - 1) % 4
                        case pygame.K_d | pygame.K_RIGHT:
                            battle.opass = (battle.opass + 1) % 2
                        case pygame.K_a | pygame.K_LEFT:
                            battle.opass = (battle.opass - 1) % 2
                        case pygame.K_SPACE:
                            battle.exec = bool(
                                (battle.strat[0] or battle.ssked)
                                and (battle.strat[1] or battle.zsked)
                            )
                            battle.a = tick
                        case pygame.K_BACKQUOTE:
                            pygame.mouse.set_visible(not pygame.mouse.get_visible())

        for portal in portals:
            # print(sawman.x+50,sawman.y+239)
            # print(sawman.dindex)
            # print(pygame.mouse.get_pos())
            # print("wazdorf")
            if debug_mode and pygame.mouse.get_visible():
                pygame.draw.rect(screen, (255, 0, 0), portal.door)

                if pygame.mouse.get_pressed() == (1, 0, 0):
                    portaldimensions.append(pygame.mouse.get_pos())
                    print("npc stuff", portaldimensions[1], portaldimensions[-1])
                    pos = (
                        min(portaldimensions[1][0], portaldimensions[-1][0]),
                        min(portaldimensions[1][1], portaldimensions[-1][1]),
                    )
                    pw = abs(portaldimensions[-1][0] - portaldimensions[1][0])
                    ph = abs(portaldimensions[-1][1] - portaldimensions[1][1])
                    print(
                        "portal stuff",
                        (
                            portaldimensions[1][0] + (pw / 2),
                            portaldimensions[1][1] + (ph / 2),
                        ),
                        (
                            pw,
                            ph,
                        ),
                    )
                    pygame.draw.rect(
                        screen,
                        (255, 0, 0),
                        pygame.Rect(pos, (pw, ph)),
                    )
                else:
                    portaldimensions = [(0, 0)]

            if (
                pygame.Rect.collidepoint(portal.door, (sawman.x + 50, sawman.y + 230))
                and not indoor
            ):
                sawman.rindex = portal.changeroom()
                indoor = True
                room = levels[sawman.rindex]
                portals = room.portals
                entertime = tick
                ysort = sorted(room.inters + [sawman, zwei], key=lambda r: r.y)
                wall = room.mask
                if room.bgm and room.bgm != bgm:
                    bgm = room.bgm
                    music.play(pygame.mixer.Sound(f"{cwd}/music/{bgm}.mp3"), -1)
            elif not pygame.Rect.collidepoint(
                portal.door, (sawman.x + 50, sawman.y + 230)
            ):
                indoor = False
        if tick - entertime < 100 and room.bgm:
            pullup(fontaliased, fontmin, screen, bgm, tick - entertime)
        screen.blit(
            latertextbg[min(tick - laterdays, 100) // 30],
            (((tick - 3) / 8) % 2, ((tick - 3) / 4) % 3),
        )
        screen.blit(
            latertextfg[min(tick - laterdays, 100) // 30],
            ((tick / 8) % 2, (tick / 2) % 3),
        )
        # if fontaliased:
        #     _apply_glow(screen, 1280, 720)
        # # shader_bloom_fast1(screen, threshold_=400, smooth_=1)
        # _add_glitch_effect(screen, 1, battle.enemies, 1280, 720)
        # _apply_flicker(screen, tick)
        pygame.display.update()
        pygame.time.Clock().tick(fps)
        tick += 1
pygame.display.quit()
pygame.quit()
