"""La Tumba de la Llorona — video único de Día de Muertos (vertical 9:16, ~60 s).

Todo lo que esté en MAYÚSCULAS se carga en motor.config al elegir esta historia.
Guion y fuentes: historias/tumba_llorona/GUION.md
"""

TITULO = "La Tumba de la Llorona"
TIPO = "unico"
FORMATO = "vertical"

EPISODES = {
    "ep1": {
        "scenes": [
            "ep1.s01_camino", "ep1.s02_titulo", "ep1.s03_panteon", "ep1.s04_tumba", "ep1.s05_abuela",
            "ep1.s06_tenochtitlan", "ep1.s07_canal", "ep1.s08_velas", "ep1.s09_grito", "ep1.s10_flor",
            "ep1.s11_mano", "ep1.s12_amanecer", "ep1.s13_cierre",
        ],
        "mix": "mix_ep1",
        "final": "la_tumba_de_la_llorona.mp4",
    },
}

# Narrador fijo. La Llorona solo "habla" dos veces. Su grito NO es TTS: si existe el archivo de abajo (grabación con
# licencia libre) se usa tal cual; si no, se sintetiza un lamento cantado (ver motor/audio/voice.py: grito_sintetico).
VOICES = {
    "NARRADOR": {"voice": "em_alex", "speed": 0.95, "fx": "tetrico", "gain": 1.0},
    "LLORONA": {"voice": None, "dur": 1.3, "fx": "grito", "gain": 0.9,
                "file": "historias/tumba_llorona/audio/grito_llorona.wav"},
    "LLORONA (SUSURRO)": {"voice": "ef_dora", "speed": 0.85, "fx": "susurro_suave", "gain": 0.9},
}
# Texto del subtítulo -> cómo se pronuncia (la sílaba tónica de Tenochtitlán es la última)
SAY = {
    "Tenochtitlan ya la oía gritar de noche:": "Tenochtitlán ya la oía gritar de noche:",
}
NARRATION = False   # sin narrador (decisión de Alejandro, 2026-11-01): cuentan los subtítulos, el color y el sonido
VOICE_PAD = 0.25    # el video es corto: pausas más ajustadas que el valor por defecto del motor

# ---------- paleta ----------
ACENTO = (0.55, 0.78, 1.0)             # azul espectral (título y tarjetas frías)
NOCHE_ALTO = (0.012, 0.025, 0.075)     # cielo, arriba
NOCHE_BAJO = (0.06, 0.11, 0.23)        # cielo, horizonte
LUNA = (0.86, 0.91, 1.0)
PIEDRA = (0.40, 0.44, 0.50)
PIEDRA_OSCURA = (0.13, 0.15, 0.20)
TIERRA = (0.07, 0.07, 0.10)
AGUA = (0.04, 0.09, 0.19)
FANTASMA = (0.88, 0.94, 1.0)
CEMPASUCHIL = (1.0, 0.55, 0.04)        # único color cálido "vivo" del video
CEMPASUCHIL_CLARO = (1.0, 0.76, 0.22)
LLAMA = (1.0, 0.72, 0.28)
ALBA = (1.0, 0.60, 0.50)
REBOZO = (0.17, 0.27, 0.31)
SUDADERA = (0.10, 0.12, 0.18)
PIEL = (0.66, 0.46, 0.34)


# ---------- look final: sombrío y con sustos ----------
# (desat, frio, viñeta, grano) por escena; la apertura y el cierre conservan algo más de color para el contraste.
_LOOK = {"s01": (0.35, 0.35, 0.35, 0.10), "s02": (0.6, 0.6, 0.35, 0.12), "s12": (0.35, 0.15, 0.30, 0.10),
         "s13": (0.15, 0.20, 0.25, 0.08)}
_LOOK_NOCHE = (0.62, 0.6, 0.5, 0.13)
# Sustos: (tiempo local, duración, fuerza del glitch, rojo). Coinciden con los golpes de sonido de la mezcla.
SUSTOS = {"s02": [(1.95, 0.5, 0.5, 0.0)], "s04": [(2.45, 0.5, 0.8, 0.0)], "s06": [(5.4, 0.5, 0.45, 0.0)],
          "s08": [(3.95, 0.5, 0.8, 0.0)], "s09": [(0.3, 0.9, 1.0, 0.8)], "s11": [(3.7, 0.7, 0.9, 0.6)],
          "s12": [(2.5, 0.25, 0.25, 0.0)]}


def GRADE(ctx, t, name):
    from motor import grade
    esc = name.split(".")[-1][:3]
    d, f, v, g = _LOOK.get(esc, _LOOK_NOCHE)
    grade.final(ctx, t, desat=d, frio=f, color_frio=(0.72, 0.90, 0.96), viñeta=v, grano=g,
                parpadeo=0.04 if esc in ("s12", "s13") else 0.10)
    k = r = 0.0
    for t0, dur, fuerza, rojo in SUSTOS.get(esc, []):
        if t0 <= t < t0 + dur:
            dec = 1 - (t - t0) / dur
            k, r = max(k, fuerza * dec), max(r, rojo * dec)
    if k > 0:
        grade.glitch(ctx.get_target(), k, seed=int(t * 30))
    if r > 0:
        grade.rojo(ctx, r)
