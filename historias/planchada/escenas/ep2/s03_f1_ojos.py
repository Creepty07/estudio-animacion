"""Ep2 escena 3 — Rafa cerró los ojos. Ella dejó la pastilla en el buró y desapareció: sin caminar, el halo se apaga."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera_center, vignette, darken
from historias.planchada.dibujo import cuarto, personajes, objetos
from historias.planchada.dibujo.paleta import fluo_brillo

DURATION = 6.0
SUBS = [
    (0.2, 2.6, "Rafa cerró los ojos.", None),
    (2.8, 5.8, "Ella dejó la pastilla y se fue.", None),
]
DEJA = 3.4               # la pastilla queda en el buró
DESAPARECE = (4.0, 4.7)  # el halo se apaga y ella se va, sin pasos


def draw(ctx, t):
    ctx.save()
    cuarto.cam(ctx, lerp(1.25, 1.35, smooth(seg(t, 0, DURATION))), lerp(420, 450, smooth(seg(t, 0, DURATION))), 850)
    cuarto.cuarto(ctx, t, fluo=0.55 + 0.1 * fluo_brillo(t, 21, "inestable"), hora=(3, 0), segundero=0, ventana=1.0, turno="dormida", escarcha=0.9,
                  pastilla_buro=t >= DEJA, seed=3)
    personajes.rafa_cama(ctx, *cuarto.CABEZA, 1.0, t, ojos="apretados", boca="cerrada", rubor=0.6, sudor=1.0)
    ex = smooth(seg(t, 2.6, DEJA))                                                   # extiende el brazo hacia el buró (mirando a la derecha)
    al = 1 - smooth(seg(t, *DESAPARECE))
    personajes.eulalia(ctx, 560, 1230, 1.0, t, pose="ofrece", cara=0.0, halo=al, alpha=al, inclina=0.12 * ex, sonrisa=0.0,
                       k_brazo=ex, pastilla=t < DEJA, espejo=True)
    ctx.restore()
    vignette(ctx, 0.72)
    darken(ctx, 1 - smooth(seg(t, 0, 0.2)))
    darken(ctx, smooth(seg(t, DURATION - 0.25, DURATION)))
