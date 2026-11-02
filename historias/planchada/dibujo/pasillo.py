"""Pasillo largo del hospital en perspectiva de un punto. Sirve para 'las luces se apagan' y 'la silueta se aleja entre las puertas'."""
import math
import cairo
from motor.primitives import src, line, glow, fill_poly, fill_rrect, mix, clamp, smooth, seg
from historias.planchada.dibujo.paleta import degradado_v, FLUO, HALO, MURO, PISO, ovalo
from historias.planchada.dibujo import personajes

VP = (540, 820)             # punto de fuga
N_PUERTAS = 6


def _k(z):
    return 1.0 / (1.0 + 4.0 * z)


def _p(z, lado, v):
    """Punto del mundo del pasillo: z 0 (cerca) … 1 (lejos); lado -1 / 0 / 1; v 0 piso … 1 techo."""
    k = _k(z)
    x = VP[0] + lado * 660 * k
    y = VP[1] + 780 * k - v * 1560 * k
    return x, y


def pasillo(ctx, t, luces=None, figura=None, puertas_luz=None, brillo=1.0, fondo_luz=0.6, n_luces=7):
    """luces: lista de brillos 0..1 de los fluorescentes (cerca → lejos); None = todas encendidas.
    figura: (z, alpha) de la silueta blanca (de espaldas); puertas_luz: lista de 0..1 por puerta."""
    luces = luces if luces is not None else [1.0] * n_luces
    puertas_luz = puertas_luz or [0.0] * N_PUERTAS
    avg = sum(luces) / len(luces)
    amb = (0.3 + 0.7 * avg) * brillo
    # techo, piso y paredes
    for pts, c0 in (
        ([_p(0, -1, 1), _p(0, 1, 1), _p(1, 1, 1), _p(1, -1, 1)], (0.04, 0.09, 0.10)),
        ([_p(0, -1, 0), _p(0, 1, 0), _p(1, 1, 0), _p(1, -1, 0)], (0.05, 0.10, 0.11)),
        ([_p(0, -1, 0), _p(0, -1, 1), _p(1, -1, 1), _p(1, -1, 0)], (0.07, 0.16, 0.18)),
        ([_p(0, 1, 0), _p(0, 1, 1), _p(1, 1, 1), _p(1, 1, 0)], (0.07, 0.16, 0.18)),
    ):
        fill_poly(ctx, pts, tuple(v * (0.5 + 0.9 * amb) for v in c0))
    # fondo del pasillo (pared final con ventanal tenue)
    a, b = _p(1, -1, 1), _p(1, 1, 0)
    ctx.rectangle(a[0], a[1], b[0] - a[0], b[1] - a[1])
    src(ctx, mix((0.03, 0.07, 0.09), (0.18, 0.38, 0.42), fondo_luz * amb))
    ctx.fill()
    # puertas a ambos lados
    for i in range(N_PUERTAS):
        z0, z1 = 0.06 + i * 0.15, 0.06 + i * 0.15 + 0.07
        for lado in (-1, 1):
            luz = puertas_luz[i] if lado > 0 else puertas_luz[i] * 0.0
            pts = [_p(z0, lado, 0), _p(z0, lado, 0.62), _p(z1, lado, 0.62), _p(z1, lado, 0)]
            fill_poly(ctx, pts, mix((0.04, 0.09, 0.10), (0.7, 0.92, 0.95), luz))
            ctx.set_line_width(max(2.0, 9 * _k(z0)))
            src(ctx, (0.02, 0.05, 0.06))
            ctx.move_to(*pts[0])
            for p in pts[1:]:
                ctx.line_to(*p)
            ctx.stroke()
            if luz > 0.02:
                mx, my = _p((z0 + z1) / 2, lado, 0.3)
                glow(ctx, mx, my, 420 * _k(z0), HALO, 0.45 * luz)
    # luces del techo
    for i, b_ in enumerate(luces):
        z0 = 0.03 + i * (0.94 / len(luces))
        z1 = z0 + 0.05
        pts = [_p(z0, -0.18, 1), _p(z0, 0.18, 1), _p(z1, 0.18, 1), _p(z1, -0.18, 1)]
        fill_poly(ctx, pts, mix((0.08, 0.14, 0.16), (0.95, 1.0, 1.0), b_))
        if b_ > 0.03:
            cx, cy = _p((z0 + z1) / 2, 0, 1)
            glow(ctx, cx, cy + 120 * _k(z0), 520 * _k(z0), FLUO, 0.40 * b_ * brillo)
            fx, fy = _p((z0 + z1) / 2, 0, 0)                                                 # charco de luz en el piso
            ovalo(ctx, fx, fy - 8 * _k(z0), 320 * _k(z0), 36 * _k(z0), FLUO, 0.14 * b_ * brillo)
    # silueta blanca
    if figura:
        z, a = figura
        k = _k(z)
        fx, fy = _p(z, 0, 0)
        personajes.eulalia(ctx, fx, fy, 0.78 * k, t, pose="pie", espalda=True, halo=0.9, alpha=a, flota=0.0)
