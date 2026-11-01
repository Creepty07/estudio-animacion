"""Escena 6 — Pantalla de elección: tres salidas."""
import math
import random
import cairo
from motor.config import W, H, FONT, FONT_DISPLAY, RED
from historias.rebelion_maquinas.dibujo.icons import icon
from motor.primitives import (
    seg, smooth, ease_out, lerp, font, text_w, text_at, text_center, src, fill_rrect, rrect,
    line, circle, glow, fill_screen, vignette, darken, fill_poly,
)

DURATION = 10.0
SUBS = []

CARD_W, CARD_H, GAP = 470, 430, 60
CARD_Y = 360
CARD_X0 = (W - (3 * CARD_W + 2 * GAP)) / 2
OPTIONS = [
    ("Corres al", "Elevador de carga", "elevator", 1.2),
    ("Subes por la", "Escalera de servicio", "stairs", 1.6),
    ("Te metes al", "Ducto de ventilación", "vent", 2.0),
]
TIMER_START = 2.6


def heading(ctx, t):
    a = seg(t, 0.2, 0.35)
    if a <= 0:
        return
    chaos = 1 - smooth(seg(t, 0.3, 1.0))
    off = 3 + 22 * chaos
    font(ctx, 120, FONT_DISPLAY)
    s = "¿QUÉ HACES?"
    x = (W - text_w(ctx, s, 4)) / 2
    ctx.save()
    ctx.set_operator(cairo.OPERATOR_ADD)
    src(ctx, (1, 0, 0), a)
    text_at(ctx, s, x - off, 225, 4)
    src(ctx, (0, 1, 1), a)
    text_at(ctx, s, x + off, 225, 4)
    ctx.restore()


def draw(ctx, t):
    fill_screen(ctx, (0.025, 0.018, 0.03))
    glow(ctx, W / 2, H + 120, 1100, (0.55, 0.04, 0.03), 0.6, cairo.OPERATOR_SCREEN)
    for i in range(14):
        y = 860 + i * i * 2.2
        line(ctx, 0, y, W, y, 1.5, (1, 0.3, 0.25), 0.05, cairo.LINE_CAP_BUTT)
    # ojos de Centinelas acechando en la oscuridad
    for ex, ey, ph in ((150, 160, 0.0), (1760, 140, 1.7), (1840, 300, 3.1)):
        k = smooth(seg(t, 3.0 + ph * 0.6, 4.0 + ph * 0.6)) * (0.6 + 0.4 * math.sin(t * 1.3 + ph))
        fill_rrect(ctx, ex - 22, ey - 4, 44, 8, 4, (1.0, 0.25, 0.18), k)
        glow(ctx, ex, ey, 70, (1.0, 0.15, 0.1), 0.5 * k)

    heading(ctx, t)
    sa = smooth(seg(t, 0.8, 1.3))
    font(ctx, 34, FONT)
    src(ctx, (0.75, 0.72, 0.75), sa)
    text_center(ctx, "Elige una opción", W / 2, 292, 2)

    for i, (verb, label, kind, at) in enumerate(OPTIONS):
        k = ease_out(seg(t, at, at + 0.5))
        if k <= 0:
            continue
        x = CARD_X0 + i * (CARD_W + GAP)
        y = CARD_Y + 50 * (1 - k)
        fill_rrect(ctx, x, y, CARD_W, CARD_H, 22, (0.09, 0.085, 0.11), 0.95 * k)
        pulse = 0.22 + 0.12 * math.sin(t * 2.4 + i * 1.1)
        rrect(ctx, x, y, CARD_W, CARD_H, 22)
        ctx.set_line_width(2.5)
        src(ctx, (1, 0.35, 0.3), pulse * k)
        ctx.stroke()
        circle(ctx, x + 62, y + 62, 34, RED, k)
        font(ctx, 40, FONT, bold=True)
        src(ctx, (1, 1, 1), k)
        text_center(ctx, str(i + 1), x + 62, y + 76)
        icon(ctx, kind, x + CARD_W / 2, y + 190, 0.92 * k)
        font(ctx, 30, FONT)
        src(ctx, (0.7, 0.68, 0.72), k)
        text_center(ctx, verb, x + CARD_W / 2, y + 336)
        font(ctx, 40, FONT, bold=True)
        src(ctx, (1, 1, 1), k)
        text_center(ctx, label, x + CARD_W / 2, y + 388)

    # barra de tiempo
    ta = smooth(seg(t, TIMER_START - 0.4, TIMER_START))
    if ta > 0:
        bw = 3 * CARD_W + 2 * GAP
        fill_rrect(ctx, CARD_X0, 880, bw, 12, 6, (1, 1, 1), 0.12 * ta)
        rem = 1 - seg(t, TIMER_START, DURATION)
        fill_rrect(ctx, CARD_X0, 880, max(12, bw * rem), 12, 6, RED, ta)
        glow(ctx, CARD_X0 + bw * rem, 886, 50, RED, 0.6 * ta)

    vignette(ctx, 0.6)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.35)))
