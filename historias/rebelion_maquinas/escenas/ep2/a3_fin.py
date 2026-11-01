"""Resultado del final malo."""
from historias.rebelion_maquinas.dibujo.cards import result_card

DURATION = 4.5
SUBS = []


def draw(ctx, t):
    result_card(ctx, t, DURATION, "malo", "FIN", "Ágora controla cada elevador de la ciudad.",
                footer="OPCIÓN 1 · ELEVADOR DE CARGA")
