"""Parte 2, escena 5 — PUENTE VIEJO: baja una muchacha con vestido de fiesta; el barandal está roto y abajo corre el río. Su asiento queda vacío."""
from motor.config import W, H
from motor.primitives import seg, smooth, lerp
from historias.ruta0.dibujo import exterior, camion, interior as I
from historias.ruta0.dibujo.comun import lluvia, niebla, marco

DURATION = 8.5
SUBS = [
    (0.3, 4.2, "En el Puente Viejo bajó una muchacha vestida de fiesta.", None),
    (4.5, 6.1, "El barandal estaba roto.", None),
    (6.4, 8.0, "Su asiento quedó vacío.", None),
]


def draw(ctx, t):
    if t < 6.3:
        z = lerp(1.0, 1.7, smooth(seg(t, 4.2, 6.2)))
        from motor.primitives import camera_center
        ctx.save()
        camera_center(ctx, z, lerp(540, 540, 0), lerp(900, 880, smooth(seg(t, 4.2, 6.2))))
        exterior.puente(ctx, t)
        exterior.letrero(ctx, 250, 1030, 1.0, "PUENTE VIEJO", smooth(seg(t, 0.2, 1.0)))
        camion.camion_lado(ctx, 700, 1010, 0.8, t, zero=1.0, puertas=1.0, faros=0.0, mirando=-1)
        I.de_pie(ctx, lerp(520, 330, smooth(seg(t, 0.8, 3.8))), 1022, 0.9, "vestido", alpha=smooth(seg(t, 0.6, 1.4)))
        ctx.restore()
        niebla(ctx, t, 0.14, y0=1000)
        lluvia(ctx, t, 140, 0.2)
    else:
        ctx.save()
        I.cam(ctx, 2.3, 870, 900)
        I.fondo(ctx, t, 0.8, 0.0, 3)
        I.asiento(ctx, 870, vacio=True)
        I.asiento(ctx, 600)
        I.pasajero(ctx, 600, "senora", t)
        I.asiento(ctx, 1140)
        I.pasajero(ctx, 1140, "obrero", t, alpha=0.0)
        ctx.restore()
    marco(ctx, t, DURATION, 0.7, 0.3, 0.25)
