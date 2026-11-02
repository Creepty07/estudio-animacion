"""Ep2 escena 4 — La fiebre subió toda la noche. El reloj gira de 3:00 a 5:40; la pastilla en el buró, fuera de su alcance. Nadie más entró."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera_center, vignette, darken, glow
from historias.planchada.dibujo import cuarto, personajes, objetos
from historias.planchada.dibujo.paleta import fluo_brillo

DURATION = 6.0
SUBS = [
    (0.2, 2.8, "La fiebre subió toda la noche.", None),
    (3.0, 5.8, "Nadie más entró.", None),
]
MIN0, MIN1 = 180.0, 340.0        # de 3:00 a 5:40 (la mezcla acelera el tic-tac y el monitor en este tramo)


def draw(ctx, t):
    u = smooth(seg(t, 0.2, 5.4))
    m = lerp(MIN0, MIN1, u)
    ctx.save()
    cuarto.cam(ctx, lerp(1.15, 1.3, smooth(seg(t, 0, DURATION))), lerp(440, 400, smooth(seg(t, 0, DURATION))), 840)
    cuarto.cuarto(ctx, t, fluo=0.55 + 0.45 * fluo_brillo(t, 22, "parpadea"), hora=(int(m // 60), m % 60), segundero=(t * 600) % 60, ventana=0.15,
                  turno="dormida", pastilla_buro=True, seed=3)
    personajes.rafa_cama(ctx, *cuarto.CABEZA, 1.0, t, ojos="fiebre", boca="abierta", rubor=1.0, sudor=1.0, respira=3.0)
    ctx.restore()
    glow(ctx, W / 2, H * 0.45, 900, (0.9, 0.2, 0.1), 0.05 + 0.12 * u)          # la fiebre sube: calor rojizo en el cuadro
    vignette(ctx, 0.72)
    darken(ctx, 1 - smooth(seg(t, 0, 0.2)))
    darken(ctx, smooth(seg(t, DURATION - 0.25, DURATION)))
