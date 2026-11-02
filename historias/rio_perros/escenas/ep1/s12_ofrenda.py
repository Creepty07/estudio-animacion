"""Escena 12 — Corte al mundo de los vivos: una ofrenda cálida con media tortilla, agua y un perrito de barro."""
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera, darken, vignette
from historias.rio_perros.dibujo import ofrenda

DURATION = 6.4
SUBS = [(0.6, 4.4, "Por eso, en muchas ofrendas hay un lugar para ellos.", None)]
CAMPANA = 0.0              # entra una campana suave con el corte


def draw(ctx, t):
    ctx.save()
    camera(ctx, lerp(1.0, 1.08, smooth(seg(t, 0, DURATION))), W / 2, H * 0.60)
    ofrenda.dibujar(ctx, t)
    ctx.restore()
    vignette(ctx, 0.5)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.7)))
    darken(ctx, smooth(seg(t, DURATION - 0.4, DURATION)))
