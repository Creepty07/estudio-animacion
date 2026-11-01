"""Tarjeta: si elegiste la opción 2 (escalera)."""
from historias.rebelion_maquinas.dibujo.cards import option_card

DURATION = 2.2
SUBS = []


def draw(ctx, t):
    option_card(ctx, t, DURATION, 2, "Subes por la", "Escalera de servicio", "stairs")
