"""El camión sin número, por fuera: viejo, diseñado desde cero (sin empresa, color ni logotipo real). El letrero "0" ámbar es su rasgo."""
import math
import random
import cairo
from motor.primitives import src, line, circle, glow, fill_rrect, fill_poly, rrect, seg, smooth, lerp, mix, font, text_center
from historias.ruta0.dibujo.paleta import (ovalo, degradado_v, trazo, AMBAR, AMBAR_CLARO, AMARILLO, ROJO, HIERRO, CAMION, CAMION_OSC)


def letrero_cero(ctx, cx, cy, w, h, enc=1.0, t=0.0, parpadeo=0.0):
    """Caja del destino con el "0" ámbar; parpadeo 0..1 lo hace titilar (se apaga cuando enc=0)."""
    f = enc * (1.0 - parpadeo * (0.5 + 0.5 * math.sin(t * 40) ** 4))
    fill_rrect(ctx, cx - w / 2, cy - h / 2, w, h, 8, (0.02, 0.025, 0.03))
    if f > 0.02:
        glow(ctx, cx, cy, w * 2.3, AMBAR, 0.55 * f, cairo.OPERATOR_SCREEN)
        fill_rrect(ctx, cx - w / 2 + 6, cy - h / 2 + 6, w - 12, h - 12, 5, mix((0.15, 0.06, 0.01), (0.55, 0.22, 0.02), f))
        font(ctx, h * 0.95, "Inter Display Black")
        src(ctx, mix((0.3, 0.1, 0.0), AMBAR_CLARO, f))
        text_center(ctx, "0", cx, cy + h * 0.34)


def camion_lado(ctx, x, y, s=1.0, t=0.0, zero=1.0, puertas=0.0, faros=1.0, luz_int=0.8, pasajeros=True, mirando=1, zero_parpadeo=0.0, humo=0.0, caras=0.0):
    """Vista lateral. (x, y) = suelo bajo el centro. El frente queda a la derecha (mirando=1) o a la izquierda (-1)."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s * mirando, s)
    bob = 1.5 * math.sin(t * 22)
    ctx.translate(0, bob)
    ovalo(ctx, 0, 4, 470, 22, (0, 0, 0), 0.5)                                                  # sombra en el piso mojado
    # carrocería
    fill_rrect(ctx, -440, -330, 880, 270, 26, CAMION)
    fill_rrect(ctx, -440, -330, 880, 36, 18, mix(CAMION, (1, 1, 1), 0.06))                      # techo
    fill_rrect(ctx, -440, -110, 880, 46, 8, CAMION_OSC)                                         # faldón sucio
    for k in range(5):                                                                          # óxido y golpes
        r = random.Random(k)
        ovalo(ctx, -380 + k * 190 + r.uniform(-20, 20), -100 + r.uniform(0, 20), r.uniform(24, 50), 10, (0.32, 0.16, 0.08), 0.35)
    line(ctx, -440, -196, 440, -196, 6, (0.5, 0.42, 0.18), 0.45)                                 # franja desvaída
    # ventanas (con la luz amarilla de adentro y las siluetas quietas)
    for i in range(7):
        wx = -400 + i * 100
        fill_rrect(ctx, wx, -300, 88, 90, 8, (0.02, 0.03, 0.035))
        if luz_int > 0:
            fill_rrect(ctx, wx + 3, -297, 82, 84, 6, mix((0.1, 0.09, 0.04), AMARILLO, 0.75 * luz_int), 0.9)
            if caras > 0:                                                                       # todos mirando hacia afuera
                ovalo(ctx, wx + 44, -258, 17, 22, (0.82, 0.85, 0.82), caras)
                for sx in (-6, 6):
                    circle(ctx, wx + 44 + sx, -262, 2.6, (0.02, 0.02, 0.03), caras)
            elif pasajeros and i % 3 != 1:
                ovalo(ctx, wx + 44, -262, 13, 16, (0.05, 0.05, 0.06), 0.9)
                ovalo(ctx, wx + 44, -222, 26, 20, (0.05, 0.05, 0.06), 0.9)
    # parabrisas y puerta (al frente, a la derecha)
    fill_poly(ctx, [(300, -300), (428, -300), (440, -200), (300, -200)], (0.02, 0.03, 0.04))
    fill_poly(ctx, [(308, -294), (420, -294), (431, -206), (308, -206)], mix((0.05, 0.07, 0.08), AMARILLO, 0.18 * luz_int), 0.9)
    fill_rrect(ctx, 296, -208, 8, 148, 0, CAMION_OSC)
    p = smooth(puertas)
    fill_rrect(ctx, 210, -296, 84, 236, 4, (0.02, 0.025, 0.03))
    if p > 0.02:
        fill_rrect(ctx, 214, -292, 76, 228, 3, mix((0.1, 0.09, 0.04), AMARILLO, 0.85 * luz_int))
        glow(ctx, 252, -180, 220, AMARILLO, 0.3 * p, cairo.OPERATOR_SCREEN)
        ovalo(ctx, 252, -150, 20, 40, (0.02, 0.02, 0.03), 0.9)                                    # silueta del chofer a contraluz
        ovalo(ctx, 252, -214, 14, 16, (0.02, 0.02, 0.03), 0.9)
    for dx in (0, 1):                                                                           # hojas plegables
        w = 38 * (1 - p)
        fill_rrect(ctx, 214 + dx * (76 - w), -292, max(w, 2), 228, 2, mix(CAMION, (0.5, 0.6, 0.65), 0.1))
    # frente: faro y letrero
    fill_rrect(ctx, 424, -150, 22, 48, 6, (0.03, 0.035, 0.04))
    if faros > 0:
        glow(ctx, 446, -126, 260, (1.0, 0.95, 0.8), 0.5 * faros, cairo.OPERATOR_SCREEN)
        g = cairo.LinearGradient(446, 0, 1100, 0)
        g.add_color_stop_rgba(0, 1, 0.95, 0.75, 0.22 * faros)
        g.add_color_stop_rgba(1, 1, 0.95, 0.75, 0.0)
        ctx.move_to(446, -130)
        ctx.line_to(1100, -260)
        ctx.line_to(1100, 20)
        ctx.close_path()
        ctx.set_source(g)
        ctx.fill()
    letrero_cero(ctx, 372, -352, 120, 52, zero, t, zero_parpadeo)
    # ruedas
    for wx in (-270, 250):
        circle(ctx, wx, -50, 62, (0.015, 0.02, 0.025))
        circle(ctx, wx, -50, 34, (0.08, 0.1, 0.11))
        for k in range(6):
            a = k / 6 * math.tau + t * 12
            line(ctx, wx + 8 * math.cos(a), -50 + 8 * math.sin(a), wx + 30 * math.cos(a), -50 + 30 * math.sin(a), 4, (0.03, 0.04, 0.05))
    ctx.restore()


def camion_frente(ctx, cx, y, s=1.0, t=0.0, zero=1.0, faros=1.0, limpia=True, parpadeo=0.0):
    """Vista de frente: dos faros, parabrisas con limpiadores y el letrero "0" arriba. (cx, y) = centro y suelo."""
    ctx.save()
    ctx.translate(cx, y)
    ctx.scale(s, s)
    ovalo(ctx, 0, 6, 330, 24, (0, 0, 0), 0.5)
    fill_rrect(ctx, -250, -640, 500, 600, 40, CAMION)
    fill_rrect(ctx, -250, -640, 500, 60, 30, mix(CAMION, (1, 1, 1), 0.06))
    fill_rrect(ctx, -232, -540, 464, 270, 14, (0.015, 0.02, 0.025))                              # parabrisas
    g = cairo.LinearGradient(-232, -540, 232, -270)
    g.add_color_stop_rgba(0, 0.6, 0.8, 0.95, 0.12)
    g.add_color_stop_rgba(0.5, 0.6, 0.8, 0.95, 0.0)
    ctx.rectangle(-232, -540, 464, 270)
    ctx.set_source(g)
    ctx.fill()
    line(ctx, 0, -540, 0, -270, 8, CAMION_OSC)
    if limpia:                                                                                  # limpiadores
        for sx in (-1, 1):
            a = 0.35 + 0.55 * (0.5 + 0.5 * math.sin(t * 4.5))
            bx, by = sx * 100, -278
            line(ctx, bx, by, bx + sx * 150 * math.cos(a), by - 150 * math.sin(a), 6, (0.01, 0.01, 0.012), 0.95)
    fill_rrect(ctx, -170, -250, 340, 70, 10, CAMION_OSC)                                         # parrilla
    for k in range(7):
        line(ctx, -150 + k * 50, -240, -150 + k * 50, -190, 5, (0.03, 0.04, 0.05))
    fill_rrect(ctx, -270, -120, 540, 56, 12, (0.1, 0.12, 0.14))                                  # defensa
    for sx in (-1, 1):
        fx = sx * 190
        circle(ctx, fx, -190, 50, (0.04, 0.045, 0.05))
        circle(ctx, fx, -190, 38, mix((0.15, 0.15, 0.12), (1.0, 0.96, 0.8), faros))
        glow(ctx, fx, -190, 520 * s ** 0.2, (1.0, 0.95, 0.8), 0.6 * faros, cairo.OPERATOR_SCREEN)
    for sx in (-1, 1):
        fill_rrect(ctx, sx * 270 - 22, -150, 44, 150, 8, (0.015, 0.02, 0.025))                    # llantas
    letrero_cero(ctx, 0, -600, 210, 70, zero, t, parpadeo)
    ctx.restore()


def camion_trasero(ctx, cx, y, s=1.0, t=0.0, freno=0.0):
    """Luces traseras rojas del último camión, que se va."""
    ctx.save()
    ctx.translate(cx, y)
    ctx.scale(s, s)
    ovalo(ctx, 0, 6, 250, 18, (0, 0, 0), 0.5)
    fill_rrect(ctx, -210, -440, 420, 400, 30, mix(CAMION, (0.2, 0.2, 0.2), 0.3))
    fill_rrect(ctx, -170, -400, 340, 140, 12, (0.02, 0.025, 0.03))
    for sx in (-1, 1):
        fill_rrect(ctx, sx * 170 - 22, -190, 44, 86, 8, mix((0.15, 0.02, 0.02), ROJO, 0.7 + 0.3 * freno))
        glow(ctx, sx * 170, -146, 230, ROJO, 0.5 + 0.3 * freno, cairo.OPERATOR_SCREEN)
    ctx.restore()


def reflejo_en_vidrio(ctx, x, y, w, h, t, alpha=0.7):
    """Lo que devuelve el vidrio de la tienda: el interior de un camión con pasajeros sentados y, entre ellos, Iván."""
    ctx.save()
    ctx.rectangle(x, y, w, h)
    ctx.clip()
    fill_rrect(ctx, x, y, w, h, 0, mix((0.04, 0.05, 0.04), AMARILLO, 0.5), 0.6 * alpha)
    for k in range(5):
        px = x + 90 + k * (w - 180) / 4
        yy = y + h * 0.62
        col = (0.05, 0.06, 0.07) if k != 2 else (0.14, 0.22, 0.36)                                  # el del medio: la sudadera de Iván
        fill_rrect(ctx, px - 42, yy - 150, 84, 150, 28, col, alpha)
        ovalo(ctx, px, yy - 190, 30, 34, (0.2, 0.2, 0.2) if k != 2 else (0.5, 0.36, 0.3), alpha)
        fill_rrect(ctx, px - 60, yy, 120, 18, 6, (0.1, 0.12, 0.14), alpha * 0.8)
    for k in range(4):
        fill_rrect(ctx, x + 30 + k * (w - 90) / 3, y + 26, 80, 12, 4, mix(AMARILLO, (1, 1, 1), 0.3), 0.7 * alpha)
    ctx.restore()
