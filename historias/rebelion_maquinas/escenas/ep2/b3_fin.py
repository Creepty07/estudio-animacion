"""Resultado del final regular."""
from historias.rebelion_maquinas.dibujo.cards import result_card

DURATION = 5.0
SUBS = []


def draw(ctx, t):
    result_card(ctx, t, DURATION, "regular", "SOBREVIVES", "…pero perdiste tu única forma de comunicarte.",
                losses=[("backpack", "Mochila"), ("radio", "Radio")], footer="OPCIÓN 2 · ESCALERA DE SERVICIO")
