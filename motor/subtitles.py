"""Subtítulos de narración (cursiva) y diálogo (con etiqueta del personaje).

Se adaptan al formato: en vertical van más arriba para no quedar debajo de los
botones y la descripción de TikTok (zona segura).
"""
from motor import config
from motor.primitives import font, text_w, text_at, wrap, fill_rrect, src, window


def _style():
    W, H = config.W, config.H
    if W < H:   # vertical
        return {"size": 54, "line_h": 70, "max_w": W - 200, "bottom": int(H * 0.75), "pad_x": 34, "pad_y": 24}
    return {"size": 44, "line_h": 58, "max_w": 1400, "bottom": H - 56, "pad_x": 38, "pad_y": 22}


def draw_subtitle(ctx, text, alpha, speaker=None, speaker_rgb=(0.55, 0.85, 1.0)):
    if alpha <= 0:
        return
    st = _style()
    W = config.W
    ctx.save()
    ctx.identity_matrix()
    font(ctx, st["size"], config.FONT, italic=speaker is None, bold=speaker is not None)
    lines = wrap(ctx, text, st["max_w"])
    box_w = max(text_w(ctx, ln) for ln in lines) + st["pad_x"] * 2
    box_h = st["line_h"] * len(lines) + st["pad_y"] * 2 - 12
    x0 = (W - box_w) / 2
    y0 = st["bottom"] - box_h
    fill_rrect(ctx, x0, y0, box_w, box_h, 14, (0.0, 0.0, 0.0), 0.62 * alpha)

    if speaker:
        font(ctx, int(st["size"] * 0.6), config.FONT, bold=True)
        tag_w = text_w(ctx, speaker, 4) + 28
        fill_rrect(ctx, x0, y0 - 46, tag_w, 38, 10, (0.0, 0.0, 0.0), 0.7 * alpha)
        src(ctx, speaker_rgb, alpha)
        text_at(ctx, speaker, x0 + 14, y0 - 18, 4)
        font(ctx, st["size"], config.FONT, bold=True)

    src(ctx, (1, 1, 1), alpha)
    for i, ln in enumerate(lines):
        lw = text_w(ctx, ln)
        text_at(ctx, ln, (W - lw) / 2, y0 + st["pad_y"] + st["size"] * 0.86 + i * st["line_h"])
    ctx.restore()


def draw_subs(ctx, t, subs):
    """subs: lista de (inicio, fin, texto, hablante|None)."""
    for start, end, text, speaker in subs:
        a = window(t, start, end, 0.2)
        if a > 0:
            draw_subtitle(ctx, text, a, speaker)
