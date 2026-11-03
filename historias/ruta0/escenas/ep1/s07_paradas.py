"""Parte 1, escena 7 — Pasaban paradas que Iván nunca había visto; calles que no eran de su ciudad. Tocó el timbre."""
import math
import cairo
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, fill_screen, glow
from historias.ruta0.dibujo import interior as I, exterior
from historias.ruta0.dibujo.paleta import ovalo, degradado_v
from historias.ruta0.dibujo.comun import marco, lluvia

DURATION = 9.0
SUBS = [
    (0.3, 3.0, "Pasaban paradas que Iván nunca había visto.", None),
    (3.3, 6.0, "Calles que no eran de su ciudad.", None),
    (6.3, 8.3, "Tocó el timbre para bajarse.", None),
]
TIMBRE = 7.0              # timbre de parada (la mezcla)


def _ventana(ctx, t):
    ctx.save()
    ctx.rectangle(60, 330, 960, 980)
    ctx.clip()
    degradado_v(ctx, 60, 330, 960, 980, (0.005, 0.012, 0.025), (0.04, 0.08, 0.11))
    for k in range(4):                                                                                  # paradas y casas ajenas que pasan
        x = 1200 - ((t * 330 + k * 420) % 1900)
        ctx.save()
        ctx.translate(x, 0)
        exterior.parada(ctx, t, 0, 1000, 1.1, 0.8, banca=(k % 2 == 0))
        ctx.restore()
        glow(ctx, x + 100, 700, 150, (0.9, 0.75, 0.4), 0.35, cairo.OPERATOR_SCREEN)
    ctx.restore()
    ctx.set_line_width(26)
    ctx.set_source_rgb(0.04, 0.045, 0.05)
    ctx.rectangle(60, 330, 960, 980)
    ctx.stroke()


def draw(ctx, t):
    fill_screen(ctx, (0.03, 0.035, 0.03))
    if t < 6.2:
        _ventana(ctx, t)
        lluvia(ctx, t, 140, 0.18)
    else:
        degradado_v(ctx, 0, 0, W, H, (0.05, 0.055, 0.05), (0.12, 0.12, 0.09))
        dedo = smooth(seg(t, 6.3, TIMBRE))
        I.boton_parada(ctx, 540, 860, 2.6, foco=smooth(seg(t, TIMBRE, TIMBRE + 0.1)), presionado=smooth(seg(t, TIMBRE - 0.1, TIMBRE)), t=t)
        ovalo(ctx, lerp(900, 600, dedo), lerp(1300, 880, dedo), 52, 120, (0.66, 0.46, 0.34), 1.0, -0.8)    # el dedo de Iván
        I.foco_parada(ctx, 540, 520, smooth(seg(t, TIMBRE, TIMBRE + 0.1)), t)
    marco(ctx, t, DURATION, 0.65, 0.3, 0.25)
