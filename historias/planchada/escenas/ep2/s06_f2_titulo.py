"""Ep2 escena 6 — Tarjeta del final 2: Tocar el timbre (final regular)."""
from motor import tarjetas
from motor.primitives import seg, smooth, darken, vignette

DURATION = 2.5
SUBS = []
GOLPE = 0.0
AMBAR = (1.0, 0.80, 0.40)


def draw(ctx, t):
    tarjetas.tarjeta_final(ctx, t, 2, "TOCAR\nEL TIMBRE", "FINAL REGULAR", AMBAR, DURATION)
    vignette(ctx, 0.55)
    darken(ctx, smooth(seg(t, DURATION - 0.15, DURATION)))
