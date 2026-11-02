"""Escena 5 — 3:00. Silencio. La ventana se abre sola de golpe: susto 1 (glitch + destello rojo)."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera_center, vignette, darken, font, src, text_center, glow
from historias.planchada.dibujo import cuarto, personajes, objetos
from historias.planchada.dibujo.paleta import fluo_brillo, FLUO

DURATION = 4.5
SUBS = [
    (1.8, 4.2, "La ventana se abrió sola.", None),
]
TEXTO_HORA = (0.3, 1.3)          # "3:00" en grande
SILENCIO = (1.2, 1.6)            # todo se apaga antes del golpe
SUSTO = 1.6                      # golpe de ventana + ráfaga (la mezcla y SUSTOS de historia.py usan este tiempo)


def draw(ctx, t):
    ctx.save()
    if t < SUSTO:                                                       # primer plano del reloj: 3:00
        z = lerp(3.0, 3.35, smooth(seg(t, 0, SUSTO)))
        cuarto.cam(ctx, z, 560, 470)
        sh = 0.0 if t < 0.3 else math.exp(-(t - 0.3) * 9) * 2.5 * math.sin(t * 90)   # sacudida al marcar las 3:00
        ctx.translate(sh, 0)
        cuarto.cuarto(ctx, t, fluo=0.75 if t < SILENCIO[0] else 0.35, hora=(3, 0), segundero=0, turno="dormida", seed=3)
    else:
        u = t - SUSTO
        cuarto.cam(ctx, lerp(1.9, 1.7, smooth(seg(u, 0, 2.9))), lerp(300, 340, smooth(seg(u, 0, 2.9))), 690)
        ap = smooth(seg(u, 0, 0.14))
        cuarto.cuarto(ctx, t, fluo=0.35 + 0.3 * fluo_brillo(t, 5, "inestable"), hora=(3, 0), segundero=0, ventana=ap, turno="dormida", seed=3)
        personajes.rafa_cama(ctx, *cuarto.CABEZA, 1.0, t, ojos="abiertos", mira=(0.2, -1.0), boca="abierta", rubor=0.5, sudor=1.0)
        objetos.vaho(ctx, cuarto.CABEZA[0] + 10, cuarto.CABEZA[1] + 30, t, 1.0)
    ctx.restore()
    if t < SILENCIO[1]:
        a = smooth(seg(t, TEXTO_HORA[0], TEXTO_HORA[0] + 0.1)) * (1 - smooth(seg(t, TEXTO_HORA[1] - 0.1, TEXTO_HORA[1] + 0.15)))
        if a > 0:
            font(ctx, 190, "Inter Display Black")
            src(ctx, (0.95, 1.0, 1.0), a)
            text_center(ctx, "3:00", W / 2, 470, 6)
    vignette(ctx, 0.72)
    darken(ctx, 1 - smooth(seg(t, 0, 0.15)))
    darken(ctx, smooth(seg(t, DURATION - 0.2, DURATION)))
