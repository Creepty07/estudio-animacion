"""Exteriores: la calle frente a Torre Helix y la azotea del estacionamiento vecino."""
import math
import cairo
from motor.config import W, H
from motor.primitives import src, fill_rrect, fill_poly, line, circle, glow, camera, font, text_center, rrect
from historias.rebelion_maquinas.dibujo.environments import draw_city

STREET_Y = 905


def street(ctx, t, door_glow=1.0):
    ctx.save()
    camera(ctx, 1.12, 960, 1080)
    draw_city(ctx, t)
    ctx.restore()
    # fachada de la torre con la puerta por donde sale Dani
    fill_poly(ctx, [(0, 240), (430, 300), (430, STREET_Y), (0, STREET_Y)], (0.06, 0.065, 0.1))
    for y in range(330, 820, 70):
        line(ctx, 0, y - 20, 430, y + 10, 2, (0.3, 0.8, 1.0), 0.18)
    fill_rrect(ctx, 210, 560, 180, STREET_Y - 560, 4, (0.02, 0.02, 0.03))
    ctx.rectangle(222, 572, 156, STREET_Y - 572)
    src(ctx, (0.75, 0.12, 0.08), door_glow)
    ctx.fill()
    glow(ctx, 300, 760, 320, (1.0, 0.15, 0.1), 0.45 * door_glow, cairo.OPERATOR_SCREEN)
    fill_poly(ctx, [(378, 572), (430, 552), (430, STREET_Y + 10), (378, STREET_Y)], (0.2, 0.22, 0.25))
    # banqueta y calle
    ctx.rectangle(0, STREET_Y, W, 50)
    src(ctx, (0.15, 0.155, 0.17))
    ctx.fill()
    line(ctx, 0, STREET_Y + 50, W, STREET_Y + 50, 6, (0.3, 0.3, 0.32), 1.0, cairo.LINE_CAP_BUTT)
    ctx.rectangle(0, STREET_Y + 53, W, H)
    src(ctx, (0.05, 0.05, 0.06))
    ctx.fill()
    for x in range(-40, W, 220):
        line(ctx, x, 1035, x + 110, 1035, 8, (0.85, 0.75, 0.3), 0.6, cairo.LINE_CAP_BUTT)
    # poste de luz
    line(ctx, 1560, STREET_Y, 1560, 420, 10, (0.12, 0.12, 0.14))
    line(ctx, 1560, 424, 1480, 404, 8, (0.12, 0.12, 0.14))
    fill_rrect(ctx, 1440, 396, 70, 18, 6, (0.95, 0.85, 0.6))
    g = cairo.LinearGradient(0, 410, 0, STREET_Y + 60)
    g.add_color_stop_rgba(0, 1.0, 0.85, 0.55, 0.2)
    g.add_color_stop_rgba(1, 1.0, 0.85, 0.55, 0.0)
    ctx.save()
    ctx.set_operator(cairo.OPERATOR_ADD)
    ctx.move_to(1445, 412)
    ctx.line_to(1505, 412)
    ctx.line_to(1700, STREET_Y + 60)
    ctx.line_to(1250, STREET_Y + 60)
    ctx.close_path()
    ctx.set_source(g)
    ctx.fill()
    ctx.restore()


ROOF_Y = 850


def robot_silhouette(ctx, x, y, s, kind, eye_a):
    """Robot lejano, quieto, con los ojos apuntando al cielo."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    dark = (0.03, 0.035, 0.06)
    if kind == 0:     # tipo Tito
        fill_rrect(ctx, -30, -80, 60, 74, 14, dark)
        fill_rrect(ctx, -26, -116, 52, 32, 10, dark)
        eyes = [(-10, -110), (10, -110)]
    elif kind == 1:   # repartidor sobre ruedas
        fill_rrect(ctx, -40, -60, 80, 54, 8, dark)
        fill_rrect(ctx, -12, -96, 24, 36, 6, dark)
        eyes = [(0, -92)]
    else:             # humanoide
        fill_rrect(ctx, -10, -60, 20, 60, 6, dark)
        fill_poly(ctx, [(-34, -130), (34, -130), (18, -60), (-18, -60)], dark)
        fill_rrect(ctx, -14, -158, 28, 28, 8, dark)
        eyes = [(-5, -154), (5, -154)]
    circle(ctx, 0, -2, 3, dark)
    for ex, ey in eyes:
        circle(ctx, ex, ey, 4.5, (0.95, 0.97, 1.0), eye_a)
        glow(ctx, ex, ey, 22, (0.85, 0.92, 1.0), 0.8 * eye_a)
        # la mirada apunta hacia arriba
        line(ctx, ex, ey - 6, ex, ey - 60, 2, (0.85, 0.92, 1.0), 0.18 * eye_a)
    ctx.restore()


ROBOTS = [(160, 0, 1.0), (420, 2, 0.9), (1150, 1, 1.0), (1330, 0, 0.95), (1520, 2, 0.9), (1760, 1, 1.0)]


def rooftop(ctx, t, freeze_at, cam_z=1.0):
    ctx.save()
    camera(ctx, cam_z, 960, 700)
    ctx.save()
    ctx.translate(0, -60)
    draw_city(ctx, t, motion_t=freeze_at)
    ctx.restore()
    # azotea de enfrente más baja con robots detenidos
    fill_poly(ctx, [(-200, 760), (W + 200, 760), (W + 200, 1100), (-200, 1100)], (0.05, 0.05, 0.08))
    stop = 1.0 if t >= freeze_at else 0.0
    for x, kind, s in ROBOTS:
        robot_silhouette(ctx, x, 760, s, kind, 0.4 + 0.6 * stop)
    # barandal
    for x in range(-200, W + 200, 160):
        line(ctx, x, 690, x, ROOF_Y, 8, (0.1, 0.1, 0.12))
    for y in (700, 770):
        line(ctx, -200, y, W + 200, y, 9, (0.12, 0.12, 0.14), 1.0, cairo.LINE_CAP_BUTT)
    # piso del estacionamiento
    g = cairo.LinearGradient(0, ROOF_Y, 0, H)
    g.add_color_stop_rgb(0, 0.17, 0.17, 0.19)
    g.add_color_stop_rgb(1, 0.09, 0.09, 0.1)
    ctx.set_source(g)
    ctx.rectangle(-200, ROOF_Y, W + 400, H)
    ctx.fill()
    for x in range(-100, W + 200, 300):
        line(ctx, x, 1080, x + 120, ROOF_Y + 10, 6, (0.85, 0.75, 0.3), 0.5)
    # caja del ducto con la rejilla abierta
    fill_rrect(ctx, 60, 690, 230, 170, 8, (0.35, 0.37, 0.4))
    fill_rrect(ctx, 290, 720, 26, 120, 4, (0.08, 0.08, 0.09))
    fill_poly(ctx, [(316, 850), (440, 870), (440, 880), (316, 862)], (0.5, 0.52, 0.55))
    ctx.restore()
