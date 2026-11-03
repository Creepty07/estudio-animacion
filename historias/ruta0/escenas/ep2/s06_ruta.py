"""Parte 2, escena 6 — Arriba del chofer brilla la ruta; las paradas que pasaron se apagan; la última se prende: IVÁN. Susto."""
from motor.config import W, H
from motor.primitives import seg, smooth, lerp
from historias.ruta0.dibujo import interior as I
from historias.ruta0.dibujo.comun import marco

DURATION = 9.5
SUBS = [
    (0.3, 2.7, "Arriba del chofer brillaba la ruta.", None),
    (3.0, 5.4, "Las paradas que pasaban se apagaban.", None),
    (6.3, 8.7, "La última tenía un nombre: Iván.", None),
]
APAGA_CURVA, APAGA_PUENTE = 3.0, 4.2
SILENCIO = (4.8, 5.7)
SUSTO = 5.7               # se prende IVÁN (la mezcla y SUSTOS)


def draw(ctx, t):
    ctx.save()
    I.cam(ctx, lerp(1.7, 2.0, smooth(seg(t, 0, DURATION))), 2380, 640)
    I.fondo(ctx, t, 0.7, 0.0, 4)
    I.asiento(ctx, 1950)
    I.chofer(ctx, I.X_CHOFER, t)
    enc = (1.0, 1.0 - smooth(seg(t, APAGA_CURVA, APAGA_CURVA + 0.4)), 1.0 - smooth(seg(t, APAGA_PUENTE, APAGA_PUENTE + 0.4)),
           1.0 if t >= SUSTO else 0.0)
    flash = 1.0 if SUSTO <= t < SUSTO + 0.6 else 0.0
    I.tablero_ruta(ctx, 2400, 470, enc, t, ivan_flash=flash)
    ctx.restore()
    marco(ctx, t, DURATION, 0.7, 0.3, 0.25)
