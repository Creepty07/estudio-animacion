"""Escena 8 — "Tranquilo. Ya estoy aquí." Se inclina sobre Rafa; la cara sigue en sombra y se ve una sonrisa amable; abre la mano: una pastilla."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera_center, vignette, darken
from historias.planchada.dibujo import cuarto, personajes, objetos
from historias.planchada.dibujo.paleta import fluo_brillo

DURATION = 8.0
SUBS = [
    (0.3, 3.4, "«Tranquilo. Ya estoy aquí.»", "Enfermera"),
    (3.9, 7.7, "«Esto te va a bajar la fiebre.»", "Enfermera"),
]
LINEAS = [0.3, 3.9]       # inicio de cada línea (la mezcla pone los murmullos debajo)
PASTILLA = 3.9            # abre la mano


def draw(ctx, t):
    k = smooth(seg(t, 0, 2.0))
    ctx.save()
    cuarto.cam(ctx, lerp(1.25, 1.5, smooth(seg(t, 0, DURATION))), lerp(420, 370, k), lerp(820, 860, k))
    cuarto.cuarto(ctx, t, fluo=0.55, hora=(3, 0), segundero=0, ventana=1.0, turno="dormida", escarcha=0.9, seed=3)
    personajes.rafa_cama(ctx, *cuarto.CABEZA, 1.0, t, ojos="abiertos", mira=(1.0, -0.4), boca="abierta", rubor=0.3, sudor=0.5)
    objetos.vaho(ctx, cuarto.CABEZA[0] + 10, cuarto.CABEZA[1] + 30, t, 1.4)
    inc = 0.50 * smooth(seg(t, 0.2, 2.0))
    ab = smooth(seg(t, 3.2, PASTILLA + 0.2))
    personajes.eulalia(ctx, 560, 1230, 1.0, t, pose="ofrece", cara=0.0, halo=1.0, inclina=inc, sonrisa=1.0, k_brazo=ab,
                       pastilla=t >= PASTILLA)
    ctx.restore()
    vignette(ctx, 0.72)
    darken(ctx, 1 - smooth(seg(t, 0, 0.2)))
    darken(ctx, smooth(seg(t, DURATION - 0.25, DURATION)))
