"""Escena 12 — Amanece: la tumba sigue vacía, pero ya tiene nombre."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera_center, vignette, darken, glow, tint, fill_screen
from motor.kit import particles
from historias.tumba_llorona.dibujo import fondo_tumba, tumbas, flores

DURATION = 4.6
SUBS = [
    (0.4, 4.3, "Al amanecer, la tumba seguía vacía... pero ya tenía nombre.", None),
]
NOMBRE = "TOMÁS"
GRABA = (2.5, 3.9)                   # el nombre se va grabando de izquierda a derecha
LETRAS = [GRABA[0] + i * (GRABA[1] - GRABA[0]) / (len(NOMBRE) - 1) for i in range(len(NOMBRE))]   # un golpe de cincel por letra
BRILLO = (3.9, 4.5)                  # la primera luz del sol recorre las letras
TUMBA = (W / 2, H * 0.62, 1.3)


def draw(ctx, t):
    k = smooth(seg(t, 0, DURATION))
    ctx.save()
    camera_center(ctx, lerp(1.16, 1.0, k), W / 2, lerp(H * 0.53, H * 0.5, k))
    fondo_tumba.fondo(ctx, t, modo="alba", niebla=1.3, avance_alba=smooth(seg(t, 0, 1.2)))
    x, y, s = TUMBA
    tumbas.tumba_sin_nombre(ctx, x, y, s, nombre=NOMBRE, grabado=smooth(seg(t, *GRABA)), tono_frio=0.15,
                            brillo_nombre=smooth(seg(t, *BRILLO)))
    flores.cempasuchil(ctx, x + 70 * s, y - 30 * s, 36 * s, seed=5)
    glow(ctx, x - 200, y - 120, 560, (1.0, 0.65, 0.4), 0.25)
    ctx.restore()
    tint(ctx, (1.0, 0.86, 0.78), 0.6)
    particles(ctx, t, (1.0, 0.8, 0.6), n=18, seed=101, rise=14, size=(1.2, 2.6), alpha=0.6)
    vignette(ctx, 0.55)
    darken(ctx, 1 - smooth(seg(t, 0, 0.35)))
    darken(ctx, smooth(seg(t, DURATION - 0.25, DURATION)))
