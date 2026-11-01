"""Dani en movimiento: correr, estar de pie, jadear y gatear. Mira a la derecha (facing=1)."""
import math
from motor.primitives import src, fill_rrect, line, circle, fill_poly, mix, TAU
from historias.rebelion_maquinas.dibujo.characters import SKIN, SUIT, SUIT_DARK, PANTS, CAP

PACK = (0.22, 0.30, 0.24)
PACK_DARK = (0.15, 0.2, 0.16)
BOOT = (0.11, 0.09, 0.08)
PANTS_BACK = mix(PANTS, (0, 0, 0), 0.25)


def limb(ctx, a, b, w, c):
    line(ctx, a[0], a[1], b[0], b[1], w, c)


def _leg(phi, hip):
    th1 = 0.65 * math.sin(phi)
    bend = 0.25 + 1.0 * max(0.0, math.cos(phi))
    knee = (hip[0] + 78 * math.sin(th1), hip[1] + 78 * math.cos(th1))
    th2 = th1 - bend
    foot = (knee[0] + 72 * math.sin(th2), knee[1] + 72 * math.cos(th2))
    return knee, foot


def _arm(phi, sh):
    a = -0.9 * math.sin(phi)
    elbow = (sh[0] + 52 * math.sin(a), sh[1] + 52 * math.cos(a))
    b = a + 1.5
    hand = (elbow[0] + 46 * math.sin(b), elbow[1] + 46 * math.cos(b) * -0.2 - 10)
    return elbow, hand


def _head(ctx, hx, hy, tilt=0.0):
    ctx.save()
    ctx.translate(hx, hy)
    ctx.rotate(tilt)
    circle(ctx, 0, 0, 30, SKIN)
    fill_poly(ctx, [(28, -2), (38, 6), (28, 9)], SKIN)
    circle(ctx, 16, -4, 3.2, (0.1, 0.07, 0.06))
    fill_rrect(ctx, -28, -8, 20, 30, 8, (0.13, 0.09, 0.07))
    circle(ctx, -12, 2, 6, mix(SKIN, (0, 0, 0), 0.15))
    ctx.arc(0, -6, 32, math.pi, TAU)
    ctx.close_path()
    src(ctx, CAP)
    ctx.fill()
    fill_rrect(ctx, 16, -12, 46, 9, 4, mix(CAP, (0, 0, 0), 0.25))
    ctx.restore()


def _torso(ctx, by, backpack):
    if backpack:
        fill_rrect(ctx, -66, -266 + by, 40, 112, 14, PACK)
        fill_rrect(ctx, -70, -214 + by, 22, 40, 6, PACK_DARK)
    fill_rrect(ctx, -36, -272 + by, 72, 130, 18, SUIT)
    ctx.rectangle(-36, -196 + by, 72, 9)
    src(ctx, (0.9, 0.92, 0.88))
    ctx.fill()
    fill_rrect(ctx, -38, -152, 76, 13, 3, (0.25, 0.16, 0.1))
    if backpack:
        line(ctx, -30, -262 + by, -10, -200 + by, 7, PACK_DARK)


def dani_pose(ctx, x, y, s, pose="stand", phase=0.0, facing=1, backpack=False,
              look_up=0.0, breathe=0.0, lean=None):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s * facing, s)
    if pose == "crawl":
        _crawl(ctx, phase, backpack)
        ctx.restore()
        return
    # sombra
    ctx.save()
    ctx.scale(1, 0.18)
    circle(ctx, 0, 0, 80, (0, 0, 0), 0.4)
    ctx.restore()

    if pose == "run":
        bob = -abs(math.sin(phase)) * 9
        lean_a = 0.2 if lean is None else lean
    elif pose == "pant":
        bob = math.sin(breathe * TAU) * 4
        lean_a = 0.32 if lean is None else lean
    else:
        bob = 0.0
        lean_a = 0.0 if lean is None else lean
    ctx.translate(0, bob)

    hip = (0, -150)
    if pose == "run":
        kb, fb = _leg(phase + math.pi, hip)
        kf, ff = _leg(phase, hip)
    else:
        kb, fb = (8, -76), (10, -8)
        kf, ff = (-8, -76), (-10, -8)
    limb(ctx, hip, kb, 24, PANTS_BACK)
    limb(ctx, kb, fb, 22, PANTS_BACK)
    fill_rrect(ctx, fb[0] - 12, fb[1] - 8, 34, 16, 6, BOOT)

    # tronco inclinado alrededor de la cadera
    ctx.save()
    ctx.translate(*hip)
    ctx.rotate(lean_a)
    ctx.translate(-hip[0], -hip[1])
    sh = (4, -252)
    if pose == "run":
        eb, hb = _arm(phase, sh)
        ef, hf = _arm(phase + math.pi, sh)
    else:
        eb, hb = (0, -200), (2, -150)
        ef, hf = (10, -200), (14, -150)
        if pose == "pant":
            ef, hf = (20, -196), (34, -150)
    limb(ctx, sh, eb, 18, SUIT_DARK)
    limb(ctx, eb, hb, 16, SUIT_DARK)
    by = 0
    _torso(ctx, by, backpack)
    _head(ctx, 4, -302, -0.35 * look_up - (0.15 if pose == "run" else 0))
    limb(ctx, sh, ef, 20, SUIT)
    limb(ctx, ef, hf, 18, SUIT)
    circle(ctx, hf[0], hf[1], 10, SKIN)
    ctx.restore()

    limb(ctx, hip, kf, 24, PANTS)
    limb(ctx, kf, ff, 22, PANTS)
    fill_rrect(ctx, ff[0] - 12, ff[1] - 8, 34, 16, 6, BOOT)
    ctx.restore()


def _crawl(ctx, phase, backpack):
    sw = math.sin(phase)
    hips, shoulders = (-60, -70), (48, -78)
    # extremidades traseras (más oscuras)
    kb = (-40 + 22 * math.sin(phase + math.pi), -6)
    limb(ctx, hips, kb, 22, PANTS_BACK)
    limb(ctx, kb, (kb[0] - 70, -12), 20, PANTS_BACK)
    hb = (60 + 22 * math.sin(phase + math.pi), -4)
    limb(ctx, shoulders, ((shoulders[0] + hb[0]) / 2 + 8, -40), 16, SUIT_DARK)
    limb(ctx, ((shoulders[0] + hb[0]) / 2 + 8, -40), hb, 15, SUIT_DARK)
    # tronco horizontal
    limb(ctx, hips, shoulders, 66, SUIT)
    line(ctx, hips[0] + 30, -74, hips[0] + 30, -54, 8, (0.9, 0.92, 0.88))
    if backpack:
        fill_rrect(ctx, -54, -134, 78, 40, 14, PACK)
        line(ctx, 12, -100, 30, -76, 7, PACK_DARK)
    _head(ctx, 92, -96, 0.25)
    # extremidades delanteras
    kf = (-40 + 22 * sw, -6)
    limb(ctx, hips, kf, 24, PANTS)
    limb(ctx, kf, (kf[0] - 72, -12), 22, PANTS)
    fill_rrect(ctx, kf[0] - 96, -22, 30, 16, 6, BOOT)
    hf = (64 + 22 * sw, -4)
    el = ((shoulders[0] + hf[0]) / 2 + 10, -40)
    limb(ctx, shoulders, el, 18, SUIT)
    limb(ctx, el, hf, 17, SUIT)
    circle(ctx, hf[0] + 4, hf[1] - 4, 9, SKIN)
