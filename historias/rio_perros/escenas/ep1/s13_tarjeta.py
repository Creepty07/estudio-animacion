"""Escena 13 — Tarjeta de cierre: ¿Y a ti, quién te cruzaría? (el texto va dibujado en la tarjeta)."""
from motor.primitives import seg, smooth, darken
from historias.rio_perros.dibujo import tarjeta

DURATION = 5.2
SUBS = []


def draw(ctx, t):
    tarjeta.dibujar(ctx, t, DURATION)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.3)))
    darken(ctx, smooth(seg(t, DURATION - 0.4, DURATION)))
