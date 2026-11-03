"""El silbido hecho visible: siete notas (do, re, mi, fa, sol, la, si) que suben en escalera, sincronizadas con el sonido."""
import math
from motor.primitives import glow, seg, smooth, line
from historias.silbon.dibujo import estilo as E

NOTAS = 7


def nota(ctx, x, y, s, rgb, alpha):
    """Una corchea (♪) dibujada con trazos: cabeza ovalada, plica y banderín."""
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(s, s)
    ctx.save()
    ctx.rotate(-0.35)
    ctx.scale(1.0, 0.72)
    ctx.new_path()
    ctx.arc(0, 0, 26, 0, math.tau)
    ctx.restore()
    ctx.set_source_rgba(*rgb, alpha)
    ctx.fill()
    ctx.new_path()
    ctx.move_to(22, -8)
    ctx.line_to(22, -112)
    ctx.curve_to(26, -80, 66, -78, 56, -34)
    ctx.set_line_width(9)
    ctx.set_line_cap(1)
    ctx.set_source_rgba(*rgb, alpha)
    ctx.stroke()
    ctx.restore()


def silbido(ctx, t, t0, cx, cy, s=1.0, dur=1.5, mantener=1.2, rgb=(1.0, 0.93, 0.62), ancho=620, alto=300, alpha=1.0):
    """Dibuja las siete notas subiendo en diagonal. Cada una aparece en t0 + i*dur/7 y se apaga `mantener` s después de la última."""
    fin = t0 + dur + mantener
    if t < t0 or t > fin + 0.5:
        return
    g = 1 - smooth(seg(t, fin, fin + 0.5))
    for i in range(NOTAS):
        ti = t0 + dur * i / NOTAS
        k = seg(t, ti, ti + 0.18)
        if k <= 0:
            continue
        x = cx + (i / (NOTAS - 1) - 0.5) * ancho * s
        y = cy - (i / (NOTAS - 1) - 0.5) * alto * s + 6 * math.sin(t * 6 + i) - 22 * (1 - smooth(k))
        reciente = 1 - smooth(seg(t, ti + 0.1, ti + 0.7))
        glow(ctx, x, y - 30 * s, 70 * s * (1 + reciente), rgb, 0.5 * alpha * g * (0.35 + 0.65 * reciente))
        nota(ctx, x, y, s * (0.9 + 0.25 * reciente) * smooth(k), rgb, alpha * g)
    ctx.set_line_width(5 * s)
    for i in range(5):                                                # pentagrama tenue
        yy = cy + (i - 2) * 22 * s
        line(ctx, cx - ancho * s * 0.62, yy, cx + ancho * s * 0.62, yy, 3, (1, 1, 1), 0.12 * alpha * g)
