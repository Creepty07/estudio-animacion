"""Ep2 escena 13 — Amanece en ámbar. Rafa, sentado y sano, da las gracias; la enfermera de turno, con el expediente, se queda quieta."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera_center, vignette, darken, glow, tint
from motor.kit import particles
from historias.planchada.dibujo import cuarto, personajes, objetos
from historias.planchada.dibujo.paleta import AMANECER

DURATION = 7.5
SUBS = [
    (0.3, 3.4, "«Gracias por mandar a Eulalia.»", "Rafa"),
    (3.8, 7.2, "«Aquí no trabaja nadie así.»", "Enfermera de turno"),
]
SILENCIO = (3.4, 3.8)     # silencio corto antes de la segunda línea


def draw(ctx, t):
    ctx.save()
    cuarto.cam(ctx, lerp(1.1, 1.25, smooth(seg(t, 0, DURATION))), 450, 830)
    am = smooth(seg(t, 0, 1.2)) * 0.4 + 0.6
    cuarto.cuarto(ctx, t, fluo=0.0, hora=(6, 5), segundero=None, ventana=0.5, amanecer=am, turno=None, pasillo=0.9, seed=3, luz_cuarto=1.0)
    # Rafa, sentado y sano, en la cama: la cobija y la almohada van dentro de rafa_sentado
    personajes.rafa_sentado(ctx, 280, 1055, 1.0, t, ojos="abiertos", boca="sonrisa" if t < 3.4 else "sonrisa")
    personajes.turno_de_pie(ctx, 650, 1215, 0.95, t, expediente=True, boca="asombro" if t > 3.8 else "seria", sorpresa=smooth(seg(t, 3.7, 4.2)))
    ctx.restore()
    glow(ctx, 265, 500, 900, AMANECER, 0.18)
    particles(ctx, t, (1.0, 0.85, 0.6), n=18, seed=11, rise=10, size=(1.2, 2.6), alpha=0.6)
    vignette(ctx, 0.5)
    darken(ctx, 1 - smooth(seg(t, 0, 0.35)))
    darken(ctx, smooth(seg(t, DURATION - 0.25, DURATION)))
