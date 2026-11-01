"""Escena 8 — Las velas del pasillo se apagan una por una, rumbo al canal, y sube la niebla."""
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera_center, vignette, darken, tint
from motor.kit import particles
from historias.tumba_llorona.dibujo import panteon, velas

DURATION = 4.6
SUBS = [
    (0.2, 2.5, "A medianoche, las velas se apagaron,", None),
    (2.6, 4.5, "una por una, rumbo al canal.", None),
]
PRIMERA = 0.7                       # se apaga la primera vela (la más cercana)
PASO = 0.34                         # tiempo entre una vela y la siguiente
APAGONES = [PRIMERA + i * PASO for i in range(len(panteon.LINEA))]        # una por cada vela, de cerca a lejos
TODAS = 3.95                        # al final también se rinden las velas de las tumbas


def draw(ctx, t):
    k = smooth(seg(t, 0, DURATION))
    inten = {i: 1 - smooth(seg(t, a, a + 0.12)) for i, a in enumerate(APAGONES)}
    ctx.save()
    camera_center(ctx, lerp(1.0, 1.3, k), W / 2, lerp(H * 0.5, H * 0.58, k))
    panteon.fondo(ctx, t)
    panteon.luces(ctx, t, linea=inten, tumbas_on=1 - smooth(seg(t, TODAS, TODAS + 0.5)),
                  niebla=lerp(1.0, 2.6, smooth(seg(t, 0.4, 4.2))))
    for i, a in enumerate(APAGONES):
        x, y, s = panteon.LINEA[i]
        velas.humo(ctx, x, y - 94 * s, a + 0.1, t, s * 0.9, 1.8)
    ctx.restore()
    tint(ctx, (0.8, 0.9, 1.0), smooth(seg(t, 1.5, 4.4)) * 0.8)
    particles(ctx, t, (0.7, 0.85, 1.0), n=14, seed=61, rise=10, size=(1, 2.2), alpha=0.5)
    vignette(ctx, 0.7)
    darken(ctx, 1 - smooth(seg(t, 0, 0.3)))
    darken(ctx, smooth(seg(t, DURATION - 0.3, DURATION)))
