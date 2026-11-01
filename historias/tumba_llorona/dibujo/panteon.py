"""El panteón junto al canal: capa estática (suelo, tumbas, árboles, agua) y capa de luces (velas, niebla)."""
import math
import random
from motor import config
from motor.config import LLAMA
from motor.primitives import glow, fill_poly, line, src, circle
from motor.layers import paint_layer
from motor.kit import fog
from historias.tumba_llorona.dibujo import cielo, paisaje, tumbas, flores, velas

BANCO_Y = 0.355                 # base de los ahuejotes (orilla lejana)
AGUA_Y = (0.355, 0.46)          # franja del canal
SUELO_Y = 0.46
LUNA_XY = (0.72, 0.13)
CERA = (0.66, 0.60, 0.50)         # cera de las velas de noche (más oscura que de día)
FILAS = [(0.51, 0.46, 12, 0.55), (0.60, 0.64, 9, 0.70), (0.705, 0.88, 7, 0.85), (0.85, 1.22, 5, 1.0)]  # y, escala, cantidad, brillo


def _generar():
    W, H = config.W, config.H
    r = random.Random(12)
    out = []
    for fila, (yf, s, n, br) in enumerate(FILAS):
        for i in range(n):
            x = (i + 0.5) / n * W + r.uniform(-0.25, 0.25) * W / n
            if abs(x - W / 2) < 95 * s:                       # pasillo central libre
                continue
            out.append(dict(fila=fila, x=x, y=yf * H + r.uniform(-6, 6), s=s * r.uniform(0.9, 1.1), br=br,
                            forma=r.choice(["cruz", "lapida", "cruz"]), velas=r.choice([0, 2, 3, 3, 4]),
                            flores=r.random() < 0.75, seed=r.randint(0, 999), especial=None))
    for fila, x, esp, forma, nvelas, flor in ((1, W * 0.66, "familia", "cruz", 4, True),
                                              (0, W * 0.20, "sin_nombre", "lapida", 0, False)):
        yf, s, _, br = FILAS[fila]
        out = [g for g in out if not (g["fila"] == fila and abs(g["x"] - x) < 120 * s)]
        out.append(dict(fila=fila, x=x, y=yf * H, s=s * 1.1, br=br, forma=forma, velas=nvelas, flores=flor,
                        seed=77 + fila, especial=esp))
    return out


TUMBAS = _generar()
FAMILIA = next(g for g in TUMBAS if g["especial"] == "familia")
SIN_NOMBRE = next(g for g in TUMBAS if g["especial"] == "sin_nombre")


def _flamas():
    """Posición de cada llama de las tumbas: (x, y, escala)."""
    out = []
    for g in TUMBAS:
        for j in range(g["velas"]):
            dx = (j - (g["velas"] - 1) / 2) * 34 * g["s"]
            out.append((g["x"] + dx, g["y"] + 8 * g["s"], 0.5 * g["s"], g["seed"] + j, g))
    return out


FLAMAS = _flamas()


def _linea_velas():
    """Fila de velas que baja por el pasillo central hasta el canal (se apagan en la escena 8)."""
    W, H = config.W, config.H
    out = []
    for i in range(10):
        u = i / 9
        y = H * (0.865 - 0.375 * u ** 0.9)
        s = 0.8 * (1 - 0.62 * u)
        out.append((W / 2 + (-1) ** i * (46 * s + 14), y, s))
    return out


LINEA = _linea_velas()


def _base(ctx):
    W, H = config.W, config.H
    paisaje.agua(ctx, H * AGUA_Y[0], H * AGUA_Y[1])
    for i in range(13):                                          # ahuejotes de la orilla lejana
        x = (i + 0.5) / 13 * W + random.Random(i).uniform(-30, 30)
        paisaje.ahuejote(ctx, x, H * BANCO_Y + 10, 0.32 + 0.2 * random.Random(40 + i).random(), seed=i)
    ctx.rectangle(0, H * BANCO_Y, W, 14)                         # banco lejano
    src(ctx, (0.012, 0.025, 0.045))
    ctx.fill()
    for i in range(7):
        paisaje.tules(ctx, (i + 0.5) / 7 * W, H * BANCO_Y + 6, 0.6, seed=i)
    cielo.gradiente_vertical(ctx, [(0, (0.05, 0.07, 0.11)), (1, (0.015, 0.02, 0.035))], H * SUELO_Y, H)
    for i in range(9):                                           # tules de la orilla cercana
        paisaje.tules(ctx, (i + 0.5) / 9 * W + 20, H * SUELO_Y + 4, 0.9, seed=30 + i, n=6)
    for g in sorted(TUMBAS, key=lambda g: g["y"]):
        s, br = g["s"], g["br"]
        if g["especial"] == "sin_nombre":
            tumbas.lapida(ctx, g["x"], g["y"] - 24 * s, s * 1.15, br * 0.75)
            fill_poly(ctx, [(g["x"] - 66 * s, g["y"] - 24 * s), (g["x"] + 66 * s, g["y"] - 24 * s),
                            (g["x"] + 50 * s, g["y"] - 44 * s), (g["x"] - 50 * s, g["y"] - 44 * s)], (0.10, 0.13, 0.19))
            ctx.rectangle(g["x"] - 66 * s, g["y"] - 24 * s, 132 * s, 24 * s)
            src(ctx, (0.07, 0.09, 0.14))
            ctx.fill()
            tumbas.maleza(ctx, g["x"], g["y"] + 4 * s, s, seed=3)
            continue
        tumbas.tumba(ctx, g["x"], g["y"], s, g["forma"], br)
        if g["flores"]:
            for k, dx in enumerate((-34, 0, 34)):
                flores.cempasuchil(ctx, g["x"] + dx * s, g["y"] - 38 * s, 17 * s, seed=g["seed"] + k, brillo=0.55 + 0.45 * br)
        for j in range(g["velas"]):
            dx = (j - (g["velas"] - 1) / 2) * 34 * s
            velas.cuerpo(ctx, g["x"] + dx, g["y"] + 8 * s, 0.5 * s, CERA)
    for (x, y, s) in LINEA:
        velas.cuerpo(ctx, x, y, s, CERA)


def fondo(ctx, t):
    """Cielo, panteón y canal con el reflejo de la luna (todo lo que va detrás de los personajes)."""
    W, H = config.W, config.H
    cielo.noche(ctx, t, horizonte=BANCO_Y + 0.05, luna_xy=LUNA_XY, r_luna=60)
    paint_layer(ctx, "panteon_base", _base)
    paisaje.reflejo_luna(ctx, t, W * LUNA_XY[0], H * AGUA_Y[0] + 4, H * AGUA_Y[1] - 2)


def luces(ctx, t, linea=None, tumbas_on=1.0, niebla=1.0):
    """Llamas, charcos de luz y niebla. linea = {índice: intensidad} de la fila de velas del pasillo."""
    W, H = config.W, config.H
    for (x, y, s, seed, g) in FLAMAS:
        velas.llama(ctx, x, y, s, t, seed=seed, intensidad=tumbas_on, luz=120, fuerza=0.38)
    for g in TUMBAS:
        if g["velas"]:
            glow(ctx, g["x"], g["y"] + 6 * g["s"], 150 * g["s"], LLAMA, 0.10 * tumbas_on)
    for i, (x, y, s) in enumerate(LINEA):
        inten = 1.0 if linea is None else linea.get(i, 1.0)
        velas.llama(ctx, x, y, s, t, seed=200 + i, intensidad=inten, luz=150, fuerza=0.42)
        glow(ctx, x, y + 6 * s, 150 * s, LLAMA, 0.10 * inten)
    fog(ctx, t, (0.55, 0.65, 0.85), 0.13 * niebla, H * 0.36, H * 0.5, seed=5, speed=12)
    fog(ctx, t, (0.5, 0.6, 0.8), 0.10 * niebla, H * 0.8, H * 1.0, seed=9, speed=16)
