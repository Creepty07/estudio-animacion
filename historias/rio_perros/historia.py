"""El río de los perros — leyenda de Día de Muertos SIN NARRADOR (vertical 9:16, ~70 s).

Todo lo que esté en MAYÚSCULAS se carga en motor.config al elegir esta historia.
La historia se cuenta con texto en pantalla (SUBS) y diseño de sonido: tambor, caracol, flauta, ladridos y agua.
Guion y fuentes: historias/rio_perros/GUION.md
"""

TITULO = "El río de los perros"
TIPO = "unico"
FORMATO = "vertical"

NARRATION = False       # sin narrador: no se generan voces; los SUBS salen como texto con sus tiempos locales
FONT = "DejaVu Serif"   # letra con serifa para los subtítulos: se siente a códice, no a red social

EPISODES = {
    "ep1": {
        "scenes": [
            "ep1.s01_gancho", "ep1.s02_titulo", "ep1.s03_rio", "ep1.s04_calle_dia", "ep1.s05_calle_noche",
            "ep1.s06_muerte", "ep1.s07_orilla", "ep1.s08_blanco_negro", "ep1.s09_otra_orilla",
            "ep1.s10_rojizo", "ep1.s11_cruce", "ep1.s12_ofrenda", "ep1.s13_tarjeta",
        ],
        "mix": "mix_ep1",
        "final": "el_rio_de_los_perros.mp4",
    },
}

# ---------- paleta: el inframundo es frío; lo cálido es lo que está vivo o es querido ----------
ACENTO = (1.0, 0.68, 0.20)             # ámbar: ojos de los perros y título
NOCHE_ALTO = (0.004, 0.012, 0.028)     # cielo del Mictlán, arriba
NOCHE_BAJO = (0.035, 0.095, 0.130)     # cielo del Mictlán, horizonte
LUNA = (0.80, 0.90, 0.95)
NIEBLA = (0.55, 0.70, 0.78)
RIO_OSCURO = (0.010, 0.030, 0.050)
RIO_CLARO = (0.050, 0.140, 0.190)
ORILLA = (0.020, 0.030, 0.040)
ROJIZO = (0.80, 0.32, 0.12)            # el perro bermejo: el único color cálido del inframundo
ROJIZO_CLARO = (1.0, 0.55, 0.25)
BLANCO = (0.93, 0.95, 0.97)
NEGRO = (0.035, 0.040, 0.055)
MANTA = (0.82, 0.78, 0.66)             # ropa de Don Celso
SOMBRERO = (0.58, 0.45, 0.27)
PIEL = (0.55, 0.38, 0.27)
ADOBE = (0.68, 0.46, 0.30)
LLAMA = (1.0, 0.72, 0.28)
CEMPASUCHIL = (1.0, 0.55, 0.04)
HILO = (0.96, 0.95, 0.90)              # hilo flojo de algodón al cuello del perro (Sahagún)


# ---------- look final por escena: (desat, frío, viñeta, grano, color_frío) ----------
_FRIO = (0.74, 0.90, 1.0)
_CALIDO = (1.0, 0.86, 0.66)
_LOOK = {
    "s01": (0.35, 0.40, 0.45, 0.10, _FRIO), "s02": (0.35, 0.40, 0.35, 0.10, _FRIO),
    "s03": (0.30, 0.42, 0.40, 0.10, _FRIO), "s04": (0.25, 0.50, 0.40, 0.09, _CALIDO),
    "s05": (0.38, 0.45, 0.40, 0.10, _FRIO), "s06": (0.28, 0.20, 0.50, 0.10, _CALIDO),
    "s07": (0.40, 0.50, 0.40, 0.11, _FRIO), "s08": (0.38, 0.50, 0.40, 0.11, _FRIO),
    "s09": (0.40, 0.50, 0.45, 0.11, _FRIO), "s10": (0.15, 0.30, 0.38, 0.10, _FRIO),
    "s11": (0.15, 0.40, 0.40, 0.10, _FRIO), "s12": (0.00, 0.28, 0.35, 0.07, _CALIDO),
    "s13": (0.12, 0.15, 0.25, 0.06, _FRIO),
}


def GRADE(ctx, t, name):
    from motor import grade
    d, f, v, g, c = _LOOK.get(name.split(".")[-1][:3], _LOOK["s03"])
    grade.final(ctx, t, desat=d, frio=f, color_frio=c, viñeta=v, grano=g)
