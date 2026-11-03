"""Parte 2, escena 3 — Repaso rápido: el letrero "0", el pasillo quieto y la mano de la pasajera en la muñeca de Iván."""
from motor.config import W, H
from motor.primitives import seg, smooth, lerp
from historias.ruta0.dibujo import exterior, camion, interior as I
from historias.ruta0.dibujo.paleta import degradado_v
from historias.ruta0.dibujo.comun import lluvia, niebla, marco

DURATION = 9.5
SUBS = [
    (0.3, 3.4, "Iván subió al último camión: uno sin número.", None),
    (3.7, 5.7, "Ninguno de sus pasajeros respira.", None),
    (6.0, 8.7, "Y una pasajera no lo dejó bajar.", None),
]


def draw(ctx, t):
    if t < 3.6:
        exterior.escena_parada(ctx, t, luz=0.6, bruma=0.4, con_parada=False)
        camion.camion_frente(ctx, 540, 1230, lerp(0.8, 1.0, t / 3.6), t, zero=1.0)
        niebla(ctx, t, 0.16)
        lluvia(ctx, t, 170, 0.24)
    elif t < 5.9:
        ctx.save()
        I.cam(ctx, 1.25, lerp(1100, 1500, smooth(seg(t, 3.6, 5.9))), 990)
        I.fondo(ctx, t, 1.0, 0.0, 2)
        for ax, tipo in ((330, "traje"), (600, "senora"), (870, "vestido"), (1140, "obrero"), (1410, "gala"), (1950, "pasajera")):
            I.asiento(ctx, ax)
            I.pasajero(ctx, ax, tipo, t)
        I.asiento(ctx, 1680)
        I.ivan(ctx, 1680, t)
        ctx.restore()
    else:
        degradado_v(ctx, 0, 0, W, H, (0.03, 0.04, 0.04), (0.08, 0.09, 0.08))
        I.mano_muneca(ctx, t, 560, 860, 1.1 + 0.02 * (t - 6.0), apretar=1.0)
    marco(ctx, t, DURATION, 0.7, 0.3, 0.25)
