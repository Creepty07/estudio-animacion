"""Escena 4 — Flashback de día: Don Celso corre a pedradas a los perros de su calle. Menos a uno."""
import math
from motor.config import W, H, ROJIZO, ACENTO
from motor.primitives import seg, smooth, ease_out, lerp, camera, circle, line, darken, vignette
from motor.kit import particles
from historias.rio_perros.dibujo import calle, celso as C, perros

DURATION = 7.8
SUBS = [
    (0.5, 4.2, "Don Celso apedreaba a todos los perros de su calle.", None),
    (4.9, 7.4, "A todos... menos a uno.", None),
]
TIROS = (1.5, 2.2, 2.9)                       # instante en que suelta cada piedra
HUYEN = tuple(a + 0.12 for a in TIROS)        # cada perro sale corriendo
CACHORRO_SALE = 5.2                           # el cachorro rojizo se asoma detrás del barril
FEET = calle.SUELO + 65
CELSO_X = 700
_PERROS = ((430, (0.60, 0.50, 0.38)), (280, (0.38, 0.33, 0.30)), (130, (0.74, 0.68, 0.58)))


def _brazo(t):
    ang = 0.15
    for T in TIROS:
        if T - 0.40 <= t < T - 0.05:
            ang = lerp(0.2, -1.5, smooth(seg(t, T - 0.40, T - 0.05)))
        elif T - 0.05 <= t < T + 0.15:
            ang = lerp(-1.5, 2.4, ease_out(seg(t, T - 0.05, T + 0.15)))
        elif T + 0.15 <= t < T + 0.70:
            ang = lerp(2.4, 0.15, smooth(seg(t, T + 0.15, T + 0.70)))
    return ang


def _tiene_piedra(t):
    return any(T - 0.40 <= t < T + 0.10 for T in TIROS)


def _perro_x(i, t):
    x0 = _PERROS[i][0]
    f = HUYEN[i]
    if t < f:
        return x0, 1, 0.0
    d = t - f
    return x0 - 520 * d - 420 * d * d, -1, 3.4


def draw(ctx, t):
    ctx.save()
    camera(ctx, lerp(1.0, 1.07, smooth(seg(t, 0, DURATION))), W * 0.55, H * 0.62)
    calle.fondo(ctx, t, noche=False)
    # perros callejeros
    for i, (x0, color) in enumerate(_PERROS):
        x, d, paso = _perro_x(i, t)
        if x < -260:
            continue
        cab = -0.55 + 0.25 * math.sin(t * 1.7 + i) if t < HUYEN[i] else 0.2
        perros.perro(ctx, x, FEET + 8 * i, 0.95, color, dir=d, t=t, paso=paso, cabeza=cab, orejas=0.5, cola=0.1)
    # Don Celso
    C.celso(ctx, CELSO_X, FEET + 6, 1.25, dir=-1, brazo_der=_brazo(t), brazo_izq=-0.2, piedra=_tiene_piedra(t), sombra=0.28)
    # piedras en el aire y polvo donde caen
    for i, T in enumerate(TIROS):
        u = seg(t, T + 0.08, T + 0.55)
        x1 = _PERROS[i][0] + 40 - 100
        if 0 < u < 1:
            x = lerp(CELSO_X - 50, x1, u)
            y = lerp(910, FEET + 40, u) - 210 * math.sin(math.pi * u) * (1 - 0.3 * u)
            line(ctx, x + 36, y + 6, x, y, 5, (0.4, 0.38, 0.35), 0.4)
            circle(ctx, x, y, 11, (0.42, 0.40, 0.38))
        v = seg(t, T + 0.55, T + 1.2)
        if 0 < v < 1:
            for k in range(6):
                circle(ctx, x1 + (k - 2.5) * 14 * (0.4 + v), FEET + 36 - 36 * v * (0.5 + 0.1 * k), 10 + 24 * v, (0.75, 0.62, 0.45), 0.35 * (1 - v))
    # el cachorro rojizo sale de detrás del barril
    if t > CACHORRO_SALE:
        u = ease_out(seg(t, CACHORRO_SALE, CACHORRO_SALE + 1.8))
        perros.perro(ctx, lerp(1020, 905, u), FEET + 22, 0.62, ROJIZO, dir=-1, t=t, paso=0.8 if u < 0.98 else 0.0,
                     cabeza=0.15, orejas=1.3, flaco=0.8, cola=0.4, rim=(1.0, 0.8, 0.5))
    calle.barril(ctx, False)
    ctx.restore()
    particles(ctx, t, (1.0, 0.85, 0.55), n=26, seed=6, rise=18, size=(1.2, 3.0), alpha=0.5)
    vignette(ctx, 0.55)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.5)))
    darken(ctx, smooth(seg(t, DURATION - 0.4, DURATION)))
