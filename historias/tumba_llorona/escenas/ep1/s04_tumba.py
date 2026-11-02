"""Escena 4 — La tumba sin nombre: la única sin velas ni flores en todo el panteón."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera_center, vignette, darken, glow
from historias.tumba_llorona.dibujo import fondo_tumba, tumbas, llorona

DURATION = 4.2
SUBS = [
    (0.2, 4.0, "Al fondo, una tumba sin nombre. Sin velas. Sin flores.", None),
]
TUMBA = (W / 2, H * 0.60, 1.2)          # x, y de la base, escala
LATIDOS = [0.3, 1.55, 2.76, 3.93]       # el latido que acompaña toda la tensión (la mezcla usa estos mismos tiempos)
SUSTO = 2.45                             # una figura pálida asoma entre los árboles, dos parpadeos
APARICION = [(2.45, 2.62), (2.72, 2.98)]


def pulso(t, latidos, k=9.0):
    return max([math.exp(-(t - b) * k) for b in latidos if b <= t] or [0.0])


def draw(ctx, t):
    k = smooth(seg(t, 0, DURATION))
    ctx.save()
    p = pulso(t, LATIDOS)
    camera_center(ctx, lerp(1.0, 1.14, k) + 0.012 * p, W / 2, lerp(H * 0.5, H * 0.46, k))
    fondo_tumba.fondo(ctx, t)
    x, y, s = TUMBA
    if any(a <= t <= b for a, b in APARICION):
        llorona.de_pie(ctx, W * 0.86, H * 0.60 + 4, 0.52, t, brazos=0.0, alpha=0.6, aura=0.8)
    for dx in (-215, -120, 140, 225):
        tumbas.maleza(ctx, x + dx * s, y + 18 * s, s * 0.8, seed=int(dx), n=6)
    tumbas.tumba_sin_nombre(ctx, x, y, s, tono_frio=0.8)
    glow(ctx, x + 120, y - 380 * s, 380, (0.5, 0.65, 1.0), 0.16)
    ctx.restore()
    vignette(ctx, 0.72)
    darken(ctx, 0.16 * (1 - p))
    darken(ctx, 1 - smooth(seg(t, 0, 0.3)))
    darken(ctx, smooth(seg(t, DURATION - 0.25, DURATION)))
