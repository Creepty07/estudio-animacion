"""Tarjetas de pantalla completa: opción elegida, resultado del final y llamados a la acción."""
import math
import random
import cairo
from motor.config import W, H, FONT, FONT_DISPLAY, RED, OUTCOME
from motor.primitives import (
    seg, smooth, ease_out, lerp, font, text_w, text_at, text_center, src, fill_rrect, rrect,
    line, glow, fill_screen, vignette, darken,
)
from historias.rebelion_maquinas.dibujo.icons import icon, cross_out

PILL_TEXT = {"malo": "FINAL MALO", "regular": "FINAL REGULAR", "bueno": "FINAL BUENO"}


def backdrop(ctx, t, rgb=(0.55, 0.04, 0.03), strength=0.55):
    fill_screen(ctx, (0.025, 0.018, 0.03))
    glow(ctx, W / 2, H + 160, 1150, rgb, strength, cairo.OPERATOR_SCREEN)
    r = random.Random(int(t * 12))
    for _ in range(4):
        y = r.uniform(0, H)
        line(ctx, 0, y, W, y, 1.5, rgb, 0.06, cairo.LINE_CAP_BUTT)


def glitch_text(ctx, s, cx, y, size, a, chaos, c1=(1, 0, 0), c2=(0, 1, 1), spacing=4):
    """Texto con aberración cromática: c1 + c2 suman blanco donde coinciden."""
    if a <= 0:
        return
    font(ctx, size, FONT_DISPLAY)
    x = cx - text_w(ctx, s, spacing) / 2
    off = 3 + 24 * chaos
    ctx.save()
    ctx.set_operator(cairo.OPERATOR_ADD)
    src(ctx, c1, a)
    text_at(ctx, s, x - off, y, spacing)
    src(ctx, c2, a)
    text_at(ctx, s, x + off, y, spacing)
    ctx.restore()


def pill(ctx, text, cx, y, rgb, a):
    font(ctx, 30, FONT, bold=True)
    w = text_w(ctx, text, 5) + 56
    rrect(ctx, cx - w / 2, y - 40, w, 58, 29)
    src(ctx, rgb, 0.16 * a)
    ctx.fill_preserve()
    ctx.set_line_width(3)
    src(ctx, rgb, a)
    ctx.stroke()
    src(ctx, rgb, a)
    text_center(ctx, text, cx, y, 5)


def option_card(ctx, t, dur, num, verb, label, kind):
    """Presenta qué opción vamos a ver (≈2 s)."""
    backdrop(ctx, t)
    k = ease_out(seg(t, 0.05, 0.5))
    font(ctx, 34, FONT, bold=True)
    src(ctx, (0.75, 0.72, 0.75), k)
    text_center(ctx, "SI ELEGISTE…", W / 2, 200, 8)
    cw, ch = 620, 560
    x, y = (W - cw) / 2, 250 + 40 * (1 - k)
    fill_rrect(ctx, x, y, cw, ch, 28, (0.09, 0.085, 0.11), 0.96 * k)
    rrect(ctx, x, y, cw, ch, 28)
    ctx.set_line_width(3)
    src(ctx, (1, 0.35, 0.3), (0.3 + 0.15 * math.sin(t * 5)) * k)
    ctx.stroke()
    from motor.primitives import circle
    circle(ctx, x + 78, y + 78, 44, RED, k)
    font(ctx, 54, FONT, bold=True)
    src(ctx, (1, 1, 1), k)
    text_center(ctx, str(num), x + 78, y + 97)
    ctx.save()
    ctx.translate(W / 2, y + 250)
    ctx.scale(1.35, 1.35)
    icon(ctx, kind, 0, 0, 0.95 * k)
    ctx.restore()
    font(ctx, 38, FONT)
    src(ctx, (0.7, 0.68, 0.72), k)
    text_center(ctx, verb, W / 2, y + 450)
    font(ctx, 54, FONT, bold=True)
    src(ctx, (1, 1, 1), k)
    text_center(ctx, label, W / 2, y + 516)
    vignette(ctx, 0.6)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.2)))
    darken(ctx, smooth(seg(t, dur - 0.3, dur)))


def result_card(ctx, t, dur, outcome, big, line_text, losses=(), footer="", sub_line=""):
    rgb = OUTCOME[outcome]
    backdrop(ctx, t, tuple(c * 0.55 for c in rgb), 0.6)
    pa = smooth(seg(t, 0.15, 0.5))
    pill(ctx, PILL_TEXT[outcome], W / 2, 215, rgb, pa)

    appear = seg(t, 0.35, 0.45)
    chaos = 1 - smooth(seg(t, 0.4, 1.2))
    if outcome == "malo":
        glitch_text(ctx, big, W / 2, 470, 230, appear, chaos)
    else:
        glitch_text(ctx, big, W / 2, 470, 190, appear, chaos * 0.6,
                    c1=(rgb[0], rgb[1] * 0.5, 0), c2=(1 - rgb[0] * 0.5, 1 - rgb[1] * 0.5 + rgb[1] * 0.5, 1))
        # el color del final asoma alrededor
        font(ctx, 190, FONT_DISPLAY)
    la = smooth(seg(t, 1.0, 1.5))
    font(ctx, 46, FONT, bold=True)
    src(ctx, (1, 1, 1), 0.92 * la)
    text_center(ctx, line_text, W / 2, 590)
    if sub_line:
        font(ctx, 36, FONT)
        src(ctx, (0.75, 0.73, 0.78), la)
        text_center(ctx, sub_line, W / 2, 645)

    if losses:
        n = len(losses)
        for i, (kind, label) in enumerate(losses):
            k = ease_out(seg(t, 1.5 + i * 0.25, 2.0 + i * 0.25))
            cx = W / 2 + (i - (n - 1) / 2) * 300
            ctx.save()
            ctx.translate(cx, 800 + 20 * (1 - k))
            ctx.scale(0.75, 0.75)
            icon(ctx, kind, 0, 0, 0.9 * k, accent=rgb)
            ctx.restore()
            xk = smooth(seg(t, 2.1 + i * 0.25, 2.35 + i * 0.25))
            if xk > 0:
                line(ctx, cx - 80, 800 - 80, cx - 80 + 160 * xk, 800 - 80 + 160 * xk, 10, rgb, 0.95)
            font(ctx, 30, FONT, bold=True)
            src(ctx, (0.85, 0.83, 0.87), k)
            text_center(ctx, label, cx, 930)
    if footer:
        fa = smooth(seg(t, 1.8, 2.3))
        font(ctx, 32, FONT, bold=True)
        src(ctx, rgb, fa)
        text_center(ctx, footer, W / 2, 1000 if losses else 820, 2)

    vignette(ctx, 0.6)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.15)))
    darken(ctx, smooth(seg(t, dur - 0.35, dur)))
