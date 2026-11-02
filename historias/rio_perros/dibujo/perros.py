"""Perros de lado, planos y con luz de contorno. Un mismo dibujo sirve para el rojizo, el blanco, el negro y los callejeros.

Convención: el perro mira a la derecha (dir=1) o a la izquierda (dir=-1); (x, y) es el piso bajo el pecho y
s la escala (a s=1 mide ~150 de alto y ~190 de largo).
"""
import math
import cairo
from motor.primitives import src, glow, circle, line, TAU, mix, lerp


def _ovalo(ctx, x, y, rx, ry, rgb, a=1.0, rot=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(rx, ry)
    ctx.arc(0, 0, 1, 0, TAU)
    ctx.restore()
    src(ctx, rgb, a)
    ctx.fill()


def _pata(ctx, cadera, rodilla, pata, ancho, rgb):
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_line_width(ancho)
    src(ctx, rgb)
    ctx.move_to(*cadera)
    ctx.line_to(*rodilla)
    ctx.line_to(*pata)
    ctx.stroke()
    _ovalo(ctx, pata[0] + 5, pata[1] - 1, ancho * 0.75, ancho * 0.42, rgb)


def _torso(ctx):
    ctx.move_to(-86, -94)
    ctx.curve_to(-92, -124, -40, -128, 0, -124)
    ctx.curve_to(46, -126, 82, -120, 90, -100)
    ctx.curve_to(94, -72, 62, -55, 22, -58)
    ctx.curve_to(-28, -52, -82, -60, -86, -94)
    ctx.close_path()


def perro(ctx, x, y, s, pelo, dir=1, t=0.0, paso=0.0, cabeza=0.0, ojos=None, orejas=1.0,
          flaco=0.0, hilo=None, rim=(0.55, 0.72, 1.0), cola=0.0, brillo_ojos=0.9):
    """paso = ciclos de marcha por segundo (0 = quieto) · cabeza: -1 olfatea el piso … +1 levanta el hocico ·
    ojos = color del brillo de los ojos (None = sin brillo) · flaco 0..1 marca las costillas · hilo = color del hilo al cuello."""
    sombra = tuple(c * 0.60 for c in pelo)
    fase = t * paso * TAU
    mov = 1.0 if paso else 0.0
    ctx.save()
    ctx.translate(x, y + (math.sin(fase * 2) * 3 * s if paso else 0))
    ctx.scale(dir * s, s)

    # ---- patas lejanas ----
    def p(cx, off, delantera):
        sw = math.sin(fase + off) * 24 * mov
        lev = max(0.0, math.cos(fase + off)) * 15 * mov
        kx = cx + sw * 0.5 + (10 if delantera else -12)
        return (cx, -72), (kx, -38 - lev * 0.4), (cx + sw, -4 - lev)

    _pata(ctx, *p(-60, math.pi, False), 17, sombra)
    _pata(ctx, *p(48, 0, True), 17, sombra)

    # ---- cola ----
    wag = math.sin(t * 9) * (14 + 14 * cola) * (0.3 + cola)
    ctx.save()
    ctx.move_to(-84, -104)
    ctx.curve_to(-120, -118 - 14 * cola, -132 + wag, -150 - 18 * cola, -138 + wag, -168 - 14 * cola)
    ctx.set_line_width(11)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    src(ctx, pelo)
    ctx.stroke()
    ctx.restore()

    # ---- torso ----
    ctx.save()
    g = cairo.LinearGradient(0, -128, 0, -54)
    g.add_color_stop_rgb(0, *mix(pelo, rim, 0.38))
    g.add_color_stop_rgb(0.35, *pelo)
    g.add_color_stop_rgb(1, *sombra)
    _torso(ctx)
    ctx.set_source(g)
    ctx.fill()
    if flaco > 0:
        for i, cx in enumerate((-8, 14, 36)):
            ctx.move_to(cx, -112)
            ctx.curve_to(cx + 8, -98, cx + 8, -84, cx, -72)
            ctx.set_line_width(3.2)
            src(ctx, (0, 0, 0), 0.26 * flaco)
            ctx.stroke()

    # ---- cuello y cabeza ----
    c = cabeza
    hx = 102 + (30 * -c if c < 0 else 6 * c)
    hy = -150 - 70 * c if c < 0 else -150 - 26 * c
    ctx.move_to(54, -126)
    ctx.line_to(90, -102)
    ctx.line_to(hx + 2, hy + 24)
    ctx.line_to(hx - 22, hy - 12)
    ctx.close_path()
    src(ctx, pelo)
    ctx.fill()
    if hilo:
        ctx.move_to(60, -112)
        ctx.curve_to(74, -98, 88, -96, 96, -106)
        ctx.set_line_width(3.5)
        src(ctx, hilo)
        ctx.stroke()
        ctx.move_to(78, -98)
        ctx.curve_to(80, -84, 78, -74, 84, -66)
        ctx.set_line_width(2.6)
        ctx.stroke()
    ctx.save()
    ctx.translate(hx, hy)
    ctx.rotate(-0.30 * c if c < 0 else -0.35 * c)
    for dx, col, ang in ((-6, sombra, -0.10), (8, pelo, 0.0)):                       # orejas: la lejana, la cercana
        ctx.move_to(dx - 10, -18)
        ctx.line_to(dx - 24 - 6 * ang * 10, -18 - 62 * orejas)
        ctx.line_to(dx + 12, -22)
        ctx.close_path()
        src(ctx, col)
        ctx.fill()
    _ovalo(ctx, 0, 0, 31, 26, mix(pelo, rim, 0.05))
    _ovalo(ctx, 38, 7, 31, 14.5, pelo)
    _ovalo(ctx, 66, 3, 7, 5.5, (0.03, 0.03, 0.04))
    line(ctx, 30, 14, 62, 14, 2.2, (0, 0, 0), 0.35)
    ctx.restore()
    ctx.restore()                                                                       # fin torso y cabeza

    # ---- patas cercanas ----
    _pata(ctx, *p(-60, 0, False), 18, pelo)
    _pata(ctx, *p(48, math.pi, True), 18, pelo)
    ctx.restore()

    # ---- ojos brillantes (sin pasar por el escalado: se ubican en pantalla) ----
    if ojos is not None:
        ang = -0.30 * c if c < 0 else -0.35 * c
        ex, ey = 15, -6
        lx = hx + ex * math.cos(ang) - ey * math.sin(ang)
        ly = hy + ex * math.sin(ang) + ey * math.cos(ang)
        gx, gy = x + dir * lx * s, y + ly * s
        glow(ctx, gx, gy, 20 * s, ojos, 0.9 * brillo_ojos)
        circle(ctx, gx, gy, 3.6 * s, mix(ojos, (1, 1, 1), 0.5), brillo_ojos)


def perro_nadando(ctx, x, y, s, pelo, t, dir=1, hilo=None, rim=(0.55, 0.72, 1.0), ondas=True):
    """Solo cabeza, cuello y lomo sobre el agua, con ondas que se abren. (x, y) = línea del agua bajo el pecho."""
    sombra = tuple(c * 0.6 for c in pelo)
    bob = math.sin(t * 5.5) * 3 * s
    ctx.save()
    ctx.translate(x, y + bob)
    ctx.scale(dir * s, s)
    ctx.move_to(-70, 4)
    ctx.curve_to(-72, -34, -30, -52, 10, -50)
    ctx.curve_to(50, -50, 78, -46, 84, -20)
    ctx.curve_to(80, 4, 40, 10, 0, 10)
    ctx.close_path()
    g = cairo.LinearGradient(0, -52, 0, 10)
    g.add_color_stop_rgb(0, *mix(pelo, rim, 0.35))
    g.add_color_stop_rgb(0.4, *pelo)
    g.add_color_stop_rgb(1, *sombra)
    ctx.set_source(g)
    ctx.fill()
    ctx.move_to(60, -44)                                                      # cuello
    ctx.line_to(86, -18)
    ctx.line_to(112, -64)
    ctx.line_to(84, -92)
    ctx.close_path()
    src(ctx, pelo)
    ctx.fill()
    if hilo:
        ctx.move_to(70, -40)
        ctx.curve_to(82, -30, 96, -34, 104, -52)
        ctx.set_line_width(3.2)
        src(ctx, hilo)
        ctx.stroke()
    ctx.save()
    ctx.translate(106, -82)
    ctx.rotate(-0.2)
    for dx, col in ((-6, sombra), (8, pelo)):
        ctx.move_to(dx - 10, -18)
        ctx.line_to(dx - 24, -18 - 56)
        ctx.line_to(dx + 12, -22)
        ctx.close_path()
        src(ctx, col)
        ctx.fill()
    _ovalo(ctx, 0, 0, 31, 26, mix(pelo, rim, 0.05))
    _ovalo(ctx, 38, 7, 31, 14.5, pelo)
    _ovalo(ctx, 66, 3, 7, 5.5, (0.03, 0.03, 0.04))
    ctx.restore()
    ctx.restore()
    if ondas:
        for i in range(3):
            k = ((t * 0.55 + i / 3) % 1.0)
            ctx.save()
            ctx.translate(x, y + 8 * s)
            ctx.scale(1, 0.18)
            ctx.arc(0, 0, (60 + 150 * k) * s, 0, TAU)
            ctx.restore()
            ctx.set_line_width(3)
            src(ctx, (0.75, 0.88, 0.95), 0.32 * (1 - k))
            ctx.stroke()
