"""Piezas visuales genéricas reutilizables en cualquier historia y formato.

Todo se calcula a partir de config.W / config.H, así funciona en vertical y horizontal.
"""
import math
import random
import cairo
from motor import config
from motor.primitives import (
    seg, smooth, font, text_w, text_at, src, glow, fill_screen, line, circle, TAU,
)


def glitch_text(ctx, s, cx, y, size, a, chaos, c1=(1, 0, 0), c2=(0, 1, 1), spacing=4, family=None):
    """Texto con aberración cromática: c1 + c2 suman blanco donde coinciden. chaos 0..1."""
    if a <= 0:
        return
    font(ctx, size, family or config.FONT_DISPLAY)
    x = cx - text_w(ctx, s, spacing) / 2
    off = 3 + 24 * chaos
    ctx.save()
    ctx.set_operator(cairo.OPERATOR_ADD)
    src(ctx, c1, a)
    text_at(ctx, s, x - off, y, spacing)
    src(ctx, c2, a)
    text_at(ctx, s, x + off, y, spacing)
    ctx.restore()


def fit_size(ctx, s, max_w, size, family=None, spacing=4):
    """Reduce el tamaño de letra hasta que el texto quepa en max_w."""
    while size > 20:
        font(ctx, size, family or config.FONT_DISPLAY)
        if text_w(ctx, s, spacing) <= max_w:
            return size
        size -= 4
    return size


def title_card(ctx, t, title_lines, kicker="", accent=(1.0, 0.16, 0.13), bg=(0.02, 0.015, 0.025), glitch=True):
    """Tarjeta de título centrada: kicker pequeño + 1-3 líneas grandes, con entrada tipo falla."""
    W, H = config.W, config.H
    fill_screen(ctx, bg)
    glow(ctx, W / 2, H * 0.55, max(W, H) * 0.6, tuple(c * 0.5 for c in accent), 0.45, cairo.OPERATOR_SCREEN)
    ka = smooth(seg(t, 0.1, 0.5))
    if kicker:
        font(ctx, int(W * 0.022), config.FONT, bold=True)
        src(ctx, (0.8, 0.78, 0.8), ka)
        tw = text_w(ctx, kicker, 8)
        text_at(ctx, kicker, (W - tw) / 2, H * 0.36, 8)
    appear = seg(t, 0.4, 0.5)
    chaos = (1 - smooth(seg(t, 0.45, 1.4))) if glitch else 0.0
    size = int(W * 0.075) if W > H else int(W * 0.12)
    n = len(title_lines)
    for i, ln in enumerate(title_lines):
        sz = fit_size(ctx, ln, W * 0.88, size)
        y = H * 0.36 + sz * 1.25 * (i + 1)
        glitch_text(ctx, ln, W / 2, y, sz, appear, chaos)
    k = smooth(seg(t, 1.6, 2.2))
    if k > 0:
        y = H * 0.36 + size * 1.25 * n + size * 0.55
        line(ctx, W / 2 - W * 0.2 * k, y, W / 2 + W * 0.2 * k, y, 4, accent, 1.0, cairo.LINE_CAP_BUTT)


# ---------- atmósfera ----------
def fog(ctx, t, rgb=(0.8, 0.85, 0.95), alpha=0.18, y0=None, y1=None, seed=1, speed=20):
    """Bancos de niebla que se desplazan lento (círculos difusos)."""
    W, H = config.W, config.H
    y0 = H * 0.6 if y0 is None else y0
    y1 = H if y1 is None else y1
    r = random.Random(seed)
    for _ in range(14):
        x = (r.uniform(0, W * 1.4) + t * speed * r.uniform(0.5, 1.5)) % (W * 1.4) - W * 0.2
        y = r.uniform(y0, y1)
        glow(ctx, x, y, r.uniform(W * 0.15, W * 0.35), rgb, alpha * r.uniform(0.5, 1.0), cairo.OPERATOR_SCREEN)


def particles(ctx, t, rgb=(1.0, 0.75, 0.35), n=40, seed=2, rise=40, size=(1.5, 4), alpha=0.8):
    """Partículas que suben y titilan (chispas, polvo, pétalos de cempasúchil...)."""
    W, H = config.W, config.H
    r = random.Random(seed)
    for _ in range(n):
        x0 = r.uniform(0, W)
        y0 = r.uniform(0, H)
        ph = r.uniform(0, TAU)
        y = (y0 - t * rise * r.uniform(0.5, 1.5)) % H
        x = x0 + math.sin(t * 0.8 + ph) * 20
        a = alpha * (0.5 + 0.5 * math.sin(t * 3 + ph))
        circle(ctx, x, y, r.uniform(*size), rgb, a)
        glow(ctx, x, y, 14, rgb, 0.4 * a)


def rain(ctx, t, n=160, alpha=0.25, seed=3, angle=0.18, speed=1600):
    W, H = config.W, config.H
    r = random.Random(seed)
    for _ in range(n):
        x0 = r.uniform(-200, W + 200)
        y = (r.uniform(0, H) + t * speed * r.uniform(0.8, 1.2)) % (H + 100) - 50
        x = x0 + (y * angle)
        line(ctx, x, y, x + 40 * angle, y + 40, 2, (0.8, 0.85, 1.0), alpha)


def candle(ctx, x, y, s, t, seed=0):
    """Vela con flama que titila (útil para Día de Muertos)."""
    r = random.Random(seed)
    ph = r.uniform(0, TAU)
    flick = 1 + 0.12 * math.sin(t * 13 + ph) + 0.06 * math.sin(t * 29 + ph * 2)
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.rectangle(-14, -90, 28, 90)
    src(ctx, (0.95, 0.92, 0.82))
    ctx.fill()
    line(ctx, 0, -90, 0, -100, 2, (0.15, 0.1, 0.05))
    ctx.save()
    ctx.translate(0, -104)
    ctx.scale(1, flick)
    ctx.move_to(0, -34)
    ctx.curve_to(12, -18, 10, -2, 0, 0)
    ctx.curve_to(-10, -2, -12, -18, 0, -34)
    src(ctx, (1.0, 0.75, 0.25))
    ctx.fill()
    ctx.restore()
    ctx.restore()
    glow(ctx, x, y - 120 * s, 160 * s * flick, (1.0, 0.6, 0.2), 0.55)
