"""Banda sonora del episodio 2 (los tres finales). producir.py llama a build()."""
import math
import numpy as np
from motor import config
from motor.config import SR
from motor.audio.synth import Track, tt, noise, band, norm, pad, fade, sweep
from motor.audio import sfx
from motor.audio.master import master
from motor.audio.mixing import scene_offsets, new_track


def alarm(dur):
    t = tt(dur)
    f = np.where((t % 1.2) < 0.6, 587.0, 440.0)
    sq = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR))
    return fade(norm(band(sq, 300, 1800)), 0.3, 0.4)


def run_steps(tr, start, end, rate, gain, pan=0.0, seed=0, metal=False):
    k = 0
    at = start
    while at < end:
        s = sfx.step_metal(seed + k) if metal else sfx.step_concrete(seed + k)
        tr.add(s, at, gain, pan)
        k += 1
        at = start + k / rate


def build():
    sc, total = scene_offsets("ep2")
    tr, total_out, voices = new_track("ep2")
    T = {k: v[0] for k, v in sc.items()}
    M = {k: v[1] for k, v in sc.items()}

    def blips(at, gain, seed):
        for d, s, g, p in sfx.glitch_blips(seed):
            tr.add(s, at + d, gain * g, p)

    # ---------- apertura ----------
    tr.add(pad([73.4, 146.8, 174.6, 220.0], M["intro"].DURATION + 0.5, 1.0, 1.0, 700), T["intro"], 0.14)
    tr.add(sfx.boom(), T["intro"] + 0.35, 0.5)
    blips(T["intro"] + 0.35, 0.12, 3)
    for i in range(3):
        tr.add(sfx.tick(), T["intro"] + 1.6 + i * 0.25, 0.16)

    # ---------- tarjetas de opción ----------
    for key in ("a0_opcion", "b0_opcion", "c0_opcion"):
        tr.add(sfx.whoosh(0.5), T[key], 0.16)
        tr.add(sfx.boom(1.5), T[key] + 0.2, 0.25)
        tr.add(sfx.tick(990), T[key] + 0.45, 0.2)

    # ---------- FINAL MALO: elevador ----------
    a1, a2 = M["a1_elevador"], M["a2_cabina"]
    A1, A2 = T["a1_elevador"], T["a2_cabina"]
    tr.add(alarm(a1.DURATION + 3.1), A1, 0.07, 0.1)
    tr.add(pad([73.4, 146.8, 155.6, 220.0], a1.DURATION + a2.DURATION, 1.0, 1.5, 900, 3), A1, 0.2)
    run_steps(tr, A1 + a1.RUN[0] + 0.1, A1 + a1.RUN[1], 4.0, 0.3, -0.2, 10)
    tr.add(sfx.tick(1500, 0.08), A1 + 0.9, 0.15)          # botón de llamada
    tr.add(sfx.ding(), A1 + a1.DING_AT, 0.35)
    tr.add(sfx.door_slide(a1.OPEN[1] - a1.OPEN[0]), A1 + a1.OPEN[0], 0.3)
    tr.add(sfx.door_slide(a1.CLOSE[1] - a1.CLOSE[0], 22), A1 + a1.CLOSE[0], 0.3)
    tr.add(sfx.jolt(32), A1 + a1.CLOSE[1], 0.25)
    tr.add(sfx.motor_hum(a1.DURATION - a1.CLOSE[1] + a2.STOP_AT), A1 + a1.CLOSE[1] + 0.2, 0.3)
    tr.add(sfx.tick(880, 0.15), A1 + a1.FLOOR_CHANGE, 0.12)
    # cabina
    for at in (0.9, 1.8):
        tr.add(sfx.tick(880, 0.15), A2 + at, 0.12)
    tr.add(sfx.jolt(), A2 + a2.STOP_AT, 0.6)
    for k in range(8):
        tr.add(band(noise(0.03, 900 + k), 600, 5000) * np.hanning(int(0.03 * SR)), A2 + a2.LIGHT_OFF + k * 0.045, 0.2)
    tr.add(sweep(220, 40, 0.8) * np.linspace(1, 0, int(0.8 * SR)), A2 + a2.LIGHT_OFF + 0.35, 0.3)
    tr.add(sfx.static(0.3), A2 + a2.AGORA_AT - 0.25, 0.05)
    tr.add(sfx.cable_snap(), A2 + a2.SNAP_AT, 0.75)
    tr.add(sfx.jolt(33), A2 + a2.SNAP_AT + 0.05, 0.5)
    tr.add(sfx.falling(a2.CRASH_AT - a2.FALL_AT), A2 + a2.FALL_AT, 0.5)
    tr.add(sfx.crash(), A2 + a2.CRASH_AT, 0.95)
    tr.add(np.sin(2 * np.pi * 3900 * tt(1.6)) * np.linspace(1, 0, int(1.6 * SR)), A2 + a2.CRASH_AT + 0.3, 0.02)
    tr.add(sfx.sting("malo"), T["a3_fin"] + 0.35, 0.5)
    blips(T["a3_fin"] + 0.35, 0.12, 5)

    # ---------- FINAL REGULAR: escalera ----------
    b1, b2 = M["b1_escalera"], M["b2_calle"]
    B1, B2 = T["b1_escalera"], T["b2_calle"]
    tr.add(alarm(b1.DURATION), B1, 0.07, -0.1)
    tr.add(pad([73.4, 110.0, 146.8, 155.6], b1.DURATION, 0.6, 0.6, 900, 5), B1, 0.18)
    run_steps(tr, B1 + 0.05, B1 + b1.GRAB_AT, 4.6, 0.32, 0.0, 40)
    run_steps(tr, B1 + 3.4, B1 + b1.GRAB_AT, 2.2, 0.32, -0.4, 60, metal=True)
    tr.add(sfx.cloth_rip(0.3, 42), B1 + b1.GRAB_AT, 0.5)
    tr.add(sfx.step_metal(70), B1 + b1.GRAB_AT, 0.25, -0.3)
    tr.add(sfx.cloth_rip(0.45, 43), B1 + b1.RELEASE_AT - 0.1, 0.55)
    run_steps(tr, B1 + b1.RELEASE_AT + 0.1, B1 + b1.DOOR_AT, 4.6, 0.32, 0.1, 80)
    tr.add(sfx.jolt(44), B1 + b1.DOOR_AT, 0.35)
    tr.add(sfx.whoosh(0.9, 400, 6000, 45), B1 + b1.DURATION - 0.6, 0.35)
    # calle
    wind = band(noise(b2.DURATION + 0.5, 5), 180, 900)
    wind *= 0.6 + 0.4 * np.sin(2 * np.pi * 0.25 * tt(len(wind) / SR))
    tr.add(fade(norm(wind), 0.3, 1.0), B2, 0.22)
    tr.add(fade(norm(band(noise(b2.DURATION, 6), 40, 220)), 0.5, 1.0), B2, 0.18)
    run_steps(tr, B2 + 0.15, B2 + b2.STOP_AT, 4.4, 0.3, 0.0, 90)
    at, k = B2 + b2.STOP_AT, 0
    while at < B2 + b2.DURATION - 0.3:
        tr.add(sfx.breath(0.32, True, 100 + k), at, 0.14)
        tr.add(sfx.breath(0.38, False, 200 + k), at + 0.36, 0.12)
        k += 1
        at += 0.62 + k * 0.04
    tr.add(pad([110.0, 130.8, 164.8], b2.DURATION - b2.LOOK_BACK + 0.5, 1.2, 1.2, 1100, 6),
           B2 + b2.LOOK_BACK - 0.3, 0.18)
    tr.add(sfx.sting("regular"), T["b3_fin"] + 0.35, 0.5)

    # ---------- FINAL BUENO: ducto ----------
    c1, c2, c3 = M["c1_ducto"], M["c2_azotea"], M["c3_radio"]
    C1, C2, C3 = T["c1_ducto"], T["c2_azotea"], T["c3_radio"]
    tr.add(band(alarm(c1.DURATION), None, 700), C1, 0.08)        # amortiguada: estás dentro del ducto
    tr.add(sfx.scan_hum(c1.DURATION), C1, 0.06, -0.2)
    tr.add(sfx.scan_hum(c1.DURATION, 233), C1, 0.06, 0.3)
    tr.add(pad([73.4, 146.8, 155.6, 220.0], c1.DURATION, 0.5, 0.5, 800, 11), C1, 0.16)
    k = 0
    while True:
        lt = 0.25 + k / 2.6
        k += 1
        if lt > c1.DURATION - 0.2:
            break
        if c1.FREEZE[0] - 0.1 < lt < c1.FREEZE[1]:
            continue
        tr.add(sfx.tap(300 + k), C1 + lt, 0.1, -0.3 + 0.6 * lt / c1.DURATION)
    for i in range(2):
        tr.add(sfx.heartbeat(), C1 + c1.FREEZE[0] + 0.1 + i * 0.7, 0.5)
    tr.add(sfx.scan_hum(c1.FREEZE[1] - c1.FREEZE[0] + 0.4, 440), C1 + c1.FREEZE[0] - 0.2, 0.05)
    tr.add(sfx.clang(510), C1 + c1.GRILLE[1], 0.35, 0.6)
    # azotea
    wind = band(noise(c2.DURATION, 15), 180, 900)
    tr.add(fade(norm(wind), 0.4, 0.6), C2, 0.2)
    hum = fade(norm(band(noise(c2.FREEZE_AT, 16), 40, 260)), 0.4, 0.05)
    tr.add(hum, C2, 0.2)
    tr.add(sfx.boom(2.5), C2 + c2.FREEZE_AT, 0.35)
    tr.add(pad([293.7, 440.0, 587.3, 659.3], c2.DURATION - c2.FREEZE_AT + 0.5, 1.5, 1.0, 3500, 12),
           C2 + c2.FREEZE_AT, 0.12)
    for k in range(3):
        tr.add(sfx.tap(400 + k), C2 + 0.2 + k * 0.38, 0.08)
    run_steps(tr, C2 + 1.4, C2 + 3.3, 2.2, 0.18, 0.0, 120)
    # radio
    tr.add(fade(sfx.static(c3.DURATION - c3.CLICK_AT, 63), 0.1, 0.5), C3 + c3.CLICK_AT, 0.04)
    tr.add(sfx.radio_click(), C3 + c3.CLICK_AT, 0.45)
    tr.add(pad([146.8, 185.0, 220.0, 293.7], c3.DURATION - 3.4, 1.2, 0.8, 2200, 13), C3 + 3.4, 0.2)
    tr.add(sfx.sting("bueno"), T["c4_fin"] + 0.35, 0.5)

    # ---------- cierre ----------
    O = T["outro"]
    tr.add(pad([146.8, 220.0, 293.7], M["outro"].DURATION, 0.5, 1.0, 1500, 14), O, 0.22)
    blips(O + 0.15, 0.1, 9)
    for i in range(3):
        tr.add(sfx.tick(), O + 0.75 + i * 0.25, 0.16)
    at = O + 1.9
    while at < O + M["outro"].DURATION - 0.5:
        tr.add(sfx.heartbeat(), at, 0.3)
        at += 0.85

    return master(tr.buf, total_out, voices, 0.4), total_out
