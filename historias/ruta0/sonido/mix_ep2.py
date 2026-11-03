"""Banda sonora de Ruta 0, parte 2 "Las paradas" (con narrador por radio)."""
import numpy as np
from motor.config import SR
from motor.audio import sfx, ambient
from motor.audio.synth import noise, band, norm, thump, pad, reverb
from historias.ruta0.sonido import comun as C

GANANCIA_DB = 0.0


def build():
    cam, ev, voices, total_out, T, M, D = C.contexto("ep2")
    env_c, env_e = np.ones(len(cam.buf)), np.ones(len(ev.buf))
    fin = {k: T[k] + D[k] for k in T}

    # =============== FONDOS ===============
    cam.add(ambient.lluvia(D["s01"] + 0.5, 21, 1.0), T["s01"], 0.26)
    cam.add(ambient.wind(D["s01"] + 0.5, 22, 90, 700, 0.45), T["s01"], 0.16)
    cam.add(pad([41.2, 61.7, 82.4], D["s02"] + 0.3, 0.5, 0.4, 460, 5), T["s02"], 0.16)
    cam.add(ambient.motor_camion(D["s02"] + D["s03"], 1.0, 23), T["s02"], 0.18)
    cam.add(ambient.lluvia(D["s03"] + 0.4, 24, 0.6, True), T["s03"], 0.20)
    cam.add(ambient.lluvia(D["s04"] + D["s05"] + 0.4, 25, 0.9), T["s04"], 0.22)                         # curva y puente: lluvia afuera
    cam.add(ambient.wind(D["s04"] + D["s05"], 26, 100, 800, 0.5), T["s04"], 0.16)
    cam.add(ambient.crickets(D["s04"], 27, 2), T["s04"], 0.04, -0.4)
    cam.add(ambient.water(D["s05"] + 0.6, 28), T["s05"] - 0.3, 0.30)                                     # el río bajo el puente
    cam.add(ambient.motor_camion(D["s04"] + 0.4, 1.0, 29), T["s04"], 0.14, 0.6)
    cam.add(ambient.motor_camion(fin["s09"] - T["s06"] - 1.0, 1.0, 30), T["s06"], 0.26)                  # de vuelta por dentro
    cam.add(ambient.lluvia(fin["s09"] - T["s06"], 31, 0.6, True), T["s06"], 0.18)
    cam.add(ambient.fluorescente(D["s06"] + D["s07"] + D["s08"], None, seed=6), T["s06"], 0.06)           # zumbido del tablero y la luz amarilla
    cam.add(pad([49.0, 73.4, 98.0], D["s06"] + D["s07"] + D["s08"], 1.0, 0.5, 400, 8), T["s06"], 0.14)
    cam.add(ambient.lluvia(D["s09"] + 0.6, 32, 1.0), T["s09"] + 3.2, 0.26)

    # silencios previos: s06 (se prende IVÁN) y s08 (la fecha de mañana)
    s6, s8 = M["s06"], M["s08"]
    C.silencio_previo(T, T["s06"] + s6.SILENCIO[0], 0, T["s06"] + s6.SUSTO, T["s06"] + s6.SUSTO + 0.6, T["s06"] + s6.SUSTO - 0.01, env_c, env_e)
    C.silencio_previo(T, T["s08"] + s8.SILENCIO[0], 0, T["s08"] + s8.SUSTO, T["s08"] + s8.SUSTO + 0.7, T["s08"] + s8.SUSTO - 0.01, env_c, env_e)

    # =============== EVENTOS ===============
    ev.add(sfx.frenos_aire(1.5, 5), T["s01"] + M["s01"].SUSTO, 0.55, 0.2)
    ev.add(sfx.susto(), T["s01"] + M["s01"].SUSTO, 0.42)
    ev.add(sfx.puertas_neumaticas(1.1, 5), T["s01"] + 0.7, 0.40, 0.3)
    ev.add(sfx.riser(3.4, 7), T["s02"] + 0.4, 0.13)
    ev.add(thump(44, 1.6, 0.5), T["s02"] + 0.45, 0.45)
    for i, a in enumerate((0.5, 1.0, 1.5, 2.0, 2.5)):                                                     # latido del repaso
        ev.add(sfx.heartbeat(), T["s03"] + 3.8 + i * 0.9, 0.20 + 0.03 * i)
    # s04: curva: frenos, puertas, rechinido de llantas lejano que se corta, glitch en la foto
    s4 = M["s04"]
    ev.add(sfx.frenos_aire(1.6, 6), T["s04"] + 0.3, 0.45, 0.4)
    ev.add(sfx.puertas_neumaticas(1.2, 6), T["s04"] + 0.8, 0.40, 0.4)
    ev.add(reverb(sfx.llantas_rechinido(1.6, 1), 1.4, 0.35, 3), T["s04"] + s4.RECHINIDO - 1.3, 0.12, 0.6)  # lejano y apagado por el eco
    ev.add(sfx.susto(), T["s04"] + s4.SUSTO, 0.30)
    ev.add(sfx.tinnitus(2.0), T["s04"] + s4.SUSTO + 0.2, 0.035)
    ev.add(sfx.puertas_neumaticas(1.0, 7), T["s04"] + 3.3, 0.35, 0.4)
    # s05: puente: frenos, puertas, motor que arranca con el asiento vacío
    ev.add(sfx.frenos_aire(1.5, 7), T["s05"] + 0.3, 0.45, 0.4)
    ev.add(sfx.puertas_neumaticas(1.2, 8), T["s05"] + 0.7, 0.40, 0.4)
    ev.add(sfx.puertas_neumaticas(1.0, 9), T["s05"] + 4.0, 0.35, 0.4)
    ev.add(ambient.motor_camion(3.0, 0.9, 33), T["s05"] + 5.2, 0.12)
    # s06: sube la tensión, silencio, se prende IVÁN
    ev.add(sfx.riser(1.4, 8), T["s06"] + s6.SILENCIO[0] - 1.4, 0.09)
    ev.add(sfx.susto(), T["s06"] + s6.SUSTO, 0.50)
    ev.add(sfx.cold_touch(1.6), T["s06"] + s6.SUSTO + 0.1, 0.18)
    ev.add(sfx.tinnitus(2.4), T["s06"] + s6.SUSTO + 0.3, 0.04)
    # s07: el latido de Iván se acelera
    t, k = 0.1, 0
    while t < D["s07"] - 0.2:
        ev.add(sfx.heartbeat(), T["s07"] + t, 0.28 + 0.015 * k)
        t += max(0.40, 0.95 - 0.1 * k)
        k += 1
    # s08: se corta todo, la fecha de mañana, tinnitus
    ev.add(sfx.tick(1900, 0.08), T["s08"] + 2.85, 0.14)
    ev.add(sfx.susto(), T["s08"] + s8.SUSTO, 0.55)
    ev.add(sfx.tinnitus(2.6), T["s08"] + s8.SUSTO + 0.2, 0.05)
    # s09: se aleja, timbre de parada lejano
    ev.add(sfx.frenos_aire(1.2, 8), T["s09"] + 3.3, 0.18, 0.2)
    ev.add(reverb(sfx.timbre_parada(), 1.6, 0.4, 4), T["s09"] + 5.0, 0.12, 0.6)
    return C.finalizar(cam, ev, env_c, env_e, voices, total_out, GANANCIA_DB)
