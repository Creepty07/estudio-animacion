"""Regla 1: si el silbido suena cerca, está lejos. Si suena lejos, ya está aquí (el Silbón crece en la ventana)."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, ease_in
from historias.silbon.dibujo import fondos, notas, hud
from historias.silbon.dibujo.silbon import silbon
from historias.silbon.dibujo.gente import persona, PERSONAJES as P
from historias.silbon.dibujo.escena import camara, marco, temblor_en

DURATION = 9.2
SUBS = [
    (0.4, 5.0, "Regla uno: si el silbido suena *cerca*, está lejos.", None),
    (5.4, 8.9, "Si suena *lejos*… ya está aquí.", None),
]
SILBIDO_1 = 1.0          # silbido fuerte (suena "cerca"): la figura se ve diminuta
SILBIDO_2 = 5.6          # silbido débil (suena "lejos")
SUSTO = 7.4              # el Silbón llena la ventana
VX, VY, VW, VH = 120, 520, 840, 560
HZ = fondos.HORIZONTE * H - 260


def _vista(t):
    def v(ctx):
        ctx.save()
        ctx.translate(0, -260)
        fondos.llano(ctx, t, luna=(0.70, 0.30), r_luna=70)
        k = ease_in(seg(t, SUSTO - 0.35, SUSTO))
        s = lerp(0.075, 1.0, k)
        silbon(ctx, W / 2, fondos.HORIZONTE * H + lerp(24, 700, k), s, t, ojos=0.4 + 0.6 * k, luz=1.0)
        ctx.restore()
    return v


def draw(ctx, t):
    ctx.save()
    camara(ctx, t, DURATION, 1.0, 1.08, 0.5, 0.42, temblor=temblor_en(t, SUSTO, 0.6, 16))
    fondos.pared(ctx, t, farol=(0.88, 0.20))
    fondos.farol(ctx, W * 0.88, H * 0.20 + 30, 1.0, t)
    fondos.marco_ventana(ctx, VX, VY, VW, VH, _vista(t))
    # tú, en primer plano, escuchando
    e = "miedo" if t >= SUSTO - 0.1 else "sospecha"
    persona(ctx, 220, 1190, 0.95, P["tu"], e, mira=(0.8, -0.4), t=t, solo_cabeza=True)
    ctx.restore()
    hud.tarjeta_regla(ctx, 1, t, 0.15, 3.0)
    notas.silbido(ctx, t, SILBIDO_1, W / 2, 470, 0.75, dur=1.2, mantener=0.9, alpha=1.0)
    notas.silbido(ctx, t, SILBIDO_2, W / 2, 470, 0.5, dur=1.0, mantener=0.6, alpha=0.5)
    marco(ctx, t, DURATION)
