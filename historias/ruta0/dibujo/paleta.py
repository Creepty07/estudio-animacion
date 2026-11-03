"""Colores y utilidades de Ruta 0: noche de lluvia azul-negra; el letrero "0" ámbar es la única luz cálida; luz amarilla enferma por dentro."""
import math
import random
import cairo
from motor.primitives import src, TAU, mix, fill_rrect, line, circle, glow

NOCHE_ALTO = (0.008, 0.016, 0.032)
NOCHE_BAJO = (0.045, 0.085, 0.13)
ASFALTO = (0.035, 0.05, 0.07)
ACERA = (0.07, 0.09, 0.11)
AMBAR = (1.0, 0.62, 0.12)
AMBAR_CLARO = (1.0, 0.8, 0.4)
AMARILLO = (0.95, 0.84, 0.36)           # luz enferma del interior
AMARILLO_OSC = (0.42, 0.36, 0.14)
ROJO = (0.95, 0.10, 0.12)
CAMION = (0.17, 0.22, 0.24)
CAMION_OSC = (0.08, 0.11, 0.13)
HIERRO = (0.14, 0.17, 0.19)
PIEL_MUERTA = (0.70, 0.72, 0.70)
PIEL_VIVA = (0.66, 0.46, 0.34)
CABELLO = (0.04, 0.035, 0.04)
SUDADERA = (0.20, 0.30, 0.46)
JEAN = (0.09, 0.12, 0.24)
ASIENTO = (0.11, 0.14, 0.17)
ASIENTO_CLARO = (0.19, 0.23, 0.26)
BLANCO_FRIO = (0.86, 0.93, 1.0)


def ovalo(ctx, x, y, rx, ry, rgb, a=1.0, rot=0.0):
    ctx.save()
    ctx.translate(x, y)
    if rot:
        ctx.rotate(rot)
    ctx.scale(rx, ry)
    ctx.arc(0, 0, 1, 0, TAU)
    ctx.restore()
    src(ctx, rgb, a)
    ctx.fill()


def degradado_v(ctx, x, y, w, h, c0, c1, a0=1.0, a1=1.0):
    g = cairo.LinearGradient(0, y, 0, y + h)
    g.add_color_stop_rgba(0, *c0, a0)
    g.add_color_stop_rgba(1, *c1, a1)
    ctx.rectangle(x, y, w, h)
    ctx.set_source(g)
    ctx.fill()


def trazo(ctx, pts, w, rgb, a=1.0):
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_line_width(w)
    src(ctx, rgb, a)
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ctx.stroke()


def parpadeo(t, seed=0, p=0.14):
    """Brillo 0..1 de una luz que se cae a ratos (como el fluorescente de La Planchada, pero amarilla)."""
    r = random.Random(seed * 1009 + int(t * 16))
    return 0.2 + 0.45 * r.random() if r.random() < p else 1.0
