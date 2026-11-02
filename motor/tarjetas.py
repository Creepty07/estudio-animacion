"""Tarjetas verticales para historias interactivas: pantalla de elección (3 opciones apiladas) y tarjeta de final.

Todo se calcula con config.W / config.H y respeta la zona segura de TikTok: pregunta y tarjetas entre y ≈ 230 y 1200,
columna derecha libre, y la banda de subtítulos (1264-1440) disponible para "Comenta 1, 2 o 3".
"""
import math
import random
from motor import config
from motor.primitives import (seg, smooth, ease_out, font, text_w, text_at, text_center, src, circle, glow, fill_rrect, rrect, line,
                              fill_screen, TAU, lerp)
from motor.kit import glitch_text, fit_size

CARD_X, CARD_W, CARD_H, CARD_GAP, CARD_Y0 = 70, 880, 220, 36, 400
RANGO_Y = (230, 1200)


def eleccion(ctx, t, pregunta, opciones, accent=(0.55, 0.96, 1.0), colores=None, t_pregunta=(0.2, 1.6), t_tarjetas=(1.8, 2.6, 3.4),
             t_fin=None, pulso=True):
    """Pregunta arriba y hasta 3 tarjetas apiladas (número grande + texto). Cada tarjeta entra en su tiempo con un golpe de luz.

    opciones: lista de textos; colores: lista de rgb por tarjeta (por defecto, accent). t_fin: desde ahí todo se desvanece.
    Devuelve los tiempos de entrada para que la mezcla los reutilice."""
    W = config.W
    colores = colores or [accent] * len(opciones)
    fade = 1.0 if t_fin is None else 1 - smooth(seg(t, t_fin - 0.3, t_fin))
    a = smooth(seg(t, t_pregunta[0], t_pregunta[0] + 0.3)) * fade
    if a > 0:
        chaos = 1 - smooth(seg(t, t_pregunta[0], t_pregunta[0] + 0.7))
        sz = fit_size(ctx, pregunta, 800, 92)
        glitch_text(ctx, pregunta, W / 2, 330, sz, a, chaos * 0.8, c1=(1, 0.2, 0.2), c2=(0.2, 1, 1))
    for i, (txt, col, t0) in enumerate(zip(opciones, colores, t_tarjetas)):
        u = seg(t, t0, t0 + 0.35)
        if u <= 0:
            continue
        k = ease_out(u)
        y = CARD_Y0 + i * (CARD_H + CARD_GAP)
        x = CARD_X - (1 - k) * 220
        golpe = max(0.0, 1 - (t - t0) / 0.5) if t >= t0 else 0.0
        al = min(1.0, u * 2) * fade
        sc = 1 + (0.04 * math.sin(t * 3.0 + i) if pulso and t > t0 + 0.6 else 0.0) * 0.5
        ctx.save()
        ctx.translate(x + CARD_W / 2, y + CARD_H / 2)
        ctx.scale(sc, sc)
        ctx.translate(-(x + CARD_W / 2), -(y + CARD_H / 2))
        if golpe > 0:
            glow(ctx, x + CARD_W / 2, y + CARD_H / 2, CARD_W * 0.7, col, 0.45 * golpe * al)
        fill_rrect(ctx, x + 6, y + 8, CARD_W, CARD_H, 36, (0, 0, 0), 0.35 * al)
        fill_rrect(ctx, x, y, CARD_W, CARD_H, 36, (0.02, 0.05, 0.07), 0.82 * al)
        rrect(ctx, x, y, CARD_W, CARD_H, 36)
        src(ctx, col, 0.14 * al)
        ctx.fill_preserve()
        ctx.set_line_width(5)
        src(ctx, col, 0.95 * al)
        ctx.stroke()
        cx, cy = x + 125, y + CARD_H / 2
        circle(ctx, cx, cy, 78, col, 0.22 * al)
        ctx.arc(cx, cy, 78, 0, TAU)
        ctx.set_line_width(5)
        src(ctx, col, al)
        ctx.stroke()
        font(ctx, 118, config.FONT_DISPLAY)
        src(ctx, (1, 1, 1), al)
        text_center(ctx, str(i + 1), cx, cy + 41)
        sz = fit_size(ctx, txt, CARD_W - 250 - 40, 58, config.FONT, 0)
        lineas = [txt]
        if sz < 50:                                                       # no cabe en una línea: se parte en dos
            words = txt.split()
            mitad = len(words) // 2
            lineas = [" ".join(words[:mitad]), " ".join(words[mitad:])]
            sz = 52
        font(ctx, sz, config.FONT, bold=True)
        src(ctx, (1, 1, 1), al)
        for j, ln in enumerate(lineas):
            text_at(ctx, ln, x + 230, cy + 20 - (len(lineas) - 1) * 34 + j * 68)
        ctx.restore()
    return t_tarjetas


def tarjeta_final(ctx, t, numero, titulo, etiqueta, accent=(0.55, 0.96, 1.0), duracion=2.5):
    """Tarjeta que abre cada final: número grande en un círculo, título del final y una etiqueta ("FINAL MALO")."""
    W, H = config.W, config.H
    fill_screen(ctx, (0.015, 0.03, 0.045))
    glow(ctx, W / 2, H * 0.40, 720, tuple(c * 0.55 for c in accent), 0.55 * smooth(seg(t, 0.0, 0.5)))
    rng = random.Random(4)
    for _ in range(26):
        x = rng.uniform(0, W)
        y = (rng.uniform(0, H) - t * rng.uniform(10, 30)) % H
        circle(ctx, x, y, rng.uniform(1.2, 2.8), accent, 0.35)
    k = ease_out(seg(t, 0.0, 0.45))
    cx, cy = W / 2, H * 0.31
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(max(0.001, k), max(0.001, k))
    circle(ctx, 0, 0, 190, accent, 0.18)
    ctx.arc(0, 0, 190, 0, TAU)
    ctx.set_line_width(9)
    src(ctx, accent, 0.95)
    ctx.stroke()
    ctx.restore()
    chaos = 1 - smooth(seg(t, 0.1, 0.9))
    glitch_text(ctx, str(numero), cx, cy + 92, 270, smooth(seg(t, 0.05, 0.25)), chaos, c1=accent, c2=(1, 1, 1), spacing=0)
    ea = smooth(seg(t, 0.35, 0.8))
    font(ctx, 44, config.FONT, bold=True)
    src(ctx, accent, ea)
    text_center(ctx, etiqueta, W / 2, H * 0.31 + 330, 12)
    lineas = titulo.split("\n")
    sz = min(fit_size(ctx, ln, W * 0.86, 108) for ln in lineas)
    for j, ln in enumerate(lineas):
        glitch_text(ctx, ln, W / 2, H * 0.31 + 450 + j * sz * 1.2, sz, smooth(seg(t, 0.4, 0.7)), chaos * 0.6, c1=(1, 0.25, 0.25), c2=(0.25, 1, 1))
    u = smooth(seg(t, 0.8, 1.4))
    line(ctx, W / 2 - 220 * u, H * 0.31 + 330 + 40, W / 2 + 220 * u, H * 0.31 + 330 + 40, 4, accent, 0.9)
