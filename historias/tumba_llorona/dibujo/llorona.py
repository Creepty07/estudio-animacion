"""La Llorona: figura blanca con velo, sin rostro visible, que se disuelve en la niebla.

Origen = punto en el suelo bajo ella (x, y). Todo se dibuja en un grupo para poder desvanecerla con `alpha`.
"""
import math
import cairo
from motor.config import FANTASMA
from motor.primitives import glow, line, src, circle, TAU, lerp

PIEL_FANTASMA = (0.93, 0.96, 1.0)
CABELLO = (0.02, 0.03, 0.07)


def _ovalo(ctx, x, y, rx, ry, rgb, a=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(rx, ry)
    ctx.arc(0, 0, 1, 0, TAU)
    ctx.restore()
    src(ctx, rgb, a)
    ctx.fill()


def _manga(ctx, p0, p1, w0=14, w1=34, caida=22):
    """Manga larga y amplia desde el hombro p0 hasta la muñeca p1."""
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]
    L = math.hypot(dx, dy) or 1.0
    nx, ny = -dy / L, dx / L
    a = (p0[0] + nx * w0, p0[1] + ny * w0)
    b = (p0[0] - nx * w0, p0[1] - ny * w0)
    c = (p1[0] - nx * w1, p1[1] - ny * w1 + caida * 0.4)
    d = (p1[0] + nx * w1, p1[1] + ny * w1 + caida * 0.4)
    ctx.move_to(*a)
    ctx.curve_to(a[0] + dx * 0.3, a[1] + dy * 0.3 + caida * 0.2, d[0] - dx * 0.25, d[1] - dy * 0.25 + caida * 0.4, *d)
    ctx.line_to(*c)
    ctx.curve_to(c[0] - dx * 0.25, c[1] - dy * 0.25 + caida * 0.4, b[0] + dx * 0.3, b[1] + dy * 0.3 + caida * 0.2, *b)
    ctx.close_path()


def mano(ctx, x, y, ang=0.0, s=1.0, a=1.0):
    """Mano pálida con los dedos largos (ang = hacia dónde apuntan, en radianes)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(ang)
    ctx.scale(s, s)
    _ovalo(ctx, 0, 0, 15, 12, PIEL_FANTASMA, a)
    for k in range(4):
        fy = -8 + k * 5.5
        line(ctx, 8, fy, 34 - abs(k - 1.5) * 4, fy + (k - 1.5) * 2.5, 4.2, PIEL_FANTASMA, a)
    line(ctx, -2, 10, 14, 24, 4.4, PIEL_FANTASMA, a)
    ctx.restore()


def _vestido(ctx, t, ancho_bajo, alto_hombro, ondas=1.0):
    """Vestido largo que se deshace en el suelo; devuelve nada, deja el trazo relleno."""
    ctx.move_to(-48, alto_hombro)
    ctx.curve_to(-64, alto_hombro + 60, -46, alto_hombro + 110, -40, alto_hombro + 140)
    ctx.curve_to(-72, alto_hombro + 250, -ancho_bajo * 0.85, alto_hombro * 0.25, -ancho_bajo, 0)
    n = 14
    for i in range(n + 1):
        u = i / n
        x = lerp(-ancho_bajo, ancho_bajo, u)
        ctx.line_to(x, 6 * ondas * math.sin(u * 9 + t * 2.0) + 4 * ondas * math.sin(u * 17 - t * 3.1))
    ctx.curve_to(ancho_bajo * 0.85, alto_hombro * 0.25, 72, alto_hombro + 250, 40, alto_hombro + 140)
    ctx.curve_to(46, alto_hombro + 110, 64, alto_hombro + 60, 48, alto_hombro)
    ctx.close_path()
    g = cairo.LinearGradient(0, alto_hombro, 0, 4)
    g.add_color_stop_rgba(0, 0.95, 0.98, 1.0, 0.98)
    g.add_color_stop_rgba(0.55, 0.82, 0.90, 1.0, 0.88)
    g.add_color_stop_rgba(1, 0.65, 0.78, 0.95, 0.0)
    ctx.set_source(g)
    ctx.fill()


def _cabeza(ctx, t, cx, cy, de_frente, giro=0.0, inclinada=0.0):
    """Cabeza cubierta por el velo. De frente no hay rostro: solo un hueco oscuro."""
    if de_frente:
        for k in range(6):                                       # mechones largos que caen por delante de los hombros
            lado = -1 if k % 2 == 0 else 1
            sw = math.sin(t * 1.3 + k) * 10
            ox = lado * (32 + (k // 2) * 10)
            ctx.move_to(cx + ox * 0.5, cy - 10)
            ctx.curve_to(cx + ox + sw, cy + 50, cx + ox * 0.6 - sw, cy + 120, cx + ox * 1.2 + sw * 1.5, cy + 190 + k * 12)
            ctx.set_line_width(10 - (k // 2) * 2)
            src(ctx, CABELLO, 0.92)
            ctx.stroke()
    else:                                                        # de espaldas: una cortina de pelo negro por la espalda
        sw = math.sin(t * 1.1) * 6
        ctx.move_to(cx - 40, cy - 10)
        ctx.curve_to(cx - 66 + sw, cy + 120, cx - 54, cy + 230, cx - 32, cy + 300)
        ctx.curve_to(cx - 8, cy + 330, cx + 8, cy + 330, cx + 32, cy + 300)
        ctx.curve_to(cx + 54, cy + 230, cx + 66 + sw, cy + 120, cx + 40, cy - 10)
        ctx.close_path()
        src(ctx, CABELLO, 0.97)
        ctx.fill()
    ctx.save()
    ctx.translate(cx, cy + inclinada * 12)
    ctx.rotate(inclinada * 0.35)
    ctx.move_to(-46, 40)
    ctx.curve_to(-52, -30, -30, -66, 0, -68)
    ctx.curve_to(30, -66, 52, -30, 46, 40)
    ctx.curve_to(30, 62, -30, 62, -46, 40)
    ctx.close_path()
    src(ctx, (0.94, 0.97, 1.0), 0.96)
    ctx.fill_preserve()
    ctx.set_line_width(2.5)
    src(ctx, FANTASMA, 0.7)
    ctx.stroke()
    if de_frente:
        k = 1 - 0.35 * abs(giro)
        _ovalo(ctx, giro * 11, 6, 25 * k, 34, (0.012, 0.018, 0.04))
        glow(ctx, giro * 11, 6, 40, (0.5, 0.65, 1.0), 0.10)
    ctx.restore()


def de_pie(ctx, x, y, s, t, brazos=0.0, alpha=1.0, de_frente=True, giro=0.0, manos=None, aura=1.0):
    """La Llorona de pie. brazos: 0 colgando … 1 alzados. manos = {'izq': (x, y), 'der': (x, y)} (locales) fuerza la posición."""
    if alpha <= 0:
        return
    glow(ctx, x, y - 280 * s, 420 * s, (0.5, 0.65, 1.0), 0.20 * alpha * aura)
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.push_group()
    sway = math.sin(t * 1.2) * 4
    _vestido(ctx, t, 150, -440)
    for lado, clave in ((-1, "izq"), (1, "der")):
        hombro = (lado * 44, -428)
        if manos and clave in manos:
            mano_xy = manos[clave]
        else:
            mano_xy = (lerp(lado * 74, lado * 175, brazos) + sway * lado, lerp(-196, -592, brazos))
        _manga(ctx, hombro, mano_xy, 15, 36 + 10 * brazos, caida=24 * (1 - brazos) + 6)
        ctx.set_source_rgba(0.92, 0.96, 1.0, 0.94)
        ctx.fill()
    _cabeza(ctx, t, 0, -492, de_frente, giro)
    for lado, clave in ((-1, "izq"), (1, "der")):
        if manos and clave in manos:
            mx, my = manos[clave]
        else:
            mx, my = lerp(lado * 74, lado * 175, brazos) + sway * lado, lerp(-196, -592, brazos)
        mano(ctx, mx, my + 6, math.pi / 2 - lado * (0.25 + 0.9 * brazos) if not (manos and clave in manos) else 0.9, 1.0)
    ctx.pop_group_to_source()
    ctx.paint_with_alpha(alpha)
    ctx.restore()


def arrodillada(ctx, x, y, s, t, alpha=1.0, respira=1.0):
    """Arrodillada sobre la tumba, encorvada hacia adelante, con las manos sobre la piedra."""
    if alpha <= 0:
        return
    glow(ctx, x, y - 160 * s, 400 * s, (0.5, 0.65, 1.0), 0.22 * alpha)
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.push_group()
    r = 1 + 0.015 * math.sin(t * 2.4) * respira
    ctx.scale(1, r)
    ctx.move_to(-70, -250)
    ctx.curve_to(-170, -210, -250, -80, -290, 0)
    for i in range(15):
        u = i / 14
        ctx.line_to(lerp(-290, 290, u), 7 * math.sin(u * 8 + t * 1.6) + 4 * math.sin(u * 15 - t * 2.4))
    ctx.curve_to(250, -80, 170, -210, 70, -250)
    ctx.curve_to(40, -280, -40, -280, -70, -250)
    ctx.close_path()
    g = cairo.LinearGradient(0, -280, 0, 6)
    g.add_color_stop_rgba(0, 0.95, 0.98, 1.0, 0.98)
    g.add_color_stop_rgba(0.6, 0.80, 0.88, 1.0, 0.9)
    g.add_color_stop_rgba(1, 0.65, 0.78, 0.95, 0.0)
    ctx.set_source(g)
    ctx.fill()
    for lado in (-1, 1):
        _manga(ctx, (lado * 62, -236), (lado * 128, -34), 16, 34, caida=10)
        ctx.set_source_rgba(0.92, 0.96, 1.0, 0.94)
        ctx.fill()
    _cabeza(ctx, t, 0, -300, True, 0.0, inclinada=0.9)
    for lado in (-1, 1):
        mano(ctx, lado * 134, -24, math.pi / 2 - lado * 0.4, 1.1)
    ctx.pop_group_to_source()
    ctx.paint_with_alpha(alpha)
    ctx.restore()
