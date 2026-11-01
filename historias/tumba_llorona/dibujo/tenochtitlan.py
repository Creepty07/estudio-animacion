"""Tenochtitlan de noche sobre el lago (flashback): siluetas de templos, antorchas y agua. Estilizado, sin pretensión arqueológica."""
import math
import random
import cairo
from motor import config
from motor.primitives import fill_poly, line, src, glow, circle, TAU, lerp
from motor.layers import paint_layer
from historias.tumba_llorona.dibujo import cielo, paisaje

HORIZONTE = 0.50
SIL = (0.012, 0.03, 0.06)
LUZ_ANTORCHA = (1.0, 0.62, 0.22)
ANTORCHAS = []          # se llena al dibujar la capa estática: (x, y)


def _escalonado(ctx, cx, yb, anchos, alto, col):
    """Pirámide escalonada: cada nivel es un trapecio más angosto."""
    for i, w in enumerate(anchos):
        y1, y0 = yb - alto * i, yb - alto * (i + 1)
        w2 = anchos[i + 1] if i + 1 < len(anchos) else w * 0.8
        fill_poly(ctx, [(cx - w / 2, y1), (cx + w / 2, y1), (cx + (w + w2) / 4, y0), (cx - (w + w2) / 4, y0)], col)


def _templo_mayor(ctx, cx, yb):
    anchos = [540, 450, 360, 270]
    alto = 62
    _escalonado(ctx, cx, yb, anchos, alto, SIL)
    top = yb - alto * len(anchos)
    g = cairo.LinearGradient(cx - 40, 0, cx + 40, 0)                       # escalinata iluminada
    g.add_color_stop_rgba(0, 0.45, 0.25, 0.12, 0.0)
    g.add_color_stop_rgba(0.5, 0.45, 0.25, 0.12, 0.55)
    g.add_color_stop_rgba(1, 0.45, 0.25, 0.12, 0.0)
    fill_poly(ctx, [(cx - 36, yb), (cx + 36, yb), (cx + 30, top), (cx - 30, top)], (0.18, 0.12, 0.10), 0.9)
    for lado in (-1, 1):                                                   # los dos adoratorios de la cima
        sx = cx + lado * 78
        fill_poly(ctx, [(sx - 46, top), (sx + 46, top), (sx + 46, top - 64), (sx - 46, top - 64)], SIL)
        fill_poly(ctx, [(sx - 58, top - 64), (sx + 58, top - 64), (sx + 34, top - 96), (sx - 34, top - 96)], SIL)
        for k in (-1, 1):
            line(ctx, sx + k * 52, top, sx + k * 52, top - 26, 4, (0.01, 0.02, 0.04))
            ANTORCHAS.append((sx + k * 52, top - 30))
    for i in range(4):                                                     # antorchas en los costados de la escalinata
        y = yb - 20 - i * 58
        for lado in (-1, 1):
            ANTORCHAS.append((cx + lado * (46 - i * 4), y))


def _edificio(ctx, x, yb, w, h, techo=0.0):
    fill_poly(ctx, [(x - w / 2, yb), (x + w / 2, yb), (x + w / 2, yb - h), (x - w / 2, yb - h)], SIL)
    if techo:
        fill_poly(ctx, [(x - w / 2 - 8, yb - h), (x + w / 2 + 8, yb - h), (x + w / 2 - 12, yb - h - techo), (x - w / 2 + 12, yb - h - techo)], SIL)


def _estatico(ctx):
    W, H = config.W, config.H
    yh = H * HORIZONTE
    ANTORCHAS.clear()
    cielo.gradiente_vertical(ctx, [(0, (0.008, 0.016, 0.045)), (0.6, (0.06, 0.10, 0.20)), (1, (0.34, 0.24, 0.30))], 0, yh + 2)
    ctx.move_to(0, yh)                                                     # montañas lejanas
    for x in range(0, W + 30, 30):
        ctx.line_to(x, yh - 70 - 60 * math.sin(x * 0.004 + 0.5) - 30 * math.sin(x * 0.011))
    ctx.line_to(W, yh)
    ctx.close_path()
    src(ctx, (0.035, 0.06, 0.11))
    ctx.fill()
    paisaje.agua(ctx, yh, H, 0.8)
    cx = W / 2
    _templo_mayor(ctx, cx, yh + 10)
    for x, w, h, t in ((cx - 330, 200, 90, 0), (cx - 230, 120, 128, 28), (cx + 260, 150, 100, 0), (cx + 380, 170, 76, 20),
                       (cx - 450, 160, 60, 0), (cx + 150, 90, 60, 0)):
        _edificio(ctx, x, yh + 8, w, h, t)
    for x in (cx - 330, cx + 260, cx - 230, cx + 380):
        ANTORCHAS.append((x, yh - 94))
    rect = random.Random(5)
    for _ in range(12):                                                    # luces de canoas y casas lejanas
        ANTORCHAS.append((rect.uniform(60, W - 60), yh + rect.uniform(4, 22)))


def dibujar(ctx, t, brillo=1.0):
    """Fondo completo del flashback. (La figura de la Llorona la agrega la escena.)"""
    W, H = config.W, config.H
    yh = H * HORIZONTE
    paint_layer(ctx, "tenochtitlan", _estatico)
    glow(ctx, W / 2, yh - 30, 700, (1.0, 0.5, 0.25), 0.16 * brillo)             # resplandor de la ciudad
    cielo.estrellas(ctx, t, 70, y_max=HORIZONTE * 0.8, seed=9)
    cielo.luna(ctx, W * 0.30, H * 0.17, 66, 0.95, rgb=(0.95, 0.88, 0.75))
    paisaje.reflejo_luna(ctx, t, W * 0.30, yh + 4, H * 0.8, brillo=0.8, rgb=(0.95, 0.88, 0.75))
    for i, (x, y) in enumerate(ANTORCHAS):
        r = random.Random(i)
        fl = 1 + 0.2 * math.sin(t * 11 + r.uniform(0, TAU)) + 0.1 * math.sin(t * 23 + r.uniform(0, TAU))
        glow(ctx, x, y, (46 + 18 * (y < yh - 150)) * fl, LUZ_ANTORCHA, 0.65 * brillo)
        circle(ctx, x, y, 3.2 * fl, (1.0, 0.85, 0.5), 0.95)
        for k in range(3):                                                 # reflejo en el agua, que tiembla
            ry = yh + 14 + (y - yh) * -0.2 + k * 34
            wv = math.sin(t * 2.1 + i + k) * 6
            line(ctx, x + wv - 8, ry + 40 + k * 24, x + wv + 8, ry + 40 + k * 24, 3, LUZ_ANTORCHA, 0.16 * brillo)
