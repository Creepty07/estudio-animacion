"""Fondo desenfocado detrás de la tumba sin nombre: lejanía con siluetas, luces como 'bokeh' y niebla.

Se usa en los primeros planos (escenas 4, 9, 10, 11 y 12). La tumba la dibuja cada escena encima.
"""
import math
import random
from motor import config
from motor.config import NOCHE_ALTO, NOCHE_BAJO, LLAMA
from motor.primitives import glow, src, TAU, mix
from motor.layers import paint_layer
from motor.kit import fog
from historias.tumba_llorona.dibujo import cielo, tumbas, paisaje

HORIZ = 0.60


def _siluetas(modo):
    def painter(ctx):
        W, H = config.W, config.H
        col = (0.012, 0.022, 0.04) if modo == "noche" else (0.10, 0.07, 0.12)
        r = random.Random(33)
        for i in range(10):
            paisaje.ahuejote(ctx, (i + 0.5) / 10 * W + r.uniform(-30, 30), H * HORIZ - 6, 0.34 + 0.18 * r.random(), seed=i, color=col)
        for i in range(16):
            x = r.uniform(0, W)
            s = r.uniform(0.28, 0.55)
            (tumbas.cruz if r.random() < 0.6 else tumbas.lapida)(ctx, x, H * HORIZ + r.uniform(0, 26), s, 0.3)
        ctx.rectangle(0, H * HORIZ - 4, W, 8)
        src(ctx, col)
        ctx.fill()
    return painter


def _suelo(modo):
    def painter(ctx):
        H = config.H
        if modo == "noche":
            cielo.gradiente_vertical(ctx, [(0, (0.045, 0.06, 0.10)), (1, (0.012, 0.016, 0.03))], H * HORIZ, H)
        else:
            cielo.gradiente_vertical(ctx, [(0, (0.22, 0.14, 0.16)), (1, (0.05, 0.04, 0.06))], H * HORIZ, H)
    return painter


def fondo(ctx, t, modo="noche", bokeh=1.0, niebla=1.0, avance_alba=1.0):
    W, H = config.W, config.H
    if modo == "noche":
        cielo.gradiente_vertical(ctx, [(0, NOCHE_ALTO), (1, NOCHE_BAJO)], 0, H * HORIZ + 2)
        cielo.estrellas(ctx, t, 60, y_max=HORIZ * 0.85, seed=21)
        cielo.luna(ctx, W * 0.78, H * 0.12, 46, 0.95)
    else:
        cielo.amanecer(ctx, avance_alba, horizonte=HORIZ)
        glow(ctx, W * 0.3, H * HORIZ, 760, (1.0, 0.62, 0.38), 0.45 * avance_alba)
    paint_layer(ctx, ("sil_" + modo, HORIZ), _siluetas(modo))
    paint_layer(ctx, ("suelo_" + modo, HORIZ), _suelo(modo))
    if modo == "noche" and bokeh > 0:
        r = random.Random(7)
        for i in range(28):                                     # velas lejanas fuera de foco
            x, y, rad = r.uniform(0, W), r.uniform(H * 0.45, H * HORIZ + 40), r.uniform(26, 70)
            glow(ctx, x, y, rad * (1 + 0.06 * math.sin(t * 2 + i)), LLAMA, 0.22 * bokeh)
    fog(ctx, t, (0.55, 0.65, 0.85) if modo == "noche" else (1.0, 0.78, 0.7), 0.12 * niebla, H * 0.52, H * 0.72, seed=4, speed=10)
