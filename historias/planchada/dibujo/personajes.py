"""Personajes de La Planchada (diseños originales).

Rafa (19 años, paciente) · Eulalia, la enfermera de blanco (la Planchada) · la enfermera de turno (uniforme moderno azul).
Rafa se dibuja con el origen en el centro de su cabeza sobre la almohada; Eulalia y la enfermera de turno, con el origen
en el suelo bajo sus pies.
"""
import math
import random
import cairo
from motor.primitives import (src, line, circle, glow, fill_rrect, fill_poly, seg, smooth, lerp, TAU, mix, clamp)
from historias.planchada.dibujo.paleta import (ovalo, trazo_grueso, BLANCO, UNIFORME_SOMBRA, CAPA, PIEL, PIEL_PALIDA, CABELLO, BATA,
                                               COBIJA, SABANA, HALO, SCRUB, SCRUB_OSC, FLUO)


# =========================================================== Rafa
def _cara_rafa(ctx, t, ojos, mira, boca, rubor, sudor):
    """Cabeza en (0, 0), radio ~46."""
    ctx.save()
    ctx.rotate(-0.08)
    for lado in (-1, 1):
        ovalo(ctx, lado * 45, 4, 8, 13, mix(PIEL, (0, 0, 0), 0.15))                       # orejas
    circle(ctx, 0, 0, 46, PIEL)
    if rubor > 0:
        for lado in (-1, 1):
            ovalo(ctx, lado * 26, 24, 15, 10, (0.95, 0.30, 0.25), 0.45 * rubor)
    ovalo(ctx, 0, -31, 49, 21, CABELLO)                                                    # pelo
    ovalo(ctx, -10, -38, 28, 12, CABELLO)
    for lado in (-1, 1):                                                                   # cejas
        ang = {"fiebre": 0.35, "apretados": 0.55, "abiertos": -0.12, "cerrados": 0.0}.get(ojos, 0.0)
        line(ctx, lado * 8, -4, lado * 30, -6 - lado * ang * 8, 4, CABELLO, 0.9)
    for lado in (-1, 1):
        ex, ey = lado * 18, 9
        if ojos == "cerrados":
            ctx.arc(ex, ey - 4, 9, 0.25, math.pi - 0.25)
            ctx.set_line_width(3.2)
            src(ctx, (0.1, 0.07, 0.07))
            ctx.stroke()
        elif ojos == "fiebre":
            ovalo(ctx, ex, ey + 1, 9, 5.5, (0.96, 0.96, 0.96))
            circle(ctx, ex + mira[0] * 2, ey + 1, 3.6, (0.12, 0.08, 0.06))
            ctx.rectangle(ex - 11, ey - 8, 22, 8)                                          # párpado pesado
            src(ctx, mix(PIEL, (0, 0, 0), 0.1))
            ctx.fill()
            line(ctx, ex - 10, ey - 1, ex + 10, ey - 1, 2.6, (0.12, 0.08, 0.07))
            ovalo(ctx, ex, ey + 12, 11, 3.5, (0.38, 0.25, 0.30), 0.55)                      # ojeras
        elif ojos == "apretados":
            line(ctx, ex - 9, ey - 5 * lado, ex + 9, ey + 3, 3.4, (0.1, 0.07, 0.07))
            line(ctx, ex - lado * 6, ey - 11, ex + lado * 14, ey - 3, 2.2, mix(PIEL, (0, 0, 0), 0.4), 0.8)
        else:                                                                              # abiertos, mirando
            ovalo(ctx, ex, ey, 10.5, 12, (0.97, 0.97, 0.97))
            circle(ctx, ex + mira[0] * 5, ey + mira[1] * 5, 5.2, (0.10, 0.06, 0.05))
            circle(ctx, ex + mira[0] * 5 - 1.5, ey + mira[1] * 5 - 2, 1.6, (1, 1, 1))
    # boca
    if boca == "abierta":
        ovalo(ctx, 0, 32, 10, 7, (0.25, 0.05, 0.06))
    elif boca == "sonrisa":
        ctx.arc(0, 22, 14, 0.5, math.pi - 0.5)
        ctx.set_line_width(3.2)
        src(ctx, (0.35, 0.12, 0.12))
        ctx.stroke()
    else:
        line(ctx, -9, 32, 9, 32, 3.4, (0.35, 0.12, 0.12))
    for i in range(int(6 * sudor)):                                                        # sudor que resbala
        f = (t * 0.45 + i * 0.37) % 1.0
        sx = (-30 + i * 11) % 60 - 30
        circle(ctx, sx, -8 + 50 * f, 3.0, (0.8, 0.95, 1.0), 0.8 * (1 - f * 0.5))
        circle(ctx, sx - 1, -9 + 50 * f, 1.1, (1, 1, 1), 0.9)
    if sudor > 0:
        ovalo(ctx, 0, -4, 34, 8, (0.85, 0.95, 1.0), 0.18 * sudor)
    ctx.restore()


def rafa_cama(ctx, x, y, s=1.0, t=0.0, ojos="fiebre", mira=(0.0, 0.0), boca="cerrada", rubor=0.6, sudor=1.0, respira=1.0,
              brazo_en_frente=0.0, vaso=False):
    """Rafa acostado, de cabeza en (x, y). Cuerpo tapado con la cobija hacia la derecha."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    rs = 1 + 0.012 * respira * math.sin(t * 2.2)
    fill_rrect(ctx, -135, 26, 270, 74, 32, SABANA)                                          # almohada
    fill_rrect(ctx, -135, 26, 270, 74, 32, (0, 0, 0), 0.0)
    ovalo(ctx, 70, 66, 100, 34, BATA)                                                       # hombros con bata
    ctx.save()
    ctx.translate(0, 6)
    ctx.scale(1, rs)
    # cobija
    ctx.move_to(70, 56)
    ctx.curve_to(150, 38, 230, 44, 300, 20)
    ctx.curve_to(340, 4, 380, 4, 420, 24)
    ctx.curve_to(470, 44, 520, 40, 560, 22)
    ctx.curve_to(600, 8, 630, 30, 640, 56)
    ctx.line_to(640, 150)
    ctx.line_to(70, 150)
    ctx.close_path()
    src(ctx, COBIJA)
    ctx.fill()
    ctx.move_to(70, 56)
    ctx.curve_to(150, 38, 230, 44, 300, 20)
    ctx.line_to(300, 52)
    ctx.curve_to(220, 70, 150, 70, 70, 84)
    ctx.close_path()
    src(ctx, SABANA)
    ctx.fill()
    for u in (330, 480, 600):
        line(ctx, u, 40, u + 8, 140, 3, (0.1, 0.2, 0.25), 0.35)
    ctx.restore()
    # brazo con el suero
    trazo_grueso(ctx, [(120, 72), (210, 66 - brazo_en_frente * 40), (290, 74 - brazo_en_frente * 70)], 36, BATA)
    circle(ctx, 305, 76 - brazo_en_frente * 72, 19, PIEL)
    line(ctx, 306, 62 - brazo_en_frente * 72, 316, 52 - brazo_en_frente * 72, 5, (0.9, 0.95, 0.95), 0.9)    # cinta del catéter
    _cara_rafa(ctx, t, ojos, mira, boca, rubor, sudor)
    ctx.restore()


def rafa_sentado(ctx, x, y, s=1.0, t=0.0, ojos="abiertos", boca="sonrisa"):
    """Rafa sentado en la cama, sano. (x, y) = punto de la cama donde se sienta."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    fill_rrect(ctx, -150, -270, 250, 90, 36, SABANA)                                        # almohada contra la cabecera
    trazo_grueso(ctx, [(60, -40), (140, -30)], 70, mix(COBIJA, (0, 0, 0), 0.2))
    fill_rrect(ctx, -70, -210, 140, 190, 40, BATA)                                          # torso
    for lado in (-1, 1):
        trazo_grueso(ctx, [(lado * 62, -180), (lado * 82, -110), (lado * 70, -60)], 34, BATA)
        circle(ctx, lado * 68, -52, 16, PIEL)
    ctx.save()
    ctx.translate(0, -262)
    ctx.rotate(0.03 * math.sin(t))
    ovalo(ctx, 0, 30, 15, 22, PIEL)
    _cara_rafa(ctx, t, ojos, (0.0, 0.0), boca, 0.0, 0.0)
    ctx.restore()
    ctx.move_to(-160, -40)                                                                  # cobija sobre las piernas
    ctx.curve_to(-60, -80, 80, -90, 230, -50)
    ctx.line_to(260, 80)
    ctx.line_to(-160, 80)
    ctx.close_path()
    src(ctx, COBIJA)
    ctx.fill()
    ctx.restore()


# =========================================================== Eulalia, la enfermera de blanco
def _manga(ctx, pts, w=36):
    trazo_grueso(ctx, pts, w, (0.90, 0.96, 0.98))
    trazo_grueso(ctx, pts, w * 0.45, UNIFORME_SOMBRA, 0.35)


def eulalia(ctx, x, y, s=1.0, t=0.0, pose="pie", cara=0.0, halo=1.0, alpha=1.0, inclina=0.0, espalda=False, sonrisa=0.0,
            pastilla=False, flota=1.0, k_brazo=1.0, espejo=False):
    """Eulalia. pose: 'pie' | 'ofrece' (extiende la mano con la pastilla hacia la izquierda) | 'frente' (mano sobre la frente de Rafa).
    cara: 0 en sombra (solo la barbilla/boca se ven) … 1 rostro visible. inclina: radianes, se inclina hacia la izquierda.
    k_brazo: 0 brazo en reposo … 1 brazo en la pose indicada. espejo: la dibuja mirando hacia la derecha."""
    if alpha <= 0:
        return
    ctx.save()
    ctx.translate(x, y + flota * 5 * math.sin(t * 1.2))
    ctx.scale(-s if espejo else s, s)
    if alpha < 1.0:
        ctx.push_group()
    if halo > 0:
        glow(ctx, 0, -330, 520, HALO, 0.34 * halo)
        glow(ctx, 0, -600, 220, HALO, 0.30 * halo)
    # falda almidonada
    ctx.move_to(-52, -332)
    onda = [4 * math.sin(i * 1.3 + t * 1.6) * flota for i in range(7)]
    ctx.curve_to(-62, -220, -110, -110, -128, -24 + onda[0])
    for i in range(1, 7):
        ctx.line_to(-128 + i * 256 / 6, -22 + onda[i] + (6 if i % 2 else 0))
    ctx.curve_to(110, -110, 62, -220, 52, -332)
    ctx.close_path()
    g = cairo.LinearGradient(-130, 0, 130, 0)
    g.add_color_stop_rgb(0, 0.72, 0.85, 0.90)
    g.add_color_stop_rgb(0.45, 0.99, 1.0, 1.0)
    g.add_color_stop_rgb(1, 0.66, 0.80, 0.87)
    ctx.set_source(g)
    ctx.fill()
    for i, px in enumerate((-70, -38, -8, 24, 56, 88)):                                       # pliegues planchados
        line(ctx, px * 0.45, -326, px * 1.35, -30, 3.2, (0.55, 0.74, 0.82), 0.55)
    line(ctx, -16, -326, -30, -34, 3, (1, 1, 1), 0.8)
    # torso, con la inclinación sobre la cintura
    ctx.save()
    ctx.translate(0, -332)
    ctx.rotate(-inclina)
    ctx.translate(0, 332)
    # capa por detrás
    if espalda:
        ctx.move_to(-76, -528)
        ctx.curve_to(-120, -400, -138, -220, -112, -150)
        ctx.line_to(112, -150)
        ctx.curve_to(138, -220, 120, -400, 76, -528)
        ctx.close_path()
        src(ctx, CAPA)
        ctx.fill()
        line(ctx, 0, -520, 0, -160, 3, (0.15, 0.22, 0.32), 0.7)
    # corpiño
    ctx.move_to(-70, -520)
    ctx.curve_to(-60, -470, -56, -400, -52, -332)
    ctx.line_to(52, -332)
    ctx.curve_to(56, -400, 60, -470, 70, -520)
    ctx.curve_to(40, -552, -40, -552, -70, -520)
    ctx.close_path()
    g2 = cairo.LinearGradient(-70, 0, 70, 0)
    g2.add_color_stop_rgb(0, 0.78, 0.89, 0.93)
    g2.add_color_stop_rgb(0.5, 1.0, 1.0, 1.0)
    g2.add_color_stop_rgb(1, 0.72, 0.85, 0.90)
    ctx.set_source(g2)
    ctx.fill()
    line(ctx, -50, -338, 50, -338, 7, (0.60, 0.74, 0.80), 0.8)                                 # cinturón
    if not espalda:
        for lado in (-1, 1):                                                                   # capa por delante: solo los lados
            ctx.move_to(lado * 62, -530)
            ctx.curve_to(lado * 112, -500, lado * 132, -380, lado * 118, -250)
            ctx.line_to(lado * 82, -276)
            ctx.curve_to(lado * 78, -380, lado * 66, -470, lado * 52, -520)
            ctx.close_path()
            src(ctx, CAPA)
            ctx.fill()
        line(ctx, -46, -540, 46, -540, 6, (0.12, 0.2, 0.3), 0.8)
    # brazos
    der_hombro = (54, -508)
    izq_hombro = (-54, -508)
    reposo = ((-96, -410), (-80, -298))
    if pose == "ofrece":
        meta = ((-140, -440), (-250 + 6 * math.sin(t * 1.5), -420))
    elif pose == "frente":
        meta = ((-158, -420), (-215, -332))
    else:
        meta = reposo
    codo = (lerp(reposo[0][0], meta[0][0], k_brazo), lerp(reposo[0][1], meta[0][1], k_brazo))
    mano = (lerp(reposo[1][0], meta[1][0], k_brazo), lerp(reposo[1][1], meta[1][1], k_brazo))
    _manga(ctx, [izq_hombro, codo, (mano[0] + 24 * k_brazo, mano[1] - 22 * (1 - k_brazo))], 30)
    _manga(ctx, [der_hombro, (96, -410), (82, -308)], 30)
    ovalo(ctx, 82, -290, 16, 20, PIEL_PALIDA)
    ovalo(ctx, mano[0], mano[1], 18, 15, PIEL_PALIDA, 1.0, 0.2)
    if pastilla:
        from historias.planchada.dibujo.objetos import pastilla as _pastilla
        _pastilla(ctx, mano[0] - 6, mano[1] - 16, 15, 1.4)
    # cabeza
    cy = -600
    fill_rrect(ctx, -14, -566, 28, 36, 8, mix(PIEL_PALIDA, (0, 0, 0), 0.1))
    ovalo(ctx, 0, cy + 4, 41, 53, CABELLO)
    if espalda:
        ovalo(ctx, 0, cy + 4, 41, 50, mix(CABELLO, (0.1, 0.12, 0.2), 0.3))
        ovalo(ctx, 0, cy - 6, 15, 10, CABELLO)
    else:
        ovalo(ctx, 0, cy + 5, 35, 46, PIEL_PALIDA)
        ovalo(ctx, 0, cy - 40, 36, 14, CABELLO)                                                # raya del pelo bajo la cofia
        if cara > 0:
            for lado in (-1, 1):
                line(ctx, lado * 10, cy - 11, lado * 27, cy - 6, 3, CABELLO, 0.9 * cara)           # cejas
                ovalo(ctx, lado * 18, cy + 3, 6, 4.2, (0.08, 0.06, 0.07), cara)                       # ojos cansados
                ovalo(ctx, lado * 18, cy + 12, 10, 2.6, (0.55, 0.50, 0.55), 0.28 * cara)           # ojeras
            line(ctx, 0, cy + 6, 3, cy + 22, 3, mix(PIEL_PALIDA, (0, 0, 0), 0.35), 0.7 * cara)
        sm = max(sonrisa, cara * 0.5)
        ctx.move_to(-10, cy + 32 - 3 * sm)
        ctx.curve_to(-4, cy + 32 + 6 * sm, 4, cy + 32 + 6 * sm, 10, cy + 32 - 3 * sm)
        ctx.set_line_width(3.2)
        src(ctx, (0.45, 0.20, 0.22))
        ctx.stroke()
        if cara < 1:                                                                           # sombra sobre el rostro
            g3 = cairo.LinearGradient(0, cy - 50, 0, cy + 22)
            g3.add_color_stop_rgba(0, 0.01, 0.03, 0.05, 0.96 * (1 - cara))
            g3.add_color_stop_rgba(0.50, 0.01, 0.03, 0.05, 0.90 * (1 - cara))
            g3.add_color_stop_rgba(0.82, 0.01, 0.03, 0.05, 0.35 * (1 - cara))
            g3.add_color_stop_rgba(1, 0.01, 0.03, 0.05, 0.0)
            ctx.save()
            ctx.arc(0, cy + 5, 36, 0, TAU)
            ctx.clip()
            ctx.rectangle(-50, cy - 60, 100, 100)
            ctx.set_source(g3)
            ctx.fill()
            ctx.restore()
    # cofia
    ctx.move_to(-48, cy - 22)
    ctx.curve_to(-52, cy - 62, -32, cy - 86, 0, cy - 88)
    ctx.curve_to(32, cy - 86, 52, cy - 62, 48, cy - 22)
    ctx.curve_to(26, cy - 36, -26, cy - 36, -48, cy - 22)
    ctx.close_path()
    src(ctx, BLANCO)
    ctx.fill()
    for lado in (-1, 1):
        fill_poly(ctx, [(lado * 44, cy - 30), (lado * 76, cy - 18), (lado * 62, cy + 8), (lado * 40, cy - 8)], (0.84, 0.93, 0.96))
    line(ctx, -44, cy - 28, 44, cy - 28, 5, (0.55, 0.72, 0.8), 0.7)
    ctx.restore()
    if alpha < 1.0:
        ctx.pop_group_to_source()
        ctx.paint_with_alpha(alpha)
    ctx.restore()


# =========================================================== enfermera de turno (uniforme moderno azul)
PELO_TURNO = (0.20, 0.11, 0.08)


def _silla_turno(ctx):
    for dx in (-60, 60):
        line(ctx, dx, -160, dx * 1.15, 0, 10, (0.06, 0.08, 0.09))
    fill_rrect(ctx, -86, -190, 172, 28, 10, (0.12, 0.17, 0.2))
    fill_rrect(ctx, -80, -420, 160, 22, 10, (0.12, 0.17, 0.2))
    line(ctx, -66, -400, -66, -180, 14, (0.10, 0.14, 0.17))
    line(ctx, 66, -400, 66, -180, 14, (0.10, 0.14, 0.17))


def turno_dormida(ctx, x, y, s=0.6, t=0.0, luz=1.0):
    """Enfermera de turno dormida en su silla del pasillo, con la cabeza caída."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    _silla_turno(ctx)
    resp = 1 + 0.015 * math.sin(t * 1.7)
    for lado in (-1, 1):                                                                    # piernas
        fill_rrect(ctx, lado * 36 - 24, -200, 48, 100, 18, SCRUB_OSC)
        fill_rrect(ctx, lado * 36 - 22, -110, 44, 108, 16, SCRUB_OSC)
        ovalo(ctx, lado * 36 + lado * 4, -4, 28, 11, (0.9, 0.9, 0.92))
    ctx.save()
    ctx.translate(0, -190)
    ctx.scale(1, resp)
    fill_rrect(ctx, -62, -230, 124, 240, 34, SCRUB)                                          # torso
    ctx.restore()
    trazo_grueso(ctx, [(-58, -370), (-60, -300), (36, -296)], 30, SCRUB)                     # brazos cruzados
    trazo_grueso(ctx, [(58, -370), (60, -306), (-30, -312)], 30, mix(SCRUB, (1, 1, 1), 0.08))
    ctx.save()
    ctx.translate(28, -415)
    ctx.rotate(0.38)                                                                         # cabeza caída hacia un lado
    ovalo(ctx, 0, 0, 40, 46, PIEL)
    ovalo(ctx, 0, -14, 44, 34, PELO_TURNO)
    ovalo(ctx, -6, -22, 38, 20, PELO_TURNO)
    line(ctx, -22, 4, -8, 6, 3, (0.1, 0.06, 0.06))                                           # ojos cerrados
    line(ctx, 8, 6, 22, 4, 3, (0.1, 0.06, 0.06))
    ctx.restore()
    ctx.restore()


def turno_de_pie(ctx, x, y, s=1.0, t=0.0, expediente=False, boca="seria", sorpresa=0.0):
    """Enfermera de turno de pie, en la puerta o junto a la cama."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    glow(ctx, 0, -330, 330, FLUO, 0.10)
    for lado in (-1, 1):
        fill_rrect(ctx, lado * 28 - 24, -300, 48, 292, 18, SCRUB_OSC)
        ovalo(ctx, lado * 30 + lado * 6, -6, 30, 12, (0.92, 0.92, 0.95))
    fill_rrect(ctx, -66, -560, 132, 280, 38, SCRUB)
    line(ctx, -22, -556, 0, -500, 4, mix(SCRUB, (1, 1, 1), 0.3), 0.8)
    line(ctx, 22, -556, 0, -500, 4, mix(SCRUB, (1, 1, 1), 0.3), 0.8)
    fill_rrect(ctx, 16, -480, 36, 46, 6, (0.9, 0.93, 0.95))                                  # gafete
    trazo_grueso(ctx, [(-60, -535), (-78, -440), (-68, -390)], 34, SCRUB)
    ovalo(ctx, -66, -378, 15, 18, PIEL)
    mano = (30, -430 + 3 * math.sin(t * 2))
    trazo_grueso(ctx, [(60, -535), (92, -460), mano], 34, SCRUB)
    if expediente:
        fill_rrect(ctx, 8, -520, 100, 130, 8, (0.86, 0.80, 0.55))
        fill_rrect(ctx, 14, -510, 88, 112, 5, (0.92, 0.93, 0.9))
        for k in range(5):
            line(ctx, 24, -490 + k * 20, 90 - (k % 2) * 20, -490 + k * 20, 3, (0.3, 0.4, 0.6), 0.6)
    ovalo(ctx, mano[0] + 4, mano[1] + 4, 15, 18, PIEL)
    fill_rrect(ctx, -14, -595, 28, 40, 8, mix(PIEL, (0, 0, 0), 0.1))
    ovalo(ctx, 0, -632, 43, 52, PELO_TURNO)
    ovalo(ctx, 0, -626, 38, 47, PIEL)
    ovalo(ctx, 0, -668, 45, 22, PELO_TURNO)
    for lado in (-1, 1):
        circle(ctx, lado * 15, -628, 4.5 + 1.2 * sorpresa, (0.1, 0.06, 0.06))
        line(ctx, lado * 8, -644 - 6 * sorpresa, lado * 24, -646 - 8 * sorpresa, 3, PELO_TURNO, 0.9)
    if boca == "habla":
        ovalo(ctx, 0, -600, 9, 6 + 3 * abs(math.sin(t * 9)), (0.3, 0.07, 0.08))
    elif boca == "asombro":
        ovalo(ctx, 0, -600, 8, 11, (0.3, 0.07, 0.08))
    else:
        line(ctx, -9, -600, 9, -600, 3.2, (0.4, 0.14, 0.14))
    ctx.restore()
