"""Escena 3 — Rafa, 19 años, su primera noche en el hospital: fachada de noche y acercamiento a la única ventana encendida."""
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera_center, vignette, darken
from motor.kit import fog
from historias.planchada.dibujo import fachada

DURATION = 5.5
SUBS = [
    (0.2, 2.6, "Rafa, 19 años.", None),
    (2.7, 5.2, "Su primera noche en el hospital.", None),
]


def draw(ctx, t):
    k = smooth(seg(t, 0.0, DURATION))
    vx, vy, vw, vh = fachada.VENTANA_LUZ
    ctx.save()
    camera_center(ctx, lerp(1.0, 3.1, k ** 1.4), lerp(W / 2, vx + vw / 2, k), lerp(H * 0.5, vy + vh / 2 + 80, k))
    fachada.fachada(ctx, t)
    ctx.restore()
    fog(ctx, t, (0.6, 0.75, 0.85), 0.10, H * 0.55, H, seed=4)
    vignette(ctx, 0.7)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.5)))
    darken(ctx, smooth(seg(t, DURATION - 0.25, DURATION)))
