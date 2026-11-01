"""Escena 7 — Siglos después: la Llorona de espaldas junto al canal, mirando el agua."""
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera_center, vignette, darken
from motor.kit import particles
from historias.tumba_llorona.dibujo import canal_vista, llorona, paisaje

DURATION = 5.15
SUBS = [
    (0.2, 2.8, "Siglos después, la contaban como una madre", None),
    (2.9, 5.0, "que perdió a sus hijos en el agua.", None),
]
ENTRA = 0.7                           # la figura se hace visible
FIGURA = (W * 0.40, H * 0.63, 0.64)


def draw(ctx, t):
    k = smooth(seg(t, 0, DURATION))
    ctx.save()
    camera_center(ctx, lerp(1.0, 1.12, k), lerp(W / 2, W * 0.46, k), lerp(H * 0.5, H * 0.55, k))
    canal_vista.dibujar(ctx, t)
    x, y, s = FIGURA
    paisaje.ondas(ctx, x, y - 34, ENTRA, t, n=3, rmax=150, achatado=0.2, a=0.4, dur=2.8)
    llorona.de_pie(ctx, x, y, s, t, de_frente=False, alpha=smooth(seg(t, ENTRA, ENTRA + 1.0)))
    ctx.restore()
    particles(ctx, t, (0.7, 0.85, 1.0), n=16, seed=52, rise=12, size=(1, 2.4), alpha=0.6)
    vignette(ctx, 0.7)
    darken(ctx, 1 - smooth(seg(t, 0, 0.5)))
    darken(ctx, smooth(seg(t, DURATION - 0.3, DURATION)))
