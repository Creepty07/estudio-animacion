"""Algo se sienta junto a la puerta: su sombra con sombrero, un saco que cae y empieza a contar huesos."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, ease_in, glow
from historias.silbon.dibujo import fondos, props, hud, estilo as E
from historias.silbon.dibujo.caras import elipse
from historias.silbon.dibujo.gente import persona, PERSONAJES as P
from historias.silbon.dibujo.escena import camara, marco, temblor_en, sombra

DURATION = 8.0
SUBS = [
    (0.4, 3.2, "Algo se sienta junto a la *puerta*.", None),
    (3.5, 7.9, "Un saco cae… y empieza a *contar huesos*.", None),
]
SOMBRA = 1.5                # aparece la sombra del sombrero bajo la puerta
SACO = 3.5                  # el saco cae
CLICS = (5.0, 5.9, 6.8)     # huesos contados: UNO, DOS, TRES
PISO = 1170


def _sombra_sombrero(ctx, x, y, a):
    ctx.save()
    ctx.translate(x, y)
    elipse(ctx, 0, 0, 170, 36)                                          # ala
    ctx.set_source_rgba(0, 0, 0, 0.88 * a)
    ctx.fill()
    elipse(ctx, 0, -48, 82, 70)                                         # copa
    ctx.set_source_rgba(0, 0, 0, 0.88 * a)
    ctx.fill()
    ctx.restore()


def draw(ctx, t):
    ctx.save()
    camara(ctx, t, DURATION, 1.0, 1.12, 0.5, 0.55, temblor=temblor_en(t, SACO, 0.6, 20))
    fondos.pared(ctx, t, farol=(0.12, 0.22), luz=0.6)
    fondos.puerta_rendija(ctx, 330, 330, 520, 840, 0.05, vista=None, t=t)
    # cuña de luna bajo la puerta y la sombra del sombrero dentro
    a = smooth(seg(t, SOMBRA, SOMBRA + 0.6))
    ctx.new_path()
    ctx.move_to(520, PISO - 20)
    ctx.line_to(660, PISO - 20)
    ctx.line_to(900, PISO + 190)
    ctx.line_to(280, PISO + 190)
    ctx.close_path()
    ctx.set_source_rgba(0.55, 0.72, 1.0, 0.22)
    ctx.fill()
    _sombra_sombrero(ctx, 590 + 6 * math.sin(t * 1.3), PISO + 80, a)
    if t >= SACO:                                                       # el saco golpea el piso y se abre
        k = seg(t, SACO - 0.25, SACO)
        y = lerp(PISO - 350, PISO + 50, ease_in(k))
        ctx.save()
        ctx.translate(430, y)
        elipse(ctx, 0, 0, 110, 90)
        ctx.set_source_rgba(0.06, 0.05, 0.05, 1)
        ctx.fill_preserve()
        ctx.set_line_width(7)
        ctx.set_source_rgb(*E.CONTORNO)
        ctx.stroke()
        ctx.restore()
        for i, c in enumerate(CLICS):                                   # huesos que salen del saco, uno por conteo
            if t >= c - 0.1:
                props.hueso(ctx, 560 + i * 120, PISO + 120 + 8 * i, 0.55, math.radians(10 - 25 * i), 150)
    # tú, atento y quieto
    persona(ctx, 170, 1150, 0.8, P["tu"], "miedo" if t > SACO else "sospecha", mira=(1.0, 0.2), t=t, solo_cabeza=True)
    ctx.restore()
    for palabra, c in zip(("UNO", "DOS", "TRES"), CLICS):
        hud.numero_conteo(ctx, palabra, t, c, W / 2, 560, dur=0.75)
    marco(ctx, t, DURATION)
