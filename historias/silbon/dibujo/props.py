"""Objetos de las escenas: el letrero de reglas, el reloj, la botella, los huesos y los efectos "se oye, se ve"."""
import math
import cairo
from motor import config
from motor.primitives import glow, line, circle, seg, smooth, font, text_w, text_at, text_center, src, lerp
from historias.silbon.dibujo import estilo as E
from historias.silbon.dibujo.caras import relleno_contorno, trazo, elipse

REGLAS_LETRERO = [                      # lo que dice el letrero del hato (una línea por regla)
    "SILBIDO CERCA = ESTÁ LEJOS",
    "NADIE BEBE AGUARDIENTE",
    "LOS PERROS NO SE CALLAN",
    "SI CAEN HUESOS, CUÉNTALOS",
]


def letrero(ctx, cx, cy, ancho, t=0.0, reveal=4.0, resaltar=0, brillo=1.0, s=1.0):
    """Tabla de madera con las 4 reglas. reveal = cuántas líneas se han "escrito" (fraccionario: se escribe poco a poco);
    resaltar = regla (1-4) que brilla en amarillo, 0 = ninguna. (cx, cy) es el centro."""
    alto = ancho * 0.92
    x0, y0 = cx - ancho / 2, cy - alto / 2
    ctx.new_path()                                                    # cuerda
    ctx.move_to(x0 + ancho * 0.18, y0)
    ctx.line_to(cx, y0 - ancho * 0.22)
    ctx.line_to(x0 + ancho * 0.82, y0)
    ctx.set_line_width(7 * s)
    ctx.set_source_rgb(0.62, 0.52, 0.34)
    ctx.stroke()
    ctx.new_path()
    ctx.rectangle(x0, y0, ancho, alto)
    relleno_contorno(ctx, E.MADERA_CLARA, s, 9)
    for i in range(1, 5):                                             # vetas y tablones
        yy = y0 + alto * i / 5
        line(ctx, x0 + 6, yy, x0 + ancho - 6, yy, 3.5, E.MADERA_OSCURA, 0.7)
    for nx, ny in ((x0 + 22, y0 + 22), (x0 + ancho - 22, y0 + 22), (x0 + 22, y0 + alto - 22), (x0 + ancho - 22, y0 + alto - 22)):
        circle(ctx, nx, ny, 6, (0.13, 0.10, 0.09))
    tam = ancho * 0.046
    font(ctx, tam * 1.18, config.FONT_DISPLAY, bold=True)
    src(ctx, (0.16, 0.08, 0.04))
    text_center(ctx, "REGLAS DEL HATO", cx, y0 + alto * 0.14, 3)
    line(ctx, x0 + ancho * 0.12, y0 + alto * 0.19, x0 + ancho * 0.88, y0 + alto * 0.19, 5, (0.16, 0.08, 0.04), 0.9)
    for i, txt in enumerate(REGLAS_LETRERO):
        k = max(0.0, min(1.0, reveal - i))
        if k <= 0:
            continue
        yy = y0 + alto * (0.36 + 0.19 * i)
        font(ctx, tam, config.FONT, bold=True)
        vis = txt[: int(len(txt) * k + 0.999)]
        es_res = resaltar == i + 1
        if es_res:
            glow(ctx, cx, yy - tam * 0.3, ancho * 0.7, (1.0, 0.8, 0.2), 0.35 * brillo)
            src(ctx, (0.62, 0.30, 0.02) if False else (0.55, 0.05, 0.03))
        else:
            src(ctx, (0.18, 0.09, 0.05), 0.55 if resaltar else 0.95)
        ctx.move_to(x0 + ancho * 0.06, yy)
        ctx.show_text(f"{i + 1}. ")
        ctx.show_text(vis)
        if es_res:
            line(ctx, x0 + ancho * 0.07, yy + 12, x0 + ancho * 0.93, yy + 12, 5, (0.8, 0.12, 0.08), 0.9)


def reloj(ctx, x, y, r, minutos, s=1.0, t=0.0):
    """Reloj de pared. minutos = minutos desde las 12:00 (7 PM = 420)."""
    ctx.new_path()
    ctx.arc(x, y, r, 0, math.tau)
    relleno_contorno(ctx, (0.93, 0.90, 0.80), s, 10)
    for i in range(12):
        a = math.tau * i / 12 - math.pi / 2
        line(ctx, x + math.cos(a) * r * 0.82, y + math.sin(a) * r * 0.82, x + math.cos(a) * r * 0.94, y + math.sin(a) * r * 0.94,
             5 * s, E.CONTORNO)
    am = math.tau * (minutos % 60) / 60 - math.pi / 2
    ah = math.tau * (minutos % 720) / 720 - math.pi / 2
    line(ctx, x, y, x + math.cos(ah) * r * 0.50, y + math.sin(ah) * r * 0.50, 12 * s, E.CONTORNO)
    line(ctx, x, y, x + math.cos(am) * r * 0.78, y + math.sin(am) * r * 0.78, 8 * s, E.CONTORNO)
    circle(ctx, x, y, 9 * s, (0.7, 0.1, 0.1))


def botella(ctx, x, y, s, giro=0.0, tapa=True, nivel=0.7):
    """Botella de aguardiente (genérica, sin marca). (x, y) = centro de la base."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(giro)
    ctx.scale(s, s)
    ctx.new_path()
    ctx.move_to(-46, 0)
    ctx.line_to(-46, -190)
    ctx.curve_to(-46, -240, -18, -250, -18, -290)
    ctx.line_to(-18, -330)
    ctx.line_to(18, -330)
    ctx.line_to(18, -290)
    ctx.curve_to(18, -250, 46, -240, 46, -190)
    ctx.line_to(46, 0)
    ctx.close_path()
    relleno_contorno(ctx, (0.62, 0.78, 0.66), 1, 7)
    ctx.save()                                                        # líquido
    ctx.new_path()
    ctx.rectangle(-44, -190 * nivel - 6, 88, 190 * nivel + 6)
    ctx.set_source_rgba(0.9, 0.88, 0.7, 0.55)
    ctx.fill()
    ctx.restore()
    ctx.new_path()
    ctx.rectangle(-46, -150, 92, 78)
    relleno_contorno(ctx, (0.93, 0.88, 0.70), 1, 5)
    font(ctx, 17, config.FONT, bold=True)
    src(ctx, (0.35, 0.08, 0.05))
    text_center(ctx, "AGUARDIENTE", 0, -104, 0.5)
    if tapa:
        ctx.new_path()
        ctx.rectangle(-22, -346, 44, 22)
        relleno_contorno(ctx, (0.74, 0.5, 0.28), 1, 6)
    ctx.restore()


def hueso(ctx, x, y, s, giro=0.0, largo=170):
    """Un fémur: caña y dos nudos en cada punta."""
    ctx.save()
    ctx.translate(x, y)
    ctx.rotate(giro)
    ctx.scale(s, s)
    ctx.new_path()
    ctx.move_to(-largo / 2, 0)
    ctx.line_to(largo / 2, 0)
    ctx.set_line_width(24)
    ctx.set_line_cap(1)
    ctx.set_source_rgb(*E.CONTORNO)
    ctx.stroke()
    for lado in (-1, 1):
        for dy in (-13, 13):
            ctx.new_path()
            ctx.arc(lado * largo / 2, dy, 17, 0, math.tau)
            relleno_contorno(ctx, E.HUESO, 1, 6)
    ctx.new_path()
    ctx.move_to(-largo / 2, 0)
    ctx.line_to(largo / 2, 0)
    ctx.set_line_width(14)
    ctx.set_source_rgb(*E.HUESO)
    ctx.stroke()
    ctx.restore()


def x_roja(ctx, x, y, s, k):
    """Una X roja que se estampa (k 0..1)."""
    if k <= 0:
        return
    sc = s * (1.0 + 0.5 * (1 - smooth(k)))
    a = min(1.0, k * 3)
    for sx in (-1, 1):
        ctx.new_path()
        ctx.move_to(x - 120 * sc, y - sx * 120 * sc)
        ctx.line_to(x + 120 * sc, y + sx * 120 * sc)
        ctx.set_line_width(38 * sc)
        ctx.set_line_cap(1)
        ctx.set_source_rgba(0.05, 0.0, 0.0, a)
        ctx.stroke()
        ctx.new_path()
        ctx.move_to(x - 120 * sc, y - sx * 120 * sc)
        ctx.line_to(x + 120 * sc, y + sx * 120 * sc)
        ctx.set_line_width(24 * sc)
        ctx.set_source_rgba(*E.ROJO, a)
        ctx.stroke()


def zzz(ctx, x, y, s, t):
    """Zetas que suben de alguien dormido."""
    for i in range(3):
        k = ((t * 0.5 + i / 3) % 1.0)
        font(ctx, (34 + 26 * k) * s, config.FONT_DISPLAY, bold=True)
        src(ctx, (0.85, 0.9, 1.0), (1 - k) * 0.9)
        ctx.move_to(x + 30 * s * k + i * 8 * s, y - 120 * s * k)
        ctx.show_text("Z")


def ondas(ctx, x, y, t, lado=1, n=4, color=(1.0, 0.95, 0.7), tam=70, ritmo=2.2, alpha=0.8):
    """Ondas de sonido que salen de (x, y) hacia `lado`: lo que se oye, se ve."""
    for i in range(n):
        k = (t * ritmo + i / n) % 1.0
        r = tam * (0.3 + 2.2 * k)
        ctx.new_path()
        centro = 0.0 if lado > 0 else math.pi
        ctx.arc(x, y, r, centro - 0.9, centro + 0.9)
        ctx.set_line_width(9 * (1 - k) + 2)
        ctx.set_line_cap(1)
        ctx.set_source_rgba(*color, alpha * (1 - k))
        ctx.stroke()
