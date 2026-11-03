"""Parte 3, escena 4 — Entonces la pasajera habló, de frente por primera vez, pálida y triste, sin respirar, los ojos en sombra.
«Este camión no se lleva a los muertos. Avisa a los que van a morir.»"""
from motor.config import W, H
from motor.primitives import seg, smooth, lerp
from historias.ruta0.dibujo import interior as I
from historias.ruta0.dibujo.paleta import degradado_v
from historias.ruta0.dibujo.comun import marco

DURATION = 9.6
SUBS = [
    (0.3, 1.9, "Entonces, la pasajera habló.", None),
    (2.2, 5.7, "«Este camión no se lleva a los muertos.»", "Pasajera"),
    (6.0, 9.1, "«Avisa a los que van a morir.»", "Pasajera"),
]


def draw(ctx, t):
    degradado_v(ctx, 0, 0, W, H, (0.025, 0.03, 0.035), (0.07, 0.075, 0.075))
    I.cara_pasajera(ctx, t, 540, 740, lerp(0.95, 1.25, smooth(seg(t, 0, DURATION))))
    marco(ctx, t, DURATION, 0.8, 0.5, 0.3)
