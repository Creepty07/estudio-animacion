"""Parte 1, escena 2 — Título con falla (título provisional) y kicker "Parte 1 de 3"."""
from motor import config
from motor.config import TITULO, AMBAR
from motor.primitives import glow
from motor.kit import title_card, particles
from historias.ruta0.dibujo.comun import marco

DURATION = 4.0
SUBS = []
TITULO_LINEAS = ["EL CAMIÓN", "SIN NÚMERO"]


def draw(ctx, t):
    title_card(ctx, t, TITULO_LINEAS, kicker="PARTE 1 DE 3", accent=AMBAR)
    particles(ctx, t, AMBAR, n=22, seed=5, rise=14, size=(1.2, 2.6), alpha=0.6)
    marco(ctx, t, DURATION, 0.6, 0.25, 0.12)
