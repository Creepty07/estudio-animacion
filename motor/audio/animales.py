"""Sonidos de perro sintetizados (ladridos, aullidos, quejidos, gruñidos, olfateo, jadeo, patas).

No hay samples ni TTS: una fuente de pulsos con armónicos pasa por filtros que imitan la garganta (formantes).
Las funciones devuelven señales mono a 48 kHz.
"""
import numpy as np
from motor.config import SR
from motor.audio.synth import tt, noise, band, norm, env_exp, fade, thump, reverb

_GARGANTA = ((600, 950, 1.0), (1300, 2300, 0.55), (2600, 4200, 0.2))


def _garganta(x, formantes=_GARGANTA):
    return sum(g * band(x, lo, hi) for lo, hi, g in formantes)


def ladrido(f0=430.0, dur=0.26, seed=0):
    """Un ladrido: tono que cae del agudo al grave, golpe de aire al inicio y caída rápida."""
    t = tt(dur)
    f = f0 * (0.85 + 0.45 * np.exp(-t / 0.06))
    ph = 2 * np.pi * np.cumsum(f) / SR
    fuente = sum(np.sin(h * ph) / h ** 0.9 for h in range(1, 22)) + 0.35 * noise(dur, 200 + seed) * np.exp(-t / 0.03)
    env = np.minimum(1, t / 0.008) * np.exp(-t / 0.075)
    return fade(norm(_garganta(fuente) * env), 0.002, 0.04)


def ladridos(veces=2, separacion=0.30, f0=430.0, seed=0, espacio=0.0):
    """Serie de ladridos, cada uno un poco distinto. espacio > 0 agrega reverb (ladrido lejano en la niebla)."""
    out = np.zeros(int((veces * separacion + 0.4) * SR))
    for i in range(veces):
        b = ladrido(f0 * (1 + 0.04 * (i % 2)), 0.26 + 0.03 * (i % 2), seed + i) * (1 - 0.1 * i)
        k = int(i * separacion * SR)
        out[k:k + len(b)] += b
    return reverb(out, 2.6, espacio, seed, 3500) if espacio else out


def aullido(dur=3.6, f0=330.0, pico=640.0, seed=0, lejano=False):
    """Aullido: sube, se sostiene con vibrato y cae. lejano = apagado y con mucho eco."""
    t = tt(dur)
    k = t / dur
    sube = np.clip(k / 0.35, 0, 1)
    baja = np.clip((k - 0.7) / 0.3, 0, 1)
    f = f0 + (pico - f0) * sube ** 0.8 - (pico - f0 * 1.05) * baja ** 1.2
    f = f * (1 + 0.012 * np.sin(2 * np.pi * 5.2 * t) * np.clip((t - 0.4) / 0.5, 0, 1))
    ph = 2 * np.pi * np.cumsum(f) / SR
    voz = band(sum(a * np.sin(h * ph) for h, a in enumerate((1, 0.7, 0.5, 0.35, 0.22, 0.14, 0.09), start=1)), 250, 3200)
    voz = voz + 0.12 * band(noise(dur, 300 + seed), 1200, 5000) * np.clip(k / 0.2, 0, 1)
    sig = norm(voz * np.clip(t / 0.35, 0, 1) * np.clip((dur - t) / 0.8, 0, 1) ** 1.5)
    if lejano:
        return reverb(band(sig, None, 1800), 3.2, 0.7, seed)
    return reverb(sig, 2.2, 0.4, seed)


def quejido(f0=900.0, dur=0.22, seed=0):
    """Quejido corto y agudo (susto de un perro que huye)."""
    t = tt(dur)
    f = f0 * (1.0 - 0.45 * (t / dur) ** 0.7)
    ph = 2 * np.pi * np.cumsum(f) / SR
    fuente = sum(np.sin(h * ph) / h for h in range(1, 9)) + 0.15 * noise(dur, 250 + seed)
    return fade(norm(band(fuente, 500, 4500) * np.minimum(1, t / 0.01) * np.exp(-t / 0.11)), 0.002, 0.05)


def grunido(dur=2.0, grave=95.0, seed=0):
    """Gruñido bajo y áspero (modulación rápida de la amplitud)."""
    t = tt(dur)
    ph = 2 * np.pi * np.cumsum(grave * (1 + 0.05 * np.sin(2 * np.pi * 0.7 * t))) / SR
    aspero = 0.55 + 0.45 * np.sin(2 * np.pi * 28 * t)
    voz = band(sum(np.sin(h * ph) / h ** 0.5 for h in range(1, 14)) * aspero, 90, 900)
    voz = voz + 0.25 * band(noise(dur, 400 + seed), 200, 1200) * aspero
    return fade(norm(voz * np.clip(t / 0.4, 0, 1) * np.clip((dur - t) / 0.5, 0, 1)), 0.01, 0.2)


def olfateo(veces=3, seed=0):
    """Husmeo rápido: varias inhalaciones cortas de aire."""
    out = np.zeros(int((veces * 0.17 + 0.2) * SR))
    for i in range(veces):
        d = 0.11
        s = band(noise(d, 600 + seed * 10 + i), 900, 5200) * np.hanning(int(d * SR)) ** 0.7
        k = int(i * 0.17 * SR)
        out[k:k + len(s)] += s * (1 - 0.12 * i)
    return norm(out)


def resoplido(dur=0.4, seed=0):
    """Bufido de desprecio: exhalación seca por la nariz."""
    n = int(dur * SR)
    s = band(noise(dur, 700 + seed), 400, 3000) * env_exp(n, 0.09) * np.minimum(1, tt(dur) / 0.015)
    return norm(s + 0.25 * thump(110, dur, 0.06))


def jadeo(dur=1.6, ritmo=0.28, seed=0):
    """Jadeo de perro cansado."""
    out = np.zeros(int(dur * SR))
    k, i = 0.0, 0
    while k < dur - 0.2:
        d = 0.2
        s = band(noise(d, 800 + seed + i), 600, 4200) * np.hanning(int(d * SR))
        a = int(k * SR)
        out[a:a + len(s)] += s * (0.8 + 0.2 * (i % 2))
        k += ritmo
        i += 1
    return norm(out)


def pata(seed=0):
    """Pata sobre tierra o piedra: golpe sordo y un roce."""
    s = 0.5 * thump(110, 0.09, 0.02) + 0.35 * band(noise(0.09, 500 + seed), 1500, 6000) * env_exp(int(0.09 * SR), 0.012)
    return norm(s)


def masticar(dur=1.6, seed=0):
    """Un perro comiendo: bocados suaves y húmedos."""
    out = np.zeros(int(dur * SR))
    r = np.random.default_rng(seed)
    k = 0.0
    while k < dur - 0.1:
        d = 0.06
        s = band(noise(d, int(r.integers(1, 10 ** 6))), 700, 4000) * np.hanning(int(d * SR))
        a = int(k * SR)
        out[a:a + len(s)] += s * r.uniform(0.5, 1.0)
        k += r.uniform(0.13, 0.2)
    return norm(out)
