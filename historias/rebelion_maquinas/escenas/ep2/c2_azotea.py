"""Final bueno 2/3 — Azotea: la ciudad entera se detiene y mira al cielo."""
from motor.primitives import seg, smooth, lerp, vignette, darken, TAU
from historias.rebelion_maquinas.dibujo.env_exterior import rooftop, ROOF_Y
from historias.rebelion_maquinas.dibujo.dani_poses import dani_pose

DURATION = 7.5
FREEZE_AT = 3.9
SUBS = [
    (0.3, 3.5, "Sales por una rejilla a la azotea del estacionamiento vecino, con tu mochila intacta.", None),
    (3.7, 7.3, "Desde ahí ves la ciudad entera: todos los robots se han detenido al mismo tiempo… mirando al cielo.", None),
]


def draw(ctx, t):
    z = lerp(1.0, 1.08, smooth(seg(t, 0.0, DURATION)))
    rooftop(ctx, t, FREEZE_AT, z)
    if t < 1.3:
        dani_pose(ctx, lerp(300, 470, seg(t, 0.1, 1.3)), ROOF_Y + 20, 1.0, "crawl",
                  phase=t * TAU * 1.3, backpack=True)
    else:
        x = lerp(560, 780, smooth(seg(t, 1.3, 3.3)))
        walking = t < 3.3
        dani_pose(ctx, x, ROOF_Y + 40, 1.15, "run" if walking else "stand",
                  phase=t * TAU * 1.1, backpack=True, lean=0.05 if walking else 0.0,
                  look_up=0.5 * smooth(seg(t, FREEZE_AT + 0.3, FREEZE_AT + 1.2)))
    vignette(ctx, 0.65)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.3)))
    darken(ctx, smooth(seg(t, DURATION - 0.3, DURATION)))
