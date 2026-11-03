"""Parte 1, escena 4 — Hasta que, entre la neblina, apareció otro: viejo, sin número, con el "0" ámbar. Iván subió."""
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, ease_out
from historias.ruta0.dibujo import exterior, camion
from historias.ruta0.dibujo.comun import lluvia, niebla, marco, ivan_de_pie

DURATION = 8.5
SUBS = [
    (0.3, 3.0, "Hasta que, entre la neblina, apareció otro.", None),
    (3.3, 6.4, "No traía número. Su letrero solo decía: cero.", None),
    (6.7, 7.9, "Iván subió.", None),
]
PUERTAS = 5.0             # se abren las puertas neumáticas (la mezcla)
FRENA = 4.2               # llega y frena
SUBE = (6.8, 7.9)         # Iván entra por la puerta


def draw(ctx, t):
    exterior.escena_parada(ctx, t, luz=0.9, bruma=0.35, x_parada=760)
    x = lerp(-620, 452, ease_out(seg(t, 0.4, FRENA + 0.3)))
    camion.camion_lado(ctx, x, exterior.SUELO + 120, 1.0, t, zero=1.0, puertas=seg(t, PUERTAS, PUERTAS + 0.6), faros=1.0, zero_parpadeo=0.5 * (1 - seg(t, 2, 4)))
    sube = seg(t, *SUBE)
    ivan_de_pie(ctx, lerp(640, 700, 0.5) + 60 * sube, exterior.SUELO + 80, 1.35, "pie", 0.0, alpha=1 - smooth(seg(t, 7.4, 7.9)))
    niebla(ctx, t, 0.22 * (1 - 0.6 * seg(t, 3, 6)))
    lluvia(ctx, t, 200, 0.26)
    marco(ctx, t, DURATION, 0.7, 0.3, 0.25)
