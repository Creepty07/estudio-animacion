"""Síntesis de sonidos con numpy: tonos, ruido, filtros y efectos."""
import numpy as np
from motor.config import SR

RNG = np.random.default_rng(42)


def tt(dur):
    return np.arange(int(dur * SR)) / SR


def noise(dur, seed=None):
    r = np.random.default_rng(seed) if seed is not None else RNG
    return r.standard_normal(int(dur * SR))


def band(sig, lo=None, hi=None, soft=0.15):
    """Filtro pasa-banda por FFT con bordes suaves (lo/hi en Hz)."""
    n = len(sig)
    spec = np.fft.rfft(sig)
    f = np.fft.rfftfreq(n, 1 / SR)
    mask = np.ones_like(f)
    if lo:
        mask *= 1 / (1 + (lo / np.maximum(f, 1e-3)) ** (2 / soft * 0.3))
    if hi:
        mask *= 1 / (1 + (f / hi) ** (2 / soft * 0.3))
    return np.fft.irfft(spec * mask, n)


def norm(sig, peak=1.0):
    m = np.max(np.abs(sig)) if len(sig) else 0
    return sig * (peak / m) if m > 0 else sig


def env_exp(n, decay):
    return np.exp(-np.arange(n) / SR / decay)


def fade(sig, a=0.01, r=0.05):
    n = len(sig)
    e = np.ones(n)
    na, nr = min(n, int(a * SR)), min(n, int(r * SR))
    if na:
        e[:na] = np.linspace(0, 1, na)
    if nr:
        e[n - nr:] *= np.linspace(1, 0, nr)
    return sig * e


def sweep(f0, f1, dur, wave="sine", curve="exp"):
    t = tt(dur)
    if curve == "exp":
        f = f0 * (f1 / f0) ** (t / dur)
    else:
        f = f0 + (f1 - f0) * t / dur
    ph = 2 * np.pi * np.cumsum(f) / SR
    if wave == "saw":
        return 2 * ((ph / (2 * np.pi)) % 1) - 1
    if wave == "square":
        return np.sign(np.sin(ph))
    return np.sin(ph)


def tone(freq, dur, harmonics=(1.0,), vibrato=0.0, vib_rate=5.0):
    t = tt(dur)
    f = freq * (1 + vibrato * np.sin(2 * np.pi * vib_rate * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    out = np.zeros_like(t)
    for k, a in enumerate(harmonics, start=1):
        out += a * np.sin(k * ph)
    return out


def metal(partials, dur, decay, seed=0):
    """Golpe metálico: parciales inarmónicos que decaen + transitorio de ruido."""
    t = tt(dur)
    r = np.random.default_rng(seed)
    out = np.zeros_like(t)
    for i, p in enumerate(partials):
        out += np.sin(2 * np.pi * p * t + r.uniform(0, 6)) * np.exp(-t / (decay * (1 - i * 0.07))) / (1 + i * 0.4)
    click = band(noise(dur, seed), 800, 6000) * np.exp(-t / 0.012)
    return out + 0.6 * click


def thump(freq, dur, decay):
    t = tt(dur)
    f = freq * (1 + 1.5 * np.exp(-t / 0.03))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / decay)


def pad(freqs, dur, attack=1.5, release=1.5, bright=900, seed=1):
    t = tt(dur)
    r = np.random.default_rng(seed)
    out = np.zeros_like(t)
    for f in freqs:
        for det in (-0.004, 0.0, 0.005):
            ph = 2 * np.pi * f * (1 + det) * t + r.uniform(0, 6)
            out += np.sin(ph) + 0.35 * np.sin(2 * ph) + 0.15 * np.sin(3 * ph)
    out = band(out, None, bright)
    out *= 0.85 + 0.15 * np.sin(2 * np.pi * 0.13 * t)
    return fade(norm(out), attack, release)


def reverb(sig, t60=1.6, wet=0.3, seed=0, brillo=4500):
    """Reverberación por convolución con una cola de ruido que decae (da espacio: cueva, río, noche abierta).
    t60 = segundos hasta que la cola baja 60 dB; wet = cuánto suena la cola respecto a la señal seca."""
    from scipy.signal import fftconvolve
    n = int(t60 * SR)
    ir = band(noise(t60, 500 + seed), 120, brillo) * np.exp(-np.arange(n) / SR * 6.9 / t60)
    ir[: int(0.012 * SR)] *= np.linspace(0, 1, int(0.012 * SR))
    ir /= max(np.abs(ir).max(), 1e-9)
    tail = fftconvolve(sig, ir)[: len(sig) + n]
    tail *= (np.abs(sig).max() / max(np.abs(tail).max(), 1e-9)) * wet
    out = np.concatenate([sig, np.zeros(n)])
    out[: len(tail)] += tail
    return out


class Track:
    """Pista estéreo donde se colocan sonidos en el tiempo.

    Con tmap (tiempo sin voz -> tiempo con voz), cada sonido se coloca donde cae su escena ya alargada;
    los sonidos largos (fondos, alarmas, zumbidos) se estiran sin cambiar de tono para seguir cubriendo
    su tramo, y los cortos (golpes, pasos) se colocan tal cual para no perder su ataque.
    """

    def __init__(self, dur, tmap=None, out_dur=None):
        self.tmap = tmap
        self.buf = np.zeros((int((out_dur or dur) * SR) + SR, 2))

    def add(self, sig, at, gain=1.0, pan=0.0):
        if self.tmap is not None:
            length = len(sig) / SR
            start = self.tmap(at)
            if length > 1.2:
                ratio = (self.tmap(at + length) - start) / length
                if ratio > 1.03:
                    from motor import config as _cfg
                    if getattr(_cfg, "ESTIRAR_RAPIDO", False):                 # remuestreo lineal: muy rápido; baja un poco el tono (válido para fondos)
                        x = np.asarray(sig, dtype=float)
                        sig = np.interp(np.linspace(0, len(x) - 1, int(len(x) * ratio)), np.arange(len(x)), x)
                    else:
                        import warnings
                        import librosa
                        with warnings.catch_warnings():
                            warnings.simplefilter("ignore")
                            sig = librosa.effects.time_stretch(np.asarray(sig, dtype=float), rate=1 / ratio)
            at = start
        i = int(at * SR)
        if i >= len(self.buf) or len(sig) == 0:
            return
        sig = sig[: len(self.buf) - i]
        l = np.cos((pan + 1) * np.pi / 4)
        r = np.sin((pan + 1) * np.pi / 4)
        self.buf[i:i + len(sig), 0] += sig * gain * l
        self.buf[i:i + len(sig), 1] += sig * gain * r
