"""Parte 2, escena 7 — Iván: «¿Por qué yo?» Ella no contesta; solo señala su boleto."""
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, fill_screen
from historias.ruta0.dibujo import interior as I
from historias.ruta0.dibujo.paleta import degradado_v
from historias.ruta0.dibujo.comun import marco
from motor.config import FECHA_MANANA

DURATION = 5.5
SUBS = [
    (0.3, 1.9, "«¿Por qué yo?»", "Iván"),
    (2.2, 4.9, "Ella no contestó. Solo señaló su boleto.", None),
]


def draw(ctx, t):
    if t < 2.1:
        ctx.save()
        I.cam(ctx, 2.6, 1740, 880)
        I.fondo(ctx, t, 0.6, 0.0, 5)
        I.asiento(ctx, 1680)
        I.ivan(ctx, 1680, t, aliento=1.2)
        I.asiento(ctx, 1950)
        I.pasajero(ctx, 1950, "pasajera", t, giro=1.0)
        ctx.restore()
    else:
        degradado_v(ctx, 0, 0, W, H, (0.03, 0.035, 0.04), (0.07, 0.08, 0.08))
        baja = smooth(seg(t, 2.4, 3.6))
        ctx.save()
        ctx.translate(0, 40 * baja)
        I.cara_pasajera(ctx, t, 540, 560, 0.95)
        ctx.restore()
        I.boleto(ctx, 540, 1090, 0.7 + 0.08 * baja, FECHA_MANANA)
    marco(ctx, t, DURATION, 0.7, 0.3, 0.25)
