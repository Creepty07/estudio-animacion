"""Instrumentos de inspiración mesoamericana, sintetizados con numpy (sin samples: cero derechos de autor).

Sirven para historias de leyenda sin narrador: el tambor, el caracol y la flauta cuentan lo que la voz no dice.
Todas las funciones devuelven señales mono a 48 kHz, ya con su reverberación.
"""
import numpy as np
from motor.config import SR
from motor.audio.synth import tt, noise, band, norm, env_exp, fade, thump, reverb


def huehuetl(fuerza=1.0, seed=0, grave=62.0, dur=2.4, espacio=0.28):
    """Tambor vertical grave: cuerpo que cae de tono + palmada de parche (ruido) + resonancia de la madera."""
    t = tt(dur)
    cuerpo = thump(grave, dur, 0.55)
    madera = sum(a * np.sin(2 * np.pi * grave * m * t) * np.exp(-t / d)
                 for m, d, a in ((1.55, 0.35, 0.35), (2.3, 0.22, 0.20), (3.4, 0.12, 0.12)))
    palmada = band(noise(0.12, 50 + seed), 300, 3200) * env_exp(int(0.12 * SR), 0.02)
    out = cuerpo + 0.6 * madera
    out[: len(palmada)] += 0.8 * fuerza * palmada
    return reverb(norm(fade(out, 0.002, 0.4)), 1.8, espacio, seed)


def caracol(freq=233.0, dur=3.2, seed=0, espacio=0.35):
    """Trompeta de caracol: entra desde abajo del tono, timbre rico y soplo de aire; llamado largo y lejano."""
    t = tt(dur)
    f = freq * (1 - 0.05 * np.exp(-t / 0.15))
    f = f * (1 + 0.006 * np.sin(2 * np.pi * 5.2 * t) * np.clip(t / 0.6, 0, 1))
    ph = 2 * np.pi * np.cumsum(f) / SR
    voz = sum(a * np.sin(h * ph) for h, a in enumerate((1.0, 0.8, 0.65, 0.45, 0.3, 0.2, 0.12, 0.08), start=1))
    voz = band(voz, 120, 2400) + 0.18 * band(noise(dur, 70 + seed), 600, 3500)
    env = np.clip(t / 0.35, 0, 1) ** 1.5 * np.exp(-np.maximum(t - dur * 0.55, 0) / (dur * 0.28))
    return reverb(norm(voz * env), 2.4, espacio, seed, 3500)


def flauta(freq, dur=1.0, seed=0, vibrato=0.007, aire=0.10):
    """Una nota de flauta/ocarina: tono casi puro, soplo al inicio y vibrato que llega después."""
    t = tt(dur)
    f = freq * (1 + vibrato * np.sin(2 * np.pi * 5.0 * t) * np.clip((t - 0.12) / 0.3, 0, 1))
    ph = 2 * np.pi * np.cumsum(f) / SR
    voz = np.sin(ph) + 0.22 * np.sin(2 * ph) + 0.08 * np.sin(3 * ph)
    voz = voz + aire * band(noise(dur, 90 + seed), 1500, 6000) * np.exp(-t / 0.2) \
        + 0.03 * band(noise(dur, 95 + seed), 800, 5000)
    return voz * np.clip(t / 0.06, 0, 1) * np.clip((dur - t) / 0.18, 0, 1)


def melodia(notas, espacio=0.38, t60=2.0):
    """notas = [(frecuencia, inicio_s, duracion_s)]. Devuelve la frase completa con reverb de sala abierta."""
    total = max(a + d for _, a, d in notas) + 0.3
    out = np.zeros(int(total * SR))
    for i, (f, a, d) in enumerate(notas):
        s = flauta(f, d, i)
        k = int(a * SR)
        out[k:k + len(s)] += s
    return reverb(norm(out), t60, espacio, 3, 5000)


def sonaja(dur=0.7, densidad=90, seed=0):
    """Ayoyotes (semillas en los tobillos): ráfaga de granos de ruido agudo."""
    n = int(dur * SR)
    out = np.zeros(n)
    r = np.random.default_rng(seed)
    g_n = int(0.03 * SR)
    for _ in range(int(dur * densidad)):
        at = int(r.uniform(0, max(dur - 0.04, 0.01)) * SR)
        g = band(noise(0.03, int(r.integers(1, 10 ** 6))), 3500, 11000) * np.exp(-np.arange(g_n) / SR / 0.006)
        out[at:at + g_n] += g[: max(0, n - at)] * r.uniform(0.3, 1.0)
    return norm(out * np.hanning(n) ** 0.6)
