"""Banda sonora de Ruta 0, parte 3 "La última parada" (con narrador por radio)."""
import numpy as np
from motor.config import SR
from motor.audio import sfx, ambient
from motor.audio.synth import noise, band, norm, thump, pad, reverb
from historias.ruta0.sonido import comun as C

GANANCIA_DB = 0.0


def build():
    cam, ev, voices, total_out, T, M, D = C.contexto("ep3")
    env_c, env_e = np.ones(len(cam.buf)), np.ones(len(ev.buf))
    fin = {k: T[k] + D[k] for k in T}
    s9, s6, s7 = M["s09"], M["s06"], M["s07"]

    # =============== FONDOS ===============
    cam.add(ambient.motor_camion(D["s01"] + D["s02"] + D["s03"] + D["s04"], 1.0, 41), T["s01"], 0.22)       # el motor, grave, por dentro
    cam.add(ambient.lluvia(D["s01"] + D["s02"] + D["s03"] + D["s04"] + 0.4, 42, 0.6, True), T["s01"], 0.17)
    cam.add(ambient.fluorescente(D["s01"] + D["s03"] + D["s04"] + 3.0, None, seed=9), T["s01"], 0.045)
    cam.add(pad([36.7, 55.0, 73.4], D["s04"] + 1.0, 1.5, 1.2, 360, 9), T["s04"], 0.22)                      # todo baja: un drone muy grave
    cam.add(ambient.lluvia(D["s05"] + D["s06"] + 0.4, 43, 1.0), T["s05"] + 2.2, 0.28)
    cam.add(ambient.motor_camion(D["s05"] + 1.0, 1.0, 44), T["s05"] + 2.2, 0.22)
    cam.add(ambient.motor_camion(D["s05"] - 4.6, 1.0, 45), T["s05"] + 4.6, 0.18)
    cam.add(ambient.wind(D["s07"] + D["s08"], 46, 80, 500, 0.3), T["s07"], 0.10)                              # ya no llueve: aire quieto
    cam.add(ambient.crickets(D["s07"] + D["s08"], 47, 3), T["s07"], 0.12, -0.3)
    cam.add(pad([73.4, 110.0, 146.8], D["s07"] + D["s08"] + D["s09"], 1.5, 1.0, 600, 13), T["s07"], 0.16)
    cam.add(ambient.lluvia(D["s09"] + 0.5, 54, 0.5, True), T["s09"], 0.12)
    cam.add(ambient.motor_camion(D["s09"] - 0.5, 1.0, 55), T["s09"], 0.10, 0.3)                                # grillos y ciudad lejana
    cam.add(ambient.murmullos(D["s07"], 48, 2), T["s07"] + 1.0, 0.02, 0.5)
    cam.add(ambient.lluvia(D["s10"] + 0.5, 49, 1.0), T["s10"], 0.26)
    cam.add(ambient.motor_camion(D["s10"] - 0.8, 1.2, 50), T["s10"], 0.16, 0.3)
    cam.add(ambient.motor_camion(4.2, 1.0, 51), T["s09"] + s9.SUSTO, 0.0)

    # silencios previos: s06 (antes del golpe de blanco), s09 (antes del susto final)
    C.silencio_previo(T, T["s06"] + s6.SILENCIO[0], 0, T["s06"] + s6.SILENCIO[1], T["s06"] + s6.SILENCIO[1] + 0.2, T["s06"] + s6.SILENCIO[1] - 0.01, env_c, env_e)
    C.silencio_previo(T, T["s09"] + s9.SUSTO - 0.55, 0, T["s09"] + s9.SUSTO, T["s09"] + s9.SUSTO + 0.9, T["s09"] + s9.SUSTO - 0.01, env_c, env_e)
    # el motor "se va de golpe" y todo se corta con el blanco
    corte = int(C.TMAP(T["s06"] + s6.BLANCO[1]) * SR)
    fin_blanco = int(C.TMAP(T["s07"]) * SR)
    env_c[corte:fin_blanco] = 0.0
    env_e[corte:fin_blanco] = 0.0

    # =============== EVENTOS ===============
    ev.add(sfx.susto(), T["s01"] + M["s01"].SUSTO, 0.42)
    ev.add(sfx.frenos_aire(1.4, 10), T["s01"] + 0.15, 0.30, 0.2)
    ev.add(sfx.riser(3.4, 9), T["s02"] + 0.4, 0.13)
    ev.add(thump(44, 1.6, 0.5), T["s02"] + 0.45, 0.45)
    for i, a in enumerate((0.0, 1.6, 3.2, 4.7, 6.2)):                                                         # un golpecito por cada corte del repaso
        ev.add(sfx.tick(1300, 0.06), T["s03"] + a, 0.10)
    for i in range(7):
        ev.add(sfx.heartbeat(), T["s03"] + 0.4 + i * 1.1, 0.20)
    ev.add(sfx.tinnitus(5.0), T["s04"] + 0.5, 0.025)
    ev.add(sfx.cold_touch(2.0), T["s04"] + 2.4, 0.10, -0.3)
    # s05: timbre de parada, el camión frena en una parada a oscuras, puertas
    s5 = M["s05"]
    ev.add(sfx.timbre_parada(), T["s05"] + s5.TIMBRE, 0.5)
    ev.add(sfx.frenos_aire(1.6, 11), T["s05"] + s5.FRENA, 0.5, 0.3)
    ev.add(sfx.puertas_neumaticas(1.2, 10), T["s05"] + s5.FRENA + 0.5, 0.45, 0.4)
    # s06: Iván baja: charcos, puertas que se cierran, y el golpe de blanco
    ev.add(sfx.puertas_neumaticas(1.1, 11), T["s06"] + 1.0, 0.40, 0.5)
    t = 0.5
    k = 0
    while t < s6.SILENCIO[0] - 0.1:
        ev.add(sfx.paso_charco(k), T["s06"] + t, 0.34, 0.2)
        t += 0.55
        k += 1
    ev.add(sfx.riser(0.7, 10), T["s06"] + s6.BLANCO[0] - 0.7, 0.10)
    ev.add(thump(40, 1.6, 0.5) + 0.4 * band(noise(1.6, 10), 80, 2000) * np.exp(-np.arange(int(1.6 * SR)) / SR / 0.2), T["s06"] + s6.BLANCO[0], 0.70)
    ev.add(sfx.frenos_aire(1.3, 12), T["s06"] + s6.BLANCO[0] + 0.02, 0.55)
    # s07: gota del techito, la ciudad, vibra el celular
    for i, a in enumerate((1.3, 2.4, 3.7)):
        from motor.audio.agua import gota
        ev.add(gota(i), T["s07"] + a, 0.18, -0.4)
    ev.add(sfx.celular_vibra(1.1), T["s07"] + s7.VIBRA, 0.40, 0.3)
    ev.add(sfx.celular_vibra(1.1), T["s07"] + s7.VIBRA + 1.2, 0.30, 0.3)
    # s08: teclas, pasos, un coche que pasa y se aleja
    ev.add(sfx.teclas(21, 1, 2.2), T["s08"] + 0.2, 0.22, 0.2)
    ev.add(sfx.celular_vibra(0.5), T["s08"] + 2.7, 0.10, 0.2)
    t, k = 3.3, 0
    while t < D["s08"] - 0.4:
        ev.add(sfx.paso_charco(10 + k), T["s08"] + t, 0.16, -0.1 + 0.05 * k)
        t += 0.55
        k += 1
    carro = M["s08"].CARRO
    ev.add(ambient.motor_camion(carro[1] - carro[0], 1.6, 52) * np.hanning(int((carro[1] - carro[0]) * SR)), T["s08"] + carro[0], 0.22, 0.0)
    ev.add(sfx.whoosh(1.2, 400, 3000, 14), T["s08"] + carro[0] + 0.4, 0.15, 0.4)
    # s09: el timbre y el motor que solo suenan "en el reflejo", y el susto final
    ev.add(sfx.riser(0.5, 11), T["s09"] + s9.SUSTO - 0.55, 0.06)
    ev.add(reverb(sfx.timbre_parada(), 1.2, 0.35, 5), T["s09"] + s9.SUSTO, 0.5, 0.0)
    ev.add(sfx.susto(), T["s09"] + s9.SUSTO, 0.55)
    ev.add(band(ambient.motor_camion(4.0, 0.9, 53), 40, 700), T["s09"] + s9.SUSTO + 0.2, 0.28, 0.0)
    ev.add(sfx.cold_touch(1.8), T["s09"] + s9.SUSTO + 0.3, 0.20, 0.3)
    ev.add(sfx.tinnitus(3.0), T["s09"] + s9.SUSTO + 0.3, 0.05)
    # s10: el "0" parpadea y se apaga; tinnitus final
    ev.add(sfx.tinnitus(2.0), T["s10"] + 1.0, 0.03)
    ev.add(sfx.radio_click(), T["s10"] + M["s10"].APAGA, 0.35)
    return C.finalizar(cam, ev, env_c, env_e, voices, total_out, GANANCIA_DB)
