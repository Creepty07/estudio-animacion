"""Parte 3, escena 6 — Iván bajó. A su espalda, todos lo miraban; él no miró atrás. El motor se va de golpe y corte a blanco."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, fill_screen
from historias.ruta0.dibujo import exterior, camion
from historias.ruta0.dibujo.comun import lluvia, niebla, marco, ivan_de_pie

DURATION = 8.0
SUBS = [
    (0.3, 1.5, "Iván bajó.", None),
    (1.8, 4.2, "A su espalda, todos lo miraban.", None),
    (4.5, 5.7, "No miró atrás.", None),
]
SILENCIO = (4.6, 5.9)     # silencio antes del golpe
BLANCO = (5.9, 7.3)       # el motor se va de golpe y la imagen se va a blanco


def draw(ctx, t):
    exterior.escena_parada(ctx, t, luz=0.0, bruma=0.5, con_parada=False)
    camion.camion_lado(ctx, 470, exterior.SUELO + 120, 1.0, t, zero=1.0, puertas=1.0 - smooth(seg(t, 0.8, 1.6)), faros=1.0,
                       caras=smooth(seg(t, 1.0, 2.0)))
    k = smooth(seg(t, 0.4, 5.8))
    ivan_de_pie(ctx, lerp(700, 560, k), lerp(exterior.SUELO + 60, exterior.SUELO + 330, k), lerp(1.1, 2.0, k), "camina", math.sin(t * 5.5) * 0.9)
    niebla(ctx, t, 0.2)
    lluvia(ctx, t, 160, 0.24)
    marco(ctx, t, DURATION, 0.7, 0.3, 0.0)
    b = smooth(seg(t, *BLANCO)) if t < 7.5 else 1.0 - smooth(seg(t, 7.5, 8.0)) * 0.0
    fill_screen(ctx, (1, 1, 1), b)
