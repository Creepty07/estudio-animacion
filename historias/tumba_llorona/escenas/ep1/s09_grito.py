"""Escena 9 — Corte seco: la Llorona arrodillada sobre la tumba sin nombre, y su grito."""
import math
import random
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera_center, vignette, darken, fill_screen, glow, tint
from motor.kit import particles
from historias.tumba_llorona.dibujo import fondo_tumba, tumbas, llorona

DURATION = 2.7
SUBS = [
    (0.3, 2.6, "¡Ay, mis hijos!", "LLORONA"),
]
GRITO = 0.3                          # corte desde negro, destello y grito
TUMBA = (W / 2, H * 0.62, 1.3)


def draw(ctx, t):
    if t < GRITO:
        fill_screen(ctx, (0, 0, 0))
        return
    dt = t - GRITO
    r = random.Random(int(t * 30))
    sacudida = 18 * math.exp(-dt * 6)
    ctx.save()
    camera_center(ctx, lerp(1.0, 1.2, smooth(seg(t, GRITO, DURATION))), W / 2, H * 0.52,
                  r.uniform(-sacudida, sacudida), r.uniform(-sacudida, sacudida))
    fondo_tumba.fondo(ctx, t, bokeh=0.15, niebla=1.6)
    x, y, s = TUMBA
    tumbas.tumba_sin_nombre(ctx, x, y, s, tono_frio=0.9)
    alza = 1 + 0.045 * math.exp(-dt * 4)                                    # se yergue al gritar
    llorona.arrodillada(ctx, x, y + 10, 1.1 * alza, t, alpha=0.93 + 0.07 * r.random())
    glow(ctx, x, y - 220, 700, (0.5, 0.65, 1.0), 0.22)
    ctx.restore()
    particles(ctx, t, (0.75, 0.88, 1.0), n=26, seed=71, rise=24, size=(1.2, 3), alpha=0.7)
    tint(ctx, (0.85, 0.92, 1.0), 0.8)
    vignette(ctx, 0.8)
    fill_screen(ctx, (0.85, 0.92, 1.0), 0.55 * math.exp(-dt * 7))
    darken(ctx, smooth(seg(t, DURATION - 0.25, DURATION)))
