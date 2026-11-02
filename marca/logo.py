"""Logo del perfil: Relatos en Penumbra. Una vela en la oscuridad con niebla (1080×1080, se recorta en círculo).

Uso:  python marca/logo.py            -> marca/logo_relatos_en_penumbra.png
Diseño propio, hecho con código. Todo lo importante queda dentro del círculo central.
"""
import math
import random
import sys
from pathlib import Path
import cairo

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from motor import config                       # noqa: E402
from motor.primitives import glow, src, circle   # noqa: E402
from motor.kit import fog                      # noqa: E402

S = 1080


def dibujar(salida):
    config.W = config.H = S
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, S, S)
    ctx = cairo.Context(surf)
    g = cairo.RadialGradient(S / 2, S * 0.46, 40, S / 2, S / 2, S * 0.78)          # fondo: azul noche casi negro
    g.add_color_stop_rgb(0, 0.06, 0.10, 0.15)
    g.add_color_stop_rgb(0.6, 0.02, 0.035, 0.06)
    g.add_color_stop_rgb(1, 0.0, 0.005, 0.015)
    ctx.set_source(g)
    ctx.paint()
    r = random.Random(3)
    for _ in range(70):                                                              # estrellas
        circle(ctx, r.uniform(0, S), r.uniform(0, S * 0.7), r.uniform(0.8, 2.2), (0.8, 0.88, 1.0), r.uniform(0.2, 0.8))
    glow(ctx, S / 2, S * 0.44, 430, (1.0, 0.55, 0.15), 0.38)                          # halo cálido
    glow(ctx, S / 2, S * 0.44, 190, (1.0, 0.75, 0.35), 0.45)
    fog(ctx, 4.0, rgb=(0.55, 0.70, 0.85), alpha=0.16, y0=S * 0.55, y1=S * 0.95, seed=5)   # niebla fría al pie
    # plato de piedra
    ctx.save()
    ctx.translate(S / 2, S * 0.755)
    ctx.scale(1, 0.24)
    ctx.arc(0, 0, 250, 0, 2 * math.pi)
    src(ctx, (0.10, 0.12, 0.16))
    ctx.fill()
    ctx.restore()
    ctx.save()
    ctx.translate(S / 2, S * 0.745)
    ctx.scale(1, 0.22)
    ctx.arc(0, 0, 232, 0, 2 * math.pi)
    src(ctx, (0.22, 0.25, 0.31))
    ctx.fill()
    ctx.restore()
    # cuerpo de la vela con degradado y goteo
    x0, x1, yb, yt = S / 2 - 62, S / 2 + 62, S * 0.745, S * 0.50
    cg = cairo.LinearGradient(x0, 0, x1, 0)
    cg.add_color_stop_rgb(0, 0.62, 0.56, 0.46)
    cg.add_color_stop_rgb(0.35, 0.95, 0.90, 0.78)
    cg.add_color_stop_rgb(1, 0.45, 0.40, 0.34)
    ctx.set_source(cg)
    ctx.rectangle(x0, yt, x1 - x0, yb - yt)
    ctx.fill()
    ctx.save()
    ctx.translate(S / 2, yt)
    ctx.scale(1, 0.2)
    ctx.arc(0, 0, 62, 0, 2 * math.pi)
    src(ctx, (0.98, 0.94, 0.84))
    ctx.fill()
    ctx.restore()
    for dx, ln in ((-34, 80), (18, 120), (46, 50)):                                    # gotas de cera
        ctx.move_to(S / 2 + dx - 9, yt + 4)
        ctx.line_to(S / 2 + dx + 9, yt + 4)
        ctx.line_to(S / 2 + dx + 9, yt + ln)
        ctx.arc(S / 2 + dx, yt + ln, 9, 0, math.pi)
        ctx.close_path()
        src(ctx, (1.0, 0.97, 0.88), 0.75)
        ctx.fill()
    ctx.set_line_width(5)                                                              # pabilo
    src(ctx, (0.1, 0.07, 0.05))
    ctx.move_to(S / 2, yt)
    ctx.curve_to(S / 2 + 3, yt - 16, S / 2 - 2, yt - 26, S / 2 + 4, yt - 34)
    ctx.stroke()
    # llama: capas de afuera hacia adentro
    fx, fy = S / 2 + 4, yt - 28
    for escala, col, a in ((1.0, (1.0, 0.42, 0.08), 0.95), (0.78, (1.0, 0.68, 0.18), 1.0), (0.5, (1.0, 0.92, 0.6), 1.0), (0.26, (1.0, 1.0, 0.95), 1.0)):
        h = 175 * escala
        w = 52 * escala
        ctx.move_to(fx, fy - h)
        ctx.curve_to(fx + w * 1.1, fy - h * 0.45, fx + w, fy - h * 0.08, fx, fy)
        ctx.curve_to(fx - w, fy - h * 0.08, fx - w * 1.1, fy - h * 0.45, fx, fy - h)
        src(ctx, col, a)
        ctx.fill()
    glow(ctx, fx, fy - 70, 150, (1.0, 0.7, 0.3), 0.5)
    fog(ctx, 9.0, rgb=(0.6, 0.74, 0.9), alpha=0.12, y0=S * 0.70, y1=S * 0.98, seed=8)  # niebla por delante
    v = cairo.RadialGradient(S / 2, S / 2, S * 0.38, S / 2, S / 2, S * 0.72)           # viñeta
    v.add_color_stop_rgba(0, 0, 0, 0, 0)
    v.add_color_stop_rgba(1, 0, 0, 0, 0.7)
    ctx.set_source(v)
    ctx.paint()
    surf.write_to_png(str(salida))


if __name__ == "__main__":
    out = ROOT / "marca" / "logo_relatos_en_penumbra.png"
    dibujar(out)
    print(out)
