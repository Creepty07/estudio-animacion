"""Parte 2, escena 1 — Gancho: un pasajero baja del camión a la orilla de la carretera; al lado, una cruz con flores."""
from motor.config import W, H
from motor.primitives import seg, smooth, lerp
from historias.ruta0.dibujo import exterior, camion, interior as I
from historias.ruta0.dibujo.comun import lluvia, niebla, marco

DURATION = 5.0
SUBS = [(0.6, 4.1, "En este camión, cada pasajero se baja donde murió.", None)]
SUSTO = 0.1


def draw(ctx, t):
    exterior.curva(ctx, t, 1.0, foto=False)
    camion.camion_lado(ctx, 180, 1190, 0.95, t, zero=1.0, puertas=1.0, faros=0.0)
    k = smooth(seg(t, 0.6, 2.6))
    I.de_pie(ctx, lerp(330, 520, k), 1190, 0.95, "obrero", alpha=smooth(seg(t, 0.5, 1.4)))
    niebla(ctx, t, 0.14)
    lluvia(ctx, t, 150, 0.2)
    marco(ctx, t, DURATION, 0.75, 0.0, 0.25)
