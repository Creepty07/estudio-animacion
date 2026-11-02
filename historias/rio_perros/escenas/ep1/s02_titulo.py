"""Escena 2 — Título: EL RÍO DE LOS PERROS sobre un llamado de caracol."""
from motor.config import W, H, ACENTO
from motor.primitives import seg, smooth, darken, vignette
from motor.kit import title_card, particles

DURATION = 3.4
SUBS = []
CARACOL = 0.0          # el caracol suena desde el primer cuadro
GOLPE = 0.42           # el título entra (golpe de tambor)


def draw(ctx, t):
    title_card(ctx, t, ["EL RÍO", "DE LOS PERROS"], kicker="LEYENDA MEXICANA", accent=ACENTO, bg=(0.004, 0.012, 0.024))
    particles(ctx, t, ACENTO, n=24, seed=5, rise=16, size=(1.2, 2.8), alpha=0.7)
    vignette(ctx, 0.62)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.2)))
    darken(ctx, smooth(seg(t, DURATION - 0.35, DURATION)))
