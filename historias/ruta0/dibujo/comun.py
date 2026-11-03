"""Ayudas de escena de Ruta 0: marco de viñeta + fundidos, lluvia y neblina."""
from motor.primitives import seg, smooth, vignette, darken, fill_screen
from motor.kit import rain, fog


def marco(ctx, t, dur, v=0.7, entra=0.3, sale=0.25):
    vignette(ctx, v)
    if entra:
        darken(ctx, 1 - smooth(seg(t, 0, entra)))
    if sale:
        darken(ctx, smooth(seg(t, dur - sale, dur)))


def lluvia(ctx, t, n=150, alpha=0.22, seed=3):
    rain(ctx, t, n=n, alpha=alpha, seed=seed, angle=0.12, speed=1500)


def niebla(ctx, t, alpha=0.14, seed=4, y0=None):
    from motor import config
    fog(ctx, t, (0.55, 0.68, 0.8), alpha, y0 if y0 is not None else config.H * 0.5, config.H * 0.95, seed=seed)


def ivan_de_pie(ctx, x, y, s=1.4, pose="pie", fase=0.0, alpha=1.0):
    """Iván de pie o caminando: reutiliza a Tomás de La Tumba de la Llorona (adolescente en sudadera) y le pone la mochila."""
    from motor.primitives import fill_rrect, line
    from historias.tumba_llorona.dibujo import personas
    if alpha < 1.0:
        ctx.push_group()
    fill_rrect(ctx, x - 104 * s, y - 300 * s, 70 * s, 150 * s, 16 * s, (0.12, 0.1, 0.09))          # mochila detrás del hombro
    personas.tomas(ctx, x, y, s, pose, fase)
    for sx in (-1, 1):                                                                               # tirantes
        line(ctx, x + sx * 40 * s, y - 286 * s, x + sx * 44 * s, y - 166 * s, 7 * s, (0.2, 0.15, 0.1), 0.9)
    if alpha < 1.0:
        ctx.pop_group_to_source()
        ctx.paint_with_alpha(alpha)
