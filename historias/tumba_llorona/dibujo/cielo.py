"""Cielos: noche con luna y estrellas, y amanecer. Todo se calcula con config.W/H."""
import math
import random
import cairo
from motor import config
from motor.config import NOCHE_ALTO, NOCHE_BAJO, LUNA
from motor.primitives import glow, circle, TAU, mix
from motor.layers import paint_layer


def gradiente_vertical(ctx, stops, y0=0.0, y1=None):
    """Rellena de y0 a y1 con un degradado; stops = [(posición 0..1, rgb)]."""
    y1 = config.H if y1 is None else y1
    g = cairo.LinearGradient(0, y0, 0, y1)
    for pos, rgb in stops:
        g.add_color_stop_rgb(pos, *rgb)
    ctx.rectangle(0, y0, config.W, y1 - y0)
    ctx.set_source(g)
    ctx.fill()


def estrellas(ctx, t, n=80, seed=4, y_max=0.4, brillo=1.0):
    W, H = config.W, config.H
    r = random.Random(seed)
    for _ in range(n):
        x, y = r.uniform(0, W), r.uniform(0, H * y_max)
        size, ph = r.uniform(0.8, 2.4), r.uniform(0, TAU)
        a = brillo * (0.35 + 0.65 * (0.5 + 0.5 * math.sin(t * r.uniform(0.6, 2.2) + ph)))
        circle(ctx, x, y, size, (0.85, 0.9, 1.0), a)


def luna(ctx, x, y, r, brillo=1.0, rgb=LUNA):
    glow(ctx, x, y, r * 7, (0.35, 0.45, 0.7), 0.35 * brillo)
    circle(ctx, x, y, r, rgb, brillo)
    for dx, dy, rr in ((-0.3, -0.2, 0.22), (0.25, 0.1, 0.16), (-0.1, 0.35, 0.12)):
        circle(ctx, x + dx * r, y + dy * r, rr * r, (0.62, 0.7, 0.85), 0.35 * brillo)


def noche(ctx, t, horizonte=0.45, luna_xy=(0.74, 0.14), r_luna=62, n_estrellas=80, brillo_luna=1.0):
    """Cielo nocturno completo. El degradado va en una capa en caché; estrellas y luna se animan."""
    W, H = config.W, config.H
    paint_layer(ctx, ("cielo_noche", horizonte),
                lambda c: gradiente_vertical(c, [(0, NOCHE_ALTO), (1, NOCHE_BAJO)], 0, H * horizonte + 2))
    estrellas(ctx, t, n_estrellas, y_max=horizonte * 0.85)
    if luna_xy is not None:
        luna(ctx, W * luna_xy[0], H * luna_xy[1], r_luna, brillo_luna)


def amanecer(ctx, avance=1.0, horizonte=0.5):
    """Cielo de amanecer: del azul de la noche al rosa y naranja. avance 0..1."""
    H = config.H
    arriba = mix(NOCHE_ALTO, (0.25, 0.30, 0.55), avance)
    medio = mix(NOCHE_BAJO, (0.85, 0.45, 0.50), avance)
    abajo = mix(NOCHE_BAJO, (1.0, 0.72, 0.42), avance)
    gradiente_vertical(ctx, [(0, arriba), (0.6, medio), (1, abajo)], 0, H * horizonte + 2)
