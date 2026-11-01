"""Banda sonora del episodio 1 (El apagón). producir.py llama a build()."""
import math
import numpy as np
from motor import config
from motor.config import SR
from motor.audio.synth import (
    Track, tt, noise, band, norm, env_exp, fade, sweep, tone, metal, thump, pad,
)
from motor.audio.master import master
from motor.audio.mixing import scene_offsets, new_track


def build():
    sc, total = scene_offsets("ep1")
    tr, total_out, voices = new_track("ep1")
    T1, _ = sc["s1_titulo"]
    T2, s2 = sc["s2_ciudad"]
    T3, s3 = sc["s3_sotano"]
    T4, s4 = sc["s4_tito"]
    T5, s5 = sc["s5_pasillo"]
    T6, s6 = sc["s6_eleccion"]

    # ---------- música de fondo ----------
    tr.add(pad([73.4, 146.8, 174.6, 220.0], T3 + 1.0, attack=2.5, release=2.5, bright=700), 0.0, 0.24)
    tension = pad([73.4, 146.8, 155.6, 220.0, 207.7], T6 - (T3 + s3.EMERGENCY), attack=2.0, release=1.5, bright=900, seed=3)
    tr.add(tension, T3 + s3.EMERGENCY, 0.2)
    tr.add(pad([36.7, 73.4, 110.0], total - T6 + 0.3, attack=0.8, release=0.6, bright=500, seed=4), T6 - 0.3, 0.2)

    # ---------- título ----------
    boom = thump(48, 3.0, 1.1) + 0.3 * band(noise(3.0, 1), None, 180) * env_exp(int(3.0 * SR), 0.4)
    tr.add(boom, T1 + 0.5, 0.9)
    r = np.random.default_rng(3)
    for i in range(14):
        at = T1 + 0.5 + r.uniform(0, 1.2) * (i / 14)
        d = r.uniform(0.02, 0.07)
        blip = band(noise(d, i), 1500, 9000) if i % 2 else np.sign(np.sin(2 * np.pi * r.uniform(300, 1600) * tt(d)))
        tr.add(fade(blip, 0.002, 0.01), at, 0.12 * (1 - i / 16), r.uniform(-0.6, 0.6))
    tr.add(fade(sweep(900, 1800, 0.9) * env_exp(int(0.9 * SR), 0.3), 0.005, 0.3), T1 + 2.15, 0.06)

    # ---------- ciudad ----------
    wind = band(noise(s2.DURATION + 1, 5), 180, 900)
    wind *= 0.6 + 0.4 * np.sin(2 * np.pi * 0.25 * tt(len(wind) / SR))
    tr.add(fade(norm(wind), 0.8, 1.2), T2 - 0.3, 0.26)
    hum = band(noise(s2.DURATION, 6), 40, 220)
    tr.add(fade(norm(hum), 1.0, 1.0), T2, 0.22)
    n_chars = len(s2.LINE1) + 4 + len(s2.LINE2)
    for i in range(n_chars):
        at = T2 + s2.TYPE_START + i / s2.CPS
        if i < len(s2.LINE1) and s2.LINE1[i] == " ":
            continue
        if len(s2.LINE1) <= i < len(s2.LINE1) + 4:
            continue
        click = band(noise(0.02, 100 + i), 2000, 7000) * env_exp(int(0.02 * SR), 0.004)
        tr.add(click, at, 0.32, -0.5)
    whoosh = band(noise(2.2, 9), 300, 2500) * np.hanning(int(2.2 * SR))
    tr.add(norm(whoosh), T2 + 1.0, 0.07, -0.6)

    # ---------- sótano ----------
    dur_lit = s3.BLACKOUT
    t = tt(dur_lit)
    buzz = sum(np.sin(2 * np.pi * f * t) * a for f, a in ((120, 1.0), (240, 0.5), (360, 0.25), (480, 0.12)))
    buzz += 0.2 * band(noise(dur_lit, 11), 2000, 6000)
    lights = np.array([s3.lights_at(x) for x in t[:: SR // 100]])
    gate = np.repeat(lights, SR // 100)[: len(t)]
    gate = np.convolve(gate, np.ones(200) / 200, mode="same")
    tr.add(fade(norm(buzz) * gate, 0.6, 0.02), T3, 0.1, -0.2)

    # Tito tararea (desafinado a propósito)
    melody = [(659, .35), (784, .35), (880, .5), (784, .35), (659, .5), (587, .35), (523, .7), (0, .3),
              (523, .35), (587, .35), (659, .5), (523, .35), (440, .7), (0, .3),
              (659, .35), (784, .35), (880, .5), (988, .35), (880, .35), (784, .7), (0, .25),
              (659, .35), (587, .35), (523, .9)]
    at = T3 + 0.8
    r = np.random.default_rng(8)
    for f, d in melody:
        if at > T3 + 9.9:
            break
        if f:
            cents = r.uniform(-45, 45)
            note = tone(f * 2 ** (cents / 1200) / 2, d, (1.0, 0.25, 0.12, 0.06), vibrato=0.012)
            tr.add(fade(note, 0.04, 0.08), at, 0.2, 0.4)
        at += d

    # trapeador
    k = 0
    while True:
        at_l = 0.2 + k * s3.MOP_PERIOD / 2
        if at_l > 10.0:
            break
        sw = band(noise(0.45, 200 + k), 900, 4500) * np.hanning(int(0.45 * SR))
        tr.add(sw, T3 + at_l, 0.11, 0.45)
        k += 1
    # chispas del tablero
    for a, b in s3.SPARKS:
        d = b - a
        cr = np.zeros(int(d * SR))
        rr = np.random.default_rng(int(a * 10))
        for _ in range(40):
            i = rr.integers(0, len(cr) - 200)
            cr[i:i + 200] += band(noise(200 / SR, int(i)), 2500, 9000) * np.exp(-np.arange(200) / 30)
        tr.add(cr, T3 + a, 0.25, -0.4)
    # parpadeo: chasquidos eléctricos
    for when, v in s3.FLICKER:
        tr.add(band(noise(0.04, int(when * 100)), 600, 5000) * env_exp(int(0.04 * SR), 0.008), T3 + when, 0.22)
    # apagón
    pdown = sweep(260, 30, 1.4) * env_exp(int(1.4 * SR), 0.6)
    tr.add(fade(pdown, 0.005, 0.2) + 0.6 * thump(55, 1.4, 0.4), T3 + s3.BLACKOUT, 0.55)
    # alarma de emergencia
    alarm_start = T3 + s3.EMERGENCY + 0.1
    alarm_end = T6 - 0.2
    t_al = tt(alarm_end - alarm_start)
    which = (t_al % 1.2) < 0.6
    f = np.where(which, 587.0, 440.0)
    sq = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR))
    al = band(sq, 300, 1800) * (0.55 + 0.45 * np.sin(2 * np.pi * t_al / 1.2 * 2) ** 2)
    tr.add(fade(norm(al), 0.3, 0.4), alarm_start, 0.08, 0.1)
    # servo: Tito gira la cabeza
    servo = band(sweep(160, 300, 2.2, "saw") * (1 + 0.15 * np.sin(2 * np.pi * 31 * tt(2.2))), 250, 3500)
    tr.add(fade(norm(servo), 0.1, 0.3), T3 + 13.4, 0.07, 0.4)

    # ---------- primer plano de Tito ----------
    tr.add(fade(norm(servo), 0.1, 0.3), T4, 0.09)
    rr = np.random.default_rng(12)
    for i, (when, s) in enumerate(s4.FLICK):
        bl = np.sign(np.sin(2 * np.pi * rr.uniform(900, 2200) * tt(0.05)))
        tr.add(fade(bl, 0.002, 0.01), T4 + when, 0.07)
    pup = sweep(220, 1100, 0.6) + 0.4 * sweep(330, 1650, 0.6)
    tr.add(fade(pup, 0.01, 0.15), T4 + 4.0, 0.12)
    for k in range(4):
        ping = (np.sin(2 * np.pi * 1760 * tt(0.6)) + 0.5 * np.sin(2 * np.pi * 2640 * tt(0.6))) * env_exp(int(0.6 * SR), 0.15)
        tr.add(ping, T4 + 4.2 + k * 0.8, 0.06)
    # las voces de Tito se agregan en audio/master.py junto con la narración

    # ---------- pasillo ----------
    # bajo pulsante
    beat = 60 / 140 / 2
    n = int(s5.DURATION / beat)
    for i in range(n):
        d = beat * 0.9
        b = band(sweep(73.4, 73.4, d, "saw"), None, 400) * env_exp(int(d * SR), 0.12)
        tr.add(b, T5 + i * beat, 0.12 + 0.1 * i / n)
    # pasos metálicos de los tres Centinelas
    for idx, (X, dz, ph) in enumerate(s5.SENTINELS):
        k = 0
        while True:
            at_l = (k * math.pi - ph) / (2 * math.pi / s5.STEP_PERIOD)
            k += 1
            if at_l < 0.1:
                continue
            if at_l > s5.DURATION:
                break
            z = s5.sentinel_z(at_l, dz)
            g = min(1.0, 4.5 / z)
            step = metal([170 + idx * 13, 395, 710, 1120], 0.5, 0.12, seed=k + idx * 50) + 1.4 * thump(62, 0.5, 0.09)
            tr.add(step, T5 + at_l, 0.22 * g * min(1, at_l / 1.2), X * 0.4)
    # puertas
    for i, (side, z, t0) in enumerate(s5.DOORS):
        sl = band(noise(s5.CLOSE_TIME, 300 + i), 400, 3000) * np.linspace(0.2, 1, int(s5.CLOSE_TIME * SR))
        tr.add(sl, T5 + t0, 0.12, side * 0.6)
        clang = metal([92, 151, 233, 368, 522, 761], 1.6, 0.45, seed=500 + i) + 1.6 * thump(48, 1.6, 0.3)
        tr.add(clang, T5 + t0 + s5.CLOSE_TIME, 0.3 * (0.75 + 0.25 * (3.5 / z)), side * 0.5)
    # subida hacia la pantalla de elección
    riser = band(noise(1.4, 77), 400, 5000) * np.linspace(0, 1, int(1.4 * SR)) ** 2
    tr.add(riser + 0.3 * sweep(100, 600, 1.4) * np.linspace(0, 1, int(1.4 * SR)), T6 - 1.4, 0.18)

    # ---------- elección ----------
    tr.add(thump(45, 2.0, 0.8) + 0.4 * metal([60, 97, 140], 2.0, 0.6, 9), T6, 0.6)
    for (_, _, _, at) in s6.OPTIONS:
        tick = np.sin(2 * np.pi * 1320 * tt(0.12)) * env_exp(int(0.12 * SR), 0.03)
        tr.add(tick, T6 + at, 0.18)
    beat_t = s6.TIMER_START
    while beat_t < s6.DURATION - 0.2:
        g = 0.35 + 0.35 * (beat_t / s6.DURATION)
        tr.add(thump(52, 0.3, 0.09), T6 + beat_t, g)
        tr.add(thump(46, 0.3, 0.09), T6 + beat_t + 0.24, g * 0.7)
        beat_t += 0.85
    k = 0
    while s6.TIMER_START + k * 0.5 < s6.DURATION:
        tk = band(noise(0.015, 900 + k), 3000, 9000) * env_exp(int(0.015 * SR), 0.003)
        tr.add(tk, T6 + s6.TIMER_START + k * 0.5, 0.12)
        k += 1

    # ---------- master ----------
    return master(tr.buf, total_out, voices, 0.5), total_out
