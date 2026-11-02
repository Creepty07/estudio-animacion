"""Escena 5 — La misma calle de noche: Don Celso, a escondidas, le deja media tortilla al cachorro."""
import math
from motor.config import W, H, ROJIZO, ACENTO
from motor.primitives import seg, smooth, ease_out, lerp, camera, darken, vignette, glow
from historias.rio_perros.dibujo import calle, celso as C, perros

DURATION = 7.0
SUBS = [(0.5, 4.2, "A uno, en secreto, le dejaba media tortilla.", None)]
LLEGA = (0.2, 2.3)          # Don Celso camina a escondidas hacia el barril
AGACHA = (2.5, 3.1)         # se agacha con la tortilla en la mano
DEJA = 3.2                  # la pone en el piso
SE_VA = 4.2                 # se da la vuelta y se va
COME = (4.3, 6.2)           # el cachorro come
FEET = calle.SUELO + 65
TORTILLA_X = 670


def _celso(t):
    """(x, dir, camina, agacha) de Don Celso en el instante t."""
    if t < LLEGA[1]:
        return lerp(-120, 520, seg(t, *LLEGA)), 1, 1.5 if t > LLEGA[0] else 0.0, 0.0
    if t < SE_VA:
        ag = smooth(seg(t, *AGACHA)) * (1 - smooth(seg(t, DEJA + 0.3, SE_VA - 0.2)))
        return 520, 1, 0.0, ag
    return 520 - 640 * smooth(seg(t, SE_VA, DURATION - 0.2)), -1, 1.4, 0.0


def _cachorro(t):
    """(x, dir, paso, cabeza, cola) del cachorro."""
    if t < 1.0:
        return 1020, -1, 0.0, 0.0, 0.0
    if t < 2.2:
        u = ease_out(seg(t, 1.0, 2.2))
        return lerp(1020, 930, u), -1, 0.7 if u < 0.97 else 0.0, 0.1, 0.2
    if t < COME[0]:
        u = smooth(seg(t, DEJA + 0.5, COME[0]))
        return lerp(930, 762, u), -1, 1.4 if 0.02 < u < 0.98 else 0.0, lerp(0.2, -1.0, u), 0.6
    if t < COME[1]:
        return 762, -1, 0.0, -1.0, 1.0
    return 762, -1, 0.0, lerp(-1.0, 0.3, smooth(seg(t, COME[1], COME[1] + 0.6))), 0.7


def draw(ctx, t):
    ctx.save()
    camera(ctx, lerp(1.0, 1.08, smooth(seg(t, 0, DURATION))), W * 0.55, H * 0.62)
    calle.fondo(ctx, t, noche=True)
    # tortilla en el piso
    if DEJA <= t < COME[1] - 0.6:
        ctx.save()
        ctx.translate(TORTILLA_X, FEET + 4)
        ctx.move_to(-34, 0)
        ctx.arc(0, 0, 34, math.pi, 0)
        ctx.close_path()
        ctx.set_source_rgb(0.93, 0.76, 0.42)
        ctx.fill()
        ctx.restore()
        glow(ctx, TORTILLA_X, FEET - 8, 90, (1.0, 0.75, 0.35), 0.18)
    cx, cd, cam, ag = _celso(t)
    C.celso(ctx, cx, FEET + 6, 1.25, dir=cd, brazo_der=1.35 if 2.5 < t < DEJA + 0.15 else 0.15, brazo_izq=-0.2,
            agacha=ag, tortilla=2.5 < t < DEJA, sombra=0.30, t=t, camina=cam, rim=(0.55, 0.7, 1.0))
    px, pd, pp, pc, pcola = _cachorro(t)
    if t >= 1.0:
        perros.perro(ctx, px, FEET + 22, 0.70, ROJIZO, dir=pd, t=t, paso=pp, cabeza=pc, orejas=1.3, flaco=0.8, cola=pcola,
                     ojos=ACENTO, brillo_ojos=0.55, rim=(0.6, 0.75, 1.0))
    calle.barril(ctx, True)
    ctx.restore()
    vignette(ctx, 0.62)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.5)))
    darken(ctx, smooth(seg(t, DURATION - 0.4, DURATION)))
