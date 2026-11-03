"""Parte 1, escena 3 — Iván perdió el último camión; bajo la lluvia esperó y no pasó ninguno."""
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, vignette, darken
from historias.ruta0.dibujo import exterior, camion
from historias.ruta0.dibujo.comun import lluvia, niebla, marco, ivan_de_pie

DURATION = 7.5
SUBS = [
    (0.3, 3.4, "Iván perdió el último camión de la noche.", None),
    (3.7, 6.8, "Bajo la lluvia esperó, y no pasó ninguno.", None),
]
SE_VA = (0.4, 3.6)        # las luces traseras del último camión se alejan


def draw(ctx, t):
    exterior.escena_parada(ctx, t, luz=1.0, bruma=0.2, x_parada=420)
    k = smooth(seg(t, *SE_VA))
    if k < 1:
        camion.camion_trasero(ctx, lerp(760, 640, k), lerp(1030, 860, k), lerp(0.7, 0.16, k), t, freno=1 - k)
    sentado = smooth(seg(t, 4.2, 4.8))
    ivan_de_pie(ctx, 300, exterior.SUELO + 70, 1.5, "pie", 0.0)
    niebla(ctx, t, 0.12)
    lluvia(ctx, t, 220, 0.26)
    marco(ctx, t, DURATION, 0.7, 0.4, 0.25)
