"""Ep2 escena 9 — Las luces del pasillo se apagaron, una por una. Al fondo, un instante, una figura blanca de espaldas."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera, vignette, darken, fill_rrect
from historias.planchada.dibujo import pasillo
from historias.planchada.dibujo.paleta import fluo_brillo

DURATION = 6.0
SUBS = [
    (0.3, 3.6, "Las luces del pasillo se apagaron, una por una.", None),
    (3.9, 5.8, "La fiebre seguía ahí.", None),
]
N = 7
APAGONES = [0.5 + 0.42 * i for i in range(N)]      # cuándo se apaga cada fluorescente (cerca → lejos); un clic por cada uno
FIGURA = (3.55, 4.25)


def draw(ctx, t):
    luces = []
    for i, a in enumerate(APAGONES):
        if t < a - 0.18:
            luces.append(1.0)
        elif t < a + 0.12:
            luces.append(0.15 + 0.5 * fluo_brillo(t, 40 + i, "inestable"))
        else:
            luces.append(0.0)
    fig = None
    if FIGURA[0] <= t <= FIGURA[1]:
        fig = (0.90, smooth(seg(t, FIGURA[0], FIGURA[0] + 0.1)) * (1 - smooth(seg(t, FIGURA[1] - 0.15, FIGURA[1]))))
    ctx.save()
    camera(ctx, lerp(1.0, 1.12, smooth(seg(t, 0, DURATION))), W / 2, 820)
    pasillo.pasillo(ctx, t, luces=luces, figura=fig, brillo=1.0, fondo_luz=0.5, n_luces=N)
    ctx.restore()
    # sombra del marco de la puerta y del pie de la cama: se ve desde la cama
    fill_rrect(ctx, 0, 1500, W, 420, 0, (0.01, 0.02, 0.03), 0.9)
    vignette(ctx, 0.8)
    darken(ctx, 1 - smooth(seg(t, 0, 0.25)))
    darken(ctx, smooth(seg(t, DURATION - 0.25, DURATION)))
