"""El camino de pétalos de cempasúchil hacia la casa con ofrenda (escena inicial, la parte 'viva' del cuento)."""
import math
import random
import cairo
from motor import config
from motor.config import NOCHE_ALTO, LLAMA
from motor.primitives import fill_poly, fill_rrect, circle, glow, line, src, TAU, lerp
from motor.layers import paint_layer
from motor.kit import particles
from historias.tumba_llorona.dibujo import cielo, flores, velas

HORIZONTE = 0.46           # fracción de la altura donde está el horizonte
FLAGS = [(0.90, 0.22, 0.52), (1.0, 0.55, 0.10), (0.10, 0.72, 0.80), (1.0, 0.82, 0.20), (0.55, 0.32, 0.80)]
VELAS_K = [0.08, 0.15, 0.25, 0.38, 0.55, 0.75]          # profundidad de cada par de velas (0 horizonte, 1 borde inferior)


def _yh():
    return config.H * HORIZONTE


def _k_a_y(k):
    return _yh() + (config.H - _yh()) * k


def _mitad_camino(k):
    return 26 + 360 * k


def _casa(ctx):
    """Casa con la ofrenda encendida en la puerta."""
    W = config.W
    cx, y = W / 2, _yh() + 8
    fill_rrect(ctx, cx - 120, y - 118, 240, 118, 4, (0.26, 0.17, 0.15))               # muro
    fill_poly(ctx, [(cx - 138, y - 116), (cx + 138, y - 116), (cx + 104, y - 168), (cx - 104, y - 168)], (0.20, 0.09, 0.08))  # tejado
    fill_rrect(ctx, cx - 30, y - 92, 60, 92, 3, (0.04, 0.03, 0.03))                   # puerta
    g = cairo.LinearGradient(0, y - 92, 0, y)
    g.add_color_stop_rgb(0, 0.95, 0.55, 0.18)
    g.add_color_stop_rgb(1, 1.0, 0.78, 0.35)
    ctx.rectangle(cx - 26, y - 88, 52, 88)
    ctx.set_source(g)
    ctx.fill()
    for i, (w, yy) in enumerate(((40, 30), (30, 52), (20, 70))):                      # altar de tres niveles
        ctx.rectangle(cx - w / 2, y - yy, w, 18)
        src(ctx, (0.45, 0.16, 0.05))
        ctx.fill()
        for j in range(3 - i):
            circle(ctx, cx - w / 2 + 8 + j * (w - 16) / max(2 - i, 1), y - yy - 3, 3.2, (1.0, 0.55, 0.05))
    for sx in (-80, 80):                                                              # ventanas con luz
        fill_rrect(ctx, cx + sx - 14, y - 84, 28, 34, 3, (0.95, 0.62, 0.22), 0.85)
    for sx in (-250, 250):                                                            # postes del papel picado
        line(ctx, cx + sx, y + 2, cx + sx, y - 230, 6, (0.08, 0.05, 0.05))


def _fondo(ctx):
    """Todo lo que no se mueve: lomas, suelo, camino con pétalos, casa y velas (cuerpo)."""
    W, H = config.W, config.H
    yh = _yh()
    cielo.gradiente_vertical(ctx, [(0, NOCHE_ALTO), (1, (0.08, 0.13, 0.26))], 0, yh + 2)
    rnd = random.Random(8)
    for capa, (col, base, amp) in enumerate(((  (0.04, 0.07, 0.13), 40, 34), ((0.025, 0.045, 0.09), 18, 22))):
        ctx.move_to(0, yh)
        for x in range(0, W + 20, 20):
            ctx.line_to(x, yh - base - amp * math.sin(x * 0.006 + capa * 2.1) - rnd.uniform(0, 5))
        ctx.line_to(W, yh)
        ctx.close_path()
        src(ctx, col)
        ctx.fill()
    cielo.gradiente_vertical(ctx, [(0, (0.03, 0.04, 0.07)), (1, (0.05, 0.05, 0.07))], yh, H)   # suelo
    fill_poly(ctx, [(W / 2 - _mitad_camino(0), yh), (W / 2 + _mitad_camino(0), yh),
                    (W / 2 + _mitad_camino(1) + 60, H), (W / 2 - _mitad_camino(1) - 60, H)], (0.10, 0.08, 0.09))
    _casa(ctx)
    for i in range(70):                                                              # pétalos: más grandes y más abiertos al acercarse
        k = (i / 70) ** 1.5 * 0.98 + 0.02
        y = _k_a_y(k)
        hw = _mitad_camino(k)
        flores.petalos_en_camino(ctx, W / 2 - hw * 0.95, W / 2 + hw * 0.95, y, 2.5 + 20 * k, int(3 + 14 * k), 100 + i, 0.55 + 0.45 * k)
    for lado in (-1, 1):                                                             # velas y flores a los lados
        for n, k in enumerate(VELAS_K):
            x = W / 2 + lado * (_mitad_camino(k) + 36 + 90 * k)
            s = 0.12 + 1.15 * k
            velas.cuerpo(ctx, x, _k_a_y(k), s)
            flores.cempasuchil(ctx, x - lado * 46 * s, _k_a_y(k) - 18 * s, 30 * s, seed=n + lado * 7)
            flores.cempasuchil(ctx, x - lado * 84 * s, _k_a_y(k) - 12 * s, 22 * s, seed=n + 40 + lado)


def _papel_picado(ctx, t):
    W = config.W
    y0 = _yh() + 8 - 230
    xa, xb = W / 2 - 250, W / 2 + 250
    n = 11
    for i in range(n):
        u = (i + 0.5) / n
        x = lerp(xa, xb, u)
        y = y0 + 30 * math.sin(math.pi * u)
        sw = math.sin(t * 2.2 + i * 0.9) * 0.08
        col = tuple(c * 0.8 for c in FLAGS[i % len(FLAGS)])
        ctx.save()
        ctx.translate(x, y)
        ctx.rotate(sw)
        ctx.move_to(-20, 0)
        ctx.line_to(20, 0)
        ctx.line_to(20, 56)
        for z in range(4):
            ctx.line_to(20 - 10 * (z + 0.5), 56 + (8 if z % 2 == 0 else 0))
            ctx.line_to(20 - 10 * (z + 1), 56)
        ctx.close_path()
        src(ctx, col, 0.9)
        ctx.fill()
        line(ctx, -8, 14, 8, 14, 2, (0, 0, 0), 0.18)
        line(ctx, -8, 28, 8, 28, 2, (0, 0, 0), 0.18)
        ctx.restore()
    for i in range(n - 1):
        u0, u1 = i / (n - 1), (i + 1) / (n - 1)
        line(ctx, lerp(xa, xb, u0), y0 + 30 * math.sin(math.pi * u0), lerp(xa, xb, u1), y0 + 30 * math.sin(math.pi * u1), 2, (0.1, 0.07, 0.07))


def dibujar(ctx, t, apagadas=None):
    """Escena completa. `apagadas` = {índice de vela: intensidad 0..1} para apagar llamas desde afuera."""
    W, H = config.W, config.H
    paint_layer(ctx, "camino_fondo", _fondo)
    cielo.estrellas(ctx, t, 70, y_max=HORIZONTE * 0.8)
    cielo.luna(ctx, W * 0.74, H * 0.14, 60)
    _papel_picado(ctx, t)
    puerta = 0.9 + 0.1 * math.sin(t * 9) * math.sin(t * 3.1)
    glow(ctx, W / 2, _yh() - 40, 220, (1.0, 0.62, 0.2), 0.55 * puerta)
    glow(ctx, W / 2, _yh() + 40, 420, (1.0, 0.55, 0.15), 0.18 * puerta)
    idx = 0
    for lado in (-1, 1):
        for n, k in enumerate(VELAS_K):
            x = W / 2 + lado * (_mitad_camino(k) + 36 + 90 * k)
            s = 0.12 + 1.15 * k
            inten = 1.0 if apagadas is None else apagadas.get(idx, 1.0)
            velas.llama(ctx, x, _k_a_y(k), s, t, seed=idx, intensidad=inten, luz=170)
            glow(ctx, W / 2 + lado * _mitad_camino(k) * 0.4, _k_a_y(k) + 14 * s, 150 * s + 20, (1.0, 0.55, 0.15), 0.10 * inten)
            idx += 1
    particles(ctx, t, (1.0, 0.7, 0.3), n=26, seed=11, rise=26, size=(1.2, 3), alpha=0.8)
