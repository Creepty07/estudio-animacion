"""Capas estáticas: se dibujan una sola vez por proceso y se reutilizan en cada cuadro.

Sirve para fondos pesados (cielo, tumbas, paisajes) que no cambian entre cuadros: el costo de dibujarlos
se paga una vez y cada cuadro solo los pega. Respeta la cámara (zoom/desplazamiento) del contexto actual.
"""
import cairo
from motor import config

_CACHE = {}


def static_layer(key, painter, size=None):
    """Superficie con lo que dibuja painter(ctx); se crea la primera vez que se pide `key`."""
    w, h = size or (config.W, config.H)
    k = (key, w, h)
    if k not in _CACHE:
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
        painter(cairo.Context(surf))
        _CACHE[k] = surf
    return _CACHE[k]


def paint_layer(ctx, key, painter, alpha=1.0, size=None, at=(0, 0)):
    surf = static_layer(key, painter, size)
    ctx.set_source_surface(surf, *at)
    ctx.paint_with_alpha(alpha)
