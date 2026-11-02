"""Escena 7 — Don Celso despierta de rodillas a la orilla del río; del agua salen manos-sombra."""
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera, darken, vignette
from historias.rio_perros.dibujo import rio, celso as C, manos

DURATION = 6.6
SUBS = [
    (0.4, 3.0, "Despertó a la orilla de un río negro.", None),
    (3.3, 6.0, "Del agua salían manos.", None),
]
DESPIERTA = 0.6
# (x, y, instante en que sube): una mano por cada golpe de agua
MANOS = ((250, 1010, 3.0), (800, 950, 3.4), (520, 870, 3.8), (930, 1120, 4.2), (110, 1130, 4.6))


def draw(ctx, t):
    ctx.save()
    camera(ctx, lerp(1.0, 1.08, smooth(seg(t, 0, DURATION))), W / 2, H * 0.62)
    rio.fondo(ctx, t)
    for i, (x, y, t0) in enumerate(MANOS):
        k = (y - rio.LEJOS_Y) / (rio.ORILLA_Y - rio.LEJOS_Y)         # perspectiva: más cerca = más grande
        s = 0.55 + 0.75 * k
        sube = smooth(seg(t, t0, t0 + 0.9)) * (1 - smooth(seg(t, t0 + 1.9, t0 + 2.7)))
        manos.mano(ctx, x, y, s, (240 + 90 * k) * sube, abre=0.4 + 0.5 * sube, t=t, seed=i * 1.7, inclina=0.08 * (i - 2))
    rio.orilla(ctx, t)
    C.celso_arrodillado(ctx, W * 0.5, 1262, 1.45, t, cabeza_baja=lerp(0.95, 0.35, smooth(seg(t, DESPIERTA, DESPIERTA + 1.4))))
    ctx.restore()
    rio.niebla_baja(ctx, t)
    vignette(ctx, 0.62)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.5)))
    darken(ctx, smooth(seg(t, DURATION - 0.4, DURATION)))
