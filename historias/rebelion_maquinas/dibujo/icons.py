"""Íconos de línea: opciones (elevador, escalera, ducto) y objetos (mochila, radio)."""
import cairo
from motor.config import RED
from motor.primitives import rrect, src, line, circle, fill_poly


def icon(ctx, kind, cx, cy, a, accent=RED, color=(1, 1, 1)):
    c = color
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    if kind == "elevator":
        rrect(ctx, cx - 62, cy - 78, 124, 160, 8)
        ctx.set_line_width(8)
        src(ctx, c, a)
        ctx.stroke()
        line(ctx, cx, cy - 74, cx, cy + 78, 6, c, a)
        fill_poly(ctx, [(cx - 34, cy - 100), (cx - 16, cy - 124), (cx + 2, cy - 100)], accent, a)
        fill_poly(ctx, [(cx + 14, cy - 124), (cx + 50, cy - 124), (cx + 32, cy - 100)], c, a * 0.5)
    elif kind == "stairs":
        ctx.set_line_width(8)
        src(ctx, c, a)
        x, y = cx - 90, cy + 80
        ctx.move_to(x, y)
        for _ in range(4):
            y -= 40
            ctx.line_to(x, y)
            x += 45
            ctx.line_to(x, y)
        ctx.stroke()
        line(ctx, cx - 40, cy - 30, cx + 40, cy - 110, 8, accent, a)
        fill_poly(ctx, [(cx + 52, cy - 122), (cx + 16, cy - 116), (cx + 46, cy - 86)], accent, a)
    elif kind == "vent":
        rrect(ctx, cx - 80, cy - 80, 160, 160, 14)
        ctx.set_line_width(8)
        src(ctx, c, a)
        ctx.stroke()
        for i in range(5):
            yy = cy - 48 + i * 24
            line(ctx, cx - 52, yy, cx + 52, yy, 7, c, a * 0.85)
        for bx, by in ((-62, -62), (62, -62), (-62, 62), (62, 62)):
            circle(ctx, cx + bx, cy + by, 5, c, a)
        line(ctx, cx + 100, cy + 40, cx + 150, cy + 40, 8, accent, a)
        fill_poly(ctx, [(cx + 96, cy + 22), (cx + 70, cy + 40), (cx + 96, cy + 58)], accent, a)
    elif kind == "backpack":
        rrect(ctx, cx - 60, cy - 70, 120, 150, 30)
        ctx.set_line_width(8)
        src(ctx, c, a)
        ctx.stroke()
        rrect(ctx, cx - 38, cy + 10, 76, 46, 10)
        ctx.stroke()
        ctx.arc(cx, cy - 70, 26, 3.14159, 0)
        ctx.stroke()
    elif kind == "radio":
        rrect(ctx, cx - 48, cy - 60, 96, 140, 16)
        ctx.set_line_width(8)
        src(ctx, c, a)
        ctx.stroke()
        line(ctx, cx + 26, cy - 60, cx + 26, cy - 120, 8, c, a)
        for i in range(4):
            line(ctx, cx - 26, cy - 30 + i * 16, cx + 26, cy - 30 + i * 16, 6, c, a * 0.8)
        circle(ctx, cx, cy + 50, 9, accent, a)


def cross_out(ctx, cx, cy, r, rgb, a):
    line(ctx, cx - r, cy - r, cx + r, cy + r, 10, rgb, a)
