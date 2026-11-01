"""Personajes: Tito, Dani y los Centinelas. Origen = punto en el suelo bajo el personaje."""
import math
import cairo
from motor.primitives import (
    rrect, src, fill_rrect, fill_poly, line, circle, glow, font, text_at, TAU, mix,
)

# ---------------- TITO ----------------
TITO_BODY = (0.80, 0.85, 0.87)
TITO_SHADE = (0.62, 0.68, 0.71)
TITO_DARK = (0.14, 0.15, 0.17)
VISOR = (0.05, 0.07, 0.10)


def _tito_eyes(ctx, look, look_y, rgb, dilate=1.0):
    squash = 1 - 0.45 * abs(look)
    for side in (-1, 1):
        ex = side * 18 * squash + look * 15
        ey = -236 + look_y
        w, h = 20 * squash * dilate, 26 * dilate
        fill_rrect(ctx, ex - w / 2, ey - h / 2, w, h, w / 2, rgb)
        fill_rrect(ctx, ex - w / 2 + 3 * squash, ey - h / 2 + 4, w * 0.35, h * 0.3, 3, (1, 1, 1), 0.55)


def tito(ctx, x, y, s, look=0.0, look_y=0.0, eye_rgb=(0.3, 0.78, 1.0),
         antenna_rgb=(0.3, 0.78, 1.0), mop_swing=0.0, show_mop=True):
    """Dibuja a Tito y devuelve la matriz de su cabeza para el pase de brillo."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)

    # sombra
    ctx.save()
    ctx.scale(1, 0.18)
    circle(ctx, 0, 0, 95, (0, 0, 0), 0.45)
    ctx.restore()

    # trapeador (detrás del cuerpo)
    if show_mop:
        mx = -150 + mop_swing
        line(ctx, mx + 6, -8, -28, -182, 7, (0.55, 0.38, 0.22))
        for i in range(9):
            a = -0.9 + i * 0.22
            line(ctx, mx, -12, mx + math.sin(a) * 34, -2 + abs(math.cos(a)) * 2, 6, (0.78, 0.82, 0.86))
        fill_rrect(ctx, mx - 22, -24, 44, 14, 5, (0.25, 0.45, 0.65))

    # base y ruedas
    fill_rrect(ctx, -70, -44, 140, 34, 14, TITO_DARK)
    for wx in (-44, 44):
        circle(ctx, wx, -14, 17, (0.08, 0.08, 0.09))
        circle(ctx, wx, -14, 7, (0.5, 0.52, 0.55))

    # cuerpo con sombreado
    g = cairo.LinearGradient(-62, 0, 62, 0)
    g.add_color_stop_rgb(0, *TITO_BODY)
    g.add_color_stop_rgb(0.65, *TITO_BODY)
    g.add_color_stop_rgb(1, *TITO_SHADE)
    rrect(ctx, -62, -192, 124, 156, 28)
    ctx.set_source(g)
    ctx.fill()
    # banda amarilla con rejillas
    ctx.save()
    rrect(ctx, -62, -192, 124, 156, 28)
    ctx.clip()
    ctx.rectangle(-62, -122, 124, 22)
    src(ctx, (0.96, 0.74, 0.15))
    ctx.fill()
    for i in range(5):
        line(ctx, -40 + i * 20, -116, -46 + i * 20, -106, 4, (0.25, 0.2, 0.05), 0.6)
    ctx.restore()
    # rejilla frontal
    for i in range(3):
        line(ctx, -30, -80 + i * 12, 30, -80 + i * 12, 4, TITO_SHADE)
    # etiqueta "TITO" escrita a mano
    ctx.save()
    ctx.translate(-8, -158)
    ctx.rotate(-0.12)
    fill_rrect(ctx, -30, -14, 60, 24, 3, (0.97, 0.96, 0.9))
    font(ctx, 17, "Inter", bold=True)
    src(ctx, (0.1, 0.1, 0.12))
    text_at(ctx, "TITO", -22, 4)
    ctx.restore()
    # brazo que sostiene el trapeador
    if show_mop:
        mx = -150 + mop_swing
        hx = -28 + 0.35 * (mx + 6 + 28)
        hy = -182 + 0.35 * (-8 + 182)
        line(ctx, -50, -150, hx, hy, 14, TITO_SHADE)
        circle(ctx, hx, hy, 10, TITO_DARK)

    # cuello
    fill_rrect(ctx, -11, -208, 22, 20, 4, TITO_DARK)

    # cabeza
    head_dx = look * 5
    ctx.translate(head_dx, 0)
    g = cairo.LinearGradient(-58, 0, 58, 0)
    g.add_color_stop_rgb(0, *TITO_BODY)
    g.add_color_stop_rgb(0.7, *TITO_BODY)
    g.add_color_stop_rgb(1, *TITO_SHADE)
    rrect(ctx, -58, -272, 116, 70, 24)
    ctx.set_source(g)
    ctx.fill()
    # tornillos y costura
    for bx, by in ((-48, -262), (48, -262), (-48, -212), (48, -212)):
        circle(ctx, bx, by, 2.4, TITO_SHADE)
    line(ctx, -40, -207, 40, -207, 1.2, TITO_SHADE)
    # rayón
    line(ctx, 30, -268, 40, -264, 1.0, TITO_SHADE)
    # antena
    line(ctx, 18, -270, 26, -300, 4, TITO_DARK)
    circle(ctx, 26, -303, 6, antenna_rgb)
    # visor
    rrect(ctx, -46 + look * 4, -259, 92, 46, 17)
    src(ctx, VISOR)
    ctx.fill()
    ctx.save()
    rrect(ctx, -46 + look * 4, -259, 92, 46, 17)
    ctx.clip()
    fill_poly(ctx, [(-20, -262), (-6, -262), (-34, -208), (-48, -208)], (1, 1, 1), 0.08)
    ctx.restore()

    head_matrix = ctx.get_matrix()
    _tito_eyes(ctx, look, look_y, eye_rgb)
    ctx.restore()
    return head_matrix


def tito_glow(ctx, head_matrix, look, look_y, eye_rgb, eye_glow=0.6, antenna_rgb=None,
              antenna_glow=0.0, dilate=1.0):
    """Redibuja ojos y antena encima de cualquier filtro de luz, con su brillo."""
    ctx.save()
    ctx.set_matrix(head_matrix)
    _tito_eyes(ctx, look, look_y, eye_rgb, dilate)
    squash = 1 - 0.45 * abs(look)
    for side in (-1, 1):
        ex = side * 18 * squash + look * 15
        glow(ctx, ex, -236 + look_y, 34 * dilate, eye_rgb, eye_glow)
    if antenna_rgb is not None:
        circle(ctx, 26, -303, 6, antenna_rgb)
        glow(ctx, 26, -303, 26, antenna_rgb, antenna_glow)
    ctx.restore()


# ---------------- DANI ----------------
SKIN = (0.78, 0.55, 0.38)
SUIT = (0.88, 0.47, 0.17)
SUIT_DARK = (0.66, 0.33, 0.11)
PANTS = (0.16, 0.20, 0.30)
CAP = (0.10, 0.32, 0.38)


def dani(ctx, x, y, s, arm=0.0, breathe=0.0):
    """Dani de perfil, mirando a la izquierda, trabajando con un desarmador."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.save()
    ctx.scale(1, 0.18)
    circle(ctx, 0, 0, 80, (0, 0, 0), 0.45)
    ctx.restore()

    # piernas y botas
    fill_rrect(ctx, -28, -152, 24, 140, 8, PANTS)
    fill_rrect(ctx, 4, -152, 24, 140, 8, mix(PANTS, (0, 0, 0), 0.2))
    fill_rrect(ctx, -36, -18, 34, 18, 6, (0.12, 0.1, 0.09))
    fill_rrect(ctx, 0, -18, 34, 18, 6, (0.1, 0.08, 0.07))

    by = breathe * 2
    # brazo trasero
    line(ctx, -2, -250 + by, -18, -160, 18, SUIT_DARK)
    # torso
    rrect(ctx, -38, -272 + by, 76, 132 - by, 18)
    src(ctx, SUIT)
    ctx.fill()
    ctx.rectangle(-38, -196 + by, 76, 9)
    src(ctx, (0.9, 0.92, 0.88))
    ctx.fill()
    fill_rrect(ctx, -40, -152, 80, 13, 3, (0.25, 0.16, 0.1))
    fill_rrect(ctx, 14, -150, 18, 24, 4, (0.3, 0.2, 0.12))

    # cabeza
    hy = -302 + by
    circle(ctx, -4, hy, 30, SKIN)
    fill_poly(ctx, [(-33, hy - 2), (-42, hy + 6), (-32, hy + 9)], SKIN)  # nariz
    circle(ctx, -20, hy - 4, 3.2, (0.1, 0.07, 0.06))  # ojo
    fill_rrect(ctx, 8, hy - 8, 20, 30, 8, (0.13, 0.09, 0.07))  # pelo nuca
    circle(ctx, 8, hy + 2, 6, mix(SKIN, (0, 0, 0), 0.15))  # oreja
    # gorra
    ctx.arc(-4, hy - 6, 32, math.pi, TAU)
    ctx.close_path()
    src(ctx, CAP)
    ctx.fill()
    fill_rrect(ctx, -62, hy - 12, 46, 9, 4, mix(CAP, (0, 0, 0), 0.25))

    # brazo delantero con desarmador
    sx, sy = 4, -252 + by
    ex, ey = -24 + arm * 2, -206 + by
    hx, hy2 = -62 + arm * 6, -236 + by + math.sin(arm * 3) * 3
    line(ctx, sx, sy, ex, ey, 20, SUIT)
    line(ctx, ex, ey, hx, hy2, 18, SUIT)
    line(ctx, hx, hy2, hx - 22, hy2 - 2, 9, (0.95, 0.75, 0.1))
    line(ctx, hx - 22, hy2 - 2, hx - 44, hy2 - 3, 3, (0.75, 0.78, 0.8))
    circle(ctx, hx, hy2, 10, SKIN)
    ctx.restore()


# ---------------- CENTINELA ----------------
def sentinel(ctx, x, y, s, phase=0.0, body=(0.04, 0.035, 0.05), rim=(1.0, 0.2, 0.15),
             rim_a=0.35, eye_a=1.0, reach=0.0, look_up=0.0):
    """reach (0..1) levanta el brazo derecho hacia adelante; devuelve la posición de esa mano."""
    ctx.save()
    bob_y = y - abs(math.sin(phase)) * 7
    ctx.translate(x, bob_y)
    ctx.scale(s, s)
    sw = math.sin(phase)

    def shape(fn):
        fn()
        src(ctx, body)
        ctx.fill_preserve()
        ctx.set_line_width(3 / max(s, 0.2))
        src(ctx, rim, rim_a)
        ctx.stroke()

    def poly_leg():
        ctx.move_to(-22, 0)
        ctx.line_to(22, 0)
        ctx.line_to(16, 222)
        ctx.line_to(30, 235)
        ctx.line_to(-26, 235)
        ctx.line_to(-16, 222)
        ctx.close_path()

    def fill_torso():
        ctx.move_to(-128, -466)
        ctx.line_to(128, -466)
        ctx.line_to(66, -262)
        ctx.line_to(-66, -262)
        ctx.close_path()

    # piernas
    for side, k in ((-1, sw), (1, -sw)):
        ctx.save()
        ctx.translate(side * 34, -235)
        ctx.rotate(k * 0.13)
        shape(poly_leg)
        ctx.restore()

    def arm(side, angle):
        ctx.save()
        ctx.translate(side * 118, -452)
        ctx.rotate(angle)
        shape(lambda: rrect(ctx, -16, 0, 32, 215, 14))
        ctx.restore()

    reach_angle = sw * 0.1 * (1 - reach) - reach * 1.35
    # brazos (el que alcanza va al frente)
    arm(-1, -sw * 0.1)
    if reach <= 0:
        arm(1, reach_angle)
    # pelvis y torso
    shape(lambda: rrect(ctx, -60, -268, 120, 44, 10))
    shape(fill_torso)
    if reach > 0:
        arm(1, reach_angle)

    # cabeza y visor
    vy = -8 * look_up
    shape(lambda: rrect(ctx, -32, -528, 64, 58, 14))
    fill_rrect(ctx, -25, -506 + vy, 50, 11, 5, (1.0, 0.25, 0.18), eye_a)
    glow(ctx, 0, -500 + vy, 60, (1.0, 0.15, 0.1), 0.7 * eye_a)
    ctx.restore()
    hx = 118 - 205 * math.sin(reach_angle)
    hy = -452 + 205 * math.cos(reach_angle)
    return x + s * hx, bob_y + s * hy
