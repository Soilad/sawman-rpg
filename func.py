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
    b.blit(surface, (0, 0))
    transform.gaussian_blur(b, thicc, dest_surface=a)
    a.fill(color, special_flags=BLEND_RGBA_MIN)
    a.set_alpha(opacity)
    a.blit(surface, (0, 0), special_flags=BLEND_RGBA_ADD)
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


def clip(surface, x, y):
    handle_surface = surface.copy()
    clipRect = Rect(x, y, 100, 239)
    handle_surface.set_clip(clipRect)
    image = surface.subsurface(handle_surface.get_clip())
    return image.copy().convert_alpha()


def enemclip(surface, pos):
    handle_surface = surface.copy()
    w, h = handle_surface.get_size()
    clipRect = Rect(pos[0] * w // 3, pos[1] * h // 2, w // 3, h // 2)
    handle_surface.set_clip(clipRect)
    image = surface.subsurface(handle_surface.get_clip())
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


def adddict(a, b):
    combinable = True
    aa = a.copy()
    bb = b.copy()
    ab = {x: aa.get(x, 0) + bb.get(x, 0) for x in set(aa).union(bb)}
    for k in bb:
        if k not in aa:
            aa[k] = 0
        if ab[k] == 0:
            del aa[k]
        if ab[k] < 0:
            combinable = False
    return ab if combinable else a


def pullup(fontaliased, fontmin, screen, bgm, a):
    screen.blit(
        fontmin.render(f": {bgm}".replace("_", " "), fontaliased, (0, 0, 0)),
        (80 - (a**1.3), 50),
    )
    screen.blit(
        fontmin.render(f": {bgm}".replace("_", " "), fontaliased, (255, 255, 255)),
        (79 - (a**1.3), 51),
    )


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
    draw.rect(screen, colour, Rect(pos[0] - (health / 2), pos[1], health, radius << 1))
    draw.circle(screen, colour, (pos[0] - (health / 2), pos[1] + radius), radius)
    draw.circle(screen, colour, (pos[0] + (health / 2), pos[1] + radius), radius)


def lognt(x):
    return x * 2 / pow(10, (len("%i" % x) - 1))
