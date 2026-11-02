"""Escena 9 — En el reflejo de la ventana, ella no estaba. Corte a ella, que sigue ahí, con la pastilla: susto 2."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera_center, vignette, darken, glow, circle, fill_rrect, line
from historias.planchada.dibujo import cuarto, personajes, objetos
from historias.planchada.dibujo.paleta import fluo_brillo, ovalo, BATA, COBIJA, CABELLO, PIEL, HALO

DURATION = 5.0
SUBS = [
    (0.4, 2.0, "Rafa miró la ventana.", None),
    (2.3, 4.8, "En el reflejo, ella no estaba.", None),
]
LATIDOS = [0.2, 0.9, 1.5]           # el latido acelera
SILENCIO = (1.9, 2.2)               # se corta todo
SUSTO = 2.2                         # corte a ella (golpe + glitch)


def _reflejo(ctx, x, y, w, h):
    """Lo que devuelve el vidrio: la cama, Rafa con la cabeza girada, y la silla de al lado… vacía."""
    ctx.save()
    ctx.translate(x + w * 0.5, y + h * 0.72)
    sc = w / 400
    ctx.scale(sc, sc)
    fill_rrect(ctx, -200, 20, 400, 40, 12, (0.8, 0.95, 1.0), 0.62)                       # cama
    fill_rrect(ctx, -200, -10, 270, 40, 18, (0.85, 0.97, 1.0), 0.55)
    ovalo(ctx, -130, -34, 38, 38, (1.0, 0.92, 0.85), 0.62)                                 # cabeza de Rafa
    ovalo(ctx, -130, -56, 40, 20, (0.1, 0.12, 0.15), 0.7)
    fill_rrect(ctx, 70, -140, 100, 12, 5, (0.85, 0.97, 1.0), 0.55)                        # silla vacía
    fill_rrect(ctx, 70, -140, 12, 170, 5, (0.85, 0.97, 1.0), 0.55)
    fill_rrect(ctx, 70, -34, 100, 12, 5, (0.85, 0.97, 1.0), 0.55)
    line(ctx, 162, -34, 162, 40, 9, (0.85, 0.97, 1.0), 0.55)
    ctx.restore()
    ctx.save()
    ctx.set_operator(__import__("cairo").OPERATOR_ADD)
    glow(ctx, x + w * 0.3, y + h * 0.3, w * 0.7, (0.6, 0.85, 0.95), 0.10)
    ctx.restore()


def draw(ctx, t):
    ctx.save()
    if t < SUSTO:
        k = smooth(seg(t, 0, SUSTO))
        cuarto.cam(ctx, lerp(1.9, 2.25, k), 265, 600)
        cuarto.cuarto(ctx, t, fluo=0.4 + 0.2 * fluo_brillo(t, 9, "inestable"), hora=(3, 0), segundero=0, ventana=0.0, escarcha=0.25, turno="dormida",
                      seed=3, reflejo=_reflejo, cortinas=False)
    else:
        cuarto.cam(ctx, lerp(1.45, 1.55, smooth(seg(t, SUSTO, DURATION))), 400, 850)
        cuarto.cuarto(ctx, t, fluo=0.55, hora=(3, 0), segundero=0, ventana=1.0, escarcha=0.9, turno="dormida", seed=3)
        personajes.rafa_cama(ctx, *cuarto.CABEZA, 1.0, t, ojos="abiertos", mira=(-1.0, -0.4), boca="abierta", rubor=0.2, sudor=0.4)
        objetos.vaho(ctx, cuarto.CABEZA[0] + 10, cuarto.CABEZA[1] + 30, t, 1.4)
        personajes.eulalia(ctx, 560, 1230, 1.0, t, pose="ofrece", cara=0.0, halo=1.2, inclina=0.5, sonrisa=1.0, k_brazo=1.0, pastilla=True)
    ctx.restore()
    vignette(ctx, 0.72)
    darken(ctx, 1 - smooth(seg(t, 0, 0.2)))
    darken(ctx, smooth(seg(t, DURATION - 0.2, DURATION)))
