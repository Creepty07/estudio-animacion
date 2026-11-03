"""Regla 3: los perros nunca se callan (ladran sin parar; cada ladrido se ve como ondas)."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp
from historias.silbon.dibujo import fondos, props, hud
from historias.silbon.dibujo.animales import perro
from historias.silbon.dibujo.escena import camara, marco, sombra

DURATION = 5.2
SUBS = [(0.4, 4.3, "Regla tres: los *perros* nunca se callan.", None)]
LADRIDOS = (1.3, 1.9, 2.5, 3.1, 3.7)      # ladridos "oíbles": el sonido cae en estos tiempos


def _ladra(t, fase=0.0):
    k = 0.0
    for b in LADRIDOS:
        d = t - (b + fase)
        if 0 <= d < 0.22:
            k = max(k, math.sin(d / 0.22 * math.pi))
    return k


def draw(ctx, t):
    hz = H * fondos.HORIZONTE
    ctx.save()
    camara(ctx, t, DURATION, 1.0, 1.1, 0.5, 0.62)
    fondos.llano(ctx, t, luna=(0.14, 0.2), r_luna=64)
    fondos.hato(ctx, W * 0.5, hz + 40, 0.75, 1.0, t)
    for x, y, s, lado, rgb, fase in ((250, 1250, 1.0, 1, (0.35, 0.25, 0.18), 0.0),
                                      (780, 1300, 1.1, -1, (0.18, 0.15, 0.14), 0.05),
                                      (520, 1420, 0.85, 1, (0.55, 0.42, 0.28), 0.1)):
        sombra(ctx, x, y + 6, 120 * s)
        l = _ladra(t, fase)
        perro(ctx, x, y, s, rgb, lado=lado, ladra=l, t=t)
        if l > 0:
            props.ondas(ctx, x + lado * 150 * s, y - 170 * s, t, lado=lado, n=3, tam=60 * s, ritmo=3.0)
    ctx.restore()
    hud.tarjeta_regla(ctx, 3, t, 0.15, 3.2)
    marco(ctx, t, DURATION)
