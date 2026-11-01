"""Escena 2 — Una vela se apaga sola ("Todos... menos una"), negro, el grito y el título."""
import math
from motor.config import W, H, ACENTO, LLAMA
from motor.primitives import seg, smooth, ease_out, lerp, glow, circle, fill_screen, vignette, darken, src
from motor.kit import title_card, particles
from historias.tumba_llorona.dibujo import velas, flores

DURATION = 4.3
SUBS = [
    (0.0, 1.5, "Todos... menos una.", None),
    (1.6, 4.1, "¡Aaay, mis hijos!", "LLORONA"),
]
APAGA = 1.05          # la llama se rinde justo en "una"
NEGRO = 1.45          # todo queda a oscuras
TITULO = 1.95         # entra el título (después del grito)
VELA_Y, VELA_S = H * 0.66, 2.7


def _vela(ctx, t):
    caida = smooth(seg(t, APAGA, APAGA + 0.35))
    inten = 1 - caida
    cx = W / 2
    # bokeh lejano: las velas del camino desenfocadas
    for i, (dx, dy, r) in enumerate(((-300, -330, 70), (260, -420, 50), (-150, -560, 40), (330, -250, 60), (60, -700, 34))):
        glow(ctx, cx + dx, VELA_Y + dy, r * 2.2, (1.0, 0.6, 0.2), 0.22 * inten)
    # pétalos caídos junto a la vela
    for i, dx in enumerate((-190, -120, 150, 210, 70)):
        flores.petalo(ctx, cx + dx, VELA_Y + 6 + (i % 2) * 8, 22 + (i % 3) * 5, 0.5 * i, (1.0, 0.5, 0.05), 0.85 * (0.35 + 0.65 * inten))
    velas.cuerpo(ctx, cx, VELA_Y, VELA_S)
    sway = 0.9 * math.sin(seg(t, APAGA - 0.25, APAGA + 0.2) * math.pi) * (1 - caida)
    velas.llama(ctx, cx, VELA_Y, VELA_S, t, seed=3, intensidad=inten, luz=260, inclinar=sway)
    velas.humo(ctx, cx, VELA_Y - 94 * VELA_S, APAGA + 0.25, t, VELA_S * 0.7, 2.0)
    # luz fría residual de la luna sobre la cera
    glow(ctx, cx + 120, VELA_Y - 160, 260, (0.45, 0.6, 1.0), 0.07 * (1 - inten))


def draw(ctx, t):
    if t < NEGRO:
        fill_screen(ctx, (0.012, 0.016, 0.03))
        _vela(ctx, t)
        particles(ctx, t, (1.0, 0.7, 0.3), n=14, seed=21, rise=20, alpha=0.7 * (1 - smooth(seg(t, APAGA, APAGA + 0.4))))
        vignette(ctx, 0.7)
        darken(ctx, 1 - smooth(seg(t, 0.0, 0.3)))
        darken(ctx, smooth(seg(t, NEGRO - 0.35, NEGRO)))
    elif t < TITULO:
        fill_screen(ctx, (0.0, 0.0, 0.0))
    else:
        tt = t - TITULO
        title_card(ctx, tt, ["LA TUMBA", "DE LA LLORONA"], kicker="LEYENDA MEXICANA", accent=ACENTO)
        particles(ctx, tt, ACENTO, n=22, seed=5, rise=18, size=(1.2, 2.8), alpha=0.7)
        vignette(ctx, 0.6)
        darken(ctx, smooth(seg(t, DURATION - 0.3, DURATION)))
