"""Texto a voz con Kokoro (modelo neuronal local, ONNX). Resultado en caché por texto+voz+velocidad."""
import hashlib
import numpy as np
import soundfile as sf
from motor import config
from motor.config import SR

_engine = None


def _kokoro():
    global _engine
    if _engine is None:
        from kokoro_onnx import Kokoro
        _engine = Kokoro(str(config.TTS_MODEL), str(config.TTS_VOICES))
    return _engine


def speak(text, voice, speed=1.0):
    """Devuelve la voz como arreglo mono a 48 kHz, sin silencios en los extremos."""
    key = hashlib.sha1(f"{voice}|{speed}|{text}".encode()).hexdigest()[:16]
    config.TTS_CACHE.mkdir(parents=True, exist_ok=True)
    path = config.TTS_CACHE / f"{key}.wav"
    if path.exists():
        data, _ = sf.read(path)
        return data
    import librosa
    samples, sr = _kokoro().create(text, voice=voice, speed=speed, lang="es")
    data = librosa.resample(np.asarray(samples, dtype=float), orig_sr=sr, target_sr=SR)
    idx = np.where(np.abs(data) > 0.01)[0]
    if len(idx):
        data = data[max(0, idx[0] - int(0.02 * SR)): idx[-1] + int(0.08 * SR)]
    sf.write(path, data, SR)
    return data
