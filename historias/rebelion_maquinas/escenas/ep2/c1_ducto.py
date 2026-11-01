"""Final bueno 1/3 — Dani gatea por el ducto mientras los Centinelas escanean abajo."""
import math
from motor.config import W
from motor.primitives import seg, smooth, lerp, darken, tint, vignette, fill_screen, TAU
from historias.rebelion_maquinas.dibujo.environments import draw_basement, beacon
from historias.rebelion_maquinas.dibujo.env_ducto import duct, scan_beam, DUCT_FLOOR, DUCT_Y0
from historias.rebelion_maquinas.dibujo.characters import sentinel
from historias.rebelion_maquinas.dibujo.dani_poses import dani_pose

DURATION = 8.0
SUBS = [
    (0.3, 3.4, "Te arrastras por el ducto, sin hacer ruido.", None),
    (3.6, 7.7, "Abajo, los Centinelas barren cada rincón con haces rojos… pero sus cuerpos no caben en el conducto.", None),
]
FREEZE = (4.4, 5.8)
GRILLE = (7.1, 7.5)
SENTINELS = [(520, 0.0), (1260, 1.9)]  # x, fase
VISOR_Y = 895 - 500 * 0.8


def dani_x(t):
    if t < FREEZE[0]:
        return lerp(80, 1000, seg(t, 0.2, FREEZE[0]))
    if t < FREEZE[1]:
        return 1000
    return lerp(1000, 2050, seg(t, FREEZE[1], DURATION))


def crawl_phase(t):
    if t < FREEZE[0]:
        return t * TAU * 1.3
    if t < FREEZE[1]:
        return FREEZE[0] * TAU * 1.3
    return (FREEZE[0] + t - FREEZE[1]) * TAU * 1.3


def beam_angle(i, t):
    base = -math.pi / 2 + math.sin(t * 0.9 + i * 2.1) * 1.15
    if i == 1:
        # durante la pausa, el haz se queda justo bajo Dani
        k = smooth(seg(t, FREEZE[0] - 0.4, FREEZE[0] + 0.2)) * (1 - smooth(seg(t, FREEZE[1] - 0.3, FREEZE[1] + 0.3)))
        target = math.atan2(DUCT_FLOOR + 20 - VISOR_Y, 1000 - 1260)
        base = lerp(base, target + math.sin(t * 3) * 0.05, k)
    return base


def draw(ctx, t):
    draw_basement(ctx, t, lights=0.0, leds=False)
    for i, (x, ph) in enumerate(SENTINELS):
        look = 1.0 if (i == 1 and FREEZE[0] < t < FREEZE[1]) else 0.0
        sentinel(ctx, x, 895, 0.8, phase=t * TAU / 2.6 + ph, look_up=look)
    darken(ctx, 0.45)
    tint(ctx, (1.0, 0.22, 0.17), 1.0)
    beacon(ctx, t, strength=0.8)
    for i, (x, ph) in enumerate(SENTINELS):
        scan_beam(ctx, x, VISOR_Y, beam_angle(i, t), length=1100, spread=0.2, a=0.5)

    duct(ctx, smooth(seg(t, *GRILLE)))
    dani_pose(ctx, dani_x(t), DUCT_FLOOR, 1.0, "crawl", phase=crawl_phase(t), backpack=True)
    # penumbra dentro del ducto
    ctx.save()
    ctx.rectangle(0, DUCT_Y0 + 22, W, DUCT_FLOOR - DUCT_Y0 - 22)
    ctx.clip()
    fill_screen(ctx, (0.0, 0.01, 0.04), 0.35)
    ctx.restore()

    vignette(ctx, 0.7)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.3)))
    darken(ctx, smooth(seg(t, DURATION - 0.3, DURATION)))
