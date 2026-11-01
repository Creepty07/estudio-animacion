"""Escena 5 — La abuela, iluminada desde abajo por una vela, le advierte a Tomás: esa tumba no se toca."""
import math
from motor.config import W, H, LLAMA, FANTASMA
from motor.primitives import seg, smooth, lerp, camera, vignette, darken, glow, fill_screen
from historias.tumba_llorona.dibujo import personas, velas

DURATION = 5.95
SUBS = [
    (0.2, 2.5, "Su abuela le advirtió: esa no se toca.", None),
    (2.55, 5.9, "Es de la Llorona. Está vacía... porque ella sigue buscando.", None),
]
HABLA = [(0.25, 2.3), (2.65, 5.7)]          # momentos aproximados en que mueve la boca
LLORONA = 3.0                               # "Es de la Llorona": la vela se achica
CARA = (W * 0.56, H * 0.37, 1.3)
VELA = (W * 0.40, H * 0.585, 1.3)           # base de la vela y escala


def _boca(t):
    for a, b in HABLA:
        if a <= t <= b:
            env = 0.55 + 0.45 * math.sin(t * 5.1)
            return max(0.0, abs(math.sin(t * 13.0)) * env)
    return 0.0


def draw(ctx, t):
    fill_screen(ctx, (0.012, 0.018, 0.034))
    ctx.save()
    camera(ctx, lerp(1.0, 1.07, smooth(seg(t, 0, DURATION))), CARA[0], CARA[1])
    cx, cy, s = CARA
    vx, vy, vs = VELA
    flame_y = vy - 94 * vs
    susto = smooth(seg(t, LLORONA, LLORONA + 0.7))
    flick = 0.85 + 0.15 * math.sin(t * 11) * math.sin(t * 3.3)
    fuerza = (1 - 0.5 * susto) * flick
    parpadeo = max(0.0, math.sin(t * 1.9 + 0.5) - 0.97) * 30                # parpadeo lento y raro
    personas.abuela_rostro(ctx, cx, cy, s, t, boca=_boca(t), luz=((vx - cx) / s, (flame_y - cy) / s),
                           fuerza=fuerza, parpadeo=min(1.0, parpadeo))
    glow(ctx, W * 0.95, H * 0.28, 620, (0.45, 0.6, 1.0), 0.20 * susto)       # luz fría que se cuela con "Llorona"
    luces = [(vx, flame_y, 560, LLAMA, 0.30 * fuerza), (-120, H * 0.30, 640, (0.45, 0.6, 1.0), 0.30)]
    personas.tomas_hombro(ctx, 30, H * 0.40, 1.0, luces=luces)
    velas.cuerpo(ctx, vx, vy, vs, (0.78, 0.72, 0.60))
    velas.llama(ctx, vx, vy, vs, t, seed=5, intensidad=1 - 0.55 * susto, luz=340, fuerza=0.5)
    ctx.restore()
    vignette(ctx, 0.75)
    darken(ctx, 1 - smooth(seg(t, 0, 0.3)))
    darken(ctx, smooth(seg(t, DURATION - 0.25, DURATION)))
