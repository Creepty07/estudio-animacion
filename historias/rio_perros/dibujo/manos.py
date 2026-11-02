"""Manos-sombra que salen del agua del río: las almas que no cruzaron. Siluetas oscuras, nada gráfico."""
import math
import cairo
from motor.primitives import src, line, TAU, smooth

COLOR = (0.006, 0.020, 0.030)
BORDE = (0.45, 0.75, 0.85)


def mano(ctx, x, y, s, alto, abre=0.5, t=0.0, seed=0, inclina=0.0):
    """(x, y) = donde el brazo sale del agua · alto = cuánto sube (px, ya escalado) · abre 0..1 separa los dedos."""
    if alto <= 4:
        return
    sway = math.sin(t * 1.1 + seed) * 14 * s
    tope = (x + sway + inclina * alto, y - alto)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.move_to(x, y + 6)
    ctx.curve_to(x + 8 * s, y - alto * 0.4, tope[0] - sway * 0.6, y - alto * 0.7, tope[0], tope[1])
    ctx.set_line_width(30 * s)
    src(ctx, COLOR)
    ctx.stroke_preserve()
    ctx.set_line_width(2.4)
    src(ctx, BORDE, 0.22)
    ctx.translate(-9 * s, 0)
    ctx.stroke()
    ctx.translate(9 * s, 0)
    ctx.save()
    ctx.translate(*tope)
    ctx.rotate(inclina * 0.8 + math.sin(t * 0.9 + seed) * 0.08)
    ctx.save()
    ctx.scale(1, 1.15)
    ctx.arc(0, -16 * s, 24 * s, 0, TAU)
    ctx.restore()
    src(ctx, COLOR)
    ctx.fill()
    for i in range(5):
        ang = (i - 2) * (0.22 + 0.2 * abre) + math.sin(t * 1.7 + seed + i) * 0.05
        largo = (58 - abs(i - 2) * 7 + (6 if i == 2 else 0)) * s
        bx, by = (i - 2) * 9 * s, -34 * s
        ctx.move_to(bx, by)
        ctx.line_to(bx + math.sin(ang) * largo, by - math.cos(ang) * largo)
        ctx.set_line_width(10 * s)
        src(ctx, COLOR)
        ctx.stroke()
    ctx.restore()
    for k in range(2):                                                          # anillos donde toca el agua
        u = ((t * 0.5 + k * 0.5) % 1.0)
        ctx.save()
        ctx.translate(x, y + 6)
        ctx.scale(1, 0.2)
        ctx.arc(0, 0, (26 + 70 * u) * s, 0, TAU)
        ctx.restore()
        ctx.set_line_width(2.6)
        src(ctx, (0.75, 0.9, 1.0), 0.28 * (1 - u))
        ctx.stroke()
