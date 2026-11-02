"""Escena 7 — El cuarto se heló. La manga blanca, perfecta; escarcha que crece en el vidrio; el vaho de Rafa. Olía a almidón."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera_center, vignette, darken
from historias.planchada.dibujo import cuarto, personajes, objetos
from historias.planchada.dibujo.paleta import fluo_brillo

DURATION = 5.5
SUBS = [
    (0.3, 2.3, "El cuarto se heló.", None),
    (2.8, 5.2, "Olía a almidón.", None),
]
ESCARCHA = (0.0, 5.0)    # la escarcha crece durante toda la escena


def draw(ctx, t):
    k = smooth(seg(t, 1.8, 3.6))
    ctx.save()
    cuarto.cam(ctx, lerp(2.5, 1.8, k), lerp(450, 270, k), lerp(830, 560, k))
    cuarto.cuarto(ctx, t, fluo=0.5 + 0.1 * fluo_brillo(t, 7, "inestable"), hora=(3, 0), segundero=0, ventana=1.0, turno="dormida",
                  escarcha=smooth(seg(t, *ESCARCHA)) * 0.9, seed=3)
    personajes.rafa_cama(ctx, *cuarto.CABEZA, 1.0, t, ojos="abiertos", mira=(1.0, -0.2), boca="abierta", rubor=0.3, sudor=0.6)
    objetos.vaho(ctx, cuarto.CABEZA[0] + 10, cuarto.CABEZA[1] + 30, t, 1.4)
    personajes.eulalia(ctx, 540, 1230, 1.0, t, pose="pie", cara=0.0, halo=1.0)
    ctx.restore()
    vignette(ctx, 0.72)
    darken(ctx, 1 - smooth(seg(t, 0, 0.2)))
    darken(ctx, smooth(seg(t, DURATION - 0.25, DURATION)))
