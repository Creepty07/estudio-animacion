"""Tarjeta de cierre: la pregunta para los comentarios, con botones SÍ / NO."""
import math
from motor import config
from motor.config import ACENTO, CEMPASUCHIL
from motor.primitives import (seg, smooth, ease_out, fill_screen, glow, font, text_center, text_w, src, fill_rrect, rrect, window,
                              TAU, lerp)
from motor.kit import particles
from historias.tumba_llorona.dibujo import flores, cielo

AZUL = (0.03, 0.05, 0.11)


def _boton(ctx, cx, cy, texto, rgb, a, pulso=0.0):
    w, h = 300, 128
    x, y = cx - w / 2, cy - h / 2
    s = 1 + 0.03 * pulso
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(s, s)
    ctx.translate(-cx, -cy)
    rrect(ctx, x, y, w, h, 34)
    src(ctx, rgb, 0.16 * a)
    ctx.fill_preserve()
    ctx.set_line_width(5)
    src(ctx, rgb, 0.95 * a)
    ctx.stroke()
    font(ctx, 76, config.FONT_DISPLAY)
    src(ctx, (1, 1, 1), a)
    text_center(ctx, texto, cx, cy + 27, 6)
    ctx.restore()


def dibujar(ctx, t, duracion):
    W, H = config.W, config.H
    fill_screen(ctx, AZUL)
    cielo.estrellas(ctx, t, 50, y_max=0.9, seed=31, brillo=0.7)
    glow(ctx, W / 2, H * 0.27, 620, (1.0, 0.5, 0.1), 0.20 * smooth(seg(t, 0.0, 0.8)))
    a = smooth(seg(t, 0.15, 0.8))
    k = max(0.001, ease_out(seg(t, 0.1, 0.9)))
    ctx.save()
    ctx.translate(W / 2, H * 0.265 + 18 * math.sin(t * 1.4))
    ctx.rotate(0.05 * math.sin(t * 0.8))
    ctx.scale(k, k)
    flores.cempasuchil(ctx, 0, 0, 160, rot=0.2, seed=9, a=a)
    ctx.restore()
    font(ctx, 78, config.FONT_DISPLAY)
    src(ctx, (1, 1, 1), smooth(seg(t, 0.5, 1.1)))
    text_center(ctx, "¿LE HABRÍAS", W / 2, H * 0.43, 4)
    text_center(ctx, "DEJADO LA FLOR?", W / 2, H * 0.43 + 96, 4)
    b = smooth(seg(t, 1.1, 1.7))
    p = 0.5 + 0.5 * math.sin(t * 3.2)
    _boton(ctx, W / 2 - 190, H * 0.545, "SÍ", (0.45, 0.95, 0.65), b, p)
    _boton(ctx, W / 2 + 190, H * 0.545, "NO", (1.0, 0.45, 0.4), b, 1 - p)
    font(ctx, 38, config.FONT, bold=True)
    src(ctx, ACENTO, smooth(seg(t, 1.5, 2.1)))
    text_center(ctx, "COMENTA", W / 2, H * 0.545 + 138, 12)
    particles(ctx, t, (1.0, 0.65, 0.2), n=26, seed=41, rise=30, size=(1.5, 3.5), alpha=0.8)
