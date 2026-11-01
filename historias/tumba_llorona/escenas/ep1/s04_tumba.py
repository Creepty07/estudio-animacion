"""Escena 4 — La tumba sin nombre: la única sin velas ni flores en todo el panteón."""
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera_center, vignette, darken, glow
from historias.tumba_llorona.dibujo import fondo_tumba, tumbas

DURATION = 3.5
SUBS = [
    (0.2, 3.3, "Al fondo, una tumba sin nombre. Sin velas. Sin flores.", None),
]
TUMBA = (W / 2, H * 0.60, 1.2)          # x, y de la base, escala


def draw(ctx, t):
    k = smooth(seg(t, 0, DURATION))
    ctx.save()
    camera_center(ctx, lerp(1.0, 1.14, k), W / 2, lerp(H * 0.5, H * 0.46, k))
    fondo_tumba.fondo(ctx, t)
    x, y, s = TUMBA
    for dx in (-215, -120, 140, 225):
        tumbas.maleza(ctx, x + dx * s, y + 18 * s, s * 0.8, seed=int(dx), n=6)
    tumbas.tumba_sin_nombre(ctx, x, y, s, tono_frio=0.8)
    glow(ctx, x + 120, y - 380 * s, 380, (0.5, 0.65, 1.0), 0.16)
    ctx.restore()
    vignette(ctx, 0.72)
    darken(ctx, 1 - smooth(seg(t, 0, 0.3)))
    darken(ctx, smooth(seg(t, DURATION - 0.25, DURATION)))
