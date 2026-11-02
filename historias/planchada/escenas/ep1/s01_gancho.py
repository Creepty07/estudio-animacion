"""Escena 1 — Gancho: una enfermera de blanco, inmóvil a contraluz en la puerta entreabierta. "Esta enfermera no trabaja aquí."."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, glow, fill_rrect, vignette, darken, fill_screen, font, src, line
from motor.kit import glitch_text, particles
from historias.planchada.dibujo import personajes
from historias.planchada.dibujo.paleta import degradado_v, fluo_brillo, FLUO, MURO

DURATION = 3.0
SUBS = []                       # el texto del gancho va grande dentro de la escena (zona segura)
SUSTO = 0.2                     # golpe + glitch + entrada del texto (la mezcla usa este tiempo)
TEXTO = (0.2, 2.8)


def draw(ctx, t):
    fill_screen(ctx, (0.015, 0.035, 0.045))
    degradado_v(ctx, 0, 0, W, 1320, (0.03, 0.07, 0.08), (0.06, 0.13, 0.15))
    # puerta entreabierta: hueco con el pasillo iluminado
    px, py, pw, ph = 300, 560, 480, 800
    b = fluo_brillo(t, 11, "parpadea")
    degradado_v(ctx, px, py, pw, ph, (0.22 * b + 0.06, 0.46 * b + 0.10, 0.50 * b + 0.12), (0.34 * b + 0.05, 0.62 * b + 0.10, 0.66 * b + 0.12))
    glow(ctx, px + pw / 2, py + ph * 0.85, 700, FLUO, 0.30 * b)
    personajes.eulalia(ctx, px + pw / 2, py + ph - 30, 0.92, t, pose="pie", cara=0.0, halo=1.2, flota=0.4)
    ctx.set_line_width(26)                                                               # marco y hoja de la puerta
    src(ctx, (0.01, 0.03, 0.04))
    ctx.rectangle(px, py, pw, ph)
    ctx.stroke()
    ctx.move_to(px + pw, py)
    ctx.line_to(px + pw + 150, py - 40)
    ctx.line_to(px + pw + 150, py + ph + 60)
    ctx.line_to(px + pw, py + ph)
    ctx.close_path()
    src(ctx, (0.02, 0.05, 0.06))
    ctx.fill()
    glow(ctx, W / 2, 80, 600, FLUO, 0.10 * b)
    particles(ctx, t, (0.7, 0.95, 1.0), n=18, seed=7, rise=10, size=(1.0, 2.2), alpha=0.5)
    a = smooth(seg(t, TEXTO[0], TEXTO[0] + 0.12)) * (1 - smooth(seg(t, TEXTO[1] - 0.15, TEXTO[1])))
    chaos = 1 - smooth(seg(t, TEXTO[0], TEXTO[0] + 0.8))
    glitch_text(ctx, "ESTA ENFERMERA", W / 2, 330, 98, a, chaos)
    glitch_text(ctx, "NO TRABAJA AQUÍ.", W / 2, 440, 98, a, chaos)
    vignette(ctx, 0.7)
    darken(ctx, smooth(seg(t, DURATION - 0.15, DURATION)))
