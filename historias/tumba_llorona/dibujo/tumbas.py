"""Cruces, lápidas y tumbas del panteón, y la tumba sin nombre."""
import math
import random
import cairo
from motor import config
from motor.config import PIEDRA, PIEDRA_OSCURA, FONT_DISPLAY
from motor.primitives import fill_rrect, fill_poly, line, src, font, text_w, text_at, TAU, mix, rrect


def _tono(rgb, br):
    return tuple(c * br for c in rgb)


def cruz(ctx, x, y, s, br=1.0):
    """Cruz de piedra con la base en (x, y); mide ~130*s."""
    col, sombra = _tono(PIEDRA, br), _tono(PIEDRA_OSCURA, br)
    fill_rrect(ctx, x - 9 * s, y - 130 * s, 18 * s, 130 * s, 3 * s, col)
    fill_rrect(ctx, x - 40 * s, y - 98 * s, 80 * s, 17 * s, 3 * s, col)
    ctx.rectangle(x + 2 * s, y - 130 * s, 7 * s, 130 * s)
    src(ctx, sombra, 0.55)
    ctx.fill()
    ctx.rectangle(x + 2 * s, y - 98 * s, 38 * s, 17 * s)
    src(ctx, sombra, 0.55)
    ctx.fill()


def _arco(ctx, x, y, w, h_recta, r):
    """Trayecto de una lápida con la parte de arriba redonda."""
    ctx.move_to(x - w / 2, y)
    ctx.line_to(x - w / 2, y - h_recta)
    ctx.arc(x, y - h_recta, r, math.pi, 2 * math.pi)
    ctx.line_to(x + w / 2, y)
    ctx.close_path()


def lapida(ctx, x, y, s, br=1.0):
    """Lápida de arco, base en (x, y); mide ~110*s."""
    col, sombra = _tono(PIEDRA, br), _tono(PIEDRA_OSCURA, br)
    g = cairo.LinearGradient(x - 40 * s, 0, x + 40 * s, 0)
    g.add_color_stop_rgb(0, *col)
    g.add_color_stop_rgb(1, *mix(col, sombra, 0.7))
    _arco(ctx, x, y, 80 * s, 70 * s, 40 * s)
    ctx.set_source(g)
    ctx.fill()
    _arco(ctx, x, y - 6 * s, 58 * s, 62 * s, 29 * s)
    ctx.set_line_width(max(1.5, 3 * s))
    src(ctx, sombra, 0.6)
    ctx.stroke()


def tumba(ctx, x, y, s, forma="cruz", br=1.0):
    """Tumba rectangular con su marcador atrás. Base frontal en (x, y)."""
    (cruz if forma == "cruz" else lapida)(ctx, x, y - 24 * s, s, br)
    fill_poly(ctx, [(x - 66 * s, y - 24 * s), (x + 66 * s, y - 24 * s), (x + 50 * s, y - 44 * s), (x - 50 * s, y - 44 * s)],
              _tono(mix(PIEDRA, PIEDRA_OSCURA, 0.25), br))
    ctx.rectangle(x - 66 * s, y - 24 * s, 132 * s, 24 * s)
    src(ctx, _tono(mix(PIEDRA, PIEDRA_OSCURA, 0.65), br))
    ctx.fill()
    line(ctx, x - 66 * s, y - 24 * s, x + 66 * s, y - 24 * s, max(1.2, 2 * s), (1, 1, 1), 0.10, cairo.LINE_CAP_BUTT)


def maleza(ctx, x, y, s, seed=0, rgb=(0.10, 0.11, 0.08), n=9):
    """Hierbas secas."""
    r = random.Random(seed)
    for _ in range(n):
        bx = x + r.uniform(-45, 45) * s
        h = r.uniform(30, 90) * s
        ctx.move_to(bx, y)
        ctx.curve_to(bx + r.uniform(-10, 10) * s, y - h * 0.5, bx + r.uniform(-30, 30) * s, y - h * 0.8, bx + r.uniform(-40, 40) * s, y - h)
        ctx.set_line_width(max(1.5, 3 * s))
        src(ctx, rgb)
        ctx.stroke()


def _grietas(ctx, x, y, s, seed):
    r = random.Random(seed)
    for _ in range(3):
        px, py = x + r.uniform(-90, 90) * s, y - r.uniform(40, 250) * s
        ctx.move_to(px, py)
        for _ in range(5):
            px += r.uniform(-18, 18) * s
            py += r.uniform(14, 34) * s
            ctx.line_to(px, py)
        ctx.set_line_width(max(1.5, 3 * s))
        src(ctx, (0.02, 0.03, 0.05), 0.85)
        ctx.stroke()


def tumba_sin_nombre(ctx, x, y, s, nombre=None, grabado=0.0, br=1.0, tono_frio=0.0, brillo_nombre=0.0):
    """La tumba sin nombre, grande, con la base en (x, y). Sin flores ni velas.

    nombre/grabado: texto que se va grabando de izquierda a derecha (0..1).
    tono_frio: 0..1 la tiñe de azul. brillo_nombre: luz tibia sobre las letras (amanecer).
    """
    col = mix(PIEDRA, (0.30, 0.38, 0.52), tono_frio)
    sombra = mix(PIEDRA_OSCURA, (0.07, 0.10, 0.18), tono_frio)
    # losa en el suelo (perspectiva)
    fill_poly(ctx, [(x - 230 * s, y), (x + 230 * s, y), (x + 170 * s, y - 70 * s), (x - 170 * s, y - 70 * s)], _tono(mix(col, sombra, 0.55), br))
    fill_poly(ctx, [(x - 230 * s, y), (x + 230 * s, y), (x + 230 * s, y + 26 * s), (x - 230 * s, y + 26 * s)], _tono(mix(col, sombra, 0.85), br))
    line(ctx, x - 230 * s, y, x + 230 * s, y, 2.5 * s, (1, 1, 1), 0.10, cairo.LINE_CAP_BUTT)
    _grietas(ctx, x, y + 6 * s, s * 0.35, 4)
    # lápida de arco, ligeramente inclinada
    ctx.save()
    ctx.translate(x, y - 56 * s)
    ctx.rotate(-0.025)
    g = cairo.LinearGradient(-150 * s, 0, 150 * s, 0)
    g.add_color_stop_rgb(0, *_tono(col, br))
    g.add_color_stop_rgb(1, *_tono(mix(col, sombra, 0.8), br))
    _arco(ctx, 0, 0, 300 * s, 250 * s, 150 * s)
    ctx.set_source(g)
    ctx.fill()
    _arco(ctx, 0, -14 * s, 232 * s, 228 * s, 116 * s)           # marco hundido
    ctx.set_line_width(5 * s)
    src(ctx, _tono(sombra, br), 0.8)
    ctx.stroke()
    _arco(ctx, 0, -10 * s, 232 * s, 228 * s, 116 * s)
    ctx.set_line_width(2 * s)
    src(ctx, (1, 1, 1), 0.07)
    ctx.stroke()
    _grietas(ctx, 0, 0, s, 7)
    for mx, my, mr in ((-120, -20, 46), (-70, -8, 30), (110, -16, 36)):   # musgo
        ctx.save()
        ctx.translate(mx * s, my * s)
        ctx.scale(mr * s, mr * 0.4 * s)
        ctx.arc(0, 0, 1, 0, TAU)
        ctx.restore()
        src(ctx, (0.05, 0.12, 0.10), 0.75)
        ctx.fill()
    if nombre and grabado > 0:
        ctx.save()
        font(ctx, 46 * s, FONT_DISPLAY)
        tw = text_w(ctx, nombre, 4 * s)
        ctx.rectangle(-tw / 2 - 12 * s, -300 * s, tw * grabado + 24 * s, 200 * s)
        ctx.clip()
        src(ctx, (1, 1, 1), 0.28)                                # borde claro abajo-derecha: relieve hundido
        text_at(ctx, nombre, -tw / 2 + 2 * s, -150 * s + 2 * s, 4 * s)
        src(ctx, (0.02, 0.03, 0.05), 0.95)
        text_at(ctx, nombre, -tw / 2, -150 * s, 4 * s)
        if brillo_nombre > 0:
            src(ctx, (1.0, 0.72, 0.40), 0.55 * brillo_nombre)
            text_at(ctx, nombre, -tw / 2 + 1.5 * s, -150 * s + 1.5 * s, 4 * s)
        ctx.restore()
    ctx.restore()
