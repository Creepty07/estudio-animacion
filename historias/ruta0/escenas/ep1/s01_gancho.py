"""Parte 1, escena 1 — Gancho: en la lluvia se acercan dos faros; arriba, el letrero con un "0" ámbar. "Esa noche pasó un camión sin número."."""
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, glow, fill_screen, vignette, darken
from historias.ruta0.dibujo import exterior, camion
from historias.ruta0.dibujo.comun import lluvia, niebla, marco

DURATION = 4.0
SUBS = [(0.6, 3.3, "Esa noche pasó un camión sin número.", None)]
SUSTO = 0.1               # frenos de aire + golpe, antes de la voz


def draw(ctx, t):
    exterior.escena_parada(ctx, t, luz=0.6, bruma=0.4, con_parada=False)
    k = smooth(seg(t, 0, DURATION))
    camion.camion_frente(ctx, 540, lerp(960, 1290, k), lerp(0.30, 1.0, k ** 1.6), t, zero=1.0, faros=1.0)
    niebla(ctx, t, 0.16)
    lluvia(ctx, t, 190, 0.26)
    marco(ctx, t, DURATION, 0.75, 0.0, 0.2)
