"""Ep2 escena 2 — Tarjeta del final 1: Fingir que duerme (final malo)."""
from motor import tarjetas
from motor.primitives import seg, smooth, darken, vignette

DURATION = 2.5
SUBS = []
GOLPE = 0.0
ROJO = (1.0, 0.45, 0.42)


def draw(ctx, t):
    tarjetas.tarjeta_final(ctx, t, 1, "FINGIR\nQUE DUERME", "FINAL MALO", ROJO, DURATION)
    vignette(ctx, 0.55)
    darken(ctx, smooth(seg(t, DURATION - 0.15, DURATION)))
