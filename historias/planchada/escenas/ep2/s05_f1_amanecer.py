"""Ep2 escena 5 — Al amanecer, la pastilla seguía ahí. Luz gris de madrugada; la cama en sombra; corte a negro antes de ver a Rafa."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera_center, vignette, darken, fill_screen
from historias.planchada.dibujo import cuarto, personajes, objetos

DURATION = 7.0
SUBS = [
    (0.3, 2.6, "Al amanecer, la pastilla seguía ahí.", None),
    (3.0, 6.7, "Ella era la única que venía a este cuarto.", None),
]
NEGRO = 6.7              # corte a negro (el tono largo y muy bajo del monitor se corta aquí)


def draw(ctx, t):
    if t >= NEGRO:
        fill_screen(ctx, (0, 0, 0))
        return
    k = smooth(seg(t, 0, NEGRO))
    ctx.save()
    cuarto.cam(ctx, lerp(2.3, 1.9, k), lerp(720, 590, k), 960)
    cuarto.cuarto(ctx, t, fluo=0.0, hora=(5, 40), segundero=None, ventana=0.1, amanecer=0.22, turno="dormida", pastilla_buro=True, seed=3,
                  luz_cuarto=0.0, gota=False)
    personajes.rafa_cama(ctx, *cuarto.CABEZA, 1.0, t, ojos="cerrados", boca="cerrada", rubor=0.0, sudor=0.0, respira=0.0)
    ctx.restore()
    fill_screen(ctx, (0.02, 0.03, 0.05), 0.35)                                            # cama en sombra
    vignette(ctx, 0.75)
    darken(ctx, 1 - smooth(seg(t, 0, 0.3)))
