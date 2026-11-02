"""Ep2 escena 15 — La leyenda (versión popular). Pasillo largo de noche: la silueta blanca se aleja entre las puertas; cada puerta se ilumina al pasar ella."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera, vignette, darken
from historias.planchada.dibujo import pasillo

DURATION = 9.5
SUBS = [
    (0.3, 3.3, "Se cuenta que Eulalia descuidó a sus pacientes", None),
    (3.4, 5.6, "por un amor que la engañó.", None),
    (5.9, 9.2, "Desde entonces, vuelve de noche a cuidarlos.", None),
]
Z0, Z1 = 0.04, 0.90


def _z(t):
    return lerp(Z0, Z1, smooth(seg(t, 0.2, DURATION - 0.6)))


def draw(ctx, t):
    z = _z(t)
    puertas = []
    for i in range(pasillo.N_PUERTAS):
        zi = 0.06 + i * 0.15 + 0.035
        d = abs(z - zi)
        puertas.append(max(0.0, 1 - d / 0.13) if z >= zi - 0.12 else 0.0)
    luces = [0.30 + 0.05 * math.sin(t * 1.3 + i) for i in range(7)]
    ctx.save()
    camera(ctx, lerp(1.0, 1.08, smooth(seg(t, 0, DURATION))), W / 2, 820)
    pasillo.pasillo(ctx, t, luces=luces, figura=(z, smooth(seg(t, 0.0, 0.5)) * (1 - smooth(seg(t, DURATION - 0.8, DURATION - 0.2)))),
                    puertas_luz=puertas, brillo=0.9, fondo_luz=0.3)
    ctx.restore()
    vignette(ctx, 0.78)
    darken(ctx, 1 - smooth(seg(t, 0, 0.3)))
    darken(ctx, smooth(seg(t, DURATION - 0.25, DURATION)))
