"""+4 HORAS: Ramiro destapa su botella (¡pop!), los perros ladran y alguien grita que se callen."""
import math
from motor.config import W, H
from motor.primitives import seg, smooth, lerp
from historias.silbon.dibujo import fondos, props, hud, estilo as E
from historias.silbon.dibujo.caras import relleno_contorno
from historias.silbon.dibujo.gente import persona, PERSONAJES as P
from historias.silbon.dibujo.animales import perro_cabeza
from historias.silbon.dibujo.escena import camara, marco

DURATION = 9.0
SUBS = [
    (0.9, 4.7, "Cuatro horas después, Ramiro *destapa* su botella.", None),
    (5.0, 8.7, "Los perros ladran. Alguien los manda a *callar*.", None),
]
RELOJ = (0.1, 1.5)          # el reloj salta de las 7 a las 11
POP = 3.45                  # el corcho sale
GRITO = (6.3, 7.6)          # Ramiro grita "¡CÁLLENSE!" (texto, no voz)
LADRIDOS = (5.1, 5.6, 6.1, 6.6, 7.1, 7.6)


def _ladra(t):
    for b in LADRIDOS:
        d = t - b
        if 0 <= d < 0.2:
            return math.sin(d / 0.2 * math.pi)
    return 0.0


def draw(ctx, t):
    ctx.save()
    camara(ctx, t, DURATION, 1.0, 1.1, 0.5, 0.55)
    fondos.pared(ctx, t, farol=(0.12, 0.22), luz=0.8)
    fondos.farol(ctx, W * 0.12, H * 0.22 + 30, 0.9, t, 0.8)
    minutos = lerp(420, 660, smooth(seg(t, *RELOJ)))
    props.reloj(ctx, 800, 640, 105, minutos, t=t)
    # Ramiro con la botella
    destapa = smooth(seg(t, 2.2, POP))
    e = "borracho" if t >= POP + 0.3 else "sonrisa"
    grito = GRITO[0] <= t <= GRITO[1]
    brazo = lerp(250, 40, destapa)
    persona(ctx, 500, 820, 1.2, P["ramiro"], "susto" if grito else e, mira=(0.0, 0.2),
            brazos={"i": (-110, brazo)}, t=t)
    props.botella(ctx, 500 - 140 * 1.2, 820 + 110 + (-brazo + 250) * 0.2, 0.55, giro=-0.2 + 0.6 * destapa, tapa=t < POP, nivel=0.7)
    if POP <= t < POP + 0.35:                                             # corcho que sale volando
        k = seg(t, POP, POP + 0.35)
        ctx.new_path()
        ctx.rectangle(420 + 140 * k, 640 - 220 * math.sin(k * 2.0), 34, 24)
        relleno_contorno(ctx, (0.74, 0.5, 0.28), 1, 5)
    # perros asomados abajo
    l = _ladra(t)
    if t >= LADRIDOS[0] - 0.2:
        perro_cabeza(ctx, 200, 1070, 0.9, (0.35, 0.25, 0.18), ladra=l, t=t)
        perro_cabeza(ctx, 880, 1090, 0.9, (0.18, 0.15, 0.14), ladra=_ladra(t - 0.05), t=t)
        if l > 0:
            props.ondas(ctx, 320, 1030, t, lado=1, n=3, tam=60, ritmo=3.0)
            props.ondas(ctx, 760, 1050, t, lado=-1, n=3, tam=60, ritmo=3.0)
    ctx.restore()
    grito = GRITO[0] <= t <= GRITO[1]
    hud.etiqueta_tiempo(ctx, "+4 HORAS", t, 0.05, 2.3)
    if grito:
        hud.texto_contorno(ctx, "¡CÁLLENSE, PERROS!", W / 2, 340, 66, (1.0, 0.45, 0.4), 1.0, escala=hud.pop(t, GRITO[0]))
    marco(ctx, t, DURATION)
