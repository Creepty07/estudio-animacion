"""Velas: el cuerpo es estático (va en capas en caché) y la llama se anima aparte."""
import math
import random
from motor.config import LLAMA
from motor.primitives import glow, line, src, TAU


def cuerpo(ctx, x, y, s, color=(0.92, 0.88, 0.78)):
    """Vela de cera con la base en (x, y). Mide ~90*s de alto."""
    ctx.rectangle(x - 12 * s, y - 84 * s, 24 * s, 84 * s)
    src(ctx, color)
    ctx.fill()
    ctx.rectangle(x + 3 * s, y - 84 * s, 9 * s, 84 * s)
    src(ctx, (0, 0, 0), 0.18)
    ctx.fill()
    line(ctx, x, y - 84 * s, x, y - 92 * s, max(1.5, 2 * s), (0.15, 0.1, 0.05))


def llama(ctx, x, y, s, t, seed=0, intensidad=1.0, luz=150, inclinar=0.0, fuerza=0.55):
    """Llama de una vela cuya base está en (x, y). intensidad 0..1; inclinar desplaza la punta (viento)."""
    if intensidad <= 0.01:
        return
    r = random.Random(seed)
    ph = r.uniform(0, TAU)
    flick = (1 + 0.12 * math.sin(t * 13 + ph) + 0.06 * math.sin(t * 29 + ph * 2)) * (0.4 + 0.6 * intensidad)
    base_y = y - 94 * s
    ctx.save()
    ctx.translate(x, base_y)
    ctx.scale(s, s * flick)
    ctx.move_to(inclinar * 30, -34)
    ctx.curve_to(12 + inclinar * 20, -18, 10, -2, 0, 0)
    ctx.curve_to(-10, -2, -12 + inclinar * 20, -18, inclinar * 30, -34)
    ctx.restore()
    src(ctx, (1.0, 0.70, 0.18), min(1.0, intensidad * 1.3))
    ctx.fill()
    glow(ctx, x, base_y - 14 * s, luz * s * flick, LLAMA, fuerza * intensidad)


def humo(ctx, x, y, t_desde, t, s=1.0, dur=2.2):
    """Hilo de humo que sube y se desvanece después de apagarse la vela (x, y = punta de la mecha)."""
    k = (t - t_desde) / dur
    if k <= 0 or k >= 1:
        return
    n = 26
    pts = []
    for i in range(n):
        u = i / (n - 1)
        pts.append((x + math.sin(u * 7 + t * 2.2) * (6 + 38 * u) * s, y - u * 230 * s * (0.4 + 0.6 * min(1, k * 2.5))))
    for i in range(n - 1):
        u = i / (n - 1)
        a = 0.35 * (1 - u) * (1 - k)
        line(ctx, pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], 3 * s * (1 + u * 3), (0.75, 0.78, 0.85), a)
