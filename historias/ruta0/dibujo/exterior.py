"""Exteriores de Ruta 0 (ciudad del Bajío sin nombre, de noche y con lluvia): calle, parada, curva, puente, tienda."""
import math
import random
import cairo
from motor import config
from motor.primitives import src, line, circle, glow, fill_rrect, fill_poly, seg, smooth, lerp, mix, font, text_center, text_w, text_at
from historias.ruta0.dibujo.paleta import (ovalo, degradado_v, trazo, NOCHE_ALTO, NOCHE_BAJO, ASFALTO, ACERA, AMBAR, AMBAR_CLARO,
                                           AMARILLO, ROJO, HIERRO, CABELLO)

HORIZONTE = 820          # donde terminan los edificios y empieza la calle
SUELO = 1130             # línea de la acera donde pisan los personajes


def cielo(ctx, t, bruma=0.0):
    degradado_v(ctx, 0, 0, 1080, HORIZONTE + 40, NOCHE_ALTO, mix(NOCHE_BAJO, (0.10, 0.14, 0.18), bruma))
    glow(ctx, 540, HORIZONTE - 40, 900, (0.25, 0.35, 0.45), 0.18, cairo.OPERATOR_SCREEN)


def edificios(ctx, seed=3, color=(0.02, 0.03, 0.045), lejos=False):
    r = random.Random(seed)
    x = -20
    while x < 1100:
        w = r.uniform(110, 230)
        h = r.uniform(180, 420) * (0.6 if lejos else 1.0)
        fill_rrect(ctx, x, HORIZONTE - h, w, h + 60, 2, color)
        for _ in range(int(w * h / 9000)):
            if r.random() < 0.12:                                                   # una que otra ventana encendida
                fill_rrect(ctx, x + r.uniform(8, w - 24), HORIZONTE - r.uniform(30, h - 20), 14, 20, 1, (0.9, 0.78, 0.4), 0.55)
        x += w + r.uniform(-10, 14)


def calle(ctx, t, mojado=1.0, y0=HORIZONTE + 30):
    degradado_v(ctx, 0, y0, 1080, 1920 - y0, (0.03, 0.045, 0.06), (0.012, 0.02, 0.03))
    degradado_v(ctx, 0, SUELO - 8, 1080, 70, ACERA, (0.03, 0.04, 0.05))                    # acera
    line(ctx, 0, SUELO - 6, 1080, SUELO - 6, 5, (0.16, 0.2, 0.24), 0.8, cairo.LINE_CAP_BUTT)   # borde
    r = random.Random(7)
    for i in range(9):                                                                      # charcos que reflejan
        ovalo(ctx, r.uniform(0, 1080), r.uniform(SUELO + 80, 1800), r.uniform(80, 240), r.uniform(10, 26), (0.12, 0.2, 0.28), 0.35 * mojado)


def farol(ctx, x, y, s, t, enc=1.0, seed=2):
    parp = 0.8 + 0.2 * math.sin(t * 9 + seed) * math.sin(t * 2.3)
    line(ctx, x, y, x, y - 560 * s, 12 * s, (0.03, 0.045, 0.06))
    line(ctx, x, y - 560 * s, x + 90 * s, y - 590 * s, 10 * s, (0.03, 0.045, 0.06))
    glow(ctx, x + 96 * s, y - 580 * s, 520 * s, (0.8, 0.92, 1.0), 0.42 * enc * parp, cairo.OPERATOR_SCREEN)
    circle(ctx, x + 96 * s, y - 580 * s, 14 * s, (0.95, 1.0, 1.0), enc)
    if enc > 0:                                                                             # cono de luz con lluvia
        g = cairo.LinearGradient(0, y - 580 * s, 0, y)
        g.add_color_stop_rgba(0, 0.8, 0.92, 1.0, 0.16 * enc)
        g.add_color_stop_rgba(1, 0.8, 0.92, 1.0, 0.0)
        ctx.move_to(x + 96 * s, y - 575 * s)
        ctx.line_to(x - 140 * s, y)
        ctx.line_to(x + 340 * s, y)
        ctx.close_path()
        ctx.set_source(g)
        ctx.fill()


def parada(ctx, t, x=380, y=SUELO + 30, s=1.3, luz=1.0, banca=True):
    """Techito de parada: dos postes, techo y banca. (x, y) = centro del piso."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    for dx in (-190, 190):
        line(ctx, dx, 0, dx, -380, 14, (0.045, 0.06, 0.075))
    fill_rrect(ctx, -240, -410, 480, 34, 6, (0.05, 0.07, 0.09))                             # techo
    fill_poly(ctx, [(-240, -376), (240, -376), (200, -350), (-200, -350)], (0.025, 0.035, 0.05))
    fill_rrect(ctx, -190, -380, 380, 150, 0, (0.07, 0.1, 0.13), 0.45)                       # panel trasero
    if banca:
        fill_rrect(ctx, -150, -120, 300, 18, 6, (0.09, 0.07, 0.06))
        for dx in (-130, 130):
            line(ctx, dx, -102, dx, -20, 10, (0.03, 0.04, 0.05))
    line(ctx, 250, 0, 250, -480, 10, (0.04, 0.055, 0.07))                                   # poste del letrero
    fill_rrect(ctx, 218, -540, 66, 70, 6, (0.12, 0.2, 0.28))
    fill_rrect(ctx, 226, -532, 50, 54, 4, (0.04, 0.07, 0.1))
    glow(ctx, 0, -300, 300, (0.7, 0.9, 1.0), 0.07 * luz, cairo.OPERATOR_SCREEN)
    ctx.restore()


def escena_parada(ctx, t, luz=1.0, bruma=0.0, con_parada=True, x_parada=380):
    cielo(ctx, t, bruma)
    edificios(ctx, 3, lejos=True)
    edificios(ctx, 9, (0.015, 0.022, 0.035))
    calle(ctx, t)
    farol(ctx, 820, SUELO + 20, 1.0, t, luz)
    if con_parada:
        parada(ctx, t, x_parada, SUELO + 30, 1.3, luz)


# ------------------------------------------------------------------ curva y puente
def cruz_flores(ctx, x, y, s, foto=True, t=0.0, brillo=1.0):
    """Cruz de camino con flores de plástico, veladora y la foto de quien murió ahí."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    line(ctx, 0, 0, 0, -330, 16, (0.28, 0.2, 0.14))
    line(ctx, -90, -240, 90, -240, 16, (0.28, 0.2, 0.14))
    for i, (dx, dy, c) in enumerate(((-46, 4, (0.8, 0.3, 0.45)), (-10, 14, (0.9, 0.8, 0.3)), (30, 6, (0.5, 0.5, 0.9)), (62, 12, (0.9, 0.5, 0.2)), (-72, 14, (0.9, 0.9, 0.9)))):
        circle(ctx, dx, dy - 8, 17, c, 0.9)
        circle(ctx, dx, dy - 8, 6, (1, 0.9, 0.4), 0.9)
    fill_rrect(ctx, 54, -52, 24, 56, 5, (0.8, 0.8, 0.75), 0.9)                              # veladora
    glow(ctx, 66, -64, 110 * brillo, (1.0, 0.7, 0.3), 0.45 * brillo * (0.85 + 0.15 * math.sin(t * 11)), cairo.OPERATOR_SCREEN)
    circle(ctx, 66, -62, 5, (1.0, 0.85, 0.5), brillo)
    if foto:
        fill_rrect(ctx, -34, -330, 68, 86, 4, (0.12, 0.1, 0.08))
        fill_rrect(ctx, -29, -325, 58, 76, 3, (0.78, 0.76, 0.7))
        ovalo(ctx, 0, -292, 15, 18, (0.52, 0.4, 0.34))                                       # cara del señor
        ovalo(ctx, 0, -306, 17, 9, (0.12, 0.1, 0.1))
        ovalo(ctx, 0, -258, 24, 12, (0.18, 0.2, 0.28))
    ctx.restore()


def barandal(ctx, x0, x1, y, roto=None, doblado=0.0):
    """Barandal de carretera; roto=(a, b) deja un hueco entre esas x; doblado inclina un tramo hacia afuera."""
    n = int((x1 - x0) / 90)
    for i in range(n + 1):
        x = x0 + i * 90
        if roto and roto[0] < x < roto[1]:
            continue
        line(ctx, x, y, x, y - 110, 9, (0.1, 0.13, 0.16))
    xa = x0
    for seg_ in ([(x0, x1)] if not roto else [(x0, roto[0]), (roto[1], x1)]):
        line(ctx, seg_[0], y - 90 - doblado * 30, seg_[1], y - 90, 14, (0.2, 0.24, 0.28))
        line(ctx, seg_[0], y - 46 - doblado * 20, seg_[1], y - 46, 10, (0.15, 0.18, 0.21))
    if roto:                                                                                # extremos torcidos y astillas
        line(ctx, roto[0], y - 90, roto[0] + 40, y - 20, 14, (0.2, 0.24, 0.28))
        line(ctx, roto[1], y - 90, roto[1] - 36, y - 10, 14, (0.2, 0.24, 0.28))


def curva(ctx, t, brillo_cruz=1.0, foto=True):
    """Curva de carretera de noche con barandal doblado y la cruz con flores (CURVA DEL AHORCADO)."""
    cielo(ctx, t, 0.3)
    r = random.Random(4)
    for i in range(8):                                                                       # cerros
        ovalo(ctx, i * 160 - 30, HORIZONTE + 20, 190, 120 + r.uniform(0, 80), (0.012, 0.02, 0.03))
    degradado_v(ctx, 0, HORIZONTE + 20, 1080, 1920 - HORIZONTE, (0.025, 0.035, 0.045), (0.01, 0.015, 0.02))
    fill_poly(ctx, [(300, HORIZONTE + 20), (560, HORIZONTE + 20), (1180, 1340), (-200, 1340)], (0.05, 0.065, 0.08))      # carretera que se tuerce
    line(ctx, 430, HORIZONTE + 30, 540, 1340, 6, (0.5, 0.45, 0.2), 0.7)
    barandal(ctx, 560, 1090, 1030, doblado=1.0)
    barandal(ctx, -20, 300, 990, doblado=0.5)
    cruz_flores(ctx, 760, 1170, 1.35, foto, t, brillo_cruz)


def puente(ctx, t, ap=1.0):
    """Puente Viejo: barandal roto y el río abajo."""
    cielo(ctx, t, 0.35)
    ovalo(ctx, 540, HORIZONTE + 40, 700, 80, (0.012, 0.02, 0.03))
    degradado_v(ctx, 0, HORIZONTE + 30, 1080, 1920 - HORIZONTE, (0.02, 0.06, 0.1), (0.005, 0.015, 0.03))              # río
    for i in range(16):
        yy = HORIZONTE + 80 + i * 55
        w = 80 + 20 * math.sin(t * 1.1 + i)
        line(ctx, 100 + (i * 137) % 900, yy, 100 + (i * 137) % 900 + w, yy, 3, (0.45, 0.6, 0.75), 0.18)
    fill_rrect(ctx, -20, 1020, 1120, 60, 4, (0.07, 0.085, 0.1))                                                     # tablero del puente
    fill_rrect(ctx, -20, 1078, 1120, 30, 0, (0.03, 0.04, 0.05))
    for i in range(7):
        fill_poly(ctx, [(i * 190 - 30, 1108), (i * 190 + 30, 1108), (i * 190 + 12, 1340), (i * 190 - 12, 1340)], (0.02, 0.03, 0.04))
    barandal(ctx, -20, 1100, 1020, roto=(380, 700))


def tienda_vidrio(ctx, t, reflejo=0.0, luz=0.4):
    """Escaparate de una tienda cerrada. reflejo 0..1: en el vidrio se ve el interior de un camión con pasajeros (ver camion.reflejo_en_vidrio)."""
    cielo(ctx, t, 0.0)
    fill_rrect(ctx, 0, HORIZONTE - 300, 1080, 1500, 0, (0.045, 0.06, 0.075))
    fill_rrect(ctx, 70, 560, 940, 720, 8, (0.012, 0.02, 0.03))                                                       # vidrio
    for k in range(3):
        fill_rrect(ctx, 100 + k * 300, 600, 270, 640, 0, (0.03, 0.045, 0.06), 0.5)
    fill_rrect(ctx, 40, 520, 1000, 50, 6, (0.09, 0.11, 0.13))
    fill_rrect(ctx, 40, 1280, 1000, 40, 4, (0.07, 0.085, 0.1))
    line(ctx, 70, 560, 1010, 1280, 4, (0.85, 0.92, 1.0), 0.04)                                                       # brillo diagonal
    degradado_v(ctx, 0, 1320, 1080, 600, (0.03, 0.045, 0.06), (0.012, 0.02, 0.03))
    glow(ctx, 540, 900, 700, (0.3, 0.45, 0.6), 0.1 * luz, cairo.OPERATOR_SCREEN)


def letrero(ctx, x, y, s, texto, luz=1.0):
    """Letrero de parada en un poste: panel oscuro con letras claras. (x, y) = pie del poste."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    line(ctx, 0, 0, 0, -420, 12, (0.04, 0.055, 0.07))
    font(ctx, 38, "Inter", bold=True)
    w = text_w(ctx, texto, 2) + 50
    fill_rrect(ctx, -w / 2, -540, w, 110, 8, (0.02, 0.03, 0.04))
    fill_rrect(ctx, -w / 2 + 6, -534, w - 12, 98, 5, (0.1, 0.16, 0.22))
    src(ctx, (0.92, 0.96, 1.0), luz)
    text_center(ctx, texto, 0, -468, 2)
    glow(ctx, 0, -480, w * 0.9, (0.6, 0.8, 1.0), 0.12 * luz, cairo.OPERATOR_SCREEN)
    ctx.restore()
