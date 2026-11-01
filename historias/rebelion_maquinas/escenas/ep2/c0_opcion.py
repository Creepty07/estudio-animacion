"""Tarjeta: si elegiste la opción 3 (ducto)."""
from historias.rebelion_maquinas.dibujo.cards import option_card

DURATION = 2.2
SUBS = []


def draw(ctx, t):
    option_card(ctx, t, DURATION, 3, "Te metes al", "Ducto de ventilación", "vent")
