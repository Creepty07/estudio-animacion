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


def line_audio(text, speaker):
    style = config.VOICES[speaker or "NARRADOR"]
    raw = speak(config.SAY.get(text, text), style["voice"], style["speed"])
    return FX[style["fx"]](raw) * style["gain"]


def build():
    out_dir = config.AUDIO_DIR / "voces"
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for ep in config.EPISODES.values():
        for name in ep["scenes"]:
            mod = config.scene_module(name)
            lines = []
            for i, (start, end, text, speaker) in enumerate(mod.SUBS):
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
