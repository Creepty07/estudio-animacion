"""Perros del hato: de cuerpo entero (ladrando o callados) y en primer plano."""
import math
from motor.primitives import clamp
from historias.silbon.dibujo import estilo as E
from historias.silbon.dibujo.caras import relleno_contorno, trazo, elipse


def perro(ctx, x, y, s, rgb, lado=1, ladra=0.0, callado=False, t=0.0, pecho=(0.88, 0.82, 0.70)):
    """Perro de lado con las patas en y. lado=1 mira a la derecha. ladra 0..1 abre el hocico; callado = orejas y cola abajo."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(lado * s, s)
    brinco = -6 * math.sin(t * 16) * ladra
    cola = -0.4 if callado else 0.7 + 0.3 * math.sin(t * 14) * (0.3 + ladra)
    ctx.new_path()                                                           # cola
    ctx.move_to(-105, -120)
    ctx.curve_to(-150, -120 - 60 * cola, -165, -150 - 60 * cola, -160, -170 - 60 * cola)
    ctx.set_line_width(26)
    ctx.set_source_rgb(*E.CONTORNO)
    ctx.set_line_cap(1)
    ctx.stroke_preserve()
    ctx.set_line_width(14)
    ctx.set_source_rgb(*rgb)
    ctx.stroke()
    for px in (-82, -44, 56, 92):                                            # patas
        ctx.new_path()
        ctx.rectangle(px - 13, -70, 26, 70)
        relleno_contorno(ctx, rgb, 1, 6)
    elipse(ctx, 0, -110 + brinco, 126, 60)                                   # cuerpo
    relleno_contorno(ctx, rgb, 1, 7)
    elipse(ctx, 70, -100 + brinco, 52, 40)                                   # pecho claro
    ctx.set_source_rgb(*pecho)
    ctx.fill()
    elipse(ctx, 0, -110 + brinco, 126, 60)
    trazo(ctx, 1, 7)
    hx, hy = 128, -152 + brinco
    ctx.new_path()                                                           # mandíbula inferior (se abre al ladrar)
    ctx.move_to(hx + 20, hy + 20)
    ctx.line_to(hx + 92, hy + 18 + 36 * ladra)
    ctx.line_to(hx + 84, hy + 38 + 36 * ladra)
    ctx.line_to(hx + 14, hy + 44)
    ctx.close_path()
    relleno_contorno(ctx, (0.45, 0.28, 0.18) if rgb[0] > 0.3 else rgb, 1, 6)
    if ladra > 0.25:
        ctx.new_path()
        ctx.move_to(hx + 22, hy + 22)
        ctx.line_to(hx + 90, hy + 20 + 34 * ladra)
        ctx.line_to(hx + 86, hy + 22)
        ctx.close_path()
        ctx.set_source_rgb(0.20, 0.03, 0.06)
        ctx.fill()
    ctx.new_path()
    ctx.arc(hx, hy, 56, 0, math.tau)                                         # cabeza
    relleno_contorno(ctx, rgb, 1, 7)
    ctx.new_path()                                                           # hocico
    ctx.move_to(hx + 22, hy - 4)
    ctx.line_to(hx + 98, hy + 2)
    ctx.line_to(hx + 94, hy + 24)
    ctx.line_to(hx + 20, hy + 26)
    ctx.close_path()
    relleno_contorno(ctx, rgb, 1, 7)
    ctx.new_path()
    ctx.arc(hx + 100, hy + 3, 12, 0, math.tau)                               # nariz
    ctx.set_source_rgb(*E.CONTORNO)
    ctx.fill()
    oreja = 30 if callado else 8
    ctx.new_path()
    ctx.move_to(hx - 22, hy - 40)
    ctx.curve_to(hx - 50, hy - 40 + oreja, hx - 50, hy + 20 + oreja, hx - 20, hy + 36 + oreja)
    ctx.curve_to(hx - 6, hy + 10, hx - 4, hy - 20, hx - 22, hy - 40)
    relleno_contorno(ctx, tuple(c * 0.62 for c in rgb), 1, 6.5)
    elipse(ctx, hx + 26, hy - 18, 17, 19 if not callado else 9)             # ojo
    relleno_contorno(ctx, (0.97, 0.97, 0.94), 1, 5)
    ctx.new_path()
    ctx.arc(hx + 30, hy - 16, 6, 0, math.tau)
    ctx.set_source_rgb(*E.CONTORNO)
    ctx.fill()
    ctx.new_path()
    ctx.move_to(hx + 8, hy - 44 + (6 if callado else 0))
    ctx.line_to(hx + 44, hy - 36 + (-6 if callado else 8))
    trazo(ctx, 1, 8)
    ctx.restore()


def perro_cabeza(ctx, x, y, s, rgb, ladra=0.0, t=0.0):
    """Primer plano de un perro que ladra, de frente: orejas caídas, ceño y colmillos."""
    sacude = 6 * s * math.sin(t * 22) * ladra
    ctx.save()
    ctx.translate(x + sacude, y)
    ctx.scale(s, s)
    for lado in (-1, 1):
        ctx.new_path()
        ctx.move_to(lado * 84, -100)
        ctx.curve_to(lado * 190, -120, lado * 200, 60, lado * 120, 110)
        ctx.curve_to(lado * 90, 60, lado * 80, -40, lado * 84, -100)
        relleno_contorno(ctx, tuple(c * 0.6 for c in rgb), 1, 7)
    ctx.new_path()
    ctx.arc(0, 0, 130, 0, math.tau)
    relleno_contorno(ctx, rgb, 1, 8)
    for lado in (-1, 1):
        elipse(ctx, lado * 52, -30, 27, 31)
        relleno_contorno(ctx, (0.97, 0.97, 0.94), 1, 5.5)
        ctx.new_path()
        ctx.arc(lado * 52, -26, 8, 0, math.tau)
        ctx.set_source_rgb(*E.CONTORNO)
        ctx.fill()
        ctx.new_path()
        ctx.move_to(lado * 92, -78)
        ctx.line_to(lado * 18, -58)
        trazo(ctx, 1, 11)
    elipse(ctx, 0, 52, 78, 58)                                               # hocico
    relleno_contorno(ctx, (0.86, 0.74, 0.58), 1, 7)
    abre = 14 + 40 * ladra
    ctx.new_path()                                                           # boca abierta
    ctx.move_to(-56, 58)
    ctx.curve_to(-40, 58 + abre * 1.3, 40, 58 + abre * 1.3, 56, 58)
    ctx.curve_to(30, 52, -30, 52, -56, 58)
    relleno_contorno(ctx, (0.22, 0.04, 0.07), 1, 6)
    for lado in (-1, 1):                                                     # colmillos
        ctx.new_path()
        ctx.move_to(lado * 40, 56)
        ctx.line_to(lado * 30, 56 + 26)
        ctx.line_to(lado * 22, 56)
        relleno_contorno(ctx, (0.97, 0.95, 0.88), 1, 4)
    elipse(ctx, 0, 26, 26, 17)                                               # nariz
    relleno_contorno(ctx, E.CONTORNO, 1, 4)
    ctx.restore()
