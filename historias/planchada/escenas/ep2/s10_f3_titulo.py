"""Ep2 escena 10 — Tarjeta del final 3: Preguntarle su nombre (final bueno)."""
from motor import tarjetas
from motor.primitives import seg, smooth, darken, vignette

DURATION = 2.5
SUBS = []
GOLPE = 0.0
CIAN = (0.55, 0.96, 1.0)


def draw(ctx, t):
    tarjetas.tarjeta_final(ctx, t, 3, "PREGUNTARLE\nSU NOMBRE", "FINAL BUENO", CIAN, DURATION)
    vignette(ctx, 0.55)
    darken(ctx, smooth(seg(t, DURATION - 0.15, DURATION)))
