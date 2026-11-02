"""Escena 10 — Entre la niebla ladra un perro rojizo: flaco, con un hilo flojo al cuello. Huele la mano de Don Celso."""
from motor.config import W, H, ROJIZO, ACENTO, HILO
from motor.primitives import seg, smooth, ease_out, lerp, camera, glow, darken, vignette
from historias.rio_perros.dibujo import rio, celso as C, perros

DURATION = 7.8
SUBS = [
    (0.4, 2.5, "Entonces ladró uno rojizo.", None),
    (2.8, 5.0, "Flaco. Con un hilo flojo al cuello.", None),
    (5.3, 7.3, "El de la media tortilla.", None),
]
LADRIDO = 0.9              # ladrido desde la niebla
LLEGA = (1.2, 3.9)         # el perro camina hasta Celso
OLFATEA = (4.2, 6.6)       # le huele la mano
CELSO_X = 300
PARA_X = 500
FEET = rio.ORILLA_Y + 30


def draw(ctx, t):
    ctx.save()
    camera(ctx, lerp(1.0, 1.14, smooth(seg(t, 0, DURATION))), W * 0.42, H * 0.64)
    rio.fondo(ctx, t)
    rio.orilla(ctx, t)
    calido = smooth(seg(t, LADRIDO, LLEGA[1]))
    glow(ctx, 1040, 1080, 620, (1.0, 0.55, 0.20), 0.30 * calido)               # contraluz cálido: viene de entre la niebla
    ag = smooth(seg(t, OLFATEA[0] - 0.7, OLFATEA[0])) * (1 - smooth(seg(t, OLFATEA[1], OLFATEA[1] + 0.8)))
    C.celso(ctx, CELSO_X, FEET + 4, 1.3, dir=1, brazo_der=lerp(0.1, 1.15, ag), brazo_izq=-0.1, agacha=0.55 * ag,
            cabeza_baja=0.3, t=t, sombra=0.30)
    if t >= LADRIDO:
        u = ease_out(seg(t, *LLEGA))
        x = lerp(1250, PARA_X, u)
        sniff = smooth(seg(t, OLFATEA[0], OLFATEA[0] + 0.5)) * (1 - smooth(seg(t, OLFATEA[1], OLFATEA[1] + 0.6)))
        perros.perro(ctx, x, FEET + 14, 1.15, ROJIZO, dir=-1, t=t, paso=1.3 if 0.02 < u < 0.97 else 0.0,
                     cabeza=lerp(0.25, -0.8, sniff), orejas=1.2, flaco=1.0, hilo=HILO, ojos=ACENTO, brillo_ojos=0.95,
                     cola=0.3 + 0.7 * sniff, rim=(1.0, 0.75, 0.45))
    ctx.restore()
    rio.niebla_baja(ctx, t, 1.0)
    vignette(ctx, 0.62)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.4)))
    darken(ctx, smooth(seg(t, DURATION - 0.4, DURATION)))
