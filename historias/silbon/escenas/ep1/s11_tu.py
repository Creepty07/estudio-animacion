"""Solo tú estás despierto: el ojo en la rendija, FALTAN 3→2→1 y el dilema (cuento en voz alta o callo)."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, window
from historias.silbon.dibujo import fondos, props, hud
from historias.silbon.dibujo.gente import persona, en_hamaca, PERSONAJES as P
from historias.silbon.dibujo.silbon import ojo_en_rendija
from historias.silbon.dibujo.escena import camara, marco, temblor_en

DURATION = 10.5
SUBS = [
    (0.4, 2.9, "Solo tú estás *despierto*.", None),
    (3.3, 7.0, "Si cuentas en voz alta, sabrá que lo *oyes*.", None),
    (7.4, 10.4, "Si callas… alguien no *amanece*.", None),
]
OJO = 3.3                   # el ojo aparece en la rendija (golpe)
FALTAN = ((3, 3.6, 5.0), (2, 5.0, 6.3), (1, 6.3, 7.3))   # (huesos, desde, hasta); cada cambio suena a hueso
FIN = 9.0                   # una de las personas dormidas se apaga


def draw(ctx, t):
    ctx.save()
    camara(ctx, t, DURATION, 1.0, 1.1, 0.5, 0.5, temblor=temblor_en(t, OJO, 0.6, 14))
    fondos.pared(ctx, t, farol=(0.12, 0.22), luz=0.55)
    # puerta con rendija a la derecha
    fondos.puerta_rendija(ctx, 640, 420, 340, 560, 0.18, vista=None, t=t)
    abre = smooth(seg(t, OJO, OJO + 0.2))
    ojo_en_rendija(ctx, 810, 700, 0.42, t, abre, math.sin(t * 2) * 0.6)
    # los demás duermen
    en_hamaca(ctx, 150, 640, 0.65, P["abuela"], "duerme", 1, (0.45, 0.3, 0.55), t)
    en_hamaca(ctx, 150, 830, 0.65, P["nina"], "duerme" if t < FIN else "duerme", 1, (0.3, 0.5, 0.6), t + 1)
    props.zzz(ctx, 250, 600, 0.8, t)
    if t < FIN:
        props.zzz(ctx, 250, 790, 0.8, t + 0.4)
    # tú, despierto y con los ojos muy abiertos
    e = "sospecha" if t < OJO else ("susto" if t < 7.4 else "miedo")
    persona(ctx, 330, 1090, 1.15, P["tu"], e, mira=(1.0, -0.2), t=t, solo_cabeza=True)
    if t >= FIN:                                                        # alguien no amanece
        props.x_roja(ctx, 235, 860, 0.9, seg(t, FIN, FIN + 0.2))
    ctx.restore()
    for n, a, b in FALTAN:
        hud.faltan(ctx, n, t, a, b)
    marco(ctx, t, DURATION)
