"""Cierre: el dilema CONTAR • CALLAR, el llamado a comentar 1 o 2 y el apagón con silbido que vuelve al gancho."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, glow, darken
from historias.silbon.dibujo import fondos, hud
from historias.silbon.dibujo.gente import persona, PERSONAJES as P
from historias.silbon.dibujo.escena import camara, marco

DURATION = 7.8
SUBS = [
    (0.4, 3.5, "¿Cuentas los huesos… o te *callas*?", None),
    (4.0, 7.4, "Comenta *1* para contar, o *2* para callar.", None),
]
BOTONES = 0.7
COMENTA = 4.0
APAGON = 6.9                # se apaga el farol
OJOS = 7.25                 # dos puntos amarillos en la oscuridad


def draw(ctx, t):
    ctx.save()
    camara(ctx, t, DURATION, 1.0, 1.1, 0.5, 0.48)
    luz = 1 - smooth(seg(t, APAGON, APAGON + 0.15))
    fondos.pared(ctx, t, farol=(0.5, 0.18), luz=luz)
    fondos.farol(ctx, W * 0.5, H * 0.18 + 30, 1.0, t, luz)
    e = "miedo" if t < 3.0 else ("sospecha" if t < 6.0 else "susto")
    persona(ctx, 540, 760, 1.5, P["tu"], e, mira=(math.sin(t * 1.4) * 0.5, -0.1), t=t, solo_cabeza=True)
    ctx.restore()
    hud.botones(ctx, t, BOTONES)
    hud.llamada_comentar(ctx, t, COMENTA, APAGON)
    if t >= APAGON:                                                     # oscuridad total y dos ojos detrás de ti
        darken(ctx, 0.97 * smooth(seg(t, APAGON, APAGON + 0.1)))
        a = smooth(seg(t, OJOS, OJOS + 0.15))
        for dx in (-34, 34):
            glow(ctx, W / 2 + dx, 700, 70, (1.0, 0.85, 0.35), 0.9 * a)
    marco(ctx, t, DURATION, sale=0.0)
