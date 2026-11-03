"""Parte 2, escena 8 — En el boleto había una fecha; corte al celular (fecha de hoy); era la de mañana. Susto principal de la parte 2."""
from motor.config import W, H, FECHA_HOY, FECHA_MANANA
from motor.primitives import seg, smooth, lerp
from historias.ruta0.dibujo import interior as I
from historias.ruta0.dibujo.paleta import degradado_v
from historias.ruta0.dibujo.comun import marco

DURATION = 6.0
SUBS = [
    (0.3, 2.7, "En el boleto había una fecha.", None),
    (3.6, 5.2, "Era la de mañana.", None),
]
SILENCIO = (2.9, 3.4)
SUSTO = 3.4               # golpe + tinnitus: el boleto tiembla con la fecha de mañana


def draw(ctx, t):
    degradado_v(ctx, 0, 0, W, H, (0.03, 0.035, 0.04), (0.08, 0.09, 0.08))
    if t < 2.9:
        I.boleto(ctx, 540, 820, 1.1 + 0.03 * t, FECHA_MANANA)
    elif t < 3.4:
        I.celular(ctx, 540, 830, 0.95, t, FECHA_HOY, "HOY", 1.0)
    else:
        I.boleto(ctx, 540, 820, 1.15, FECHA_MANANA, glitch=max(0.25, 1 - (t - 3.4) / 1.2), t=t)
    marco(ctx, t, DURATION, 0.7, 0.3, 0.3)
