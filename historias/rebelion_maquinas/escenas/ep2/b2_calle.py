"""Final regular 2/2 — Dani sale a la calle, vivo pero sin mochila."""
import math
from motor.primitives import seg, smooth, ease_out, lerp, vignette, darken, fill_screen, TAU
from historias.rebelion_maquinas.dibujo.env_exterior import street, STREET_Y
from historias.rebelion_maquinas.dibujo.dani_poses import dani_pose

DURATION = 6.5
SUBS = [
    (0.4, 3.2, "Sales a la calle vivo, con el corazón en la garganta.", None),
    (3.4, 6.2, "Pero tu mochila se quedó adentro, con tu radio y tu linterna.", None),
]
STOP_AT = 2.4
LOOK_BACK = 3.6


def draw(ctx, t):
    street(ctx, t)
    x = lerp(300, 1050, ease_out(seg(t, 0.1, STOP_AT)))
    if t < STOP_AT:
        dani_pose(ctx, x, STREET_Y + 30, 1.25, "run", phase=t * TAU * 2.2, backpack=False)
    else:
        facing = -1 if t > LOOK_BACK else 1
        dani_pose(ctx, x, STREET_Y + 30, 1.25, "pant", facing=facing, breathe=t * 1.6,
                  lean=lerp(0.32, 0.12, smooth(seg(t, LOOK_BACK, LOOK_BACK + 0.6))))
    vignette(ctx, 0.65)
    fill_screen(ctx, (1, 1, 1), 1 - smooth(seg(t, 0.0, 0.35)))
    darken(ctx, smooth(seg(t, DURATION - 0.4, DURATION)))
