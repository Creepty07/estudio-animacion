"""Gradación de color final (se aplica sobre cada cuadro, antes de los subtítulos).

Da el "look" de la historia sin tocar los dibujos: desaturar, enfriar, oscurecer los bordes, grano de película y
un parpadeo leve. Cada historia decide cuánto en su propia función GRADE (ver historia.py).
"""
import random
import cairo
import numpy as np
from motor import config
from motor.primitives import vignette

_GRANO = {}


def _grano():
    """Ruido en escala de grises, un poco más grande que el cuadro para poder moverlo al azar."""
    k = (config.W, config.H)
    if k not in _GRANO:
        w, h = config.W + 200, config.H + 200
        v = np.random.default_rng(4).normal(0.5, 0.22, (h, w)).clip(0, 1)
        g = (v * 255).astype(np.uint8)
        px = np.zeros((h, w, 4), np.uint8)
        px[..., 0] = px[..., 1] = px[..., 2] = g
        px[..., 3] = 255
        _GRANO[k] = (cairo.ImageSurface.create_for_data(bytearray(px.tobytes()), cairo.FORMAT_ARGB32, w, h), px)
    return _GRANO[k][0]


def final(ctx, t, desat=0.45, frio=0.45, color_frio=(0.74, 0.90, 1.0), viñeta=0.35, grano=0.10, parpadeo=0.04):
    """desat 0..1 (1 = blanco y negro), frio 0..1 (mezcla con color_frio), viñeta extra, grano y parpadeo."""
    ctx.identity_matrix()
    ctx.reset_clip()
    W, H = config.W, config.H
    if desat > 0:
        ctx.set_operator(cairo.OPERATOR_HSL_SATURATION)
        ctx.set_source_rgb(0.5, 0.5, 0.5)
        ctx.paint_with_alpha(desat)
    if frio > 0:
        ctx.set_operator(cairo.OPERATOR_MULTIPLY)
        ctx.set_source_rgb(*color_frio)
        ctx.paint_with_alpha(frio)
    ctx.set_operator(cairo.OPERATOR_OVER)
    if viñeta > 0:
        vignette(ctx, viñeta)
    r = random.Random(int(t * 24))
    if grano > 0:
        ctx.set_operator(cairo.OPERATOR_OVERLAY)
        ctx.set_source_surface(_grano(), -r.randint(0, 200), -r.randint(0, 200))
        ctx.paint_with_alpha(grano)
        ctx.set_operator(cairo.OPERATOR_OVER)
    if parpadeo > 0:
        ctx.set_source_rgba(0, 0, 0, parpadeo * r.random() ** 2)
        ctx.paint()
