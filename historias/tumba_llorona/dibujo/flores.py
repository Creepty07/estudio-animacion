"""Cempasúchil: la flor de Día de Muertos, dibujada con anillos de pétalos."""
import math
import random
from motor.primitives import TAU, src

_ANILLOS = [  # (pétalos, escala, color)
    (14, 1.00, (0.93, 0.40, 0.02)),
    (12, 0.80, (1.00, 0.55, 0.05)),
    (9, 0.58, (1.00, 0.70, 0.14)),
    (6, 0.36, (1.00, 0.82, 0.30)),
]


def _ovalo(ctx, x, y, rx, ry, rot, rgb, a=1.0):
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(rot)
    ctx.scale(rx, ry)
    ctx.arc(0, 0, 1, 0, TAU)
    ctx.restore()
    src(ctx, rgb, a)
    ctx.fill()


def cempasuchil(ctx, x, y, r, rot=0.0, seed=0, brillo=1.0, a=1.0):
    """Flor vista de frente. r = radio total; brillo < 1 la oscurece (flores lejanas o en sombra)."""
    rnd = random.Random(seed)
    for n, esc, col in _ANILLOS:
        off = rnd.uniform(0, TAU) + rot
        for i in range(n):
            ang = off + TAU * i / n
            d = r * esc * 0.55
            _ovalo(ctx, x + math.cos(ang) * d, y + math.sin(ang) * d, r * esc * 0.5, r * esc * 0.26, ang,
                   tuple(min(1.0, c * brillo) for c in col), a)
    _ovalo(ctx, x, y, r * 0.13, r * 0.13, 0, tuple(c * brillo for c in (0.75, 0.30, 0.02)), a)


def petalo(ctx, x, y, s, rot=0.0, rgb=(1.0, 0.55, 0.05), a=1.0):
    """Un pétalo suelto (camino de pétalos)."""
    _ovalo(ctx, x, y, s, s * 0.45, rot, rgb, a)


def petalos_en_camino(ctx, x0, x1, y, s, n, seed, brillo=1.0):
    """Esparce n pétalos entre x0 y x1 a la altura y (s = tamaño en esa profundidad)."""
    rnd = random.Random(seed)
    for _ in range(n):
        rgb = rnd.choice([(1.0, 0.55, 0.05), (0.95, 0.42, 0.03), (1.0, 0.72, 0.18)])
        petalo(ctx, rnd.uniform(x0, x1), y + rnd.uniform(-s, s), s * rnd.uniform(0.7, 1.2),
               rnd.uniform(0, math.pi), tuple(c * brillo for c in rgb))
