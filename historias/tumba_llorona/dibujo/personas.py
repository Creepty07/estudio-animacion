"""Tomás y su abuela. Casi siempre de espalda o en sombra; la abuela tiene primer plano en la escena 5.

Origen de cada figura = punto en el suelo bajo sus pies (x, y); s = escala (1 = ~340 px de alto el chico).
"""
import math
import cairo
from motor.config import PIEL, SUDADERA, REBOZO, LLAMA
from motor.primitives import fill_rrect, fill_poly, line, circle, src, glow, TAU, mix

JEAN = (0.09, 0.12, 0.24)
CABELLO = (0.035, 0.03, 0.04)
ZAPATO = (0.045, 0.045, 0.06)
FALDA = (0.22, 0.10, 0.14)
CANAS = (0.62, 0.62, 0.66)


def con_luz(ctx, dibujar, luces, caja=None):
    """Dibuja la figura en un grupo y le suma luz solo encima de ella.

    luces = [(x, y, radio, rgb, fuerza)] en coordenadas del mundo. caja = (x, y, w, h) limita el trabajo.
    """
    ctx.save()
    if caja:
        ctx.rectangle(*caja)
        ctx.clip()
    ctx.push_group()
    dibujar()
    ctx.set_operator(cairo.OPERATOR_ATOP)
    for lx, ly, r, rgb, fz in luces:
        g = cairo.RadialGradient(lx, ly, 0, lx, ly, r)
        g.add_color_stop_rgba(0, *rgb, fz)
        g.add_color_stop_rgba(1, *rgb, 0)
        ctx.set_source(g)
        ctx.paint()
    ctx.set_operator(cairo.OPERATOR_OVER)
    ctx.pop_group_to_source()
    ctx.paint()
    ctx.restore()


def _ovalo(ctx, x, y, rx, ry, rgb, a=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(rx, ry)
    ctx.arc(0, 0, 1, 0, TAU)
    ctx.restore()
    src(ctx, rgb, a)
    ctx.fill()


# ---------------------------------------------------------------- Tomás
def _tomas_pie(ctx, fase):
    bob = -3 * abs(fase)
    ctx.translate(0, bob)
    for lado in (-1, 1):
        lift = 16 * max(0.0, fase * (-lado))
        fill_rrect(ctx, lado * 25 - 17, -190, 34, 182 - lift, 10, JEAN)
        _ovalo(ctx, lado * 25, -8 - lift, 25, 11, ZAPATO)
    _torso_cabeza(ctx, 0, fase)


def _tomas_arrodillado(ctx):
    for lado in (-1, 1):
        fill_rrect(ctx, lado * 26 - 21, -84, 42, 76, 16, JEAN)           # pantorrillas dobladas
        _ovalo(ctx, lado * 26, -9, 26, 10, ZAPATO)
    _ovalo(ctx, 0, -92, 74, 34, JEAN)                                   # cadera sobre los talones
    ctx.save()
    ctx.translate(0, 112)
    _torso_cabeza(ctx, 0, 0, sin_cintura=True)
    ctx.restore()


def _torso_cabeza(ctx, _swing, fase, sin_cintura=False):
    sw = 8 * fase
    for lado in (-1, 1):                                                 # brazos
        fill_rrect(ctx, lado * 73 - 14, -284 + sw * lado, 28, 124, 13, mix(SUDADERA, (0.2, 0.22, 0.3), 0.15))
        circle(ctx, lado * 73, -156 + sw * lado, 12, PIEL)
    fill_rrect(ctx, -62, -292, 124, 144, 26, SUDADERA)                   # torso
    fill_rrect(ctx, -62, -166, 124, 18, 8, mix(SUDADERA, (0, 0, 0), 0.3))
    _ovalo(ctx, 0, -293, 48, 24, mix(SUDADERA, (0, 0, 0), 0.35))         # capucha caída
    circle(ctx, 0, -334, 34, PIEL)                                       # cabeza
    for lado in (-1, 1):
        _ovalo(ctx, lado * 34, -330, 6, 10, mix(PIEL, (0, 0, 0), 0.15))
    _ovalo(ctx, 0, -343, 37, 34, CABELLO)                                # pelo


def tomas(ctx, x, y, s, pose="pie", fase=0.0, luces=None):
    """pose: 'pie' | 'camina' (usa fase -1..1) | 'arrodillado'."""
    def dibujo():
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(s, s)
        if pose == "arrodillado":
            _tomas_arrodillado(ctx)
        else:
            _tomas_pie(ctx, fase if pose == "camina" else 0.0)
        ctx.restore()
    if luces:
        con_luz(ctx, dibujo, luces, (x - 140 * s, y - 440 * s, 280 * s, 470 * s))
    else:
        dibujo()


def tomas_hombro(ctx, x, y, s, luces=None):
    """Primer plano de Tomás de espalda, cortado por el borde: cabeza y hombros enormes y oscuros."""
    def dibujo():
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(s, s)
        _ovalo(ctx, 0, 190, 330, 190, SUDADERA)                          # hombros
        _ovalo(ctx, 0, 120, 120, 60, mix(SUDADERA, (0, 0, 0), 0.35))     # capucha
        circle(ctx, 0, 0, 130, CABELLO)                                  # cabeza
        _ovalo(ctx, -122, 18, 18, 32, mix(PIEL, (0, 0, 0), 0.45))
        ctx.restore()
    if luces:
        con_luz(ctx, dibujo, luces)
    else:
        dibujo()


# ---------------------------------------------------------------- Abuela
def abuela(ctx, x, y, s, luces=None):
    """La abuela de espalda, con rebozo sobre la cabeza y falda larga (~300 px de alto)."""
    def dibujo():
        ctx.save()
        ctx.translate(x, y)
        ctx.scale(s, s)
        fill_poly(ctx, [(-46, -130), (46, -130), (62, -8), (-62, -8)], FALDA)
        for lado in (-1, 1):
            _ovalo(ctx, lado * 22, -6, 22, 9, ZAPATO)
        ctx.move_to(-80, -120)
        ctx.curve_to(-94, -200, -72, -272, 0, -284)
        ctx.curve_to(72, -272, 94, -200, 80, -120)
        ctx.close_path()
        g = cairo.LinearGradient(0, -284, 0, -120)
        g.add_color_stop_rgb(0, *mix(REBOZO, (1, 1, 1), 0.12))
        g.add_color_stop_rgb(1, *REBOZO)
        ctx.set_source(g)
        ctx.fill()
        for yy in (-150, -176, -202):
            line(ctx, -78 + (-yy - 120) * 0.05, yy, 78 - (-yy - 120) * 0.05, yy, 3, (0.6, 0.8, 0.85), 0.22)
        for i in range(17):
            line(ctx, -78 + i * 9.8, -120, -78 + i * 9.8 + 1, -106, 2, mix(REBOZO, (1, 1, 1), 0.2))
        ctx.restore()
    if luces:
        con_luz(ctx, dibujo, luces, (x - 120 * s, y - 310 * s, 240 * s, 330 * s))
    else:
        dibujo()


def abuela_rostro(ctx, x, y, s, t, boca=0.0, luz=(-210, 330), fuerza=1.0, parpadeo=0.0):
    """Primer plano frontal. luz = posición (local) de la vela que la ilumina desde abajo. boca 0..1 al hablar."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    # rebozo
    ctx.move_to(-480, 620)
    ctx.curve_to(-470, 200, -340, -260, 0, -285)
    ctx.curve_to(340, -260, 470, 200, 480, 620)
    ctx.close_path()
    g = cairo.LinearGradient(0, -285, 0, 620)
    g.add_color_stop_rgb(0, *mix(REBOZO, (1, 1, 1), 0.1))
    g.add_color_stop_rgb(1, *mix(REBOZO, (0, 0, 0), 0.3))
    ctx.set_source(g)
    ctx.fill()
    _ovalo(ctx, 0, 22, 208, 252, (0.02, 0.025, 0.035))                   # abertura oscura
    ctx.save()                                                           # canas asomando por el borde
    ctx.translate(0, 22)
    ctx.scale(200, 245)
    ctx.arc(0, 0, 1, math.pi * 1.02, math.pi * 1.98)
    ctx.restore()
    ctx.set_line_width(26)
    src(ctx, CANAS, 0.85)
    ctx.stroke()
    for k in range(14):
        a = math.pi * (1.06 + 0.067 * k)
        line(ctx, math.cos(a) * 200, 22 + math.sin(a) * 245, math.cos(a) * 168, 22 + math.sin(a) * 205, 3, (0.3, 0.3, 0.34), 0.7)
    fill_rrect(ctx, -64, 150, 128, 500, 30, (0.46, 0.31, 0.25))          # cuello
    # cara
    g = cairo.LinearGradient(0, -185, 0, 205)
    g.add_color_stop_rgb(0, 0.40, 0.27, 0.22)
    g.add_color_stop_rgb(1, 0.68, 0.48, 0.37)
    ctx.save()
    ctx.translate(0, 12)
    ctx.scale(150, 195)
    ctx.arc(0, 0, 1, 0, TAU)
    ctx.restore()
    ctx.set_source(g)
    ctx.fill()
    # luz cálida desde abajo (solo sobre la piel)
    ctx.save()
    ctx.rectangle(-64, 190, 128, 140)
    ctx.clip()
    glow(ctx, luz[0], luz[1], 520, LLAMA, 0.32 * fuerza)
    ctx.restore()
    ctx.save()
    ctx.translate(0, 12)
    ctx.scale(150, 195)
    ctx.arc(0, 0, 1, 0, TAU)
    ctx.restore()
    ctx.clip()
    glow(ctx, luz[0], luz[1], 520, LLAMA, 0.48 * fuerza)
    gs = cairo.LinearGradient(0, -190, 0, 60)                            # sombra de arriba: la luz llega de abajo
    gs.add_color_stop_rgba(0, 0, 0, 0, 0.62)
    gs.add_color_stop_rgba(1, 0, 0, 0, 0.0)
    ctx.rectangle(-160, -190, 320, 260)
    ctx.set_source(gs)
    ctx.fill()
    ctx.reset_clip()
    # arrugas
    for yy, a in ((-132, 0.22), (-112, 0.2), (-92, 0.16)):
        ctx.move_to(-92, yy)
        ctx.curve_to(-40, yy - 12, 40, yy - 12, 92, yy)
        ctx.set_line_width(4)
        src(ctx, (0.1, 0.05, 0.05), a)
        ctx.stroke()
    for lado in (-1, 1):
        ctx.move_to(lado * 46, 66)
        ctx.curve_to(lado * 66, 100, lado * 72, 126, lado * 64, 156)
        ctx.set_line_width(5)
        src(ctx, (0.1, 0.05, 0.05), 0.35)
        ctx.stroke()
        for k in range(3):
            line(ctx, lado * 108, -22 + k * 10, lado * (128 + k * 5), -30 + k * 20, 2.5, (0.1, 0.05, 0.05), 0.3)
    # ojos y cejas
    for lado in (-1, 1):
        ex = lado * 62
        _ovalo(ctx, ex, -28, 52, 30, (0.05, 0.03, 0.03), 0.28)             # cuenca en sombra
        cerrado = parpadeo
        ctx.move_to(ex - 36, -26)
        ctx.curve_to(ex - 14, -42 + 18 * cerrado, ex + 14, -42 + 18 * cerrado, ex + 36, -26)
        ctx.curve_to(ex + 14, -12 - 10 * cerrado, ex - 14, -12 - 10 * cerrado, ex - 36, -26)
        ctx.close_path()
        src(ctx, (0.80, 0.76, 0.72))
        ctx.fill()
        if cerrado < 0.8:
            circle(ctx, ex + lado * -2, -25 + 3 * cerrado, 12, (0.07, 0.04, 0.04))
            circle(ctx, ex + lado * -2 - 4, -30, 3.0, (1, 0.9, 0.7), 0.9)
        ctx.move_to(ex - 40, -26)
        ctx.curve_to(ex - 14, -46 + 18 * cerrado, ex + 14, -46 + 18 * cerrado, ex + 40, -26)
        ctx.set_line_width(7)
        src(ctx, (0.04, 0.02, 0.02))
        ctx.stroke()
        ctx.move_to(ex - lado * 40, -72)
        ctx.curve_to(ex - lado * 10, -92, ex + lado * 28, -80, ex + lado * 42, -62)
        ctx.set_line_width(15)
        src(ctx, (0.55, 0.55, 0.58), 0.92)
        ctx.stroke()
    # nariz
    ctx.move_to(-10, -30)
    ctx.curve_to(-26, 20, -34, 52, -26, 72)
    ctx.set_line_width(4)
    src(ctx, (0.1, 0.05, 0.05), 0.28)
    ctx.stroke()
    _ovalo(ctx, 0, 74, 30, 14, (0.78, 0.55, 0.40), 0.55 * fuerza)
    for lado in (-1, 1):
        _ovalo(ctx, lado * 13, 76, 6, 4, (0.12, 0.05, 0.05), 0.85)
    # boca
    my = 132
    if boca > 0.05:
        _ovalo(ctx, 0, my + 6, 30, 4 + 17 * boca, (0.10, 0.03, 0.04))
    ctx.move_to(-38, my)
    ctx.curve_to(-16, my - 6, 16, my - 6, 38, my)
    ctx.set_line_width(6)
    src(ctx, (0.40, 0.19, 0.19))
    ctx.stroke()
    ctx.move_to(-34, my + 8 + 8 * boca)
    ctx.curve_to(-12, my + 14 + 16 * boca, 12, my + 14 + 16 * boca, 34, my + 8 + 8 * boca)
    ctx.set_line_width(7)
    src(ctx, (0.45, 0.22, 0.20), 0.9)
    ctx.stroke()
    for lado in (-1, 1):
        ctx.move_to(lado * 38, my)
        ctx.curve_to(lado * 46, my + 10, lado * 46, my + 20, lado * 42, my + 28)
        ctx.set_line_width(4)
        src(ctx, (0.1, 0.05, 0.05), 0.3)
        ctx.stroke()
    # chal por delante del cuello
    for lado in (-1, 1):
        ctx.move_to(lado * 330, 330)
        ctx.curve_to(lado * 200, 270, lado * 90, 250, lado * -50, 290)
        ctx.line_to(lado * -20, 640)
        ctx.line_to(lado * 360, 640)
        ctx.close_path()
        src(ctx, mix(REBOZO, (1, 1, 1), 0.06))
        ctx.fill()
        for k in range(9):
            line(ctx, lado * (150 + k * 28), 560 + k * 4, lado * (146 + k * 28), 600 + k * 4, 2, (0.6, 0.8, 0.85), 0.2)
    glow(ctx, luz[0], luz[1] + 120, 600, LLAMA, 0.22 * fuerza)
    for lado in (-1, 1):                                                 # aretes
        circle(ctx, lado * 154, 92, 9, (0.92, 0.72, 0.3))
        circle(ctx, lado * 152, 89, 3, (1, 0.95, 0.8), 0.9)
    ctx.restore()
