"""Fachada de un hospital sin nombre, de noche, con una sola ventana encendida (la del cuarto de Rafa)."""
import math
import random
import cairo
from motor.primitives import src, line, circle, glow, fill_rrect, fill_poly, mix
from historias.planchada.dibujo.paleta import degradado_v, ovalo, FLUO

VENTANA_LUZ = (706, 812, 56, 78)        # x, y, w, h de la ventana encendida (el zoom de la escena apunta aquí)


def fachada(ctx, t):
    degradado_v(ctx, 0, 0, 1080, 1920, (0.005, 0.02, 0.04), (0.04, 0.10, 0.13))
    r = random.Random(5)
    for _ in range(60):
        circle(ctx, r.uniform(0, 1080), r.uniform(0, 640), r.uniform(0.8, 2.0), (0.85, 0.93, 1.0), 0.35 + 0.35 * math.sin(t * 2 + r.uniform(0, 6)) ** 2)
    # edificio
    cuerpo = (90, 460, 900, 800)
    fill_rrect(ctx, 90, 470, 900, 790, 6, (0.045, 0.085, 0.10))
    fill_rrect(ctx, 60, 440, 960, 40, 4, (0.03, 0.06, 0.075))                              # cornisa
    fill_rrect(ctx, 420, 360, 240, 90, 4, (0.04, 0.075, 0.09))                             # torre central
    # ventanas
    for fila in range(4):
        for col in range(10):
            x = 118 + col * 88
            y = 520 + fila * 150
            if col in (4, 5) and fila == 3:
                continue
            fill_rrect(ctx, x, y, 56, 78, 3, (0.015, 0.03, 0.04))
            fill_rrect(ctx, x, y, 56, 78, 3, (0.15, 0.32, 0.36), 0.12)
            line(ctx, x + 28, y, x + 28, y + 78, 2, (0.03, 0.06, 0.07), 0.9)
    # la ventana encendida (parpadea apenas)
    vx, vy, vw, vh = VENTANA_LUZ
    pulso = 0.9 + 0.1 * math.sin(t * 7) * math.sin(t * 3.1)
    fill_rrect(ctx, vx, vy, vw, vh, 3, mix((0.5, 0.9, 0.95), (0.85, 1.0, 1.0), pulso))
    line(ctx, vx + vw / 2, vy, vx + vw / 2, vy + vh, 2.5, (0.03, 0.06, 0.07), 0.9)
    line(ctx, vx, vy + vh * 0.52, vx + vw, vy + vh * 0.52, 2.5, (0.03, 0.06, 0.07), 0.9)
    ovalo(ctx, vx + vw * 0.28, vy + vh * 0.72, 12, 20, (0.1, 0.2, 0.22), 0.5)             # cortina contra la luz
    glow(ctx, vx + vw / 2, vy + vh / 2, 340, FLUO, 0.45 * pulso)
    # entrada con marquesina y cruz
    fill_rrect(ctx, 400, 1090, 280, 20, 4, (0.03, 0.06, 0.075))
    fill_rrect(ctx, 424, 1110, 232, 150, 4, (0.02, 0.04, 0.05))
    fill_rrect(ctx, 440, 1120, 200, 140, 3, (0.12, 0.26, 0.30), 0.55)
    glow(ctx, 540, 1190, 220, FLUO, 0.14)
    fill_rrect(ctx, 520, 1028, 40, 12, 2, (0.4, 0.7, 0.75), 0.7)                          # cruz (sin letrero ni nombre)
    fill_rrect(ctx, 534, 1014, 12, 40, 2, (0.4, 0.7, 0.75), 0.7)
    # suelo, banqueta, farol y árboles
    degradado_v(ctx, 0, 1260, 1080, 660, (0.03, 0.06, 0.07), (0.01, 0.03, 0.04))
    ovalo(ctx, 540, 1330, 360, 36, FLUO, 0.07)
    for fx, fh in ((60, 330), (990, 380)):
        line(ctx, fx, 1270, fx, 1270 - fh, 16, (0.01, 0.025, 0.03))
        ovalo(ctx, fx, 1270 - fh - 60, 120, 110, (0.01, 0.025, 0.03))
        ovalo(ctx, fx + 40, 1270 - fh - 20, 90, 80, (0.01, 0.025, 0.03))
    line(ctx, 250, 1270, 250, 960, 8, (0.02, 0.04, 0.05))                                  # farol
    glow(ctx, 250, 950, 220, (0.7, 0.95, 1.0), 0.35 + 0.05 * math.sin(t * 11))
    circle(ctx, 250, 952, 10, (0.9, 1.0, 1.0))
