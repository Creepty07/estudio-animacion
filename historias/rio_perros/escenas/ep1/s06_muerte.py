"""Escena 6 — Don Celso muere en su cama: el último aliento y la vela que se apaga."""
from motor.config import W, H, LLAMA
from motor.primitives import seg, smooth, lerp, camera, glow, darken, vignette
from historias.rio_perros.dibujo import cuarto
from historias.tumba_llorona.dibujo import velas

DURATION = 6.0
SUBS = [(0.5, 3.6, "Don Celso murió viejo y solo.", None)]
ULTIMO_ALIENTO = 2.9      # el pecho deja de moverse (exhalación larga)
APAGA = 3.5               # la vela se apaga (soplo)


def draw(ctx, t):
    ctx.save()
    camera(ctx, lerp(1.0, 1.12, smooth(seg(t, 0, DURATION))), W * 0.78, H * 0.58)
    llama = max(0.001, 1.0 - smooth(seg(t, ULTIMO_ALIENTO - 0.2, APAGA))) if t < APAGA else 0.0
    respira = 1.0 - smooth(seg(t, ULTIMO_ALIENTO, ULTIMO_ALIENTO + 0.4))
    cuarto.dibujar(ctx, t, llama=llama if llama > 0 else 0.001, respira=respira)
    if t >= APAGA:
        velas.humo(ctx, cuarto.VELA_X, cuarto.VELA_Y - 110, APAGA, t, s=1.6)
    ctx.restore()
    # al apagarse la vela solo queda la luz fría de la luna por la ventana
    darken(ctx, 0.55 * smooth(seg(t, APAGA - 0.1, APAGA + 0.5)))
    glow(ctx, 270, 500, 620, (0.35, 0.55, 0.95), 0.20 * smooth(seg(t, APAGA, APAGA + 1.0)))
    vignette(ctx, 0.6)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.5)))
    darken(ctx, smooth(seg(t, DURATION - 0.5, DURATION)))
