"""Paisaje de canal (estilo Xochimilco): ahuejotes, tules y agua con el reflejo de la luna."""
import math
import random
import cairo
from motor import config
from motor.config import AGUA, LUNA
from motor.primitives import line, src, circle, TAU, glow


def _ovalo(ctx, x, y, rx, ry, rgb, a=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(rx, ry)
    ctx.arc(0, 0, 1, 0, TAU)
    ctx.restore()
    src(ctx, rgb, a)
    ctx.fill()


def ahuejote(ctx, x, y, s, seed=0, color=(0.012, 0.025, 0.045)):
    """Ahuejote: árbol alto y angosto de las chinampas. (x, y) = base; mide ~520*s."""
    r = random.Random(seed)
    line(ctx, x, y, x + r.uniform(-12, 12) * s, y - 330 * s, 15 * s, color)
    for i in range(18):
        u = i / 17
        cy = y - (170 + 350 * u) * s
        w = (78 * (1 - abs(u - 0.42) * 0.95) + 10) * s
        _ovalo(ctx, x + r.uniform(-20, 20) * s, cy, w, 40 * s, color)
        for _ in range(3):                                   # ramas colgantes
            bx = x + r.uniform(-w, w) * 0.8
            line(ctx, bx, cy, bx + r.uniform(-8, 8) * s, cy + r.uniform(40, 90) * s, 3 * s, color, 0.9)


def tules(ctx, x, y, s, seed=0, n=8, color=(0.01, 0.03, 0.05)):
    """Carrizos en la orilla."""
    r = random.Random(seed)
    for _ in range(n):
        bx = x + r.uniform(-40, 40) * s
        h = r.uniform(70, 150) * s
        ctx.move_to(bx, y)
        ctx.curve_to(bx + r.uniform(-12, 12) * s, y - h * 0.5, bx + r.uniform(-25, 25) * s, y - h * 0.8, bx + r.uniform(-35, 35) * s, y - h)
        ctx.set_line_width(max(2.0, 4 * s))
        src(ctx, color)
        ctx.stroke()


def agua(ctx, y0, y1, claro=1.0):
    """Superficie del canal (sin reflejos animados)."""
    g = cairo.LinearGradient(0, y0, 0, y1)
    g.add_color_stop_rgb(0, *(c * 1.5 * claro for c in AGUA))
    g.add_color_stop_rgb(1, *(c * 0.7 * claro for c in AGUA))
    ctx.rectangle(0, y0, config.W, y1 - y0)
    ctx.set_source(g)
    ctx.fill()


def reflejo_luna(ctx, t, x, y0, y1, brillo=1.0, rgb=LUNA):
    """Camino de luna sobre el agua: franjas que tiemblan."""
    n = 14
    for i in range(n):
        u = (i + 0.5) / n
        y = y0 + (y1 - y0) * u
        w = (16 + 120 * u) * (0.55 + 0.45 * math.sin(t * 1.7 + i * 1.3))
        line(ctx, x - w / 2, y, x + w / 2, y, 4 + 3 * u, rgb, 0.30 * (1 - 0.5 * u) * brillo, cairo.LINE_CAP_ROUND)


def ondas(ctx, x, y, t0, t, n=3, rmax=170, achatado=0.22, a=0.45, rgb=(0.8, 0.9, 1.0), dur=2.2):
    """Anillos que se abren desde (x, y) a partir de t0 y se desvanecen."""
    for k in range(n):
        u = (t - t0 - k * 0.55) / dur
        if 0 < u < 1:
            ctx.save()
            ctx.translate(x, y)
            ctx.scale(1, achatado)
            ctx.arc(0, 0, rmax * math.sqrt(u), 0, TAU)
            ctx.restore()
            ctx.set_line_width(3)
            src(ctx, rgb, a * (1 - u))
            ctx.stroke()
