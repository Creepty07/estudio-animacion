"""Parte 3, escena 1 — Gancho: el dedo de Iván sobre el botón de parada; detrás, desenfocado, el tablero con IVÁN."""
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, glow
from historias.ruta0.dibujo import interior as I
from historias.ruta0.dibujo.paleta import ovalo, degradado_v
from historias.ruta0.dibujo.comun import marco

DURATION = 6.0
SUBS = [
    (0.6, 3.3, "Iván ya sabía cuál era su parada.", None),
    (3.6, 5.2, "Tenía que bajarse antes.", None),
]
SUSTO = 0.1


def draw(ctx, t):
    degradado_v(ctx, 0, 0, W, H, (0.05, 0.055, 0.05), (0.12, 0.12, 0.09))
    ctx.save()
    ctx.translate(540, 500)
    ctx.scale(1.1, 1.1)
    ctx.translate(-2400, -470)
    I.tablero_ruta(ctx, 2400, 470, (1, 0, 0, 1), t, ivan_flash=0.0)
    ctx.restore()
    for dx, a in ((-18, 0.10), (0, 0.16), (18, 0.10)):                       # desenfoque: copias flojas encima
        ctx.set_source_rgba(0.04, 0.045, 0.04, a * 3)
        ctx.rectangle(0, 300, W, 500)
        ctx.fill()
    d = smooth(seg(t, 0.3, 3.6))
    I.boton_parada(ctx, 540, 1000, 2.6, foco=0.0, presionado=0.0, t=t)
    ovalo(ctx, lerp(820, 600, d), lerp(1280, 1000, d), 52, 120, (0.66, 0.46, 0.34), 1.0, -0.8)       # el dedo, vacilando
    marco(ctx, t, DURATION, 0.7, 0.0, 0.25)
