"""Colores y utilidades comunes de La Planchada: noche azul-verdosa de hospital; el uniforme blanco es la única luz limpia."""
import math
import random
import cairo
from motor.primitives import src, TAU, mix

NOCHE = (0.015, 0.04, 0.055)
MURO = (0.085, 0.19, 0.21)
MURO_ALTO = (0.05, 0.12, 0.14)
RIEL = (0.12, 0.27, 0.29)
PISO = (0.045, 0.09, 0.10)
FLUO = (0.55, 0.96, 1.0)               # cian del fluorescente
HALO = (0.78, 0.94, 1.0)               # halo frío de la enfermera
BLANCO = (0.96, 0.99, 1.0)
UNIFORME_SOMBRA = (0.72, 0.86, 0.90)
CAPA = (0.035, 0.06, 0.12)
ROJO = (0.95, 0.10, 0.12)
AMANECER = (1.0, 0.72, 0.38)
AMANECER_ROSA = (1.0, 0.55, 0.45)
PIEL = (0.80, 0.62, 0.50)
PIEL_PALIDA = (0.88, 0.84, 0.82)
CABELLO = (0.05, 0.04, 0.05)
BATA = (0.45, 0.66, 0.70)              # bata de paciente
COBIJA = (0.20, 0.36, 0.42)
SABANA = (0.50, 0.68, 0.70)
METAL = (0.55, 0.68, 0.72)
SCRUB = (0.14, 0.34, 0.62)             # uniforme moderno de la enfermera de turno
SCRUB_OSC = (0.08, 0.18, 0.36)
SEPIA = (0.62, 0.42, 0.22)


def ovalo(ctx, x, y, rx, ry, rgb, a=1.0, rot=0.0):
    ctx.save()
    ctx.translate(x, y)
    if rot:
        ctx.rotate(rot)
    ctx.scale(rx, ry)
    ctx.arc(0, 0, 1, 0, TAU)
    ctx.restore()
    src(ctx, rgb, a)
    ctx.fill()


def degradado_v(ctx, x, y, w, h, c0, c1, a0=1.0, a1=1.0):
    g = cairo.LinearGradient(0, y, 0, y + h)
    g.add_color_stop_rgba(0, *c0, a0)
    g.add_color_stop_rgba(1, *c1, a1)
    ctx.rectangle(x, y, w, h)
    ctx.set_source(g)
    ctx.fill()


def fluo_brillo(t, seed=0, modo="parpadea"):
    """Brillo 0..1 de un fluorescente. 'fijo' casi constante; 'parpadea' con caídas cortas; 'inestable' se cae seguido."""
    if modo == "fijo":
        return 0.97 + 0.03 * math.sin(t * 90)
    r = random.Random(seed * 1009 + int(t * 18))
    p = 0.14 if modo == "parpadea" else 0.42
    if r.random() < p:
        return 0.15 + 0.5 * r.random()
    return 1.0


def tubo_fluo(ctx, x, y, w, brillo, h=16):
    """Fluorescente de techo (tubo) con su resplandor."""
    from motor.primitives import glow, fill_rrect
    fill_rrect(ctx, x - 6, y - 4, w + 12, h + 8, 5, (0.10, 0.16, 0.18))
    fill_rrect(ctx, x, y, w, h, 6, mix((0.2, 0.3, 0.3), (0.92, 1.0, 1.0), brillo))
    if brillo > 0.05:
        glow(ctx, x + w / 2, y + h / 2, w * 0.75, FLUO, 0.35 * brillo)


def trazo_grueso(ctx, pts, w, rgb, a=1.0):
    """Polilínea con puntas redondas (mangas, brazos, tubos)."""
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_line_width(w)
    src(ctx, rgb, a)
    ctx.move_to(*pts[0])
    for p in pts[1:]:
        ctx.line_to(*p)
    ctx.stroke()
