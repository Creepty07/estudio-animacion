"""Parte 3, escena 9 — En su bolsillo seguía el boleto. En el vidrio de una tienda, su reflejo seguía sentado en el camión, entre los pasajeros.
Susto final: el reflejo lo mira. ¿Se salvó? ¿O sigue en el camión?"""
import math
from motor.config import W, H, FECHA_MANANA
from motor.primitives import seg, smooth, lerp, fill_screen, glow
from historias.ruta0.dibujo import exterior, camion, interior as I
from historias.ruta0.dibujo.comun import marco, ivan_de_pie, niebla

DURATION = 13.0
SUBS = [
    (0.3, 2.7, "En su bolsillo seguía el boleto.", None),
    (3.0, 6.5, "Y en el vidrio de una tienda, su reflejo", None),
    (6.8, 8.8, "seguía sentado en el camión.", None),
    (9.7, 12.4, "¿Se salvó? ¿O sigue en el camión?", None),
]
REFLEJO = (3.2, 8.5)      # el reflejo aparece despacio
SUSTO = 9.1               # timbre + motor que solo suena en el reflejo + golpe (la mezcla)


def draw(ctx, t):
    if t < 2.9:
        from historias.ruta0.dibujo.paleta import degradado_v
        degradado_v(ctx, 0, 0, W, H, (0.03, 0.04, 0.05), (0.08, 0.09, 0.1))
        I.boleto(ctx, 540, 820, lerp(0.8, 1.0, t / 2.9), FECHA_MANANA)
    else:
        exterior.tienda_vidrio(ctx, t)
        a = smooth(seg(t, *REFLEJO)) * (0.9 if t < SUSTO else 1.0)
        camion.reflejo_en_vidrio(ctx, 70, 560, 940, 720, t, a)
        if SUSTO <= t < SUSTO + 1.0:                                                             # el reflejo gira y mira
            k = 1 - (t - SUSTO)
            glow(ctx, 540, 900, 600, (0.95, 0.12, 0.12), 0.25 * k)
        w = smooth(seg(t, 3.0, 9.0))
        ivan_de_pie(ctx, lerp(260, 760, w), 1400, 1.25, "camina", math.sin(t * 5.0) * 0.9)
        niebla(ctx, t, 0.05)
    marco(ctx, t, DURATION, 0.7, 0.3, 0.3)
