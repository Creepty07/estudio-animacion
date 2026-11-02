"""Sonidos de agua sintetizados: chapoteos, nado, agua que sube y gotas. Señales mono a 48 kHz."""
import numpy as np
from motor.config import SR
from motor.audio.synth import tt, noise, band, norm, env_exp, fade, sweep


def chapoteo(dur=1.0, seed=0, fuerza=1.0):
    """Salpicadura: golpe de ruido de agua y burbujas que suben de tono."""
    n = int(dur * SR)
    t = tt(dur)
    s = band(noise(dur, 900 + seed), 250, 4500) * np.minimum(1, t / 0.01) * np.exp(-t / (0.12 + 0.1 * fuerza))
    r = np.random.default_rng(seed)
    for _ in range(int(8 + 8 * fuerza)):
        d = r.uniform(0.04, 0.09)
        b = sweep(r.uniform(450, 900), r.uniform(1200, 2200), d, curve="lin") * np.hanning(int(d * SR))
        a = int(r.uniform(0.02, min(0.6, dur - 0.1)) * SR)
        s[a:a + len(b)] += 0.25 * b[: max(0, n - a)]
    return fade(norm(s), 0.003, 0.15)


def nado(dur=3.0, ritmo=0.62, seed=0):
    """Un animal nadando: brazadas suaves y alternadas sobre el agua."""
    out = np.zeros(int(dur * SR))
    k, i = 0.0, 0
    while k < dur - 0.3:
        c = chapoteo(0.5, seed + i, 0.35) * (0.7 + 0.3 * (i % 2))
        a = int(k * SR)
        out[a:a + len(c)] += c[: max(0, len(out) - a)]
        k += ritmo
        i += 1
    return norm(out)


def agua_sube(dur=1.8, seed=0):
    """Agua que se levanta despacio (manos, olas): un swell que crece y se deshace en gotas."""
    n = int(dur * SR)
    t = tt(dur)
    s = band(noise(dur, 950 + seed), 150, 2200) * np.hanning(n) ** 1.4
    r = np.random.default_rng(seed)
    for _ in range(6):
        a = int(r.uniform(dur * 0.5, dur - 0.2) * SR)
        g = gota(seed + _)
        s[a:a + len(g)] += 0.35 * g[: max(0, n - a)]
    return fade(norm(s), 0.05, 0.4)


def gota(seed=0):
    """Una gota que cae al agua."""
    r = np.random.default_rng(seed)
    d = 0.14
    t = tt(d)
    f0 = r.uniform(900, 1400)
    return norm(np.sin(2 * np.pi * np.cumsum(f0 * (1 + 1.6 * t / d)) / SR) * np.exp(-t / 0.035))
