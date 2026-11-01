"""Plantilla de historia. Copia con: python producir.py --nueva <nombre> [--formato vertical|horizontal]

TIPO:  lineal (capítulos en orden) | interactiva (capítulos con elección) | unico (un solo video)
Todo lo que esté en MAYÚSCULAS se carga en motor.config al elegir esta historia.
"""

TITULO = "Título de la historia"
TIPO = "unico"
FORMATO = "vertical"

EPISODES = {
    "ep1": {
        "scenes": ["ep1.s1_ejemplo"],
        "mix": "mix_ep1",
        "final": "video_ep1.mp4",
    },
}

# El narrador se fija una vez por historia y no cambia entre capítulos.
# Voces Kokoro en español: em_alex, em_santa (hombre) · ef_dora (mujer). fx: none | robot | agora | radio
VOICES = {
    "NARRADOR": {"voice": "em_alex", "speed": 1.05, "fx": "none", "gain": 1.0},
}
SAY = {}

ACENTO = (1.0, 0.55, 0.15)
