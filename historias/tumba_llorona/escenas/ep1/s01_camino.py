"""Escena 1 — El camino de cempasúchil hacia la ofrenda. Lo cálido y vivo del Día de Muertos."""
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera, vignette, darken
from motor.kit import fog
from historias.tumba_llorona.dibujo import camino

DURATION = 4.2
SUBS = [
    (0.3, 3.9, "Día de Muertos: los muertos vuelven a casa.", None),
]


def draw(ctx, t):
    ctx.save()
    camera(ctx, lerp(1.0, 1.17, smooth(seg(t, 0, DURATION))), W / 2, H * 0.47)
    camino.dibujar(ctx, t)
    ctx.restore()
    fog(ctx, t, (0.55, 0.62, 0.8), 0.10, H * 0.5, H * 0.95, seed=3)
    vignette(ctx, 0.62)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.5)))
    darken(ctx, smooth(seg(t, DURATION - 0.25, DURATION)))
