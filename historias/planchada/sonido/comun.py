"""Piezas compartidas por las mezclas de La Planchada.

Regla de la enfermera: NUNCA suenan sus pasos. Cuando aparece, el reloj y el monitor se caen y queda el goteo.
"""
import numpy as np
from motor.config import SR
from motor.audio import sfx, ambient, agua
from motor.audio.synth import band, norm, fade, noise, env_exp, thump, tt
from historias.planchada.dibujo.paleta import fluo_brillo

PERIODO_GOTA = 1 / 0.9          # la gota del suero cae cada 1.11 s (igual que en dibujo/cuarto.py: suero())


def hum(tr, T, dur, seed, modo="parpadea", gain=0.12, lo=0.0, extra=None):
    """Zumbido de fluorescente de una escena, con el mismo parpadeo que dibuja la escena (mismo seed y modo)."""
    if modo == "fijo":
        sig = ambient.fluorescente(dur, None, seed=seed)
    else:
        f = (lambda x: lo + (1 - lo) * fluo_brillo(x, seed, modo)) if extra is None else extra
        sig = ambient.fluorescente(dur, f, seed=seed)
    tr.add(sig, T, gain)


def goteo(tr, T, dur, gain=0.22, desde=0.0, pan=-0.3):
    """Gota del suero: cae cada 1.11 s, sincronizada con el dibujo (llega al fondo de la cámara en cada múltiplo)."""
    k = int(np.ceil(desde / PERIODO_GOTA))
    while k * PERIODO_GOTA < dur - 0.1:
        tr.add(agua.gota(k % 7), T + k * PERIODO_GOTA, gain * (0.85 + 0.15 * ((k * 5) % 3) / 2), pan)
        k += 1


def reloj(tr, T, dur, gain=0.16, desde=0.0, cada=1.0, hasta=None):
    """Tic grave del reloj de pared, uno por segundo (en 'cada' segundos)."""
    t = desde
    hasta = dur if hasta is None else hasta
    while t < hasta - 0.05:
        tr.add(sfx.tick(520 if int(round(t / cada)) % 2 == 0 else 470, 0.07), T + t, gain, 0.35)
        t += cada


def monitor(tr, T, dur, gain=0.12, desde=0.5, cada=1.0, hasta=None):
    t = desde
    hasta = dur if hasta is None else hasta
    while t < hasta - 0.1:
        tr.add(sfx.monitor_pitido(), T + t, gain, 0.5)
        t += cada


def hielo(seed=0):
    """Crujido agudo de hielo que se forma en el vidrio."""
    return norm(band(sfx.creak(0.9, seed), 1800, 9000)) * np.hanning(int(0.9 * SR)) ** 0.5


def dip(buf, env_ready, a, b, c, d, nivel=0.04):
    """Curva de silencio: baja a `nivel` entre a y b, se queda hasta c, vuelve a 1 en d (tiempos absolutos en s)."""
    ia, ib, ic, id_ = (int(x * SR) for x in (a, b, c, d))
    env_ready[ia:ib] = np.minimum(env_ready[ia:ib], np.linspace(1, nivel, ib - ia))
    env_ready[ib:ic] = np.minimum(env_ready[ib:ic], nivel)
    env_ready[ic:id_] = np.minimum(env_ready[ic:id_], np.linspace(nivel, 1, id_ - ic))
