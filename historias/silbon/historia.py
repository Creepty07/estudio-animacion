"""Las reglas del Silbón — video único tipo "reglas", vertical 9:16, ≈90 s.

Narrador fijo: ElevenLabs (voz DdKbXdRlBmj7Ty7N0FVr, eleven_v4), una toma por línea en audio/narrador/ (ver narracion.py).
Los diálogos de personajes salen solo como subtítulo con etiqueta ("mudo"). Subtítulos estilo "reglas": palabra a palabra,
con la palabra clave en amarillo. Todo lo que esté en MAYÚSCULAS se carga en motor.config al elegir esta historia.
"""

TITULO = "Las reglas del Silbón"
TIPO = "unico"
FORMATO = "vertical"

EPISODES = {
    "ep1": {
        "scenes": ["ep1.s01_gancho", "ep1.s02_llegas", "ep1.s03_letrero", "ep1.s04_regla1", "ep1.s05_regla2",
                   "ep1.s06_regla3", "ep1.s07_regla4", "ep1.s08_tiempo", "ep1.s09_silencio", "ep1.s10_puerta",
                   "ep1.s11_tu", "ep1.s12_cierre"],
        "mix": "mix_ep1",
        "final": "las_reglas_del_silbon.mp4",
    },
}

NARRATION = True
VOICES = {
    "NARRADOR": {"mapa": "historias/silbon/audio/narrador", "fx": "tetrico", "gain": 1.0},
    "Llanero": {"mudo": True}, "Ramiro": {"mudo": True},
}
SAY = {}
VOICE_PAD = 0.25
MAX_STRETCH = 2.0
ESTIRAR_RAPIDO = True
SUBTITLE_STYLE = "reglas"

ACENTO = (1.0, 0.82, 0.16)

# Sustos: (tiempo local, duración, fuerza del glitch, rojo). Coinciden con los golpes de sonido de la mezcla.
SUSTOS = {
    "ep1.s01": [(3.0, 0.6, 1.0, 0.0)],      # el ojo en la rendija
    "ep1.s04": [(7.4, 0.7, 0.9, 0.3)],      # el Silbón gigante en la ventana
    "ep1.s09": [(7.1, 0.6, 0.5, 0.0)],      # "lejísimos"
    "ep1.s10": [(3.5, 0.5, 0.7, 0.4)],      # el saco cae
    "ep1.s11": [(3.3, 0.6, 1.0, 0.7)],      # el ojo vuelve
    "ep1.s12": [(7.2, 0.6, 0.8, 0.5)],      # apagón final
}


def GRADE(ctx, t, name):
    from motor import grade
    clave = name.split("_")[0]
    grade.final(ctx, t, desat=0.14, frio=0.25, viñeta=0.30, grano=0.05, parpadeo=0.03)
    k = r = 0.0
    for t0, dur, fuerza, rojo in SUSTOS.get(clave, []):
        if t0 <= t < t0 + dur:
            dec = 1 - (t - t0) / dur
            k, r = max(k, fuerza * dec), max(r, rojo * dec)
    if k > 0:
        grade.glitch(ctx.get_target(), k, seed=int(t * 30))
    if r > 0:
        grade.rojo(ctx, r)
