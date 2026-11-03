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


def murmullos(dur, seed=1, voces=3):
    """Voces susurradas que no se entienden: aire con formantes de vocal que se enciende y se apaga como sílabas."""
    from motor.audio.voice import _resonar
    r = np.random.default_rng(seed)
    n = int(dur * SR)
    out = np.zeros(n)
    for v in range(voces):
        gate = np.zeros(n)
        t = r.uniform(0, 0.4)
        while t < dur:
            d = r.uniform(0.10, 0.28)
            i, j = int(t * SR), min(n, int((t + d) * SR))
            gate[i:j] = np.hanning(max(j - i, 1)) ** 0.7
            t += d + r.uniform(0.04, 0.3) * (1 + (r.random() < 0.25) * 3)
        vocal = r.choice(["a", "i", "o", "u"])
        src = noise(dur, seed * 31 + v)
        w = _resonar(src, vocal) * gate
        w = band(w, 300, 6500)
        out += w / max(np.abs(w).max(), 1e-6) * r.uniform(0.5, 1.0)
    return fade(norm(out), 0.6, 0.8)


def fluorescente(dur, brillo=None, freq=120.0, seed=0):
    """Zumbido de fluorescente (red de 60 Hz: 120 Hz y armónicos) con un silbido agudo de balastro.
    brillo: función opcional t -> 0..1 (la misma del dibujo); cuando cae, el zumbido se apaga y cada vuelta suena un clic."""
    t = tt(dur)
    sig = np.sin(2 * np.pi * freq * t) + 0.55 * np.sin(2 * np.pi * freq * 2 * t + 0.7) + 0.30 * np.sin(2 * np.pi * freq * 3 * t + 1.9)
    sig += 0.15 * band(noise(dur, 70 + seed), 1800, 7000) + 0.04 * np.sin(2 * np.pi * 7100 * t)
    sig = sig * (0.92 + 0.08 * np.sin(2 * np.pi * 0.7 * t))
    if brillo is not None:
        ts = np.arange(0, dur, 1 / 60)
        g = np.array([brillo(x) for x in ts])
        gate = np.interp(t, ts, g) ** 2.0
        sig = sig * gate
        for i in np.where(np.abs(np.diff(g)) > 0.25)[0]:                       # clic del balastro al caer o volver
            j = int(ts[i + 1] * SR)
            c = band(noise(0.02, seed * 50 + int(i)), 1200, 8000) * np.exp(-np.arange(int(0.02 * SR)) / SR / 0.004)
            sig[j:j + len(c)] += 0.9 * c[: max(0, len(sig) - j)]
    return fade(norm(sig), 0.02, 0.05)


def lluvia(dur, seed=1, intensidad=1.0, interior=False):
    """Lluvia en lámina: ruido filtrado con ráfagas de densidad y un rumor grave; interior=True la apaga contra el vidrio y la carrocería."""
    t = tt(dur)
    lo, hi = (500, 4200) if interior else (900, 9500)
    sig = band(noise(dur, seed), lo, hi)
    dens = np.convolve(noise(dur, seed + 1), np.ones(int(0.35 * SR)) / int(0.35 * SR), mode="same")
    dens = 0.8 + 0.2 * dens / max(np.abs(dens).max(), 1e-6)
    sig = sig * dens + 0.5 * band(noise(dur, seed + 2), 120, 700) * (0.7 if interior else 0.35)
    r = np.random.default_rng(seed)
    for _ in range(int(dur * 14 * intensidad)):                                    # gotas gordas contra el vidrio o la lámina
        i = int(r.uniform(0, max(dur - 0.05, 0.01)) * SR)
        g = band(noise(r.uniform(0.008, 0.02), int(r.integers(0, 99999))), 1800, 7000)
        g = g * np.hanning(len(g))
        m = min(len(g), len(sig) - i)
        sig[i:i + m] += r.uniform(0.4, 1.2) * g[:m]
    return fade(norm(sig), 0.6, 0.8)


def motor_camion(dur, grave=1.0, seed=4, traqueteo=1.0):
    """Motor diésel viejo al ralentí: pulsos graves (~11 Hz), rumor de cilindros y traqueteo de lámina. grave<1 lo sube de tono (acelera)."""
    t = tt(dur)
    f = 11.0 / max(grave, 0.2)
    pulso = (0.55 + 0.45 * np.clip(np.sin(2 * np.pi * f * t), 0, 1) ** 2)
    base = np.sin(2 * np.pi * 46 / max(grave, 0.2) * t) + 0.6 * np.sin(2 * np.pi * 92 / max(grave, 0.2) * t + 1.1) + 0.3 * np.sin(2 * np.pi * 138 / max(grave, 0.2) * t)
    sig = band(base * pulso, 30, 420) + 0.35 * band(noise(dur, seed), 80, 900) * pulso
    sig += 0.12 * traqueteo * band(noise(dur, seed + 5), 700, 2600) * (0.5 + 0.5 * np.sin(2 * np.pi * 2.3 * t))
    return fade(norm(sig), 0.5, 0.6)
