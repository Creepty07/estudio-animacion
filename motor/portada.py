"""Portada (miniatura) de un video: un cuadro de una escena, sin subtítulos, con el título encima.

Uso:  python -m motor.portada <historia> <escena> <segundo_local> "LINEA 1|LINEA 2" salida.png ["KICKER"]
La imagen sale en el formato de la historia (vertical 1080×1920). El título va en la franja central (y ~ 1180-1500),
dentro del recorte 3:4 con el que TikTok muestra las portadas en la cuadrícula del perfil.
"""
import sys
import cairo
from motor import config


def portada(historia, escena, t, lineas, salida, kicker=""):
    config.load(historia)
    config.SUBTITLES = False
    from motor import render
    from motor.kit import glitch_text, fit_size
    from motor.primitives import font, text_w, text_at, src
    W, H = config.W, config.H
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    render.frame(escena, config.scene_module(escena), t, surf)
    ctx = cairo.Context(surf)
    g = cairo.LinearGradient(0, H * 0.52, 0, H * 0.86)                      # sombra para que el título se lea sobre cualquier cuadro
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(0.55, 0, 0, 0, 0.62)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.0)
    ctx.set_source(g)
    ctx.paint()
    size = min(fit_size(ctx, ln, W - 150, 128) for ln in lineas)
    y = H * 0.68 - (len(lineas) - 1) * size * 0.55
    for i, ln in enumerate(lineas):
        glitch_text(ctx, ln, W / 2, y + i * size * 1.15, size, 1.0, 0.12)
    if kicker:
        font(ctx, 40, config.FONT, bold=True)
        src(ctx, (0.78, 0.86, 1.0), 0.95)
        text_at(ctx, kicker, W / 2 - text_w(ctx, kicker, 12) / 2, y - size * 1.05, 12)
    surf.write_to_png(salida)
    return salida


if __name__ == "__main__":
    a = sys.argv
    portada(a[1], a[2], float(a[3]), a[4].split("|"), a[5], a[6] if len(a) > 6 else "")
    print(a[5])
