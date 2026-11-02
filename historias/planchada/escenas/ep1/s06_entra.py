"""Escena 6 — Ya está dentro, sin haber caminado. Uniforme blanco sin una arruga; la cara en sombra, solo la barbilla en su halo."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera_center, vignette, darken
from historias.planchada.dibujo import cuarto, personajes, objetos
from historias.planchada.dibujo.paleta import fluo_brillo

DURATION = 8.0
SUBS = [
    (0.5, 3.2, "No se oyeron sus pasos.", None),
    (3.8, 7.6, "Su uniforme no tenía ni una arruga.", None),
]
APARECE = 0.2            # ella está dentro: se caen el reloj y el monitor (la mezcla)


def draw(ctx, t):
    k = smooth(seg(t, 0, DURATION))
    ctx.save()
    cuarto.cam(ctx, lerp(1.15, 1.7, k), lerp(430, 500, k), lerp(870, 720, k))
    cuarto.cuarto(ctx, t, fluo=0.45 + 0.1 * fluo_brillo(t, 6, "inestable"), hora=(3, 0), segundero=0, ventana=1.0, turno="dormida", seed=3, gota=True)
    personajes.rafa_cama(ctx, *cuarto.CABEZA, 1.0, t, ojos="abiertos", mira=(1.0, -0.5), boca="abierta", rubor=0.5, sudor=1.0)
    objetos.vaho(ctx, cuarto.CABEZA[0] + 10, cuarto.CABEZA[1] + 30, t, 1.0)
    personajes.eulalia(ctx, 540, 1230, 1.0, t, pose="pie", cara=0.0, halo=1.0, alpha=smooth(seg(t, 0.0, 0.4)))
    ctx.restore()
    vignette(ctx, 0.72)
    darken(ctx, 1 - smooth(seg(t, 0, 0.2)))
    darken(ctx, smooth(seg(t, DURATION - 0.25, DURATION)))
