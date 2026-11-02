"""Escena 9 — Plano abierto: Don Celso, diminuto, y en la otra orilla los perros que apedreó, mirándolo."""
from motor.config import W, H, ACENTO
from motor.primitives import seg, smooth, lerp, camera, darken, vignette
from historias.rio_perros.dibujo import rio, celso as C, ojos

DURATION = 6.0
SUBS = [
    (0.4, 3.1, "Del otro lado, los perros que apedreó lo miraban.", None),
    (3.4, 5.4, "Ninguno cruzó.", None),
]
LADRIDO_LEJOS = 5.2        # a lo lejos ladra otro perro (anuncia la escena siguiente)
# (x, y, escala, separación, instante en que abre los ojos)
PARES = ((120, 706, 0.42, 36, 0.9), (330, 700, 0.55, 46, 1.3), (520, 710, 0.45, 38, 1.7), (690, 702, 0.58, 48, 1.1),
         (860, 708, 0.48, 40, 2.1), (990, 704, 0.40, 34, 1.5), (440, 722, 0.36, 30, 2.4))


def draw(ctx, t):
    ctx.save()
    camera(ctx, lerp(1.0, 1.05, smooth(seg(t, 0, DURATION))), W * 0.30, H * 0.55)
    rio.fondo(ctx, t)
    for x, y, s, sep, t0 in PARES:
        parpadeo = 1.0 if (int((t + x) * 1.3) % 7) else 0.15
        ojos.par(ctx, x, y, s, smooth(seg(t, t0, t0 + 0.5)), parpadeo, ACENTO, sep)
    rio.orilla(ctx, t)
    C.celso(ctx, 230, rio.ORILLA_Y + 28, 0.95, dir=1, brazo_der=0.1, brazo_izq=-0.1, cabeza_baja=0.35, t=t, sombra=0.3)
    ctx.restore()
    rio.niebla_baja(ctx, t, 1.3)
    vignette(ctx, 0.66)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.4)))
    darken(ctx, smooth(seg(t, DURATION - 0.4, DURATION)))
