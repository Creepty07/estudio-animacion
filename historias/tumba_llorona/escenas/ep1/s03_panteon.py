"""Escena 3 — El panteón de noche, junto al canal. Tomás y su abuela velan al abuelo."""
import math
from motor.config import W, H, LLAMA
from motor.primitives import seg, smooth, lerp, camera_center, vignette, darken
from motor.kit import particles
from historias.tumba_llorona.dibujo import panteon, personas

DURATION = 4.55
SUBS = [
    (0.2, 2.2, "Esa noche, Tomás veló a su abuelo", None),
    (2.5, 4.4, "en el panteón, junto al canal.", None),
]
ZOOM = 1.25
# la cámara se acerca a la tumba de la familia sin salirse del cuadro (el centro se limita a lo visible)
CX_MAX = W - W / (2 * ZOOM)
CY_MAX = H - H / (2 * ZOOM)


def draw(ctx, t):
    k = smooth(seg(t, 0, DURATION))
    fam = panteon.FAMILIA
    ctx.save()
    camera_center(ctx, lerp(1.0, ZOOM, k), lerp(W / 2, min(fam["x"] - 60, CX_MAX), k),
                  lerp(H * 0.5, min(fam["y"] - 40, CY_MAX), k))
    panteon.fondo(ctx, t)
    panteon.luces(ctx, t)
    luces = [(fam["x"], fam["y"] - 60, 420, LLAMA, 0.45)]
    bx, by = fam["x"], fam["y"] + 105
    respira = 1 + 0.006 * math.sin(t * 1.6)
    personas.abuela(ctx, bx - 70, by + 6, 0.62 * respira, luces=luces)
    personas.tomas(ctx, bx + 50, by + 10, 0.56, "pie", luces=luces)
    ctx.restore()
    particles(ctx, t, (1.0, 0.7, 0.3), n=20, seed=14, rise=22, alpha=0.7)
    vignette(ctx, 0.65)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.3)))
