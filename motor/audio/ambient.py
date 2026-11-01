"""Ambientes continuos (fondos de sonido) sintetizados. Cada función devuelve una señal mono a 48 kHz."""
import numpy as np
from motor.config import SR
from motor.audio.synth import tt, noise, band, norm, fade


def wind(dur, seed=5, lo=180, hi=900, gust=0.35):
    """Viento: ruido filtrado con ráfagas lentas."""
    sig = band(noise(dur, seed), lo, hi)
    t = tt(dur)
    slow = np.convolve(noise(dur, seed + 1), np.ones(int(0.8 * SR)) / int(0.8 * SR), mode="same")
    slow = slow / max(np.abs(slow).max(), 1e-6)
    sig *= (1 - gust) + gust * (0.5 + 0.5 * slow) + 0.1 * np.sin(2 * np.pi * 0.21 * t)
    return fade(norm(sig), 0.8, 1.2)


def crickets(dur, seed=7, voices=3):
    """Grillos: trenes de pulsos agudos, cada uno con su tono y su ritmo."""
    t = tt(dur)
    r = np.random.default_rng(seed)
    out = np.zeros(len(t))
    for _ in range(voices):
        f = r.uniform(4200, 5400)
        period = r.uniform(0.38, 0.55)
        phase = r.uniform(0, period)
        local = (t + phase) % period
        gate = np.zeros(len(t))
        for k in range(3):
            c = 0.05 + k * 0.075
            gate += np.exp(-((local - c) / 0.018) ** 2)
        out += np.sin(2 * np.pi * f * t) * gate * r.uniform(0.6, 1.0)
    return fade(norm(out), 1.0, 1.0)


def water(dur, seed=9):
    """Agua quieta de canal: chapoteo suave y lento."""
    t = tt(dur)
    sig = band(noise(dur, seed), 160, 1400)
    sig *= 0.55 + 0.25 * np.sin(2 * np.pi * 0.37 * t) + 0.2 * np.sin(2 * np.pi * 0.71 * t + 1.3)
    return fade(norm(sig), 0.8, 1.0)


def dawn_birds(dur, seed=11, chirps=14):
    """Pájaros del amanecer: gorjeos cortos con glissando."""
    out = np.zeros(int(dur * SR))
    r = np.random.default_rng(seed)
    for _ in range(chirps):
        at = r.uniform(0, max(dur - 0.5, 0.1))
        d = r.uniform(0.07, 0.2)
        f0, f1 = r.uniform(2200, 3800), r.uniform(2800, 5200)
        t = tt(d)
        f = f0 + (f1 - f0) * (t / d) ** 0.6
        chirp = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.hanning(len(t))
        for rep in range(int(r.integers(1, 4))):
            i = int((at + rep * (d + 0.05)) * SR)
            if i + len(chirp) < len(out):
                out[i:i + len(chirp)] += chirp * r.uniform(0.5, 1.0)
    return fade(norm(out), 0.3, 0.6)


def lamp_hum(dur, freq=55.0):
    """Zumbido grave y constante (tensión)."""
    t = tt(dur)
    sig = np.sin(2 * np.pi * freq * t) + 0.5 * np.sin(2 * np.pi * freq * 2.01 * t) + 0.2 * np.sin(2 * np.pi * freq * 3 * t)
    sig *= 0.8 + 0.2 * np.sin(2 * np.pi * 0.3 * t)
    return fade(norm(sig), 1.0, 1.0)
