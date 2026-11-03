"""Parte 1, escena 6 — Nadie se movía. El aliento de Iván empaña el vidrio; el de los demás, no. Silencio total. Nadie respiraba."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, fill_screen
from historias.ruta0.dibujo import interior as I
from historias.ruta0.dibujo.comun import marco

DURATION = 9.5
SUBS = [
    (0.3, 1.5, "Nadie se movía.", None),
    (1.8, 6.5, "El aliento de Iván empañaba el vidrio; el de los demás, no.", None),
    (7.7, 8.9, "Nadie respiraba.", None),
]
SILENCIO = (6.6, 7.7)     # se va todo (motor, lluvia): silencio total
GLITCH = 7.7


def draw(ctx, t):
    if t < 1.7:
        ctx.save()
        I.cam(ctx, 1.25, lerp(1250, 1500, smooth(seg(t, 0, 1.7))), 990)
        I.fondo(ctx, t, 1.0, 0.0, 1)
        for ax, tipo in ((870, "vestido"), (1140, "obrero"), (1410, "gala"), (1950, "pasajera"), (600, "senora"), (330, "traje")):
            I.asiento(ctx, ax)
            I.pasajero(ctx, ax, tipo, t)
        I.asiento(ctx, 1680)
        I.ivan(ctx, 1680, t)
        ctx.restore()
    elif t < 6.7:
        fill_screen(ctx, (0.02, 0.03, 0.03))
        I.ventanas_vaho(ctx, t, aliento=smooth(seg(t, 1.8, 3.5)))
    elif t < 7.7:
        fill_screen(ctx, (0.0, 0.0, 0.0))
    else:
        ctx.save()
        I.cam(ctx, 2.7, 1700, 900)
        I.fondo(ctx, t, 0.5, 0.0, 1, flicker=False)
        I.asiento(ctx, 1680)
        I.ivan(ctx, 1680, t, aliento=1.2)
        ctx.restore()
    marco(ctx, t, DURATION, 0.7, 0.2, 0.3)
