"""Escena 2 — Ciudad Nodo de noche y acercamiento a Torre Helix."""
from motor.config import W, H, FONT_MONO, RED
from motor.primitives import seg, smooth, lerp, camera, font, text_at, text_w, src, darken, vignette, fill_rrect
from historias.rebelion_maquinas.dibujo.environments import draw_city

DURATION = 7.0
SUBS = [
    (0.6, 2.9, "Ciudad Nodo, año 2041.", None),
    (3.1, 6.5, "Los robots hacen todo el trabajo. Y una sola inteligencia los controla a todos: Ágora.", None),
]

LINE1 = "TORRE HELIX · SÓTANO -3"
LINE2 = "11:47 P. M."
TYPE_START, CPS = 1.4, 16.0


def typed(t):
    n = max(0, int((t - TYPE_START) * CPS))
    return LINE1[:n], LINE2[:max(0, n - len(LINE1) - 4)]


def draw(ctx, t):
    z = lerp(1.0, 1.55, smooth(seg(t, 0.3, 7.0)))
    ctx.save()
    camera(ctx, z, 960, 930)
    draw_city(ctx, t)
    ctx.restore()
    vignette(ctx, 0.6)

    # rótulo de ubicación que se escribe solo
    l1, l2 = typed(t)
    if l1:
        font(ctx, 38, FONT_MONO, bold=True)
        fill_rrect(ctx, 96, 92, 620, 128, 10, (0, 0, 0), 0.5)
        src(ctx, (0.85, 0.92, 1.0))
        text_at(ctx, l1, 124, 146)
        src(ctx, RED)
        text_at(ctx, l2, 124, 196)
        if (t * 2.2) % 1 < 0.55:
            cur_line, txt, y = (2, l2, 196) if l2 or len(l1) == len(LINE1) else (1, l1, 146)
            x = 124 + text_w(ctx, txt)
            ctx.rectangle(x + 4, y - 30, 18, 34)
            src(ctx, (0.85, 0.92, 1.0), 0.9)
            ctx.fill()

    darken(ctx, 1 - smooth(seg(t, 0.0, 0.7)))
    darken(ctx, smooth(seg(t, 6.3, 7.0)))
