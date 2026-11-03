"""Parte 3, escena 2 — Título con falla y kicker "Parte 3 de 3"."""
from motor.config import AMBAR
from motor.kit import title_card, particles
from historias.ruta0.dibujo.comun import marco

DURATION = 4.0
SUBS = []


def draw(ctx, t):
    title_card(ctx, t, ["EL CAMIÓN", "SIN NÚMERO"], kicker="PARTE 3 DE 3", accent=AMBAR)
    particles(ctx, t, AMBAR, n=22, seed=7, rise=14, size=(1.2, 2.6), alpha=0.6)
    marco(ctx, t, DURATION, 0.6, 0.25, 0.12)
