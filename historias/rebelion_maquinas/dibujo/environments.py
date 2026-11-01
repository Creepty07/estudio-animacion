"""Escenarios: ciudad nocturna, sótano de Torre Helix y pasillo de emergencia."""
import math
import random
import cairo
from motor.config import W, H
from motor.primitives import (
    rrect, src, fill_rrect, fill_poly, line, circle, glow, font, text_at, text_center,
    TAU, mix, clamp,
)

# =============== CIUDAD ===============
_rng = random.Random(7)
STARS = [(_rng.uniform(0, W), _rng.uniform(0, 620), _rng.uniform(0.6, 1.8), _rng.uniform(0, TAU))
         for _ in range(160)]


def _skyline(seed, base_y, hmin, hmax, wmin, wmax, color, win_density, win_colors, skip=None):
    r = random.Random(seed)
    out, x = [], -40
    while x < W + 40:
        w = r.uniform(wmin, wmax)
        h = r.uniform(hmin, hmax)
        if skip and skip[0] < x + w / 2 < skip[1]:
            x += w
            continue
        wins = []
        for wy in range(int(base_y - h + 24), int(base_y - 20), 26):
            for wx in range(int(x + 12), int(x + w - 16), 22):
                if r.random() < win_density:
                    wins.append((wx, wy, r.choice(win_colors), r.uniform(0.4, 1.0)))
        out.append((x, w, h, wins))
        x += w + r.uniform(4, 18)
    return out


FAR = _skyline(3, 1080, 180, 420, 70, 160, (0.07, 0.07, 0.14), 0.12,
               [(0.5, 0.6, 0.9), (0.9, 0.7, 0.4)])
NEAR = _skyline(11, 1080, 120, 330, 110, 220, (0.025, 0.028, 0.06), 0.22,
                [(1.0, 0.78, 0.45), (0.55, 0.8, 1.0), (1.0, 0.9, 0.7)], skip=(780, 1140))


def draw_city(ctx, t, motion_t=None):
    """motion_t congela drones y la banda de la torre en ese instante (ciudad detenida)."""
    mt = t if motion_t is None else min(t, motion_t)
    g = cairo.LinearGradient(0, 0, 0, 900)
    g.add_color_stop_rgb(0, 0.015, 0.02, 0.06)
    g.add_color_stop_rgb(0.7, 0.07, 0.05, 0.15)
    g.add_color_stop_rgb(1, 0.16, 0.08, 0.2)
    ctx.set_source(g)
    ctx.rectangle(-200, -200, W + 400, H + 400)
    ctx.fill()

    for x, y, r, ph in STARS:
        circle(ctx, x, y, r, (1, 1, 1), 0.35 + 0.35 * math.sin(t * 2 + ph))
    circle(ctx, 1560, 190, 58, (0.92, 0.9, 0.82))
    circle(ctx, 1578, 178, 54, (0.9, 0.88, 0.8), 0.0)
    glow(ctx, 1560, 190, 220, (0.6, 0.6, 0.8), 0.25, cairo.OPERATOR_SCREEN)

    for layer, col in ((FAR, (0.07, 0.07, 0.14)), (NEAR, (0.025, 0.028, 0.06))):
        for x, w, h, wins in layer:
            ctx.rectangle(x, 1080 - h, w, h + 50)
            src(ctx, col)
            ctx.fill()
            for wx, wy, c, a in wins:
                ctx.rectangle(wx, wy, 9, 12)
                src(ctx, c, a * (0.55 if layer is FAR else 0.9))
                ctx.fill()

    draw_helix_tower(ctx, mt)

    # drones cruzando el cielo
    for i, (y0, speed, ph) in enumerate(((260, 140, 0), (380, -110, 2), (180, 90, 4))):
        x = (200 + i * 600 + mt * speed) % (W + 200) - 100
        y = y0 + math.sin(mt * 1.5 + ph) * 8
        fill_rrect(ctx, x - 14, y - 3, 28, 6, 3, (0.1, 0.1, 0.12))
        blink = 1.0 if (t * 2 + ph) % 1 < 0.25 else 0.2
        circle(ctx, x - 12, y, 2.5, (1, 0.2, 0.2), blink)
        glow(ctx, x - 12, y, 18, (1, 0.2, 0.2), 0.6 * blink)
        circle(ctx, x + 12, y, 2.5, (0.6, 0.9, 1.0), 0.9)

    g = cairo.LinearGradient(0, 1000, 0, 1080)
    g.add_color_stop_rgba(0, 0.0, 0.0, 0.0, 0)
    g.add_color_stop_rgba(1, 0.0, 0.0, 0.0, 0.9)
    ctx.set_source(g)
    ctx.rectangle(-200, 1000, W + 400, 300)
    ctx.fill()


def draw_helix_tower(ctx, t):
    cx, base, top = 960, 1080, 170
    half_b, half_t = 150, 92
    fill_poly(ctx, [(cx - half_b, base + 60), (cx + half_b, base + 60), (cx + half_t, top), (cx - half_t, top)],
              (0.045, 0.05, 0.09))
    # lado en sombra
    fill_poly(ctx, [(cx + 40, base + 60), (cx + half_b, base + 60), (cx + half_t, top), (cx + 24, top)],
              (0.03, 0.03, 0.06))
    # coronación y aguja
    fill_poly(ctx, [(cx - half_t, top), (cx + half_t, top), (cx + 50, top - 50), (cx - 50, top - 50)],
              (0.05, 0.055, 0.1))
    line(ctx, cx, top - 50, cx, top - 170, 5, (0.08, 0.08, 0.12))
    blink = 1.0 if t % 1.2 < 0.5 else 0.15
    circle(ctx, cx, top - 172, 5, (1, 0.2, 0.2), blink)
    glow(ctx, cx, top - 172, 40, (1, 0.15, 0.1), 0.8 * blink)

    # banda de luz helicoidal que sube
    pitch = 46.0
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    for k in range(-2, 22):
        prev = None
        for i in range(0, 41):
            th = i / 40 * math.pi - math.pi / 2
            y = base - (k + i / 40 * 0.5 + (t * 0.35) % 1) * pitch
            if y < top + 6 or y > base:
                prev = None
                continue
            frac = (base - y) / (base - top)
            half = half_b + (half_t - half_b) * frac
            x = cx + math.sin(th) * half * 0.98
            bright = math.cos(th)
            if prev:
                ctx.set_line_width(4)
                ctx.set_source_rgba(0.3, 0.85, 1.0, 0.15 + 0.75 * max(0.0, bright))
                ctx.move_to(*prev)
                ctx.line_to(x, y)
                ctx.stroke()
            prev = (x, y)
    glow(ctx, cx, 640, 420, (0.2, 0.6, 1.0), 0.12, cairo.OPERATOR_SCREEN)
    # letrero
    font(ctx, 26, "Inter", bold=True)
    src(ctx, (0.6, 0.9, 1.0), 0.85)
    text_center(ctx, "HELIX", cx, top + 46, 10)


# =============== SÓTANO ===============
FLOOR_Y = 830
_r2 = random.Random(21)
WALL_STAINS = [(_r2.uniform(0, W), _r2.uniform(200, 800), _r2.uniform(40, 140)) for _ in range(14)]


def draw_basement(ctx, t, lights=1.0, leds=True, spark=0.0):
    # muro
    g = cairo.LinearGradient(0, 0, 0, FLOOR_Y)
    g.add_color_stop_rgb(0, 0.10, 0.115, 0.14)
    g.add_color_stop_rgb(0.6, 0.20, 0.215, 0.24)
    g.add_color_stop_rgb(1, 0.17, 0.18, 0.2)
    ctx.set_source(g)
    ctx.rectangle(-200, -200, W + 400, FLOOR_Y + 200)
    ctx.fill()
    for x, y, r in WALL_STAINS:
        glow(ctx, x, y, r, (0.05, 0.05, 0.04), 0.35, cairo.OPERATOR_OVER)
    for x in range(-160, W + 200, 320):
        line(ctx, x, 150, x, FLOOR_Y, 3, (0, 0, 0), 0.25, cairo.LINE_CAP_BUTT)
    line(ctx, -200, 470, W + 200, 470, 3, (0, 0, 0), 0.2, cairo.LINE_CAP_BUTT)

    # letrero pintado
    font(ctx, 96, "Inter Display Black")
    src(ctx, (0.85, 0.66, 0.14), 0.75)
    text_at(ctx, "SÓTANO -3", 960, 360, 6)
    for i in range(12):
        fill_poly(ctx, [(960 + i * 44, 384), (982 + i * 44, 384), (962 + i * 44, 398), (940 + i * 44, 398)],
                  (0.85, 0.66, 0.14), 0.7)

    # tuberías
    ctx.rectangle(-200, 52, W + 400, 40)
    src(ctx, (0.30, 0.33, 0.36))
    ctx.fill()
    line(ctx, -200, 60, W + 200, 60, 4, (0.5, 0.53, 0.55), 0.6, cairo.LINE_CAP_BUTT)
    for x in range(-100, W + 200, 380):
        fill_rrect(ctx, x, 46, 34, 52, 4, (0.24, 0.26, 0.28))
    ctx.rectangle(-200, 112, W + 400, 18)
    src(ctx, (0.40, 0.26, 0.17))
    ctx.fill()
    ctx.rectangle(1810, 92, 34, FLOOR_Y - 92)
    src(ctx, (0.28, 0.3, 0.33))
    ctx.fill()

    # puerta de salida
    fill_rrect(ctx, 1610, 430, 190, FLOOR_Y - 430, 4, (0.13, 0.15, 0.17))
    ctx.rectangle(1626, 446, 158, FLOOR_Y - 446)
    src(ctx, (0.22, 0.25, 0.27))
    ctx.fill()
    fill_rrect(ctx, 1760, 620, 14, 46, 4, (0.6, 0.62, 0.64))
    fill_rrect(ctx, 1640, 372, 130, 42, 6, (0.05, 0.35, 0.18))
    font(ctx, 26, "Inter", bold=True)
    src(ctx, (0.75, 1.0, 0.8))
    text_center(ctx, "SALIDA", 1705, 402, 2)
    glow(ctx, 1705, 393, 110, (0.2, 1.0, 0.45), 0.25)

    # tablero eléctrico (abierto)
    fill_poly(ctx, [(250, 352), (318, 340), (318, 732), (250, 716)], (0.33, 0.36, 0.38))
    fill_poly(ctx, [(262, 470), (300, 462), (281, 432)], (0.95, 0.75, 0.1))
    fill_rrect(ctx, 318, 340, 380, 392, 8, (0.42, 0.45, 0.47))
    fill_rrect(ctx, 336, 358, 344, 356, 4, (0.08, 0.09, 0.1))
    for row in range(4):
        for col in range(8):
            bx, by = 356 + col * 34, 382 + row * 78
            fill_rrect(ctx, bx, by, 24, 52, 3, (0.72, 0.74, 0.76))
            up = (row * 8 + col) % 5 != 3
            fill_rrect(ctx, bx + 6, by + (8 if up else 28), 12, 16, 2, (0.2, 0.2, 0.22))
    for i in range(4):
        lx, ly = 652, 384 + i * 40
        if i == 2:
            on = leds and (t * 1.4) % 1 < 0.5
            c = (1.0, 0.2, 0.15)
        else:
            on = leds
            c = (0.3, 1.0, 0.4)
        circle(ctx, lx, ly, 7, c if on else (0.15, 0.15, 0.15))
        if on:
            glow(ctx, lx, ly, 28, c, 0.6)
    # cables al suelo
    ctx.set_line_width(10)
    for i, col in enumerate(((0.05, 0.05, 0.05), (0.3, 0.1, 0.08), (0.05, 0.1, 0.25))):
        src(ctx, col)
        ctx.move_to(420 + i * 30, 732)
        ctx.curve_to(420 + i * 30, 790, 360 + i * 50, 800, 330 + i * 60, FLOOR_Y + 20)
        ctx.stroke()

    # chispas
    if spark > 0:
        r = random.Random(int(t * 30))
        for _ in range(14):
            a = r.uniform(0, TAU)
            ln = r.uniform(12, 60) * spark
            line(ctx, 600, 560, 600 + math.cos(a) * ln, 560 + math.sin(a) * ln, 3, (1, 0.95, 0.6), spark)
        glow(ctx, 600, 560, 140, (1, 0.85, 0.4), 0.8 * spark)

    # piso
    g = cairo.LinearGradient(0, FLOOR_Y, 0, H)
    g.add_color_stop_rgb(0, 0.12, 0.125, 0.14)
    g.add_color_stop_rgb(1, 0.05, 0.055, 0.065)
    ctx.set_source(g)
    ctx.rectangle(-200, FLOOR_Y, W + 400, H - FLOOR_Y + 200)
    ctx.fill()
    ctx.rectangle(-200, FLOOR_Y - 14, W + 400, 14)
    src(ctx, (0.07, 0.075, 0.085))
    ctx.fill()
    for i, y in enumerate((880, 950, 1040)):
        line(ctx, -200, y, W + 200, y, 2, (0, 0, 0), 0.25, cairo.LINE_CAP_BUTT)
    # charco brillante
    ctx.save()
    ctx.translate(1190, 905)
    ctx.scale(1, 0.12)
    circle(ctx, 0, 0, 160, (0.55, 0.7, 0.85), 0.12)
    ctx.restore()

    # letrero de piso mojado
    fill_poly(ctx, [(990, 905), (1052, 905), (1036, 765), (1006, 765)], (0.96, 0.78, 0.12))
    fill_poly(ctx, [(1021, 787), (1038, 821), (1004, 821)], (0.1, 0.1, 0.1))
    font(ctx, 22, "Inter", bold=True)
    src(ctx, (0.96, 0.78, 0.12))
    text_center(ctx, "!", 1021, 817)
    # cubeta
    fill_poly(ctx, [(1520, 827), (1620, 827), (1606, 909), (1534, 909)], (0.96, 0.78, 0.12))
    fill_rrect(ctx, 1514, 819, 112, 14, 4, (0.8, 0.62, 0.08))
    fill_rrect(ctx, 1556, 793, 30, 30, 4, (0.45, 0.47, 0.5))

    # lámparas fluorescentes
    for cx in (520, 1440):
        line(ctx, cx - 120, 130, cx - 120, 160, 3, (0.2, 0.2, 0.2))
        line(ctx, cx + 120, 130, cx + 120, 160, 3, (0.2, 0.2, 0.2))
        fill_rrect(ctx, cx - 160, 158, 320, 20, 6, (0.18, 0.19, 0.2))
        tube = mix((0.35, 0.37, 0.4), (0.92, 0.97, 1.0), lights)
        fill_rrect(ctx, cx - 148, 176, 296, 10, 5, tube)
        if lights > 0:
            g = cairo.LinearGradient(0, 186, 0, FLOOR_Y + 120)
            g.add_color_stop_rgba(0, 0.85, 0.95, 1.0, 0.16 * lights)
            g.add_color_stop_rgba(1, 0.85, 0.95, 1.0, 0.0)
            ctx.save()
            ctx.set_operator(cairo.OPERATOR_ADD)
            poly_pts = [(cx - 150, 186), (cx + 150, 186), (cx + 470, FLOOR_Y + 120), (cx - 470, FLOOR_Y + 120)]
            ctx.move_to(*poly_pts[0])
            for p in poly_pts[1:]:
                ctx.line_to(*p)
            ctx.close_path()
            ctx.set_source(g)
            ctx.fill()
            ctx.restore()
            glow(ctx, cx, 182, 240, (0.8, 0.92, 1.0), 0.35 * lights)


def beacon(ctx, t, x=960, y=200, strength=1.0):
    """Luz giratoria de emergencia en el techo."""
    ang = t * 3.2
    fill_rrect(ctx, x - 34, y - 46, 68, 16, 4, (0.12, 0.12, 0.12))
    ctx.arc(x, y - 30, 28, math.pi, TAU)
    ctx.close_path()
    src(ctx, (1.0, 0.22, 0.16))
    ctx.fill()
    glow(ctx, x, y - 40, 140, (1.0, 0.15, 0.1), 0.9 * strength)
    left = max(0.0, math.cos(ang))
    right = max(0.0, -math.cos(ang))
    glow(ctx, 420, 500, 900, (1.0, 0.12, 0.08), 0.55 * strength * (0.35 + left), cairo.OPERATOR_SCREEN)
    glow(ctx, 1500, 500, 900, (1.0, 0.12, 0.08), 0.55 * strength * (0.35 + right), cairo.OPERATOR_SCREEN)


# =============== PASILLO ===============
VPX, VPY = 960, 500
F = 820.0
FLOOR_Yw, CEIL_Yw, HALF_Xw = 1.6, -1.9, 3.0
Z_END = 15.0


def proj(X, Y, z):
    return VPX + X * F / z, VPY + Y * F / z


def wall_quad(X0, Y0, X1, Y1, z0, z1, along="x"):
    """Cuadrilátero en perspectiva: plano de pared (X fijo) o piso/techo (Y fijo)."""
    if along == "wall":
        return [proj(X0, Y0, z0), proj(X0, Y0, z1), proj(X0, Y1, z1), proj(X0, Y1, z0)]
    return [proj(X0, Y0, z0), proj(X1, Y0, z0), proj(X1, Y0, z1), proj(X0, Y0, z1)]


def draw_corridor(ctx, t, doors_p):
    """doors_p: lista de (lado, z0, progreso_cierre 0..1)."""
    ctx.rectangle(-200, -200, W + 400, H + 400)
    src(ctx, (0.05, 0.01, 0.012))
    ctx.fill()

    # fondo brillante (de donde vienen los Centinelas)
    bx0, by0 = proj(-HALF_Xw, CEIL_Yw, Z_END)
    bx1, by1 = proj(HALF_Xw, FLOOR_Yw, Z_END)
    ctx.rectangle(bx0, by0, bx1 - bx0, by1 - by0)
    src(ctx, (0.55, 0.1, 0.08))
    ctx.fill()
    glow(ctx, VPX, VPY + 20, 420, (1.0, 0.45, 0.35), 0.8, cairo.OPERATOR_SCREEN)

    zs = [1.0 + i * 0.5 for i in range(int((Z_END - 1.0) / 0.5) + 1)]
    for z0, z1 in zip(zs[:-1], zs[1:]):
        fog = clamp((z0 - 1) / (Z_END - 1))
        k = 0.12 + 0.55 * fog ** 1.6
        floor_c = (0.22 * k + 0.04, 0.03 * k, 0.03 * k)
        wall_c = (0.30 * k + 0.05, 0.04 * k + 0.01, 0.04 * k + 0.01)
        ceil_c = (0.16 * k + 0.02, 0.02 * k, 0.02 * k)
        fill_poly(ctx, wall_quad(-HALF_Xw, FLOOR_Yw, HALF_Xw, FLOOR_Yw, z0, z1), floor_c)
        fill_poly(ctx, wall_quad(-HALF_Xw, CEIL_Yw, HALF_Xw, CEIL_Yw, z0, z1), ceil_c)
        fill_poly(ctx, wall_quad(-HALF_Xw, CEIL_Yw, 0, FLOOR_Yw, z0, z1, "wall"), wall_c)
        fill_poly(ctx, wall_quad(HALF_Xw, CEIL_Yw, 0, FLOOR_Yw, z0, z1, "wall"), wall_c)

    # líneas guía del piso y zócalos
    for X in (-1.2, 1.2):
        x0, y0 = proj(X, FLOOR_Yw, 1.0)
        x1, y1 = proj(X, FLOOR_Yw, Z_END)
        line(ctx, x0, y0, x1, y1, 4, (1.0, 0.3, 0.2), 0.25)
    for X in (-HALF_Xw, HALF_Xw):
        x0, y0 = proj(X, FLOOR_Yw - 0.15, 1.0)
        x1, y1 = proj(X, FLOOR_Yw - 0.15, Z_END)
        line(ctx, x0, y0, x1, y1, 3, (0, 0, 0), 0.5)

    # puertas con cortinas metálicas
    for side, z0, p in doors_p:
        X = side * HALF_Xw
        z1 = z0 + 1.3
        top, bot = -0.7, FLOOR_Yw
        frame = wall_quad(X, top - 0.12, 0, bot, z0 - 0.12, z1 + 0.12, "wall")
        fill_poly(ctx, frame, (0.12, 0.03, 0.03))
        fill_poly(ctx, wall_quad(X, top, 0, bot, z0, z1, "wall"), (0.01, 0.0, 0.0))
        if p > 0:
            yb = top + (bot - top) * p
            fill_poly(ctx, wall_quad(X, top, 0, yb, z0, z1, "wall"), (0.36, 0.1, 0.09))
            n = 9
            for i in range(1, n):
                yy = top + (yb - top) * i / n
                a0 = proj(X, yy, z0)
                a1 = proj(X, yy, z1)
                line(ctx, a0[0], a0[1], a1[0], a1[1], 2, (0.12, 0.02, 0.02), 0.8)
            e0 = proj(X, yb, z0)
            e1 = proj(X, yb, z1)
            line(ctx, e0[0], e0[1], e1[0], e1[1], 5, (0.6, 0.18, 0.14))

    # lámparas de techo
    for i, z in enumerate((2.2, 4.4, 6.6, 8.8, 11.0, 13.2)):
        pulse = 0.5 + 0.5 * math.sin(t * 5 - i * 0.9)
        x, y = proj(0, CEIL_Yw + 0.05, z)
        w = 0.7 * F / z
        fill_rrect(ctx, x - w / 2, y - 3, w, max(4, 0.12 * F / z), 3, (1.0, 0.3, 0.22), 0.5 + 0.5 * pulse)
        glow(ctx, x, y + 0.2 * F / z, 1.6 * F / z, (1.0, 0.15, 0.1), 0.25 + 0.3 * pulse, cairo.OPERATOR_SCREEN)
        fx, fy = proj(0, FLOOR_Yw, z)
        ctx.save()
        ctx.translate(fx, fy)
        ctx.scale(1, 0.15)
        glow(ctx, 0, 0, 1.4 * F / z, (1.0, 0.2, 0.15), 0.18 + 0.18 * pulse, cairo.OPERATOR_SCREEN)
        ctx.restore()
