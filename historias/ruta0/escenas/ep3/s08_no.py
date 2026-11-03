"""Parte 3, escena 8 — Iván: «No, gracias. Me voy a pie.» Esa noche no se subió: se va caminando; unos faros pasan por la calle de atrás, sin detalle."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, fill_screen, glow
from historias.ruta0.dibujo import exterior, interior as I
from historias.ruta0.dibujo.paleta import degradado_v
from historias.ruta0.dibujo.comun import marco, ivan_de_pie, niebla

DURATION = 7.5
SUBS = [
    (0.3, 3.0, "«No, gracias. Me voy a pie.»", "Iván"),
    (3.3, 6.8, "Esa noche, Iván no se subió a ese coche.", None),
]
CARRO = (4.4, 6.0)        # un coche pasa y se aleja normal (la mezcla)


def draw(ctx, t):
    if t < 3.1:
        degradado_v(ctx, 0, 0, W, H, (0.03, 0.04, 0.06), (0.08, 0.1, 0.14))
        escribe = int(seg(t, 0.2, 2.2) * 21)
        I.celular(ctx, 540, 780, 0.95, t, ("No, gracias. Me voy a pie.")[:escribe], "", 1.0, remitente="Iván")
    else:
        exterior.escena_parada(ctx, t, luz=0.8, bruma=0.0, x_parada=300)
        k = seg(t, CARRO[0], CARRO[1])
        if 0 < k < 1:                                                                            # faros de un coche detrás
            x = lerp(-100, 1200, k)
            glow(ctx, x, exterior.HORIZONTE + 160, 220, (1.0, 0.95, 0.8), 0.55)
            glow(ctx, x + 70, exterior.HORIZONTE + 160, 220, (1.0, 0.95, 0.8), 0.55)
        w = smooth(seg(t, 3.2, 7.2))
        ivan_de_pie(ctx, lerp(520, 980, w), exterior.SUELO + 110, 1.4, "camina", math.sin(t * 5.2) * 0.9, alpha=1 - smooth(seg(t, 6.6, 7.4)))
        niebla(ctx, t, 0.06)
    marco(ctx, t, DURATION, 0.65, 0.3, 0.3)
