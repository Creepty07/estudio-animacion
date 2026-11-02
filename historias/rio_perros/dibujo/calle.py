"""Calle de pueblo (flashback de Don Celso): adobe, teja, puerta de arco, piso de tierra y papel picado.

De día va en tonos de sepia cálida (recuerdo); de noche, azul frío con una sola ventana encendida.
El piso queda en y = SUELO; los personajes se dibujan encima con los pies entre SUELO y SUELO + 90.
"""
import math
import random
import cairo
from motor import config
from motor.config import ADOBE
from motor.primitives import src, line, glow, circle, fill_poly, TAU, mix
from motor.layers import paint_layer
from historias.tumba_llorona.dibujo import cielo

SUELO = 1170          # línea donde termina el muro y empieza el piso (para H = 1920); los pies pisan en SUELO + 65


def _tono(rgb, noche):
    if not noche:
        return rgb
    return mix(tuple(c * 0.30 for c in rgb), (0.03, 0.06, 0.14), 0.40)


def _estatico(c, noche):
    W, H = config.W, config.H
    # ---- cielo ----
    if noche:
        cielo.gradiente_vertical(c, [(0, (0.010, 0.020, 0.055)), (1, (0.060, 0.105, 0.200))], 0, SUELO)
    else:
        cielo.gradiente_vertical(c, [(0, (0.62, 0.70, 0.80)), (0.6, (0.96, 0.80, 0.60)), (1, (1.0, 0.86, 0.60))], 0, SUELO)
    # ---- loma lejana ----
    r = random.Random(11)
    pts = [(0, 700)]
    x = 0
    while x < W + 80:
        x += r.uniform(80, 150)
        pts.append((x, 640 + r.uniform(-40, 40)))
    pts += [(W + 80, 760), (0, 760)]
    fill_poly(c, pts, _tono((0.50, 0.46, 0.44), noche), 1.0)
    # ---- casa A (izquierda, baja) y casa B (derecha, alta) ----
    for x0, x1, top, col in ((-10, 530, 720, ADOBE), (530, W + 10, 610, (0.72, 0.55, 0.34))):
        c.rectangle(x0, top, x1 - x0, SUELO - top)
        src(c, _tono(col, noche))
        c.fill()
        c.rectangle(x0, top, x1 - x0, 14)                                              # sombra bajo el alero
        src(c, (0, 0, 0), 0.30)
        c.fill()
        c.rectangle(x0, SUELO - 62, x1 - x0, 62)                                       # zócalo encalado
        src(c, _tono((0.88, 0.84, 0.74), noche))
        c.fill()
        for i in range(int((x1 - x0) / 34) + 2):                                       # hilera de tejas
            circle(c, x0 + i * 34, top - 6, 22, _tono((0.55, 0.20, 0.13), noche))
        c.rectangle(x0, top - 6, x1 - x0, 26)
        src(c, _tono((0.50, 0.17, 0.11), noche))
        c.fill()
    # grietas y manchas del adobe
    r = random.Random(5)
    for _ in range(26):
        x, y = r.uniform(0, W), r.uniform(700, SUELO - 90)
        line(c, x, y, x + r.uniform(-30, 30), y + r.uniform(20, 60), 3, (0, 0, 0), 0.10 if not noche else 0.18)
    # puerta con arco (casa B)
    c.move_to(710, SUELO - 62)
    c.line_to(710, SUELO - 300)
    c.curve_to(710, SUELO - 400, 900, SUELO - 400, 900, SUELO - 300)
    c.line_to(900, SUELO - 62)
    c.close_path()
    src(c, _tono((0.20, 0.11, 0.07), noche))
    c.fill()
    for xx in (755, 805, 855):
        line(c, xx, SUELO - 70, xx, SUELO - 330, 3, (0, 0, 0), 0.35)
    # ventana con postigos (casa B, izquierda) y ventana de la casa A
    for vx, vy, encendida in ((590, 800, False), (130, 860, noche)):
        c.rectangle(vx, vy, 110, 150)
        src(c, (1.0, 0.78, 0.38) if encendida else _tono((0.10, 0.07, 0.06), noche))
        c.fill()
        c.rectangle(vx - 26, vy - 6, 26, 162)
        c.rectangle(vx + 110, vy - 6, 26, 162)
        src(c, _tono((0.25, 0.42, 0.40), noche))
        c.fill()
    # ---- piso de tierra con piedras ----
    g = cairo.LinearGradient(0, SUELO, 0, H)
    g.add_color_stop_rgb(0, *_tono((0.55, 0.40, 0.28), noche))
    g.add_color_stop_rgb(1, *_tono((0.28, 0.20, 0.15), noche))
    c.rectangle(0, SUELO, W, H - SUELO)
    c.set_source(g)
    c.fill()
    r = random.Random(8)
    for _ in range(90):
        x, y = r.uniform(0, W), r.uniform(SUELO + 20, SUELO + 420)
        c.save()
        c.translate(x, y)
        c.scale(r.uniform(14, 40), r.uniform(6, 14))
        c.arc(0, 0, 1, 0, TAU)
        c.restore()
        src(c, _tono((0.42, 0.34, 0.28), noche), 0.55)
        c.fill()


def barril(ctx, noche=False, x=968):
    """El barril donde se esconde el cachorro. Va aparte del fondo para dibujarlo DESPUÉS del perro y que lo tape."""
    ctx.rectangle(x - 56, SUELO - 20, 112, 150)
    src(ctx, _tono((0.42, 0.26, 0.15), noche))
    ctx.fill()
    ctx.rectangle(x - 56, SUELO - 20, 28, 150)
    src(ctx, (1, 1, 1), 0.07)
    ctx.fill()
    for yy in (SUELO + 18, SUELO + 92):
        ctx.rectangle(x - 58, yy, 116, 9)
        src(ctx, _tono((0.22, 0.17, 0.14), noche))
        ctx.fill()


def papel_picado(ctx, t, noche=False):
    """Banderines de papel picado cruzando la calle; se mecen con el aire."""
    W = config.W
    paleta = ((1.0, 0.55, 0.10), (0.85, 0.15, 0.50), (0.45, 0.25, 0.75), (0.15, 0.65, 0.65), (1.0, 0.85, 0.20))
    for hilo_y, sag in ((330, 70), (400, 52)):
        pts = []
        for i in range(0, W + 60, 60):
            u = i / W
            pts.append((i, hilo_y + sag * 4 * u * (1 - u)))
        ctx.move_to(*pts[0])
        for p in pts[1:]:
            ctx.line_to(*p)
        ctx.set_line_width(2.4)
        src(ctx, (0.1, 0.08, 0.07), 0.8)
        ctx.stroke()
        for i, (px, py) in enumerate(pts[:-1]):
            col = paleta[(i + int(hilo_y)) % len(paleta)]
            col = tuple(c * 0.30 for c in col) if noche else col
            sw = math.sin(t * 1.6 + i * 0.7) * 5
            ctx.save()
            ctx.translate(px + 22, py)
            ctx.rotate(math.radians(sw))
            ctx.move_to(-20, 0)
            ctx.line_to(20, 0)
            ctx.line_to(20, 56)
            ctx.line_to(10, 70)
            ctx.line_to(0, 56)
            ctx.line_to(-10, 70)
            ctx.line_to(-20, 56)
            ctx.close_path()
            src(ctx, col, 0.92)
            ctx.fill()
            for dx in (-10, 0, 10):                                                   # calados
                circle(ctx, dx, 22, 3.2, (0, 0, 0), 0.30)
            ctx.restore()


def fondo(ctx, t, noche=False):
    paint_layer(ctx, ("calle", noche), lambda c: _estatico(c, noche))
    if noche:
        cielo.estrellas(ctx, t, 50, y_max=0.30, seed=9, brillo=0.8)
        cielo.luna(ctx, config.W * 0.78, 250, 52, 0.95)
        glow(ctx, 185, 935, 330, (1.0, 0.68, 0.30), 0.32)                              # ventana encendida
    papel_picado(ctx, t, noche)
