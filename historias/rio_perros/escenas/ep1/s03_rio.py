"""Escena 3 — El río del inframundo y la estela con el perro tallado. Dos líneas de texto y una cita a Sahagún."""
from motor.config import W, H, ACENTO
from motor.primitives import seg, smooth, lerp, camera, font, text_center, src, darken, vignette, window
from historias.rio_perros.dibujo import rio, glifo, ojos

DURATION = 7.4
SUBS = [
    (0.5, 3.2, "Camino al Mictlán hay un río.", None),
    (3.6, 6.6, "Solo un perro puede cruzarte.", None),
]
AULLIDO = 2.2          # aullido lejano
OJOS_LEJOS = 4.8       # se abren unos ojos en la otra orilla (anuncia lo que viene)


def draw(ctx, t):
    ctx.save()
    camera(ctx, lerp(1.0, 1.10, smooth(seg(t, 0, DURATION))), W / 2, H * 0.50)
    rio.fondo(ctx, t)
    a = smooth(seg(t, OJOS_LEJOS, OJOS_LEJOS + 0.4))
    ojos.par(ctx, W * 0.30, rio.LEJOS_Y + 4, 0.55, a, separacion=46)
    rio.orilla(ctx, t)
    glifo.estela(ctx, W * 0.80, rio.ORILLA_Y + 60, 1.0, t, brillo=smooth(seg(t, 0.3, 1.4)))
    ctx.restore()
    rio.niebla_baja(ctx, t)
    font(ctx, 30, "DejaVu Serif", italic=True)
    src(ctx, (0.80, 0.88, 0.92), 0.85 * window(t, 4.4, 7.1, 0.5))
    text_center(ctx, "FRAY BERNARDINO DE SAHAGÚN · SIGLO XVI", W / 2, 215, 3)
    vignette(ctx, 0.62)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.5)))
    darken(ctx, smooth(seg(t, DURATION - 0.35, DURATION)))
