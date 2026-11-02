"""Ep2 escena 1 — Gancho: la mano de la enfermera con la pastilla, en primer plano. "1, 2 o 3. Esto le pasó a Rafa."."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, vignette, darken, fill_screen, glow
from motor.kit import glitch_text, particles
from historias.planchada.dibujo import objetos
from historias.planchada.dibujo.paleta import degradado_v, FLUO

DURATION = 4.0
SUBS = []
SUSTO = 0.2                          # golpe + zumbido de fluorescente
T1 = (0.2, 1.8)                      # "1, 2 o 3."
T2 = (2.0, 3.8)                      # "Esto le pasó a Rafa."


def draw(ctx, t):
    fill_screen(ctx, (0.012, 0.03, 0.04))
    degradado_v(ctx, 0, 0, W, H, (0.02, 0.05, 0.06), (0.05, 0.12, 0.14))
    glow(ctx, W / 2, 820, 800, FLUO, 0.15)
    ctx.save()
    ctx.translate(0, 8 * math.sin(t * 2.0))
    objetos.mano_pastilla(ctx, 620, 860, 1.5, t, brillo=1.0 + 0.2 * math.sin(t * 5))
    ctx.restore()
    particles(ctx, t, (0.7, 0.95, 1.0), n=16, seed=9, rise=10, size=(1.0, 2.2), alpha=0.5)
    a1 = smooth(seg(t, T1[0], T1[0] + 0.1)) * (1 - smooth(seg(t, T1[1] - 0.1, T1[1])))
    a2 = smooth(seg(t, T2[0], T2[0] + 0.15)) * (1 - smooth(seg(t, T2[1] - 0.15, T2[1])))
    glitch_text(ctx, "1, 2 o 3.", W / 2, 400, 140, a1, 1 - smooth(seg(t, T1[0], T1[0] + 0.7)))
    glitch_text(ctx, "ESTO LE PASÓ", W / 2, 360, 88, a2, 1 - smooth(seg(t, T2[0], T2[0] + 0.6)) * 0.9)
    glitch_text(ctx, "A RAFA.", W / 2, 462, 88, a2, 1 - smooth(seg(t, T2[0], T2[0] + 0.6)) * 0.9)
    vignette(ctx, 0.7)
    darken(ctx, smooth(seg(t, DURATION - 0.15, DURATION)))
