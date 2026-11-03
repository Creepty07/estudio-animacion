"""Personas del estilo "Reglas": cabeza grande sobre un cuerpo de palitos con manos y pies redondos.

La cabeza se dibuja en (x, y) y el cuerpo cuelga hacia abajo (a escala 1 los pies quedan en y + 440).
"""
import math
from motor.primitives import clamp
from historias.silbon.dibujo import estilo as E
from historias.silbon.dibujo.caras import cabeza, relleno_contorno, trazo, elipse

R = E.RADIO_CABEZA


# ---------- pelo y accesorios (se pasan a `cabeza` como pelo / extra) ----------
def juntar(*fs):
    def f(ctx, x, y, s):
        for g in fs:
            g(ctx, x, y, s)
    return f


def pelo_corto(color):
    def f(ctx, x, y, s):
        r, n = R * s, 16
        pts = [(x + math.cos(math.pi * 1.10 + math.pi * 0.80 * i / n) * r * 1.02,
                y + math.sin(math.pi * 1.10 + math.pi * 0.80 * i / n) * r * 1.02) for i in range(n + 1)]
        for i in range(8, -1, -1):                                       # fleco en zigzag, de derecha a izquierda
            pts.append((x + (i / 8 * 2 - 1) * r * 0.86, y - r * (0.70 if i % 2 else 0.80)))
        ctx.new_path()
        ctx.move_to(*pts[0])
        for p in pts[1:]:
            ctx.line_to(*p)
        ctx.close_path()
        relleno_contorno(ctx, color, s, 6.5)
    return f


def chongo(color):
    def f(ctx, x, y, s):
        pelo_corto(color)(ctx, x, y, s)
        ctx.new_path()
        ctx.arc(x, y - R * 1.12 * s, R * 0.36 * s, 0, math.tau)
        relleno_contorno(ctx, color, s, 6.5)
    return f


def trenzas(color):
    def f(ctx, x, y, s):
        pelo_corto(color)(ctx, x, y, s)
        for lado in (-1, 1):
            ctx.new_path()
            ctx.arc(x + lado * R * 1.02 * s, y + R * 0.15 * s, R * 0.27 * s, 0, math.tau)
            relleno_contorno(ctx, color, s, 6.5)
    return f


def sombrero_llanero(color, banda=(0.18, 0.1, 0.07)):
    def f(ctx, x, y, s):
        r = R * s
        ctx.new_path()                                                     # copa
        ctx.move_to(x - r * 0.62, y - r * 0.74)
        ctx.curve_to(x - r * 0.66, y - r * 1.45, x + r * 0.66, y - r * 1.45, x + r * 0.62, y - r * 0.74)
        ctx.close_path()
        relleno_contorno(ctx, color, s, 6.5)
        ctx.new_path()                                                     # banda
        ctx.rectangle(x - r * 0.63, y - r * 0.98, r * 1.26, r * 0.2)
        relleno_contorno(ctx, banda, s, 5)
        elipse(ctx, x, y - r * 0.72, r * 1.6, r * 0.27)                    # ala
        relleno_contorno(ctx, color, s, 6.5)
    return f


def gorra(color):
    def f(ctx, x, y, s):
        r = R * s
        ctx.new_path()
        ctx.arc(x, y, r * 1.04, math.pi * 1.04, math.pi * 1.96)
        ctx.line_to(x + r * 0.99, y - r * 0.66)
        ctx.line_to(x - r * 0.99, y - r * 0.66)
        ctx.close_path()
        relleno_contorno(ctx, color, s, 6.5)
        elipse(ctx, x + r * 0.62, y - r * 0.60, r * 0.78, r * 0.17)
        relleno_contorno(ctx, color, s, 6.5)
    return f


def bigote(color):
    def f(ctx, x, y, s):
        r = R * s
        for lado in (-1, 1):
            ctx.save()
            ctx.translate(x + lado * r * 0.24, y + r * 0.40)
            ctx.rotate(lado * -0.25)
            elipse(ctx, 0, 0, r * 0.30, r * 0.11)
            ctx.restore()
            relleno_contorno(ctx, color, s, 5)
    return f


def lentes():
    def f(ctx, x, y, s):
        for lado in (-1, 1):
            ctx.new_path()
            ctx.arc(x + lado * 40 * s, y - 4 * s, 43 * s, 0, math.tau)
            trazo(ctx, s, 6)
        ctx.new_path()
        ctx.move_to(x - 4 * s, y - 8 * s)
        ctx.line_to(x + 4 * s, y - 8 * s)
        trazo(ctx, s, 6)
    return f


# ---------- personajes ----------
PERSONAJES = {
    "tu": dict(piel=E.PIEL_TU, ropa=(0.16, 0.38, 0.30), pantalon=(0.16, 0.18, 0.30), mochila=True,
               pelo=pelo_corto((0.20, 0.12, 0.09))),
    "llanero": dict(piel=E.PIEL_LLANERO, ropa=(0.70, 0.66, 0.52), pantalon=(0.30, 0.22, 0.16),
                    extra=juntar(bigote((0.80, 0.80, 0.78)), sombrero_llanero((0.80, 0.70, 0.46)))),
    "ramiro": dict(piel=E.PIEL_RAMIRO, ropa=(0.62, 0.20, 0.18), pantalon=(0.18, 0.20, 0.32),
                   pelo=pelo_corto((0.10, 0.07, 0.06)), extra=gorra((0.18, 0.36, 0.62))),
    "abuela": dict(piel=E.PIEL_ABUELA, ropa=(0.50, 0.30, 0.42), pantalon=(0.28, 0.22, 0.30),
                   pelo=chongo((0.74, 0.74, 0.76)), extra=lentes()),
    "nina": dict(piel=E.PIEL_NINA, ropa=(0.86, 0.60, 0.30), pantalon=(0.30, 0.30, 0.50), pelo=trenzas((0.10, 0.07, 0.06))),
}


# ---------- cuerpo ----------
def miembro(ctx, x0, y0, x1, y1, s, ancho, rgb):
    """Palito con contorno: brazo o pierna."""
    ctx.new_path()
    ctx.move_to(x0, y0)
    ctx.line_to(x1, y1)
    ctx.set_line_cap(1)
    ctx.set_line_width((ancho + 2 * E.GROSOR * 0.62) * s)
    ctx.set_source_rgb(*E.CONTORNO)
    ctx.stroke()
    ctx.new_path()
    ctx.move_to(x0, y0)
    ctx.line_to(x1, y1)
    ctx.set_line_width(ancho * s)
    ctx.set_source_rgb(*rgb)
    ctx.stroke()


def _cuerpo(ctx, x, y, s, p, brazos, fase):
    ropa, pant, piel = p["ropa"], p["pantalon"], p["piel"]
    for lado in (-1, 1):                                                     # piernas y zapatos
        ang = 0.0 if fase is None else math.sin(fase + (0 if lado < 0 else math.pi))
        pie = (x + lado * 34 * s + ang * 44 * s, y + (430 - max(0.0, ang) * 18) * s)
        miembro(ctx, x + lado * 30 * s, y + 262 * s, pie[0], pie[1], s, 22, pant)
        elipse(ctx, pie[0] + 10 * s, pie[1] + 4 * s, 30 * s, 15 * s)
        relleno_contorno(ctx, (0.12, 0.09, 0.08), s, 5.5)
    if p.get("mochila"):
        ctx.new_path()
        ctx.rectangle(x - 118 * s, y + 100 * s, 66 * s, 130 * s)
        relleno_contorno(ctx, (0.30, 0.22, 0.12), s, 6)
    ctx.new_path()                                                           # torso
    ctx.move_to(x - 66 * s, y + 90 * s)
    ctx.line_to(x + 66 * s, y + 90 * s)
    ctx.line_to(x + 60 * s, y + 280 * s)
    ctx.line_to(x - 60 * s, y + 280 * s)
    ctx.close_path()
    relleno_contorno(ctx, ropa, s)
    brazos = brazos or {}
    for lado, k in ((-1, "i"), (1, "d")):                                    # brazos y manos
        hx, hy = brazos.get(k, (lado * 92, 262))
        hombro = (x + lado * 62 * s, y + 130 * s)
        mano = (x + hx * s, y + hy * s)
        miembro(ctx, hombro[0], hombro[1], mano[0], mano[1], s, 20, ropa)
        ctx.new_path()
        ctx.arc(mano[0], mano[1], 19 * s, 0, math.tau)
        relleno_contorno(ctx, piel, s, 5.5)


def persona(ctx, x, y, s, p, e="normal", mira=(0.0, 0.0), brazos=None, fase=None, t=0.0, parpadeo=0.0, solo_cabeza=False):
    """p: un dict de PERSONAJES. brazos: {"i": (x, y), "d": (x, y)} con las manos relativas a la cabeza (a escala 1).
    fase: None = de pie; un ángulo = caminando."""
    if not solo_cabeza:
        _cuerpo(ctx, x, y, s, p, brazos, fase)
    cabeza(ctx, x, y, s, p["piel"], e, mira, parpadeo, p.get("pelo"), p.get("extra"), t)


def en_hamaca(ctx, x, y, s, p, e="duerme", lado=1, manta=None, t=0.0, mira=(0.0, 0.0), respira=True):
    """Persona acostada: la cabeza en (x, y) y el cuerpo tapado con una manta hacia `lado`."""
    manta = manta or (0.62, 0.28, 0.24)
    sube = 5 * s * math.sin(t * 2.0) if respira else 0.0
    ctx.new_path()
    ctx.move_to(x + lado * 70 * s, y + 20 * s)
    ctx.curve_to(x + lado * 150 * s, y - 40 * s + sube, x + lado * 330 * s, y - 20 * s + sube, x + lado * 440 * s, y + 50 * s)
    ctx.line_to(x + lado * 440 * s, y + 120 * s)
    ctx.line_to(x + lado * 70 * s, y + 130 * s)
    ctx.close_path()
    relleno_contorno(ctx, manta, s)
    for i in range(1, 4):                                                    # rayas de la manta
        ctx.new_path()
        ctx.move_to(x + lado * (70 + i * 90) * s, y + 5 * s + 4 * i * s)
        ctx.line_to(x + lado * (70 + i * 90) * s, y + 125 * s)
        ctx.set_line_width(7 * s)
        ctx.set_source_rgba(0, 0, 0, 0.22)
        ctx.stroke()
    cabeza(ctx, x, y, s, p["piel"], e, mira, 0.0, p.get("pelo"), p.get("extra"), t)
