"""Escena 6 — Flashback: Tenochtitlan de noche, y la mujer que gritaba sobre el agua (sexto presagio)."""
import math
import random
from motor.config import W, H, FANTASMA
from motor.primitives import seg, smooth, ease_out, lerp, camera, vignette, darken, tint, font, text_center, src, line
from historias.tumba_llorona.dibujo import tenochtitlan, llorona, paisaje
from motor import config

DURATION = 8.2
SUBS = [
    (0.3, 2.7, "Antes de que llegaran los españoles,", None),
    (2.8, 5.2, "Tenochtitlan ya la oía gritar de noche:", None),
    (5.4, 8.0, "¡Hijitos míos! ¿A dónde los llevaré?", None),
]
APARECE = 5.0                    # empieza a verse la mujer sobre el agua
GRITO = 5.4                      # "¡Hijitos míos!"
FIGURA = (W * 0.72, H * 0.62, 0.62)


def draw(ctx, t):
    r = random.Random(int(t * 24))
    ctx.save()
    camera(ctx, lerp(1.0, 1.1, smooth(seg(t, 0, DURATION))), W / 2, H * 0.52)
    tenochtitlan.dibujar(ctx, t, brillo=0.92 + 0.08 * r.random())
    a = smooth(seg(t, APARECE, APARECE + 1.4)) * 0.88
    if a > 0:
        x, y, s = FIGURA
        bob = 6 * math.sin(t * 1.3)
        brazos = smooth(seg(t, GRITO - 0.3, GRITO + 0.9))
        paisaje.ondas(ctx, x, y + 6, APARECE, t, n=4, rmax=210, a=0.5, dur=2.6)
        llorona.de_pie(ctx, x, y + bob, s, t, brazos=brazos, alpha=a, giro=0.0, aura=1.3)
    ctx.restore()
    # rótulo del lugar
    k = smooth(seg(t, 0.5, 1.3)) * (1 - smooth(seg(t, 3.2, 3.9)))
    if k > 0:
        font(ctx, 44, config.FONT, bold=True)
        src(ctx, (1.0, 0.88, 0.7), k)
        text_center(ctx, "TENOCHTITLAN", W / 2, H * 0.12, 14)
        line(ctx, W / 2 - 150, H * 0.12 + 28, W / 2 + 150, H * 0.12 + 28, 3, (1.0, 0.7, 0.35), 0.8 * k)
    tint(ctx, (0.9, 0.94, 1.0), 0.8)
    vignette(ctx, 0.78)
    flash = max(0.0, 1 - abs(t - GRITO) * 5) * 0.10
    darken(ctx, 1 - smooth(seg(t, 0, 0.4)) - flash)
    darken(ctx, smooth(seg(t, DURATION - 0.3, DURATION)))
