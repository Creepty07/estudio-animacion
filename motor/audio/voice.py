"""Efectos de cada personaje sobre la voz sintetizada (la voz base viene de audio/tts.py)."""
import numpy as np
from motor.config import SR
from motor.audio.synth import band, norm, tt


def _echo(x, taps=((0.07, 0.35), (0.13, 0.25), (0.21, 0.16), (0.33, 0.1))):
    out = np.concatenate([x, np.zeros(int(0.5 * SR))])
    for delay, g in taps:
        d = int(delay * SR)
        out[d:d + len(x)] += g * x
    return out


def fx_none(x):
    return norm(band(x, 70, 12000), 0.85)


def fx_robot(x):
    """Tito: modulación en anillo suave + eco metálico corto; se entiende pero suena a máquina."""
    t = tt(len(x) / SR)
    y = 0.75 * x + 0.45 * x * np.sin(2 * np.pi * 52 * t)
    d = int(0.008 * SR)
    comb = y.copy()
    comb[d:] += 0.4 * y[:-d]
    comb = np.round(band(comb, 160, 7000) * 64) / 64
    return norm(band(comb, 140, 8000), 0.85)


def fx_agora(x):
    """Ágora: serena, con un leve coro y eco de sala grande."""
    t = tt(len(x) / SR)
    d = int(0.012 * SR)
    chorus = x.copy()
    chorus[d:] += 0.45 * x[:-d] * (0.8 + 0.2 * np.sin(2 * np.pi * 0.7 * t[d:]))
    return norm(band(_echo(band(chorus, 110, 9000)), 90, 9000), 0.85)


def fx_radio(x):
    """Voz a través de una radio: banda estrecha, saturada y con estática."""
    y = np.tanh(norm(band(x, 350, 3300)) * 2.2)
    static = band(np.random.default_rng(3).standard_normal(len(y)), 1500, 6000) * 0.06
    return norm(y + static, 0.85)


def _vibrato(x, depth=0.0007, rate=5.2):
    """Oscilación leve de tono (retardo variable): la voz 'tiembla' como si no estuviera del todo ahí."""
    n = len(x)
    idx = np.arange(n) + depth * SR * np.sin(2 * np.pi * rate * np.arange(n) / SR)
    return np.interp(idx, np.arange(n), x)


def _tail(x, taps):
    """Ecos largos y cada vez más opacos (taps = (retardo s, ganancia, corte agudo Hz))."""
    out = np.concatenate([x, np.zeros(int(max(d for d, _, _ in taps) * SR) + 1)])
    for delay, gain, hi in taps:
        d = int(delay * SR)
        out[d:d + len(x)] += gain * band(x, 150, hi)
    return out


def fx_espectro(x):
    """La Llorona: voz que tiembla, con un doble grave desafinado, aire y ecos largos."""
    import librosa
    y = _vibrato(x)
    low = librosa.effects.pitch_shift(np.asarray(y, dtype=float), sr=SR, n_steps=-4)
    y = 0.8 * y + 0.45 * low
    env = np.convolve(np.abs(y), np.ones(int(0.03 * SR)) / int(0.03 * SR), mode="same")
    air = band(np.random.default_rng(17).standard_normal(len(y)), 800, 5000)
    y = y + 0.35 * air * env / max(env.max(), 1e-6)
    return norm(_tail(band(y, 120, 9000), ((0.21, 0.5, 3500), (0.43, 0.36, 2800), (0.69, 0.24, 2200), (0.97, 0.13, 1800))), 0.85)


def fx_susurro(x):
    """Susurro: se conserva el contorno de la voz pero con fase al azar (suena a aire, sin tono), más eco."""
    import librosa
    spec = librosa.stft(np.asarray(x, dtype=float), n_fft=1024, hop_length=256)
    phase = np.exp(1j * np.random.default_rng(5).uniform(0, 2 * np.pi, spec.shape))
    y = librosa.istft(np.abs(spec) * phase, hop_length=256, length=len(x))
    return norm(_tail(band(y, 300, 7000), ((0.18, 0.35, 3000), (0.4, 0.22, 2400), (0.7, 0.12, 1800))), 0.85)


FX = {"none": fx_none, "robot": fx_robot, "agora": fx_agora, "radio": fx_radio,
      "espectro": fx_espectro, "susurro": fx_susurro}
