"""Efectos de sonido reutilizables (devuelven señales mono a 48 kHz)."""
import numpy as np
from motor.config import SR
from motor.audio.synth import tt, noise, band, norm, env_exp, fade, sweep, tone, metal, thump, pad


def n(dur):
    return int(dur * SR)


def boom(dur=3.0):
    return thump(48, dur, 1.1) + 0.3 * band(noise(dur, 1), None, 180) * env_exp(n(dur), 0.4)


def glitch_blips(seed=3, count=14, span=1.2):
    """Lista de (desfase, señal, ganancia relativa, paneo)."""
    r = np.random.default_rng(seed)
    out = []
    for i in range(count):
        d = r.uniform(0.02, 0.07)
        if i % 2:
            s = band(noise(d, seed * 100 + i), 1500, 9000)
        else:
            s = np.sign(np.sin(2 * np.pi * r.uniform(300, 1600) * tt(d)))
        out.append((r.uniform(0, span) * (i / count), fade(s, 0.002, 0.01), 1 - i / (count + 2), r.uniform(-0.6, 0.6)))
    return out


def tick(freq=1320, dur=0.12):
    return np.sin(2 * np.pi * freq * tt(dur)) * env_exp(n(dur), 0.03)


def whoosh(dur=0.6, lo=300, hi=3000, seed=9):
    return norm(band(noise(dur, seed), lo, hi) * np.hanning(n(dur)))


def ding():
    t = tt(2.0)
    s = (np.sin(2 * np.pi * 1318.5 * t) + 0.4 * np.sin(2 * np.pi * 2637 * t) + 0.25 * np.sin(2 * np.pi * 3955 * t))
    return fade(s * env_exp(n(2.0), 0.55), 0.003, 0.3)


def door_slide(dur=0.7, seed=21):
    s = band(noise(dur, seed), 200, 1800) * np.hanning(n(dur))
    s += 0.4 * band(sweep(90, 70, dur, "saw"), None, 500) * np.hanning(n(dur))
    return norm(s)


def motor_hum(dur, seed=4):
    t = tt(dur)
    s = band(sweep(55, 62, dur, "saw"), None, 300) + 0.3 * band(noise(dur, seed), 60, 400)
    s *= 0.85 + 0.15 * np.sin(2 * np.pi * 7 * t)
    return fade(norm(s), 0.4, 0.3)


def jolt(seed=31):
    return norm(1.4 * thump(55, 1.0, 0.25) + metal([110, 187, 260, 410], 1.0, 0.3, seed))


def clang(seed=500):
    return norm(metal([92, 151, 233, 368, 522, 761], 1.6, 0.45, seed=seed) + 1.6 * thump(48, 1.6, 0.3))


def cable_snap():
    crack = band(noise(0.08, 77), 1500, 12000) * env_exp(n(0.08), 0.01)
    ping = metal([2100, 3300, 4700, 6100], 0.8, 0.18, 12)
    whip = whoosh(0.35, 800, 5000, 78)
    out = np.zeros(n(0.8))
    out[: len(crack)] += crack * 1.6
    out += ping * 0.6
    out[: len(whip)] += whip * 0.5
    return norm(out)


def falling(dur):
    s = band(noise(dur, 88), 200, 3000) * np.linspace(0.2, 1.0, n(dur)) ** 1.5
    s += 0.3 * sweep(80, 300, dur) * np.linspace(0, 1, n(dur))
    return norm(s)


def crash():
    dur = 2.5
    s = band(noise(dur, 99), 60, 6000) * env_exp(n(dur), 0.35)
    s += 2.0 * thump(40, dur, 0.6)
    s += 0.8 * metal([70, 113, 166, 240, 330], dur, 0.8, 5)
    return norm(s)


def step_concrete(seed=0):
    s = 1.3 * thump(85, 0.18, 0.04) + 0.5 * band(noise(0.18, 300 + seed), 900, 5000) * env_exp(n(0.18), 0.015)
    return norm(s)


def step_metal(seed=0, base=170):
    return norm(metal([base, 395, 710, 1120], 0.5, 0.12, seed=seed) + 1.4 * thump(62, 0.5, 0.09))


def cloth_rip(dur=0.35, seed=41):
    s = band(noise(dur, seed), 1200, 6000)
    jitter = (np.random.default_rng(seed).random(n(dur)) > 0.6).astype(float)
    jitter = np.convolve(jitter, np.ones(120) / 120, mode="same")
    return norm(s * jitter * np.hanning(n(dur)))


def breath(dur=0.5, inhale=True, seed=51):
    s = band(noise(dur, seed), 500 if inhale else 350, 2400 if inhale else 1600)
    env = np.hanning(n(dur)) ** (0.7 if inhale else 1.2)
    return norm(s * env)


def tap(seed=0):
    return norm(metal([310, 523, 870], 0.25, 0.05, seed) + 0.6 * thump(120, 0.25, 0.03))


def scan_hum(dur, freq=220):
    t = tt(dur)
    s = np.sin(2 * np.pi * freq * t) + 0.5 * np.sin(2 * np.pi * freq * 1.5 * t)
    s *= 0.6 + 0.4 * np.sin(2 * np.pi * 3.2 * t)
    return fade(norm(s), 0.3, 0.3)


def static(dur, seed=61):
    s = band(noise(dur, seed), 1200, 7000)
    r = np.random.default_rng(seed)
    crackle = np.zeros(n(dur))
    for _ in range(int(dur * 40)):
        i = r.integers(0, max(1, len(crackle) - 100))
        crackle[i:i + 100] += r.uniform(-1, 1) * np.exp(-np.arange(100) / 15)
    return norm(0.5 * s + crackle)


def radio_click():
    c = band(noise(0.03, 71), 500, 6000) * env_exp(n(0.03), 0.005)
    out = np.zeros(n(0.4))
    out[: len(c)] += c * 2
    st = static(0.35, 72) * np.linspace(1, 0, n(0.35))
    out[n(0.05): n(0.05) + len(st)] += 0.5 * st
    return norm(out)


def heartbeat():
    out = np.zeros(n(0.6))
    out += thump(52, 0.6, 0.09)
    b = thump(46, 0.36, 0.09)
    out[n(0.24): n(0.24) + len(b)] += 0.7 * b
    return norm(out)


def sting(kind):
    """Golpe musical de la tarjeta de resultado."""
    if kind == "malo":
        s = 1.2 * boom(3.5) + 0.5 * pad([36.7, 73.4, 77.8, 110.0], 3.5, 0.02, 1.5, 700, 7)
    elif kind == "regular":
        s = 0.6 * thump(55, 3.5, 0.6) + pad([110.0, 130.8, 164.8, 220.0], 3.5, 0.05, 1.6, 1400, 8)
    else:
        s = 0.5 * thump(60, 4.0, 0.5) + pad([146.8, 185.0, 220.0, 293.7, 370.0], 4.0, 0.08, 1.8, 2600, 9)
        s += 0.3 * pad([587.3, 740.0, 880.0], 4.0, 0.4, 1.8, 5000, 10)
    return norm(s)
