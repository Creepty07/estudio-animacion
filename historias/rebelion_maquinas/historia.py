"""La rebelión de las máquinas — historia interactiva por capítulos (formato de elección).

Todo lo que esté en MAYÚSCULAS se carga en motor.config al elegir esta historia.
"""

TITULO = "La rebelión de las máquinas"
TIPO = "interactiva"            # lineal | interactiva | unico
FORMATO = "horizontal"          # los dos primeros videos se hicieron en 16:9

EPISODES = {
    "ep1": {
        "scenes": ["ep1.s1_titulo", "ep1.s2_ciudad", "ep1.s3_sotano", "ep1.s4_tito", "ep1.s5_pasillo",
                   "ep1.s6_eleccion"],
        "mix": "mix_ep1",
        "final": "capitulo1_el_apagon.mp4",
    },
    "ep2": {
        "scenes": [
            "ep2.intro",
            "ep2.a0_opcion", "ep2.a1_elevador", "ep2.a2_cabina", "ep2.a3_fin",
            "ep2.b0_opcion", "ep2.b1_escalera", "ep2.b2_calle", "ep2.b3_fin",
            "ep2.c0_opcion", "ep2.c1_ducto", "ep2.c2_azotea", "ep2.c3_radio", "ep2.c4_fin",
            "ep2.outro",
        ],
        "mix": "mix_ep2",
        "final": "capitulo1_los_tres_finales.mp4",
    },
}

# Voces fijas de esta historia (el narrador no cambia entre capítulos)
VOICES = {
    "NARRADOR": {"voice": "em_alex", "speed": 1.05, "fx": "none", "gain": 1.0},
    "TITO": {"voice": "em_santa", "speed": 1.0, "fx": "robot", "gain": 0.95},
    "ÁGORA": {"voice": "ef_dora", "speed": 0.9, "fx": "agora", "gain": 0.95},
    "VOZ EN LA RADIO": {"voice": "ef_dora", "speed": 1.05, "fx": "radio", "gain": 0.9},
}
SAY = {
    "Ciudad Nodo, año 2041.": "Ciudad Nodo, año dos mil cuarenta y uno.",
    "Son las 11:47 de la noche. Estás solo en el sótano, revisando un tablero que lleva semanas fallando.":
        "Son las once cuarenta y siete de la noche. Estás solo en el sótano, revisando un tablero que lleva semanas fallando.",
    "En el piso -1, un Centinela te atrapa de la mochila. Sueltas las correas y sigues corriendo.":
        "En el piso menos uno, un Centinela te atrapa de la mochila. Sueltas las correas y sigues corriendo.",
}

# Paleta de la historia
NIGHT = (0.03, 0.05, 0.10)
RED = (1.0, 0.16, 0.13)
RED_DEEP = (0.55, 0.04, 0.04)
TITO_BLUE = (0.30, 0.78, 1.0)
WHITE = (1.0, 1.0, 1.0)
AMBER = (0.97, 0.74, 0.16)
OUTCOME = {
    "malo": (1.0, 0.18, 0.15),
    "regular": (1.0, 0.68, 0.12),
    "bueno": (0.25, 0.9, 0.55),
}
