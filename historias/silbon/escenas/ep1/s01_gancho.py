"""Gancho (0-5.8 s): un silbido de siete notas en el llano y, de golpe, el ojo del Silbón por la rendija de la puerta."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, darken, glow
from historias.silbon.dibujo import fondos, notas, hud
from historias.silbon.dibujo.silbon import silbon, ojo_en_rendija
from historias.silbon.dibujo.escena import camara, marco, temblor_en

DURATION = 5.8
SUBS = [
    (0.3, 2.6, "Si oyes este *silbido*…", None),
    (2.9, 5.5, "alguien en tu casa *no amanece*.", None),
]
SILBIDO = 0.0            # las siete notas (el sonido arranca en el primer cuadro)
SUSTO = 3.0              # el ojo aparece detrás de la puerta (golpe + glitch)
PARPADEO = 4.5
CORTE = 2.9              # del llano a la puerta


def _vista_noche(ctx):
    fondos.llano(ctx, 0.0, luna=(0.5, 0.16), r_luna=90, cocuyos=False)


def draw(ctx, t, ):
    hz = H * fondos.HORIZONTE
    if t < CORTE:
        ctx.save()
        camara(ctx, t, CORTE, 1.0, 2.1, 0.5, 0.60)                   # zoom hacia la figura lejana
        fondos.llano(ctx, t, luna=(0.82, 0.26), r_luna=84)
        silbon(ctx, W / 2, hz + 38, 0.14, t, ojos=0.5 + 0.5 * seg(t, 1.6, 2.6), luz=0.9)
        ctx.restore()
        notas.silbido(ctx, t, SILBIDO, W / 2, H * 0.26, 1.15, dur=1.4, mantener=1.0)
        hud.usa_audifonos(ctx, t, 0.25, 2.7)
    else:
        u = t - CORTE
        ctx.save()
        camara(ctx, u, DURATION - CORTE, 1.0, 1.16, 0.5, 0.48, temblor=temblor_en(u, 0.1, 0.5, 14))
        fondos.pared(ctx, t, farol=(0.5, 0.45), luz=0.5)
        fondos.puerta_rendija(ctx, 80, 140, W - 160, H - 360, 0.20, vista=_vista_noche, t=t)
        abre = smooth(seg(t, SUSTO, SUSTO + 0.22)) * (1 - 0.97 * smooth(seg(t, PARPADEO, PARPADEO + 0.1)) * (1 - smooth(seg(t, PARPADEO + 0.14, PARPADEO + 0.3))))
        mira = 0.0 if t < 4.8 else math.sin((t - 4.8) * 3) * 0.8
        ojo_en_rendija(ctx, W / 2, H * 0.43, 1.28, t, abre, mira)
        ctx.restore()
    marco(ctx, t, DURATION, entra=0.0, sale=0.06)
