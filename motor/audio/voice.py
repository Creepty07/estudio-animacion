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


FX = {"none": fx_none, "robot": fx_robot, "agora": fx_agora, "radio": fx_radio}
