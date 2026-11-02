"""Ep2 escena 8 — Entró la enfermera de turno: se prende la luz; junto a la cama no hay nadie; la cortina se mueve."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera_center, vignette, darken
from historias.planchada.dibujo import cuarto, personajes, objetos

DURATION = 7.0
SUBS = [
    (0.2, 2.2, "Entró la enfermera de turno.", None),
    (2.4, 4.7, "«¿De blanco almidonado?»", "Enfermera de turno"),
    (4.8, 6.8, "«Aquí ya nadie viste así.»", "Enfermera de turno"),
]
ENTRA = 0.5               # prende la luz del cuarto (clic) y suenan sus pasos (normales, a diferencia de la otra)
PASOS = [0.1, 0.55, 1.0, 1.45]


def draw(ctx, t):
    luz = smooth(seg(t, ENTRA, ENTRA + 0.1))
    ctx.save()
    cuarto.cam(ctx, lerp(1.12, 1.25, smooth(seg(t, 0, DURATION))), lerp(560, 520, smooth(seg(t, 0, DURATION))), 840)
    cuarto.cuarto(ctx, t, fluo=0.25 + 0.75 * luz, hora=(3, 40), segundero=None, ventana=0.35, turno=None, pasillo=1.0, seed=3, pastilla_buro=True)
    personajes.rafa_cama(ctx, *cuarto.CABEZA, 1.0, t, ojos="cerrados", boca="cerrada", rubor=0.8, sudor=1.0)
    x = lerp(880, 650, smooth(seg(t, 0.05, 1.6)))
    personajes.turno_de_pie(ctx, x, 1215, 0.95, t, expediente=True, boca="habla" if 2.4 <= t <= 6.8 else "seria", sorpresa=smooth(seg(t, 2.2, 2.6)))
    ctx.restore()
    vignette(ctx, 0.62)
    darken(ctx, 1 - smooth(seg(t, 0, 0.2)))
    darken(ctx, smooth(seg(t, DURATION - 0.25, DURATION)))
