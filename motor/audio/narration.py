"""Genera todas las líneas habladas (narración y diálogos) a partir de los SUBS de cada escena.

Escribe out/audio/voces.json con, por escena: inicio local, texto, hablante, archivo y duración.
Se ejecuta desde producir.py.
"""
import json
import soundfile as sf
from motor import config
from motor.config import SR
from motor.audio.tts import speak
from motor.audio.voice import FX


def _desde_archivo(path):
    """Línea real grabada (WAV/MP3/OGG con licencia libre): mono, a 48 kHz y sin silencios en los extremos."""
    import librosa
    import numpy as np
    from motor.config import SR
    data, _ = librosa.load(str(path), sr=SR, mono=True)
    idx = np.where(np.abs(data) > 0.01)[0]
    if len(idx):
        data = data[max(0, idx[0] - int(0.02 * SR)): idx[-1] + int(0.08 * SR)]
    return data / max(np.abs(data).max(), 1e-6) * 0.85


def line_audio(text, speaker):
    """Voz de una línea. Si el personaje trae 'file' y existe, usa esa grabación; si no, 'voice' (Kokoro) o,
    con voice=None, el sonido sintetizado de FX[fx] con la duración 'dur' (cada texto cambia la semilla)."""
    import numpy as np
    from motor.config import SR
    style = config.VOICES[speaker or "NARRADOR"]
    if style.get("mapa"):                                       # tomas pregrabadas (p. ej. ElevenLabs): texto del subtítulo -> archivo
        import json
        carpeta = config.ROOT / style["mapa"]
        toma = json.loads((carpeta / "lineas.json").read_text())[text]
        return FX[style["fx"]](_desde_archivo(carpeta / toma["archivo"])) * style["gain"]
    f = style.get("file")
    if f and (config.ROOT / f).exists():
        return _desde_archivo(config.ROOT / f) * style["gain"]
    if style.get("voice") is None:
        raw = np.zeros(int(style["dur"] * SR))
        return FX[style["fx"]](raw) * style["gain"] if style["fx"] != "grito" else FX["grito"](raw, seed=len(text)) * style["gain"]
    raw = speak(config.SAY.get(text, text), style["voice"], style["speed"])
    return FX[style["fx"]](raw) * style["gain"]


def build():
    """Genera las voces. Con NARRATION = False (historias sin narrador) no hace nada: los SUBS salen como texto
    en pantalla con sus tiempos locales y la banda sonora lleva todo el peso."""
    if not config.NARRATION:                         # video sin voces: solo subtítulos y sonido
        return {}
    out_dir = config.AUDIO_DIR / "voces"
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for ep in config.EPISODES.values():
        for name in ep["scenes"]:
            mod = config.scene_module(name)
            lines = []
            for i, (start, end, text, speaker) in enumerate(mod.SUBS):
                if config.VOICES[speaker or "NARRADOR"].get("mudo"):    # diálogo que solo se lee: sin voz y sin alargar la escena
                    lines.append({"start": start, "text": text, "speaker": speaker, "wav": None,
                                  "dur": round(end - start, 3), "mudo": True})
                    continue
                audio = line_audio(text, speaker)
                path = out_dir / f"{name}_{i}.wav"
                sf.write(path, audio, SR)
                lines.append({"start": start, "text": text, "speaker": speaker,
                              "wav": str(path), "dur": round(len(audio) / SR, 3)})
            manifest[name] = lines
    config.VOICE_MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=1))
    return manifest


if __name__ == "__main__":
    m = build()
    for name, lines in m.items():
        for ln in lines:
            print(f"{name:18s} {ln['start']:5.1f}s  {ln['dur']:4.1f}s  {ln['speaker'] or 'NARRADOR':16s} {ln['text'][:50]}")
