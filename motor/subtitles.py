"""Subtítulos de narración y diálogo (con etiqueta del personaje).

Dos estilos, elegidos por historia con SUBTITLE_STYLE en historia.py:
  - "caja" (el de siempre): cursiva sobre una caja negra translúcida.
  - "reglas": negrita blanca con contorno negro, sin caja; lo que va entre *asteriscos* sale en amarillo y las
    palabras aparecen una a una al ritmo de la voz (lo que oyes, lo ves).

Se adaptan al formato: en vertical van más arriba para no quedar debajo de los botones y la descripción de
TikTok (zona segura).
"""
import re
from motor import config
from motor.primitives import font, text_w, text_at, wrap, fill_rrect, src, window, clamp

AMARILLO = (1.0, 0.82, 0.16)


def _style():
    W, H = config.W, config.H
    if config.SUBTITLE_STYLE == "reglas":
        if W < H:
            return {"size": 62, "line_h": 80, "max_w": W - 170, "bottom": int(H * 0.765), "pad_x": 0, "pad_y": 0, "contorno": 11}
        return {"size": 50, "line_h": 66, "max_w": 1500, "bottom": H - 60, "pad_x": 0, "pad_y": 0, "contorno": 9}
    if W < H:   # vertical
        return {"size": 54, "line_h": 70, "max_w": W - 200, "bottom": int(H * 0.75), "pad_x": 34, "pad_y": 24}
    return {"size": 44, "line_h": 58, "max_w": 1400, "bottom": H - 56, "pad_x": 38, "pad_y": 22}


def _tokens(text):
    """Texto con *marcas* -> lista de palabras; cada palabra es una lista de (trozo, resaltado)."""
    tokens, cur = [], []
    for i, parte in enumerate(text.split("*")):
        resaltado = i % 2 == 1
        for m in re.finditer(r"\s+|\S+", parte):
            s = m.group()
            if s.isspace():
                if cur:
                    tokens.append(cur)
                    cur = []
            else:
                cur.append((s, resaltado))
    if cur:
        tokens.append(cur)
    return tokens


def _ancho(ctx, token):
    return sum(text_w(ctx, s) for s, _ in token)


def _lineas(ctx, tokens, max_w):
    """Reparte las palabras en renglones que caben en max_w. Devuelve listas de índices de palabra."""
    esp = text_w(ctx, " ")
    lineas, cur, w = [], [], 0.0
    for i, tk in enumerate(tokens):
        tw = _ancho(ctx, tk)
        if cur and w + esp + tw > max_w:
            lineas.append(cur)
            cur, w = [], 0.0
        w += (esp if cur else 0) + tw
        cur.append(i)
    if cur:
        lineas.append(cur)
    return lineas


def _etiqueta(ctx, speaker, x0, y0, alpha, st, rgb):
    font(ctx, int(st["size"] * 0.6), config.FONT, bold=True)
    tag_w = text_w(ctx, speaker, 4) + 28
    fill_rrect(ctx, x0, y0 - 46, tag_w, 38, 10, (0.0, 0.0, 0.0), 0.7 * alpha)
    src(ctx, rgb, alpha)
    text_at(ctx, speaker, x0 + 14, y0 - 18, 4)


def _draw_reglas(ctx, text, alpha, speaker, prog, speaker_rgb):
    st = _style()
    W = config.W
    font(ctx, st["size"], config.FONT, bold=True)
    tokens = _tokens(text)
    lineas = _lineas(ctx, tokens, st["max_w"])
    esp = text_w(ctx, " ")
    total = sum(sum(len(s) for s, _ in tk) for tk in tokens) or 1
    y_top = st["bottom"] - st["line_h"] * len(lineas)
    if speaker:
        ancho_max = max(sum(_ancho(ctx, tokens[i]) for i in ln) + esp * (len(ln) - 1) for ln in lineas)
        _etiqueta(ctx, speaker, (W - ancho_max) / 2, y_top + 8, alpha, st, speaker_rgb)
        font(ctx, st["size"], config.FONT, bold=True)
    vistos = 0.0                                              # letras que ya "pasaron" para decidir qué palabras se ven
    ctx.set_line_join(1)                                      # LINE_JOIN_ROUND
    for r, ln in enumerate(lineas):
        ancho = sum(_ancho(ctx, tokens[i]) for i in ln) + esp * (len(ln) - 1)
        x = (W - ancho) / 2
        y = y_top + st["line_h"] * (r + 1) - 18
        for i in ln:
            tk = tokens[i]
            visible = prog is None or vistos / total <= prog + 1e-6
            vistos += sum(len(s) for s, _ in tk)
            tw = _ancho(ctx, tk)
            if visible:
                cx = x
                for s, hl in tk:
                    ctx.move_to(cx, y)
                    ctx.text_path(s)
                    ctx.set_line_width(st["contorno"])
                    src(ctx, (0.0, 0.0, 0.0), 0.95 * alpha)
                    ctx.stroke_preserve()
                    src(ctx, AMARILLO if (hl and not speaker) else (1, 1, 1), alpha)
                    ctx.fill()
                    cx += text_w(ctx, s)
            x += tw + esp


def draw_subtitle(ctx, text, alpha, speaker=None, speaker_rgb=(0.55, 0.85, 1.0), prog=None):
    if alpha <= 0:
        return
    ctx.save()
    ctx.identity_matrix()
    if config.SUBTITLE_STYLE == "reglas":
        _draw_reglas(ctx, text, alpha, speaker, prog, speaker_rgb)
        ctx.restore()
        return
    st = _style()
    W = config.W
    font(ctx, st["size"], config.FONT, italic=speaker is None, bold=speaker is not None)
    lines = wrap(ctx, text, st["max_w"])
    box_w = max(text_w(ctx, ln) for ln in lines) + st["pad_x"] * 2
    box_h = st["line_h"] * len(lines) + st["pad_y"] * 2 - 12
    x0 = (W - box_w) / 2
    y0 = st["bottom"] - box_h
    fill_rrect(ctx, x0, y0, box_w, box_h, 14, (0.0, 0.0, 0.0), 0.62 * alpha)

    if speaker:
        _etiqueta(ctx, speaker, x0, y0, alpha, st, speaker_rgb)
        font(ctx, st["size"], config.FONT, bold=True)

    src(ctx, (1, 1, 1), alpha)
    for i, ln in enumerate(lines):
        lw = text_w(ctx, ln)
        text_at(ctx, ln, (W - lw) / 2, y0 + st["pad_y"] + st["size"] * 0.86 + i * st["line_h"])
    ctx.restore()


def draw_subs(ctx, t, subs):
    """subs: lista de (inicio, fin, texto, hablante|None)."""
    reglas = config.SUBTITLE_STYLE == "reglas"
    for start, end, text, speaker in subs:
        a = window(t, start, end, 0.08 if reglas else 0.2)
        if a > 0:
            prog = clamp((t - start) / max(0.4, 0.8 * (end - start))) if reglas else None
            draw_subtitle(ctx, text, a, speaker, prog=prog)
