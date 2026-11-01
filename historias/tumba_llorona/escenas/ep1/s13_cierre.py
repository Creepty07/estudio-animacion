"""Escena 13 — Tarjeta de cierre: "¿Le habrías dejado la flor?" con SÍ / NO para los comentarios."""
from motor.primitives import seg, smooth, darken
from historias.tumba_llorona.dibujo import tarjeta

DURATION = 3.7
SUBS = [
    (0.3, 3.5, "¿Tú le habrías dejado la flor? Comenta sí o no.", None),
]


def draw(ctx, t):
    tarjeta.dibujar(ctx, t, DURATION)
    darken(ctx, 1 - smooth(seg(t, 0, 0.3)))
    darken(ctx, smooth(seg(t, DURATION - 0.4, DURATION)))
