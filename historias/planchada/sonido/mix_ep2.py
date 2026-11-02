"""Banda sonora de La Planchada, ep2 "Los tres finales" (sin narrador).

Final malo: el monitor se acelera y queda un tono bajo que corta a negro (sugerido, no mostrado).
Final regular: el timbre y el contraste entre los pasos normales de la enfermera de turno y la otra, que nunca suena.
Final bueno: todo baja menos el goteo; entra una nota grave cálida bajo el nombre; amanecer con pájaros.
"""
import numpy as np
from motor.config import SR
from motor.audio import sfx, ambient
from motor.audio.synth import noise, band, norm, env_exp, fade, thump, pad, tt
from motor.audio.master import master
from motor.audio.mixing import scene_offsets, new_track
from historias.planchada.sonido import comun as C
from historias.planchada.dibujo.paleta import fluo_brillo


GANANCIA_DB = -2.3


def _golpe(ev, t, g=0.7, f=46):
    ev.add(thump(f, 1.8, 0.5) + 0.3 * band(noise(1.8, int(t * 10) % 99), 100, 2200) * env_exp(int(1.8 * SR), 0.15), t, g)


def build():
    sc, total = scene_offsets("ep2")
    cam, total_out, _ = new_track("ep2")
    ev, _, _ = new_track("ep2")
    T = {k.split("_")[0]: v[0] for k, v in sc.items()}
    M = {k.split("_")[0]: v[1] for k, v in sc.items()}
    D = {k: M[k].DURATION for k in M}
    fin = {k: T[k] + D[k] for k in T}
    env = np.ones(len(cam.buf))

    # =============== s01 gancho ===============
    C.hum(cam, T["s01"], D["s01"], 11, "parpadea", 0.14)
    cam.add(pad([41.2, 61.7, 82.4], D["s01"], 0.4, 0.3, 420, 6), T["s01"], 0.16)
    ev.add(sfx.susto(), T["s01"] + M["s01"].SUSTO, 0.5)
    ev.add(sfx.tinnitus(2.6), T["s01"] + M["s01"].SUSTO + 0.2, 0.04)

    # =============== tarjetas de final: golpe grave sobre cama de fluorescente + drone ===============
    for k, drone in (("s02", [36.7, 55.0]), ("s06", [41.2, 61.7]), ("s10", [49.0, 73.4, 98.0])):
        C.hum(cam, T[k], D[k], 1, "fijo", 0.10)
        cam.add(pad(drone, D[k] + 0.2, 0.2, 0.3, 420, 3), T[k], 0.2)
        _golpe(ev, T[k], 0.65)
    ev.add(sfx.bell(196.0, 4.0, 4), T["s10"] + 0.1, 0.16)                       # campana suave: el único final bueno

    # =============== FINAL MALO ===============
    # s03: ojos cerrados; ella deja la pastilla y se va (sin pasos); tinnitus que se va
    s3 = M["s03"]
    cam.add(pad([41.2, 55.0, 82.4], D["s03"], 0.6, 0.4, 400, 5), T["s03"], 0.18)
    cam.add(ambient.wind(D["s03"], 6, 120, 900, 0.5), T["s03"], 0.14)
    C.goteo(ev, T["s03"], D["s03"], 0.22)
    ev.add(sfx.tinnitus(3.0), T["s03"], 0.05)
    for a in (2.7, 3.0):
        ev.add(sfx.cloth_rip(0.3, 52), T["s03"] + a, 0.08, 0.3)
    ev.add(sfx.tap(1), T["s03"] + s3.DEJA, 0.14, 0.4)                          # la pastilla sobre el buró
    ev.add(sfx.cold_touch(1.4), T["s03"] + s3.DESAPARECE[0], 0.12, 0.2)
    C.hum(cam, T["s03"], D["s03"], 22, "inestable", 0.03, lo=0.1)

    # s04: el reloj acelera 3:00 → 5:40; tic-tac, latido y monitor suben
    s4 = M["s04"]
    C.hum(cam, T["s04"], D["s04"], 22, "parpadea", 0.12)
    cam.add(pad([41.2, 55.0, 61.7], D["s04"], 0.8, 0.3, 450, 8), T["s04"], 0.20)
    ts = np.linspace(0, D["s04"], 4000)
    from motor.primitives import smooth, seg
    u = np.array([smooth(seg(x, 0.2, 5.4)) for x in ts])
    N = 30
    cruz = np.searchsorted(u * N, np.arange(1, N + 1))
    for i, j in enumerate(cruz):
        if j < len(ts):
            ev.add(sfx.tick(520 if i % 2 == 0 else 470, 0.06), T["s04"] + ts[j], 0.16, 0.35)
    ph, x, k = 0.0, 0.0, 0
    while x < D["s04"] - 0.1:                                                  # monitor: de 1 a 2.6 pitidos por s
        rate = 1.0 + 1.6 * smooth(seg(x, 0.2, 5.4))
        ph += rate * 0.02
        if ph >= 1.0:
            ph -= 1.0
            ev.add(sfx.monitor_pitido(1040 + 25 * k), T["s04"] + x, 0.11, 0.5)
            ev.add(sfx.heartbeat(), T["s04"] + x - 0.02, 0.12 + 0.18 * smooth(seg(x, 0, 5.4)))
            k += 1
        x += 0.02
    C.goteo(ev, T["s04"], D["s04"], 0.18)

    # s05: amanecer gris: el monitor se acelera y queda un tono largo MUY bajo que corta a negro
    s5 = M["s05"]
    cam.add(ambient.wind(D["s05"], 9, 100, 600, 0.4), T["s05"], 0.10)
    cam.add(pad([36.7, 55.0], s5.NEGRO, 1.0, 0.1, 380, 2), T["s05"], 0.14)
    x, per = 0.2, 0.7
    while x < 3.0:
        ev.add(sfx.monitor_pitido(1040), T["s05"] + x, 0.11, 0.5)
        per = max(0.22, per * 0.88)
        x += per
    n_t = int((s5.NEGRO - 3.0) * SR)
    tn = np.arange(n_t) / SR
    tono = (np.sin(2 * np.pi * 88 * tn) + 0.4 * np.sin(2 * np.pi * 176 * tn)) * np.minimum(1, tn / 0.4)
    ev.add(norm(tono), T["s05"] + 3.0, 0.30, 0.0)
    corte5 = int((T["s05"] + s5.NEGRO) * SR)
    env[corte5:int((T["s06"] + 0.05) * SR)] = 0.0                              # negro seco

    # =============== FINAL REGULAR ===============
    s7, s8, s9 = M["s07"], M["s08"], M["s09"]
    C.hum(cam, T["s07"], D["s07"], 31, "inestable", 0.10, lo=0.1)
    cam.add(pad([49.0, 73.4], D["s07"], 0.6, 0.3, 420, 4), T["s07"], 0.17)
    for i, a in enumerate(s7.PULSOS):                                          # el timbre: clic del botón y zumbador en el pasillo
        ev.add(sfx.tap(5 + i), T["s07"] + a, 0.16, -0.2)
        ev.add(sfx.timbre_buzz(0.5, i), T["s07"] + a + 0.02, 0.28, 0.6)
    for a in (s7.CORTE + 0.25, s7.CORTE + 1.1, s7.CORTE + 2.0):                # la luz roja insiste, más lejos
        ev.add(sfx.timbre_buzz(0.35, 7), T["s07"] + a, 0.10, 0.7)
    ev.add(sfx.cloth_rip(0.35, 61), T["s07"] + s7.CORTE + 1.9, 0.08, 0.2)
    ev.add(sfx.cold_touch(1.4), T["s07"] + s7.CORTE + 2.7, 0.10)

    # s08: la enfermera de turno SÍ tiene pasos; clic de la luz del cuarto
    cam.add(ambient.wind(D["s08"], 10, 140, 700, 0.5), T["s08"], 0.10)
    ev.add(sfx.radio_click(), T["s08"] + s8.ENTRA, 0.30)
    C.hum(cam, T["s08"] + s8.ENTRA, D["s08"] - s8.ENTRA, 3, "fijo", 0.10)
    for i, a in enumerate(s8.PASOS):
        ev.add(sfx.step_concrete(i), T["s08"] + a, 0.34, 0.3 - 0.1 * i)
    ev.add(sfx.cloth_rip(0.3, 70), T["s08"] + 3.4, 0.06, 0.4)

    # s09: un clic eléctrico por cada luz; lamento lejano al aparecer la figura
    cam.add(pad([41.2, 55.0, 61.7], D["s09"], 0.6, 0.3, 380, 6), T["s09"], 0.14)
    ap = s9.APAGONES
    C.hum(cam, T["s09"], D["s09"], 40, "parpadea", 0.13,
          extra=lambda x: sum(1 for a in ap if x < a) / len(ap))
    for i, a in enumerate(ap):
        ev.add(sfx.tick(2200, 0.05), T["s09"] + a, 0.18, -0.5 + 0.15 * i)
        ev.add(sfx.radio_click(), T["s09"] + a + 0.02, 0.20, -0.5 + 0.15 * i)
    ev.add(sfx.wail(2.4, 380, 780, 430, 5), T["s09"] + s9.FIGURA[0] - 0.1, 0.07, 0.6)
    C.goteo(ev, T["s09"], D["s09"], 0.16, 3.0)

    # =============== FINAL BUENO ===============
    s11, s12, s13, s14 = M["s11"], M["s12"], M["s13"], M["s14"]
    # s11: «¿Cómo se llama?» → todo baja menos el goteo y un drone muy bajo → nota cálida bajo «Eulalia»
    C.hum(cam, T["s11"], D["s11"], 61, "inestable", 0.10, lo=0.1)
    cam.add(ambient.wind(D["s11"], 12, 120, 800, 0.5), T["s11"], 0.12)
    C.dip(cam.buf, env, T["s11"] + s11.SILENCIO[0] - 0.1, T["s11"] + s11.SILENCIO[0] + 0.1, T["s11"] + s11.NOMBRE - 0.1, T["s11"] + s11.NOMBRE + 0.4, 0.0)
    ev.add(pad([36.7, 55.0], D["s11"], 0.4, 0.3, 300, 3), T["s11"], 0.08)
    C.goteo(ev, T["s11"], D["s11"], 0.22)
    t, k = 0.3, 0
    while t < s11.SILENCIO[0] - 0.4:
        ev.add(sfx.heartbeat(), T["s11"] + t, 0.30)
        t += 1.0
    ev.add(sfx.bell(110.0, 5.0, 6), T["s11"] + s11.NOMBRE, 0.34)
    ev.add(pad([110.0, 138.6, 164.8], 2.5, 0.2, 1.5, 900, 11), T["s11"] + s11.NOMBRE, 0.12)

    # s12: el trago, el roce helado en la frente, el latido se calma, la escarcha se deshace
    cam.add(ambient.wind(D["s12"], 13, 120, 700, 0.4), T["s12"], 0.08)
    cam.add(pad([73.4, 110.0, 146.8], D["s12"], 0.8, 0.8, 800, 12), T["s12"], 0.12)
    C.hum(cam, T["s12"], D["s12"], 9, "fijo", 0.08)
    ev.add(sfx.tragar(), T["s12"] + s12.TRAGA + 0.2, 0.22, -0.2)
    ev.add(sfx.cold_touch(1.8), T["s12"] + s12.TOQUE, 0.26, -0.3)
    C.goteo(ev, T["s12"], D["s12"], 0.20)
    t, k = 0.3, 0
    while t < D["s12"] - 0.3:
        ev.add(sfx.heartbeat(), T["s12"] + t, max(0.10, 0.34 - 0.04 * k))
        t += 0.9 + 0.12 * k
        k += 1
    ev.add(sfx.crackle(2.2, 8, 8), T["s12"] + 3.0, 0.08)

    # s13: amanecer ámbar: pájaros, aire tibio, un silencio corto antes de la segunda línea
    cam.add(ambient.dawn_birds(D["s13"] - 0.3, 11, 12), T["s13"] + 0.3, 0.17)
    cam.add(pad([146.8, 185.0, 220.0], D["s13"], 1.2, 1.2, 1600, 14), T["s13"], 0.12)
    cam.add(ambient.wind(D["s13"], 15, 150, 700, 0.3), T["s13"], 0.07)
    C.dip(cam.buf, env, T["s13"] + s13.SILENCIO[0] - 0.1, T["s13"] + s13.SILENCIO[0], T["s13"] + s13.SILENCIO[1] - 0.05, T["s13"] + s13.SILENCIO[1] + 0.4, 0.15)

    # s14: el expediente; silencio previo, glitch suave + tinnitus en la «E.»
    cam.add(pad([73.4, 110.0], D["s14"], 0.6, 0.6, 600, 15), T["s14"], 0.12)
    ev.add(sfx.cloth_rip(0.4, 80), T["s14"] + 0.3, 0.10, 0.2)
    ev.add(sfx.cloth_rip(0.3, 81), T["s14"] + 1.6, 0.07, -0.2)
    C.dip(cam.buf, env, T["s14"] + s14.SILENCIO - 0.4, T["s14"] + s14.SILENCIO - 0.05, T["s14"] + s14.SUSTO, T["s14"] + s14.SUSTO + 1.0, 0.0)
    ev.add(sfx.susto(), T["s14"] + s14.SUSTO, 0.22)
    ev.add(sfx.tinnitus(2.8), T["s14"] + s14.SUSTO + 0.1, 0.06)

    # s15: la leyenda: drone cálido-frío, murmullos muy bajos, viento; sin pasos
    s15 = __import__("historias.planchada.escenas.ep2.s15_f3_leyenda", fromlist=["_z"])
    cam.add(pad([73.4, 110.0, 146.8, 185.0], D["s15"], 1.5, 1.5, 700, 16), T["s15"], 0.15)
    cam.add(ambient.wind(D["s15"], 17, 100, 650, 0.4), T["s15"], 0.11)
    cam.add(ambient.murmullos(D["s15"] - 1.0, 18, 3), T["s15"] + 0.5, 0.065, 0.3)
    cam.add(ambient.fluorescente(D["s15"], None, seed=4), T["s15"], 0.03)
    zs = np.array([s15._z(x) for x in np.linspace(0, D["s15"], 3000)])
    for i in range(6):                                                         # una puerta se ilumina al pasar ella
        zi = 0.06 + i * 0.15 + 0.035
        j = int(np.searchsorted(zs, zi))
        if j < len(zs):
            ev.add(sfx.tick(900, 0.08), T["s15"] + np.linspace(0, D["s15"], 3000)[j], 0.06, 0.4)

    # s16: cierre: el fluorescente parpadea, se apaga en APAGA, y queda el tinnitus
    s16 = M["s16"]
    def b16(x):
        if x < s16.APAGA - 0.7:
            return fluo_brillo(x, 51, "inestable")
        return 0.5 * fluo_brillo(x, 52, "inestable") if x < s16.APAGA else 0.0
    C.hum(cam, T["s16"], D["s16"], 51, "inestable", 0.12, extra=b16)
    cam.add(pad([41.2, 61.7], D["s16"], 0.6, 0.4, 380, 17), T["s16"], 0.12)
    ev.add(sfx.tinnitus(1.4), T["s16"] + s16.APAGA, 0.05)

    # =============== MEZCLA FINAL ===============
    cam.buf *= env[:, None]
    ev.buf[int((T["s05"] + s5.NEGRO) * SR):int((T["s06"] + 0.05) * SR)] = 0.0
    bed = np.tanh((cam.buf + ev.buf) * 1.1)
    out = master(bed, total_out, [], 0.5, bed_peak=0.9)
    out = np.tanh(out * 1.8) / np.tanh(1.8)
    out = out * 10 ** (GANANCIA_DB / 20)
    return out, total_out
