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


def glitch(surface, k, seed=0):
    """Falla digital en un susto: separa los canales rojo y azul y desplaza franjas horizontales. k 0..1."""
    if k <= 0.02:
        return
    surface.flush()
    h, w, stride = surface.get_height(), surface.get_width(), surface.get_stride()
    a = np.ndarray((h, stride // 4, 4), dtype=np.uint8, buffer=surface.get_data())
    r = np.random.default_rng(seed)
    d = int(4 + 14 * k)
    a[:, :, 2] = np.roll(a[:, :, 2], d, axis=1)           # rojo a la derecha
    a[:, :, 0] = np.roll(a[:, :, 0], -d, axis=1)          # azul a la izquierda
    for _ in range(int(2 + 9 * k)):
        y0, hh = int(r.integers(0, h - 90)), int(r.integers(8, 90))
        a[y0:y0 + hh] = np.roll(a[y0:y0 + hh], int(r.integers(-90, 90) * k), axis=1)
    surface.mark_dirty()


def rojo(ctx, k):
    """Destello rojo oscuro en los bordes (sangre, alarma) con intensidad k 0..1."""
    if k <= 0.01:
        return
    W, H = config.W, config.H
    ctx.identity_matrix()
    g = cairo.RadialGradient(W / 2, H / 2, H * 0.2, W / 2, H / 2, H * 0.7)
    g.add_color_stop_rgba(0, 0.4, 0, 0, 0)
    g.add_color_stop_rgba(1, 0.55, 0.02, 0.03, 0.55 * k)
    ctx.set_source(g)
    ctx.paint()
