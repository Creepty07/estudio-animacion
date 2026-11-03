"""Ayudas de cámara y transición comunes a todas las escenas del Silbón."""
import math
from motor import config
from motor.primitives import camera, seg, smooth, lerp, darken, vignette


def camara(ctx, t, dur, z0=1.0, z1=1.1, fx=0.5, fy=0.5, temblor=0.0, desde=0.0):
    """Zoom lento (efecto Ken Burns) hacia (fx, fy) en fracciones de pantalla. temblor = píxeles de sacudida."""
    k = smooth(seg(t, desde, dur))
    W, H = config.W, config.H
    dx = temblor * math.sin(t * 53) if temblor else 0.0
    dy = temblor * math.cos(t * 61) if temblor else 0.0
    camera(ctx, lerp(z0, z1, k), W * fx, H * fy, dx, dy)


def temblor_en(t, t0, dur, fuerza):
    """Sacudida que decae desde t0 (para el momento del susto)."""
    if t < t0 or t > t0 + dur:
        return 0.0
    return fuerza * (1 - (t - t0) / dur)


def marco(ctx, t, dur, entra=0.08, sale=0.08, v=0.55):
    """Viñeta y fundidos muy cortos (cortes casi secos, como en el video de referencia)."""
    vignette(ctx, v)
    if entra:
        darken(ctx, 1 - smooth(seg(t, 0, entra)))
    if sale:
        darken(ctx, smooth(seg(t, dur - sale, dur)))


def sombra(ctx, x, y, rx, ry=None, a=0.4):
    """Sombra ovalada en el piso."""
    from historias.silbon.dibujo.caras import elipse
    elipse(ctx, x, y, rx, ry or rx * 0.22)
    ctx.set_source_rgba(0, 0, 0, a)
    ctx.fill()
