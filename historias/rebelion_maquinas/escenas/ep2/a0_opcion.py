"""Tarjeta: si elegiste la opción 1 (elevador)."""
from historias.rebelion_maquinas.dibujo.cards import option_card

DURATION = 2.2
SUBS = []


def draw(ctx, t):
    option_card(ctx, t, DURATION, 1, "Corres al", "Elevador de carga", "elevator")
