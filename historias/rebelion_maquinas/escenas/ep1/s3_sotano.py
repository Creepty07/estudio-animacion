"""Escena 3 — Sótano: turno de noche, apagón y luces de emergencia."""
import math
from motor.config import TITO_BLUE
from motor.primitives import (
    seg, smooth, lerp, camera, darken, tint, vignette, font, text_at, src, window, TAU,
)
from historias.rebelion_maquinas.dibujo.environments import draw_basement, beacon
from historias.rebelion_maquinas.dibujo.characters import tito, tito_glow, dani

DURATION = 16.0
SUBS = [
    (1.0, 5.0, "Son las 11:47 de la noche. Estás solo en el sótano, revisando un tablero que lleva semanas fallando.", None),
    (5.2, 9.8, "A tu lado, Tito pasa el trapeador y tararea una canción desafinada, como todas las noches.", None),
    (10.2, 12.3, "De pronto, las luces se apagan.", None),
    (12.6, 15.8, "Se encienden las luces de emergencia. Tito se detiene… y gira la cabeza hacia ti, muy despacio.", None),
]

BLACKOUT, EMERGENCY = 11.2, 12.2
FLICKER = [(10.0, 0.0), (10.07, 1.0), (10.22, 0.0), (10.3, 0.8), (10.5, 0.0), (10.58, 1.0),
           (10.78, 0.0), (10.84, 0.4), (10.95, 0.0)]
SPARKS = [(3.2, 3.5), (7.6, 7.9)]
TITO_X, TITO_Y, TITO_S = 1330, 898, 1.15
MOP_PERIOD = 1.6


def lights_at(t):
    if t < FLICKER[0][0]:
        return 1.0
    val = 0.0
    for when, v in FLICKER:
        if t >= when:
            val = v
    return val


def emergency_at(t):
    e = smooth(seg(t, EMERGENCY, EMERGENCY + 0.8))
    if EMERGENCY + 0.15 < t < EMERGENCY + 0.3:
        e *= 0.3
    return e


def mop_swing(t):
    amp = 1 - smooth(seg(t, 10.0, 10.6))
    return 42 * math.sin(TAU * t / MOP_PERIOD) * amp


def tito_look(t):
    turn = smooth(seg(t, 13.4, 15.6))
    return lerp(0.35, -0.9, turn), lerp(5.0, 0.0, smooth(seg(t, 10.2, 11.0)))


def draw_notes(ctx, t):
    font(ctx, 46, "DejaVu Sans")
    head_x, head_y = TITO_X, TITO_Y - 300 * TITO_S
    k = 0
    while True:
        born = 0.8 + k * 0.7
        if born > 9.6:
            break
        age = t - born
        if 0 <= age <= 1.9:
            a = math.sin(math.pi * age / 1.9)
            x = head_x + 30 + math.sin(age * 4 + k) * 22 + (k % 3) * 14
            y = head_y - 20 - age * 75
            src(ctx, (0.75, 0.9, 1.0), 0.85 * a)
            text_at(ctx, "♪" if k % 2 else "♫", x, y)
        k += 1


def draw(ctx, t):
    lights = lights_at(t) if t < BLACKOUT else 0.0
    e = emergency_at(t)
    leds = t < BLACKOUT and lights > 0.5
    spark = max((math.sin(math.pi * seg(t, a, b)) for a, b in SPARKS), default=0.0)
    look, look_y = tito_look(t)

    ctx.save()
    z = lerp(1.0, 1.05, t / DURATION) + 0.12 * smooth(seg(t, 13.2, 16.0))
    fx = lerp(960, 1250, smooth(seg(t, 13.2, 16.0)))
    camera(ctx, z, fx, 640)
    draw_basement(ctx, t, lights=lights, leds=leds, spark=spark if t < BLACKOUT else 0.0)
    working = t < 10.3
    dani(ctx, 770, 895, 1.32, arm=math.sin(t * 3.1) if working else 0.6, breathe=math.sin(t * 1.6))
    head = tito(ctx, TITO_X, TITO_Y, TITO_S, look=look, look_y=look_y, mop_swing=mop_swing(t))
    if t < 10.0:
        draw_notes(ctx, t)
    ctx.restore()

    # iluminación
    if t < BLACKOUT:
        darken(ctx, 0.92 * (1 - lights))
    else:
        darken(ctx, 0.95 - 0.5 * e)
        tint(ctx, (1.0, 0.22, 0.17), e)
        if e > 0:
            ctx.save()
            camera(ctx, z, fx, 640)
            beacon(ctx, t, strength=e)
            ctx.restore()

    # los ojos de Tito siempre brillan (lo único visible en el apagón)
    ctx.save()
    ctx.identity_matrix()
    tito_glow(ctx, head, look, look_y, TITO_BLUE, eye_glow=0.35 if t < BLACKOUT else 0.7)
    ctx.restore()

    vignette(ctx, 0.7)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.8)))
