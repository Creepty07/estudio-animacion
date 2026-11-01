"""Cierre del video 2: llamado a comentar y seguir la serie."""
import math
from motor.config import W, H, FONT, RED, OUTCOME
from motor.primitives import (
    seg, smooth, ease_out, font, src, text_at, text_center, text_w, fill_rrect, circle, vignette, darken, glow,
)
from historias.rebelion_maquinas.dibujo.cards import backdrop, glitch_text

DURATION = 5.0
SUBS = []
ROWS = [
    ("1", "Elevador de carga", "Moriste", "malo"),
    ("2", "Escalera de servicio", "Sobreviviste… sin mochila", "regular"),
    ("3", "Ducto de ventilación", "Sobreviviste · camino oficial", "bueno"),
]


def draw(ctx, t):
    backdrop(ctx, t)
    glitch_text(ctx, "¿CUÁL ELEGISTE TÚ?", W / 2, 230, 120, seg(t, 0.15, 0.25), 1 - smooth(seg(t, 0.2, 0.9)))
    for i, (num, label, result, kind) in enumerate(ROWS):
        k = ease_out(seg(t, 0.7 + i * 0.25, 1.2 + i * 0.25))
        if k <= 0:
            continue
        rgb = OUTCOME[kind]
        y = 330 + i * 140 + 30 * (1 - k)
        x0, w = 360, 1200
        fill_rrect(ctx, x0, y, w, 112, 20, (0.09, 0.085, 0.11), 0.95 * k)
        fill_rrect(ctx, x0, y, 12, 112, 6, rgb, k)
        circle(ctx, x0 + 76, y + 56, 32, RED, k)
        font(ctx, 38, FONT, bold=True)
        src(ctx, (1, 1, 1), k)
        text_center(ctx, num, x0 + 76, y + 70)
        font(ctx, 42, FONT, bold=True)
        text_at(ctx, label, x0 + 140, y + 70)
        font(ctx, 36, FONT, bold=True)
        src(ctx, rgb, k)
        text_at(ctx, result, x0 + w - 40 - text_w(ctx, result), y + 70)
    ca = smooth(seg(t, 1.9, 2.4))
    pulse = 0.85 + 0.15 * math.sin(t * 5)
    font(ctx, 58, "Inter Display Black")
    src(ctx, (1, 1, 1), ca * pulse)
    text_center(ctx, "COMENTA 1, 2 O 3", W / 2, 850, 3)
    font(ctx, 36, FONT)
    src(ctx, (0.75, 0.73, 0.78), ca)
    text_center(ctx, "Sigue la serie: el Capítulo 2 viene pronto", W / 2, 920)
    vignette(ctx, 0.6)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.2)))
    darken(ctx, smooth(seg(t, DURATION - 0.4, DURATION)))
