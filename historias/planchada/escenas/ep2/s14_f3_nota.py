"""Ep2 escena 14 — En el expediente había una nota: «Fiebre bajó. 3:00 a. m. — E.» Letra antigua, tinta sepia; glitch en la «E.» (susto 3, leve)."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera_center, vignette, darken, glow, fill_screen, circle
from historias.planchada.dibujo import objetos
from historias.planchada.dibujo.paleta import degradado_v, ovalo, PIEL, AMANECER

DURATION = 6.5
SUBS = [
    (0.3, 3.0, "En el expediente había una nota.", None),
    (3.2, 6.2, "«Fiebre bajó. 3:00 a. m. — E.»", None),
]
SILENCIO = 3.0           # silencio previo
SUSTO = 3.2              # glitch suave + tinnitus sobre la «E.»


def draw(ctx, t):
    fill_screen(ctx, (0.04, 0.05, 0.06))
    degradado_v(ctx, 0, 0, W, H, (0.05, 0.07, 0.08), (0.14, 0.12, 0.11))
    glow(ctx, 200, 300, 900, AMANECER, 0.18)
    k = smooth(seg(t, 0, DURATION))
    ctx.save()
    camera_center(ctx, lerp(1.0, 1.10, k), 540, 840)
    ge = smooth(seg(t, SUSTO, SUSTO + 0.1)) * (1 - smooth(seg(t, SUSTO + 0.5, SUSTO + 0.8)))
    objetos.expediente(ctx, 540, 700, 1.05, t, nota_alpha=smooth(seg(t, 0.0, 0.01)) if t >= 3.0 else smooth(seg(t, 0.4, 1.2)), glitch_e=ge)
    for dx in (-290, -200):                                                              # los dedos que sostienen la hoja
        ovalo(ctx, 540 + dx, 1070, 46, 64, PIEL, 1.0, 0.2)
    ctx.restore()
    vignette(ctx, 0.6)
    darken(ctx, 1 - smooth(seg(t, 0, 0.3)))
    darken(ctx, smooth(seg(t, DURATION - 0.25, DURATION)))
