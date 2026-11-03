"""Llegas al hato: te alcanza la noche y un viejo llanero te jala del brazo."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp
from historias.silbon.dibujo import fondos, hud
from historias.silbon.dibujo.gente import persona, PERSONAJES as P
from historias.silbon.dibujo.escena import camara, marco, sombra

DURATION = 9.0
SUBS = [
    (0.3, 3.7, "Imagina que la *noche* te alcanza en los llanos.", None),
    (4.0, 6.6, "Un viejo llanero te jala del brazo.", None),
    (6.9, 8.9, "«¡Entra, muchacho! ¡Ya!»", "Llanero"),
]
LLANERO_SALE = 4.0       # el llanero sale corriendo del hato
AGARRA = 5.0             # le agarra el brazo
PIE_Y = 1460


def draw(ctx, t):
    hz = H * fondos.HORIZONTE
    ctx.save()
    camara(ctx, t, DURATION, 1.0, 1.14, 0.55, 0.62)
    fondos.llano(ctx, t, luna=(0.20, 0.14), r_luna=60)
    fondos.hato(ctx, W * 0.74, hz + 70, 0.9, 1.0, t)
    # tú caminas hacia el hato; al agarrarte el brazo te frenan y te jalan
    camina = 1 - smooth(seg(t, AGARRA, AGARRA + 0.35))
    x_tu = lerp(150, 520, seg(t, 0.0, AGARRA)) + lerp(0, 120, smooth(seg(t, AGARRA + 0.5, 8.6)))
    x_ll = lerp(1050, x_tu + 215, smooth(seg(t, LLANERO_SALE, AGARRA))) + lerp(0, 120, smooth(seg(t, AGARRA + 0.5, 8.6)))
    y_cab = PIE_Y - 430 * 1.2
    fase = t * 7.0
    e_tu = "normal" if t < AGARRA else "susto" if t < 6.7 else "miedo"
    jalado = smooth(seg(t, AGARRA - 0.1, AGARRA + 0.3))
    brazos_tu = {"d": (lerp(92, 205, jalado), lerp(262, 150, jalado))}
    sombra(ctx, x_tu + 8, PIE_Y + 10, 120)
    persona(ctx, x_tu, y_cab, 1.2, P["tu"], e_tu, mira=(0.6, 0.0), brazos=brazos_tu, fase=fase if camina > 0.01 else None, t=t)
    if t >= LLANERO_SALE:
        sombra(ctx, x_ll + 8, PIE_Y + 10, 120)
        corre = fase * 1.4 if t < AGARRA else None
        agarra = smooth(seg(t, AGARRA - 0.15, AGARRA))
        brazos_ll = {"i": (lerp(-92, -60, agarra), lerp(262, 70, agarra))}
        persona(ctx, x_ll, y_cab, 1.2, P["llanero"], "serio" if t > 6.5 else "normal", mira=(-1.0, 0.0),
                brazos=brazos_ll, fase=corre, t=t)
    ctx.restore()
    hud.caja_hud(ctx, "NOCHE 1 · 7:00 PM · HATO LA ESPERANZA", t, 0.2, 5.2)
    marco(ctx, t, DURATION)
