"""Paleta y medidas del estilo "Reglas": cabezas redondas, ojos enormes, contorno grueso, noche azul con luz ámbar.

Todo lo que se repite en los dibujos (colores, grosor del contorno, tamaños de la cabeza) vive aquí; los demás módulos
solo lo importan. Los números de tamaño son "a escala 1": cada función los multiplica por su escala `s`.
"""
# ---------- contorno y proporciones ----------
CONTORNO = (0.05, 0.05, 0.09)
GROSOR = 7.0                 # grosor del contorno a escala 1
RADIO_CABEZA = 105.0         # la cabeza se dibuja en el origen; el cuerpo cuelga hacia abajo

# ---------- cielo y luz ----------
NOCHE_ARRIBA = (0.02, 0.035, 0.11)
NOCHE_MEDIO = (0.07, 0.09, 0.24)
NOCHE_HORIZONTE = (0.22, 0.20, 0.42)
LUNA = (0.94, 0.96, 1.0)
LLAMA = (1.0, 0.72, 0.28)               # farol, vela: la luz cálida de adentro
LUZ_FRIA = (0.55, 0.70, 1.0)

# ---------- texto y HUD ----------
AMARILLO = (1.0, 0.82, 0.16)
ROJO = (0.90, 0.12, 0.15)
AZUL = (0.20, 0.45, 0.90)
BLANCO = (1.0, 1.0, 1.0)

# ---------- materiales ----------
MADERA = (0.36, 0.22, 0.13)
MADERA_OSCURA = (0.20, 0.12, 0.08)
MADERA_CLARA = (0.55, 0.37, 0.22)
PARED = (0.46, 0.36, 0.28)
PAJA = (0.45, 0.36, 0.18)
HUESO = (0.93, 0.90, 0.80)
VIDRIO = (0.28, 0.5, 0.36)

# ---------- personajes ----------
PIEL_TU = (0.70, 0.76, 0.80)            # gris azulado, como en el video de referencia
PIEL_LLANERO = (0.78, 0.60, 0.44)
PIEL_RAMIRO = (0.74, 0.64, 0.52)
PIEL_ABUELA = (0.76, 0.70, 0.68)
PIEL_NINA = (0.80, 0.66, 0.54)
