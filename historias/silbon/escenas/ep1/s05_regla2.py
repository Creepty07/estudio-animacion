"""Regla 2: nadie bebe aguardiente de noche (la botella se tacha con una X roja)."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp
from historias.silbon.dibujo import fondos, props, hud
from historias.silbon.dibujo.gente import persona, PERSONAJES as P
from historias.silbon.dibujo.escena import camara, marco, sombra

DURATION = 5.4
SUBS = [(0.4, 4.2, "Regla dos: nadie bebe *aguardiente* de noche.", None)]
BOTELLA = 0.9            # la botella entra a escena (golpe seco sobre la mesa)
X_ROJA = 2.5             # se estampa la X (cuando se dice "aguardiente")


def draw(ctx, t):
    ctx.save()
    camara(ctx, t, DURATION, 1.0, 1.1, 0.5, 0.55)
    fondos.pared(ctx, t, farol=(0.14, 0.22))
    fondos.farol(ctx, W * 0.14, H * 0.22 + 30, 1.0, t)
    # mesa
    ctx.new_path()
    ctx.rectangle(120, 1060, 840, 60)
    from historias.silbon.dibujo.caras import relleno_contorno
    from historias.silbon.dibujo import estilo as E
    relleno_contorno(ctx, E.MADERA, 1.0, 8)
    ctx.new_path()
    ctx.rectangle(190, 1120, 50, 220)
    relleno_contorno(ctx, E.MADERA_OSCURA, 1.0, 8)
    ctx.new_path()
    ctx.rectangle(840, 1120, 50, 220)
    relleno_contorno(ctx, E.MADERA_OSCURA, 1.0, 8)
    # botella cae desde arriba y rebota
    k = smooth(seg(t, BOTELLA - 0.25, BOTELLA))
    y_b = lerp(560, 1060, k) - 14 * max(0.0, math.sin(seg(t, BOTELLA, BOTELLA + 0.25) * math.pi))
    props.botella(ctx, 400, y_b, 1.35)
    props.x_roja(ctx, 400, 790, 1.5, seg(t, X_ROJA, X_ROJA + 0.22))
    # Ramiro quiere agarrarla y se arrepiente
    e = "sonrisa" if t < X_ROJA else "sospecha"
    mano = lerp(250, 60, smooth(seg(t, 1.2, 2.2))) if t < X_ROJA else lerp(60, 230, smooth(seg(t, X_ROJA + 0.2, X_ROJA + 0.8)))
    persona(ctx, 780, 760, 1.15, P["ramiro"], e, mira=(-0.9, 0.3), brazos={"i": (-mano, 250)}, t=t, solo_cabeza=False)
    ctx.restore()
    hud.tarjeta_regla(ctx, 2, t, 0.15, 3.2)
    marco(ctx, t, DURATION)
