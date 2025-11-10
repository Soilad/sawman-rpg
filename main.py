import pygame
from func import pullup, _apply_glow, _add_glitch_effect, _apply_flicker
from pygame.math import clamp, lerp
from enum import Enum, auto, IntEnum
from PygameShader.shader import chromatic
from classes import (
    Room,
    player_vars,
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


class Menu(Enum):
    MAIN_MENU = auto()
    SETTINGS = auto()
    CREDITS = auto()
    GAME = auto()
    ESCAPEMENU = auto()


current_menu = Menu.MAIN_MENU


with open("settings.json") as json_data:
    settings_json = load(json_data)


portal_size: list[tuple[int,int]] = [(0, 0)]
pw, ph = portal_size[0]


initial_textbox_tick: int = 0
textbox_y: int = 600
print(nighttime.strftime("%H %m %p"))

textbox_surface: pygame.Surface = pygame.image.load(f"{cwd}/ui/textbox.png").convert_alpha()
inventory_surface: pygame.Surface = pygame.image.load(f"{cwd}/ui/inventory.png").convert_alpha()

font_medium = pygame.font.Font(f"{cwd}/ui/Soilad.ttf", 48)
font_small = pygame.font.Font(f"{cwd}/ui/Soilad.ttf", 24)

keys = pygame.key.get_pressed()

tick: int = 0
in_door: bool = False
laterdays: int = 0

latertextbg: tuple[pygame.Surface] = (
    font_medium.render("Later days.", fontaliased, (0, 0, 0)),
    font_medium.render("Later days..", fontaliased, (0, 0, 0)),
    font_medium.render("Later days...", fontaliased, (0, 0, 0)),
    font_medium.render("", fontaliased, (0, 0, 0)),
)
latertextfg = (
   font_medium.render("Later days.", fontaliased, (255, 255, 255)),
   font_medium.render("Later days..", fontaliased, (255, 255, 255)),
   font_medium.render("Later days...", fontaliased, (255, 255, 255)),
   font_medium.render("", fontaliased, (255, 255, 255)),
)
run: bool = True
menu_bg: pygame.Surface = pygame.image.load(f"{cwd}/ui/bg{nighttime.strftime('%p').lower()}.png")
tab = [1] # tf is tab

tick: int = 0
m_scroll: int = 0
b_scroll: int = 0
m_togg: bool = False
b_togg: bool = False

menu_buttons: tuple[Button] = (
    Button("Start Game", (200, 200), (160, 40), 5),
    Button("Continue Game", (200, 250), (160, 40), 5),
    Button("Settings", (200, 300), (160, 40), 5),
    Button("Credits", (200, 350), (160, 40), 5),
    Button("Exit", (200, 400), (160, 40), 5),
)

settings_buttons: tuple[Button] = (
    Button("UI Size", (200, 200), (160, 40), 5),
    Button("FPS", (200, 250), (160, 40), 5),
    Button("Sound Volume", (200, 300), (160, 40), 5),
    Button("Music Volume", (200, 350), (160, 40), 5),
    Button("Scroll Invert", (200, 400), (160, 40), 5),
    Button("Exit", (200, 450), (160, 40), 5),
)

night: pygame.Surface = pygame.image.load(f"{cwd}/ui/night.png").convert()


current_room: Room = levels[player_vars.room_index]
portals = current_room.portals
wall = current_room.mask
aaa = list(
    dict.fromkeys(
        [
            y
            for y in [x.bgm for x in levels][: player_vars.room_index :]
            if not isinstance(y, int)
        ]
    )
)
bgm = current_room.bgm if not isinstance(current_room.bgm, int) else aaa[-1]
music.play(pygame.mixer.Sound(f"{cwd}/music/{bgm}.mp3"), -1)
entertime = tick
if tick - entertime < 10:
    pullup(fontaliased, font_small, screen, bgm, tick - entertime)
camera_x = camera_y = 0
current_room.render(camera_x, camera_y)
if current_room.h != 720:
    if sawman.dx or sawman.dy:
        camera_x, camera_y = (camera_x, camera_y) - sawman.final_position + (640, 360)
    else:
        camera_x = camera_y = 0

ysort = sorted(current_room.inters + [sawman, zwei], key=lambda r: r.current_position.y)
pygame.display.update()

keydown = False

music.set_volume(mvol)


while run:
    if (current_menu == Menu.MAIN_MENU) or (current_menu == Menu.SETTINGS):
        screen.blit(menu_bg, (0, 0))
    mpos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    b_togg = False

    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                run = False
            case pygame.MOUSEWHEEL:
                b_scroll = settings_json["Scroll Invert"] * event.y
                m_scroll = min(
                    max(m_scroll - scrollinvert * event.y, 0),
                    len(inventory.inventory_dict.copy()) - 1,
                )
                b_togg = True
            case pygame.MOUSEBUTTONDOWN:
                m_scroll = 0
                b_togg = True
            case pygame.MOUSEBUTTONUP:
                m_scroll = 0
                b_togg = False
                m_togg = True
            case pygame.KEYUP:
                keydown = False
                match event.key:
                    case pygame.K_RETURN | pygame.K_z:
                        player_vars.dialog_index += 1
                        initial_textbox_tick = tick
                    case pygame.K_TAB | pygame.K_c:
                        inventory.update_items()
                        inventory.update_health(player_vars)
                        inventory.tubes = []
                        pygame.mouse.set_visible(not pygame.mouse.get_visible())
                        inventory.SHOW_INVENTORY = not inventory.SHOW_INVENTORY
                        music.set_volume(mvol / (1 + inventory.SHOW_INVENTORY))
                        inventory.initial_open = tick

                    case pygame.K_F4:
                        pygame.display.toggle_fullscreen()
            case pygame.KEYDOWN:
                keydown = True
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

    match current_menu:
        case Menu.MAIN_MENU:
            for i in menu_buttons:
                if i.draw(screen, mpos, b_togg, tab, settings_json):
                    tab = i.draw(screen, mpos, b_togg, tab, settings_json)

            match tab:
                case "Start Game":
                    current_menu = Menu.GAME
                    m_togg = False
                    tab = 0
                    pygame.mouse.set_visible(False)

                case "Continue Game":
                    current_menu = Menu.GAME
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
                    m_togg = False
                    tab = 0
                    pygame.mouse.set_visible(False)

                case "Settings":
                    current_menu = Menu.SETTINGS
                case "Exit":
                    run = False
                    pygame.quit()
            tab = 0
        case Menu.SETTINGS:
            for i in settings_buttons:
                if i.draw(screen, mpos, b_togg, tab, settings_json):
                    tab = i.draw(screen, mpos, b_togg, tab, settings_json)
            match tab:
                case "Scroll Invert":
                    settings_json["Scroll Invert"] *= -1
                case "UI Size":
                    settings_json["UI Size"] += b_scroll * (
                        1 + 9 * keys[pygame.K_LSHIFT]
                    )
                    settings_json["UI Size"] = clamp(settings_json["UI Size"], 14, 40)
                case "Sound Volume":
                    settings_json["Sound Volume"] += b_scroll * (
                        1 + 9 * keys[pygame.K_LSHIFT]
                    )
                    settings_json["Sound Volume"] = clamp(
                        settings_json["Sound Volume"], 0, 100
                    )
                case "Music Volume":
                    settings_json["Music Volume"] += b_scroll * (
                        1 + 9 * keys[pygame.K_LSHIFT]
                    )
                    settings_json["Music Volume"] = clamp(
                        settings_json["Music Volume"], 0, 100
                    )

                    pygame.mixer.music.set_volume(settings_json["Music Volume"] / 100)

                case "FPS":
                    settings_json["FPS"] += b_scroll * (1 + 9 * keys[pygame.K_LSHIFT])
                    settings_json["FPS"] = clamp(settings_json["FPS"], 12, 999)

                case "Exit":
                    current_menu = Menu.MAIN_MENU

            with open("settings.json", "w") as json_data:
                dump(settings_json, json_data)

            tab = 0

        case Menu.GAME:
            if not battle.enemies:
                current_room.render(camera_x, camera_y)
                if current_room.h != 720:
                        if pygame.math.Vector2.length_squared(sawman.delta_position):
                            camera_x, camera_y = (camera_x, camera_y) - sawman.final_position + (640, 360)
                            camera_x = clamp(-(sawman.final_position.x - 640), current_room.w // -2, current_room.w // 2)
                            camera_y = clamp(-(sawman.final_position.y - 360), current_room.h // -2, current_room.h // 2)
                else:
                    camera_x = camera_y = 0

                for item in ysort:
                    item.move(
                        player_vars, current_room, keys, tick, wall, entertime, ysort, (camera_x, camera_y)
                    )

                if debug_mode:
                    pygame.draw.circle(screen, (255, 127, 0), (sawman.current_position + (50 * sawman.scale, 239 - (125 * sawman.scale))), 4)
                if current_room.inters:
                    for inter in current_room.inters:
                        # pygame.draw.rect(screen, (255,0,0),inter.rect)

                        if keydown:
                            ysort = sorted(
                                current_room.inters + [sawman, zwei], key=lambda r: r.current_position.y
                            )
                        if pygame.Rect.collidepoint(
                            inter.rect, sawman.final_position + (50, 0)
                        ):
                            if player_vars.dialog_index:
                                sawman.stop = True
                                inter.textbox(
                                    textbox_surface,
                                    player_vars,
                                    inventory,
                                    b_togg,
                                    int((tick - initial_textbox_tick) * 1.2),
                                    textbox_y,
                                )
                                textbox_y = round(lerp(textbox_y, 300 if inter.dialog[player_vars.dialog_index - 1][1] == "..." else 0, (tick - initial_textbox_tick) / 45))
                            else:
                                sawman.stop = False
                                textbox_y = round(
                                    lerp(textbox_y, 300, (tick - initial_textbox_tick) / 45)
                                )
                else:
                    ysort = sorted([sawman, zwei], key=lambda r: r.current_position.y)

            else:
                # print(battle.enemies)
                battle.render(player_vars, tick, keys, bgm, inventory)
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
                if not (player_vars.s_health or player_vars.z_health):
                    game = False
                    pygame.mouse.set_visible(not pygame.mouse.get_visible())
                    menu = True
            if current_room.dialog:
                player_vars.dialog_index = 1 if not player_vars.dialog_index else player_vars.dialog_index
                sawman.stop = True
                textbox_y = int(lerp(textbox_y, 0, (tick - entertime) / 45))
                current_room.textbox(player_vars, tick - initial_textbox_tick, textbox_y)
            elif not current_room.dialog:
                sawman.stop = False
                # textbox_y = 600
            if nighttime.strftime("%p") == "PM" and current_room.outside and not battle.enemies:
                screen.blit(night, (0, 0), special_flags=pygame.BLEND_SUB)
            inventory.open(player_vars, m_scroll, b_togg, tick)

            for portal in portals:
                # print(sawman.x+50,sawman.y+239)
                # print(player_vars.dialog_index)
                # print(pygame.mouse.get_pos())
                # print("wazdorf")
                if debug_mode and pygame.mouse.get_visible():
                    pygame.draw.rect(screen, (255, 0, 0), portal.door)

                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        portal_size.append(pygame.mouse.get_pos())
                        print("npc stuff", portal_size[1], portal_size[-1])
                        pos = (
                            min(portal_size[1][0], portal_size[-1][0]),
                            min(portal_size[1][1], portal_size[-1][1]),
                        )
                        pw = abs(portal_size[-1][0] - portal_size[1][0])
                        ph = abs(portal_size[-1][1] - portal_size[1][1])
                        print(
                            "portal stuff",
                            (
                                portal_size[1][0] + (pw / 2),
                                portal_size[1][1] + (ph / 2),
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
                        portal_size = [(0, 0)]

                # print(in_door)
                if pygame.Rect.collidepoint(portal.door, sawman.current_position + (50, 230)):
                    if not in_door:
                        player_vars.current_position = sawman.current_position = zwei.current_position = portal.new_position
                        zwei.positions_list = [portal.new_position]
                        player_vars.room_index = portal.room_index
                        in_door = True
                        current_room = levels[player_vars.room_index]
                        portals = current_room.portals
                        entertime = tick
                        print(*(r.current_position for r in current_room.inters))
                        ysort = sorted(current_room.inters + [sawman, zwei], key=lambda r: r.current_position.y)
                        wall = current_room.mask
                        if current_room.bgm and current_room.bgm != bgm:
                            bgm = current_room.bgm
                            music.play(pygame.mixer.Sound(f"{cwd}/music/{bgm}.mp3"), -1)
                    else:
                        in_door = False
                else:
                    in_door = False
            if tick - entertime < 100 and current_room.bgm:
                pullup(fontaliased, font_small, screen, bgm, tick - entertime)
            screen.blit(
                latertextbg[min(tick - laterdays, 100) // 30],
                (((tick - 3) / 8) % 2, ((tick - 3) / 4) % 3),
            )
            screen.blit(
                latertextfg[min(tick - laterdays, 100) // 30],
                ((tick / 8) % 2, (tick / 2) % 3),
            )
            if fontaliased:
                _apply_glow(screen, 1280, 720)
            # shader_bloom_fast1(screen, threshold_=400, smooth_=1)
            _add_glitch_effect(screen, 1, battle.enemies, 1280, 720)
            _apply_flicker(screen, tick)
            tick += 1
    pygame.time.Clock().tick(settings_json["FPS"])
    pygame.display.update()


pygame.display.quit()
pygame.quit()
