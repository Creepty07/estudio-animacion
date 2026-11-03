"""Parte 2, escena 4 — CURVA DEL AHORCADO: un señor con ropa de trabajo se baja; en la cruz con flores está su foto.
Rechinido de llantas lejano que se corta (sugerido, nunca mostrado)."""
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera_center
from historias.ruta0.dibujo import exterior, camion, interior as I
from historias.ruta0.dibujo.comun import lluvia, niebla, marco

DURATION = 11.5
SUBS = [
    (0.3, 3.8, "En la Curva del Ahorcado, un señor se bajó.", None),
    (4.1, 7.6, "Junto a la curva había una cruz con flores,", None),
    (8.4, 10.8, "y en la cruz, su foto.", None),
]
RECHINIDO = 7.5           # llantas lejanas que se cortan (la mezcla)
SUSTO = 7.9               # glitch en la foto de la cruz


def draw(ctx, t):
    k1 = smooth(seg(t, 3.8, 7.3))
    k2 = smooth(seg(t, 8.0, 10.8))
    z = lerp(lerp(1.0, 1.6, k1), 3.3, k2)
    cx = lerp(lerp(540, 700, k1), 760, k2)
    cy = lerp(lerp(900, 880, k1), 790, k2)
    ctx.save()
    camera_center(ctx, z, cx, cy)
    exterior.curva(ctx, t, 1.0, foto=True)
    exterior.letrero(ctx, 330, 1000, 1.0, "CURVA DEL AHORCADO", smooth(seg(t, 0.2, 1.0)))
    camion.camion_lado(ctx, 190, 1190, 0.95, t, zero=1.0, puertas=1.0, faros=0.0, pasajeros=True)
    I.de_pie(ctx, lerp(330, 560, smooth(seg(t, 0.6, 3.0))), 1190, 0.95, "obrero", alpha=smooth(seg(t, 0.4, 1.2)))
    ctx.restore()
    niebla(ctx, t, 0.12)
    lluvia(ctx, t, 140, 0.18)
    marco(ctx, t, DURATION, 0.75, 0.3, 0.3)
