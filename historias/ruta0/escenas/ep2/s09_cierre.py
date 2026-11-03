"""Parte 2, escena 9 — ¿Se puede bajar antes de su parada? El tablero con IVÁN encendido; el camión entra a un túnel de neblina."""
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, ease_in
from historias.ruta0.dibujo import interior as I, exterior, camion
from historias.ruta0.dibujo.comun import lluvia, niebla, marco

DURATION = 6.5
SUBS = [
    (0.3, 3.0, "¿Se puede bajar antes de su parada?", None),
    (3.3, 5.7, "Comenta «sigue» para la parte final.", None),
]


def draw(ctx, t):
    if t < 3.2:
        ctx.save()
        I.cam(ctx, lerp(1.9, 1.5, smooth(seg(t, 0, 3.2))), 2380, 660)
        I.fondo(ctx, t, 0.6, 0.0, 6)
        I.chofer(ctx, I.X_CHOFER, t)
        I.tablero_ruta(ctx, 2400, 470, (1, 0, 0, 1), t)
        ctx.restore()
    else:
        exterior.escena_parada(ctx, t, luz=0.3, bruma=0.7, con_parada=False)
        k = smooth(seg(t, 3.2, 6.3))
        camion.camion_trasero(ctx, 540, lerp(1250, 900, k), lerp(1.0, 0.18, k), t)
        niebla(ctx, t, 0.2 + 0.5 * k, seed=11)
        lluvia(ctx, t, 160, 0.2)
    marco(ctx, t, DURATION, 0.8, 0.3, 0.3)
