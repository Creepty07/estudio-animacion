"""Piezas del sonido de "Las reglas del Silbón": contexto de la mezcla, silencios previos a los sustos y el silbido de siete notas.

Reparto de pesos: el sonido (silbido, ladridos, golpes, silencios) lleva la tensión y el narrador la historia. El fondo baja bajo la voz
(ducking) y se corta en seco antes de cada susto. El silbido se coloca NOTA POR NOTA (cada nota < 1.2 s) para que el motor no la estire
al alargar la escena con la voz: así no cambia de tono y cada nota cae justo cuando se dibuja en pantalla (notas.silbido).
"""
import numpy as np
from motor.config import SR
from motor.audio import sfx
from motor.audio.synth import noise, band, norm, env_exp, fade, thump, tt, reverb
from motor.audio.master import master
from motor.audio.mixing import scene_offsets, new_track
from motor import timeline

TMAP = None                    # tiempo sin voz -> con voz del episodio en curso (se fija en contexto())
GANANCIA_DB = 0.0

NOTAS_HZ = (1046.5, 1174.7, 1318.5, 1396.9, 1568.0, 1760.0, 1975.5)      # do, re, mi, fa, sol, la, si (una octava arriba)


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
    """Curva de silencio sobre `env` (tiempos sin voz): baja entre a y b, queda hasta c, vuelve a 1 en d."""
    ia, ib, ic, id_ = (int(TMAP(x) * SR) for x in (a, b, c, d))
    env[ia:ib] = np.minimum(env[ia:ib], np.linspace(1, nivel, ib - ia))
    env[ib:ic] = np.minimum(env[ib:ic], nivel)
    env[ic:id_] = np.minimum(env[ic:id_], np.linspace(nivel, 1, id_ - ic))


def silencio(env_cam, env_ev, a, c, d_cam, d_ev, nivel=0.0):
    """Silencio de `a` a `c` (tiempos sin voz absolutos). Los fondos vuelven en d_cam; los eventos justo antes del golpe en d_ev."""
    dip(env_cam, a - 0.1, a, c, d_cam, nivel)
    dip(env_ev, a - 0.1, a, c - 0.03, d_ev, nivel)


def nota_silbido(i, dur=0.34, lejano=False, seed=0):
    """Una nota del silbido: sinusoide con vibrato leve, entrada con soplo de aire y cola suave."""
    f = NOTAS_HZ[i] * (0.992 if lejano else 1.0)
    t = tt(dur)
    f_t = f * (0.97 + 0.03 * np.minimum(1, t / 0.05)) * (1 + 0.004 * np.sin(2 * np.pi * 6.2 * t))
    fase = 2 * np.pi * np.cumsum(f_t) / SR
    tono = np.sin(fase) + 0.10 * np.sin(2 * fase)
    aire = band(noise(dur, 300 + seed + i), f * 0.8, f * 1.5) * 0.35
    env = np.minimum(1, t / 0.025) * np.exp(-np.maximum(0, t - dur * 0.45) / 0.09)
    s = norm((tono + aire) * env)
    if lejano:
        s = reverb(band(s, None, 2400), 2.4, 0.5, seed + i, 2500)
    return fade(s, 0.004, 0.05)


def silbido(ev, T0, dur=1.4, gain=0.5, lejano=False, notas=7, pan=0.0, seed=0):
    """Pone las `notas` primeras notas del silbido, repartidas en `dur` s desde T0 (tiempo sin voz): igual que notas.silbido()."""
    for i in range(notas):
        ev.add(nota_silbido(i, 0.36, lejano, seed), T0 + dur * i / 7, gain * (0.9 + 0.1 * i / 6), pan)


def pop_corcho():
    d = 0.25
    t = tt(d)
    s = thump(210, d, 0.04) + 0.8 * band(noise(d, 91), 900, 5200) * env_exp(len(t), 0.025)
    return norm(s)


def finalizar(cam, ev, env_cam, env_ev, voices, total_out, ganancia_db):
    cam.buf *= env_cam[:, None]
    ev.buf *= env_ev[:, None]
    bed = np.tanh((cam.buf + ev.buf) * 1.1)
    out = master(bed, total_out, voices, 0.5, bed_peak=0.82, duck=0.55, voice_peak=0.95)
    out = np.tanh(out * 1.5) / np.tanh(1.5)
    return out * 10 ** (ganancia_db / 20), total_out
