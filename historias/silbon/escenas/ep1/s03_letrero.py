"""Adentro, un letrero con cuatro reglas: se van escribiendo a medida que se nombran."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp
from historias.silbon.dibujo import fondos, props
from historias.silbon.dibujo.gente import persona, en_hamaca, PERSONAJES as P
from historias.silbon.dibujo.escena import camara, marco

DURATION = 5.2
SUBS = [(0.3, 3.9, "Adentro, un letrero con *cuatro reglas*.", None)]
ESCRIBE = (0.9, 3.5)      # las cuatro líneas se escriben entre estos tiempos


def draw(ctx, t):
    ctx.save()
    camara(ctx, t, DURATION, 1.0, 1.1, 0.5, 0.42)
    fondos.pared(ctx, t, farol=(0.86, 0.22))
    fondos.farol(ctx, W * 0.86, H * 0.22 + 40, 1.1, t)
    reveal = 4.0 * seg(t, *ESCRIBE)
    props.letrero(ctx, W / 2, 590, 760, t, reveal=reveal)
    # gente dormida abajo y tú mirando el letrero
    en_hamaca(ctx, 160, 1035, 0.75, P["abuela"], "duerme", 1, (0.45, 0.3, 0.55), t)
    en_hamaca(ctx, 160, 1150, 0.75, P["nina"], "duerme", 1, (0.3, 0.5, 0.6), t + 1)
    props.zzz(ctx, 230, 990, 0.9, t)
    persona(ctx, 820, 1110, 0.95, P["tu"], "serio", mira=(0.5, -0.8), t=t, solo_cabeza=True)
    ctx.restore()
    marco(ctx, t, DURATION)
