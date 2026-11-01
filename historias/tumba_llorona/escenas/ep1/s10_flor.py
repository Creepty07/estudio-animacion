"""Escena 10 — Tomás no corre: se acerca, y deja un cempasúchil sobre la piedra."""
import math
from motor.config import W, H, FANTASMA
from motor.primitives import seg, smooth, lerp, camera_center, vignette, darken, glow, tint
from motor.kit import particles
from historias.tumba_llorona.dibujo import fondo_tumba, tumbas, personas, flores, primer_plano

DURATION = 5.0
SUBS = [
    (0.2, 2.4, "Tomás no corrió. Le dio lástima,", None),
    (2.5, 4.9, "y dejó un cempasúchil sobre la piedra.", None),
]
CAMINA_HASTA = 2.15                  # deja de caminar
CORTE = 2.45                         # corte al primer plano de la piedra
LLEGA, SUELTA, SALE = 0.5, 1.2, 1.9  # tiempos dentro de la toma del primer plano
T_SUELTA = CORTE + SUELTA            # momento exacto en que la flor toca la piedra
TUMBA = (W * 0.62, H * 0.60, 1.0)
INICIO, FINAL = (W * 0.16, H * 0.70, 1.1), (W * 0.40, H * 0.655, 0.9)


def _toma_ancha(ctx, t):
    ctx.save()
    camera_center(ctx, lerp(1.0, 1.1, smooth(seg(t, 0, CORTE))), W / 2, H * 0.5)
    fondo_tumba.fondo(ctx, t, bokeh=0.12)
    x, y, s = TUMBA
    tumbas.tumba_sin_nombre(ctx, x, y, s, tono_frio=0.9)
    k = smooth(seg(t, 0.1, CAMINA_HASTA))
    px, py, ps = (lerp(INICIO[i], FINAL[i], k) for i in range(3))
    fase = math.sin(t * 7.0) * (1 - smooth(seg(t, CAMINA_HASTA - 0.4, CAMINA_HASTA)))
    luces = [(x, y - 300, 700, (0.55, 0.7, 1.0), 0.35)]
    personas.tomas(ctx, px, py, ps, "camina", fase, luces=luces)
    fx, fy = px + 73 * ps, py - 150 * ps
    flores.cempasuchil(ctx, fx, fy, 22 * ps, seed=5)
    glow(ctx, fx, fy, 90 * ps, (1.0, 0.55, 0.1), 0.35)
    ctx.restore()
    particles(ctx, t, (0.75, 0.88, 1.0), n=14, seed=81, rise=14, size=(1, 2.2), alpha=0.5)
    tint(ctx, (0.88, 0.94, 1.0), 0.7)
    vignette(ctx, 0.75)
    darken(ctx, 1 - smooth(seg(t, 0, 0.3)))


def _primer_plano(ctx, t):
    tt = t - CORTE
    ctx.save()
    camera_center(ctx, lerp(1.0, 1.08, smooth(seg(tt, 0, DURATION - CORTE))), W / 2, H / 2)
    primer_plano.dibujar(ctx, tt, LLEGA, SUELTA, SALE)
    ctx.restore()
    vignette(ctx, 0.75)
    darken(ctx, smooth(seg(t, DURATION - 0.25, DURATION)))


def draw(ctx, t):
    if t < CORTE:
        _toma_ancha(ctx, t)
    else:
        _primer_plano(ctx, t)
