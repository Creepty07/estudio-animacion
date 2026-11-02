"""Banda sonora de La Planchada, ep1 "La enfermera de las 3:00" (sin narrador): el sonido cuenta el miedo.

Capas: fondos continuos (fluorescente con el mismo parpadeo que se ve, viento, drone) + sonido de acción sincronizado
(goteo, reloj, monitor, hielo, murmullos, latido) + silencios que preparan cada golpe.
Regla de la enfermera: nunca suenan sus pasos; al aparecer se caen el reloj y el monitor y queda el goteo.
"""
import numpy as np
from motor.config import SR
from motor.audio import sfx, ambient
from motor.audio.synth import noise, band, norm, env_exp, fade, thump, pad
from motor.audio.master import master
from motor.audio.mixing import scene_offsets, new_track
from historias.planchada.sonido import comun as C


GANANCIA_DB = -2.8                # se ajusta midiendo la banda (verificador-video: referencia -13.3 / -13.6 LUFS)


def build():
    sc, total = scene_offsets("ep1")
    cam, total_out, _ = new_track("ep1")                      # fondos (se pueden apagar antes de un golpe)
    ev, _, _ = new_track("ep1")                               # eventos
    T = {k.split("_")[0]: v[0] for k, v in sc.items()}
    M = {k.split("_")[0]: v[1] for k, v in sc.items()}
    D = {k: M[k].DURATION for k in M}
    fin = {k: T[k] + D[k] for k in T}

    # =============== FONDOS ===============
    # s01 gancho: zumbido desde el cuadro 0
    C.hum(cam, T["s01"], D["s01"], 11, "parpadea", 0.16)
    # s02 título: drone frío bajo el título
    cam.add(pad([41.2, 61.7, 82.4], D["s02"] + 0.3, 0.6, 0.4, 500, 6), T["s02"], 0.18)
    # s03 hospital: viento, grillos lejanos, zumbido de la ventana encendida
    cam.add(ambient.wind(D["s03"] + 0.8, 5, 90, 700, 0.5), T["s03"], 0.24)
    cam.add(ambient.crickets(D["s03"] + 0.4, 7, 2), T["s03"], 0.05, 0.4)
    cam.add(ambient.fluorescente(D["s03"], None, seed=3), T["s03"] + 1.5, 0.05)
    # s04 cuarto: fluorescente que parpadea, goteo, reloj, monitor
    C.hum(cam, T["s04"], D["s04"], 3, "parpadea", 0.12, lo=0.0)
    cam.add(pad([41.2, 55.0], D["s04"] + D["s05"], 1.2, 0.2, 400, 4), T["s04"], 0.10)
    # s05 → s10: viento por la ventana abierta (entra a las 1.6 de s05) y drone grave que crece
    cam.add(ambient.wind(fin["s09"] - T["s05"] - 1.6 + 0.6, 8, 120, 900, 0.5), T["s05"] + 1.6, 0.26)
    cam.add(pad([41.2, 61.7, 82.4, 87.3], fin["s10"] - T["s06"], 2.0, 0.4, 420, 7), T["s06"], 0.22)
    cam.add(pad([55.0, 58.3, 110.0], fin["s10"] - T["s08"], 3.0, 0.4, 380, 5), T["s08"], 0.13)
    C.hum(cam, T["s06"], fin["s09"] - T["s06"], 6, "inestable", 0.035, lo=0.1)
    # s08: voces que no se entienden bajo cada línea
    for k, a in enumerate(M["s08"].LINEAS):
        cam.add(ambient.murmullos(3.3, 12 + k, 2), T["s08"] + a, 0.075, -0.4 + 0.8 * k)
    # s10: drone y latido hasta el corte a negro
    cam.add(pad([36.7, 55.0, 73.4], M["s10"].NEGRO + 0.2, 0.3, 0.2, 360, 9), T["s10"], 0.2)

    # silencios que preparan los golpes (s05 previo al susto, s09 antes del corte, s10 final)
    env = np.ones(len(cam.buf))
    s5, s9 = M["s05"], M["s09"]
    C.dip(cam.buf, env, T["s05"] + s5.SILENCIO[0] - 0.05, T["s05"] + s5.SILENCIO[0] + 0.05, T["s05"] + s5.SUSTO, T["s05"] + s5.SUSTO + 0.5, 0.0)
    C.dip(cam.buf, env, T["s09"] + s9.SILENCIO[0] - 0.05, T["s09"] + s9.SILENCIO[0] + 0.05, T["s09"] + s9.SUSTO, T["s09"] + s9.SUSTO + 1.2, 0.0)
    cam.buf *= env[:, None]
    # los eventos también se callan en esos silencios (recuperan justo antes del golpe para no comerse su ataque)
    env_ev = np.ones(len(ev.buf))
    C.dip(ev.buf, env_ev, T["s05"] + s5.SILENCIO[0] - 0.05, T["s05"] + s5.SILENCIO[0] + 0.05, T["s05"] + s5.SUSTO - 0.03, T["s05"] + s5.SUSTO - 0.01, 0.0)
    C.dip(ev.buf, env_ev, T["s09"] + s9.SILENCIO[0] - 0.05, T["s09"] + s9.SILENCIO[0] + 0.05, T["s09"] + s9.SUSTO - 0.03, T["s09"] + s9.SUSTO - 0.01, 0.0)
    ev.buf *= env_ev[:, None]

    # =============== EVENTOS ===============
    # --- s01: golpe con glitch y tinnitus que se apaga ---
    ev.add(sfx.susto(), T["s01"] + M["s01"].SUSTO, 0.5)
    ev.add(sfx.tinnitus(3.0), T["s01"] + M["s01"].SUSTO + 0.2, 0.05)

    # --- s02: riser corto que se corta en seco, y un golpe grave al entrar el título ---
    ev.add(sfx.riser(3.4, 1), T["s02"] + 0.4, 0.14)
    ev.add(thump(44, 1.6, 0.5), T["s02"] + 0.45, 0.45)

    # --- s03: perro lejano (sin sirenas) ---
    from motor.audio.voice import aullido
    ev.add(aullido(3.0, 2), T["s03"] + 2.2, 0.10, 0.6)

    # --- s04: goteo, reloj (tic grave), monitor (pitido suave) ---
    C.goteo(ev, T["s04"], D["s04"], 0.22)
    C.reloj(ev, T["s04"], D["s04"], 0.17, 0.0, M["s04"].RELOJ_TIC)
    C.monitor(ev, T["s04"], D["s04"], 0.11, 0.5, 1.0)
    C.goteo(ev, T["s05"], 1.2, 0.20)
    C.reloj(ev, T["s05"], 1.2, 0.17, 0.0, 1.0)
    C.monitor(ev, T["s05"], 1.2, 0.11, 0.5, 1.0)

    # --- s05: 3:00 (campanada baja), silencio, y la ventana: susto 1 ---
    ev.add(sfx.bell(98.0, 0.85, 2), T["s05"] + 0.3, 0.12)                      # campanada breve: no debe tapar el silencio
    ev.add(sfx.susto(), T["s05"] + s5.SUSTO, 0.55)
    ev.add(thump(58, 1.2, 0.3) + 0.5 * band(noise(1.2, 5), 100, 2500) * env_exp(int(1.2 * SR), 0.25), T["s05"] + s5.SUSTO, 0.5)
    ev.add(ambient.wind(2.2, 14, 150, 1800, 0.2), T["s05"] + s5.SUSTO - 0.05, 0.55, -0.2)         # la ráfaga
    ev.add(sfx.creak(0.8, 3), T["s05"] + s5.SUSTO + 0.05, 0.25, -0.5)
    ev.add(sfx.tinnitus(2.4), T["s05"] + s5.SUSTO + 0.3, 0.04)

    # --- s06: ella ya está dentro. Sin pasos. Goteo, silbido en el oído, aliento de Rafa ---
    C.goteo(ev, T["s06"], D["s06"], 0.24, 0.5)
    ev.add(sfx.tinnitus(5.0), T["s06"] + M["s06"].APARECE, 0.035)
    ev.add(sfx.cold_touch(1.8), T["s06"] + 0.2, 0.14, 0.3)
    for i, a in enumerate((1.6, 3.3, 5.0, 6.7)):
        ev.add(sfx.breath(0.7, i % 2 == 0, 52 + i), T["s06"] + a, 0.07, -0.5)

    # --- s07: frío: viento por la ventana, hielo que cruje, goteo ---
    C.goteo(ev, T["s07"], D["s07"], 0.22)
    for i, a in enumerate((0.5, 1.5, 2.6, 3.6, 4.5)):
        ev.add(C.hielo(i), T["s07"] + a, 0.20, -0.5 + 0.2 * i)
    ev.add(sfx.cold_touch(2.4), T["s07"] + 0.3, 0.16)
    ev.add(sfx.breath(0.8, True, 61), T["s07"] + 3.1, 0.08, -0.4)

    # --- s08: tela almidonada al moverse, el latido de Rafa entra y crece ---
    for a, sd in ((0.5, 1), (1.5, 2), (3.5, 3), (4.2, 4)):
        ev.add(sfx.cloth_rip(0.3, 40 + sd), T["s08"] + a, 0.10, 0.2)
    C.goteo(ev, T["s08"], D["s08"], 0.20)
    t, k = 0.6, 0
    while t < D["s08"] - 0.3:
        ev.add(sfx.heartbeat(), T["s08"] + t, min(0.40, 0.18 + 0.02 * k))
        t += 1.15 - min(0.3, 0.025 * k)
        k += 1

    # --- s09: el latido acelera → silencio → susto 2 ---
    for k, b in enumerate(s9.LATIDOS):
        ev.add(sfx.heartbeat(), T["s09"] + b, 0.45 + 0.03 * k)
    ev.add(sfx.susto(), T["s09"] + s9.SUSTO, 0.55)
    ev.add(sfx.tinnitus(2.6), T["s09"] + s9.SUSTO + 0.2, 0.06)
    C.goteo(ev, T["s09"], D["s09"], 0.20, s9.SUSTO + 0.5)

    # --- s10: tres golpes graves (uno por tarjeta) y el latido hasta el corte a negro ---
    s10 = M["s10"]
    for i, a in enumerate(s10.TARJETAS):
        ev.add(thump(52 - 4 * i, 1.4, 0.4) + 0.3 * band(noise(1.4, 30 + i), 120, 2500) * env_exp(int(1.4 * SR), 0.12),
               T["s10"] + a, 0.70)
    t, k = 0.3, 0
    while t < s10.NEGRO - 0.2:
        ev.add(sfx.heartbeat(), T["s10"] + t, 0.30 + 0.01 * min(k, 12))
        t += 1.0 - min(0.25, 0.02 * k)
        k += 1
    # =============== MEZCLA FINAL ===============
    bed = cam.buf + ev.buf
    corte = int((T["s10"] + s10.NEGRO) * SR)                  # corte a negro seco: todo se apaga de golpe
    bed[corte:] = 0.0
    bed = np.tanh(bed * 1.1)
    out = master(bed, total_out, [], 0.05, bed_peak=0.9)
    out[corte:] = 0.0
    out = np.tanh(out * 1.8) / np.tanh(1.8)
    out = out * 10 ** (GANANCIA_DB / 20)                      # nivel de la casa (~ -13.5 LUFS, pico < -1 dBFS)
    return out, total_out
