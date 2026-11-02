"""Estela de piedra con una cabeza de perro tallada (glifo de diseño propio, inspirado en el lugar de los perros)."""
import math
from motor.config import ACENTO
from motor.primitives import src, line, glow, rrect, TAU, mix


def _cabeza(ctx, s, rgb, a):
    """Cabeza de perro de perfil hecha con trazos rectos y curvas: oreja en punta, hocico largo, ojo y tres muescas."""
    pts = [(-34, 30), (-40, -14), (-28, -52), (-12, -20), (6, -22), (40, -4), (62, -4), (62, 12), (40, 18),
           (24, 34), (4, 44), (-22, 44)]
    ctx.move_to(*[v * s for v in pts[0]])
    for p in pts[1:]:
        ctx.line_to(p[0] * s, p[1] * s)
    ctx.close_path()
    ctx.set_line_width(5.5 * s)
    ctx.set_line_join(1)
    src(ctx, rgb, a)
    ctx.stroke()
    ctx.arc(14 * s, 2 * s, 5.5 * s, 0, TAU)
    src(ctx, rgb, a)
    ctx.fill()
    for i in range(3):                                                         # muescas del cuello
        line(ctx, (-20 + i * 12) * s, 52 * s, (-20 + i * 12) * s, 66 * s, 4.2 * s, rgb, a)
    ctx.arc(0, 0, 92 * s, 0, TAU)                                              # disco
    ctx.set_line_width(3.6 * s)
    src(ctx, rgb, a * 0.8)
    ctx.stroke()


def estela(ctx, x, y, s, t, brillo=1.0):
    """(x, y) = base de la piedra. Mide ~340*s de alto. El glifo palpita como brasa."""
    ancho, alto = 190 * s, 340 * s
    rrect(ctx, x - ancho / 2, y - alto, ancho, alto + 4, 60 * s)
    src(ctx, (0.08, 0.11, 0.13))
    ctx.fill()
    rrect(ctx, x - ancho / 2 + ancho * 0.62, y - alto + 20, ancho * 0.38 - 6, alto - 16, 50 * s)
    src(ctx, (0, 0, 0), 0.30)
    ctx.fill()
    pulso = 0.78 + 0.22 * math.sin(t * 2.2)
    ctx.save()
    ctx.translate(x, y - alto * 0.55)
    glow(ctx, 0, 0, 150 * s, ACENTO, 0.30 * pulso * brillo)
    _cabeza(ctx, s * 0.95, mix(ACENTO, (1, 0.9, 0.7), 0.25), 0.9 * pulso * brillo)
    ctx.restore()
