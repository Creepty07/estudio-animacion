"""La Planchada — interactiva (vertical 9:16). ep1 "La enfermera de las 3:00" (~60 s) y ep2 "Los tres finales" (~91 s).

Todo lo que esté en MAYÚSCULAS se carga en motor.config al elegir esta historia.
Guion y fuentes: historias/planchada/GUION.md (copia de docs/estudio/guion_planchada.md) y docs/estudio/investigacion_planchada.md
"""

TITULO = "La Planchada"
TIPO = "interactiva"
FORMATO = "vertical"

EPISODES = {
    "ep1": {
        "scenes": [
            "ep1.s01_gancho", "ep1.s02_titulo", "ep1.s03_hospital", "ep1.s04_cuarto", "ep1.s05_ventana",
            "ep1.s06_entra", "ep1.s07_frio", "ep1.s08_pastilla", "ep1.s09_reflejo", "ep1.s10_eleccion",
        ],
        "mix": "mix_ep1",
        "final": "la_planchada_ep1.mp4",
    },
    "ep2": {
        "scenes": [
            "ep2.s01_gancho", "ep2.s02_f1_titulo", "ep2.s03_f1_ojos", "ep2.s04_f1_fiebre", "ep2.s05_f1_amanecer",
            "ep2.s06_f2_titulo", "ep2.s07_f2_timbre", "ep2.s08_f2_turno", "ep2.s09_f2_pasillo",
            "ep2.s10_f3_titulo", "ep2.s11_f3_nombre", "ep2.s12_f3_pastilla", "ep2.s13_f3_amanecer", "ep2.s14_f3_nota",
            "ep2.s15_f3_leyenda", "ep2.s16_cierre",
        ],
        "mix": "mix_ep2",
        "final": "la_planchada_ep2.mp4",
    },
}

# Sin narrador (regla de la casa): cuentan el texto, el color y el sonido. Los diálogos salen como subtítulos con etiqueta.
NARRATION = False
VOICES = {}
SAY = {}

# ---------- paleta ----------
ACENTO = (0.55, 0.96, 1.0)             # cian de fluorescente (títulos y tarjetas)
ROJO_TIMBRE = (0.95, 0.10, 0.12)       # rojo solo en el timbre y los sustos
AMBAR = (1.0, 0.72, 0.38)              # amanecer del final bueno

# ---------- look final: frío, desaturado, con grano; el amanecer entra con color ----------
# (desat, frío, viñeta, grano, color_frío) por escena. La clave es "epN.sNN".
_NOCHE = (0.50, 0.42, 0.45, 0.12, (0.78, 0.95, 1.0))
_LOOK = {
    "ep1.s02": (0.60, 0.50, 0.35, 0.12, (0.74, 0.95, 1.0)),
    "ep1.s10": (0.45, 0.40, 0.40, 0.11, (0.80, 0.95, 1.0)),
    "ep2.s02": (0.60, 0.50, 0.35, 0.12, (0.74, 0.95, 1.0)),
    "ep2.s05": (0.65, 0.30, 0.55, 0.14, (0.86, 0.92, 0.98)),          # luz gris de madrugada
    "ep2.s10": (0.30, 0.15, 0.35, 0.10, (0.90, 0.97, 1.0)),
    "ep2.s13": (0.10, 0.05, 0.28, 0.08, (1.0, 0.93, 0.85)),            # amanecer ámbar
    "ep2.s14": (0.28, 0.10, 0.30, 0.09, (1.0, 0.95, 0.88)),
    "ep2.s16": (0.40, 0.35, 0.40, 0.10, (0.80, 0.95, 1.0)),
}
# Sustos: (tiempo local, duración, fuerza del glitch, rojo). Coinciden con los golpes de sonido de las mezclas.
SUSTOS = {
    "ep1.s01": [(0.2, 0.6, 1.0, 0.0)],
    "ep1.s05": [(1.6, 0.7, 1.0, 0.8)],
    "ep1.s09": [(2.2, 0.7, 1.0, 0.55)],
    "ep2.s01": [(0.2, 0.6, 1.0, 0.0)],
    "ep2.s14": [(3.2, 0.7, 0.45, 0.0)],
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
