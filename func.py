from pygame import (
    Rect,
    draw,
    transform,
    Surface,
    SRCALPHA,
    BLEND_RGBA_ADD,
    BLEND_RGBA_MIN,
)
import random


def scroll(s):
    l = []
    for i in range(len(s) + 1):
        l.append(s[:i])
    return l


def glow(surface, thicc, color):
    opacity = 255
    if isinstance(thicc, float):
        opacity = round((thicc % 1) * 255)
        thicc = round(thicc + 1)
    b = Surface(
        (surface.get_width() + (4 * thicc), surface.get_height() + (4 * thicc)),
        flags=SRCALPHA,
    )
    a = b.copy()
    b.blit(surface)
    transform.gaussian_blur(b, thicc, dest_surface=a)
    a.fill(color, special_flags=BLEND_RGBA_MIN)
    a.set_alpha(opacity)
    a.blit(surface)
    return a


def shadow(surface, thicc, color):
    b = Surface(
        (surface.get_width() + 4 * thicc, surface.get_height() + 4 * thicc),
        flags=SRCALPHA,
    )
    a = b.copy()
    b.blit(surface, (0, 0))
    transform.gaussian_blur(b, thicc, dest_surface=a)
    a.fill(color, special_flags=BLEND_RGBA_MIN)
    a.blit(surface, (0, 0))
    return a


# def clip(surface, x, y):
#     handle_surface = surface.copy()
#     clipRect = Rect(x, y, 100, 239)
#     handle_surface.set_clip(clipRect)
#     image = surface.subsurface(handle_surface.get_clip())
#     return image.copy().convert_alpha()

def clip(surface: Surface , sprite_width: int, sprite_height: int) -> dict[tuple[int,int]:Surface]:
    spritesheet_dict: dict = {}
    sheet_width, sheet_height = surface.get_size()
    for x in range(sheet_width//sprite_width + 1):
        for y in range(sheet_height//sprite_height + 1):
            clipRect = Rect(x*sprite_width, y*sprite_height, sprite_width, sprite_height)
            surface.set_clip(clipRect)
            image = surface.subsurface(surface.get_clip())
            spritesheet_dict[(x,y)] = image.convert_alpha()
    return spritesheet_dict



def enemclip(surface, pos):
    handle_surface = surface.copy()
    w, h = handle_surface.get_size()
    clipRect = Rect(pos[0] * w // 3, pos[1] * h // 2, w // 3, h // 2)
    handle_surface.set_clip(clipRect)
    image = surface.subsurface(handle_surface.get_clip())
    give_items,
    return image.copy().convert_alpha(), w // 3, h // 2


def lerp(i, f, t, thresh=20):
    return i * (1 - t) + f * (t) if t <= 1 else f


def coler(x):
    # x = x * 3 / 50
    return (
        (max(min(abs(((x - 240) % 360) - 180), 120), 60) - 60) * 255 / 60,
        (max(min(abs(((x - 120) % 360) - 180), 120), 60) - 60) * 255 / 60,
        (max(min(abs((x % 360) - 180), 120), 60) - 60) * 255 / 60,
    )

def putlines(text):
    nllimit = 8
    # text = [f'{x} ' for x in f'{text.capitalize()}'.split()]
    text = f"{text.capitalize()}".replace(" ", " ☎").split("☎")
    for nl in range(nllimit - 1, len(text), nllimit):
        text.insert(nl, "\n")
    return "".join(text)

def giveable(inventory: dict[tuple[str, int], int], items_given: dict[tuple[str, int], int]) -> bool:
    # if items_given:
    #     for item in items_given:
    #         if items_given[item] + inventory.get(item, 0) < 0:
    #             return False
    # return True
    return all([item_count + inventory.get(item, 0) >= 0 for item, item_count in items_given.items()])

def give_items(inventory: dict[tuple[str, int]: int], items_given: dict[tuple[str, int]: int]):
    for item in items_given:
        if inventory.get(item, 0) + items_given[item] > 0:
            inventory[item] = inventory.get(item, 0) + items_given[item]
        else:
            del inventory[item]

def pullup(fontaliased, font_small, screen, bgm, initial_tick) -> None:
    text = f": {bgm.replace("_", " ")}"
    x_position = (initial_tick**1.3)
    screen.blit(font_small.render(text, fontaliased, (0, 0, 0)), (80 - x_position, 50))
    screen.blit(font_small.render(text, fontaliased, (255, 255, 255)), (79 - x_position, 51))


def _apply_glow(screen, w, h):
    burl = 5
    glow_surf = transform.smoothscale(screen, (w // burl, h // burl))
    glow_surf = transform.smoothscale(glow_surf, (w, h))
    glow_surf.set_alpha(100)
    screen.blit(glow_surf, (0, 0))


def _add_glitch_effect(glitch_surface, intensity, enemies, w, h):
    shift_amount = intensity + (5 * len(enemies))
    if random.random() < 0.05 + (0.05 * len(enemies)):
        y_start = random.randint(0, h - 20)
        slice_height = random.randint(5, 20)
        offset = random.randint(-shift_amount, shift_amount)

        slice_area = Rect(0, y_start, w, slice_height)
        slice_copy = glitch_surface.subsurface(slice_area).copy()
        glitch_surface.blit(slice_copy, (offset, y_start))


def _apply_flicker(screen, tick):
    if tick % 144 == 0:
        flicker_surface = Surface(screen.get_size(), SRCALPHA)
        flicker_surface.fill((255, 255, 255, 2))
        screen.blit(flicker_surface, (0, 0))


def bar(screen, health, pos, colour=(0, 0, 0), radius=10):
    draw.rect(screen, colour, Rect(pos[0] - (health / 2), pos[1], health, radius << 1), border_radius=radius)


def lognt(x):
    return x * 2 / pow(10, (len("%i" % x) - 1))

def set_dialog(dialog, font, fontaliased):
    dialog_len = len(dialog)
    rendered_dialog = [
        scroll(x) for x in [putlines(x[1]) for x in dialog]
    ]
    for i in rendered_dialog:
        idex = rendered_dialog.index(i)
        for j in i:
            jdex = i.index(j)
            rendered_dialog[idex][jdex] = [
                font.render(k, fontaliased, (255, 255, 255))
                for k in rendered_dialog[idex][jdex].split("\n")
            ]
    return dialog_len, rendered_dialog

