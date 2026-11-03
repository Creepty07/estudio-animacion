"""Ruta 0 — "El camión sin número" (título provisional, ver GUION.md) · serie lineal de 3 partes, vertical 9:16.

Versión B del guion: CON narrador (voz de ElevenLabs filtrada como si saliera de una radio vieja). Los diálogos de los personajes
siguen como subtítulo con etiqueta, sin voz. Parte 1 ≈ 70 s, parte 2 ≈ 66 s, parte 3 ≈ 83 s (la voz real puede alargar las escenas).
Todo lo que esté en MAYÚSCULAS se carga en motor.config al elegir esta historia.
"""

TITULO = "El camión sin número"          # PROVISIONAL: Alejandro aún no confirma el título (ver GUION.md)
TIPO = "lineal"
FORMATO = "vertical"

EPISODES = {
    "ep1": {
        "scenes": ["ep1.s01_gancho", "ep1.s02_titulo", "ep1.s03_parada", "ep1.s04_llega", "ep1.s05_dentro", "ep1.s06_quietos",
                   "ep1.s07_paradas", "ep1.s08_pasajera", "ep1.s09_cierre"],
        "mix": "mix_ep1",
        "final": "ruta0_parte1.mp4",
    },
    "ep2": {
        "scenes": ["ep2.s01_gancho", "ep2.s02_titulo", "ep2.s03_repaso", "ep2.s04_curva", "ep2.s05_puente", "ep2.s06_ruta",
                   "ep2.s07_pasajera", "ep2.s08_boleto", "ep2.s09_cierre"],
        "mix": "mix_ep2",
        "final": "ruta0_parte2.mp4",
    },
    "ep3": {
        "scenes": ["ep3.s01_gancho", "ep3.s02_titulo", "ep3.s03_repaso", "ep3.s04_giro", "ep3.s05_timbre", "ep3.s06_bajar",
                   "ep3.s07_despierta", "ep3.s08_no", "ep3.s09_o_no", "ep3.s10_cierre"],
        "mix": "mix_ep3",
        "final": "ruta0_parte3.mp4",
    },
}

# Un narrador fijo en las tres partes: tomas pregrabadas de ElevenLabs (voz DdKbXdRlBmj7Ty7N0FVr, modelo eleven_v4) en
# audio/narrador/, una por línea (mapa texto -> archivo en lineas.json), con el efecto de radio vieja `radio_tetrico`.
# Los personajes no hablan con voz: sus líneas salen como subtítulo con etiqueta ("mudo": ni voz ni alargar la escena).
NARRATION = True
VOICES = {
    "NARRADOR": {"mapa": "historias/ruta0/audio/narrador", "fx": "radio_tetrico", "gain": 1.0},
    "Iván": {"mudo": True}, "Pasajera": {"mudo": True}, "Chofer": {"mudo": True}, "Beto": {"mudo": True},
}
SAY = {}
VOICE_PAD = 0.3
ESTIRAR_RAPIDO = True      # los fondos se estiran por remuestreo (librosa tardaba ~15 min por mezcla); el tono de lluvia/motor baja un poco
MAX_STRETCH = 1.6

# Fechas del boleto y del celular. PROVISIONALES: Redes las fija según el día de publicación de la parte 2 (mañana = hoy + 1).
FECHA_HOY = "3 NOV"
FECHA_MANANA = "4 NOV"

# ---------- paleta ----------
PIEL = (0.66, 0.46, 0.34)                # colores que usa Tomás (tumba_llorona/dibujo/personas.py), reutilizado para Iván de pie
SUDADERA = (0.20, 0.30, 0.46)
REBOZO = (0.17, 0.27, 0.31)
LLAMA = (1.0, 0.72, 0.28)
ACENTO = (1.0, 0.62, 0.12)               # el "0" ámbar: único color cálido
AMBAR = (1.0, 0.62, 0.12)
ROJO_TIMBRE = (0.95, 0.10, 0.12)

# ---------- look final: frío, desaturado, grano; el interior conserva su amarillo enfermo ----------
_NOCHE = (0.50, 0.40, 0.46, 0.12, (0.80, 0.93, 1.0))
_LOOK = {
    "ep1.s02": (0.55, 0.45, 0.35, 0.12, (0.78, 0.92, 1.0)), "ep2.s02": (0.55, 0.45, 0.35, 0.12, (0.78, 0.92, 1.0)),
    "ep3.s02": (0.55, 0.45, 0.35, 0.12, (0.78, 0.92, 1.0)),
    "ep1.s05": (0.32, 0.18, 0.40, 0.11, (0.95, 0.97, 1.0)), "ep1.s06": (0.34, 0.2, 0.42, 0.11, (0.95, 0.97, 1.0)),
    "ep1.s07": (0.34, 0.2, 0.42, 0.11, (0.95, 0.97, 1.0)), "ep2.s06": (0.30, 0.15, 0.40, 0.11, (0.97, 0.98, 1.0)),
    "ep3.s07": (0.45, 0.35, 0.36, 0.10, (0.88, 0.96, 1.0)),
}
# Sustos: (tiempo local, duración, fuerza del glitch, rojo). Coinciden con los golpes de sonido de las mezclas.
SUSTOS = {
    "ep1.s01": [(0.1, 0.6, 1.0, 0.0)], "ep1.s06": [(7.7, 0.7, 0.4, 0.0)], "ep1.s08": [(6.3, 0.8, 1.0, 0.8)],
    "ep2.s01": [(0.1, 0.6, 1.0, 0.0)], "ep2.s04": [(7.9, 0.6, 0.8, 0.0)], "ep2.s06": [(5.7, 0.8, 1.0, 0.6)],
    "ep2.s08": [(3.0, 0.8, 1.0, 0.5)],
    "ep3.s01": [(0.1, 0.6, 1.0, 0.0)], "ep3.s09": [(9.1, 0.9, 1.0, 0.7)],
}


def GRADE(ctx, t, name):
    from motor import grade
    clave = name.split("_")[0]
    d, f, v, g, cf = _LOOK.get(clave, _NOCHE)
    grade.final(ctx, t, desat=d, frio=f, color_frio=cf, viñeta=v, grano=g, parpadeo=0.05)
    k = r = 0.0
    for t0, dur, fuerza, rojo in SUSTOS.get(clave, []):
        if t0 <= t < t0 + dur:
            dec = 1 - (t - t0) / dur
            k, r = max(k, fuerza * dec), max(r, rojo * dec)
    if k > 0:
        grade.glitch(ctx.get_target(), k, seed=int(t * 30))
    if r > 0:
        grade.rojo(ctx, r)
