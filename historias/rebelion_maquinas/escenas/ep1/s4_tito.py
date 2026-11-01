"""Escena 4 — Primer plano de Tito: sus ojos pasan de azul a blanco."""
import math
import random
import cairo
from motor.config import W, H, TITO_BLUE, WHITE
from motor.primitives import seg, smooth, lerp, glow, tint, vignette, fill_screen, circle, src, TAU
from historias.rebelion_maquinas.dibujo.characters import tito, tito_glow

DURATION = 9.0
# Los tiempos de los diálogos se ajustan a la duración real de la voz (ver audio/voice.py)
LINE1_AT, LINE2_AT = 4.3, 6.9
SUBS = [
    (LINE1_AT, 6.85, "Instrucción recibida de Ágora.", "TITO"),
    (LINE2_AT, 8.9, "Lo siento, Dani.", "TITO"),
]

_r = random.Random(5)
BOKEH = [(_r.uniform(0, W), _r.uniform(0, H), _r.uniform(40, 140), _r.uniform(0.05, 0.18)) for _ in range(18)]
# patrón de parpadeo azul/blanco entre 3.0 y 4.0 s
FLICK = [(3.0, 1), (3.12, 0), (3.2, 1), (3.38, 0), (3.5, 1), (3.56, 0), (3.7, 1), (3.78, 0), (3.86, 1), (4.0, 1)]


def eye_state(t):
    """0 = azul, 1 = blanco."""
    if t < 3.0:
        return 0
    v = 0
    for when, s in FLICK:
        if t >= when:
            v = s
    return v


def draw(ctx, t):
    # fondo: sótano desenfocado en rojo
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.10, 0.02, 0.02)
    g.add_color_stop_rgb(1, 0.03, 0.005, 0.005)
    ctx.set_source(g)
    ctx.paint()
    for x, y, r, a in BOKEH:
        glow(ctx, x, y, r, (1.0, 0.25, 0.15), a, cairo.OPERATOR_SCREEN)

    s = lerp(5.4, 6.0, smooth(t / DURATION))
    look = lerp(0.75, 0.0, smooth(seg(t, 0.0, 2.6)))
    white = eye_state(t)
    eye_rgb = WHITE if white else TITO_BLUE
    ant = smooth(seg(t, 4.0, 4.4))
    dilate = 1.0 + 0.15 * smooth(seg(t, 4.0, 4.5))

    head = tito(ctx, 960, 520 + 245 * s, s, look=look, eye_rgb=eye_rgb, show_mop=False,
                antenna_rgb=(0.2, 0.25, 0.3))

    # luz roja de emergencia + luz giratoria barriendo la cara
    tint(ctx, (1.0, 0.32, 0.26), 0.88)
    sweep = 0.5 + 0.5 * math.sin(t * 3.2)
    glow(ctx, lerp(200, 1720, sweep), 300, 900, (1.0, 0.2, 0.12), 0.35, cairo.OPERATOR_SCREEN)

    tito_glow(ctx, head, look, 0.0, eye_rgb, eye_glow=0.9 if white else 0.6,
              antenna_rgb=mix_ant(ant), antenna_glow=ant, dilate=dilate)

    # ondas de señal saliendo de la antena (Ágora le habla)
    if ant > 0:
        ctx.save()
        ctx.set_matrix(head)
        for k in range(4):
            age = (t - 4.2 - k * 0.8)
            if 0 <= age <= 1.6:
                r = 8 + age * 26
                ctx.set_line_width(1.6)
                src(ctx, WHITE, 0.6 * (1 - age / 1.6) * ant)
                ctx.arc(26, -303, r, 0, TAU)
                ctx.stroke()
        ctx.restore()

    vignette(ctx, 0.75)


def mix_ant(k):
    return tuple(lerp(a, b, k) for a, b in zip((0.2, 0.25, 0.3), WHITE))
