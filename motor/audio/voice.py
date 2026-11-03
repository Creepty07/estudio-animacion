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


def fx_radio_tetrico(x, seed=7):
    """Narrador que llega por una radio vieja en la noche: banda estrecha con el medio resaltado, saturación suave,
    una señal que sube y baja (como si se fuera la emisora), estática, un chasquido al abrir y cerrar el canal
    y un eco corto de cuarto vacío. Se entiende bien: el miedo está en el color, no en esconder la voz."""
    r = np.random.default_rng(seed)
    n = len(x)
    y = band(x, 300, 3400)
    y = y + 0.55 * band(x, 1200, 2600)                                              # medios de bocina
    y = np.tanh(norm(y) * 2.0)
    t = np.arange(n) / SR
    y = y * (0.88 + 0.12 * np.sin(2 * np.pi * 0.31 * t + r.uniform(0, 6)))          # la señal flota
    y = y * (1 - 0.35 * np.clip(np.sin(2 * np.pi * 7.3 * t) * np.sin(2 * np.pi * 0.9 * t), 0, 1) ** 4)   # leve interferencia
    est = band(r.standard_normal(n), 900, 7000)
    est = est * (0.05 + 0.04 * np.abs(np.sin(2 * np.pi * 1.7 * t)))
    for _ in range(int(2 + n / SR)):                                                # chasquidos sueltos
        i = int(r.uniform(0, max(n - 400, 1)))
        est[i:i + 300] += r.uniform(-0.25, 0.25) * np.exp(-np.arange(min(300, n - i)) / 40.0)
    y = y + est
    sq = int(0.045 * SR)                                                            # chasquido de apertura y cierre
    pad = np.zeros(int(0.12 * SR))
    y = np.concatenate([pad, y, pad])
    y[:sq] += band(r.standard_normal(sq), 600, 6000) * np.hanning(sq) * 0.35
    y[-sq:] += band(r.standard_normal(sq), 600, 6000) * np.hanning(sq) * 0.30
    d = int(0.11 * SR)                                                              # cuarto vacío
    out = np.concatenate([y, np.zeros(d)])
    out[d:d + len(y)] += 0.16 * band(y, 250, 2600)
    return norm(out, 0.85)


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


def fx_tetrico(x):
    """Narración sombría y limpia: un poco más de graves y una sala pequeña y oscura. No altera el tono."""
    y = band(x, 70, 9500)
    y = y + 0.35 * band(y, 80, 260)
    y = _tail(y, ((0.08, 0.16, 3000), (0.19, 0.10, 2400), (0.36, 0.06, 1800)))
    return norm(y, 0.85)


def fx_susurro_suave(x):
    """Susurro que sigue entendiéndose: voz baja y sin graves más aire que sigue su volumen, con cola larga."""
    y = band(x, 180, 7000)
    env = np.convolve(np.abs(y), np.ones(int(0.02 * SR)) / int(0.02 * SR), mode="same")
    env = env / max(env.max(), 1e-6)
    breath = band(np.random.default_rng(23).standard_normal(len(y)), 1500, 8000) * env * 0.5 * max(np.abs(y).max(), 1e-6)
    y = 0.6 * y + breath
    return norm(_tail(y, ((0.2, 0.3, 3000), (0.45, 0.2, 2400), (0.8, 0.12, 1800))), 0.75)


_VOCALES = {"a": ((750, 90, 1.0), (1250, 110, 0.5), (2600, 160, 0.25)),
            "i": ((300, 70, 1.0), (2300, 120, 0.45), (3100, 160, 0.25)),
            "o": ((450, 80, 1.0), (800, 90, 0.5), (2830, 150, 0.2)),
            "u": ((325, 70, 1.0), (700, 90, 0.4), (2530, 150, 0.15))}


def _resonar(src, vocal):
    """Filtra una fuente con los formantes de una vocal (resonadores de 2.º orden en paralelo)."""
    from scipy.signal import lfilter
    out = np.zeros(len(src))
    for f, bw, g in _VOCALES[vocal]:
        r = np.exp(-np.pi * bw / SR)
        out += g * lfilter([1 - r], [1, -2 * r * np.cos(2 * np.pi * f / SR), r * r], src)
    return out


def grito_sintetico(dur=2.2, seed=1, lejano=False, puntos=((0, 330), (0.12, 520), (0.4, 660), (0.7, 560), (1.0, 280)),
                    vocales=("a", "i")):
    """Lamento de mujer, 'aaaay': voz cantada sintetizada (fuente con vibrato + formantes de /a/ que pasa a /i/).

    No es un modelo de voz ni una grabación: se calcula directo, sin tono robótico de TTS.
    """
    r = np.random.default_rng(seed)
    n = int(dur * SR)
    t = np.arange(n) / SR
    k = t / dur
    f = np.interp(k, [p[0] for p in puntos], [p[1] for p in puntos])
    jit = np.convolve(r.standard_normal(n), np.ones(int(0.06 * SR)) / int(0.06 * SR), mode="same")
    f = f * (1 + (0.006 + 0.025 * k) * np.sin(2 * np.pi * 5.5 * t) + 0.12 * jit / max(np.abs(jit).max(), 1e-6) * 0.15)
    phase = np.cumsum(f) / SR
    src = 2 * (phase % 1.0) - 1.0
    src = src * np.exp(-0.0 * t) + 0.12 * r.standard_normal(n)            # un poco de aire
    a, i = _resonar(src, vocales[0]), _resonar(src, vocales[1])
    w = np.clip((k - 0.72) / 0.2, 0, 1)
    y = (1 - w) * a + w * i
    env = np.minimum(1, t / 0.08) * np.where(k < 0.75, 1.0, np.exp(-(k - 0.75) * 7))
    y = y * env * np.minimum(1, (n - np.arange(n)) / (0.08 * SR))
    if lejano:
        y = band(y, 300, 1800)
    return norm(_tail(band(y, 200, 6500), ((0.15, 0.4, 3500), (0.33, 0.3, 2800), (0.55, 0.2, 2200),
                                            (0.85, 0.12, 1800), (1.2, 0.07, 1500))), 0.85)


def aullido(dur=3.0, seed=2):
    """Aullido de perro lejano: tono largo que sube y baja, vocal /o/ que cierra en /u/, con mucha sala."""
    return grito_sintetico(dur, seed, lejano=True, puntos=((0, 240), (0.2, 420), (0.5, 470), (0.8, 380), (1.0, 230)),
                           vocales=("o", "u"))


def fx_grito(x, seed=1):
    """El grito de la Llorona sin TTS: ignora la voz de entrada y usa la duración del arreglo."""
    return grito_sintetico(max(len(x) / SR, 0.5), seed)


FX = {"none": fx_none, "tetrico": fx_tetrico, "susurro_suave": fx_susurro_suave, "grito": fx_grito, "robot": fx_robot, "agora": fx_agora, "radio": fx_radio, "radio_tetrico": fx_radio_tetrico,
      "espectro": fx_espectro, "susurro": fx_susurro}
