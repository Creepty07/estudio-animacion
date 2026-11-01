"""Resultado del final bueno (el camino oficial de la serie)."""
from historias.rebelion_maquinas.dibujo.cards import result_card

DURATION = 5.5
SUBS = []


def draw(ctx, t):
    result_card(ctx, t, DURATION, "bueno", "SOBREVIVES", "No pierdes nada. Y no estás solo.",
                sub_line="Este es el camino oficial de la historia.",
                footer="CONTINÚA EN EL CAPÍTULO 2 · LA CIUDAD CALLADA")
