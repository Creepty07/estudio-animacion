"""Apertura del video 2: los tres finales del Capítulo 1."""
import math
from motor.config import W, H, FONT, RED
from motor.primitives import seg, smooth, ease_out, font, src, text_center, fill_rrect, rrect, circle, vignette, darken
from historias.rebelion_maquinas.dibujo.cards import backdrop, glitch_text
from historias.rebelion_maquinas.dibujo.icons import icon

DURATION = 4.5
SUBS = []
MINI = [("1", "Elevador", "elevator"), ("2", "Escalera", "stairs"), ("3", "Ducto", "vent")]


def draw(ctx, t):
    backdrop(ctx, t)
    ka = smooth(seg(t, 0.1, 0.5))
    font(ctx, 36, FONT, bold=True)
    src(ctx, (0.75, 0.72, 0.75), ka)
    text_center(ctx, "CAPÍTULO 1  ·  EL APAGÓN", W / 2, 230, 8)
    glitch_text(ctx, "LOS 3 FINALES", W / 2, 400, 170, seg(t, 0.35, 0.45), 1 - smooth(seg(t, 0.4, 1.3)))
    sa = smooth(seg(t, 1.0, 1.4))
    font(ctx, 44, FONT)
    src(ctx, (1, 1, 1), 0.85 * sa)
    text_center(ctx, "¿Sobreviviste a tu elección?", W / 2, 490)
    for i, (num, label, kind) in enumerate(MINI):
        k = ease_out(seg(t, 1.5 + i * 0.25, 2.0 + i * 0.25))
        if k <= 0:
            continue
        cw, ch = 360, 330
        x = W / 2 + (i - 1) * 420 - cw / 2
        y = 570 + 40 * (1 - k)
        fill_rrect(ctx, x, y, cw, ch, 22, (0.09, 0.085, 0.11), 0.95 * k)
        rrect(ctx, x, y, cw, ch, 22)
        ctx.set_line_width(2.5)
        src(ctx, (1, 0.35, 0.3), (0.25 + 0.12 * math.sin(t * 3 + i)) * k)
        ctx.stroke()
        circle(ctx, x + 50, y + 50, 28, RED, k)
        font(ctx, 34, FONT, bold=True)
        src(ctx, (1, 1, 1), k)
        text_center(ctx, num, x + 50, y + 62)
        ctx.save()
        ctx.translate(x + cw / 2, y + 150)
        ctx.scale(0.8, 0.8)
        icon(ctx, kind, 0, 0, 0.92 * k)
        ctx.restore()
        font(ctx, 38, FONT, bold=True)
        src(ctx, (1, 1, 1), k)
        text_center(ctx, label, x + cw / 2, y + 290)
    vignette(ctx, 0.6)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.2)))
    darken(ctx, smooth(seg(t, DURATION - 0.3, DURATION)))
