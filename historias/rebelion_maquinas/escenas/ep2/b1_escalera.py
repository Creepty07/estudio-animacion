"""Final regular 1/2 — Escalera de servicio: un Centinela arranca la mochila de Dani."""
import math
import cairo
from motor.config import W, H
from motor.primitives import seg, smooth, ease_out, ease_in, lerp, darken, tint, vignette, glow, fill_rrect, line, TAU
from historias.rebelion_maquinas.dibujo.env_escalera import stairwell, stair_y, lamp_positions, exit_glow, landing_x, LANDING_W, FLOOR_W
from historias.rebelion_maquinas.dibujo.dani_poses import dani_pose, PACK, PACK_DARK
from historias.rebelion_maquinas.dibujo.characters import sentinel

DURATION = 7.5
SUBS = [
    (0.3, 3.8, "Subes los escalones de dos en dos.", None),
    (4.0, 7.3, "En el piso -1, un Centinela te atrapa de la mochila. Sueltas las correas y sigues corriendo.", None),
]
GRAB_AT = 4.7          # la mano cierra sobre la mochila
RELEASE_AT = 5.15      # Dani suelta las correas
DOOR_AT = 6.9
DANI_S, SENT_S = 0.95, 0.82


def dani_u(t):
    u_grab = landing_x(2) + 150
    if t < GRAB_AT:
        return lerp(60, u_grab, seg(t, 0.0, GRAB_AT))
    if t < RELEASE_AT:
        return u_grab - 25 * math.sin(math.pi * seg(t, GRAB_AT, RELEASE_AT))
    return lerp(u_grab, landing_x(3) + 395, ease_out(seg(t, RELEASE_AT, DOOR_AT)) * 0.6 + seg(t, RELEASE_AT, DOOR_AT) * 0.4)


def sent_u(t):
    """El Centinela sube detrás y se detiene al atrapar la mochila."""
    target = dani_u(GRAB_AT) - 190
    return lerp(landing_x(1) + 330, target, ease_out(seg(t, 3.4, GRAB_AT)))


def pack_draw(ctx, x, y, s, a=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.rotate(-0.3)
    fill_rrect(ctx, -22, -10, 44, 80, 14, (0.42, 0.24, 0.18), a)
    fill_rrect(ctx, -26, 20, 18, 30, 6, PACK_DARK, a)
    line(ctx, 14, -6, 30, 60, 6, PACK_DARK, a)
    line(ctx, -8, -6, -28, 70, 6, PACK_DARK, a)
    ctx.restore()


def draw(ctx, t):
    du = dani_u(t)
    cam_x = du + 120
    cam_y = stair_y(du) - 120
    m = stairwell(ctx, cam_x, cam_y)
    ctx.save()
    ctx.set_matrix(m)

    # Centinela
    su = sent_u(t)
    s_vis = smooth(seg(t, 3.2, 3.8))
    hand = None
    if s_vis > 0:
        moving = t < GRAB_AT
        reach = smooth(seg(t, 4.2, GRAB_AT))
        hand = sentinel(ctx, su, stair_y(su), SENT_S, phase=t * TAU / 0.9 if moving else 0.4,
                        reach=reach, eye_a=s_vis, rim_a=0.4 * s_vis)

    # Dani
    running = t < GRAB_AT or t > RELEASE_AT
    has_pack = t < RELEASE_AT
    if t < DOOR_AT + 0.15:
        dani_pose(ctx, du, stair_y(du), DANI_S, "run" if running else "stand",
                  phase=t * TAU * 2.3, backpack=has_pack, lean=0.32 if running else -0.2)
    ctx.restore()

    # iluminación roja de emergencia
    darken(ctx, 0.08)
    tint(ctx, (1.0, 0.3, 0.24), 0.85)
    ctx.save()
    ctx.set_matrix(m)
    for i, (lx, ly) in enumerate(lamp_positions()):
        pulse = 0.6 + 0.4 * math.sin(t * 6 + i)
        glow(ctx, lx, ly, 60, (1, 0.3, 0.2), 0.9 * pulse)
        glow(ctx, lx, ly + 200, 700, (1, 0.12, 0.08), 0.35 * pulse, cairo.OPERATOR_SCREEN)
    ctx.restore()
    exit_glow(ctx, m, smooth(seg(t, DOOR_AT - 0.2, DOOR_AT + 0.3)))
    # la mochila arrancada, en la mano del Centinela
    if not has_pack and hand:
        ctx.save()
        ctx.set_matrix(m)
        pack_draw(ctx, hand[0] + 6, hand[1] - 10, 1.5)
        ctx.restore()

    vignette(ctx, 0.7)
    from motor.primitives import fill_screen
    fill_screen(ctx, (1, 1, 1), smooth(seg(t, DURATION - 0.45, DURATION)))
