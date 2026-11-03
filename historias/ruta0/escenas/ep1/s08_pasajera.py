"""Parte 1, escena 8 — Se abre la puerta a una parada negra. Iván se levanta y una mano pálida lo agarra: la pasajera, la primera que se mueve.
«Tú todavía no te bajas aquí.» Susto principal de la parte 1."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, fill_screen
from historias.ruta0.dibujo import interior as I
from historias.ruta0.dibujo.paleta import degradado_v
from historias.ruta0.dibujo.comun import marco

DURATION = 10.0
SUBS = [
    (0.3, 3.0, "El camión se detuvo. Iván se levantó.", None),
    (3.3, 6.0, "Y por primera vez, alguien se movió.", None),
    (6.8, 9.5, "«Tú todavía no te bajas aquí.»", "Pasajera"),
]
SUSTO = 6.3               # golpe + glitch + destello rojo (la mezcla y SUSTOS de historia.py)
PUERTAS = (0.6, 1.2, 9.0)  # se abre, y se cierra en 9.0


def draw(ctx, t):
    if t < 6.3:
        ctx.save()
        giro = smooth(seg(t, 3.4, 5.8))
        I.cam(ctx, lerp(1.4, 2.0, smooth(seg(t, 0, 6.3))), 2020, 990)
        I.fondo(ctx, t, 0.8, 0.0, 1)
        for ax in I.ASIENTOS:
            I.asiento(ctx, ax)
        for ax, tipo in ((1410, "gala"), (1140, "obrero"), (870, "vestido")):
            I.pasajero(ctx, ax, tipo, t)
        I.pasajero(ctx, 1950, "pasajera", t, giro=giro)
        levanta = smooth(seg(t, 0.4, 2.8))
        I.ivan(ctx, 1680 + 120 * levanta, t, y=I.CADERA - 40 * levanta)
        I.chofer(ctx, I.X_CHOFER, t)
        puerta_abierta = smooth(seg(t, *PUERTAS[:2]))
        ctx.save()                                                                                     # el hueco de la puerta: una parada negra con un farol lejano
        ctx.rectangle(I.X_PUERTA - 50, 470, 110, 800)
        ctx.clip()
        ctx.set_source_rgba(0.005, 0.012, 0.025, 0.96 * puerta_abierta)
        ctx.paint()
        from motor.primitives import glow as _g
        _g(ctx, I.X_PUERTA + 10, 760, 140, (0.5, 0.65, 0.8), 0.18 * puerta_abierta)
        ctx.restore()
        ctx.set_line_width(10)
        ctx.set_source_rgba(0.03, 0.035, 0.035, puerta_abierta)
        ctx.rectangle(I.X_PUERTA - 50, 470, 110, 800)
        ctx.stroke()
        ctx.restore()
    elif t < 6.8:
        degradado_v(ctx, 0, 0, W, H, (0.03, 0.04, 0.04), (0.08, 0.09, 0.08))
        I.mano_muneca(ctx, t, 560, 880, 1.15 + 0.03 * math.sin(t * 40), apretar=1.0)
    else:
        degradado_v(ctx, 0, 0, W, H, (0.03, 0.035, 0.04), (0.07, 0.08, 0.08))
        I.cara_pasajera(ctx, t, 540, 800, 1.2 + 0.04 * (t - 6.8))
    marco(ctx, t, DURATION, 0.7, 0.3, 0.3)
