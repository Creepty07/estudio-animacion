"""Piezas compartidas por las tres mezclas de Ruta 0 (versión con narrador por radio).

Reparto de pesos: el sonido (lluvia, motor, frenos, silencios, golpes) lleva la tensión y el narrador la historia. Entre frases el fondo
sube (bed_peak 0.82); debajo de la voz baja (ducking 0.55) y la voz va a 0.95. Los silencios previos a cada susto se aplican a las dos pistas.
Regla: los pasajeros no hacen ningún ruido; solo respiran Iván y el chofer al hablar, y suena el camión.
"""
import numpy as np
from motor.config import SR
from motor.audio import sfx, ambient
from motor.audio.synth import noise, band, norm, env_exp, fade, thump, pad
from motor.audio.master import master
from motor.audio.mixing import scene_offsets, new_track
from motor import timeline

TMAP = None                  # tiempo sin voz -> tiempo con voz del episodio en curso (se fija en contexto())

GANANCIA_DB = 0.0            # se ajusta midiendo cada banda (referencia: -13.3 a -13.6 LUFS)


def contexto(ep):
    sc, total = scene_offsets(ep)
    global TMAP
    TMAP = timeline.episode(ep)[0]
    cam, total_out, voices = new_track(ep)                       # fondos
    ev, _, _ = new_track(ep)                                     # eventos
    T = {k.split("_")[0]: v[0] for k, v in sc.items()}
    M = {k.split("_")[0]: v[1] for k, v in sc.items()}
    D = {k: M[k].DURATION for k in M}
    return cam, ev, voices, total_out, T, M, D


def dip(env, a, b, c, d, nivel=0.0):
    """Curva de silencio sobre `env` (tiempos absolutos sin voz): baja entre a y b, queda hasta c, vuelve a 1 en d."""
    ia, ib, ic, id_ = (int(TMAP(x) * SR) for x in (a, b, c, d))      # los buffers están en tiempo con voz: hay que convertir
    env[ia:ib] = np.minimum(env[ia:ib], np.linspace(1, nivel, ib - ia))
    env[ib:ic] = np.minimum(env[ib:ic], nivel)
    env[ic:id_] = np.minimum(env[ic:id_], np.linspace(nivel, 1, id_ - ic))


def finalizar(cam, ev, env_cam, env_ev, voices, total_out, ganancia_db):
    cam.buf *= env_cam[:, None]
    ev.buf *= env_ev[:, None]
    bed = np.tanh((cam.buf + ev.buf) * 1.1)
    out = master(bed, total_out, voices, 0.5, bed_peak=0.82, duck=0.55, voice_peak=0.95)
    out = np.tanh(out * 1.5) / np.tanh(1.5)
    return out * 10 ** (ganancia_db / 20), total_out


def silencio_previo(T, a, b, c, d_cam, d_ev, env_cam, env_ev, nivel=0.0):
    """Silencio de `a` a `c` (tiempos locales absolutos). Los fondos recuperan en d_cam; los eventos justo antes del golpe en d_ev."""
    dip(env_cam, a - 0.1, a, c, d_cam, nivel)
    dip(env_ev, a - 0.1, a, c - 0.03, d_ev, nivel)
