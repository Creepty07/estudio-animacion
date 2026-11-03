"""Parte 1, escena 9 — ¿Dónde se baja Iván? El camión se pierde en la neblina; solo queda el "0" ámbar, que se apaga. Comenta «sigue»."""
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, fill_screen, ease_in
from historias.ruta0.dibujo import exterior, camion
from historias.ruta0.dibujo.comun import lluvia, niebla, marco

DURATION = 7.0
SUBS = [
    (0.3, 1.9, "¿Dónde se baja Iván?", None),
    (2.2, 6.1, "Comenta «sigue», y te lo cuento en la parte dos.", None),
]
APAGA = 6.2               # el "0" se apaga con un clic


def draw(ctx, t):
    exterior.escena_parada(ctx, t, luz=0.5, bruma=0.6, con_parada=False)
    x = lerp(520, 1500, ease_in(seg(t, 0.0, 4.5)))
    if t < 4.6:
        camion.camion_lado(ctx, x, exterior.SUELO + 120, lerp(1.0, 0.55, seg(t, 0, 4.5)), t, zero=1.0, faros=1.0)
    niebla(ctx, t, 0.10 + 0.5 * seg(t, 1, 4.5))
    if t >= 3.0:
        a = 1.0 if t < APAGA else 0.0
        camion.letrero_cero(ctx, 900, 760, 150, 64, a * smooth(seg(t, 3.0, 4.2)), t, 0.15)
    niebla(ctx, t, 0.2, seed=9)
    lluvia(ctx, t, 160, 0.2)
    marco(ctx, t, DURATION, 0.8, 0.2, 0.2)
