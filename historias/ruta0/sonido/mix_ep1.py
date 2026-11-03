"""Banda sonora de Ruta 0, parte 1 "El último camión" (con narrador por radio)."""
import numpy as np
from motor.config import SR
from motor.audio import sfx, ambient
from motor.audio.synth import noise, band, norm, thump, pad
from motor.audio.voice import aullido
from historias.ruta0.sonido import comun as C

GANANCIA_DB = 0.0


def build():
    cam, ev, voices, total_out, T, M, D = C.contexto("ep1")
    env_c, env_e = np.ones(len(cam.buf)), np.ones(len(ev.buf))
    fin = {k: T[k] + D[k] for k in T}

    # =============== FONDOS ===============
    cam.add(ambient.lluvia(fin["s04"] - T["s01"] + 0.6, 3, 1.0), T["s01"], 0.30)                      # lluvia en lámina (exterior)
    cam.add(ambient.motor_camion(D["s01"] + 0.5, 1.0, 4), T["s01"], 0.20, 0.0)
    cam.add(pad([41.2, 55.0], D["s02"] + 0.3, 0.6, 0.4, 480, 6), T["s02"], 0.16)
    cam.add(ambient.wind(D["s03"] + 0.6, 5, 90, 700, 0.4), T["s03"], 0.12)
    cam.add(ambient.motor_camion(3.4, 1.0, 5), T["s03"] + 0.3, 0.16, 0.5)                              # el último camión se aleja
    cam.add(ambient.motor_camion(D["s04"] - 0.2, 1.0, 6), T["s04"] + 0.2, 0.26)                        # el camión sin número se acerca
    cam.add(ambient.lluvia(fin["s09"] - T["s05"] + 0.6, 7, 0.6, True), T["s05"], 0.20)                 # lluvia contra el vidrio, por dentro
    cam.add(ambient.motor_camion(M["s06"].SILENCIO[0] - 0.0 + D["s05"], 1.0, 8), T["s05"], 0.26)        # motor por dentro
    cam.add(pad([49.0, 73.4, 82.4], M["s06"].SILENCIO[0] + D["s05"], 1.2, 0.2, 380, 4), T["s05"], 0.14)
    cam.add(ambient.fluorescente(D["s05"] + D["s06"], None, seed=3), T["s05"], 0.045)                  # la luz amarilla que zumba
    cam.add(ambient.motor_camion(fin["s09"] - T["s06"] - M["s06"].SILENCIO[1] + 0.1 - 1.0, 0.8, 9), T["s06"] + M["s06"].SILENCIO[1] + 0.9, 0.28)   # vuelve más grave
    cam.add(ambient.lluvia(D["s09"] + 0.6, 11, 1.0), T["s09"], 0.30)
    cam.add(ambient.motor_camion(D["s09"] - 0.6, 1.2, 12), T["s09"], 0.20, 0.3)
    cam.add(pad([41.2, 61.7, 82.4], D["s07"] + D["s08"], 1.5, 0.5, 400, 7), T["s07"], 0.16)

    # silencios que preparan los golpes: s06 (todo se va) y s08 (antes de la mano)
    s6, s8 = M["s06"], M["s08"]
    C.silencio_previo(T, T["s06"] + s6.SILENCIO[0], 0, T["s06"] + s6.SILENCIO[1], T["s06"] + s6.SILENCIO[1] + 0.9, T["s06"] + s6.SILENCIO[1] - 0.02, env_c, env_e)
    C.silencio_previo(T, T["s08"] + 5.7, 0, T["s08"] + s8.SUSTO, T["s08"] + s8.SUSTO + 0.6, T["s08"] + s8.SUSTO - 0.01, env_c, env_e)

    # =============== EVENTOS ===============
    # s01: frenos de aire y golpe antes de la voz
    ev.add(sfx.frenos_aire(1.5, 1), T["s01"] + M["s01"].SUSTO, 0.55, 0.2)
    ev.add(sfx.susto(), T["s01"] + M["s01"].SUSTO, 0.42)
    ev.add(sfx.tinnitus(2.4), T["s01"] + 0.4, 0.03)
    # s02: riser corto que se corta en seco + golpe del título
    ev.add(sfx.riser(3.4, 1), T["s02"] + 0.4, 0.13)
    ev.add(thump(44, 1.6, 0.5), T["s02"] + 0.45, 0.45)
    # s03: charcos, perro lejano
    for i, a in enumerate((1.2, 2.5, 4.2, 5.8)):
        ev.add(sfx.paso_charco(i), T["s03"] + a, 0.12, -0.4)
    ev.add(aullido(3.0, 2), T["s03"] + 4.0, 0.10, 0.6)
    # s04: frenos, puertas neumáticas, el paso de Iván al subir
    s4 = M["s04"]
    ev.add(sfx.frenos_aire(1.6, 2), T["s04"] + s4.FRENA, 0.5, 0.3)
    ev.add(sfx.puertas_neumaticas(1.2, 1), T["s04"] + s4.PUERTAS, 0.5, 0.4)
    ev.add(sfx.step_metal(1, 150), T["s04"] + 7.1, 0.28, 0.3)
    ev.add(sfx.step_metal(2, 160), T["s04"] + 7.5, 0.26, 0.4)
    ev.add(sfx.puertas_neumaticas(1.0, 2), T["s04"] + 7.9, 0.4, 0.4)
    # s05: el papel del boleto y los pasos de Iván por el pasillo
    ev.add(sfx.cloth_rip(0.3, 31), T["s05"] + M["s05"].BOLETO, 0.12, 0.6)
    for i, a in enumerate((3.8, 4.3, 4.8, 5.4, 6.0, 6.6, 7.2)):
        ev.add(sfx.step_metal(i, 140), T["s05"] + a, 0.16, 0.2 - 0.1 * i)
    ev.add(sfx.cloth_rip(0.5, 32), T["s05"] + M["s05"].SENTADO, 0.14, 0.0)
    # s06: tras el silencio, solo la respiración y el latido de Iván + glitch suave
    for i, a in enumerate((0.9, 1.9)):
        pass
    for i in range(3):
        ev.add(sfx.breath(0.8, i % 2 == 0, 40 + i), T["s06"] + s6.GLITCH + 0.2 + i * 0.5, 0.20, -0.2)
    ev.add(sfx.heartbeat(), T["s06"] + s6.GLITCH, 0.42)
    ev.add(sfx.heartbeat(), T["s06"] + s6.GLITCH + 0.9, 0.44)
    ev.add(sfx.tinnitus(1.8), T["s06"] + s6.GLITCH + 0.1, 0.03)
    # s07: el timbre de parada y los frenos
    ev.add(sfx.timbre_parada(), T["s07"] + M["s07"].TIMBRE, 0.5)
    ev.add(sfx.frenos_aire(1.5, 3), T["s07"] + M["s07"].TIMBRE + 1.0, 0.4, 0.2)
    # s08: se detiene, puertas, la mano pálida y el susto principal
    ev.add(sfx.frenos_aire(1.5, 4), T["s08"] + 0.4, 0.45, 0.3)
    ev.add(sfx.puertas_neumaticas(1.2, 3), T["s08"] + 1.0, 0.45, 0.4)
    ev.add(sfx.riser(1.0, 6), T["s08"] + 4.6, 0.10)
    ev.add(sfx.susto(), T["s08"] + s8.SUSTO, 0.55)
    ev.add(sfx.cold_touch(1.8), T["s08"] + s8.SUSTO + 0.1, 0.22, -0.3)
    ev.add(sfx.tinnitus(2.4), T["s08"] + s8.SUSTO + 0.3, 0.04)
    ev.add(sfx.puertas_neumaticas(1.1, 4), T["s08"] + 9.0, 0.45, 0.4)
    # s09: motor que se aleja y el clic del "0" que se apaga
    ev.add(sfx.tinnitus(2.4), T["s09"] + 3.0, 0.03)
    ev.add(sfx.radio_click(), T["s09"] + M["s09"].APAGA, 0.35)

    return C.finalizar(cam, ev, env_c, env_e, voices, total_out, GANANCIA_DB)
