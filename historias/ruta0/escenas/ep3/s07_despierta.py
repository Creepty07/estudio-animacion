"""Parte 3, escena 7 — Iván abre los ojos en la banca de su parada; ya no llueve. Vibra su celular: Beto: «¿Te llevo? Ya voy en el coche.»"""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, fill_screen, glow
from historias.ruta0.dibujo import exterior, interior as I
from historias.ruta0.dibujo.paleta import ovalo, degradado_v
from historias.ruta0.dibujo.comun import marco, ivan_de_pie, niebla

DURATION = 9.6
SUBS = [
    (0.3, 3.8, "Abrió los ojos en la banca de su parada.", None),
    (4.1, 5.7, "Entonces vibró su celular.", None),
    (6.0, 9.1, "«¿Te llevo? Ya voy en el coche.»", "Beto"),
]
VIBRA = 4.6               # vibración del celular (la mezcla)


def draw(ctx, t):
    if t < 5.9:
        exterior.escena_parada(ctx, t, luz=0.8, bruma=0.0, x_parada=540)
        abre = smooth(seg(t, 0.5, 1.8))
        ctx.save()
        ctx.translate(540, exterior.SUELO + 30 - 100)
        ctx.rotate(0.0)
        ovalo(ctx, 0, 40, 74, 60, (0.2, 0.3, 0.46))                                              # Iván dormido en la banca, ahora despierta
        ovalo(ctx, 0, -60, 40, 46, (0.66, 0.46, 0.34))
        ovalo(ctx, -6, -86, 42, 24, (0.04, 0.035, 0.04))
        for sx in (-14, 14):
            ovalo(ctx, sx, -58, 8, 8 * abre + 1.5, (0.96, 0.96, 0.96))
            ovalo(ctx, sx, -58, 4, 4 * abre + 0.8, (0.05, 0.03, 0.03))
        ctx.restore()
        niebla(ctx, t, 0.08)
    else:
        degradado_v(ctx, 0, 0, W, H, (0.03, 0.04, 0.06), (0.08, 0.1, 0.14))
    if t >= 4.6:
        k = smooth(seg(t, 4.6, 6.0))
        I.celular(ctx, 540, lerp(1500, 760, k), lerp(0.7, 0.95, k), t, "¿Te llevo?", "Ya voy en el coche.", 1.0, vibra=1.0 if t < 6.0 else 0.0, remitente="Beto")
    marco(ctx, t, DURATION, 0.65, 0.4, 0.3)
