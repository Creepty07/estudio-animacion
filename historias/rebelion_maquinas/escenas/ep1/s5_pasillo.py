"""Escena 5 — Pasillo: los Centinelas avanzan y las puertas se cierran."""
import math
import random
from motor.config import TITO_BLUE
from motor.primitives import seg, smooth, ease_in, lerp, clamp, camera, mix, vignette, darken, TAU
from historias.rebelion_maquinas.dibujo.environments import draw_corridor, proj, FLOOR_Yw, F
from historias.rebelion_maquinas.dibujo.characters import sentinel

DURATION = 8.0
SUBS = [
    (0.4, 3.6, "Por el pasillo suenan pasos metálicos: los Centinelas vienen por ti.", None),
    (3.9, 7.6, "Las puertas del sótano se cierran, una por una.", None),
]

# (lado, profundidad z, momento en que empieza a cerrarse)
DOORS = [(-1, 10.0, 2.0), (1, 10.0, 2.8), (-1, 6.6, 3.6), (1, 6.6, 4.3), (-1, 3.2, 5.0), (1, 3.2, 5.6)]
CLOSE_TIME = 0.28
SLAMS = [t0 + CLOSE_TIME for _, _, t0 in DOORS]
STEP_PERIOD = 1.1  # un ciclo = dos pasos
SENTINELS = [(-0.95, 0.0, 0.0), (0.95, 0.5, 1.3), (0.0, 1.7, 2.4)]  # X, z extra, fase


def sentinel_z(t, dz):
    return lerp(13.6, 5.4, t / DURATION) + dz


def shake(t):
    amp = 0.0
    for s in SLAMS:
        if t >= s:
            amp += 16 * math.exp(-(t - s) * 10)
    r = random.Random(int(t * 30))
    return r.uniform(-amp, amp), r.uniform(-amp, amp)


def draw(ctx, t):
    doors = [(side, z, ease_in(seg(t, t0, t0 + CLOSE_TIME))) for side, z, t0 in DOORS]
    dx, dy = shake(t)
    ctx.save()
    camera(ctx, lerp(1.0, 1.08, t / DURATION), 960, 520, dx, dy)
    draw_corridor(ctx, t, doors)

    appear = smooth(seg(t, 0.0, 1.4))
    for X, dz, ph in sorted(SENTINELS, key=lambda s: -sentinel_z(t, s[1])):
        z = sentinel_z(t, dz)
        x, y = proj(X, FLOOR_Yw, z)
        fog = clamp((z - 5) / 9)
        body = mix((0.035, 0.03, 0.04), (0.6, 0.12, 0.09), 0.85 * fog + 0.15 * (1 - appear))
        sentinel(ctx, x, y, (F / z) / 195, phase=t * TAU / STEP_PERIOD + ph,
                 body=body, rim_a=0.45 * appear, eye_a=appear)
    ctx.restore()

    vignette(ctx, 0.75)
    darken(ctx, smooth(seg(t, 7.5, 8.0)))
