"""Escena 8 — Llegan el perro blanco y el perro negro; cada uno da su excusa (Sahagún) y se va."""
from motor.config import W, H, BLANCO, NEGRO, ACENTO
from motor.primitives import seg, smooth, ease_out, ease_in, lerp, camera, darken, vignette, glow
from historias.rio_perros.dibujo import rio, celso as C, perros

DURATION = 9.2
SUBS = [
    (0.3, 1.9, "Llegó un perro blanco.", None),
    (2.1, 3.9, "Perro blanco: «Ya me lavé.»", None),
    (4.5, 5.8, "Llegó uno negro.", None),
    (6.0, 7.8, "Perro negro: «Estoy manchado.»", None),
]
# (entra, se detiene, habla, se da la vuelta) por perro
BLANCO_T = (0.2, 1.9, 2.1, 3.9)
NEGRO_T = (4.3, 5.8, 6.0, 7.8)
PARA_X = 650
CELSO_X = 290
FEET = rio.ORILLA_Y + 30


def _perro(t, ts):
    """(x, dir, paso, hablando) o None si no está en cuadro."""
    t_in, t_stop, t_hab, t_out = ts
    if t < t_in:
        return None
    if t < t_stop:
        u = ease_out(seg(t, t_in, t_stop))
        return lerp(1330, PARA_X, u), -1, 1.5 if u < 0.97 else 0.0, False
    if t < t_out:
        return PARA_X, -1, 0.0, t_hab <= t < t_out - 0.3
    u = ease_in(seg(t, t_out, t_out + 1.7))
    if u >= 1:
        return None
    return lerp(PARA_X, 1380, u), 1, 1.5, False


def draw(ctx, t):
    ctx.save()
    camera(ctx, lerp(1.0, 1.06, smooth(seg(t, 0, DURATION))), W * 0.55, H * 0.64)
    rio.fondo(ctx, t)
    rio.orilla(ctx, t)
    baja = 0.08 + 0.4 * smooth(seg(t, BLANCO_T[3], BLANCO_T[3] + 0.8)) + 0.4 * smooth(seg(t, NEGRO_T[3], NEGRO_T[3] + 0.8))
    C.celso(ctx, CELSO_X, FEET + 4, 1.3, dir=1, brazo_der=0.1, brazo_izq=-0.1, cabeza_baja=baja, t=t, sombra=0.30)
    for pelo, ts, y_off in ((BLANCO, BLANCO_T, 0), (NEGRO, NEGRO_T, 10)):
        p = _perro(t, ts)
        if p is None:
            continue
        x, d, paso, habla = p
        cab = 0.22 + (0.10 if habla and int(t * 6) % 2 else 0.0)
        if pelo is NEGRO:                                              # el perro negro necesita un halo frío para no perderse en la noche
            glow(ctx, x, FEET - 60, 330, (0.40, 0.62, 0.80), 0.32)
        perros.perro(ctx, x, FEET + 12 + y_off, 1.1, pelo, dir=d, t=t, paso=paso, cabeza=cab, orejas=0.9, cola=0.0,
                     brillo_ojos=0.8, ojos=ACENTO if pelo is NEGRO else None, rim=(0.75, 0.9, 1.0))
    ctx.restore()
    rio.niebla_baja(ctx, t, 1.1)
    vignette(ctx, 0.62)
    darken(ctx, 1 - smooth(seg(t, 0.0, 0.4)))
    darken(ctx, smooth(seg(t, DURATION - 0.4, DURATION)))
