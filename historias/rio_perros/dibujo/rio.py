"""El río del inframundo: cielo sin luna, montañas lejanas, orilla del otro lado, agua negra con niebla y la orilla de acá.

Capas de atrás hacia adelante: fondo() -> (lo que flota en el agua) -> orilla() -> personajes -> niebla_baja().
La línea de la orilla de acá está en ORILLA_Y; ahí pisan Don Celso y los perros.
"""
import math
import random
import cairo
from motor import config
from motor.config import RIO_OSCURO, RIO_CLARO, ORILLA, NIEBLA
from motor.primitives import src, line, glow, circle, fill_poly, TAU, mix
from motor.layers import paint_layer
from motor.kit import fog
from historias.tumba_llorona.dibujo import cielo

LEJOS_Y = 700         # donde la orilla de enfrente toca el agua
ORILLA_Y = 1250       # la orilla de acá


def _estatico_cielo(c):
    W = config.W
    cielo.gradiente_vertical(c, [(0, config.NOCHE_ALTO), (1, config.NOCHE_BAJO)], 0, LEJOS_Y + 4)
    r = random.Random(3)
    for ancho, color, base, alto in ((1.0, (0.020, 0.050, 0.070), 640, 90), (1.0, (0.008, 0.022, 0.032), 672, 64)):
        pts = [(-20, LEJOS_Y)]
        x = -20
        while x < W + 60:
            x += r.uniform(60, 130)
            pts.append((x, base - r.uniform(0, alto) * (1 if int(x) % 2 else 0.55)))
        pts += [(W + 60, LEJOS_Y), (-20, LEJOS_Y)]
        fill_poly(c, pts, color, 1.0)


def _estatico_rio(c):
    W = config.W
    g = cairo.LinearGradient(0, LEJOS_Y, 0, ORILLA_Y)
    g.add_color_stop_rgb(0, *RIO_CLARO)
    g.add_color_stop_rgb(0.5, *mix(RIO_CLARO, RIO_OSCURO, 0.7))
    g.add_color_stop_rgb(1, *RIO_OSCURO)
    c.rectangle(0, LEJOS_Y, W, ORILLA_Y - LEJOS_Y + 4)
    c.set_source(g)
    c.fill()
    c.rectangle(0, LEJOS_Y - 2, W, 46)                                         # orilla de enfrente
    src(c, (0.006, 0.014, 0.020))
    c.fill()
    r = random.Random(14)
    for _ in range(40):                                                         # matorrales de la orilla lejana
        x = r.uniform(0, W)
        c.save()
        c.translate(x, LEJOS_Y + 2)
        c.scale(r.uniform(16, 44), r.uniform(8, 22))
        c.arc(0, 0, 1, math.pi, TAU)
        c.restore()
        src(c, (0.006, 0.014, 0.020))
        c.fill()


def _estatico_orilla(c):
    W, H = config.W, config.H
    r = random.Random(21)
    pts = [(-10, ORILLA_Y + 14)]
    x = -10
    while x < W + 30:
        x += r.uniform(26, 64)
        pts.append((x, ORILLA_Y + r.uniform(-8, 14)))
    pts += [(W + 30, H + 10), (-10, H + 10)]
    fill_poly(c, pts, ORILLA, 1.0)
    for _ in range(46):                                                         # piedras y guijarros
        x, y = r.uniform(0, W), r.uniform(ORILLA_Y + 24, ORILLA_Y + 300)
        c.save()
        c.translate(x, y)
        c.scale(r.uniform(10, 34), r.uniform(5, 15))
        c.arc(0, 0, 1, 0, TAU)
        c.restore()
        src(c, (0.05, 0.075, 0.09), 0.9)
        c.fill()


def fondo(ctx, t):
    """Cielo, montañas, orilla lejana y agua. Las ondas se mueven; el resto va en caché."""
    W = config.W
    paint_layer(ctx, "rio_cielo", _estatico_cielo)
    cielo.estrellas(ctx, t, 55, seed=12, y_max=0.30, brillo=0.7)
    glow(ctx, W * 0.5, LEJOS_Y - 10, 700, (0.20, 0.45, 0.55), 0.26)             # resplandor frío en el horizonte
    paint_layer(ctx, "rio_agua", _estatico_rio)
    r = random.Random(33)
    for i in range(70):                                                         # ondas largas que avanzan despacio
        k = r.uniform(0, 1)
        y = LEJOS_Y + 30 + (ORILLA_Y - LEJOS_Y - 40) * k ** 1.2
        largo = 30 + 140 * k
        x = (r.uniform(0, W * 1.2) + t * (6 + 22 * k)) % (W * 1.2) - W * 0.1
        a = 0.06 + 0.18 * k * (0.5 + 0.5 * math.sin(t * 0.9 + i))
        line(ctx, x, y, x + largo, y, 1.6 + 2.4 * k, (0.60, 0.80, 0.90), a)


def orilla(ctx, t):
    paint_layer(ctx, "rio_orilla", _estatico_orilla)


def niebla_baja(ctx, t, fuerza=1.0):
    fog(ctx, t, NIEBLA, 0.11 * fuerza, LEJOS_Y - 80, ORILLA_Y - 40, seed=4, speed=14)
    fog(ctx, t, NIEBLA, 0.08 * fuerza, ORILLA_Y - 20, config.H, seed=7, speed=9)
