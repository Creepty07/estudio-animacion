"""Interior del camión sin número, en corte lateral. Mundo de 2700 px de ancho (el frente y el chofer a la derecha).
Las escenas lo encuadran con `cam()`, que no deja ver fuera del dibujo."""
import math
import random
import cairo
from motor.primitives import (src, line, circle, glow, fill_rrect, fill_poly, rrect, seg, smooth, lerp, mix, clamp, font, text_center, text_at,
                              text_w, camera_center, TAU)
from historias.ruta0.dibujo.paleta import (ovalo, degradado_v, trazo, parpadeo, AMARILLO, AMARILLO_OSC, AMBAR, AMBAR_CLARO, ROJO, HIERRO,
                                           ASIENTO, ASIENTO_CLARO, PIEL_MUERTA, PIEL_VIVA, CABELLO, SUDADERA, JEAN, CAMION_OSC)

ANCHO = 2700
PISO = 1270            # suelo del pasillo
CADERA = 1120          # altura de la cadera de quien va sentado
ASIENTOS = [330, 600, 870, 1140, 1410, 1680, 1950]
X_CHOFER = 2420
X_PUERTA = 2200


def cam(ctx, z, cx, cy, dx=0.0, dy=0.0):
    """Cámara que no se sale del interior (0..ANCHO de ancho, 0..1920 de alto)."""
    hx, hy = 540 / z, 960 / z
    camera_center(ctx, z, min(max(cx, hx), ANCHO - hx), min(max(cy, hy), 1920 - hy), dx, dy)


def tubo(ctx, x, y, w, b):
    fill_rrect(ctx, x - 6, y - 5, w + 12, 24, 5, (0.07, 0.08, 0.08))
    fill_rrect(ctx, x, y, w, 14, 5, mix((0.2, 0.2, 0.15), (1.0, 0.95, 0.6), b))
    if b > 0.05:
        glow(ctx, x + w / 2, y + 8, w * 0.8, AMARILLO, 0.35 * b, cairo.OPERATOR_SCREEN)


def ventana_exterior(ctx, x, y, w, h, t, vel=1.0, seed=0, lluvia=1.0, vaho=0.0, vidrio=1.0):
    """Una ventana: la noche corre afuera (luces borrosas que pasan) y la lluvia resbala en el vidrio."""
    ctx.save()
    ctx.rectangle(x, y, w, h)
    ctx.clip()
    degradado_v(ctx, x, y, w, h, (0.005, 0.012, 0.025), (0.03, 0.06, 0.09))
    r = random.Random(seed)
    for i in range(3):                                                                       # luces de la calle que pasan
        px = (x + w - ((t * 150 * vel + r.uniform(0, 600)) % (w + 200))) + 60
        glow(ctx, px, y + r.uniform(0.35, 0.8) * h, 60 + r.uniform(0, 40), (0.9, 0.75, 0.4) if i % 2 else (0.7, 0.85, 1.0), 0.45, cairo.OPERATOR_SCREEN)
    for i in range(int(9 * lluvia)):                                                         # gotas que resbalan
        gx = x + r.uniform(0.05, 0.95) * w
        gy = y + ((r.uniform(0, 1) * h + t * r.uniform(40, 110)) % h)
        line(ctx, gx, gy, gx + 2, gy + r.uniform(14, 40), 2.4, (0.8, 0.9, 1.0), 0.28)
    if vaho > 0:
        glow(ctx, x + w * 0.5, y + h * 0.55, w * 0.8, (0.85, 0.92, 1.0), 0.55 * vaho, cairo.OPERATOR_OVER)
        src(ctx, (0.8, 0.88, 0.95), 0.25 * vaho)
        ctx.rectangle(x, y, w, h)
        ctx.fill()
    g = cairo.LinearGradient(x, y, x + w, y + h)
    g.add_color_stop_rgba(0, 1, 1, 1, 0.09)
    g.add_color_stop_rgba(0.5, 1, 1, 1, 0.0)
    ctx.set_source(g)
    ctx.paint()
    ctx.restore()
    ctx.set_line_width(14)
    src(ctx, (0.05, 0.06, 0.07))
    ctx.rectangle(x, y, w, h)
    ctx.stroke()


def fondo(ctx, t, luz=1.0, vel=1.0, seed=1, flicker=True):
    """Paredes, piso, ventanas, tubos amarillos que parpadean, barras para agarrarse."""
    b = (lambda s: parpadeo(t, seed * 7 + s, 0.16)) if flicker else (lambda s: 1.0)
    base = 0.30 + 0.7 * luz
    degradado_v(ctx, 0, 0, ANCHO, PISO, mix((0.04, 0.05, 0.05), (0.14, 0.15, 0.12), base * 0.6), mix((0.07, 0.075, 0.07), (0.20, 0.20, 0.15), base * 0.7))
    fill_rrect(ctx, 0, 380, ANCHO, 60, 0, (0.05, 0.055, 0.055))                                # dintel arriba de las ventanas
    fill_rrect(ctx, 0, 850, ANCHO, 420, 0, mix((0.05, 0.055, 0.05), (0.13, 0.13, 0.1), base * 0.5))   # tablero bajo ventanas
    degradado_v(ctx, 0, PISO, ANCHO, 1920 - PISO, (0.04, 0.045, 0.045), (0.01, 0.012, 0.012))
    for x in range(40, ANCHO, 60):
        line(ctx, x, PISO + 4, x + 18, 1920, 3, (0.015, 0.02, 0.02), 0.6)
    for i, ax in enumerate(ASIENTOS):
        ventana_exterior(ctx, ax - 120, 470, 240, 330, t, vel, seed + i)
    ventana_exterior(ctx, 2080, 470, 240, 330, t, vel, seed + 20)
    for i in range(7):
        tubo(ctx, 150 + i * 380, 300, 170, b(i) * luz)
    line(ctx, 0, 410, ANCHO, 410, 10, (0.55, 0.58, 0.55), 0.55)                                 # barra de agarre
    for x in (430, 1090, 1750):
        line(ctx, x, 410, x, PISO - 20, 9, (0.5, 0.52, 0.5), 0.5)
    if luz > 0.05:                                                                              # luz amarilla enferma sobre todo
        degradado_v(ctx, 0, 300, ANCHO, 900, AMARILLO, AMARILLO, 0.07 * luz, 0.0)


def asiento(ctx, x, vacio=False):
    fill_rrect(ctx, x - 78, CADERA - 250, 40, 290, 14, ASIENTO)                                  # respaldo (el pasajero mira a la derecha)
    fill_rrect(ctx, x - 64, CADERA - 250, 16, 250, 8, ASIENTO_CLARO, 0.4)
    fill_rrect(ctx, x - 70, CADERA, 170, 36, 12, ASIENTO)                                        # cojín
    fill_rrect(ctx, x - 64, CADERA, 160, 10, 5, ASIENTO_CLARO, 0.5)
    line(ctx, x - 10, CADERA + 36, x - 10, PISO, 10, (0.03, 0.035, 0.04))
    if vacio:
        glow(ctx, x + 10, CADERA - 80, 160, AMARILLO, 0.05, cairo.OPERATOR_SCREEN)


TIPOS = {
    "traje": {"torso": (0.07, 0.07, 0.10), "detalle": (0.82, 0.84, 0.86), "pelo": (0.05, 0.05, 0.06)},
    "vestido": {"torso": (0.34, 0.12, 0.38), "detalle": (0.82, 0.7, 0.7), "pelo": (0.04, 0.03, 0.04)},
    "domingo": {"torso": (0.70, 0.68, 0.60), "detalle": (0.30, 0.2, 0.12), "pelo": (0.30, 0.3, 0.32)},
    "senora": {"torso": (0.22, 0.24, 0.30), "detalle": (0.5, 0.5, 0.55), "pelo": (0.6, 0.6, 0.64)},
    "gala": {"torso": (0.10, 0.16, 0.30), "detalle": (0.85, 0.85, 0.9), "pelo": (0.05, 0.04, 0.04)},
    "obrero": {"torso": (0.30, 0.27, 0.18), "detalle": (0.5, 0.4, 0.2), "pelo": (0.08, 0.07, 0.06)},
    "pasajera": {"torso": (0.26, 0.33, 0.34), "detalle": (0.5, 0.5, 0.5), "pelo": (0.04, 0.03, 0.04)},
}


def _cabeza(ctx, tipo, giro, pelo):
    """Cabeza de perfil (mira a la derecha). giro 1 = vuelta hacia la cámara, con la cara de frente."""
    c = PIEL_MUERTA
    if giro < 0.5:
        ovalo(ctx, 0, 0, 36, 42, c)
        ovalo(ctx, -10, -14, 36, 30, pelo)
        ovalo(ctx, 30, 6, 7, 9, mix(c, (0, 0, 0), 0.12))                                       # nariz
        circle(ctx, 14, -6, 4.2, (0.92, 0.94, 0.95))
        circle(ctx, 15.5, -6, 2.2, (0.03, 0.03, 0.04))
        line(ctx, 16, 22, 30, 21, 3, (0.25, 0.18, 0.18))
    else:
        ovalo(ctx, 0, 0, 42, 46, c)
        ovalo(ctx, 0, -20, 44, 30, pelo)
        for sx in (-1, 1):
            ovalo(ctx, sx * 16, -4, 9, 6, (0.02, 0.02, 0.03), 0.95)                            # ojos en sombra
        line(ctx, -12, 26, 12, 26, 3, (0.22, 0.16, 0.16))


def pasajero(ctx, x, tipo="traje", t=0.0, giro=0.0, alpha=1.0, mano=None):
    """Pasajero quieto, sentado, mirando al frente. Origen en (x, CADERA). No respira ni parpadea."""
    d = TIPOS[tipo]
    if alpha < 1.0:
        ctx.push_group()
    ctx.save()
    ctx.translate(x, CADERA)
    trazo(ctx, [(0, 0), (86, -4), (100, 104)], 36, (0.05, 0.06, 0.08))                         # pierna
    ovalo(ctx, 104, 124, 34, 12, (0.02, 0.02, 0.03))
    fill_rrect(ctx, -38, -176, 76, 186, 28, d["torso"])                                         # torso
    if tipo == "traje":
        fill_poly(ctx, [(10, -170), (34, -170), (26, -70), (14, -70)], d["detalle"])
        fill_poly(ctx, [(16, -168), (24, -168), (21, -96)], (0.1, 0.12, 0.3))
    elif tipo == "domingo":
        fill_rrect(ctx, -2, -170, 38, 110, 10, d["detalle"], 0.8)
    elif tipo == "vestido":
        fill_poly(ctx, [(-38, 0), (92, 6), (86, 36), (-38, 30)], d["torso"])
        circle(ctx, 22, -150, 5, (0.9, 0.8, 0.6))
    elif tipo == "senora":
        fill_poly(ctx, [(-40, -170), (40, -150), (46, -10), (-40, 10)], (0.3, 0.3, 0.36))
    trazo(ctx, [(2, -148), (46, -96), (74, -62)], 24, d["torso"])                                # brazo sobre la pierna
    circle(ctx, 78, -58, 13, PIEL_MUERTA)
    ctx.save()
    ctx.translate(6, -216)
    ctx.rotate(-0.05 * giro)
    fill_rrect(ctx, -10, 24, 20, 30, 6, mix(PIEL_MUERTA, (0, 0, 0), 0.15))
    _cabeza(ctx, tipo, giro, d["pelo"])
    ctx.restore()
    ctx.restore()
    if alpha < 1.0:
        ctx.pop_group_to_source()
        ctx.paint_with_alpha(alpha)


def ivan(ctx, x, t=0.0, sentado=True, aliento=1.0, mochila=True, y=None):
    """Iván sentado (sudadera, mochila en las piernas). Él sí respira y su aliento se ve."""
    y = CADERA if y is None else y
    ctx.save()
    ctx.translate(x, y)
    pecho = 1 + 0.018 * math.sin(t * 2.4)
    trazo(ctx, [(0, 0), (90, -2), (104, 108)], 38, JEAN)
    ovalo(ctx, 108, 126, 36, 13, (0.9, 0.9, 0.92))
    ctx.save()
    ctx.scale(1, pecho)
    fill_rrect(ctx, -40, -178, 80, 190, 30, SUDADERA)
    ctx.restore()
    ovalo(ctx, 0, -164, 40, 20, mix(SUDADERA, (0, 0, 0), 0.3))                                   # capucha
    if mochila:
        fill_rrect(ctx, 20, -78, 76, 92, 14, (0.12, 0.1, 0.09))
        line(ctx, 26, -50, 90, -50, 4, (0.3, 0.25, 0.2), 0.8)
    trazo(ctx, [(2, -148), (46, -96), (76, -74)], 26, SUDADERA)
    circle(ctx, 80, -72, 14, PIEL_VIVA)
    ctx.save()
    ctx.translate(6, -216)
    ovalo(ctx, 0, 0, 36, 42, PIEL_VIVA)
    ovalo(ctx, -8, -16, 38, 28, CABELLO)
    ovalo(ctx, 30, 6, 7, 9, mix(PIEL_VIVA, (0, 0, 0), 0.12))
    circle(ctx, 14, -6, 4.6, (0.96, 0.96, 0.96))
    circle(ctx, 15.8, -6, 2.4, (0.05, 0.03, 0.03))
    line(ctx, 16, 22, 28, 21, 3, (0.3, 0.14, 0.12))
    ctx.restore()
    ctx.restore()
    if aliento > 0:                                                                              # vaho que sale de su boca
        for i in range(5):
            f = (t * 0.6 + i / 5) % 1.0
            glow(ctx, x + 46 + 40 * f, y - 190 - 50 * f, 18 + 46 * f, (0.85, 0.95, 1.0), 0.3 * aliento * (1 - f), cairo.OPERATOR_OVER)


def chofer(ctx, x=X_CHOFER, t=0.0, brazo=0.0, gorra=True):
    """El chofer: nunca se le ve la cara (de espaldas / a contraluz). brazo 0..1 extiende el brazo hacia atrás con un boleto."""
    ctx.save()
    ctx.translate(x, CADERA)
    fill_rrect(ctx, -60, -280, 120, 330, 20, (0.03, 0.035, 0.04))                               # asiento del chofer
    fill_rrect(ctx, -34, -190, 78, 200, 26, (0.05, 0.06, 0.08))                                  # espalda
    ovalo(ctx, 6, -222, 38, 44, (0.02, 0.022, 0.025))                                            # cabeza en sombra
    if gorra:
        fill_rrect(ctx, -30, -258, 76, 20, 8, (0.02, 0.025, 0.03))
        fill_rrect(ctx, 30, -246, 36, 8, 4, (0.02, 0.025, 0.03))
    trazo(ctx, [(0, -150), (-40 - 130 * brazo, -90 + 30 * brazo), (-70 - 250 * brazo, -70 + 80 * brazo)], 24, (0.07, 0.08, 0.1))
    circle(ctx, -74 - 250 * brazo, -68 + 80 * brazo, 12, (0.46, 0.34, 0.28))
    if brazo > 0.3:
        fill_rrect(ctx, -110 - 250 * brazo, -60 + 80 * brazo, 34, 22, 2, (0.9, 0.88, 0.8))      # el boleto
    ctx.restore()
    ctx.save()                                                                                   # volante y tablero
    ctx.translate(x + 140, CADERA - 120)
    ovalo(ctx, 0, 0, 18, 70, (0.04, 0.045, 0.05), 1.0, -0.3)
    line(ctx, 0, 40, -70, 130, 10, (0.04, 0.045, 0.05))
    ctx.restore()


def tablero_ruta(ctx, x=2400, y=470, enc=(1, 1, 1, 1), t=0.0, ivan_flash=0.0, escala=1.0):
    """Tablero luminoso arriba del chofer: paradas de la ruta. enc = cuáles están encendidas; la última dice IVÁN."""
    nombres = ["TERMINAL", "CURVA DEL AHORCADO", "PUENTE VIEJO", "IVÁN"]
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(escala, escala)
    fill_rrect(ctx, -270, -30, 540, 340, 12, (0.02, 0.025, 0.03))
    fill_rrect(ctx, -260, -20, 520, 320, 8, (0.045, 0.05, 0.05))
    line(ctx, -210, 34, -210, 244, 6, (0.18, 0.2, 0.2))                                            # la línea de la ruta con sus focos
    for i, (n, e) in enumerate(zip(nombres, enc)):
        yy = 20 + i * 70
        es_ivan = (i == 3)
        col = AMBAR if es_ivan else AMARILLO
        e = e * (1 - 0.5 * (0.5 + 0.5 * math.sin(t * 30)) * ivan_flash if es_ivan else 1) if e else 0
        circle(ctx, -210, yy + 14, 11, mix((0.12, 0.12, 0.1), col, e))
        if e > 0.05:
            glow(ctx, -210, yy + 14, 60, col, 0.5 * e, cairo.OPERATOR_SCREEN)
        font(ctx, 31 if not es_ivan else 42, "Inter", bold=True)
        src(ctx, mix((0.2, 0.2, 0.18), col, e))
        text_at(ctx, n, -182, yy + 26, 0.5)
    ctx.restore()


def boton_parada(ctx, x, y, s=1.0, foco=0.0, presionado=0.0, t=0.0):
    """Barra con el botón de "PARADA" y el foco rojo del tablero."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    fill_rrect(ctx, -90, -16, 180, 32, 8, (0.78, 0.8, 0.4), 0.9)
    fill_rrect(ctx, -40, -34, 80, 60, 16, (0.55, 0.06, 0.07) if foco < 0.2 else (0.9, 0.1, 0.1))
    circle(ctx, 0, -4 + 6 * presionado, 24, mix((0.5, 0.05, 0.06), ROJO, 0.4 + 0.5 * (1 - presionado)))
    font(ctx, 16, "Inter", bold=True)
    src(ctx, (0.1, 0.1, 0.05))
    text_center(ctx, "PARADA", 0, 44)
    ctx.restore()


def foco_parada(ctx, x, y, foco, t=0.0):
    """Foco rojo de "SE SOLICITA PARADA" sobre el parabrisas."""
    fill_rrect(ctx, x - 120, y - 24, 240, 48, 10, (0.06, 0.03, 0.03))
    f = foco * (0.6 + 0.4 * (0.5 + 0.5 * math.sin(t * 9)))
    fill_rrect(ctx, x - 108, y - 14, 216, 28, 6, mix((0.15, 0.03, 0.03), ROJO, f))
    font(ctx, 20, "Inter", bold=True)
    src(ctx, mix((0.3, 0.1, 0.1), (1, 0.85, 0.85), f))
    text_center(ctx, "SE SOLICITA PARADA", x, y + 7, 2)
    glow(ctx, x, y, 320, ROJO, 0.6 * f, cairo.OPERATOR_SCREEN)


# ------------------------------------------------------------------ primeros planos (cuadro completo)
def ventanas_vaho(ctx, t, aliento=1.0):
    """Dos vidrios: el de Iván se empaña con su aliento; el del pasajero de al lado sigue limpio. Ojos que no parpadean abajo."""
    for k, (x, vaho) in enumerate(((70, aliento * (0.5 + 0.5 * math.sin(t * 2.4)) ** 0.5), (570, 0.0))):
        ventana_exterior(ctx, x, 420, 440, 600, t, 0.8, 30 + k, 1.0, vaho)
    for x, c in ((290, (0.86, 0.9, 0.9)), (790, (0.7, 0.72, 0.7))):                           # perfiles en el borde inferior
        fill_rrect(ctx, x - 120, 1040, 240, 300, 50, (0.05, 0.06, 0.08))
        ovalo(ctx, x, 1010, 58, 68, c if x < 500 else PIEL_MUERTA)
        circle(ctx, x + 22, 1000, 7, (0.95, 0.96, 0.96))
        circle(ctx, x + 24, 1000, 3.6, (0.02, 0.02, 0.03))


def mano_muneca(ctx, t, cx=540, cy=900, s=1.0, apretar=1.0):
    """Mano pálida que agarra una muñeca cálida (la de Iván)."""
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(s, s)
    trazo(ctx, [(-540, 140), (-120, 40)], 150, SUDADERA)                                        # manga de Iván
    trazo(ctx, [(-190, 56), (80, 6)], 108, PIEL_VIVA)                                           # su muñeca
    for k in range(4):                                                                          # dedos pálidos que rodean
        ctx.save()
        ctx.translate(-70 + k * 46, -66 + k * 6)
        ctx.rotate(1.25)
        fill_rrect(ctx, -10, -26, 180 - 10 * apretar, 52, 26, PIEL_MUERTA)
        ctx.restore()
    ovalo(ctx, -10, -10, 150, 86, PIEL_MUERTA, 1.0, -0.12)
    ctx.save()
    ctx.translate(-120, 20)
    ctx.rotate(0.6)
    fill_rrect(ctx, 0, -28, 150, 56, 28, PIEL_MUERTA)                                           # pulgar
    ctx.restore()
    trazo(ctx, [(620, -240), (150, -40)], 120, (0.3, 0.2, 0.34))                                # manga de la pasajera
    ctx.restore()


def cara_pasajera(ctx, t, cx=540, cy=820, s=1.0, giro=1.0):
    """La pasajera de frente, pálida y triste, sin respirar; los ojos en sombra."""
    ctx.save()
    ctx.translate(cx, cy)
    ctx.scale(s, s)
    fill_rrect(ctx, -250, 160, 500, 600, 120, (0.26, 0.33, 0.34))                               # vestido
    ovalo(ctx, 0, 110, 70, 64, mix(PIEL_MUERTA, (0, 0, 0), 0.2))
    ovalo(ctx, 0, -20, 150, 180, (0.04, 0.03, 0.04))                                             # pelo detrás
    ovalo(ctx, 0, 0, 120, 150, PIEL_MUERTA)
    ovalo(ctx, 0, -110, 124, 74, (0.04, 0.03, 0.04))
    for sx in (-1, 1):
        ovalo(ctx, sx * 48, -6, 30, 18, (0.02, 0.02, 0.03), 0.95)                               # ojos en sombra
        ovalo(ctx, sx * 48, 24, 34, 8, (0.28, 0.3, 0.36), 0.5)                                  # ojeras
    line(ctx, 0, 10, 8, 62, 5, mix(PIEL_MUERTA, (0, 0, 0), 0.35), 0.8)
    ctx.move_to(-30, 98)
    ctx.curve_to(-14, 88, 14, 88, 30, 98)                                                        # boca triste
    ctx.set_line_width(5)
    src(ctx, (0.3, 0.2, 0.22))
    ctx.stroke()
    g = cairo.LinearGradient(0, -90, 0, 40)                                                      # sombra sobre los ojos
    g.add_color_stop_rgba(0, 0, 0, 0, 0.55)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.0)
    ctx.save()
    ovalo_clip = ctx.arc(0, 0, 120, 0, TAU)
    ctx.clip()
    ctx.rectangle(-130, -110, 260, 150)
    ctx.set_source(g)
    ctx.fill()
    ctx.restore()
    ctx.restore()


def boleto(ctx, cx, cy, s=1.0, fecha="03 NOV", glitch=0.0, t=0.0, rot=-0.06):
    """Boleto de papel: "RUTA 0 · VÁLIDO: <fecha>"."""
    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(rot)
    ctx.scale(s, s)
    fill_rrect(ctx, -300, -150, 600, 300, 12, (0.02, 0.02, 0.02), 0.4)
    fill_rrect(ctx, -310, -160, 600, 300, 12, (0.9, 0.88, 0.78))
    for k in range(10):
        circle(ctx, -310 + 30 + k * 60, -160, 8, (0.02, 0.02, 0.03), 0.9)                       # perforación
    font(ctx, 62, "Inter Display Black")
    src(ctx, (0.12, 0.1, 0.08))
    text_center(ctx, "RUTA 0", -10, -62, 4)
    line(ctx, -260, -36, 240, -36, 4, (0.2, 0.18, 0.14), 0.7)
    font(ctx, 34, "DejaVu Sans Mono", bold=True)
    src(ctx, (0.22, 0.2, 0.16))
    text_center(ctx, "VÁLIDO:", -10, 12)
    font(ctx, 78, "DejaVu Sans Mono", bold=True)
    gx = random.Random(int(t * 30)).uniform(-16, 16) * glitch
    if glitch > 0:
        ctx.save()
        ctx.set_operator(cairo.OPERATOR_ADD)
        src(ctx, (1, 0, 0), 0.8 * glitch)
        text_center(ctx, fecha, -10 + gx - 8, 100)
        src(ctx, (0, 1, 1), 0.8 * glitch)
        text_center(ctx, fecha, -10 + gx + 8, 100)
        ctx.restore()
    src(ctx, (0.5, 0.06, 0.06) if glitch > 0 else (0.12, 0.1, 0.08))
    text_center(ctx, fecha, -10 + gx, 100)
    ctx.restore()


def celular(ctx, cx, cy, s=1.0, t=0.0, linea1="", linea2="", brillo=1.0, vibra=0.0, remitente=""):
    """Celular de Iván: fecha de hoy o el mensaje de Beto. vibra 0..1 lo hace temblar."""
    ctx.save()
    ctx.translate(cx + (random.Random(int(t * 40)).uniform(-5, 5) * vibra), cy)
    ctx.scale(s, s)
    ctx.rotate(0.04)
    fill_rrect(ctx, -230, -430, 460, 860, 54, (0.01, 0.012, 0.015))
    fill_rrect(ctx, -214, -414, 428, 828, 44, mix((0.03, 0.05, 0.08), (0.12, 0.2, 0.3), brillo))
    glow(ctx, 0, 0, 700, (0.4, 0.65, 0.95), 0.2 * brillo, cairo.OPERATOR_SCREEN)
    if remitente:
        fill_rrect(ctx, -190, -300, 380, 190, 26, (0.16, 0.26, 0.4), 0.95)
        font(ctx, 28, "Inter", bold=True)
        src(ctx, (0.6, 0.8, 1.0))
        text_at(ctx, remitente, -166, -250)
        font(ctx, 34, "Inter", bold=True)
        src(ctx, (0.96, 0.98, 1.0))
        for i, ln in enumerate((linea1, linea2)):
            text_at(ctx, ln, -166, -200 + i * 52)
    else:
        font(ctx, 150, "Inter Display Black")
        src(ctx, (0.95, 0.98, 1.0))
        text_center(ctx, linea1, 0, -100)
        font(ctx, 40, "Inter", bold=True)
        src(ctx, (0.7, 0.85, 1.0))
        text_center(ctx, linea2, 0, -30)
    ctx.restore()


def de_pie(ctx, x, y, s=1.0, tipo="obrero", alpha=1.0, mira=1):
    """Pasajero que se bajó: de pie, quieto, de frente, en la orilla. (x, y) = suelo bajo sus pies. Sin sombra: no pisa del todo."""
    d = TIPOS[tipo]
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    if alpha < 1.0:
        ctx.push_group()
    for sx in (-1, 1):
        fill_rrect(ctx, sx * 26 - 20, -190, 40, 186, 16, (0.05, 0.06, 0.08))
        ovalo(ctx, sx * 28, -4, 28, 11, (0.02, 0.02, 0.03))
    if tipo == "vestido":
        fill_poly(ctx, [(-50, -330), (50, -330), (96, -100), (-96, -100)], d["torso"])
    else:
        fill_rrect(ctx, -56, -380, 112, 220, 34, d["torso"])
    for sx in (-1, 1):
        trazo(ctx, [(sx * 54, -350), (sx * 70, -250), (sx * 62, -170)], 28, d["torso"])
        circle(ctx, sx * 62, -156, 15, PIEL_MUERTA)
    fill_rrect(ctx, -12, -404, 24, 36, 6, mix(PIEL_MUERTA, (0, 0, 0), 0.15))
    ovalo(ctx, 0, -440, 38, 46, PIEL_MUERTA)
    ovalo(ctx, 0, -462, 40, 28, d["pelo"])
    for sx in (-1, 1):
        circle(ctx, sx * 14, -440, 4.6, (0.93, 0.95, 0.95))
        circle(ctx, sx * 14, -440, 2.4, (0.02, 0.02, 0.03))
    line(ctx, -9, -414, 9, -414, 3, (0.25, 0.18, 0.18))
    if alpha < 1.0:
        ctx.pop_group_to_source()
        ctx.paint_with_alpha(alpha)
    ctx.restore()
