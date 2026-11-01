"""Primer plano de la piedra de la tumba con la flor que deja Tomás (escena 10)."""
import math
import random
import cairo
from motor import config
from motor.config import SUDADERA, PIEL
from motor.primitives import glow, line, src, circle, fill_screen, seg, smooth, ease_out, lerp, TAU, mix
from motor.layers import paint_layer
from historias.tumba_llorona.dibujo import cielo, flores

FLOR = (0.52, 0.47)         # posición final de la flor (fracción de pantalla)


def _piedra(ctx):
    W, H = config.W, config.H
    cielo.gradiente_vertical(ctx, [(0, (0.17, 0.21, 0.28)), (1, (0.06, 0.08, 0.12))], 0, H)
    r = random.Random(3)
    for _ in range(900):                                           # granos
        circle(ctx, r.uniform(0, W), r.uniform(0, H), r.uniform(1, 3.5), (1, 1, 1) if r.random() < 0.5 else (0, 0, 0), r.uniform(0.02, 0.07))
    for _ in range(5):                                             # grietas
        x, y = r.uniform(0, W), r.uniform(0, H)
        ctx.move_to(x, y)
        for _ in range(7):
            x += r.uniform(-60, 60)
            y += r.uniform(30, 110)
            ctx.line_to(x, y)
        ctx.set_line_width(r.uniform(3, 6))
        src(ctx, (0.01, 0.02, 0.04), 0.8)
        ctx.stroke()
    for _ in range(7):                                             # líquenes
        glow(ctx, r.uniform(0, W), r.uniform(0, H), r.uniform(60, 150), (0.12, 0.28, 0.24), 0.18, cairo.OPERATOR_OVER)


def _flor_posada(ctx, t_desde, t):
    W, H = config.W, config.H
    fx, fy = W * FLOR[0], H * FLOR[1]
    k = seg(t, t_desde, t_desde + 0.5)
    squash = 1 + 0.07 * math.sin(k * math.pi) * (1 - k)
    glow(ctx, fx, fy, 520, (1.0, 0.5, 0.1), 0.32 * smooth(k))
    ctx.save()
    ctx.translate(fx, fy)
    ctx.scale(1, 0.92 * squash)
    flores.cempasuchil(ctx, 0, 0, 120, rot=0.4, seed=5)
    ctx.restore()
    return fx, fy


def dibujar(ctx, t, t_llega=0.5, t_suelta=1.2, t_sale=2.0):
    """t = tiempo local de la toma. La mano trae la flor, la suelta y se retira."""
    W, H = config.W, config.H
    paint_layer(ctx, "piedra_primer_plano", _piedra)
    fx, fy = W * FLOR[0], H * FLOR[1]
    # sombra suave de la flor sobre la piedra
    glow(ctx, fx + 10, fy + 40, 190, (0, 0, 0), 0.5, cairo.OPERATOR_OVER)
    traer = ease_out(seg(t, t_llega - 0.9, t_suelta))
    sale = smooth(seg(t, t_sale, t_sale + 0.9))
    inicio, fin = (-160.0, 40.0), (fx - 60, fy - 80)
    hx = lerp(inicio[0], fin[0], traer) + lerp(0, -260, sale)
    hy = lerp(inicio[1], fin[1], traer) + lerp(0, -150, sale)
    if t < t_suelta:
        flores_pos = (hx + 62, hy + 62)
        line(ctx, hx + 20, hy + 20, flores_pos[0], flores_pos[1], 9, (0.2, 0.36, 0.16))
        flores.cempasuchil(ctx, flores_pos[0], flores_pos[1], 120, rot=0.4, seed=5)
    else:
        _flor_posada(ctx, t_suelta, t)
    # brazo con sudadera y mano
    ang = math.atan2(hy - (hy - 340), hx - (hx - 560))
    ctx.save()
    ctx.translate(hx, hy)
    ctx.rotate(ang)
    ctx.rectangle(-900, -58, 880, 116)
    src(ctx, mix(SUDADERA, (0.2, 0.22, 0.3), 0.25))
    ctx.fill()
    ctx.rectangle(-60, -62, 54, 124)
    src(ctx, mix(SUDADERA, (0, 0, 0), 0.3))
    ctx.fill()
    ctx.save()
    ctx.translate(34, 0)
    ctx.scale(66, 44)
    ctx.arc(0, 0, 1, 0, TAU)
    ctx.restore()
    src(ctx, mix(PIEL, (0, 0, 0), 0.25))
    ctx.fill()
    for k in range(3):
        line(ctx, 60, -16 + k * 16, 92 - abs(k - 1) * 4, -12 + k * 12, 13, mix(PIEL, (0, 0, 0), 0.25))
    ctx.restore()
    glow(ctx, hx + 20, hy, 340, (1.0, 0.55, 0.15), 0.18)        # la flor ilumina la mano
