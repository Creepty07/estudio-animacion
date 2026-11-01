"""Escena de ejemplo: tarjeta de título + una línea narrada.

Contrato de toda escena:
  DURATION  duración en segundos sin voz (el motor la alarga si una línea no cabe)
  SUBS      lista de (inicio, fin, texto, hablante|None); cada línea se narra con la voz de su hablante
  draw(ctx, t)  dibuja el instante t (tiempo local de la escena) a tamaño config.W x config.H
"""
from motor.config import W, H, ACENTO
from motor.primitives import seg, smooth, darken, vignette
from motor.kit import title_card, particles

DURATION = 5.0
SUBS = [
    (2.2, 4.8, "Así empieza una historia nueva.", None),
]


def draw(ctx, t):
    title_card(ctx, t, ["TÍTULO", "DE LA HISTORIA"], kicker="CAPÍTULO 1", accent=ACENTO)
    particles(ctx, t, ACENTO, n=30)
    vignette(ctx, 0.6)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.3)))
    darken(ctx, smooth(seg(t, DURATION - 0.3, DURATION)))
