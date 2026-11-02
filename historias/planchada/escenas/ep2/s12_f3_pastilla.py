"""Ep2 escena 12 — Rafa se tomó la pastilla. Su mano estaba helada. Ella le pone la mano en la frente y él se duerme; la escarcha se deshace."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera_center, vignette, darken
from historias.planchada.dibujo import cuarto, personajes, objetos

DURATION = 5.5
SUBS = [
    (0.2, 2.4, "Rafa se tomó la pastilla.", None),
    (2.7, 5.3, "Su mano estaba helada.", None),
]
TOQUE = 2.7               # cold_touch: la mano en la frente
TRAGA = 1.3


def draw(ctx, t):
    ctx.save()
    cuarto.cam(ctx, lerp(1.35, 1.6, smooth(seg(t, 0, DURATION))), 330, 880)
    esc = 0.9 * (1 - smooth(seg(t, 3.0, 5.2)))
    cuarto.cuarto(ctx, t, fluo=0.9, hora=(3, 0), segundero=None, ventana=1.0, escarcha=esc, turno="dormida", seed=3)
    dormido = smooth(seg(t, 4.2, 4.8)) > 0.5
    ojos = "cerrados" if dormido else "abiertos"
    boca = "abierta" if 1.1 <= t <= 1.9 else "cerrada"
    personajes.rafa_cama(ctx, *cuarto.CABEZA, 1.0, t, ojos=ojos, mira=(1.0, -0.3), boca=boca, rubor=max(0.0, 0.5 - 0.5 * smooth(seg(t, 2.7, 5.0))),
                         sudor=max(0.0, 1 - smooth(seg(t, 2.7, 4.5))), respira=1.0)
    k = smooth(seg(t, 2.0, TOQUE))
    personajes.eulalia(ctx, 560, 1230, 1.0, t, pose="frente", cara=0.9, halo=1.0, inclina=0.42 * smooth(seg(t, 0.2, 1.6)), sonrisa=0.9,
                       k_brazo=k, pastilla=t < 1.4)
    ctx.restore()
    vignette(ctx, 0.62)
    darken(ctx, 1 - smooth(seg(t, 0, 0.2)))
    darken(ctx, smooth(seg(t, DURATION - 0.25, DURATION)))
