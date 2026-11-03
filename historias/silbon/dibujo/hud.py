"""Textos y marcas en pantalla del estilo "Reglas": recuadro rojo de lugar y hora, saltos de tiempo, tarjetas de regla,
cuenta regresiva y botones del dilema. Se dibujan en coordenadas de pantalla (después de la cámara)."""
import math
from motor import config
from motor.primitives import font, text_w, text_at, text_center, src, fill_rrect, rrect, seg, smooth, window, clamp
from historias.silbon.dibujo import estilo as E

Y_TOP = 250                                  # altura de los textos grandes de arriba (debajo de la barra de TikTok)


def pop(t, t0, dur=0.24):
    """Escala 0 -> 1.12 -> 1 con rebote (la entrada de un rótulo)."""
    k = seg(t, t0, t0 + dur)
    if k <= 0:
        return 0.0
    c1 = 1.9
    return 1 + (c1 + 1) * (k - 1) ** 3 + c1 * (k - 1) ** 2


def texto_contorno(ctx, s, cx, y, size, rgb=E.BLANCO, alpha=1.0, contorno=None, family=None, spacing=0.0, escala=1.0):
    """Texto centrado con contorno negro grueso (legible sobre cualquier fondo)."""
    ctx.save()
    ctx.identity_matrix()
    font(ctx, size * escala, family or config.FONT_DISPLAY, bold=True)
    w = text_w(ctx, s, spacing)
    ctx.set_line_join(1)
    x = cx - w / 2
    for ch, adv in _letras(ctx, s, spacing):
        ctx.move_to(x, y)
        ctx.text_path(ch)
        ctx.set_line_width((contorno or size * 0.16) * escala)
        src(ctx, (0, 0, 0), 0.95 * alpha)
        ctx.stroke_preserve()
        src(ctx, rgb, alpha)
        ctx.fill()
        x += adv
    ctx.restore()


def _letras(ctx, s, spacing):
    if spacing == 0:
        yield s, ctx.text_extents(s).x_advance
        return
    for ch in s:
        yield ch, ctx.text_extents(ch).x_advance + spacing


def caja_hud(ctx, texto, t, t0, t1):
    """Recuadro rojo estilo cámara de seguridad: lugar, hora y noche."""
    a = window(t, t0, t1, 0.15)
    if a <= 0:
        return
    ctx.save()
    ctx.identity_matrix()
    font(ctx, 29, config.FONT_MONO, bold=True)
    w = text_w(ctx, texto, 2) + 62
    x, y, h = 54, 168, 62
    fill_rrect(ctx, x, y, w, h, 9, (0.0, 0.0, 0.0), 0.55 * a)
    rrect(ctx, x, y, w, h, 9)
    ctx.set_line_width(4)
    src(ctx, E.ROJO, a)
    ctx.stroke()
    if int(t * 2) % 2 == 0:                                           # punto REC que parpadea
        ctx.new_path()
        ctx.arc(x + 24, y + h / 2, 7, 0, math.tau)
        src(ctx, E.ROJO, a)
        ctx.fill()
    src(ctx, (0.92, 0.92, 0.92), a)
    text_at(ctx, texto, x + 42, y + h / 2 + 10, 2)
    ctx.restore()


def etiqueta_tiempo(ctx, texto, t, t0, t1):
    """"+4 HORAS": salto de tiempo en amarillo."""
    a = window(t, t0, t1, 0.12)
    if a > 0:
        texto_contorno(ctx, texto, config.W / 2, Y_TOP, 78, E.AMARILLO, a, escala=pop(t, t0))


def tarjeta_regla(ctx, n, t, t0, t1):
    """"REGLA Nº 1": tarjeta blanca arriba al centro."""
    a = window(t, t0, t1, 0.12)
    if a > 0:
        texto_contorno(ctx, f"REGLA Nº {n}", config.W / 2, Y_TOP + 10, 92, E.BLANCO, a, escala=pop(t, t0), spacing=3)


def faltan(ctx, n, t, t0, t1, golpe=None):
    """"FALTAN 3" en amarillo; `golpe` = momento en que el número cambia (rebote)."""
    a = window(t, t0, t1, 0.12)
    if a <= 0:
        return
    esc = pop(t, t0)
    if golpe is not None and t >= golpe:
        esc *= 1 + 0.0
        esc = max(esc, pop(t, golpe, 0.3) * 1.0)
    texto_contorno(ctx, f"FALTAN {n}", config.W / 2, Y_TOP, 92, E.AMARILLO, a, escala=esc, spacing=3)
    texto_contorno(ctx, "HUESOS", config.W / 2, Y_TOP + 62, 40, E.BLANCO, a, escala=esc, spacing=8)


def boton(ctx, texto, cx, y, rgb, a, escala=1.0):
    ctx.save()
    ctx.identity_matrix()
    font(ctx, 44 * escala, config.FONT_DISPLAY, bold=True)
    w = text_w(ctx, texto, 3) + 70 * escala
    h = 78 * escala
    ctx.translate(cx, y)
    fill_rrect(ctx, -w / 2 + 4, -h / 2 + 8, w, h, h / 2, (0, 0, 0), 0.5 * a)
    fill_rrect(ctx, -w / 2, -h / 2, w, h, h / 2, rgb, a)
    rrect(ctx, -w / 2, -h / 2, w, h, h / 2)
    ctx.set_line_width(5)
    src(ctx, (1, 1, 1), 0.9 * a)
    ctx.stroke()
    src(ctx, (1, 1, 1), a)
    text_at(ctx, texto, -text_w(ctx, texto, 3) / 2, 15 * escala, 3)
    ctx.restore()


def botones(ctx, t, t0, t1=None):
    """Los dos botones del dilema, CONTAR (rojo) y CALLAR (azul), con un punto en medio."""
    a = 1.0 if t1 is None else window(t, t0, t1, 0.12)
    if t < t0 or a <= 0:
        return
    esc = pop(t, t0, 0.3) * (1 + 0.025 * math.sin(t * 5))
    W = config.W
    boton(ctx, "CONTAR", W / 2 - 190, Y_TOP - 6, E.ROJO, a, esc)
    boton(ctx, "CALLAR", W / 2 + 190, Y_TOP - 6, E.AZUL, a, esc)
    ctx.save()
    ctx.identity_matrix()
    ctx.new_path()
    ctx.arc(W / 2, Y_TOP - 6, 9, 0, math.tau)
    src(ctx, (1, 1, 1), a)
    ctx.fill()
    ctx.restore()


def llamada_comentar(ctx, t, t0, t1=None):
    """Panel "COMENTA  1 = CONTAR · 2 = CALLAR" encima de los subtítulos."""
    a = 1.0 if t1 is None else window(t, t0, t1, 0.15)
    if t < t0 or a <= 0:
        return
    esc = pop(t, t0, 0.3)
    W = config.W
    ctx.save()
    ctx.identity_matrix()
    ctx.translate(W / 2, 1160)
    ctx.scale(esc, esc)
    fill_rrect(ctx, -400, -92, 800, 184, 30, (0, 0, 0), 0.62 * a)
    rrect(ctx, -400, -92, 800, 184, 30)
    ctx.set_line_width(5)
    src(ctx, E.AMARILLO, a)
    ctx.stroke()
    ctx.restore()
    texto_contorno(ctx, "COMENTA", W / 2, 1120, 46, E.AMARILLO, a, escala=esc, spacing=6)
    texto_contorno(ctx, "1 = CONTAR", W / 2 - 165, 1194, 44, (1.0, 0.45, 0.45), a, escala=esc)
    texto_contorno(ctx, "2 = CALLAR", W / 2 + 175, 1194, 44, (0.55, 0.75, 1.0), a, escala=esc)


def numero_conteo(ctx, palabra, t, t0, x, y, dur=1.0):
    """Un número que se canta ("UNO", "DOS"…) enorme, que sacude y se apaga: lo que se oye, se ve."""
    k = seg(t, t0, t0 + dur)
    if t < t0 or k >= 1:
        return
    a = 1 - smooth(seg(k, 0.55, 1.0))
    sacudida = 9 * math.sin(t * 60) * (1 - k)
    texto_contorno(ctx, palabra, x + sacudida, y, 150, E.AMARILLO, a, escala=pop(t, t0, 0.18), spacing=4)


def usa_audifonos(ctx, t, t0, t1):
    a = window(t, t0, t1, 0.2)
    if a <= 0:
        return
    ctx.save()
    ctx.identity_matrix()
    font(ctx, 32, config.FONT, bold=True)
    txt = "USA AUDÍFONOS"
    w = text_w(ctx, txt, 5) + 56
    x, y = config.W / 2 - w / 2, 172
    fill_rrect(ctx, x, y, w, 58, 29, (0, 0, 0), 0.55 * a)
    rrect(ctx, x, y, w, 58, 29)
    ctx.set_line_width(3)
    src(ctx, (1, 1, 1), 0.85 * a)
    ctx.stroke()
    src(ctx, (1, 1, 1), a)
    text_at(ctx, txt, x + 28, y + 39, 5)
    ctx.restore()
