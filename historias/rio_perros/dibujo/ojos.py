"""Ojos ámbar que brillan en la niebla: la mirada de los perros."""
import math
import cairo
from motor.config import ACENTO
from motor.primitives import src, glow, TAU, mix


def _almendra(ctx, x, y, w, h, rgb, a):
    ctx.move_to(x - w, y)
    ctx.curve_to(x - w * 0.4, y - h, x + w * 0.4, y - h, x + w, y)
    ctx.curve_to(x + w * 0.4, y + h * 0.8, x - w * 0.4, y + h * 0.8, x - w, y)
    ctx.close_path()
    src(ctx, rgb, a)
    ctx.fill()


def par(ctx, x, y, s=1.0, a=1.0, abre=1.0, color=ACENTO, separacion=46):
    """Un par de ojos. abre 0..1 los entrecierra (parpadeo o aparición)."""
    if a <= 0 or abre <= 0.02:
        return
    for sx in (-1, 1):
        ex = x + sx * separacion * 0.5 * s
        glow(ctx, ex, y, 46 * s, color, 0.55 * a)
        _almendra(ctx, ex, y, 19 * s, 11 * s * abre, color, a)
        _almendra(ctx, ex, y, 11 * s, 6 * s * abre, mix(color, (1, 1, 1), 0.55), a)
        ctx.save()
        ctx.translate(ex, y)
        ctx.scale(0.35, 0.9 * abre)
        ctx.arc(0, 0, 5.4 * s, 0, TAU)
        ctx.restore()
        src(ctx, (0.05, 0.02, 0.01), a)
        ctx.fill()
