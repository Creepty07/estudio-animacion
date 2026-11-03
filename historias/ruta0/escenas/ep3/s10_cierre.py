"""Parte 3, escena 10 — ¿Iván despertó de verdad? El "0" ámbar en la neblina parpadea y se apaga. Comenta: sí o no."""
from motor.config import W, H
from motor.primitives import seg, smooth, fill_screen
from historias.ruta0.dibujo import exterior, camion
from historias.ruta0.dibujo.comun import lluvia, niebla, marco

DURATION = 6.0
SUBS = [
    (0.3, 1.9, "¿Iván despertó de verdad?", None),
    (2.2, 3.8, "Comenta: sí o no.", None),
]
APAGA = 4.6               # clic final


def draw(ctx, t):
    exterior.escena_parada(ctx, t, luz=0.3, bruma=0.8, con_parada=False)
    a = 1.0 if t < APAGA else 0.0
    camion.letrero_cero(ctx, 540, 760, 190, 80, a * smooth(seg(t, 0.0, 0.8)), t, 0.25 if t > 3.0 else 0.0)
    niebla(ctx, t, 0.25, seed=12)
    lluvia(ctx, t, 150, 0.2)
    marco(ctx, t, DURATION, 0.85, 0.3, 0.25)
