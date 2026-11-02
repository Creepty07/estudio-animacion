"""Escena 11 — El perro rojizo se echa al agua con Don Celso a cuestas y los dos se pierden en la niebla."""
import cairo
from motor.config import W, H, ROJIZO, ACENTO, HILO
from motor.primitives import seg, smooth, ease_out, lerp, camera, darken, vignette, window
from historias.rio_perros.dibujo import rio, celso as C, perros, ojos

DURATION = 8.0
SUBS = [
    (0.5, 2.6, "Lo olió... y se echó al agua.", None),
    (3.5, 7.0, "Dicen que los perros no olvidan quién les dio de comer.", None),
]
SE_ECHA = 0.5              # entra al agua (chapoteo)
NADA = (0.9, 7.0)          # tramo de nado en diagonal hacia la otra orilla
DESAPARECE = (5.6, 7.3)    # la niebla se los traga
OJOS = ((200, 705, 0.45, 38), (620, 702, 0.55, 46), (900, 708, 0.42, 36))


def _pos(u):
    return lerp(900, 380, u ** 0.9), lerp(1190, 790, u), lerp(1.55, 0.5, u ** 0.85)


def draw(ctx, t):
    ctx.save()
    camera(ctx, lerp(1.0, 1.04, smooth(seg(t, 0, DURATION))), W / 2, H * 0.55)
    rio.fondo(ctx, t)
    for x, y, s, sep in OJOS:
        ojos.par(ctx, x, y, s, 0.8 * window(t, 0.2, 5.0, 0.8), 1.0, ACENTO, sep)
    # grupo del nadador para poder desvanecerlo en la niebla
    ctx.push_group()
    u = smooth(seg(t, *NADA))
    x, y, s = _pos(u)
    perros.perro_nadando(ctx, x, y, s, ROJIZO, t, dir=-1, hilo=HILO, rim=(1.0, 0.75, 0.45))
    C.celso_en_el_lomo(ctx, x - 30 * s, y - 6 * s, s, t, dir=-1)
    ctx.pop_group_to_source()
    ctx.paint_with_alpha(1.0 - smooth(seg(t, *DESAPARECE)) if t >= SE_ECHA else 0.0)
    rio.orilla(ctx, t) if t < 1.2 else None
    ctx.restore()
    rio.niebla_baja(ctx, t, 1.0 + 1.4 * smooth(seg(t, 3.0, DESAPARECE[1])))
    vignette(ctx, 0.64)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.4)))
    darken(ctx, smooth(seg(t, DURATION - 0.5, DURATION)))
