"""Escena 2 — Título con falla: LA PLANCHADA · "Tú eliges el final"."""
from motor.config import W, H, ACENTO
from motor.primitives import seg, smooth, vignette, darken
from motor.kit import title_card, particles

DURATION = 4.0
SUBS = []
CORTE = DURATION - 0.0        # el riser de la mezcla se corta en seco al final


def draw(ctx, t):
    title_card(ctx, t, ["LA", "PLANCHADA"], kicker="TÚ ELIGES EL FINAL", accent=ACENTO)
    particles(ctx, t, ACENTO, n=24, seed=5, rise=16, size=(1.2, 2.8), alpha=0.7)
    vignette(ctx, 0.6)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.25)))
    darken(ctx, smooth(seg(t, DURATION - 0.12, DURATION)))
