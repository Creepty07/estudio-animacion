"""Don Celso: señor de pueblo con sombrero de palma, bigote y ropa de manta. Personaje original.

Mira al frente (de tres cuartos); `dir` solo voltea a quién apunta el brazo que tira. (x, y) = piso bajo los pies;
s = escala (a s=1 mide ~320 de alto).
Ángulos de los brazos: 0 cuelga, 1.57 apunta al frente en horizontal, 2.6 arriba y adelante, negativo hacia atrás.
"""
import math
import cairo
from motor.config import MANTA, SOMBRERO, PIEL
from motor.primitives import src, line, circle, glow, TAU, mix


def _ovalo(ctx, x, y, rx, ry, rgb, a=1.0, rot=0.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(rx, ry)
    ctx.arc(0, 0, 1, 0, TAU)
    ctx.restore()
    src(ctx, rgb, a)
    ctx.fill()


def _brazo(ctx, hombro, ang, largo, dir, rgb, mano=None, piedra=False):
    hx = hombro[0] + dir * largo * math.sin(ang)
    hy = hombro[1] + largo * math.cos(ang)
    codo = (hombro[0] + dir * largo * 0.5 * math.sin(ang * 0.8), hombro[1] + largo * 0.5 * math.cos(ang * 0.8) + 4)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_line_width(24)
    src(ctx, rgb)
    ctx.move_to(*hombro)
    ctx.line_to(*codo)
    ctx.line_to(hx, hy)
    ctx.stroke()
    circle(ctx, hx, hy, 12, mano or PIEL)
    if piedra:
        circle(ctx, hx + dir * 6, hy - 6, 9, (0.40, 0.38, 0.36))
    return hx, hy


def celso(ctx, x, y, s, dir=1, brazo_der=0.15, brazo_izq=-0.1, agacha=0.0, cabeza_baja=0.0, piedra=False,
          sombra=None, tortilla=False, rim=(0.9, 0.7, 0.5), t=0.0, camina=0.0):
    """agacha 0..1: se dobla y se inclina al frente · cabeza_baja 0..1: agacha la cabeza ·
    piedra: lleva una piedra en la mano que tira · tortilla: sostiene media tortilla en la mano derecha ·
    camina: pasos por segundo (0 = quieto; t = tiempo para el ciclo)."""
    ropa = MANTA
    ropa_osc = tuple(c * 0.72 for c in ropa)
    fase = t * camina * TAU
    ctx.save()
    ctx.translate(x, y - (abs(math.sin(fase)) * 4 * s if camina else 0))
    ctx.scale(s, s)
    k = 1 - 0.36 * agacha                                        # alto del cuerpo al agacharse
    inclina = 0.34 * agacha

    # piernas y huaraches
    for i, (dx, col) in enumerate(((-17, ropa_osc), (17, ropa))):
        sw = math.sin(fase + i * math.pi) * 22 if camina else 0
        lev = max(0.0, math.cos(fase + i * math.pi)) * 14 if camina else 0
        fx = dx * (1 + 0.4 * agacha) + (24 * agacha * dir) + sw
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_width(28)
        src(ctx, col)
        ctx.move_to(dx * (1 + 0.9 * agacha), -130 * k)
        ctx.line_to(fx, -8 - lev)
        ctx.stroke()
        _ovalo(ctx, fx + dir * 7, -5 - lev, 22, 8, (0.30, 0.20, 0.12))

    # torso y cabeza (se inclinan juntos al agacharse)
    ctx.save()
    ctx.translate(0, -130 * k)
    ctx.rotate(inclina * dir)
    ctx.translate(0, 130 * k)
    base = -130 * k
    torso = [(-36, base), (-30, base - 118), (30, base - 118), (36, base)]
    ctx.move_to(*torso[0])
    for p in torso[1:]:
        ctx.line_to(*p)
    ctx.close_path()
    g = cairo.LinearGradient(-36, 0, 36, 0)
    g.add_color_stop_rgb(0, *ropa)
    g.add_color_stop_rgb(1, *mix(ropa, rim, 0.18))
    ctx.set_source(g)
    ctx.fill()
    ctx.set_line_width(7)
    src(ctx, (0.45, 0.22, 0.16))                                  # faja del sarape cruzada al pecho
    ctx.move_to(-28, base - 112)
    ctx.line_to(24, base - 20)
    ctx.stroke()

    cuello_y = base - 124
    _brazo(ctx, (-30, base - 108), brazo_izq, 104 * (0.8 if agacha else 1), -dir, ropa_osc,
           mano=PIEL)
    cabeza_y = cuello_y - 26 + 14 * cabeza_baja
    line(ctx, 0, cuello_y + 6, 0, cabeza_y + 16, 18, PIEL)
    _ovalo(ctx, 0, cabeza_y, 25, 28, PIEL)
    # bigote y sombra del ala del sombrero sobre el rostro
    _ovalo(ctx, 0, cabeza_y + 11, 16, 5, (0.10, 0.07, 0.06))
    ctx.rectangle(-26, cabeza_y - 16, 52, 14)
    src(ctx, (0, 0, 0), 0.38)
    ctx.fill()
    # sombrero de palma
    _ovalo(ctx, 0, cabeza_y - 17, 56, 11, SOMBRERO)
    ctx.move_to(-31, cabeza_y - 19)
    ctx.curve_to(-31, cabeza_y - 62, 31, cabeza_y - 62, 31, cabeza_y - 19)
    ctx.close_path()
    src(ctx, mix(SOMBRERO, (1, 1, 1), 0.08))
    ctx.fill()
    ctx.rectangle(-31, cabeza_y - 30, 62, 8)
    src(ctx, (0.30, 0.16, 0.12))
    ctx.fill()
    mx, my = _brazo(ctx, (30, base - 108), brazo_der, 104 * (0.8 if agacha else 1), dir, ropa, piedra=piedra)
    if tortilla:
        ctx.save()
        ctx.translate(mx, my - 4)
        ctx.rotate(-0.3)
        ctx.move_to(-15, 0)
        ctx.arc(0, 0, 16, math.pi, 0)
        ctx.close_path()
        src(ctx, (0.93, 0.78, 0.46))
        ctx.fill()
        ctx.restore()
    ctx.restore()
    ctx.restore()
    if sombra:
        ctx.save()
        ctx.translate(x, y + 4)
        ctx.scale(1, 0.14)
        ctx.arc(0, 0, 70 * s, 0, TAU)
        ctx.restore()
        src(ctx, (0, 0, 0), sombra)
        ctx.fill()


def celso_arrodillado(ctx, x, y, s, t=0.0, cabeza_baja=0.6, rim=(0.55, 0.72, 1.0)):
    """De rodillas en la orilla, de frente a la cámara, con los hombros caídos. (x, y) = rodillas en el piso."""
    ropa = MANTA
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    resp = math.sin(t * 1.6) * 3
    for dx in (-30, 30):                                           # muslos y rodillas
        _ovalo(ctx, dx, -10, 26, 16, tuple(c * 0.75 for c in ropa))
    ctx.move_to(-46, -6)                                           # torso
    ctx.line_to(-32, -150 + resp)
    ctx.line_to(32, -150 + resp)
    ctx.line_to(46, -6)
    ctx.close_path()
    g = cairo.LinearGradient(-46, 0, 46, 0)
    g.add_color_stop_rgb(0, *tuple(c * 0.7 for c in ropa))
    g.add_color_stop_rgb(1, *mix(ropa, rim, 0.25))
    ctx.set_source(g)
    ctx.fill()
    for sx in (-1, 1):                                             # brazos sobre las rodillas
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.set_line_width(24)
        src(ctx, tuple(c * 0.8 for c in ropa))
        ctx.move_to(sx * 32, -140 + resp)
        ctx.line_to(sx * 44, -64)
        ctx.line_to(sx * 36, -22)
        ctx.stroke()
        circle(ctx, sx * 36, -20, 11, PIEL)
    cabeza_y = -176 + 16 * cabeza_baja + resp
    line(ctx, 0, -150 + resp, 0, cabeza_y + 16, 18, PIEL)
    _ovalo(ctx, 0, cabeza_y, 25, 28, PIEL)
    _ovalo(ctx, 0, cabeza_y + 11, 16, 5, (0.10, 0.07, 0.06))
    ctx.rectangle(-26, cabeza_y - 16, 52, 14)
    src(ctx, (0, 0, 0), 0.38)
    ctx.fill()
    _ovalo(ctx, 0, cabeza_y - 17, 56, 11, SOMBRERO)
    ctx.move_to(-31, cabeza_y - 19)
    ctx.curve_to(-31, cabeza_y - 62, 31, cabeza_y - 62, 31, cabeza_y - 19)
    ctx.close_path()
    src(ctx, mix(SOMBRERO, (1, 1, 1), 0.08))
    ctx.fill()
    ctx.rectangle(-31, cabeza_y - 30, 62, 8)
    src(ctx, (0.30, 0.16, 0.12))
    ctx.fill()
    ctx.restore()


def celso_en_el_lomo(ctx, x, y, s, t=0.0, dir=1):
    """Don Celso montado a cuestas de un perro que nada: solo medio cuerpo, abrazado al cuello. (x, y) = línea del agua."""
    ropa = MANTA
    bob = math.sin(t * 5.5) * 3
    ctx.save()
    ctx.translate(x, y + bob)
    ctx.scale(dir * s, s)
    ctx.move_to(-34, -36)                                          # torso inclinado hacia el cuello del perro
    ctx.line_to(-10, -150)
    ctx.line_to(36, -134)
    ctx.line_to(46, -34)
    ctx.close_path()
    src(ctx, ropa)
    ctx.fill()
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_width(22)
    src(ctx, tuple(c * 0.8 for c in ropa))
    ctx.move_to(24, -126)
    ctx.line_to(76, -110)
    ctx.line_to(92, -92)
    ctx.stroke()
    circle(ctx, 94, -90, 11, PIEL)
    line(ctx, 14, -148, 22, -166, 18, PIEL)
    _ovalo(ctx, 26, -184, 25, 28, PIEL)
    ctx.rectangle(0, -202, 52, 14)
    src(ctx, (0, 0, 0), 0.35)
    ctx.fill()
    _ovalo(ctx, 28, -201, 56, 11, SOMBRERO, rot=0.1)
    ctx.move_to(-3, -203)
    ctx.curve_to(-3, -246, 59, -246, 59, -203)
    ctx.close_path()
    src(ctx, mix(SOMBRERO, (1, 1, 1), 0.08))
    ctx.fill()
    ctx.restore()
