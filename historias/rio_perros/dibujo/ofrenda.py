"""La ofrenda de hoy: la única escena cálida del video. Altar con arco de cempasúchil, velas, agua,
media tortilla y un perrito de barro."""
import math
import cairo
from motor import config
from motor.config import CEMPASUCHIL, LLAMA
from motor.primitives import src, line, glow, circle, fill_screen, rrect, TAU, mix, seg, smooth
from motor.kit import particles
from motor.layers import paint_layer
from historias.tumba_llorona.dibujo import flores, velas
from historias.rio_perros.dibujo import perros, calle

MESA_Y = 1020


def _estatico(c):
    W, H = config.W, config.H
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.06, 0.035, 0.03)
    g.add_color_stop_rgb(1, 0.13, 0.07, 0.05)
    c.rectangle(0, 0, W, H)
    c.set_source(g)
    c.fill()
    # arco de cempasúchil
    for i in range(19):
        u = i / 18
        ang = math.pi * (1.0 - u)
        fx, fy = W / 2 + math.cos(ang) * 400, MESA_Y - 80 - math.sin(ang) * 470
        flores.cempasuchil(c, fx, fy, 50 + 6 * math.sin(i * 1.7), rot=i, seed=i + 3, brillo=0.95)
    # mesa con mantel
    c.rectangle(0, MESA_Y, W, 360)
    src(c, (0.78, 0.30, 0.08))
    c.fill()
    c.rectangle(0, MESA_Y, W, 14)
    src(c, (1.0, 0.65, 0.20))
    c.fill()
    for i in range(14):                                                        # picado del mantel
        px = 40 + i * 80
        c.move_to(px - 24, MESA_Y + 60)
        c.line_to(px + 24, MESA_Y + 60)
        c.line_to(px, MESA_Y + 108)
        c.close_path()
        src(c, (1.0, 0.82, 0.30), 0.85)
        c.fill()
    # pétalos sobre la mesa
    for i in range(34):
        px = 40 + (i * 131) % (W - 80)
        flores.petalo(c, px, MESA_Y - 6 + (i * 17) % 22, 18 + (i % 4) * 4, i * 0.7, (1.0, 0.55 + 0.1 * (i % 3), 0.05), 0.95)
    # plato con media tortilla
    c.save()
    c.translate(300, MESA_Y - 10)
    c.scale(1, 0.26)
    c.arc(0, 0, 110, 0, TAU)
    c.restore()
    src(c, (0.88, 0.82, 0.70))
    c.fill()
    c.save()
    c.translate(300, MESA_Y - 30)
    c.move_to(-68, 8)
    c.arc(0, 8, 68, math.pi, 0)
    c.close_path()
    src(c, (0.93, 0.76, 0.42))
    c.fill()
    c.restore()
    # recipiente con agua
    c.save()
    c.translate(790, MESA_Y - 8)
    c.scale(1, 0.30)
    c.arc(0, 0, 112, 0, TAU)
    c.restore()
    src(c, (0.55, 0.30, 0.18))
    c.fill()
    c.save()
    c.translate(790, MESA_Y - 14)
    c.scale(1, 0.26)
    c.arc(0, 0, 90, 0, TAU)
    c.restore()
    src(c, (0.14, 0.28, 0.36))
    c.fill()


def dibujar(ctx, t):
    W, H = config.W, config.H
    paint_layer(ctx, "ofrenda_fija", _estatico)
    # velas
    for vx, vs, sd in ((130, 2.0, 1), (540, 2.4, 2), (950, 2.0, 3)):
        velas.cuerpo(ctx, vx, MESA_Y, vs)
        velas.llama(ctx, vx, MESA_Y, vs, t, seed=sd, luz=240)
    # perrito de barro junto a la vela central
    perros.perro(ctx, 640, MESA_Y + 4, 0.62, (0.60, 0.33, 0.20), dir=-1, orejas=1.1, hilo=config.HILO, rim=(1.0, 0.75, 0.45))
    # reflejo de la llama en el agua
    glow(ctx, 790 + 20 * math.sin(t * 1.3), MESA_Y - 12, 70, LLAMA, 0.22)
    # humo de copal
    for i in range(3):
        base_x = 540 + 40 * i
        for j in range(24):
            u = j / 23
            px = base_x + math.sin(u * 6 + t * 1.2 + i) * (10 + 50 * u)
            py = MESA_Y - 260 - u * 330
            circle(ctx, px, py, 3 + 8 * u, (0.85, 0.85, 0.9), 0.07 * (1 - u))
    particles(ctx, t, (1.0, 0.7, 0.3), n=34, seed=17, rise=26, alpha=0.7)
