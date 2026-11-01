"""Vista del canal de frente: agua ancha, ahuejotes en ambas orillas y la luna reflejada (escena 7)."""
import random
from motor import config
from motor.primitives import src
from motor.layers import paint_layer
from historias.tumba_llorona.dibujo import cielo, paisaje

HORIZ = 0.40
ORILLA_Y = 0.615        # donde empieza la tierra del primer plano


def _base(ctx):
    W, H = config.W, config.H
    paisaje.agua(ctx, H * HORIZ, H, 1.1)
    r = random.Random(61)
    for i in range(9):                                            # orilla lejana
        paisaje.ahuejote(ctx, (i + 0.5) / 9 * W + r.uniform(-25, 25), H * HORIZ + 8, 0.42 + 0.22 * r.random(), seed=i)
    ctx.rectangle(0, H * HORIZ, W, 12)
    src(ctx, (0.012, 0.025, 0.045))
    ctx.fill()
    for lado, x in ((-1, 90), (1, W - 70)):                       # ahuejotes grandes en primer plano, a los lados
        paisaje.ahuejote(ctx, x, H * 0.70, 1.0, seed=70 + lado)
    cielo.gradiente_vertical(ctx, [(0, (0.025, 0.03, 0.045)), (1, (0.008, 0.01, 0.02))], H * ORILLA_Y, H)
    ctx.move_to(0, H * ORILLA_Y)                                  # borde de tierra irregular
    for x in range(0, W + 40, 40):
        ctx.line_to(x, H * ORILLA_Y - 8 + 10 * ((x // 40) % 3))
    ctx.line_to(W, H * ORILLA_Y + 20)
    ctx.line_to(0, H * ORILLA_Y + 20)
    ctx.close_path()
    src(ctx, (0.03, 0.035, 0.05))
    ctx.fill()
    for i in range(8):
        paisaje.tules(ctx, (i + 0.5) / 8 * W, H * ORILLA_Y + 14, 1.0, seed=90 + i, n=7)


def dibujar(ctx, t, niebla=1.0):
    from motor.kit import fog
    W, H = config.W, config.H
    cielo.noche(ctx, t, horizonte=HORIZ + 0.02, luna_xy=(0.62, 0.17), r_luna=74, n_estrellas=70)
    paint_layer(ctx, "canal_vista", _base)
    paisaje.reflejo_luna(ctx, t, W * 0.62, H * HORIZ + 8, H * ORILLA_Y - 20, brillo=1.1)
    fog(ctx, t, (0.55, 0.66, 0.86), 0.16 * niebla, H * 0.36, H * 0.5, seed=12, speed=8)
    fog(ctx, t, (0.5, 0.62, 0.84), 0.12 * niebla, H * 0.5, H * 0.62, seed=19, speed=12)
