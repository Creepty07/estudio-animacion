"""Ep2 escena 11 — «¿Cómo se llama?» Ella se detiene y, por primera vez, se le ve la cara: joven, cansada, amable. El fluorescente deja de parpadear."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera_center, vignette, darken
from historias.planchada.dibujo import cuarto, personajes, objetos

DURATION = 6.0
SUBS = [
    (0.2, 2.4, "«¿Cómo se llama?»", "Rafa"),
    (3.6, 5.8, "«Eulalia.»", "Enfermera"),
]
SILENCIO = (2.4, 3.6)     # todo baja menos el goteo y un drone muy bajo
NOMBRE = 3.6              # nota grave cálida bajo el nombre
CARA = (3.0, 3.7)         # el rostro aparece


def draw(ctx, t):
    k = smooth(seg(t, 2.0, 3.6))
    ctx.save()
    cuarto.cam(ctx, lerp(1.3, 2.3, k), lerp(430, 520, k), lerp(840, 700, k))
    estable = smooth(seg(t, 2.5, 3.0))
    cuarto.cuarto(ctx, t, fluo=lerp(0.5 + 0.25 * math.sin(t * 40) ** 2, 0.95, estable), hora=(3, 0), segundero=None, ventana=1.0, turno="dormida", seed=3)
    habla = t < 2.4 and int(t * 6) % 2 == 0
    personajes.rafa_cama(ctx, *cuarto.CABEZA, 1.0, t, ojos="abiertos", mira=(1.0, -0.2), boca="abierta" if habla else "cerrada", rubor=0.3, sudor=0.5)
    objetos.vaho(ctx, cuarto.CABEZA[0] + 10, cuarto.CABEZA[1] + 30, t, 1.2)
    personajes.eulalia(ctx, 560, 1230, 1.0, t, pose="ofrece", cara=smooth(seg(t, *CARA)), halo=1.0, inclina=0.35 * (1 - k * 0.7), sonrisa=0.4 * smooth(seg(t, 3.4, 4.2)),
                       k_brazo=1.0, pastilla=True)
    ctx.restore()
    vignette(ctx, 0.66)
    darken(ctx, 1 - smooth(seg(t, 0, 0.2)))
    darken(ctx, smooth(seg(t, DURATION - 0.25, DURATION)))
