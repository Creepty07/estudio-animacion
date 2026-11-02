"""Tarjeta de cierre: "¿Y a ti, quién te cruzaría?" y una caja de comentarios donde escribir el nombre del perro."""
import math
from motor import config
from motor.config import ACENTO, CEMPASUCHIL
from motor.primitives import (seg, smooth, ease_out, fill_screen, glow, font, text_center, src, rrect, circle, TAU, lerp)
from motor.kit import particles
from historias.tumba_llorona.dibujo import cielo, flores

AZUL = (0.015, 0.035, 0.065)


def _huella(ctx, x, y, s, a, rot=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(s, s)
    ctx.save()
    ctx.scale(1, 0.85)
    ctx.arc(0, 18, 26, 0, TAU)
    ctx.restore()
    src(ctx, ACENTO, a)
    ctx.fill()
    for dx, dy, r in ((-34, -10, 11), (-13, -30, 12), (13, -30, 12), (34, -10, 11)):
        circle(ctx, dx, dy, r, ACENTO, a)
    ctx.restore()


def dibujar(ctx, t, duracion):
    W, H = config.W, config.H
    fill_screen(ctx, AZUL)
    cielo.estrellas(ctx, t, 55, y_max=0.9, seed=31, brillo=0.6)
    glow(ctx, W / 2, 330, 640, (1.0, 0.55, 0.15), 0.22 * smooth(seg(t, 0.0, 0.9)))
    # flor y huellas que suben hacia la caja
    k = max(0.001, ease_out(seg(t, 0.1, 0.9)))
    ctx.save()
    ctx.translate(W / 2, 260 + 10 * math.sin(t * 1.4))
    ctx.scale(k, k)
    flores.cempasuchil(ctx, 0, 0, 110, rot=0.2, seed=9, a=smooth(seg(t, 0.1, 0.8)))
    ctx.restore()
    font(ctx, 108, config.FONT_DISPLAY)
    for i, linea in enumerate(("¿Y A TI,", "QUIÉN TE", "CRUZARÍA?")):
        a = smooth(seg(t, 0.5 + 0.25 * i, 1.0 + 0.25 * i))
        src(ctx, (1, 1, 1), a)
        text_center(ctx, linea, W / 2 + (1 - a) * 30, 500 + 118 * i, 4)
    # caja de comentario con cursor
    b = smooth(seg(t, 1.7, 2.3))
    y0 = 905
    rrect(ctx, 110, y0, W - 220, 150, 40)
    src(ctx, ACENTO, 0.14 * b)
    ctx.fill_preserve()
    ctx.set_line_width(5)
    src(ctx, ACENTO, 0.95 * b)
    ctx.stroke()
    font(ctx, 54, config.FONT, bold=True)
    src(ctx, (1, 1, 1), 0.92 * b)
    escrito = "ESCRIBE SU NOMBRE"
    n = int(len(escrito) * smooth(seg(t, 2.2, 3.4)))
    texto = escrito[:n]
    ctx.move_to(150, y0 + 94)
    ctx.show_text(texto)
    if int(t * 2.4) % 2 == 0 and b > 0.5:
        ext = ctx.text_extents(texto).x_advance
        ctx.rectangle(150 + ext + 6, y0 + 42, 5, 64)
        src(ctx, ACENTO, 1.0)
        ctx.fill()
    for i in range(3):
        a = smooth(seg(t, 1.2 + 0.3 * i, 1.7 + 0.3 * i)) * (0.55 + 0.45 * math.sin(t * 3 - i))
        _huella(ctx, W / 2 + (-70 if i % 2 else 70), 1130 + 48 * i, 0.62, 0.8 * max(0.2, a), 0.2 if i % 2 else -0.2)
    particles(ctx, t, (1.0, 0.65, 0.2), n=26, seed=41, rise=30, size=(1.5, 3.5), alpha=0.8)
