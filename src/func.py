import random
from collections.abc import Callable
from textwrap import wrap
from typing import TYPE_CHECKING, Any

from numba import jit
from pygame import (
    BLEND_RGBA_MIN,
    SRCALPHA,
    Rect,
    Surface,
    Vector2,
    draw,
    font,
    transform,
)

from consts import FONT_ALIASED, font_medium
from structs import World

if TYPE_CHECKING:
    from components.overlay import SurfaceOverlay


@jit
def scroll(string: str):
    _len = len(string) + 1
    for i in range(1, _len):
        yield string[:i]


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

def clip(surface: Surface , sprite_width: int, sprite_height: int) -> dict[tuple[int,int], Surface]:
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

@jit
def coler(x):
    # x = x * 3 / 50
    return (
        (max(min(abs(((x - 240) % 360) - 180), 120), 60) - 60) * 255 / 60,
        (max(min(abs(((x - 120) % 360) - 180), 120), 60) - 60) * 255 / 60,
        (max(min(abs((x % 360) - 180), 120), 60) - 60) * 255 / 60,
    )

def giveable(inventory: dict[tuple[str, int], int], items_given: dict[tuple[str, int], int]) -> bool:
    # if items_given:
    #     for item in items_given:
    #         if items_given[item] + inventory.get(item, 0) < 0:
    #             return False
    # return True
    return all([item_count + inventory.get(item, 0) >= 0 for item, item_count in items_given.items()])

def give_items(inventory: dict[tuple[str, int], int], items_given: dict[tuple[str, int], int]):
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

@jit
def lognt(x):
    return x * 2 / pow(10, (len(f"{int(x)}" ) - 1))

def set_dialog(
    text: str,
    font: font.Font,
    position: Vector2 = Vector2(0, 0),
    width: int = 40,
) -> list[list[SurfaceOverlay]]:
    """
    frames[time][line]: one frame per typed character, each holding one
    overlay per line revealed so far (the last one partially typed).
    The full text is wrapped up front so words don't jump lines while typing.
    """
    # imported here to avoid a cycle: components -> interfaces -> func
    from components.overlay import SurfaceOverlay

    lines       = wrap(text, width=width)
    line_height = font.get_linesize()

    def line_overlay(index: int, part: str) -> SurfaceOverlay:
        return SurfaceOverlay(
            surface  = font.render(part, FONT_ALIASED, (255, 255, 255,)),
            position = Vector2(position) + Vector2(0, index * line_height),
            z        = 6,
        )

    frames:   list[list[SurfaceOverlay]] = []
    finished: list[SurfaceOverlay]       = []
    for index, line in enumerate(lines):
        for shown in range(1, len(line) + 1):
            frames.append(finished + [line_overlay(index, line[:shown])])
        # the fully typed line is the last frame's overlay; reuse it from now on
        finished = frames[-1]
    return frames

def lerp(initial, final, rate=4):
    return (
        (
            (rate - 1)*initial
            + final
        ) / rate
    )


def UIanimation(
    a_object: Any,
    a_attribute: list[str],
    a_final,
    rate: int = 4,
) -> Callable[[World], bool]:
    # walk ["a", "b", "c"] down to a_object.a.b, which owns "c"
    *path, attribute = a_attribute
    _object = a_object
    for name in path:
        _object = getattr(_object, name)

    # keep our own float copy instead of re-reading the attribute each frame:
    # Rect fields truncate to int, which throws away sub-pixel progress and
    # stalls the animation a few px short of a_final
    position = float(getattr(_object, attribute))

    def animation(world: World) -> bool:
        nonlocal position
        position = lerp(position, a_final, rate)
        if abs(a_final - position) < 0.5:
            position = a_final
        setattr(_object, attribute, position)
        a_object.update()
        return position == a_final

    animation.target = (_object, attribute)  # pyright: ignore[reportFunctionMemberAccess]
    return animation



if __name__ == "__main__":
    from pprint import pp
    pp([x for x in set_dialog("loren ipsum dolor set ament", font_medium)])
