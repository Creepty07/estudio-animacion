"""Regla 4: si caen huesos junto a la puerta, cuéntalos en voz alta (caen tres; se cantan UNO, DOS, TRES)."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, ease_in
from historias.silbon.dibujo import fondos, props, hud
from historias.silbon.dibujo.gente import persona, PERSONAJES as P
from historias.silbon.dibujo.escena import camara, marco, temblor_en, sombra

DURATION = 8.0
SUBS = [
    (0.4, 4.6, "Regla cuatro: si caen *huesos* junto a la puerta…", None),
    (4.9, 7.6, "cuéntalos en *voz alta*.", None),
]
CAEN = (2.6, 3.3, 3.9)           # cada hueso golpea el piso
CUENTA = (5.2, 6.0, 6.8)         # UNO, DOS, TRES
PISO = 1170


def draw(ctx, t):
    ctx.save()
    camara(ctx, t, DURATION, 1.0, 1.1, 0.5, 0.5, temblor=max(temblor_en(t, c, 0.25, 6) for c in CAEN))
    fondos.pared(ctx, t, farol=(0.90, 0.22))
    fondos.farol(ctx, W * 0.90, H * 0.22 + 30, 0.9, t)
    fondos.puerta_rendija(ctx, 330, 330, 520, 840, 0.05, vista=None, t=t)
    # franja de luna que se cuela bajo la puerta
    ctx.new_path()
    ctx.rectangle(330, PISO - 20, 520, 20)
    ctx.set_source_rgba(0.6, 0.75, 1.0, 0.35)
    ctx.fill()
    # huesos que caen (uno por golpe)
    pos = ((470, 8, 150), (600, -12, 120), (730, 20, 160))
    for i, (c, (x, giro, largo)) in enumerate(zip(CAEN, pos)):
        k = seg(t, c - 0.3, c)
        if k <= 0:
            continue
        y = lerp(300, PISO + 40, ease_in(k)) - 22 * max(0.0, math.sin(seg(t, c, c + 0.3) * math.pi))
        sombra(ctx, x, PISO + 56, 80, 14, 0.35)
        props.hueso(ctx, x, y, 0.8, math.radians(giro + 90 * (1 - k)), largo)
    # el llanero pide silencio y luego señala los huesos
    e = "shh" if t < 4.9 else "serio"
    persona(ctx, 175, 700, 0.95, P["llanero"], e, mira=(1.0, 0.3), t=t,
            brazos={"d": (60, 40)} if t < 4.9 else None)
    ctx.restore()
    hud.tarjeta_regla(ctx, 4, t, 0.15, 3.2)
    for palabra, c in zip(("UNO", "DOS", "TRES"), CUENTA):
        hud.numero_conteo(ctx, palabra, t, c, W / 2, 560, dur=0.75)
    marco(ctx, t, DURATION)
