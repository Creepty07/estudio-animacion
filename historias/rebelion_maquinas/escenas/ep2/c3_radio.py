"""Final bueno 3/3 — La radio hace clic: una voz pregunta si hay alguien vivo."""
import random
import cairo
from motor.config import W, H
from motor.primitives import seg, smooth, lerp, camera, glow, vignette, darken, fill_screen, line

DURATION = 6.0
CLICK_AT = 0.9
VOICE_AT = 1.7
VOICE_LEN = 1.5    # se ajusta a la duración real de la voz
SUBS = [
    (0.2, 1.5, "Tu radio hace clic…", None),
    (VOICE_AT, VOICE_AT + VOICE_LEN + 0.2, "¿Hay alguien vivo?", "VOZ EN LA RADIO"),
    (4.1, 5.8, "No estás solo.", None),
]
_r = random.Random(17)
BOKEH = [(_r.uniform(0, W), _r.uniform(0, H), _r.uniform(40, 160), _r.choice(
    [(0.3, 0.6, 1.0), (1.0, 0.75, 0.4), (0.6, 0.4, 1.0)]), _r.uniform(0.08, 0.2)) for _ in range(22)]


def draw(ctx, t):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.02, 0.025, 0.07)
    g.add_color_stop_rgb(1, 0.07, 0.04, 0.12)
    ctx.set_source(g)
    ctx.paint()
    for x, y, r, c, a in BOKEH:
        glow(ctx, x, y, r, c, a, cairo.OPERATOR_SCREEN)
    from historias.rebelion_maquinas.dibujo.env_ducto import radio_closeup
    speaking = VOICE_AT <= t <= VOICE_AT + VOICE_LEN
    ctx.save()
    camera(ctx, lerp(1.0, 1.08, smooth(t / DURATION)), 960, 560)
    led = t >= CLICK_AT and (t < VOICE_AT or speaking or (t * 2) % 1 < 0.6)
    radio_closeup(ctx, t, led, t >= CLICK_AT, 1.0 if speaking else 0.08)
    ctx.restore()
    # estática al encender
    if CLICK_AT <= t < CLICK_AT + 0.25:
        r = random.Random(int(t * 30))
        for _ in range(30):
            y = r.uniform(0, H)
            line(ctx, 0, y, W, y, r.uniform(1, 3), (1, 1, 1), 0.08)
    vignette(ctx, 0.7)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.3)))
    darken(ctx, smooth(seg(t, DURATION - 0.35, DURATION)))
