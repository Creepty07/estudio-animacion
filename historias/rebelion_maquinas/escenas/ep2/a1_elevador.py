"""Final malo 1/2 — Dani corre al montacargas; las puertas se abren solas."""
import math
from motor.primitives import seg, smooth, ease_out, lerp, camera, darken, tint, vignette, TAU
from historias.rebelion_maquinas.dibujo.environments import beacon
from historias.rebelion_maquinas.dibujo.env_elevador import elevator_hall, light_spill, OPEN_X0, OPEN_X1, OPEN_Y0, FLOOR_Y, MID, PANEL_W
from historias.rebelion_maquinas.dibujo.dani_poses import dani_pose

DURATION = 7.0
SUBS = [
    (0.3, 3.3, "Corres al elevador. Las puertas se abren con un suave «ding»… como si te estuvieran esperando.", None),
    (3.5, 6.8, "Entras. Las puertas se cierran y la cabina empieza a subir.", None),
]
DING_AT = 1.25
OPEN = (1.35, 2.0)
CLOSE = (3.6, 4.5)
FLOOR_CHANGE = 5.6
RUN = (0.15, 3.0)


def open_amount(t):
    return smooth(seg(t, *OPEN)) * (1 - smooth(seg(t, *CLOSE)))


def dani_x(t):
    return lerp(-120, 900, ease_out(seg(t, *RUN)) * 0.15 + seg(t, *RUN) * 0.85)


def draw_dani(ctx, t):
    x = dani_x(t)
    if t < RUN[1]:
        dani_pose(ctx, x, FLOOR_Y + 40, 1.25, "run", phase=t * TAU * 2.0, backpack=True)
    else:
        dani_pose(ctx, x, FLOOR_Y + 40, 1.25, "stand", facing=-1, backpack=True,
                  look_up=smooth(seg(t, 4.6, 5.4)))


def draw(ctx, t):
    o = open_amount(t)
    inside = dani_x(t) > OPEN_X0 + 40
    ctx.save()
    z = lerp(1.0, 1.06, t / DURATION) + 0.08 * smooth(seg(t, 4.6, 7.0))
    camera(ctx, z, 960, lerp(560, 330, smooth(seg(t, 4.6, 7.0))))

    def inside_fn(c):
        if inside:
            draw_dani(c, t)

    floor_text = "-3" if t < FLOOR_CHANGE else "-2"
    elevator_hall(ctx, t, o, floor_text, arrow_on=t > CLOSE[1] and (t * 2.5) % 1 < 0.6,
                  button_on=0.9 < t < CLOSE[1], draw_inside=inside_fn)
    if not inside:
        draw_dani(ctx, t)
    m = ctx.get_matrix()
    ctx.restore()

    # luz roja de emergencia en todo, menos el hueco abierto de la cabina
    ctx.save()
    ctx.set_matrix(m)
    gap = PANEL_W * o
    ctx.set_fill_rule(1)  # EVEN_ODD
    ctx.rectangle(-400, -400, 2800, 2000)
    if gap > 1:
        ctx.rectangle(MID - gap, OPEN_Y0, gap * 2, FLOOR_Y - OPEN_Y0)
    ctx.clip()
    darken(ctx, 0.3)
    tint(ctx, (1.0, 0.24, 0.19), 1.0)
    ctx.restore()
    ctx.save()
    ctx.set_matrix(m)
    beacon(ctx, t, x=360, y=200, strength=0.8)
    light_spill(ctx, o)
    ctx.restore()

    vignette(ctx, 0.7)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.25)))
    darken(ctx, smooth(seg(t, DURATION - 0.3, DURATION)))
