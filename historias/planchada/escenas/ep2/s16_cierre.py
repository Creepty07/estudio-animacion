"""Ep2 escena 16 — Tarjeta de cierre: la cofia sobre una silla vacía, en la penumbra. ¿Qué final elegiste? Comenta 1, 2 o 3."""
import math
from motor import config
from motor.config import W, H, ACENTO
from motor.primitives import seg, smooth, vignette, darken, glow, fill_screen, font, src, text_center, circle
from motor.kit import glitch_text, candle, fit_size
from historias.planchada.dibujo import objetos
from historias.planchada.dibujo.paleta import degradado_v, fluo_brillo, tubo_fluo, FLUO

DURATION = 6.2
SUBS = []
APAGA = 6.0              # el fluorescente parpadea y se apaga; tinnitus final
T1 = (0.2, 2.8)          # "¿Tú le habrías preguntado su nombre?"
T2 = (3.0, 6.0)          # "¿Qué final elegiste? Comenta 1, 2 o 3."


def draw(ctx, t):
    fill_screen(ctx, (0.012, 0.03, 0.04))
    b = fluo_brillo(t, 51, "inestable") if t < APAGA - 0.7 else (0.5 * fluo_brillo(t, 52, "inestable") if t < APAGA else 0.0)
    degradado_v(ctx, 0, 0, W, H, (0.02, 0.05, 0.06), (0.04, 0.09, 0.10))
    tubo_fluo(ctx, 270, 70, 540, b, 18)
    glow(ctx, W / 2, 900, 800, FLUO, 0.20 * b)
    objetos.silla(ctx, 540, 900, 1.15)
    objetos.cofia(ctx, 540, 820, 1.0, 0.05)
    a1 = smooth(seg(t, T1[0], T1[0] + 0.3)) * (1 - smooth(seg(t, T1[1] - 0.2, T1[1])))
    a2 = smooth(seg(t, T2[0], T2[0] + 0.3))
    chaos1 = 1 - smooth(seg(t, T1[0], T1[0] + 0.6))
    for i, ln in enumerate(("¿TÚ LE HABRÍAS", "PREGUNTADO SU NOMBRE?")):
        glitch_text(ctx, ln, W / 2, 290 + i * 92, fit_size(ctx, "PREGUNTADO SU NOMBRE?", 800, 80), a1, chaos1 * 0.7)
    glitch_text(ctx, "¿QUÉ FINAL ELEGISTE?", W / 2, 300, fit_size(ctx, "¿QUÉ FINAL ELEGISTE?", 800, 80), a2, (1 - smooth(seg(t, T2[0], T2[0] + 0.6))) * 0.6)
    candle(ctx, 540, 1330, 1.2, t, seed=3)                                                   # la vela del perfil
    font(ctx, 80, config.FONT_DISPLAY)
    src(ctx, ACENTO, a2)
    text_center(ctx, "COMENTA 1, 2 O 3", W / 2 - 20, 1120, 2)
    vignette(ctx, 0.7)
    darken(ctx, 1 - smooth(seg(t, 0, 0.25)))
    darken(ctx, smooth(seg(t, DURATION - 0.2, DURATION)))
