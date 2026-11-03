"""Fondos del Silbón: el llano de noche, el hato por fuera y el interior del hato."""
import math
import random
import cairo
from motor import config
from motor.layers import paint_layer
from motor.primitives import glow, lerp, seg, smooth, line, circle, fill_poly, src
from historias.silbon.dibujo import estilo as E
from historias.silbon.dibujo.caras import relleno_contorno, trazo, elipse

HORIZONTE = 0.56                       # fracción de la altura donde termina el llano


def _grad(ctx, y0, y1, c0, c1, c2=None):
    g = cairo.LinearGradient(0, y0, 0, y1)
    g.add_color_stop_rgb(0, *c0)
    if c2:
        g.add_color_stop_rgb(0.55, *c1)
        g.add_color_stop_rgb(1, *c2)
    else:
        g.add_color_stop_rgb(1, *c1)
    ctx.set_source(g)


def palma(ctx, x, y, s, rgb=(0.015, 0.03, 0.05)):
    """Palma de moriche en silueta: tronco fino y abanico de hojas."""
    ctx.new_path()
    ctx.move_to(x - 7 * s, y)
    ctx.curve_to(x - 5 * s, y - 150 * s, x + 6 * s, y - 250 * s, x + 2 * s, y - 330 * s)
    ctx.line_to(x + 11 * s, y - 330 * s)
    ctx.curve_to(x + 14 * s, y - 250 * s, x + 4 * s, y - 150 * s, x + 7 * s, y)
    ctx.close_path()
    ctx.set_source_rgb(*rgb)
    ctx.fill()
    for i in range(11):
        a = math.pi * (1.08 + 0.84 * i / 10)
        cx, cy = x + 6 * s, y - 330 * s
        ctx.new_path()
        ctx.move_to(cx, cy)
        ctx.curve_to(cx + math.cos(a) * 60 * s, cy + math.sin(a) * 70 * s - 20 * s,
                     cx + math.cos(a) * 120 * s, cy + math.sin(a) * 90 * s - 10 * s,
                     cx + math.cos(a) * 150 * s, cy + math.sin(a) * 60 * s + 50 * s)
        ctx.set_line_width(9 * s)
        ctx.set_source_rgb(*rgb)
        ctx.stroke()


def _pintar_llano(ctx):
    W, H = config.W, config.H
    hz = H * HORIZONTE
    _grad(ctx, 0, hz, E.NOCHE_ARRIBA, E.NOCHE_MEDIO, E.NOCHE_HORIZONTE)
    ctx.rectangle(0, 0, W, hz + 2)
    ctx.fill()
    r = random.Random(7)
    for _ in range(150):                                              # estrellas
        sx, sy = r.uniform(0, W), r.uniform(0, hz * 0.85)
        circle(ctx, sx, sy, r.choice((1.2, 1.6, 2.2)), (0.9, 0.93, 1.0), r.uniform(0.25, 0.9))
    ctx.new_path()                                                    # lomas lejanas
    ctx.move_to(0, hz)
    for i in range(0, W + 60, 60):
        ctx.line_to(i, hz - 26 - 22 * math.sin(i * 0.011) - 10 * math.sin(i * 0.037))
    ctx.line_to(W, hz + 2)
    ctx.line_to(0, hz + 2)
    ctx.close_path()
    ctx.set_source_rgb(0.05, 0.06, 0.15)
    ctx.fill()
    _grad(ctx, hz, H, (0.07, 0.10, 0.17), (0.02, 0.04, 0.07))        # suelo
    ctx.rectangle(0, hz, W, H - hz)
    ctx.fill()
    ctx.new_path()                                                    # camino de tierra hacia el horizonte
    ctx.move_to(W * 0.5 - 22, hz)
    ctx.line_to(W * 0.5 + 22, hz)
    ctx.line_to(W * 0.98, H)
    ctx.line_to(W * 0.02, H)
    ctx.close_path()
    g = cairo.LinearGradient(0, hz, 0, H)
    g.add_color_stop_rgba(0, 0.34, 0.30, 0.40, 0.25)
    g.add_color_stop_rgba(1, 0.30, 0.25, 0.28, 0.65)
    ctx.set_source(g)
    ctx.fill()
    for _ in range(420):                                              # matas de pasto en perspectiva
        k = r.random() ** 1.6
        gy = hz + 8 + k * (H - hz)
        gx = r.uniform(-20, W + 20)
        if abs(gx - W / 2) < 18 + k * W * 0.45 * 0.96 and r.random() < 0.8:
            continue
        h = 8 + 70 * k
        for j in (-1, 0, 1):
            line(ctx, gx + j * 5 * (0.4 + k), gy, gx + j * 11 * (0.4 + k), gy - h * (0.7 + 0.3 * r.random()),
                 1.6 + 2.2 * k, (0.05, 0.12 + 0.1 * r.random(), 0.12), 0.9)
    for px, ps in ((150, 0.55), (880, 0.7), (990, 0.45), (60, 0.4)):  # palmas de moriche
        palma(ctx, px, hz + 8, ps)


def _luna(ctx, x, y, r):
    glow(ctx, x, y, r * 5.5, (0.5, 0.6, 1.0), 0.35)
    circle(ctx, x, y, r, E.LUNA)
    for dx, dy, rr in ((-0.3, -0.2, 0.22), (0.25, 0.25, 0.3), (0.1, -0.4, 0.15)):   # mares
        circle(ctx, x + dx * r, y + dy * r, rr * r, (0.80, 0.84, 0.95), 0.8)


def llano(ctx, t, luna=(0.80, 0.12), r_luna=62, cocuyos=True, silbon_x=None):
    """El llano de noche. luna = posición en fracción de pantalla. cocuyos = luciérnagas."""
    W, H = config.W, config.H
    paint_layer(ctx, "llano", _pintar_llano)
    if luna:
        _luna(ctx, W * luna[0], H * luna[1], r_luna)
    if cocuyos:
        r = random.Random(3)
        for i in range(26):
            bx, by = r.uniform(0, W), r.uniform(H * 0.60, H * 0.96)
            ph = r.uniform(0, 6.28)
            x = bx + 40 * math.sin(t * 0.5 + ph)
            y = by + 24 * math.sin(t * 0.7 + ph * 2)
            a = 0.5 + 0.5 * math.sin(t * 2.2 + ph)
            glow(ctx, x, y, 22 + 6 * a, (0.8, 1.0, 0.4), 0.7 * a)


def hato(ctx, x, y, s, luz=1.0, t=0.0):
    """El hato por fuera (casa de bahareque y techo de palma). (x, y) = centro de la base."""
    ctx.new_path()                                                    # pared
    ctx.rectangle(x - 190 * s, y - 190 * s, 380 * s, 190 * s)
    relleno_contorno(ctx, (0.34, 0.27, 0.24), s, 6)
    ctx.new_path()                                                    # techo de palma
    ctx.move_to(x - 250 * s, y - 180 * s)
    ctx.line_to(x, y - 350 * s)
    ctx.line_to(x + 250 * s, y - 180 * s)
    ctx.close_path()
    relleno_contorno(ctx, E.PAJA, s, 6)
    for i in range(-5, 6):                                            # paja
        ctx.new_path()
        ctx.move_to(x + i * 40 * s * 0.5 * 0.2, y - 340 * s + abs(i) * 4 * s)
        ctx.line_to(x + i * 46 * s, y - 188 * s)
        ctx.set_line_width(3 * s)
        ctx.set_source_rgba(0.12, 0.08, 0.03, 0.55)
        ctx.stroke()
    glow(ctx, x, y - 70 * s, 260 * s, E.LLAMA, 0.45 * luz)
    ctx.new_path()                                                    # puerta con luz
    ctx.rectangle(x - 44 * s, y - 132 * s, 88 * s, 132 * s)
    relleno_contorno(ctx, (1.0, 0.66, 0.24), s, 6)
    ctx.new_path()                                                    # ventana
    ctx.rectangle(x + 100 * s, y - 130 * s, 56 * s, 56 * s)
    relleno_contorno(ctx, (1.0, 0.62, 0.22), s, 5)
    glow(ctx, x + 128 * s, y - 100 * s, 90 * s, E.LLAMA, 0.4 * luz)


def _pintar_pared(ctx):
    W, H = config.W, config.H
    _grad(ctx, 0, H, (0.30, 0.22, 0.17), (0.18, 0.12, 0.10))
    ctx.rectangle(0, 0, W, H)
    ctx.fill()
    r = random.Random(11)
    for _ in range(46):                                               # grietas y manchas del bahareque
        gx, gy = r.uniform(0, W), r.uniform(0, H)
        line(ctx, gx, gy, gx + r.uniform(-60, 60), gy + r.uniform(30, 130), 2.5, (0.10, 0.06, 0.04), 0.45)
    for _ in range(40):
        circle(ctx, r.uniform(0, W), r.uniform(0, H), r.uniform(20, 70), (0.12, 0.08, 0.06), 0.07)
    for i in range(7):                                                # tablones del piso
        y0 = H * 0.80 + i * 52
        ctx.rectangle(0, y0, W, H)
    ctx.new_path()
    _grad(ctx, H * 0.80, H, (0.14, 0.09, 0.07), (0.07, 0.05, 0.05))
    ctx.rectangle(0, H * 0.80, W, H * 0.20)
    ctx.fill()
    for i in range(1, 8):
        y0 = H * 0.80 + i * 52 * (i / 7 + 0.4)
        line(ctx, 0, y0, W, y0, 3, (0.03, 0.02, 0.02), 0.6)
    for bx in (0, 1):                                                 # vigas del techo
        ctx.new_path()
    ctx.rectangle(0, 0, W, 150)
    ctx.set_source_rgb(0.10, 0.065, 0.045)
    ctx.fill()
    for i in range(0, W + 140, 140):
        line(ctx, i, 0, i + 70, 150, 16, (0.17, 0.10, 0.07), 1.0)


def pared(ctx, t, farol=(0.5, 0.30), luz=1.0, parpadeo=True):
    """Pared interior de bahareque con piso y vigas, alumbrada por un farol. farol = posición en fracción de pantalla."""
    W, H = config.W, config.H
    paint_layer(ctx, "pared", _pintar_pared)
    fx, fy = W * farol[0], H * farol[1]
    fl = 1 + (0.06 * math.sin(t * 11) + 0.04 * math.sin(t * 23)) if parpadeo else 1.0
    glow(ctx, fx, fy, 900 * fl * luz, E.LLAMA, 0.50 * luz)
    glow(ctx, fx, fy, 380 * fl * luz, (1.0, 0.85, 0.5), 0.40 * luz)


def farol(ctx, x, y, s, t=0.0, luz=1.0):
    """Farol de petróleo colgado: cadena, vidrio y llama."""
    fl = 1 + 0.08 * math.sin(t * 13) + 0.05 * math.sin(t * 29)
    line(ctx, x, y - 140 * s, x, y - 60 * s, 4 * s, (0.05, 0.04, 0.04))
    ctx.new_path()
    ctx.rectangle(x - 30 * s, y - 60 * s, 60 * s, 90 * s)
    relleno_contorno(ctx, (1.0, 0.82, 0.45), s, 5)
    glow(ctx, x, y - 14 * s, 160 * s * fl * luz, E.LLAMA, 0.8 * luz)
    ctx.new_path()
    ctx.move_to(x, y + 14 * s)
    ctx.curve_to(x + 14 * s, y - 4 * s, x + 8 * s, y - 24 * s * fl, x, y - 34 * s * fl)
    ctx.curve_to(x - 8 * s, y - 24 * s * fl, x - 14 * s, y - 4 * s, x, y + 14 * s)
    ctx.set_source_rgb(1.0, 0.97, 0.7)
    ctx.fill()
    ctx.new_path()
    ctx.rectangle(x - 36 * s, y - 70 * s, 72 * s, 14 * s)
    relleno_contorno(ctx, (0.15, 0.1, 0.08), s, 5)
    ctx.new_path()
    ctx.rectangle(x - 36 * s, y + 28 * s, 72 * s, 14 * s)
    relleno_contorno(ctx, (0.15, 0.1, 0.08), s, 5)


def marco_ventana(ctx, x, y, w, h, vista, s=1.0):
    """Ventana de madera con postigos: `vista(ctx)` dibuja lo que se ve afuera (se recorta al hueco)."""
    ctx.save()
    ctx.new_path()
    ctx.rectangle(x, y, w, h)
    ctx.clip()
    vista(ctx)
    ctx.restore()
    ctx.new_path()
    ctx.rectangle(x, y, w, h)
    trazo(ctx, s, 16)
    ctx.new_path()
    ctx.rectangle(x - 14 * s, y - 14 * s, w + 28 * s, h + 28 * s)
    ctx.set_source_rgb(*E.MADERA_OSCURA)
    ctx.set_line_width(26 * s)
    ctx.stroke()
    line(ctx, x + w / 2, y, x + w / 2, y + h, 14 * s, E.MADERA_OSCURA)
    line(ctx, x, y + h * 0.5, x + w, y + h * 0.5, 14 * s, E.MADERA_OSCURA)


def puerta_rendija(ctx, x, y, w, h, ancho_rendija=0.12, vista=None, t=0.0):
    """Puerta de tablones con una rendija vertical por la que se ve la noche. x, y = esquina superior izquierda."""
    ctx.save()
    ctx.new_path()
    ctx.rectangle(x, y, w, h)
    ctx.clip()
    ctx.set_source_rgb(0.015, 0.02, 0.04)
    ctx.paint()
    if vista:
        rw = w * ancho_rendija
        ctx.save()
        ctx.new_path()
        ctx.rectangle(x + w / 2 - rw / 2, y, rw, h)
        ctx.clip()
        vista(ctx)
        ctx.restore()
    for lado in (-1, 1):                                              # los dos tablones que forman la rendija
        px0 = x if lado < 0 else x + w / 2 + w * ancho_rendija / 2
        pw = w / 2 - w * ancho_rendija / 2
        ctx.new_path()
        ctx.rectangle(px0, y, pw, h)
        ctx.set_source_rgb(*E.MADERA)
        ctx.fill()
        for i in range(1, 4):
            line(ctx, px0, y + h * i / 4, px0 + pw, y + h * i / 4 + 6, 3, E.MADERA_OSCURA, 0.7)
        ctx.new_path()
        ctx.rectangle(px0, y, pw, h)
        trazo(ctx, 1.0, 8)
    ctx.restore()
