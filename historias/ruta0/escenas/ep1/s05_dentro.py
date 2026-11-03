"""Parte 1, escena 5 — El chofer le dio un boleto sin voltear; pasajeros muy arreglados, quietos; nadie levantó la vista. Iván se sienta."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp
from historias.ruta0.dibujo import interior as I
from historias.ruta0.dibujo.comun import marco, ivan_de_pie

DURATION = 10.0
SUBS = [
    (0.3, 4.2, "El chofer le dio un boleto sin voltear a verlo.", None),
    (4.5, 7.6, "Los pasajeros iban arreglados, como para una fiesta.", None),
    (7.9, 9.5, "Ninguno levantó la vista.", None),
]
BOLETO = 1.6              # papel que cambia de mano
SENTADO = 8.3
PASAJEROS = [(330, "traje"), (600, "senora"), (870, "vestido"), (1140, "obrero"), (1410, "gala"), (1950, "pasajera")]


def draw(ctx, t):
    k1 = smooth(seg(t, 4.2, 6.2))
    k2 = smooth(seg(t, 7.4, 8.6))
    ctx.save()
    I.cam(ctx, lerp(1.5, 1.25, k1), lerp(lerp(2330, 1550, k1), 1700, k2), lerp(1010, 990, k1))
    I.fondo(ctx, t, 1.0, 0.0, 1)
    for ax in I.ASIENTOS:
        I.asiento(ctx, ax)
    for ax, tipo in PASAJEROS:
        I.pasajero(ctx, ax, tipo, t)
    I.chofer(ctx, I.X_CHOFER, t, brazo=smooth(seg(t, 0.4, BOLETO)) * (1 - smooth(seg(t, 2.6, 3.4))))
    I.tablero_ruta(ctx, 2400, 470, (1, 1, 1, 0), t)
    if t < SENTADO:
        x = lerp(2190, 1760, smooth(seg(t, 3.4, 7.4)))
        ivan_de_pie(ctx, x, I.PISO - 4, 1.05, "pie" if t < 3.6 or t > 7.4 else "camina", math.sin(t * 7) * 0.8)
    else:
        I.ivan(ctx, 1680, t)
    ctx.restore()
    marco(ctx, t, DURATION, 0.6, 0.3, 0.25)
