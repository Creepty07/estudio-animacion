"""El cuarto de Don Celso: cama, ventana con luna y una vela en la mesita. La vela da toda la luz tibia."""
import math
import cairo
from motor import config
from motor.config import SOMBRERO, PIEL, LLAMA
from motor.primitives import src, glow, circle, fill_screen, TAU, mix
from motor.layers import paint_layer
from historias.tumba_llorona.dibujo import velas

PISO = 1190
VELA_X, VELA_Y, VELA_S = 940, 1128, 1.9


def _estatico(c):
    W, H = config.W, config.H
    g = cairo.LinearGradient(0, 0, 0, PISO)
    g.add_color_stop_rgb(0, 0.10, 0.065, 0.05)
    g.add_color_stop_rgb(1, 0.20, 0.12, 0.085)
    c.rectangle(0, 0, W, PISO)
    c.set_source(g)
    c.fill()
    c.rectangle(0, PISO, W, H - PISO)
    src(c, (0.07, 0.045, 0.035))
    c.fill()
    # ventana con luna
    gv = cairo.LinearGradient(0, 380, 0, 800)
    gv.add_color_stop_rgb(0, 0.10, 0.18, 0.35)
    gv.add_color_stop_rgb(1, 0.22, 0.34, 0.52)
    c.rectangle(110, 380, 250, 400)
    c.set_source(gv)
    c.fill()
    circle(c, 270, 500, 34, (0.85, 0.92, 1.0), 0.9)
    for x, y, w, h in ((100, 370, 270, 14), (100, 780, 270, 14), (100, 370, 14, 424), (356, 370, 14, 424), (228, 370, 14, 424), (100, 570, 270, 12)):
        c.rectangle(x, y, w, h)
        src(c, (0.12, 0.07, 0.045))
        c.fill()
    # cama
    for lx in (170, 890):
        c.rectangle(lx, 1040, 22, 150)
        src(c, (0.14, 0.08, 0.05))
        c.fill()
    c.rectangle(150, 1010, 780, 52)
    src(c, (0.17, 0.10, 0.065))
    c.fill()
    c.rectangle(890, 840, 28, 230)                                                      # cabecera
    src(c, (0.14, 0.08, 0.05))
    c.fill()
    # mesita
    c.rectangle(860, 1130, 190, 24)
    src(c, (0.16, 0.09, 0.06))
    c.fill()
    c.rectangle(880, 1154, 24, 100)
    c.rectangle(1010, 1154, 24, 100)
    src(c, (0.14, 0.08, 0.05))
    c.fill()


def dibujar(ctx, t, llama=1.0, respira=1.0):
    """llama 0..1 = intensidad de la vela · respira 0..1 = cuánto se mueve el pecho."""
    W, H = config.W, config.H
    paint_layer(ctx, "cuarto_fijo", _estatico)
    # colchón, cuerpo bajo la cobija y almohada
    ctx.rectangle(160, 990, 740, 40)
    src(ctx, (0.50, 0.45, 0.38))
    ctx.fill()
    pecho = math.sin(t * 2.4) * 6 * respira
    ctx.move_to(190, 1000)
    ctx.curve_to(260, 930 - pecho, 330, 930 - pecho, 420, 960 - pecho * 0.8)
    ctx.curve_to(560, 975, 700, 925 - pecho, 800, 955 - pecho * 0.6)
    ctx.curve_to(850, 965, 880, 985, 888, 1000)
    ctx.close_path()
    src(ctx, (0.32, 0.24, 0.20))
    ctx.fill()
    for fx in (330, 520, 700):                                                          # pliegues de la cobija
        ctx.move_to(fx, 978)
        ctx.curve_to(fx + 14, 990, fx + 6, 1000, fx + 16, 1004)
        ctx.set_line_width(5)
        src(ctx, (0, 0, 0), 0.22)
        ctx.stroke()
    ctx.save()
    ctx.translate(836, 954 - pecho * 0.5)
    ctx.scale(1, 0.62)
    ctx.arc(0, 0, 56, 0, TAU)
    ctx.restore()
    src(ctx, (0.60, 0.58, 0.52))
    ctx.fill()
    ctx.save()
    ctx.translate(826, 934 - pecho * 0.5)                                               # cabeza sobre la almohada
    ctx.scale(1, 1.05)
    ctx.arc(0, 0, 25, 0, TAU)
    ctx.restore()
    src(ctx, PIEL)
    ctx.fill()
    ctx.save()
    ctx.translate(826, 944 - pecho * 0.5)
    ctx.scale(1, 0.36)
    ctx.arc(0, 0, 16, 0, TAU)
    ctx.restore()
    src(ctx, (0.10, 0.07, 0.06))
    ctx.fill()
    # sombrero colgado de la cabecera
    ctx.save()
    ctx.translate(904, 836)
    ctx.rotate(-0.15)
    ctx.save()
    ctx.scale(1, 0.2)
    ctx.arc(0, 0, 58, 0, TAU)
    ctx.restore()
    src(ctx, SOMBRERO)
    ctx.fill()
    ctx.move_to(-30, -2)
    ctx.curve_to(-30, -44, 30, -44, 30, -2)
    ctx.close_path()
    src(ctx, mix(SOMBRERO, (1, 1, 1), 0.08))
    ctx.fill()
    ctx.restore()
    # vela
    velas.cuerpo(ctx, VELA_X, VELA_Y, VELA_S)
    velas.llama(ctx, VELA_X, VELA_Y, VELA_S, t, seed=4, intensidad=llama, luz=420)
    glow(ctx, VELA_X - 120, VELA_Y - 100, 760 * llama, LLAMA, 0.16 * llama)
