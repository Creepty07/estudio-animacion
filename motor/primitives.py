"""Primitivas de dibujo y animación compartidas por todas las escenas."""
import math
import cairo
from motor import config

TAU = math.tau


# ---------- tiempo y easing ----------
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def lerp(a, b, t):
    return a + (b - a) * t


def seg(t, a, b):
    """Progreso 0..1 de t dentro del intervalo [a, b]."""
    if b == a:
        return 1.0 if t >= b else 0.0
    return clamp((t - a) / (b - a))


def smooth(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_in(x):
    x = clamp(x)
    return x ** 3


def mix(c1, c2, t):
    return tuple(lerp(a, b, t) for a, b in zip(c1, c2))


def window(t, a, b, fade=0.25):
    """Opacidad de algo visible entre a y b, con fundidos de entrada y salida."""
    if t < a or t > b:
        return 0.0
    return min(seg(t, a, a + fade), 1 - seg(t, b - fade, b))


# ---------- formas ----------
def rrect(ctx, x, y, w, h, r):
    r = max(0.0, min(r, w / 2, h / 2))
    ctx.new_sub_path()
    ctx.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    ctx.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    ctx.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    ctx.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    ctx.close_path()


def src(ctx, c, a=1.0):
    if len(c) == 4:
        ctx.set_source_rgba(*c)
    else:
        ctx.set_source_rgba(c[0], c[1], c[2], a)


def fill_rrect(ctx, x, y, w, h, r, c, a=1.0):
    rrect(ctx, x, y, w, h, r)
    src(ctx, c, a)
    ctx.fill()


def poly(ctx, pts):
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ctx.close_path()


def fill_poly(ctx, pts, c, a=1.0):
    poly(ctx, pts)
    src(ctx, c, a)
    ctx.fill()


def line(ctx, x0, y0, x1, y1, w, c, a=1.0, cap=cairo.LINE_CAP_ROUND):
    ctx.set_line_cap(cap)
    ctx.set_line_width(w)
    src(ctx, c, a)
    ctx.move_to(x0, y0)
    ctx.line_to(x1, y1)
    ctx.stroke()


def circle(ctx, x, y, r, c, a=1.0):
    ctx.arc(x, y, r, 0, TAU)
    src(ctx, c, a)
    ctx.fill()


# ---------- luz ----------
def glow(ctx, x, y, r, rgb, alpha=1.0, op=cairo.OPERATOR_ADD):
    if alpha <= 0 or r <= 0:
        return
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, *rgb, alpha)
    g.add_color_stop_rgba(0.3, *rgb, alpha * 0.4)
    g.add_color_stop_rgba(1, *rgb, 0)
    ctx.save()
    ctx.set_operator(op)
    ctx.set_source(g)
    ctx.arc(x, y, r, 0, TAU)
    ctx.fill()
    ctx.restore()


def fill_screen(ctx, rgb, alpha=1.0, op=cairo.OPERATOR_OVER):
    if alpha <= 0:
        return
    ctx.save()
    ctx.identity_matrix()
    ctx.set_operator(op)
    ctx.set_source_rgba(rgb[0], rgb[1], rgb[2], alpha)
    ctx.rectangle(0, 0, config.W, config.H)
    ctx.fill()
    ctx.restore()


def tint(ctx, rgb, strength=1.0):
    """Multiplica toda la imagen por un color (luz de color)."""
    if strength <= 0:
        return
    fill_screen(ctx, mix((1, 1, 1), rgb, strength), 1.0, cairo.OPERATOR_MULTIPLY)


def darken(ctx, alpha):
    fill_screen(ctx, (0, 0, 0), alpha)


def vignette(ctx, strength=0.65):
    ctx.save()
    ctx.identity_matrix()
    W, H = config.W, config.H
    if W >= H:
        g = cairo.RadialGradient(W / 2, H / 2, H * 0.35, W / 2, H / 2, W * 0.62)
    else:
        g = cairo.RadialGradient(W / 2, H / 2, W * 0.45, W / 2, H / 2, H * 0.62)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, strength)
    ctx.set_source(g)
    ctx.rectangle(0, 0, config.W, config.H)
    ctx.fill()
    ctx.restore()


def camera(ctx, scale, fx, fy, dx=0.0, dy=0.0):
    """Zoom alrededor del punto (fx, fy) más un desplazamiento (temblor)."""
    ctx.translate(fx + dx, fy + dy)
    ctx.scale(scale, scale)
    ctx.translate(-fx, -fy)


# ---------- texto ----------
def font(ctx, size, family=None, bold=False, italic=False):
    ctx.select_font_face(
        family or config.FONT,
        cairo.FONT_SLANT_ITALIC if italic else cairo.FONT_SLANT_NORMAL,
        cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL,
    )
    ctx.set_font_size(size)


def text_w(ctx, s, spacing=0.0):
    if spacing == 0:
        return ctx.text_extents(s).x_advance
    return sum(ctx.text_extents(ch).x_advance for ch in s) + spacing * (len(s) - 1)


def text_at(ctx, s, x, y, spacing=0.0):
    if spacing == 0:
        ctx.move_to(x, y)
        ctx.show_text(s)
        return
    for ch in s:
        ctx.move_to(x, y)
        ctx.show_text(ch)
        x += ctx.text_extents(ch).x_advance + spacing


def text_center(ctx, s, cx, y, spacing=0.0):
    text_at(ctx, s, cx - text_w(ctx, s, spacing) / 2, y, spacing)


def wrap(ctx, text, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if text_w(ctx, trial) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines
