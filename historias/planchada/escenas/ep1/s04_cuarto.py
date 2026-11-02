"""Escena 4 — La fiebre no bajaba. Rafa en la cama, suero, reloj 2:59; por la puerta, la enfermera de turno dormida."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera_center, vignette, darken
from historias.planchada.dibujo import cuarto, personajes
from historias.planchada.dibujo.paleta import fluo_brillo

DURATION = 6.5
SUBS = [
    (0.2, 2.8, "La fiebre no bajaba.", None),
    (3.0, 6.2, "En el pasillo, la enfermera de turno dormía.", None),
]
RELOJ_TIC = 1.0          # el reloj marca un tic por segundo (la mezcla usa estos mismos tiempos)


def draw(ctx, t):
    k = smooth(seg(t, 0, 2.8))
    k2 = smooth(seg(t, 2.8, 5.2))
    ctx.save()
    cuarto.cam(ctx, lerp(1.30, 1.38, k) - 0.1 * k2, lerp(lerp(300, 380, k), 700, k2), lerp(900, 830, k2))
    b = 0.55 + 0.45 * fluo_brillo(t, 3, "parpadea")
    cuarto.cuarto(ctx, t, fluo=b, hora=(2, 59), segundero=(int(t) * 1 + 40) % 60, turno="dormida", pasillo=1.0, seed=3)
    personajes.rafa_cama(ctx, *cuarto.CABEZA, 1.0, t, ojos="fiebre", boca="cerrada", rubor=0.8, sudor=1.0)
    ctx.restore()
    vignette(ctx, 0.7)
    darken(ctx, 1 - smooth(seg(t, 0, 0.4)))
    darken(ctx, smooth(seg(t, DURATION - 0.25, DURATION)))
