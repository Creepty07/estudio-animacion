"""Escena 10 — ¿Qué hace Rafa? Tres tarjetas verticales (1 Fingir que duerme · 2 Tocar el timbre · 3 Preguntarle su nombre).
Al fondo, la enfermera desenfocada con la pastilla. El latido se corta en seco a negro en 10.3."""
import math
from motor.config import W, H, ACENTO
from motor.primitives import seg, smooth, vignette, darken, glow, fill_screen
from motor import tarjetas
from historias.planchada.dibujo import personajes
from historias.planchada.dibujo.paleta import degradado_v, FLUO

DURATION = 10.5
SUBS = [
    (8.2, 10.2, "Comenta 1, 2 o 3.", None),
]
TARJETAS = [1.8, 2.6, 3.4]       # golpe grave por tarjeta (la mezcla)
NEGRO = 10.3                     # corte a negro seco
OPCIONES = ["Fingir que duerme", "Tocar el timbre", "Preguntarle su nombre"]
COLORES = [(1.0, 0.45, 0.42), (1.0, 0.80, 0.40), (0.55, 0.96, 1.0)]       # malo, regular, bueno (sin decir cuál es cuál)


def draw(ctx, t):
    if t >= NEGRO:
        fill_screen(ctx, (0, 0, 0))
        return
    fill_screen(ctx, (0.015, 0.035, 0.05))
    degradado_v(ctx, 0, 0, W, H, (0.02, 0.05, 0.07), (0.04, 0.10, 0.12))
    for dx, a in ((-14, 0.10), (0, 0.18), (14, 0.10)):                                 # fondo desenfocado: tres copias flojas
        ctx.save()
        ctx.translate(dx, 0)
        personajes.eulalia(ctx, 540, 1420, 1.55, t, pose="ofrece", cara=0.0, halo=1.3, alpha=a, inclina=0.0, pastilla=False, k_brazo=1.0)
        ctx.restore()
    glow(ctx, 540, 960, 700, FLUO, 0.10)
    tarjetas.eleccion(ctx, t, "¿QUÉ HACE RAFA?", OPCIONES, ACENTO, COLORES, t_pregunta=(0.2, 1.6), t_tarjetas=tuple(TARJETAS))
    vignette(ctx, 0.6)
    darken(ctx, 1 - smooth(seg(t, 0, 0.2)))
