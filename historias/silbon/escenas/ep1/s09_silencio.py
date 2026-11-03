"""Silencio total; el silbido suena cerca (todos sonríen) y luego, lejísimos (las sonrisas se apagan)."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, window
from historias.silbon.dibujo import fondos, notas, props
from historias.silbon.dibujo.gente import persona, en_hamaca, PERSONAJES as P
from historias.silbon.dibujo.animales import perro
from historias.silbon.dibujo.escena import camara, marco, sombra

DURATION = 10.6
SUBS = [
    (0.4, 1.9, "*Silencio*.", None),
    (3.1, 6.8, "El silbido suena *cerca*. Todos sonríen.", None),
    (7.1, 10.1, "Pero ahora suena… *lejísimos*.", None),
]
SILENCIO = (0.6, 3.0)       # sin sonido alguno: el hueco antes del silbido
CERCA = 3.0                 # silbido fuerte: las siete notas grandes
LEJOS = 7.0                 # silbido lejano: notas chicas y pálidas


def draw(ctx, t):
    ctx.save()
    camara(ctx, t, DURATION, 1.0, 1.08, 0.5, 0.45)
    luz = 0.7 + 0.3 * smooth(seg(t, 2.8, 3.1)) - 0.25 * smooth(seg(t, LEJOS, LEJOS + 0.4))
    fondos.pared(ctx, t, farol=(0.5, 0.20), luz=luz, parpadeo=t > 2.9)
    fondos.farol(ctx, W * 0.5, H * 0.20 + 30, 0.9, t, luz)
    sonrien = smooth(seg(t, CERCA + 0.1, CERCA + 0.5)) * (1 - smooth(seg(t, LEJOS + 0.2, LEJOS + 0.8)))
    e = "sonrisa" if sonrien > 0.5 else ("miedo" if t > LEJOS + 0.4 else "sospecha")
    en_hamaca(ctx, 150, 760, 0.7, P["abuela"], e, 1, (0.45, 0.3, 0.55), t, respira=False)
    en_hamaca(ctx, 150, 980, 0.7, P["nina"], e, 1, (0.3, 0.5, 0.6), t + 1, respira=False)
    persona(ctx, 850, 760, 0.9, P["ramiro"], "borracho" if e == "sonrisa" else e, mira=(0.0, -0.3), t=t, solo_cabeza=True)
    persona(ctx, 850, 1010, 0.9, P["llanero"], e, mira=(0.0, -0.3), t=t, solo_cabeza=True)
    perro(ctx, 560, 1200, 0.6, (0.35, 0.25, 0.18), lado=1, callado=True, t=t)
    ctx.restore()
    notas.silbido(ctx, t, CERCA, W / 2, 440, 1.25, dur=1.4, mantener=1.6, alpha=1.0)
    notas.silbido(ctx, t, LEJOS, W / 2, 430, 0.45, dur=1.4, mantener=1.2, alpha=0.55)
    marco(ctx, t, DURATION)
