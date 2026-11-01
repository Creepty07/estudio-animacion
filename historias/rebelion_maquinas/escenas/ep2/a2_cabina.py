"""Final malo 2/2 — La cabina se detiene entre pisos, habla Ágora y los cables ceden."""
import math
import random
from motor.config import W, H
from motor.primitives import seg, smooth, ease_out, lerp, darken, vignette, fill_screen, glow, line, TAU
from historias.rebelion_maquinas.dibujo.env_elevador import shaft, cabin, CAB_Y1
from historias.rebelion_maquinas.dibujo.dani_poses import dani_pose

DURATION = 10.6
AGORA_AT = 4.1
AGORA_LEN = 3.7   # duración real de la voz (ver audio/voice.py)
SNAP_AT = 8.2
FALL_AT = 8.6
CRASH_AT = 9.75
STOP_AT = 2.6
LIGHT_OFF = 3.0
SUBS = [
    (0.3, 2.8, "La cabina sube… y se detiene entre dos pisos.", None),
    (3.0, 3.95, "La luz se apaga.", None),
    (AGORA_AT, AGORA_AT + AGORA_LEN + 0.1, "No tienes por qué tener miedo, Dani.", "ÁGORA"),
    (SNAP_AT, CRASH_AT, "Se oye un chasquido. Los cables ceden.", None),
]


def travel(t):
    return 1050 * (1 - (1 - seg(t, 0.0, STOP_AT)) ** 2)


def floor_text(t):
    if t < 0.9:
        return "-3"
    if t < 1.8:
        return "-2"
    if t < STOP_AT:
        return "-1"
    return "--" if (t * 2) % 1 < 0.5 else "-1"


def light_at(t):
    if t < LIGHT_OFF:
        return 1.0
    if t < LIGHT_OFF + 0.35:
        return 1.0 if int(t * 22) % 2 else 0.2
    return 0.0


def shake(t):
    amp = 0.0
    for at, a, d in ((STOP_AT, 18, 8), (SNAP_AT, 26, 6)):
        if t >= at:
            amp += a * math.exp(-(t - at) * d)
    if FALL_AT < t < CRASH_AT:
        amp += 6
    r = random.Random(int(t * 30))
    return r.uniform(-amp, amp), r.uniform(-amp, amp)


def draw(ctx, t):
    off = travel(t)
    dx, dy = shake(t)
    fall = 0.5 * 2600 * max(0.0, t - FALL_AT) ** 2
    drop = 22 * smooth(seg(t, SNAP_AT, SNAP_AT + 0.15))
    ctx.save()
    ctx.translate(dx, dy)
    shaft(ctx, off - fall * 0.35)
    light = light_at(t)
    speaker = 0.0
    if AGORA_AT <= t <= AGORA_AT + AGORA_LEN:
        speaker = 0.55 + 0.45 * abs(math.sin((t - AGORA_AT) * 9))
    broken = smooth(seg(t, SNAP_AT, SNAP_AT + 0.4))

    def person(c):
        dani_pose(c, 1010, CAB_Y1 + 2, 1.15, "stand", facing=-1, backpack=True,
                  look_up=0.8 if t < 4.0 or t > SNAP_AT else 1.0)
        if light < 1:
            # sombra sobre la cabina cuando se apaga la luz
            c.save()
            c.rectangle(600, 250, 720, 610)
            c.clip()
            c.set_source_rgba(0.0, 0.0, 0.02, 0.82 * (1 - light))
            c.paint()
            c.restore()

    cabin(ctx, 0, drop + fall, light, speaker, floor_text(t) if t < FALL_AT else "??", broken, t, person)
    if SNAP_AT <= t < SNAP_AT + 0.35:
        r = random.Random(int(t * 30))
        for _ in range(12):
            a = r.uniform(0, TAU)
            ln = r.uniform(20, 90)
            line(ctx, 960, 120 + drop, 960 + math.cos(a) * ln, 120 + drop + math.sin(a) * ln, 3, (1, 0.9, 0.5))
        glow(ctx, 960, 120 + drop, 180, (1, 0.8, 0.4), 0.9)
    ctx.restore()

    # líneas de velocidad durante la caída
    if FALL_AT < t < CRASH_AT:
        k = seg(t, FALL_AT, CRASH_AT)
        r = random.Random(int(t * 30))
        for _ in range(int(10 + 30 * k)):
            x = r.uniform(0, W)
            y = r.uniform(0, H)
            line(ctx, x, y, x, y - 120 - 300 * k, 2, (1, 1, 1), 0.12 + 0.2 * k)

    vignette(ctx, 0.75)
    darken(ctx, 0.25 * (1 - light))
    if t >= CRASH_AT:
        flash = 1 - seg(t, CRASH_AT, CRASH_AT + 0.12)
        fill_screen(ctx, (0, 0, 0))
        fill_screen(ctx, (1, 0.85, 0.8), 0.9 * flash)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.25)))
