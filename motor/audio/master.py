"""Etapa final: agrega las voces sobre la mezcla, baja el fondo cuando alguien habla y limita picos."""
import numpy as np
import soundfile as sf
from motor.config import SR
from motor.audio.synth import norm

BED_PEAK = 0.65      # el fondo queda por debajo de la voz
DUCK = 0.5           # cuánto se baja el fondo mientras hay voz
VOICE_PEAK = 0.9


def master(bed, total, voices, fade_out=0.45, bed_peak=BED_PEAK, duck=DUCK, voice_peak=VOICE_PEAK):
    """bed_peak: pico del fondo. Con voz queda en 0.65 (debajo de la voz); sin narrador se sube (p. ej. 0.9)."""
    n = int(total * SR)
    bed = norm(bed[:n], bed_peak)
    vox = np.zeros(n)
    for at, wav, _speaker in voices:
        data, _ = sf.read(wav)
        i = int(at * SR)
        data = data[: max(0, n - i)]
        vox[i:i + len(data)] += data
    if np.abs(vox).max() > 0:
        vox = norm(vox, voice_peak) * 0.95
        env = np.convolve(np.abs(vox), np.ones(int(0.05 * SR)) / int(0.05 * SR), mode="same")
        env = np.clip(env / (env.max() * 0.25), 0, 1)
        env = np.convolve(env, np.ones(int(0.25 * SR)) / int(0.25 * SR), mode="same")
        bed = bed * (1 - duck * env)[:, None]
    out = bed + vox[:, None]
    out = np.tanh(out * 1.15) / np.tanh(1.15)
    end = int(fade_out * SR)
    out[-end:] *= np.linspace(1, 0, end)[:, None]
    return out


def write_wav(path, data):
    """Guarda audio estéreo float [-1, 1] como WAV de 16 bits."""
    path.parent.mkdir(parents=True, exist_ok=True)
    sf.write(path, np.clip(data, -1, 1), SR, subtype="PCM_16")
