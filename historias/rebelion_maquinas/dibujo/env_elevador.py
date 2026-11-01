"""Elevador de carga: pasillo con puertas y el cubo (vista en corte) con la cabina."""
import math
import cairo
from motor.config import W, H, FONT_MONO
from motor.primitives import (
    rrect, src, fill_rrect, fill_poly, line, circle, glow, font, text_center, clamp, TAU, mix,
)

FLOOR_Y = 830
OPEN_X0, OPEN_X1, OPEN_Y0 = 740, 1180, 300
MID = (OPEN_X0 + OPEN_X1) / 2
PANEL_W = (OPEN_X1 - OPEN_X0) / 2


def concrete_wall(ctx, top=(0.10, 0.115, 0.14), bottom=(0.19, 0.2, 0.23)):
    g = cairo.LinearGradient(0, 0, 0, FLOOR_Y)
    g.add_color_stop_rgb(0, *top)
    g.add_color_stop_rgb(1, *bottom)
    ctx.set_source(g)
    ctx.rectangle(-300, -300, W + 600, FLOOR_Y + 300)
    ctx.fill()
    for x in range(-160, W + 300, 320):
        line(ctx, x, 0, x, FLOOR_Y, 3, (0, 0, 0), 0.25, cairo.LINE_CAP_BUTT)
    g = cairo.LinearGradient(0, FLOOR_Y, 0, H)
    g.add_color_stop_rgb(0, 0.12, 0.125, 0.14)
    g.add_color_stop_rgb(1, 0.05, 0.055, 0.065)
    ctx.set_source(g)
    ctx.rectangle(-300, FLOOR_Y, W + 600, H - FLOOR_Y + 300)
    ctx.fill()
    ctx.rectangle(-300, FLOOR_Y - 14, W + 600, 14)
    src(ctx, (0.07, 0.075, 0.085))
    ctx.fill()


def hazard_band(ctx, x, y, w, h, n=None):
    ctx.save()
    ctx.rectangle(x, y, w, h)
    ctx.clip()
    src(ctx, (0.95, 0.75, 0.1))
    ctx.paint()
    step = h * 1.4
    i = 0
    xx = x - h
    while xx < x + w + h:
        fill_poly(ctx, [(xx, y + h), (xx + step / 2, y + h), (xx + step / 2 + h, y), (xx + h, y)], (0.08, 0.08, 0.08))
        xx += step
        i += 1
    ctx.restore()


def cabin_interior(ctx, x0, y0, x1, y1, light=1.0):
    """Interior cálido de la cabina (luz blanca sospechosamente acogedora)."""
    warm_top = mix((0.05, 0.05, 0.07), (0.98, 0.93, 0.82), light)
    warm_bot = mix((0.03, 0.03, 0.04), (0.78, 0.72, 0.6), light)
    g = cairo.LinearGradient(0, y0, 0, y1)
    g.add_color_stop_rgb(0, *warm_top)
    g.add_color_stop_rgb(1, *warm_bot)
    ctx.set_source(g)
    ctx.rectangle(x0, y0, x1 - x0, y1 - y0)
    ctx.fill()
    inset = 60
    side = mix((0.02, 0.02, 0.03), (0.66, 0.6, 0.5), light)
    fill_poly(ctx, [(x0, y0), (x0 + inset, y0 + inset), (x0 + inset, y1 - inset * 0.6), (x0, y1)], side)
    fill_poly(ctx, [(x1, y0), (x1 - inset, y0 + inset), (x1 - inset, y1 - inset * 0.6), (x1, y1)], side)
    fill_poly(ctx, [(x0, y1), (x1, y1), (x1 - inset, y1 - inset * 0.6), (x0 + inset, y1 - inset * 0.6)],
              mix((0.02, 0.02, 0.02), (0.55, 0.5, 0.42), light))
    line(ctx, x0 + inset, y0 + (y1 - y0) * 0.55, x1 - inset, y0 + (y1 - y0) * 0.55, 8,
         mix((0.1, 0.1, 0.1), (0.6, 0.6, 0.62), light))
    fill_rrect(ctx, (x0 + x1) / 2 - 110, y0 + 14, 220, 18, 6, mix((0.1, 0.1, 0.1), (1, 1, 0.95), light))


def door_panel(ctx, x, y, w, h):
    g = cairo.LinearGradient(x, 0, x + w, 0)
    g.add_color_stop_rgb(0, 0.46, 0.48, 0.5)
    g.add_color_stop_rgb(1, 0.38, 0.4, 0.42)
    ctx.set_source(g)
    ctx.rectangle(x, y, w, h)
    ctx.fill()
    for i in range(1, 6):
        yy = y + h * i / 6
        line(ctx, x + 8, yy, x + w - 8, yy, 3, (0.25, 0.27, 0.29), 0.8, cairo.LINE_CAP_BUTT)


def digits(ctx, text, cx, cy, size, rgb, a=1.0):
    font(ctx, size, FONT_MONO, bold=True)
    src(ctx, rgb, a)
    text_center(ctx, text, cx, cy + size * 0.36)
    glow(ctx, cx, cy, size * 1.4, rgb, 0.35 * a)


def elevator_hall(ctx, t, open_k, floor_text, arrow_on, button_on, draw_inside):
    """open_k: 0 cerrado .. 1 abierto. draw_inside(ctx) dibuja lo que está dentro de la cabina."""
    concrete_wall(ctx)
    font(ctx, 64, "Inter Display Black")
    src(ctx, (0.85, 0.66, 0.14), 0.6)
    text_center(ctx, "MONTACARGAS", 960, 150, 8)
    # marco
    fill_rrect(ctx, OPEN_X0 - 44, OPEN_Y0 - 50, (OPEN_X1 - OPEN_X0) + 88, FLOOR_Y - OPEN_Y0 + 50, 6, (0.3, 0.32, 0.34))
    hazard_band(ctx, OPEN_X0 - 44, OPEN_Y0 - 50, (OPEN_X1 - OPEN_X0) + 88, 34)
    cabin_interior(ctx, OPEN_X0, OPEN_Y0, OPEN_X1, FLOOR_Y)
    draw_inside(ctx)
    # puertas
    ctx.save()
    ctx.rectangle(OPEN_X0, OPEN_Y0, OPEN_X1 - OPEN_X0, FLOOR_Y - OPEN_Y0)
    ctx.clip()
    off = PANEL_W * open_k
    door_panel(ctx, OPEN_X0 - off, OPEN_Y0, PANEL_W, FLOOR_Y - OPEN_Y0)
    door_panel(ctx, MID + off, OPEN_Y0, PANEL_W, FLOOR_Y - OPEN_Y0)
    ctx.rectangle(MID - off - 12, OPEN_Y0, 12, FLOOR_Y - OPEN_Y0)
    ctx.rectangle(MID + off, OPEN_Y0, 12, FLOOR_Y - OPEN_Y0)
    src(ctx, (0.08, 0.08, 0.09))
    ctx.fill()
    ctx.restore()
    # indicador de piso
    fill_rrect(ctx, MID - 90, 196, 180, 66, 8, (0.04, 0.04, 0.05))
    digits(ctx, floor_text, MID + 20, 229, 46, (1.0, 0.25, 0.18))
    if arrow_on:
        fill_poly(ctx, [(MID - 66, 244), (MID - 48, 214), (MID - 30, 244)], (1.0, 0.25, 0.18))
    # botonera
    fill_rrect(ctx, 1262, 520, 70, 130, 8, (0.42, 0.44, 0.46))
    circle(ctx, 1297, 560, 16, (1, 0.8, 0.2) if button_on else (0.2, 0.2, 0.2))
    if button_on:
        glow(ctx, 1297, 560, 50, (1, 0.8, 0.2), 0.6)
    circle(ctx, 1297, 612, 16, (0.2, 0.2, 0.2))


def light_spill(ctx, open_k):
    if open_k <= 0:
        return
    half = PANEL_W * open_k
    g = cairo.LinearGradient(0, FLOOR_Y, 0, H)
    g.add_color_stop_rgba(0, 1.0, 0.9, 0.7, 0.32 * open_k)
    g.add_color_stop_rgba(1, 1.0, 0.9, 0.7, 0.0)
    ctx.save()
    ctx.set_operator(cairo.OPERATOR_ADD)
    ctx.move_to(MID - half, FLOOR_Y)
    ctx.line_to(MID + half, FLOOR_Y)
    ctx.line_to(MID + half * 1.9, H)
    ctx.line_to(MID - half * 1.9, H)
    ctx.close_path()
    ctx.set_source(g)
    ctx.fill()
    ctx.restore()


# ---------- cubo del elevador ----------
CAB_X0, CAB_X1, CAB_Y0, CAB_Y1 = 600, 1320, 250, 860
SLAB_GAP = 700
FLOOR_NAMES = {-2: "-3", -1: "-2", 0: "-1", 1: "PB", 2: "1"}


def shaft(ctx, offset):
    """Paredes del cubo; offset = cuánto ha subido la cabina (las losas bajan)."""
    g = cairo.LinearGradient(0, 0, W, 0)
    g.add_color_stop_rgb(0, 0.05, 0.055, 0.07)
    g.add_color_stop_rgb(0.5, 0.11, 0.12, 0.14)
    g.add_color_stop_rgb(1, 0.05, 0.055, 0.07)
    ctx.set_source(g)
    ctx.rectangle(-300, -300, W + 600, H + 600)
    ctx.fill()
    for x in (520, 1400):
        ctx.rectangle(x - 14, -300, 28, H + 600)
        src(ctx, (0.22, 0.24, 0.26))
        ctx.fill()
        for k in range(-3, 10):
            yy = (k * 180 + offset) % (H + 360) - 180
            fill_rrect(ctx, x - 20, yy, 40, 14, 3, (0.3, 0.32, 0.34))
    for k in range(-3, 4):
        y = 560 - k * SLAB_GAP + (offset - 1050)
        if -200 < y < H + 200:
            ctx.rectangle(-300, y, W + 600, 70)
            src(ctx, (0.2, 0.21, 0.22))
            ctx.fill()
            hazard_band(ctx, -300, y, W + 600, 14)
            name = FLOOR_NAMES.get(k)
            if name:
                font(ctx, 110, "Inter Display Black")
                src(ctx, (0.85, 0.66, 0.14), 0.55)
                text_center(ctx, name, 260, y - 40)
                text_center(ctx, name, 1660, y - 40)


def cabin(ctx, x_off, y_off, light, speaker_k, floor_text, cables_broken, t, draw_person):
    ctx.save()
    ctx.translate(x_off, y_off)
    # cables
    for i, cx in enumerate((900, 960, 1020)):
        if cables_broken > 0 and i == 1:
            ang = cables_broken * 1.4
            ln = 500
            line(ctx, cx, CAB_Y0 - 400, cx + math.sin(ang) * ln * 0.4, CAB_Y0 - 400 + math.cos(ang) * 120, 6, (0.35, 0.36, 0.38))
            continue
        if cables_broken >= 1 and i != 1:
            line(ctx, cx, CAB_Y0 - 20, cx + (i - 1) * 40, CAB_Y0 - 180, 6, (0.35, 0.36, 0.38))
            continue
        line(ctx, cx, CAB_Y0 - 20, cx, -1200, 6, (0.35, 0.36, 0.38), 1.0, cairo.LINE_CAP_BUTT)
    fill_rrect(ctx, 880, CAB_Y0 - 40, 160, 40, 6, (0.25, 0.26, 0.28))
    # caja
    fill_rrect(ctx, CAB_X0 - 30, CAB_Y0 - 20, CAB_X1 - CAB_X0 + 60, CAB_Y1 - CAB_Y0 + 50, 10, (0.3, 0.32, 0.34))
    cabin_interior(ctx, CAB_X0, CAB_Y0, CAB_X1, CAB_Y1, light)
    draw_person(ctx)
    # oscuridad dentro cuando se apaga la luz
    # bocina en el techo
    sx, sy = CAB_X0 + 120, CAB_Y0 + 40
    circle(ctx, sx, sy, 26, (0.15, 0.15, 0.17))
    for i in range(-2, 3):
        line(ctx, sx - 14, sy + i * 7, sx + 14, sy + i * 7, 2, (0.05, 0.05, 0.05))
    if speaker_k > 0:
        glow(ctx, sx, sy, 120, (0.85, 0.92, 1.0), 0.7 * speaker_k)
        for k in range(3):
            r = 34 + k * 22 + speaker_k * 6
            ctx.set_line_width(3)
            src(ctx, (0.85, 0.92, 1.0), 0.35 * speaker_k / (k + 1))
            ctx.arc(sx, sy, r, -0.9, 0.9)
            ctx.stroke()
    # indicador
    fill_rrect(ctx, 900, CAB_Y0 + 60, 120, 50, 6, (0.04, 0.04, 0.05))
    digits(ctx, floor_text, 960, CAB_Y0 + 85, 34, (1.0, 0.25, 0.18))
    # suelo de la cabina
    ctx.rectangle(CAB_X0 - 30, CAB_Y1, CAB_X1 - CAB_X0 + 60, 30)
    src(ctx, (0.2, 0.21, 0.22))
    ctx.fill()
    ctx.restore()
