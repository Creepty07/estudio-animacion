"""Escena 1 — Gancho sin voz: tres golpes de tambor, tres líneas de texto y dos ojos ámbar que se abren en la niebla.

El texto grande hace de subtítulo (por eso SUBS va vacío): cada línea entra con su golpe de huehuetl.
"""
import math
from motor.config import W, H, ACENTO, NIEBLA
from motor.primitives import seg, smooth, ease_out, fill_screen, glow, font, text_center, src, darken, vignette
from motor.kit import fog, fit_size
from historias.rio_perros.dibujo import ojos

DURATION = 3.9
SUBS = []
LINEAS = (("CUANDO MUERES,", 0.30), ("UN PERRO DECIDE", 1.05), ("SI CRUZAS.", 1.80))
GOLPES = tuple(a for _, a in LINEAS)     # el sonido pone un golpe de tambor en cada uno
OJOS = 2.45                              # se abren los ojos (y gruñe)


def draw(ctx, t):
    fill_screen(ctx, (0.004, 0.010, 0.022))
    glow(ctx, W / 2, H * 0.50, 760, (0.10, 0.26, 0.34), 0.28 * smooth(seg(t, 0.0, 1.2)))
    fog(ctx, t, NIEBLA, 0.16, H * 0.38, H * 0.82, seed=2)
    for i, (txt, a0) in enumerate(LINEAS):
        k = seg(t, a0, a0 + 0.10)
        if k <= 0:
            continue
        pop = 1.0 + 0.20 * (1 - ease_out(seg(t, a0, a0 + 0.28)))
        golpe = math.sin(seg(t, a0, a0 + 0.22) * math.pi) * 6 * (1 if i < 2 else 2)
        size = 150 if i == 2 else 104
        ctx.save()
        ctx.translate(W / 2 + golpe * (-1) ** i, H * 0.285 + 150 * i)
        ctx.scale(pop, pop)
        sz = fit_size(ctx, txt, W * 0.90, size)
        font(ctx, sz, "Inter Display Black")
        glow(ctx, 0, -sz * 0.35, sz * 3.0, ACENTO if i == 2 else (0.5, 0.8, 0.95), 0.12 * k)
        src(ctx, ACENTO if i == 2 else (1, 1, 1), k)
        text_center(ctx, txt, 0, 0, 4)
        ctx.restore()
    a = smooth(seg(t, OJOS, OJOS + 0.30))
    parp = 1 - 0.9 * smooth(seg(t, 3.15, 3.22)) * (1 - smooth(seg(t, 3.22, 3.32)))
    ojos.par(ctx, W / 2, H * 0.60, 3.2, a, abre=parp * smooth(seg(t, OJOS, OJOS + 0.25)))
    vignette(ctx, 0.7)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.12)))
    darken(ctx, smooth(seg(t, DURATION - 0.40, DURATION)))
