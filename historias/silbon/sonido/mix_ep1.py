"""Banda sonora de "Las reglas del Silbón": cama de grillos/viento/farol, silbido de siete notas, ladridos, huesos y silencios antes de cada susto.
Todo se coloca con las constantes de tiempo de las escenas (en mayúsculas), así el sonido cae justo cuando se ve."""
import numpy as np
from motor.audio import sfx, ambient
from motor.audio.animales import ladridos, aullido
from motor.audio.synth import pad, thump
from historias.silbon.sonido import comun as C

GANANCIA_DB = -13.0           # provisional (voz de prueba); se reajusta al llegar la voz real: objetivo -13.3 a -13.6 LUFS


def build():
    cam, ev, voices, total_out, T, M, D = C.contexto("ep1")
    env_c, env_e = np.ones(len(cam.buf)), np.ones(len(ev.buf))

    # =============== FONDOS ===============
    cam.add(ambient.crickets(D["s01"] + D["s02"] + 0.6, 3, 3), T["s01"], 0.12)
    cam.add(ambient.wind(D["s01"] + D["s02"] + 0.6, 5, 90, 700, 0.5), T["s01"], 0.10)
    cam.add(pad([55.0, 82.4], D["s01"] + 0.3, 0.6, 0.6, 500, 6), T["s01"], 0.14)
    interior = sum(D[k] for k in ("s03", "s04", "s05"))
    cam.add(ambient.lamp_hum(interior + 0.4, 55.0), T["s03"], 0.08)
    cam.add(ambient.wind(interior + 0.4, 8, 70, 420, 0.3), T["s03"], 0.07)
    cam.add(pad([49.0, 73.4], interior + 0.4, 1.2, 0.8, 380, 4), T["s03"], 0.13)
    cam.add(ambient.crickets(D["s06"] + 0.5, 4, 3), T["s06"], 0.12)
    cam.add(ambient.wind(D["s06"] + 0.5, 9, 90, 700, 0.4), T["s06"], 0.09)
    resto = sum(D[k] for k in ("s07", "s08", "s09", "s10", "s11", "s12"))
    cam.add(ambient.lamp_hum(resto + 0.4, 55.0), T["s07"], 0.08)
    cam.add(pad([41.2, 61.7, 82.4], resto + 0.4, 1.5, 1.0, 420, 7), T["s07"], 0.15)
    cam.add(ambient.wind(resto + 0.4, 12, 70, 420, 0.3), T["s07"], 0.06)

    # silencios que preparan cada susto (los fondos y los eventos se cortan; la voz no)
    m1, m4, m9, m10, m11, m12 = M["s01"], M["s04"], M["s09"], M["s10"], M["s11"], M["s12"]
    C.silencio(env_c, env_e, T["s01"] + 2.0, T["s01"] + m1.SUSTO, T["s01"] + m1.SUSTO + 0.8, T["s01"] + m1.SUSTO - 0.01)
    C.silencio(env_c, env_e, T["s04"] + 6.7, T["s04"] + m4.SUSTO, T["s04"] + m4.SUSTO + 0.8, T["s04"] + m4.SUSTO - 0.01)
    C.silencio(env_c, env_e, T["s09"] + m9.SILENCIO[0], T["s09"] + m9.SILENCIO[1], T["s09"] + m9.SILENCIO[1] + 0.2, T["s09"] + m9.SILENCIO[1] - 0.01)
    C.silencio(env_c, env_e, T["s10"] + 2.9, T["s10"] + m10.SACO, T["s10"] + m10.SACO + 0.8, T["s10"] + m10.SACO - 0.01)
    C.silencio(env_c, env_e, T["s11"] + 2.6, T["s11"] + m11.OJO, T["s11"] + m11.OJO + 0.8, T["s11"] + m11.OJO - 0.01)
    C.silencio(env_c, env_e, T["s12"] + m12.APAGON - 0.05, T["s12"] + 7.6, T["s12"] + 7.8, T["s12"] + 7.6)

    # =============== EVENTOS ===============
    # s01 gancho: el silbido desde el primer cuadro y el golpe cuando aparece el ojo
    C.silbido(ev, T["s01"] + 0.0, 1.4, 0.55)
    ev.add(sfx.susto(), T["s01"] + m1.SUSTO, 0.50)
    ev.add(sfx.tinnitus(2.0), T["s01"] + m1.SUSTO + 0.2, 0.03)
    ev.add(sfx.heartbeat(), T["s01"] + m1.SUSTO + 0.5, 0.35)
    # s02: pasos en tierra, aullido lejano, el llanero corre y te agarra el brazo
    for i, a in enumerate((0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5)):
        ev.add(sfx.step_dirt(i), T["s02"] + a, 0.12, -0.3 + 0.07 * i)
    ev.add(aullido(3.0, 330, 640, 4, True), T["s02"] + 1.6, 0.09, 0.6)
    for i, a in enumerate((4.3, 4.55, 4.8)):
        ev.add(sfx.step_dirt(10 + i), T["s02"] + a, 0.20, 0.6)
    ev.add(sfx.cloth_rip(0.3, 51), T["s02"] + M["s02"].AGARRA, 0.18, 0.2)
    ev.add(sfx.breath(0.5, True, 61), T["s02"] + M["s02"].AGARRA + 0.2, 0.18)
    ev.add(sfx.creak(1.0, 3), T["s02"] + 7.0, 0.20, 0.3)
    # s03: la puerta se cierra, se escribe el letrero (cincel) y los demás duermen
    ev.add(thump(70, 0.5, 0.10), T["s03"] + 0.05, 0.40)
    for i in range(4):
        ev.add(sfx.chisel(i), T["s03"] + 0.9 + 0.65 * i, 0.22, 0.1)
    ev.add(sfx.breath(1.0, False, 71), T["s03"] + 2.2, 0.10, -0.5)
    # s04: silbido cerca (fuerte) y luego lejano (débil); el Silbón llena la ventana
    s4 = M["s04"]
    C.silbido(ev, T["s04"] + s4.SILBIDO_1, 1.2, 0.50, seed=5)
    C.silbido(ev, T["s04"] + s4.SILBIDO_2, 1.0, 0.30, lejano=True, seed=9)
    ev.add(sfx.riser(0.8, 4), T["s04"] + s4.SUSTO - 0.8, 0.0)
    ev.add(sfx.susto(), T["s04"] + s4.SUSTO, 0.55)
    ev.add(sfx.tinnitus(1.8), T["s04"] + s4.SUSTO + 0.2, 0.03)
    # s05: la botella cae sobre la mesa y la X roja se estampa
    s5 = M["s05"]
    ev.add(thump(95, 0.35, 0.08), T["s05"] + s5.BOTELLA, 0.30, -0.3)
    ev.add(sfx.clang(520), T["s05"] + s5.BOTELLA, 0.10, -0.3)
    ev.add(thump(60, 0.5, 0.12), T["s05"] + s5.X_ROJA, 0.45)
    ev.add(sfx.tick(900, 0.1), T["s05"] + s5.X_ROJA, 0.15)
    # s06: ladridos sin parar (tres perros, tres tonos)
    s6 = M["s06"]
    for i, b in enumerate(s6.LADRIDOS):
        ev.add(ladridos(1, 0.3, 420, 20 + i), T["s06"] + b, 0.55, -0.5)
        ev.add(ladridos(1, 0.3, 310, 40 + i), T["s06"] + b + 0.05, 0.50, 0.5)
        ev.add(ladridos(1, 0.3, 520, 60 + i), T["s06"] + b + 0.10, 0.35, 0.0)
    # s07: tres huesos caen (golpe seco) y se cuentan UNO, DOS, TRES (clic de hueso)
    s7 = M["s07"]
    for i, c in enumerate(s7.CAEN):
        ev.add(thump(110 - 12 * i, 0.25, 0.06), T["s07"] + c, 0.30)
        ev.add(sfx.tap(i), T["s07"] + c, 0.50)
    ev.add(sfx.breath(0.7, False, 81), T["s07"] + 4.7, 0.12, -0.5)
    for i, c in enumerate(s7.CUENTA):
        ev.add(sfx.tap(10 + i), T["s07"] + c, 0.55)
        ev.add(sfx.heartbeat(), T["s07"] + c, 0.18)
    # s08: reloj acelerado, corcho, trago, ladridos y grito
    s8 = M["s08"]
    for i in range(14):
        ev.add(sfx.tick(1320, 0.05), T["s08"] + 0.12 + 0.1 * i, 0.12)
    ev.add(sfx.whoosh(0.9, 200, 1500, 3), T["s08"] + 0.1, 0.22)
    ev.add(C.pop_corcho(), T["s08"] + s8.POP, 0.50, 0.3)
    ev.add(sfx.tragar(1), T["s08"] + s8.POP + 0.6, 0.28)
    for i, b in enumerate(s8.LADRIDOS):
        ev.add(ladridos(1, 0.3, 400, 80 + i), T["s08"] + b, 0.55, -0.5)
        ev.add(ladridos(1, 0.3, 330, 90 + i), T["s08"] + b + 0.04, 0.50, 0.5)
    # s09: silencio total, silbido cerca (fuerte) y luego lejísimos; latido que sube
    ev.add(sfx.tinnitus(2.0), T["s09"] + 1.2, 0.012)
    C.silbido(ev, T["s09"] + m9.CERCA, 1.4, 0.55, seed=13)
    C.silbido(ev, T["s09"] + m9.LEJOS, 1.4, 0.35, lejano=True, seed=17)
    ev.add(sfx.riser(1.2, 8), T["s09"] + m9.LEJOS - 0.2, 0.06)
    for i in range(3):
        ev.add(sfx.heartbeat(), T["s09"] + 8.2 + 0.9 * i, 0.22 + 0.04 * i)
    # s10: algo se sienta junto a la puerta; cae el saco; se cuentan los huesos
    ev.add(sfx.creak(1.3, 5), T["s10"] + 1.2, 0.22, 0.2)
    ev.add(sfx.step_dirt(30), T["s10"] + 1.5, 0.12, 0.2)
    ev.add(sfx.susto(), T["s10"] + m10.SACO, 0.50)
    ev.add(thump(45, 1.0, 0.30), T["s10"] + m10.SACO, 0.55)
    for i in range(4):
        ev.add(sfx.tap(20 + i), T["s10"] + m10.SACO + 0.15 + 0.12 * i, 0.25)
    for i, c in enumerate(m10.CLICS):
        ev.add(sfx.tap(30 + i), T["s10"] + c, 0.55)
        ev.add(sfx.heartbeat(), T["s10"] + c, 0.22)
    # s11: el ojo vuelve; cada "FALTAN" suena a hueso; latido sostenido; alguien no amanece
    ev.add(sfx.susto(), T["s11"] + m11.OJO, 0.52)
    ev.add(sfx.tinnitus(2.0), T["s11"] + m11.OJO + 0.2, 0.03)
    for i, (n, a, b) in enumerate(m11.FALTAN):
        ev.add(sfx.tap(40 + i), T["s11"] + a, 0.55)
    for i in range(7):
        ev.add(sfx.heartbeat(), T["s11"] + 4.0 + 0.8 * i, 0.20 + 0.03 * i)
    ev.add(thump(55, 0.6, 0.14), T["s11"] + m11.FIN, 0.45)
    ev.add(sfx.breath(0.9, False, 91), T["s11"] + m11.FIN, 0.10, -0.5)
    # s12: botones, campanilla del llamado, apagón y el silbido que reinicia el bucle
    ev.add(sfx.whoosh(0.4, 400, 2500, 5), T["s12"] + m12.BOTONES, 0.20)
    ev.add(sfx.ding(), T["s12"] + m12.COMENTA, 0.12)
    ev.add(sfx.candle_puff(2), T["s12"] + m12.APAGON, 0.35)
    ev.add(sfx.susto(), T["s12"] + m12.OJOS, 0.35)
    C.silbido(ev, T["s12"] + m12.OJOS + 0.05, 0.5, 0.40, notas=3, seed=21)

    return C.finalizar(cam, ev, env_c, env_e, voices, total_out, GANANCIA_DB)
