"""El cuarto del hospital (sin nombre, ficticio). Todo en coordenadas del mundo 1080×1920; las escenas lo encuadran con la cámara.

Planta: cabecera de la cama a la izquierda bajo la ventana; reloj en la pared del centro; puerta al pasillo a la derecha;
buró entre la cama y la puerta; el suero junto a la cama. Suelo en y = 1190.
"""
import math
import cairo
from motor.primitives import (src, line, circle, glow, fill_rrect, fill_poly, seg, smooth, lerp, mix, clamp, vignette)
from historias.planchada.dibujo.paleta import (ovalo, degradado_v, fluo_brillo, tubo_fluo, trazo_grueso, MURO, MURO_ALTO, RIEL,
                                               PISO, FLUO, METAL, HALO)
from historias.planchada.dibujo import objetos, personajes

SUELO = 1190


def cam(ctx, z, cx, cy, dx=0.0, dy=0.0):
    """Cámara centrada en (cx, cy) con zoom z, sin salirse del cuarto (nunca se ven franjas negras fuera del dibujo)."""
    from motor.primitives import camera_center
    hx, hy = 540 / z, 960 / z
    camera_center(ctx, z, min(max(cx, hx), 1080 - hx), min(max(cy, hy), 1920 - hy), dx, dy)
VENTANA = (110, 290, 310, 470)
RELOJ = (560, 470, 78)
PUERTA = (770, 360, 240, SUELO - 360)
CABEZA = (190, 950)                    # centro de la cabeza de Rafa sobre la almohada
BURO = (665, 960, 92)


def _pasillo_visto_desde_cuarto(ctx, x, y, w, h, t, luz, turno, seed):
    """Lo que se ve por la puerta abierta: pasillo cian con una enfermera de turno dormida en su silla."""
    ctx.save()
    ctx.rectangle(x, y, w, h)
    ctx.clip()
    degradado_v(ctx, x, y, w, h, mix((0.05, 0.14, 0.16), (0.16, 0.34, 0.37), luz), mix((0.07, 0.17, 0.19), (0.24, 0.46, 0.5), luz))
    degradado_v(ctx, x, y + h * 0.80, w, h * 0.20, (0.05, 0.11, 0.12), (0.10, 0.20, 0.22))
    b = fluo_brillo(t, seed + 4, "inestable")
    tubo_fluo(ctx, x + 40, y + 30, w - 80, b * luz, 12)
    glow(ctx, x + w / 2, y + h * 0.85, w * 0.9, FLUO, 0.22 * b * luz)
    if turno == "dormida":
        personajes.turno_dormida(ctx, x + w * 0.52, y + h * 0.90, 0.55, t, b)
    ctx.restore()
    ctx.set_line_width(16)                                                                  # marco
    src(ctx, (0.03, 0.07, 0.08))
    ctx.rectangle(x, y, w, h)
    ctx.stroke()


def cama(ctx):
    """Estructura de la cama (sin Rafa ni cobija)."""
    for lx in (60, 620):
        line(ctx, lx, 1100, lx, SUELO + 10, 16, (0.07, 0.12, 0.13))
    fill_rrect(ctx, 52, 1006, 600, 22, 8, (0.15, 0.20, 0.22))                               # colchón (borde)
    fill_rrect(ctx, 46, 1040, 612, 56, 10, (0.12, 0.2, 0.22))                               # bastidor
    fill_rrect(ctx, 30, 880, 34, 240, 12, (0.12, 0.2, 0.22))                                # cabecera
    fill_rrect(ctx, 640, 960, 26, 150, 12, (0.12, 0.2, 0.22))                               # piecera


def suero(ctx, t, gota_visible=True):
    """Poste del suero con bolsa, cámara de goteo y tubo hacia el brazo de Rafa."""
    px = 480
    line(ctx, px, 560, px, 1080, 9, (0.40, 0.52, 0.56))
    line(ctx, px - 36, 566, px + 36, 566, 8, (0.40, 0.52, 0.56))
    fill_rrect(ctx, px - 36, 580, 72, 130, 22, (0.55, 0.78, 0.82), )
    fill_rrect(ctx, px - 30, 626, 60, 78, 18, (0.70, 0.92, 0.95), 0.55)
    fill_rrect(ctx, px - 11, 714, 22, 76, 8, (0.78, 0.9, 0.92), 0.8)                         # cámara de goteo
    if gota_visible:
        f = (t * 0.9) % 1.0
        circle(ctx, px, 728 + 46 * f * f, 4 + 1.5 * (1 - f), (0.9, 1.0, 1.0), 0.95)
    trazo_grueso(ctx, [(px, 790), (px - 4, 880), (px - 60, 960), (px - 120, 1010), (px - 160, 1040)], 4, (0.82, 0.92, 0.94), 0.8)


def buro(ctx, pastilla_vis=False, t=0.0):
    x, y, w = BURO
    fill_rrect(ctx, x, y, w, SUELO - y, 8, (0.11, 0.20, 0.22))
    fill_rrect(ctx, x - 6, y - 10, w + 12, 18, 6, (0.17, 0.30, 0.33))
    fill_rrect(ctx, x + 8, y + 36, w - 16, 50, 6, (0.08, 0.15, 0.16))
    circle(ctx, x + w / 2, y + 61, 5, (0.45, 0.55, 0.55))
    fill_rrect(ctx, x + 18, y - 38, 26, 28, 6, (0.55, 0.78, 0.82), 0.7)                      # vaso
    if pastilla_vis:
        objetos.pastilla(ctx, x + 66, y - 18, 9, 0.9 + 0.1 * math.sin(t * 3))


def cuarto(ctx, t, *, fluo=1.0, ventana=0.0, escarcha=0.0, amanecer=0.0, hora=(2, 59), segundero=None, turno="dormida",
           pasillo=1.0, gota=True, pastilla_buro=False, seed=1, reflejo=None, luz_cuarto=1.0, lampara_roja=0.0, cortinas=True):
    """Dibuja el cuarto completo. fluo: brillo del fluorescente del techo 0..1 (usa fluo_brillo en la escena)."""
    base = 0.30 + 0.70 * fluo
    base *= (0.5 + 0.5 * luz_cuarto) if luz_cuarto < 1 else 1.0
    c = lambda col: tuple(v * (0.6 + 0.4 * base) for v in col)
    amb = mix((1, 1, 1), (1.0, 0.86, 0.72), amanecer * 0.6)
    # muro y piso
    degradado_v(ctx, 0, 0, 1080, SUELO, c(MURO_ALTO), c(MURO))
    degradado_v(ctx, 0, 880, 1080, 24, c(RIEL), c(RIEL))
    line(ctx, 0, 884, 1080, 884, 5, c((0.2, 0.38, 0.4)), 1.0, cairo.LINE_CAP_BUTT)
    degradado_v(ctx, 0, SUELO, 1080, 1920 - SUELO, c(PISO), (0.02, 0.04, 0.05))
    line(ctx, 0, SUELO + 2, 1080, SUELO + 2, 12, (0.02, 0.05, 0.06), 1.0, cairo.LINE_CAP_BUTT)
    for i in range(1, 8):                                                                   # juntas del piso
        line(ctx, 540 + (i - 4) * 90, SUELO + 6, 540 + (i - 4) * 260, 1920, 3, (0.02, 0.05, 0.06), 0.6)
    # puerta al pasillo
    px, py, pw, ph = PUERTA
    _pasillo_visto_desde_cuarto(ctx, px, py, pw, ph, t, pasillo, turno, seed)
    # ventana y reloj
    vx, vy, vw, vh = VENTANA
    objetos.ventana(ctx, vx, vy, vw, vh, apertura=ventana, escarcha=escarcha, amanecer=amanecer, t=t, luz=base, reflejo=reflejo, cortinas=cortinas)
    rx, ry, rr = RELOJ
    objetos.reloj(ctx, rx, ry, rr, hora[0], hora[1], base, segundero)
    cama(ctx)
    suero(ctx, t, gota)
    buro(ctx, pastilla_buro, t)
    # tubo fluorescente del techo y luz que cae
    tubo_fluo(ctx, 330, 36, 430, fluo, 18)
    if fluo > 0.05:
        g = cairo.LinearGradient(0, 56, 0, 900)
        g.add_color_stop_rgba(0, *FLUO, 0.16 * fluo)
        g.add_color_stop_rgba(1, *FLUO, 0.0)
        ctx.move_to(330, 56)
        ctx.line_to(760, 56)
        ctx.line_to(1080, 900)
        ctx.line_to(0, 900)
        ctx.close_path()
        ctx.set_source(g)
        ctx.save()
        ctx.set_operator(cairo.OPERATOR_ADD)
        ctx.fill()
        ctx.restore()
    if lampara_roja > 0:                                                                    # luz de llamado sobre la puerta
        fill_rrect(ctx, 860, 312, 100, 30, 10, (0.3, 0.03, 0.04))
        fill_rrect(ctx, 866, 318, 88, 18, 8, (1.0, 0.2, 0.2), 0.3 + 0.7 * lampara_roja)
        glow(ctx, 910, 327, 380, (1.0, 0.12, 0.12), 0.55 * lampara_roja)
    if amanecer > 0:                                                                        # luz ámbar desde la ventana
        glow(ctx, 265, 520, 900, (1.0, 0.7, 0.4), 0.30 * amanecer)
