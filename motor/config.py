"""Configuración central del motor.

Valores por defecto para todas las historias + carga de la historia activa.
La historia se elige con la variable de entorno HISTORIA (producir.py la pone sola).
Todo lo que la historia defina en MAYÚSCULAS en su historia.py sobrescribe o se agrega aquí,
así cualquier módulo puede hacer `from motor.config import W, H, ROJO, ...`.
"""
import importlib
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------- video ----------
FORMATS = {"horizontal": (1920, 1080), "vertical": (1080, 1920)}
FORMATO = "vertical"            # TikTok por defecto; cada historia puede cambiarlo
W, H = FORMATS[FORMATO]
FPS = 30
X264 = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p"]
WORKERS = 2                     # escenas que se renderizan en paralelo

# ---------- texto ----------
FONT = "Inter"
FONT_DISPLAY = "Inter Display Black"
FONT_MONO = "DejaVu Sans Mono"
SUBTITLES = True

# ---------- audio y voz ----------
SR = 48000
NARRATION = True
TTS_MODEL = ROOT / "models" / "kokoro-v1.0.onnx"
TTS_VOICES = ROOT / "models" / "voices-v1.0.bin"
TTS_CACHE = ROOT / "out" / "_tts_cache"
# Voces Kokoro en español: em_alex y em_santa (hombre), ef_dora (mujer).
# fx: none | robot | agora (eco serena) | radio. Cada historia fija su NARRADOR y sus personajes.
VOICES = {
    "NARRADOR": {"voice": "em_alex", "speed": 1.05, "fx": "none", "gain": 1.0},
}
SAY = {}                        # texto del subtítulo -> cómo se pronuncia
VOICE_PAD = 0.35                # silencio mínimo después de cada línea
MAX_STRETCH = 2.2               # lo más que se alarga un tramo de escena para que quepa su línea

# ---------- historia activa ----------
STORY = None
EPISODES = {}
OUT = SCENES_DIR = STILLS_DIR = AUDIO_DIR = VOICE_MANIFEST = None


def load(slug):
    """Carga historias/<slug>/historia.py y recalcula rutas y formato."""
    global STORY, W, H, OUT, SCENES_DIR, STILLS_DIR, AUDIO_DIR, VOICE_MANIFEST
    mod = importlib.import_module(f"historias.{slug}.historia")
    g = globals()
    for name, value in vars(mod).items():
        if name.isupper():
            if name == "VOICES":
                g["VOICES"] = {**g["VOICES"], **value}
            else:
                g[name] = value
    STORY = slug
    W, H = FORMATS[g["FORMATO"]]
    OUT = ROOT / "out" / slug
    SCENES_DIR = OUT / "escenas"
    STILLS_DIR = OUT / "cuadros"
    AUDIO_DIR = OUT / "audio"
    VOICE_MANIFEST = AUDIO_DIR / "voces.json"


def scene_module(name):
    """Módulo de una escena: 'ep1.s1_titulo' -> historias.<slug>.escenas.ep1.s1_titulo."""
    return importlib.import_module(f"historias.{STORY}.escenas.{name}")


def episode(ep):
    return EPISODES[ep]


def audio_path(ep):
    return AUDIO_DIR / f"banda_{ep}.wav"


def final_path(ep):
    return OUT / EPISODES[ep]["final"]


if os.environ.get("HISTORIA"):
    load(os.environ["HISTORIA"])
