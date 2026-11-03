"""Parte 3, escena 5 — Iván tocó el timbre; el camión frenó en una parada a oscuras; el chofer no volteó: «Al bajar, no mires atrás.»"""
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, ease_out
from historias.ruta0.dibujo import interior as I, exterior, camion
from historias.ruta0.dibujo.paleta import degradado_v
from historias.ruta0.dibujo.comun import lluvia, niebla, marco

DURATION = 10.1
SUBS = [
    (0.3, 1.9, "Iván tocó el timbre.", None),
    (2.2, 5.3, "El camión frenó en una parada a oscuras.", None),
    (5.6, 7.2, "El chofer no volteó.", None),
    (7.5, 9.9, "«Al bajar, no mires atrás.»", "Chofer"),
]
TIMBRE = 0.9              # timbre + foco rojo (la mezcla)
FRENA = 3.6               # frenos de aire y puertas (la mezcla)


def draw(ctx, t):
    if t < 2.1:
        degradado_v(ctx, 0, 0, W, H, (0.05, 0.055, 0.05), (0.12, 0.12, 0.09))
        f = smooth(seg(t, TIMBRE, TIMBRE + 0.1))
        I.boton_parada(ctx, 540, 900, 2.6, foco=f, presionado=smooth(seg(t, TIMBRE - 0.1, TIMBRE)), t=t)
        I.foco_parada(ctx, 540, 560, f, t)
    elif t < 5.5:
        exterior.escena_parada(ctx, t, luz=0.0, bruma=0.5, con_parada=False)
        x = lerp(-500, 452, ease_out(seg(t, 2.2, FRENA + 0.4)))
        camion.camion_lado(ctx, x, exterior.SUELO + 120, 1.0, t, zero=1.0, puertas=seg(t, FRENA + 0.2, FRENA + 0.9), faros=1.0)
        niebla(ctx, t, 0.2)
        lluvia(ctx, t, 150, 0.22)
    else:
        ctx.save()
        I.cam(ctx, lerp(2.0, 2.3, smooth(seg(t, 5.5, 9.9))), 2330, 900)
        I.fondo(ctx, t, 0.5, 0.0, 8)
        I.chofer(ctx, I.X_CHOFER, t)
        ctx.restore()
    marco(ctx, t, DURATION, 0.7, 0.3, 0.3)
