"""El Silbón (diseño original): figura altísima y flaca, sombrero enorme, saco de huesos al hombro y ojos que brillan."""
import math
from motor.primitives import glow, lerp
from historias.silbon.dibujo import estilo as E
from historias.silbon.dibujo.caras import relleno_contorno, trazo, elipse

ROPA = (0.045, 0.045, 0.07)
BORDE = (0.34, 0.44, 0.78)          # luz fría de la luna en el filo de la silueta
SACO = (0.26, 0.20, 0.15)


def _forma(ctx, s, rgb=ROPA, borde=BORDE, luz=1.0):
    """Rellena el trazado actual y le pone un filo claro (silueta legible contra el cielo)."""
    ctx.set_source_rgb(*rgb)
    ctx.fill_preserve()
    ctx.set_line_width(3.2 * s)
    ctx.set_line_join(1)
    ctx.set_source_rgba(*borde, 0.85 * luz)
    ctx.stroke()


def _hueso(ctx, x0, y0, x1, y1, s):
    ctx.new_path()
    ctx.move_to(x0, y0)
    ctx.line_to(x1, y1)
    ctx.set_line_cap(1)
    ctx.set_line_width(11 * s)
    ctx.set_source_rgb(*E.HUESO)
    ctx.stroke()
    for (px, py) in ((x1, y1),):                                      # nudo del hueso
        ctx.new_path()
        ctx.arc(px, py, 9 * s, 0, math.tau)
        ctx.fill()
        ctx.arc(px + 7 * s, py - 4 * s, 7 * s, 0, math.tau)
        ctx.fill()


def silbon(ctx, x, y, s, t=0.0, ojos=1.0, luz=1.0, balanceo=0.0):
    """Origen en los pies; mide ~830*s de alto. ojos 0..1 = brillo de los ojos; balanceo mueve el cuerpo de lado a lado."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.rotate(0.012 * math.sin(t * 1.4) + balanceo)
    # saco de huesos (detrás del cuerpo, sobre el hombro derecho)
    ctx.new_path()
    ctx.move_to(40, -610)
    ctx.curve_to(150, -650, 190, -520, 120, -430)
    ctx.curve_to(80, -390, 30, -420, 20, -500)
    ctx.close_path()
    _forma(ctx, 1, SACO, (0.5, 0.42, 0.3), luz)
    for ang, largo in ((-0.5, 70), (-0.1, 84), (0.35, 62)):            # huesos que asoman por la boca del saco
        _hueso(ctx, 105, -560, 105 + math.sin(ang) * largo, -560 - math.cos(ang) * largo, 1)
    # piernas larguísimas
    for lado in (-1, 1):
        ctx.new_path()
        ctx.move_to(lado * 22, -330)
        ctx.line_to(lado * 36 + 6 * math.sin(t * 1.4 + lado), 0)
        ctx.set_line_width(26)
        ctx.set_line_cap(1)
        ctx.set_source_rgb(*ROPA)
        ctx.stroke()
        elipse(ctx, lado * 40 + 12, 0, 34, 12)
        _forma(ctx, 1, ROPA, BORDE, luz)
    # abrigo largo
    ctx.new_path()
    ctx.move_to(-52, -640)
    ctx.line_to(52, -640)
    ctx.curve_to(70, -500, 86, -380, 92, -290)
    ctx.line_to(-92, -290)
    ctx.curve_to(-86, -380, -70, -500, -52, -640)
    _forma(ctx, 1, ROPA, BORDE, luz)
    # brazos que llegan a las rodillas, con dedos de araña
    for lado in (-1, 1):
        mano = (lado * 98 + 8 * math.sin(t * 1.4 + lado), -250)
        ctx.new_path()
        ctx.move_to(lado * 50, -630)
        ctx.curve_to(lado * 100, -520, lado * 112, -380, mano[0], mano[1])
        ctx.set_line_width(20)
        ctx.set_line_cap(1)
        ctx.set_source_rgb(*ROPA)
        ctx.stroke()
        for k in range(-2, 3):
            ctx.new_path()
            ctx.move_to(mano[0], mano[1])
            ctx.line_to(mano[0] + k * 12, mano[1] + 70 - abs(k) * 8)
            ctx.set_line_width(5)
            ctx.set_source_rgb(*E.HUESO)
            ctx.stroke()
    # cabeza bajo el sombrero y ojos
    elipse(ctx, 0, -690, 40, 54)
    _forma(ctx, 1, (0.03, 0.03, 0.05), BORDE, luz)
    # sombrero de ala ancha
    ctx.new_path()
    ctx.move_to(-66, -728)
    ctx.curve_to(-62, -830, 62, -830, 66, -728)
    ctx.close_path()
    _forma(ctx, 1, ROPA, BORDE, luz)
    elipse(ctx, 0, -724, 168, 26)
    _forma(ctx, 1, ROPA, BORDE, luz)
    if ojos > 0.02:
        for lado in (-1, 1):
            ex, ey = lado * 17, -698
            glow(ctx, ex, ey, 70 * ojos, (1.0, 0.85, 0.35), 0.8 * ojos)
            elipse(ctx, ex, ey, 11, 7.5 * min(1.0, ojos * 1.3))
            ctx.set_source_rgb(1.0, 0.97, 0.7)
            ctx.fill()
    ctx.restore()


def ojo_en_rendija(ctx, x, y, s, t=0.0, abierto=1.0, mira=0.0):
    """El ojo del Silbón visto por una rendija: enorme, amarillento, con venas y pupila de rendija."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    glow(ctx, 0, 0, 340, (1.0, 0.78, 0.25), 0.55 * abierto)
    h = 118 * max(abierto, 0.03)
    elipse(ctx, 0, 0, 190, h)
    ctx.set_source_rgb(1.0, 0.94, 0.62)
    ctx.fill_preserve()
    ctx.set_line_width(9)
    ctx.set_source_rgb(0.05, 0.03, 0.03)
    ctx.stroke()
    if abierto > 0.2:
        ctx.save()
        elipse(ctx, 0, 0, 190, h)
        ctx.clip()
        for i in range(9):                                            # venas
            a = math.tau * i / 9 + 0.3
            ctx.new_path()
            ctx.move_to(math.cos(a) * 190, math.sin(a) * h * 1.2)
            ctx.line_to(math.cos(a) * 80, math.sin(a) * h * 0.5)
            ctx.set_line_width(3)
            ctx.set_source_rgba(0.78, 0.2, 0.15, 0.55)
            ctx.stroke()
        px = mira * 70
        elipse(ctx, px, 0, 42, h * 0.9)
        ctx.set_source_rgb(0.03, 0.02, 0.02)
        ctx.fill()
        elipse(ctx, px, 0, 9, h * 0.8)
        ctx.set_source_rgb(1, 0.95, 0.7)
        ctx.fill()
        ctx.restore()
    ctx.restore()
