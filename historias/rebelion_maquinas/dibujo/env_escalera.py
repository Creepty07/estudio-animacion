"""Escalera de servicio en corte lateral. Coordenadas de mundo: x a la derecha, y hacia abajo,
con el descanso del piso -3 en y = 0 y cada piso 420 px más arriba."""
import cairo
from motor.config import W, H
from motor.primitives import src, fill_rrect, fill_poly, line, circle, glow, font, text_center, mix

FH = 420           # alto de un piso
STEPS = 12
STEP_W, STEP_H = 36, FH / STEPS
FLIGHT_W = STEPS * STEP_W
LANDING_W = 260
FLOOR_W = FLIGHT_W + LANDING_W
FLOORS = ["-3", "-2", "-1", "PB"]
SLAB = 70


def landing_x(f):
    return f * FLOOR_W


def stair_y(u):
    """Altura del piso de la escalera (y de mundo) en la posición horizontal u."""
    f = int(u // FLOOR_W)
    local = u - f * FLOOR_W
    base = -f * FH
    if local <= LANDING_W or f >= len(FLOORS) - 1:
        return base
    k = min(STEPS, int((local - LANDING_W) // STEP_W) + 1)
    return base - k * STEP_H


def stairwell(ctx, cam_x, cam_y):
    """Dibuja muro, tramos, barandales, letreros y la puerta de salida en PB."""
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.15, 0.16, 0.18)
    g.add_color_stop_rgb(1, 0.2, 0.21, 0.23)
    ctx.set_source(g)
    ctx.paint()
    ctx.save()
    ctx.translate(W / 2 - cam_x, H * 0.62 - cam_y)
    # juntas del muro
    for k in range(-2, 16):
        x = k * 300 + 40
        line(ctx, x, -2200, x, 800, 3, (0, 0, 0), 0.2, cairo.LINE_CAP_BUTT)
    for f, name in enumerate(FLOORS):
        lx = landing_x(f)
        y = -f * FH
        # letrero del piso pintado en el muro
        font(ctx, 150, "Inter Display Black")
        src(ctx, (0.85, 0.66, 0.14), 0.7)
        text_center(ctx, name, lx + LANDING_W / 2, y - 120)
        # lámpara de emergencia
        fill_rrect(ctx, lx + 40, y - 330, 50, 24, 6, (0.3, 0.3, 0.32))
        if name == "PB":
            # puerta de salida
            fill_rrect(ctx, lx + 330, y - 300, 130, 300, 4, (0.12, 0.14, 0.16))
            ctx.rectangle(lx + 342, y - 288, 106, 288)
            src(ctx, (0.25, 0.28, 0.3))
            ctx.fill()
            fill_rrect(ctx, lx + 340, y - 350, 120, 38, 6, (0.05, 0.35, 0.18))
            font(ctx, 24, "Inter", bold=True)
            src(ctx, (0.75, 1.0, 0.8))
            text_center(ctx, "SALIDA", lx + 400, y - 323, 2)
    # losas y tramos
    for f in range(len(FLOORS)):
        lx = landing_x(f)
        y = -f * FH
        conc = (0.32, 0.33, 0.35)
        fill_poly(ctx, [(lx - 10, y), (lx + LANDING_W, y), (lx + LANDING_W, y + SLAB), (lx - 10, y + SLAB)], conc)
        if f == len(FLOORS) - 1:
            fill_poly(ctx, [(lx + LANDING_W, y), (lx + LANDING_W + 600, y), (lx + LANDING_W + 600, y + SLAB),
                            (lx + LANDING_W, y + SLAB)], conc)
            continue
        pts = [(lx + LANDING_W, y)]
        for k in range(1, STEPS + 1):
            x0 = lx + LANDING_W + (k - 1) * STEP_W
            pts.append((x0, y - k * STEP_H))
            pts.append((x0 + STEP_W, y - k * STEP_H))
        pts.append((lx + FLOOR_W, y - FH + SLAB))
        pts.append((lx + LANDING_W, y + SLAB))
        fill_poly(ctx, pts, conc)
        line(ctx, lx + LANDING_W, y + SLAB, lx + FLOOR_W, y - FH + SLAB, 4, (0.2, 0.2, 0.22))
        # barandal
        line(ctx, lx + LANDING_W, y - 100, lx + FLOOR_W, y - FH - 100, 7, (0.55, 0.12, 0.1))
        for k in range(0, STEPS + 1, 3):
            px = lx + LANDING_W + k * STEP_W
            py = y - k * STEP_H
            line(ctx, px + 10, py, px + 10, py - 100, 4, (0.4, 0.1, 0.08))
    m = ctx.get_matrix()
    ctx.restore()
    return m


def lamp_positions():
    return [(landing_x(f) + 65, -f * FH - 318) for f in range(len(FLOORS))]


def exit_glow(ctx, m, k):
    if k <= 0:
        return
    ctx.save()
    ctx.set_matrix(m)
    lx, y = landing_x(len(FLOORS) - 1), -(len(FLOORS) - 1) * FH
    ctx.rectangle(lx + 342, y - 288, 106 * k, 288)
    src(ctx, (0.85, 0.9, 1.0))
    ctx.fill()
    glow(ctx, lx + 395, y - 150, 500 * k, (0.7, 0.8, 1.0), 0.8 * k)
    ctx.restore()
