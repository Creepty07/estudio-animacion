"""Escena 11 — "El llanto se detuvo." Silencio, el susurro y la mano blanca en el hombro de Tomás. Corte a negro."""
import math
import random
from motor.config import W, H, FANTASMA
from motor.primitives import seg, smooth, ease_out, lerp, camera_center, vignette, darken, glow, tint, fill_screen
from motor.kit import particles
from historias.tumba_llorona.dibujo import fondo_tumba, tumbas, personas, flores, llorona

DURATION = 5.45
SUBS = [
    (0.2, 1.7, "El llanto se detuvo.", None),
    (2.4, 4.8, "¿Eres tú... mi niño?", "LLORONA (SUSURRO)"),
]
GIRA = (1.5, 3.0)                    # la cabeza gira despacio hacia Tomás, en el silencio
MANO = (2.9, 3.7)                    # la mano sube y se posa en su hombro
TOQUE = MANO[1]
NEGRO = 4.4                          # corte seco a negro
TUMBA = (W * 0.50, H * 0.52, 0.72)
TOMAS = (W * 0.30, H * 0.645, 1.45)
FIG = (W * 0.72, H * 0.62, 1.0)


def draw(ctx, t):
    if t >= NEGRO:
        fill_screen(ctx, (0, 0, 0))
        return
    r = random.Random(int(t * 30))
    sobresalto = math.exp(-(t - TOQUE) * 9) if t >= TOQUE else 0.0
    ctx.save()
    camera_center(ctx, lerp(1.0, 1.1, smooth(seg(t, 0, NEGRO))), W / 2, H * 0.55)
    fondo_tumba.fondo(ctx, t, bokeh=0.0, niebla=1.5)
    tx, ty, ts = TUMBA
    tumbas.tumba_sin_nombre(ctx, tx, ty, ts, tono_frio=0.9)
    flores.cempasuchil(ctx, tx + 70 * ts, ty - 28 * ts, 34 * ts, seed=5)       # la flor que dejó Tomás
    glow(ctx, tx + 70 * ts, ty - 28 * ts, 160 * ts, (1.0, 0.55, 0.1), 0.35)
    fx, fy, fs = FIG
    giro = lerp(0.9, -0.9, smooth(seg(t, *GIRA)))
    # la mano va del costado al hombro de Tomás (que se encuentra más a la izquierda)
    qx, qy, qs = TOMAS
    hombro = (qx + 62 * qs, qy - 190 * qs + 8 * sobresalto)
    objetivo = ((hombro[0] - fx) / fs, (hombro[1] - fy) / fs)
    k = ease_out(seg(t, *MANO))
    mano_xy = (lerp(-74, objetivo[0], k), lerp(-196, objetivo[1], k))
    alpha = smooth(seg(t, 0.0, 0.5))
    llorona.de_pie(ctx, fx, fy, fs, t, brazos=0.0, alpha=alpha, giro=giro, manos={"izq": mano_xy}, aura=1.1)
    luces = [(fx, fy - 300, 700, FANTASMA, 0.42), (W * 0.3, H * 0.2, 800, (0.5, 0.65, 1.0), 0.25)]
    personas.tomas(ctx, qx, qy - 6 * sobresalto, qs, "arrodillado", luces=luces)
    glow(ctx, hombro[0] + 30, hombro[1], 220, FANTASMA, 0.28 * smooth(seg(t, MANO[0] + 0.3, TOQUE)))
    ctx.restore()
    particles(ctx, t, (0.75, 0.88, 1.0), n=16, seed=91, rise=12, size=(1, 2.2), alpha=0.5)
    tint(ctx, (0.85, 0.92, 1.0), 0.8)
    vignette(ctx, 0.8)
    darken(ctx, 1 - smooth(seg(t, 0, 0.3)))
    if sobresalto > 0.2:
        fill_screen(ctx, (0.85, 0.92, 1.0), 0.12 * sobresalto)
