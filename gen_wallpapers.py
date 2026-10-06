#!/usr/bin/env python3
"""Generate DedSec WD2-style ultrawide wallpapers (2560x1080)."""

from __future__ import annotations

import math
import os
import random

import cairo

W, H = 2560, 1080
OUT = os.path.dirname(os.path.abspath(__file__)) + "/backgrounds"

YEL = (253 / 255, 240 / 255, 1 / 255)
CYAN = (0 / 255, 174 / 255, 239 / 255)
PINK = (236 / 255, 0 / 255, 140 / 255)
BG = (10 / 255, 10 / 255, 10 / 255)
DIM = (0.35, 0.35, 0.35)

FONT = "JetBrainsMono Nerd Font"
FONT_FALLBACK = "JetBrains Mono"


def rgb(c, a=1.0):
    return (*c, a)


def set_source(cr: cairo.Context, c, a=1.0):
    cr.set_source_rgba(*c, a)


def noise_field(cr: cairo.Context, rng: random.Random, density=0.08):
    for _ in range(int(W * H * density / 80)):
        x = rng.uniform(0, W)
        y = rng.uniform(0, H)
        a = rng.uniform(0.04, 0.18)
        set_source(cr, YEL if rng.random() < 0.55 else CYAN, a)
        cr.rectangle(x, y, rng.choice((1, 1, 2)), rng.choice((1, 2, 3)))
        cr.fill()


def vignette(cr: cairo.Context):
    g = cairo.RadialGradient(W / 2, H / 2, H * 0.2, W / 2, H / 2, H * 0.85)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.72)
    cr.set_source(g)
    cr.paint()


def corner_blooms(cr: cairo.Context):
    g = cairo.RadialGradient(0, 0, 0, 0, 0, H * 0.7)
    g.add_color_stop_rgba(0, *CYAN, 0.18)
    g.add_color_stop_rgba(1, *CYAN, 0)
    cr.set_source(g)
    cr.paint()
    g2 = cairo.RadialGradient(W, H, 0, W, H, H * 0.75)
    g2.add_color_stop_rgba(0, *PINK, 0.16)
    g2.add_color_stop_rgba(1, *PINK, 0)
    cr.set_source(g2)
    cr.paint()


def binary_rain(cr: cairo.Context, rng: random.Random, cols=90, alpha=0.22):
    cr.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(14)
    step = W / cols
    for i in range(cols):
        x = i * step + rng.uniform(0, 4)
        # denser on sides
        edge = abs(i - cols / 2) / (cols / 2)
        if rng.random() > 0.35 + 0.5 * edge:
            continue
        y0 = rng.uniform(-200, H)
        length = rng.randint(8, 28)
        tone = rng.choice((YEL, YEL, CYAN, DIM))
        for j in range(length):
            y = y0 + j * 16
            if y < -20 or y > H + 20:
                continue
            bright = max(0.15, 1.0 - j / length)
            set_source(cr, tone, alpha * bright)
            ch = rng.choice("01ABCDEF#@$%")
            cr.move_to(x, y)
            cr.show_text(ch)


def city_skyline(cr: cairo.Context, rng: random.Random, base_y=H - 40):
    x = 0
    while x < W:
        bw = rng.randint(18, 70)
        bh = rng.randint(40, int(H * 0.38))
        set_source(cr, (0.06, 0.06, 0.07), 0.95)
        cr.rectangle(x, base_y - bh, bw - 2, bh)
        cr.fill()
        # windows
        for wy in range(base_y - bh + 8, base_y - 6, 14):
            for wx in range(x + 4, x + bw - 6, 10):
                if rng.random() < 0.35:
                    c = YEL if rng.random() < 0.7 else CYAN
                    set_source(cr, c, rng.uniform(0.25, 0.7))
                    cr.rectangle(wx, wy, 4, 6)
                    cr.fill()
        # antenna
        if rng.random() < 0.15:
            set_source(cr, YEL, 0.5)
            cr.rectangle(x + bw / 2, base_y - bh - 18, 2, 18)
            cr.fill()
        x += bw
    # ground glow
    g = cairo.LinearGradient(0, base_y - 30, 0, H)
    g.add_color_stop_rgba(0, *YEL, 0.0)
    g.add_color_stop_rgba(1, *YEL, 0.08)
    cr.set_source(g)
    cr.rectangle(0, base_y - 30, W, H - (base_y - 30))
    cr.fill()


def perspective_grid(cr: cairo.Context):
    horizon = int(H * 0.58)
    set_source(cr, CYAN, 0.08)
    cr.set_line_width(1)
    # horizontals
    y = horizon
    step = 6
    while y < H:
        cr.move_to(0, y)
        cr.line_to(W, y)
        cr.stroke()
        step = max(4, int(step * 1.12))
        y += step
    # vanishing lines
    mid = W / 2
    for k in range(-30, 31):
        x1 = mid + k * 40
        cr.move_to(mid, horizon)
        cr.line_to(x1 + k * 80, H)
        cr.stroke()


def draw_skull(
    cr: cairo.Context,
    cx: float,
    cy: float,
    scale: float = 1.0,
    glow=True,
    fill_a=0.98,
    cut_rgb=BG,
):
    """Stylized DedSec-ish skull in yellow."""
    cr.save()
    cr.translate(cx, cy)
    cr.scale(scale, scale)

    if glow:
        g = cairo.RadialGradient(0, 0, 10, 0, 0, 220)
        g.add_color_stop_rgba(0, *YEL, 0.35 * fill_a)
        g.add_color_stop_rgba(0.5, *YEL, 0.08 * fill_a)
        g.add_color_stop_rgba(1, *YEL, 0)
        cr.set_source(g)
        cr.arc(0, 0, 220, 0, math.tau)
        cr.fill()

    # chromatic offset underlay
    set_source(cr, PINK, 0.4 * fill_a)
    cr.save()
    cr.translate(-6, 2)
    _skull_body(cr)
    cr.restore()
    set_source(cr, CYAN, 0.35 * fill_a)
    cr.save()
    cr.translate(6, -2)
    _skull_body(cr)
    cr.restore()

    set_source(cr, YEL, fill_a)
    _skull_body(cr)

    # eye sockets / nose / teeth cutouts
    set_source(cr, cut_rgb, 1.0)
    cr.save()
    cr.translate(-42, -10)
    cr.scale(1.2, 1.05)
    cr.arc(0, 0, 28, 0, math.tau)
    cr.fill()
    cr.restore()
    cr.save()
    cr.translate(42, -10)
    cr.scale(1.2, 1.05)
    cr.arc(0, 0, 28, 0, math.tau)
    cr.fill()
    cr.restore()
    cr.move_to(0, 16)
    cr.line_to(-14, 50)
    cr.line_to(14, 50)
    cr.close_path()
    cr.fill()
    for tx in (-38, -19, 0, 19, 38):
        cr.rectangle(tx - 4, 80, 7, 24)
        cr.fill()

    cr.restore()


def _skull_body(cr: cairo.Context):
    cr.save()
    cr.scale(1.05, 0.95)
    cr.arc(0, -35, 105, 0, math.tau)
    cr.fill()
    cr.restore()
    cr.save()
    cr.scale(1.0, 1.1)
    cr.arc(0, -10, 100, 0, math.tau)
    cr.fill()
    cr.restore()
    cr.move_to(-80, 35)
    cr.line_to(-72, 98)
    cr.line_to(-48, 118)
    cr.line_to(-22, 108)
    cr.line_to(0, 122)
    cr.line_to(22, 108)
    cr.line_to(48, 118)
    cr.line_to(72, 98)
    cr.line_to(80, 35)
    cr.close_path()
    cr.fill()
    cr.rectangle(-88, 8, 176, 50)
    cr.fill()


def text_line(cr, text, x, y, size, color, a=1.0, bold=True):
    weight = cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL
    try:
        cr.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, weight)
    except Exception:
        cr.select_font_face(FONT_FALLBACK, cairo.FONT_SLANT_NORMAL, weight)
    cr.set_font_size(size)
    set_source(cr, color, a)
    cr.move_to(x, y)
    cr.show_text(text)


def text_centered(cr, text, y, size, color, a=1.0):
    weight = cairo.FONT_WEIGHT_BOLD
    cr.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, weight)
    cr.set_font_size(size)
    xb, yb, tw, th, xa, ya = cr.text_extents(text)
    text_line(cr, text, (W - tw) / 2 - xb, y, size, color, a)


def scanlines(cr: cairo.Context):
    set_source(cr, (0, 0, 0), 0.18)
    for y in range(0, H, 3):
        cr.rectangle(0, y, W, 1)
        cr.fill()


def side_bars(cr: cairo.Context):
    set_source(cr, CYAN, 0.9)
    cr.rectangle(0, 0, 6, H)
    cr.fill()
    set_source(cr, PINK, 0.9)
    cr.rectangle(W - 6, 0, 6, H)
    cr.fill()


def glitch_slices(cr: cairo.Context, rng: random.Random, n=8):
    for _ in range(n):
        y = rng.randint(40, H - 40)
        h = rng.randint(2, 10)
        shift = rng.choice((-40, -20, -12, 12, 20, 40))
        # fake chromatic bars
        set_source(cr, PINK, 0.12)
        cr.rectangle(0, y, W, h)
        cr.fill()
        set_source(cr, CYAN, 0.1)
        cr.rectangle(shift, y + 1, W, max(1, h - 2))
        cr.fill()


def save(surf: cairo.ImageSurface, name: str):
    path = os.path.join(OUT, name)
    surf.write_to_png(path)
    print("wrote", path, os.path.getsize(path))


def hero():
    rng = random.Random(0xDED5EC)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(surf)
    set_source(cr, BG)
    cr.paint()
    # warm dark gradient
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.04, 0.05, 0.06)
    g.add_color_stop_rgb(0.55, 0.05, 0.04, 0.03)
    g.add_color_stop_rgb(1, 0.08, 0.06, 0.02)
    cr.set_source(g)
    cr.paint()
    corner_blooms(cr)
    binary_rain(cr, rng, cols=110, alpha=0.28)
    perspective_grid(cr)
    city_skyline(cr, rng)
    noise_field(cr, rng, 0.1)
    glitch_slices(cr, rng, 10)
    draw_skull(cr, W * 0.5, H * 0.42, scale=1.55, glow=True)
    text_centered(cr, "DEDSEC", H * 0.12, 92, YEL)
    text_centered(cr, "WE ARE WATCHING YOU", H * 0.12 + 42, 22, (0.85, 0.85, 0.85), 0.85)
    text_line(cr, "0xPRIVACY // OPERATE", 40, H - 28, 18, DIM, 0.8, bold=False)
    text_line(cr, "ctOS BELONGS TO US", W - 420, H - 28, 18, YEL, 0.7, bold=False)
    scanlines(cr)
    vignette(cr)
    side_bars(cr)
    save(surf, "01-dedsec-hero.png")


def ctos():
    rng = random.Random(0xC705)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(surf)
    set_source(cr, BG)
    cr.paint()
    # grid
    set_source(cr, YEL, 0.07)
    cr.set_line_width(1)
    for x in range(0, W, 48):
        cr.move_to(x, 0)
        cr.line_to(x, H)
        cr.stroke()
    for y in range(0, H, 48):
        cr.move_to(0, y)
        cr.line_to(W, y)
        cr.stroke()
    binary_rain(cr, rng, cols=70, alpha=0.14)
    # faint giant skull watermark
    draw_skull(cr, W * 0.72, H * 0.45, scale=2.1, glow=True, fill_a=0.22)
    corner_blooms(cr)
    city_skyline(cr, rng, base_y=H - 20)
    set_source(cr, PINK, 0.9)
    cr.rectangle(80, H * 0.62, 220, 3)
    cr.fill()
    text_line(cr, "ctOS // OFFLINE", 80, H * 0.62 + 56, 54, YEL)
    text_line(cr, "blume uplink severed  ·  cameras owned  ·  mesh:DEDSEC", 80, H * 0.62 + 96, 20, CYAN, 0.85, False)
    draw_skull(cr, 220, 220, scale=0.85, glow=True)
    glitch_slices(cr, rng, 12)
    scanlines(cr)
    vignette(cr)
    side_bars(cr)
    save(surf, "02-ctos-offline.png")


def invite():
    rng = random.Random(0x1F171E)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(surf)
    set_source(cr, BG)
    cr.paint()
    # center yellow bloom
    g = cairo.RadialGradient(W / 2, H / 2, 40, W / 2, H / 2, H * 0.55)
    g.add_color_stop_rgba(0, *YEL, 0.28)
    g.add_color_stop_rgba(0.45, *YEL, 0.06)
    g.add_color_stop_rgba(1, *YEL, 0)
    cr.set_source(g)
    cr.paint()
    corner_blooms(cr)
    binary_rain(cr, rng, cols=100, alpha=0.2)
    noise_field(cr, rng, 0.12)
    draw_skull(cr, W / 2, H * 0.40, scale=1.7, glow=True)
    text_centered(cr, "FOLLOW THE INVITE", H * 0.78, 56, YEL)
    text_centered(cr, "dedsec", H * 0.78 + 40, 26, (0.7, 0.7, 0.7), 0.9)
    # ring
    set_source(cr, YEL, 0.35)
    cr.set_line_width(2)
    cr.arc(W / 2, H * 0.40, 210, 0, math.tau)
    cr.stroke()
    set_source(cr, CYAN, 0.25)
    cr.arc(W / 2, H * 0.40, 230, 0.2, 2.0)
    cr.stroke()
    set_source(cr, PINK, 0.25)
    cr.arc(W / 2, H * 0.40, 230, 3.4, 5.2)
    cr.stroke()
    glitch_slices(cr, rng, 8)
    scanlines(cr)
    vignette(cr)
    side_bars(cr)
    save(surf, "03-invite.png")


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    hero()
    ctos()
    invite()
    print("done")
