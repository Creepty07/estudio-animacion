"""Cabezas del estilo "Reglas": círculo grande, ojos enormes con pupila chica, cejas gruesas y boca simple."""
import math
import cairo
from motor.primitives import clamp, fill_poly
from historias.silbon.dibujo import estilo as E

# Expresiones: ceja (px; negativo = interior arriba, preocupado; positivo = enojo), abierto (1 = normal), pupila (px),
# boca (forma), abre (apertura de la boca), parpado (fracción del ojo tapada arriba), sudor.
EXPR = {
    "normal": dict(ceja=0, abierto=1.0, pupila=9.5, boca="neutra", abre=1.0, parpado=0.0, sudor=False),
    "serio": dict(ceja=6, abierto=0.9, pupila=9.5, boca="neutra", abre=1.0, parpado=0.18, sudor=False),
    "sospecha": dict(ceja=10, abierto=0.8, pupila=8, boca="ladeada", abre=1.0, parpado=0.3, sudor=False),
    "miedo": dict(ceja=-16, abierto=1.12, pupila=5.5, boca="dientes", abre=1.0, parpado=0.0, sudor=True),
    "susto": dict(ceja=-20, abierto=1.22, pupila=4.2, boca="grito", abre=0.9, parpado=0.0, sudor=True),
    "sonrisa": dict(ceja=-4, abierto=0.88, pupila=9.5, boca="sonrisa", abre=1.0, parpado=0.0, sudor=False),
    "alivio": dict(ceja=-8, abierto=0.7, pupila=9, boca="sonrisa", abre=1.0, parpado=0.25, sudor=False),
    "sueno": dict(ceja=0, abierto=0.55, pupila=9, boca="neutra", abre=1.0, parpado=0.5, sudor=False),
    "duerme": dict(ceja=-2, abierto=0.0, pupila=9, boca="o", abre=0.35, parpado=0.0, sudor=False),
    "tristeza": dict(ceja=-14, abierto=0.9, pupila=9.5, boca="triste", abre=1.0, parpado=0.1, sudor=False),
    "shh": dict(ceja=4, abierto=0.95, pupila=8, boca="neutra", abre=1.0, parpado=0.1, sudor=False),
    "borracho": dict(ceja=-3, abierto=0.6, pupila=8, boca="ladeada", abre=1.0, parpado=0.4, sudor=False),
}


def expr(nombre, **cambios):
    """Una expresión por nombre, con los números que quieras cambiar (sirve para animar con lerp)."""
    return {**EXPR[nombre], **cambios}


def relleno_contorno(ctx, rgb, s, grosor=None, alpha=1.0):
    """Rellena el trazado actual y le pone el contorno grueso de la casa."""
    ctx.set_source_rgba(*rgb, alpha)
    ctx.fill_preserve()
    ctx.set_line_width((grosor or E.GROSOR) * s)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_source_rgb(*E.CONTORNO)
    ctx.stroke()


def trazo(ctx, s, grosor=None):
    ctx.set_line_width((grosor or E.GROSOR) * s)
    ctx.set_line_join(cairo.LINE_JOIN_ROUND)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.set_source_rgb(*E.CONTORNO)
    ctx.stroke()


def elipse(ctx, x, y, rx, ry):
    ctx.save()
    ctx.translate(x, y)
    ctx.scale(max(rx, 0.01), max(ry, 0.01))
    ctx.new_sub_path()
    ctx.arc(0, 0, 1, 0, math.tau)
    ctx.restore()


def ojo(ctx, x, y, s, piel, mira=(0.0, 0.0), abierto=1.0, pupila=9.5, parpado=0.0, rx=31.0, ry=36.0):
    """Un ojo centrado en (x, y). mira en -1..1 mueve la pupila; abierto 0 = cerrado (rayita)."""
    if abierto < 0.1:
        ctx.new_path()
        ctx.arc(x, y - 6 * s, rx * 0.8 * s, 0.15 * math.pi, 0.85 * math.pi)
        trazo(ctx, s, 6.5)
        return
    h = ry * abierto
    elipse(ctx, x, y, rx * s, h * s)
    relleno_contorno(ctx, (0.97, 0.97, 0.94), s, 5.5)
    px = x + mira[0] * (rx - pupila - 5) * s
    py = y + mira[1] * max(h - pupila - 5, 0) * s
    ctx.new_path()
    ctx.arc(px, py, pupila * s, 0, math.tau)
    ctx.set_source_rgb(*E.CONTORNO)
    ctx.fill()
    if parpado > 0.02:                                       # párpado: tapa la parte de arriba del ojo
        ctx.save()
        elipse(ctx, x, y, rx * s, h * s)
        ctx.clip()
        yb = y - h * s + 2 * h * s * parpado
        ctx.rectangle(x - rx * s - 4, y - h * s - 6, 2 * rx * s + 8, yb - (y - h * s - 6))
        ctx.set_source_rgb(*piel)
        ctx.fill()
        ctx.restore()
        ctx.new_path()
        ctx.move_to(x - rx * s, yb)
        ctx.line_to(x + rx * s, yb)
        trazo(ctx, s, 5.5)
    elipse(ctx, x, y, rx * s, h * s)
    trazo(ctx, s, 5.5)


def ceja(ctx, x, y, s, lado, tilt):
    """Ceja gruesa. lado -1 = ojo izquierdo, +1 = derecho; tilt > 0 baja el extremo interior (enojo)."""
    L = 46
    ctx.new_path()
    ctx.move_to(x - lado * L / 2 * s, y - tilt * s)              # extremo exterior
    ctx.line_to(x + lado * L / 2 * s, y + tilt * s)              # extremo interior
    trazo(ctx, s, 10.5)


def boca(ctx, x, y, s, forma, abre=1.0):
    ctx.new_path()
    if forma == "neutra":
        ctx.move_to(x - 22 * s, y)
        ctx.curve_to(x - 8 * s, y + 5 * s, x + 8 * s, y + 5 * s, x + 22 * s, y)
        trazo(ctx, s, 6.5)
    elif forma == "ladeada":
        ctx.move_to(x - 24 * s, y + 6 * s)
        ctx.curve_to(x - 4 * s, y + 10 * s, x + 14 * s, y + 2 * s, x + 26 * s, y - 8 * s)
        trazo(ctx, s, 6.5)
    elif forma == "sonrisa":
        ctx.arc(x, y - 16 * s, 36 * s, 0.17 * math.pi, 0.83 * math.pi)
        trazo(ctx, s, 6.5)
    elif forma == "triste":
        ctx.arc(x, y + 34 * s, 30 * s, 1.17 * math.pi, 1.83 * math.pi)
        trazo(ctx, s, 6.5)
    elif forma == "o":
        elipse(ctx, x, y + 4 * s, 13 * s, 17 * s * max(abre, 0.2))
        relleno_contorno(ctx, (0.16, 0.04, 0.06), s, 5.5)
    elif forma == "grito":
        elipse(ctx, x, y + 14 * s, 36 * s, 44 * s * max(abre, 0.2))
        relleno_contorno(ctx, (0.18, 0.03, 0.06), s, 6)
        ctx.save()
        elipse(ctx, x, y + 14 * s, 36 * s, 44 * s * max(abre, 0.2))
        ctx.clip()
        elipse(ctx, x, y + 44 * s, 24 * s, 16 * s)                  # lengua
        ctx.set_source_rgb(0.78, 0.30, 0.34)
        ctx.fill()
        ctx.restore()
    elif forma == "dientes":                                         # dientes apretados, como el cuadro de referencia
        ctx.save()
        ctx.translate(x, y + 4 * s)
        w, h = 68 * s, 30 * s
        ctx.new_path()
        ctx.rectangle(-w / 2, -h / 2, w, h)
        relleno_contorno(ctx, (0.96, 0.95, 0.90), s, 5.5)
        for i in (-2, -1, 0, 1, 2):
            ctx.move_to(i * w / 5 + w / 10 - w / 10 + (0), -h / 2)
            ctx.line_to(i * w / 5, h / 2)
        ctx.move_to(-w / 2, 0)
        ctx.line_to(w / 2, 0)
        trazo(ctx, s, 3.5)
        ctx.restore()


def gota_sudor(ctx, x, y, s, t=0.0):
    ctx.new_path()
    ctx.move_to(x, y - 22 * s)
    ctx.curve_to(x + 15 * s, y, x + 13 * s, y + 18 * s, x, y + 20 * s)
    ctx.curve_to(x - 13 * s, y + 18 * s, x - 15 * s, y, x, y - 22 * s)
    relleno_contorno(ctx, (0.62, 0.84, 1.0), s, 4.5)


def cabeza(ctx, x, y, s, piel, e="normal", mira=(0.0, 0.0), parpadeo=0.0, pelo=None, extra=None, t=0.0):
    """Cabeza con centro en (x, y). e: nombre de expresión o dict (ver EXPR). parpadeo 0..1 cierra los ojos.
    pelo/extra: funciones (ctx, x, y, s) que dibujan pelo, sombrero, bigote, lentes… por encima de la cara."""
    ex = EXPR[e] if isinstance(e, str) else e
    r = E.RADIO_CABEZA * s
    ctx.new_path()
    ctx.arc(x, y, r, 0, math.tau)
    relleno_contorno(ctx, piel, s)
    dx, dy = 40 * s, -4 * s
    ab = ex["abierto"] * (1 - clamp(parpadeo))
    for lado in (-1, 1):
        ojo(ctx, x + lado * dx, y + dy, s, piel, mira, ab, ex["pupila"], ex["parpado"])
        if ex["ceja"] != 0 or ex["abierto"] > 1.0:
            ceja(ctx, x + lado * dx, y + dy - 52 * s * ex["abierto"] ** 0.5, s, lado, ex["ceja"])
        else:
            ceja(ctx, x + lado * dx, y + dy - 52 * s, s, lado, 0)
    boca(ctx, x, y + 58 * s, s, ex["boca"], ex["abre"])
    if ex.get("sudor"):
        gota_sudor(ctx, x + 84 * s, y - 36 * s + 5 * s * math.sin(t * 5), s)
    if pelo:
        pelo(ctx, x, y, s)
    if extra:
        extra(ctx, x, y, s)
