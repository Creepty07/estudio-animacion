"""Ducto de ventilación en corte sobre el sótano, haces de escaneo y radio en primer plano."""
import math
import cairo
from motor.config import W, H, FONT_MONO
from motor.primitives import src, fill_rrect, fill_poly, line, circle, glow, rrect, font, text_center, mix, TAU

DUCT_Y0, DUCT_Y1 = 120, 400
WALL = 22
DUCT_FLOOR = DUCT_Y1 - WALL


def duct(ctx, grille_k=0.0):
    """grille_k: 0 = rejilla puesta, 1 = rejilla caída."""
    g = cairo.LinearGradient(0, DUCT_Y0, 0, DUCT_Y1)
    g.add_color_stop_rgb(0, 0.05, 0.055, 0.065)
    g.add_color_stop_rgb(1, 0.09, 0.1, 0.11)
    ctx.set_source(g)
    ctx.rectangle(-200, DUCT_Y0, W + 400, DUCT_Y1 - DUCT_Y0)
    ctx.fill()
    for x in range(-100, W + 200, 260):
        line(ctx, x, DUCT_Y0 + WALL, x, DUCT_FLOOR, 3, (0, 0, 0), 0.4, cairo.LINE_CAP_BUTT)
        circle(ctx, x - 8, DUCT_Y0 + WALL + 12, 3, (0.25, 0.27, 0.3))
    for y0 in (DUCT_Y0, DUCT_FLOOR):
        g = cairo.LinearGradient(0, y0, 0, y0 + WALL)
        g.add_color_stop_rgb(0, 0.55, 0.58, 0.62)
        g.add_color_stop_rgb(1, 0.35, 0.37, 0.4)
        ctx.set_source(g)
        ctx.rectangle(-200, y0, W + 400, WALL)
        ctx.fill()
    # soportes al techo
    for x in range(100, W, 480):
        line(ctx, x, 0, x, DUCT_Y0, 6, (0.22, 0.23, 0.25))
    # rejilla al final
    gx = W - 120
    if grille_k < 1:
        ctx.save()
        ctx.translate(gx, DUCT_FLOOR)
        ctx.rotate(-grille_k * 1.4)
        fill_rrect(ctx, 0, -(DUCT_FLOOR - DUCT_Y0 - WALL), 22, DUCT_FLOOR - DUCT_Y0 - WALL, 3, (0.45, 0.47, 0.5))
        for i in range(6):
            yy = -(DUCT_FLOOR - DUCT_Y0 - WALL) + 16 + i * 30
            line(ctx, 2, yy, 20, yy + 8, 4, (0.2, 0.2, 0.22))
        ctx.restore()


def scan_beam(ctx, x, y, angle, length=900, spread=0.22, a=0.3):
    """Haz rojo en forma de cono que sale del visor; se corta en la base del ducto."""
    ctx.save()
    ctx.rectangle(-200, DUCT_Y1, W + 400, H)
    ctx.clip()
    x1 = x + math.cos(angle - spread) * length
    y1 = y + math.sin(angle - spread) * length
    x2 = x + math.cos(angle + spread) * length
    y2 = y + math.sin(angle + spread) * length
    g = cairo.RadialGradient(x, y, 0, x, y, length)
    g.add_color_stop_rgba(0, 1.0, 0.25, 0.15, a)
    g.add_color_stop_rgba(1, 1.0, 0.1, 0.05, 0.0)
    ctx.set_operator(cairo.OPERATOR_ADD)
    ctx.move_to(x, y)
    ctx.line_to(x1, y1)
    ctx.line_to(x2, y2)
    ctx.close_path()
    ctx.set_source(g)
    ctx.fill()
    ctx.restore()


def beam_hit_x(x, y, angle):
    """Dónde toca el centro del haz la base del ducto (o None)."""
    s = math.sin(angle)
    if s >= -0.05:
        return None
    return x + (DUCT_Y1 - y) / s * math.cos(angle)


# ---------- radio en primer plano ----------
SKIN = (0.78, 0.55, 0.38)


def radio_closeup(ctx, t, led_on, screen_on, level):
    cx, top, bot = 960, 250, 930
    # brazo y mano por detrás
    fill_poly(ctx, [(560, 1080), (760, 1080), (900, 860), (760, 800)], (0.88, 0.47, 0.17))
    fill_rrect(ctx, 760, 690, 230, 230, 90, SKIN)
    # antena
    fill_rrect(ctx, 1060, 60, 34, 220, 14, (0.1, 0.1, 0.11))
    # cuerpo
    g = cairo.LinearGradient(820, 0, 1100, 0)
    g.add_color_stop_rgb(0, 0.2, 0.21, 0.23)
    g.add_color_stop_rgb(1, 0.11, 0.115, 0.13)
    rrect(ctx, 820, top, 280, bot - top, 44)
    ctx.set_source(g)
    ctx.fill()
    line(ctx, 846, top + 40, 846, bot - 40, 3, (1, 1, 1), 0.08)
    # bocina
    for i in range(7):
        y = top + 70 + i * 30
        line(ctx, 870, y, 1050, y, 12, (0.05, 0.05, 0.06))
    # led
    circle(ctx, 880, top + 30, 10, (0.3, 1.0, 0.45) if led_on else (0.15, 0.17, 0.15))
    if led_on:
        glow(ctx, 880, top + 30, 50, (0.3, 1.0, 0.45), 0.8)
    # pantalla
    sx0, sy0, sw, sh = 860, 560, 200, 110
    fill_rrect(ctx, sx0, sy0, sw, sh, 10, (0.15, 0.3, 0.2) if screen_on else (0.06, 0.08, 0.07))
    if screen_on:
        font(ctx, 22, FONT_MONO, bold=True)
        src(ctx, (0.6, 1.0, 0.7))
        text_center(ctx, "CANAL 3", sx0 + sw / 2, sy0 + 30)
        for i in range(12):
            h = 6 + level * 46 * abs(math.sin(t * 13 + i * 1.7)) * (0.5 + 0.5 * math.sin(i * 2.3 + t * 5))
            ctx.rectangle(sx0 + 20 + i * 14, sy0 + 82 - h / 2, 8, max(4, h))
            src(ctx, (0.6, 1.0, 0.7))
            ctx.fill()
        glow(ctx, sx0 + sw / 2, sy0 + sh / 2, 200, (0.4, 1.0, 0.6), 0.25)
    # botón lateral
    fill_rrect(ctx, 806, 420, 16, 110, 6, (0.08, 0.08, 0.09))
    # dedos que envuelven el radio
    for i in range(4):
        y = 700 + i * 52
        fill_rrect(ctx, 780, y, 120 - i * 8, 46, 22, SKIN)
        line(ctx, 880 - i * 8, y + 8, 880 - i * 8, y + 38, 3, mix(SKIN, (0, 0, 0), 0.25))
