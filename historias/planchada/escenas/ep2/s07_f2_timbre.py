"""Ep2 escena 7 — Rafa tocó el timbre: primer plano del botón rojo y la luz roja sobre la puerta. Ella lo miró… y bajó la mano."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera_center, vignette, darken, glow, fill_screen
from historias.planchada.dibujo import cuarto, personajes, objetos
from historias.planchada.dibujo.paleta import fluo_brillo, degradado_v

DURATION = 6.0
SUBS = [
    (0.2, 2.4, "Rafa tocó el timbre.", None),
    (2.6, 5.8, "Ella lo miró… y bajó la mano.", None),
]
PULSOS = [0.9, 1.7]       # dos pulsaciones: zumbador en el pasillo (la mezcla)
CORTE = 2.3               # del primer plano del botón al cuarto con la luz roja


def draw(ctx, t):
    if t < CORTE:
        fill_screen(ctx, (0.02, 0.04, 0.05))
        degradado_v(ctx, 0, 0, W, H, (0.03, 0.06, 0.07), (0.07, 0.14, 0.16))
        pres = max([math.exp(-(t - p) * 7) for p in PULSOS if p <= t] or [0.0])
        ctx.save()
        ctx.translate(540 + (0.8 if pres > 0.3 else 0), 880)
        objetos.timbre(ctx, 0, 0, 1.55, presionado=min(1.0, pres * 1.4))
        ctx.restore()
        glow(ctx, 540, 900, 900, (1.0, 0.1, 0.1), 0.35 * pres)
    else:
        u = t - CORTE
        ctx.save()
        cuarto.cam(ctx, lerp(1.25, 1.35, smooth(seg(u, 0, 3.7))), lerp(520, 560, smooth(seg(u, 0, 3.7))), 830)
        luz = 0.5 + 0.5 * math.sin(u * 7) ** 2
        cuarto.cuarto(ctx, t, fluo=0.45 + 0.4 * fluo_brillo(t, 31, "inestable"), hora=(3, 0), segundero=0, ventana=0.3, turno="dormida",
                      lampara_roja=luz, seed=3)
        personajes.rafa_cama(ctx, *cuarto.CABEZA, 1.0, t, ojos="abiertos", mira=(1.0, -0.2), boca="cerrada", rubor=0.5, sudor=0.8)
        baja = smooth(seg(u, 1.9, 3.1))
        personajes.eulalia(ctx, 560, 1230, 1.0, t, pose="ofrece", cara=0.0, halo=1.0, inclina=0.2 * (1 - baja), sonrisa=0.0,
                           k_brazo=1 - baja, pastilla=True)
        ctx.restore()
    vignette(ctx, 0.72)
    darken(ctx, 1 - smooth(seg(t, 0, 0.2)))
    darken(ctx, smooth(seg(t, DURATION - 0.25, DURATION)))
