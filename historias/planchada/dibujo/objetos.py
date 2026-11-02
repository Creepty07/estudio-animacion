"""Objetos y primeros planos de La Planchada: reloj, ventana (cortina, escarcha, reflejo), timbre, expediente, pastilla."""
import math
import random
import cairo
from motor import config
from motor.primitives import (src, line, circle, glow, fill_rrect, rrect, fill_poly, font, text_w, text_at, text_center,
                              seg, smooth, lerp, TAU, mix, clamp)
from historias.planchada.dibujo.paleta import (ovalo, degradado_v, trazo_grueso, METAL, FLUO, HALO, BLANCO, SEPIA, ROJO,
                                               AMANECER, AMANECER_ROSA, PIEL_PALIDA)


# ------------------------------------------------------------------ reloj
def reloj(ctx, cx, cy, r, hora, minuto, luz=1.0, segundero=None):
    """Reloj de pared. hora 0-12, minuto 0-60 (la hora se corre con los minutos). segundero: segundos o None."""
    circle(ctx, cx, cy, r * 1.12, (0.03, 0.05, 0.06))
    circle(ctx, cx, cy, r, mix((0.15, 0.22, 0.23), (0.82, 0.90, 0.90), 0.8 * luz))
    for i in range(60):
        a = i / 60 * TAU - math.pi / 2
        gordo = i % 5 == 0
        r0 = r * (0.80 if gordo else 0.90)
        line(ctx, cx + math.cos(a) * r0, cy + math.sin(a) * r0, cx + math.cos(a) * r * 0.96, cy + math.sin(a) * r * 0.96,
             max(2.0, r * (0.045 if gordo else 0.02)), (0.06, 0.08, 0.09), 0.9)
    ah = ((hora % 12) + minuto / 60) / 12 * TAU - math.pi / 2
    am = minuto / 60 * TAU - math.pi / 2
    line(ctx, cx, cy, cx + math.cos(ah) * r * 0.5, cy + math.sin(ah) * r * 0.5, r * 0.09, (0.04, 0.05, 0.06))
    line(ctx, cx, cy, cx + math.cos(am) * r * 0.78, cy + math.sin(am) * r * 0.78, r * 0.06, (0.04, 0.05, 0.06))
    if segundero is not None:
        a = segundero / 60 * TAU - math.pi / 2
        line(ctx, cx - math.cos(a) * r * 0.14, cy - math.sin(a) * r * 0.14, cx + math.cos(a) * r * 0.85, cy + math.sin(a) * r * 0.85,
             max(1.5, r * 0.02), (0.75, 0.1, 0.1))
    circle(ctx, cx, cy, r * 0.07, (0.04, 0.05, 0.06))


# ------------------------------------------------------------------ ventana
def _escarcha(ctx, x, y, w, h, k, seed=3):
    """Cristales de hielo que crecen desde los bordes del vidrio; k 0..1."""
    if k <= 0:
        return
    ctx.save()
    ctx.rectangle(x, y, w, h)
    ctx.clip()
    r = random.Random(seed)
    src(ctx, (0.88, 0.97, 1.0), 0.20 * k)
    ctx.rectangle(x, y, w, h)
    ctx.fill()
    for i in range(46):
        lado = i % 4
        u = r.random()
        if lado == 0:
            p, d = (x + u * w, y), (r.uniform(-0.4, 0.4), 1.0)
        elif lado == 1:
            p, d = (x + u * w, y + h), (r.uniform(-0.4, 0.4), -1.0)
        elif lado == 2:
            p, d = (x, y + u * h), (1.0, r.uniform(-0.4, 0.4))
        else:
            p, d = (x + w, y + u * h), (-1.0, r.uniform(-0.4, 0.4))
        largo = r.uniform(40, 150) * k * (0.6 + 0.4 * (1 - abs(u - 0.5) * 2))
        _rama(ctx, p, d, largo, 3.0, r, 0.65 * min(1.0, k * 1.6))
    ctx.restore()


def _rama(ctx, p, d, largo, grosor, r, a, prof=0):
    n = math.hypot(*d) or 1
    d = (d[0] / n, d[1] / n)
    q = (p[0] + d[0] * largo, p[1] + d[1] * largo)
    line(ctx, p[0], p[1], q[0], q[1], grosor, (0.90, 0.98, 1.0), a)
    if prof < 2 and largo > 14:
        for f in (0.45, 0.75):
            m = (p[0] + d[0] * largo * f, p[1] + d[1] * largo * f)
            for s in (-1, 1):
                ang = s * r.uniform(0.6, 1.0)
                dd = (d[0] * math.cos(ang) - d[1] * math.sin(ang), d[0] * math.sin(ang) + d[1] * math.cos(ang))
                _rama(ctx, m, dd, largo * 0.38, grosor * 0.7, r, a * 0.9, prof + 1)


def cielo_ventana(ctx, x, y, w, h, amanecer=0.0):
    """Lo que se ve afuera: noche con árboles oscuros; con amanecer>0 el cielo se vuelve ámbar y rosa."""
    ctx.save()
    ctx.rectangle(x, y, w, h)
    ctx.clip()
    noche0, noche1 = (0.01, 0.03, 0.06), (0.05, 0.12, 0.17)
    dia0, dia1 = (0.55, 0.45, 0.55), (1.0, 0.72, 0.42)
    degradado_v(ctx, x, y, w, h, mix(noche0, dia0, amanecer), mix(noche1, dia1, amanecer))
    r = random.Random(11)
    for _ in range(14):
        circle(ctx, x + r.uniform(0.05, 0.95) * w, y + r.uniform(0.04, 0.5) * h, r.uniform(1.2, 2.4), (0.9, 0.95, 1.0), 0.7 * (1 - amanecer))
    for cx_, rr in ((0.18, 0.30), (0.52, 0.38), (0.88, 0.32)):                           # copas de árboles
        ovalo(ctx, x + cx_ * w, y + h * 0.98, w * rr, h * 0.22, mix((0.01, 0.03, 0.04), (0.18, 0.12, 0.12), amanecer * 0.7))
    if amanecer > 0:
        glow(ctx, x + w * 0.5, y + h * 0.9, w * 0.9, AMANECER, 0.6 * amanecer)
    ctx.restore()


def cortina(ctx, x, y, w, h, viento=0.0, t=0.0, lado=1):
    """Cortina clara que se infla con el viento. viento 0..1. lado=1 desde la derecha."""
    ancho = w * 0.30
    ctx.save()
    n = 14
    pts_a, pts_b = [], []
    for i in range(n + 1):
        u = i / n
        sw = viento * (50 + 70 * u) * (0.7 + 0.3 * math.sin(t * 7 + u * 5)) * lado
        base = x + (w - ancho * (1 - 0.1 * u)) if lado > 0 else x + ancho * (1 - 0.1 * u)
        pts_a.append((base - sw - (14 * viento * u) * lado, y + u * h * 0.78))
        pts_b.append((base + (ancho * 0.9 if lado > 0 else -ancho * 0.9) - sw * 0.7, y + u * h * 0.78))
    ctx.move_to(*pts_a[0])
    for p in pts_a[1:]:
        ctx.line_to(*p)
    for p in reversed(pts_b):
        ctx.line_to(*p)
    ctx.close_path()
    g = cairo.LinearGradient(x, 0, x + w, 0)
    g.add_color_stop_rgba(0, 0.55, 0.72, 0.74, 0.9)
    g.add_color_stop_rgba(1, 0.32, 0.5, 0.54, 0.92)
    ctx.set_source(g)
    ctx.fill()
    for i in range(1, 6):                                                              # pliegues
        k = i / 6
        ctx.move_to(*pts_a[0])
        ctx.new_path()
        line(ctx, lerp(pts_a[0][0], pts_b[0][0], k), pts_a[0][1], lerp(pts_a[-1][0], pts_b[-1][0], k), pts_a[-1][1], 3, (0.05, 0.12, 0.14), 0.25)
    ctx.restore()


def ventana(ctx, x, y, w, h, apertura=0.0, escarcha=0.0, amanecer=0.0, t=0.0, cortinas=True, luz=1.0, reflejo=None):
    """Ventana de dos hojas. apertura 0 cerrada → 1 abierta de golpe. reflejo(ctx, x, y, w, h) pinta el reflejo en el vidrio."""
    fr = 14
    cielo_ventana(ctx, x, y, w, h, amanecer)
    # hojas del vidrio (se angostan al abrirse hacia adentro)
    ap = clamp(apertura)
    hoja_w = (w / 2) * (1 - 0.82 * ap)
    for lado in (-1, 1):
        hx = x if lado < 0 else x + w - hoja_w
        ctx.save()
        ctx.rectangle(hx, y, hoja_w, h)
        ctx.clip()
        src(ctx, (0.35, 0.62, 0.7), 0.16 * (1 - ap * 0.4))
        ctx.paint()
        g = cairo.LinearGradient(hx, y, hx + hoja_w, y + h)
        g.add_color_stop_rgba(0, 1, 1, 1, 0.13)
        g.add_color_stop_rgba(0.4, 1, 1, 1, 0.0)
        ctx.set_source(g)
        ctx.paint()
        if reflejo is not None and ap < 0.05:
            reflejo(ctx, x, y, w, h)
        _escarcha(ctx, hx, y, hoja_w, h, escarcha, seed=5 + (lado > 0))
        ctx.restore()
        ctx.set_line_width(fr)
        src(ctx, (0.04, 0.09, 0.10))
        ctx.rectangle(hx, y, hoja_w, h)
        ctx.stroke()
    if ap < 0.3:                                                                       # travesaño
        line(ctx, x, y + h * 0.52, x + w, y + h * 0.52, fr * 0.7, (0.04, 0.09, 0.10), 1.0, cairo.LINE_CAP_BUTT)
    ctx.set_line_width(fr)
    src(ctx, (0.04, 0.09, 0.10))
    ctx.rectangle(x - fr / 2, y - fr / 2, w + fr, h + fr)
    ctx.stroke()
    # repisa
    fill_rrect(ctx, x - 24, y + h + 4, w + 48, 20, 6, (0.12, 0.26, 0.28))
    if cortinas:
        cortina(ctx, x - 24, y - 20, w + 48, h + 20, viento=ap, t=t, lado=1)
        cortina(ctx, x - 24, y - 20, w + 48, h + 20, viento=ap * 0.9, t=t + 1.3, lado=-1)


# ------------------------------------------------------------------ timbre
def timbre(ctx, cx, cy, s, presionado=0.0, luz_roja=0.0):
    """Botón de llamado a la enfermera: cable, caja gris y botón rojo."""
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(s, s)
    trazo_grueso(ctx, [(0, -420), (30, -300), (-20, -190), (0, -90)], 12, (0.07, 0.1, 0.11))
    fill_rrect(ctx, -170, -100, 340, 240, 60, (0.72, 0.80, 0.80))
    fill_rrect(ctx, -170, -100, 340, 240, 60, (0, 0, 0), 0.0)
    rrect(ctx, -170, -100, 340, 240, 60)
    ctx.set_line_width(8)
    src(ctx, (0.25, 0.34, 0.35))
    ctx.stroke()
    off = 12 * presionado
    circle(ctx, 0, 20 + off * 0.5, 96, (0.28, 0.04, 0.05))
    circle(ctx, 0, 14 + off, 88 - off * 0.3, mix((0.95, 0.12, 0.14), (0.55, 0.06, 0.08), presionado))
    circle(ctx, -26, -14 + off, 26, (1.0, 0.7, 0.7), 0.45 * (1 - presionado))
    ctx.restore()


# ------------------------------------------------------------------ mano con pastilla
def pastilla(ctx, x, y, r, brillo=1.0, rot=0.3):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    glow(ctx, 0, 0, r * 4.2, HALO, 0.35 * brillo)
    fill_rrect(ctx, -r * 1.35, -r * 0.62, r * 2.7, r * 1.24, r * 0.62, (0.96, 0.98, 0.98))
    line(ctx, 0, -r * 0.62, 0, r * 0.62, max(1.5, r * 0.08), (0.65, 0.76, 0.78), 1.0, cairo.LINE_CAP_BUTT)
    ctx.restore()


def mano_pastilla(ctx, cx, cy, s, t=0.0, brillo=1.0, pastilla_visible=True):
    """Primer plano de la mano abierta de la enfermera: palma pálida con la pastilla, manga blanca al fondo."""
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(s, s)
    glow(ctx, 0, 0, 520, HALO, 0.25)
    trazo_grueso(ctx, [(-380, 180), (-170, 90)], 190, (0.93, 0.97, 0.98))                     # manga almidonada
    trazo_grueso(ctx, [(-380, 180), (-170, 90)], 150, (0.80, 0.90, 0.93), 0.5)
    # palma y dedos (dedos largos, juntos y un poco curvos; el pulgar sale por arriba)
    fill_rrect(ctx, -170, -70, 300, 230, 70, PIEL_PALIDA)
    for dx, dy, ang, ln, w_ in ((110, -62, -0.30, 215, 54), (120, 0, -0.10, 245, 56), (112, 62, 0.08, 225, 52), (92, 118, 0.30, 170, 46)):
        ctx.save()
        ctx.translate(dx, dy)
        ctx.rotate(ang)
        fill_rrect(ctx, 0, -w_ / 2, ln, w_, w_ / 2, PIEL_PALIDA)
        for k in (0.38, 0.72):                                                                 # nudillos
            line(ctx, ln * k, -w_ * 0.28, ln * k, w_ * 0.28, 2.5, (0.60, 0.55, 0.56), 0.5)
        ctx.restore()
    ctx.save()
    ctx.translate(-50, -48)
    ctx.rotate(-0.95)
    fill_rrect(ctx, 0, -32, 190, 64, 32, PIEL_PALIDA)
    ctx.restore()
    ovalo(ctx, 10, 25, 150, 90, (0.70, 0.64, 0.64), 0.35, -0.15)                              # sombra de la palma
    if pastilla_visible:
        pastilla(ctx, 20 + 3 * math.sin(t * 1.3), 20, 40, brillo)
    ctx.restore()


# ------------------------------------------------------------------ expediente con la nota
def expediente(ctx, cx, cy, s, t, nota_alpha=1.0, glitch_e=0.0):
    """Hoja de expediente: anotaciones modernas en azul y, entre ellas, una nota en tinta sepia con letra antigua."""
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(s, s)
    ctx.rotate(-0.04)
    fill_rrect(ctx, -330, -440, 660, 880, 14, (0.04, 0.07, 0.08), 0.5)                         # sombra
    fill_rrect(ctx, -340, -450, 660, 880, 14, (0.88, 0.90, 0.86))
    rr = random.Random(8)
    font(ctx, 30, config.FONT, bold=True)
    src(ctx, (0.15, 0.25, 0.4))
    text_at(ctx, "EXPEDIENTE · HABITACIÓN 4", -300, -392, 3)
    line(ctx, -300, -370, 280, -370, 3, (0.15, 0.25, 0.4), 0.6)
    for i in range(11):                                                                       # anotaciones modernas
        y = -320 + i * 52
        if 3 <= i <= 6:
            continue
        w_ = rr.uniform(300, 560)
        line(ctx, -300, y, -300 + w_, y, 9, (0.18, 0.30, 0.55), 0.55)
        line(ctx, -300, y + 20, -300 + w_ * 0.7, y + 20, 5, (0.18, 0.30, 0.55), 0.3)
    # la nota antigua, en el hueco
    ctx.save()
    ctx.rotate(0.025)
    src(ctx, (0.80, 0.74, 0.6), 0.9 * nota_alpha)
    ctx.rectangle(-320, -170, 620, 250)
    ctx.fill()
    font(ctx, 54, "DejaVu Serif", italic=True)
    src(ctx, SEPIA, nota_alpha)
    text_at(ctx, "Fiebre bajó.", -290, -92, 2)
    text_at(ctx, "3:00 a. m.", -290, -22, 2)
    font(ctx, 70, "DejaVu Serif", italic=True, bold=True)
    gx = 120 + (random.Random(int(t * 30)).uniform(-14, 14) if glitch_e > 0 else 0)
    if glitch_e > 0:
        ctx.save()
        ctx.set_operator(cairo.OPERATOR_ADD)
        src(ctx, (1, 0, 0), 0.8 * glitch_e)
        text_at(ctx, "— E.", gx - 8, 56)
        src(ctx, (0, 1, 1), 0.8 * glitch_e)
        text_at(ctx, "— E.", gx + 8, 56)
        ctx.restore()
    src(ctx, SEPIA, nota_alpha)
    text_at(ctx, "— E.", gx, 56)
    ctx.restore()
    ctx.restore()


# ------------------------------------------------------------------ cofia sobre la silla
def silla(ctx, cx, cy, s):
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(s, s)
    for dx in (-110, 110):
        line(ctx, dx, 0, dx * 1.12, 330, 16, (0.05, 0.08, 0.09))
    fill_rrect(ctx, -150, -20, 300, 36, 12, (0.10, 0.17, 0.19))
    fill_rrect(ctx, -140, -400, 280, 28, 12, (0.10, 0.17, 0.19))
    for dx in (-110, 110):
        line(ctx, dx, -380, dx, -16, 18, (0.08, 0.13, 0.15))
    for k in (-60, 0, 60):
        line(ctx, k, -372, k, -60, 10, (0.07, 0.12, 0.13))
    ctx.restore()


def cofia(ctx, cx, cy, s, rot=0.0):
    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(rot)
    ctx.scale(s, s)
    glow(ctx, 0, 0, 260, HALO, 0.3)
    ctx.move_to(-130, 40)
    ctx.curve_to(-120, -60, -60, -110, 0, -100)
    ctx.curve_to(70, -110, 130, -50, 140, 40)
    ctx.curve_to(60, 70, -60, 70, -130, 40)
    ctx.close_path()
    src(ctx, BLANCO)
    ctx.fill()
    ctx.move_to(-130, 40)
    ctx.curve_to(-60, 70, 60, 70, 140, 40)
    ctx.set_line_width(14)
    src(ctx, (0.72, 0.86, 0.9))
    ctx.stroke()
    line(ctx, -80, -50, 90, -52, 6, (0.78, 0.88, 0.92), 0.8)
    ctx.restore()


# ------------------------------------------------------------------ vaho
def vaho(ctx, x, y, t, fuerza=1.0, seed=2):
    """Respiración visible en el aire frío: bocanadas que suben y se abren."""
    r = random.Random(seed)
    for i in range(5):
        fase = ((t * 0.7 + i / 5) % 1.0)
        a = (1 - fase) * 0.30 * fuerza * smooth(seg(fase, 0, 0.15))
        glow(ctx, x + 40 * fase + r.uniform(-8, 8), y - 90 * fase, 26 + 70 * fase, (0.85, 0.96, 1.0), a, cairo.OPERATOR_OVER)
