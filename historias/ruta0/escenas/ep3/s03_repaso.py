"""Parte 3, escena 3 — Repaso: la cruz de la curva, el puente, la pasajera que le agarra la muñeca, el tablero con IVÁN y el boleto."""
from motor.config import W, H, FECHA_MANANA
from motor.primitives import seg, smooth, lerp, camera_center
from historias.ruta0.dibujo import exterior, interior as I
from historias.ruta0.dibujo.paleta import degradado_v
from historias.ruta0.dibujo.comun import lluvia, niebla, marco

DURATION = 8.0
SUBS = [
    (0.3, 4.6, "En el camión sin número, cada pasajero se bajó donde murió.", None),
    (4.9, 7.3, "Y su boleto era de mañana.", None),
]


def draw(ctx, t):
    if t < 1.6:
        ctx.save()
        camera_center(ctx, 2.2, 760, 860)
        exterior.curva(ctx, t, 1.0, True)
        ctx.restore()
    elif t < 3.2:
        ctx.save()
        camera_center(ctx, 1.3, 540, 900)
        exterior.puente(ctx, t)
        ctx.restore()
    elif t < 4.7:
        degradado_v(ctx, 0, 0, W, H, (0.03, 0.04, 0.04), (0.08, 0.09, 0.08))
        I.mano_muneca(ctx, t, 560, 860, 1.1, apretar=1.0)
    elif t < 6.2:
        ctx.save()
        I.cam(ctx, 1.7, 2380, 640)
        I.fondo(ctx, t, 0.6, 0.0, 7)
        I.tablero_ruta(ctx, 2400, 470, (1, 0, 0, 1), t)
        ctx.restore()
    else:
        degradado_v(ctx, 0, 0, W, H, (0.03, 0.035, 0.04), (0.08, 0.09, 0.08))
        I.boleto(ctx, 540, 820, 1.1, FECHA_MANANA)
    lluvia(ctx, t, 90, 0.12) if t < 3.2 else None
    marco(ctx, t, DURATION, 0.7, 0.3, 0.25)
