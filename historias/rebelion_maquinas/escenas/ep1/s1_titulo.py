"""Escena 1 — Título con efecto de falla (glitch)."""
import random
import cairo
from motor.config import W, H, FONT, FONT_DISPLAY, RED
from motor.primitives import (
    seg, ease_out, smooth, font, text_w, text_at, fill_screen, darken, vignette, src, line, glow,
)

DURATION = 6.0
SUBS = []

L1, L2 = "LA REBELIÓN", "DE LAS MÁQUINAS"


def _title(ctx, dx=0.0, rgb=(1, 1, 1), a=1.0):
    font(ctx, 150, FONT_DISPLAY)
    src(ctx, rgb, a)
    text_at(ctx, L1, (W - text_w(ctx, L1, 6)) / 2 + dx, 470, 6)
    text_at(ctx, L2, (W - text_w(ctx, L2, 6)) / 2 + dx, 630, 6)


def draw(ctx, t):
    fill_screen(ctx, (0.012, 0.01, 0.016))
    r = random.Random(int(t * 30))

    # líneas de interferencia de fondo
    for _ in range(6):
        y = r.uniform(0, H)
        line(ctx, 0, y, W, y, r.uniform(1, 3), RED, r.uniform(0.03, 0.09), cairo.LINE_CAP_BUTT)
    glow(ctx, W / 2, 560, 900, (0.5, 0.03, 0.03), 0.35, cairo.OPERATOR_SCREEN)

    appear = seg(t, 0.5, 0.62)
    chaos = 1 - smooth(seg(t, 0.6, 1.8))
    if appear > 0:
        # aberración cromática: rojo y cian desplazados, suman blanco
        off = 4 + 26 * chaos
        ctx.save()
        ctx.set_operator(cairo.OPERATOR_ADD)
        _title(ctx, -off, (1, 0, 0), appear)
        _title(ctx, off, (0, 1, 1), appear)
        ctx.restore()
        # cortes horizontales desplazados
        if chaos > 0.05:
            for _ in range(int(3 + 7 * chaos)):
                y = r.uniform(330, 660)
                h = r.uniform(6, 40)
                ctx.save()
                ctx.rectangle(0, y, W, h)
                ctx.clip()
                fill_screen(ctx, (0.012, 0.01, 0.016))
                _title(ctx, r.uniform(-90, 90) * chaos, (1, 1, 1), appear)
                ctx.restore()
        # parpadeo inicial
        if t < 1.0 and r.random() < 0.25:
            darken(ctx, 0.6)

    # línea roja y subtítulo
    k = ease_out(seg(t, 2.1, 2.8))
    if k > 0:
        w = 760 * k
        line(ctx, W / 2 - w / 2, 690, W / 2 + w / 2, 690, 4, RED, 1.0, cairo.LINE_CAP_BUTT)
        glow(ctx, W / 2, 690, 260 * k, RED, 0.35)
    a = smooth(seg(t, 2.6, 3.4))
    if a > 0:
        font(ctx, 42, FONT, bold=True)
        p1, p2 = "CAPÍTULO 1  ·  ", "EL APAGÓN"
        total = text_w(ctx, p1 + p2, 10)
        x = (W - total) / 2
        src(ctx, (0.75, 0.75, 0.78), a)
        text_at(ctx, p1, x, 770, 10)
        x += text_w(ctx, p1, 10) + 10
        src(ctx, RED, a)
        text_at(ctx, p2, x, 770, 10)

    vignette(ctx, 0.7)
    darken(ctx, smooth(seg(t, 5.2, 6.0)))
