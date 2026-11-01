"""Banda sonora de La Tumba de la Llorona. Todo se sincroniza con las constantes de cada escena."""
import numpy as np
from motor.config import SR
from motor.audio import sfx
from motor.audio import ambient
from motor.audio.synth import noise, band, norm, env_exp, fade, sweep, tt, thump, pad
from motor.audio.voice import grito_sintetico
from motor.audio.master import master
from motor.audio.mixing import scene_offsets, new_track


def build():
    sc, total = scene_offsets("ep1")
    tr, total_out, voices = new_track("ep1")
    T = {k.split("_")[0]: v[0] for k, v in sc.items()}          # s01 -> inicio sin voz
    M = {k.split("_")[0]: v[1] for k, v in sc.items()}          # s01 -> módulo de la escena
    fin = {k: T[k] + M[k].DURATION for k in T}

    # ---------- fondos ----------
    tr.add(ambient.wind(fin["s10"] - T["s01"] + 1.5, 5, 90, 650, 0.45), T["s01"], 0.26)             # viento de toda la noche
    tr.add(ambient.crickets(fin["s03"] - T["s03"], 7), T["s03"], 0.06)               # los grillos solo en el panteón; luego se callan               # grillos desde el panteón
        # drones graves y disonantes (segunda menor) que crecen hasta el negro de la escena 11
    tr.add(pad([41.2, 61.7, 82.4, 87.3], fin["s11"] - T["s03"] - 0.6, 2.5, 0.3, 450, 6), T["s03"], 0.20)
    tr.add(ambient.lamp_hum(fin["s05"] - T["s04"], 43.0), T["s04"], 0.12)
    tr.add(ambient.water(M["s06"].DURATION + 0.6, 9), T["s06"] - 0.3, 0.22)           # lago del flashback
    tr.add(ambient.water(M["s07"].DURATION + 0.6, 10), T["s07"] - 0.3, 0.26)          # canal
    tr.add(pad([73.4, 110.0, 146.8], M["s07"].DURATION + 0.8, 1.5, 1.2, 600, 2), T["s07"] - 0.4, 0.14)
    tr.add(ambient.dawn_birds(M["s12"].DURATION + 0.6, 11, 8), T["s12"] - 0.2, 0.20)
    tr.add(ambient.wind(M["s12"].DURATION + M["s13"].DURATION, 6, 150, 700, 0.3), T["s12"], 0.10)

    # ---------- escena 1: campana lejana ----------
    tr.add(sfx.bell(196.0, 6.0), T["s01"] + 0.15, 0.30, 0.2)

    # ---------- escena 2: la vela se apaga, negro, grito y título ----------
    s2 = M["s02"]
    tr.add(sfx.candle_puff(0), T["s02"] + s2.APAGA, 0.45)
    n_sw = int(1.1 * SR)                                                              # swell inverso que sube hacia el título
    sw = band(noise(1.1, 12), 700, 6000) * np.linspace(0, 1, n_sw) ** 2.5
    tr.add(norm(sw), T["s02"] + s2.TITULO - 1.1, 0.20)
    boom = thump(48, 3.0, 1.1) + 0.3 * band(noise(3.0, 1), None, 180) * env_exp(int(3.0 * SR), 0.4)
    tr.add(boom, T["s02"] + s2.TITULO, 0.85)
    r = np.random.default_rng(3)
    for i in range(12):
        at = T["s02"] + s2.TITULO + r.uniform(0, 0.9) * (i / 12)
        d = r.uniform(0.02, 0.06)
        blip = band(noise(d, i), 1500, 9000) if i % 2 else np.sign(np.sin(2 * np.pi * r.uniform(300, 1600) * tt(d)))
        tr.add(fade(blip, 0.002, 0.01), at, 0.10 * (1 - i / 14), r.uniform(-0.6, 0.6))

    # ---------- escenas 4 y 5: latido que se acelera ----------
    t, paso, g = T["s04"] + 0.3, 1.25, 0.25
    while t < fin["s05"] - 0.2:
        tr.add(sfx.heartbeat(), t, g)
        t += paso
        paso = max(0.8, paso - 0.04)
        g = min(0.45, g + 0.012)

    # ---------- escena 6: grito lejano bajo "¡Hijitos míos!" ----------
    tr.add(grito_sintetico(2.2, 9, lejano=True), T["s06"] + M["s06"].GRITO - 0.1, 0.12, 0.5)   # grito lejano bajo la voz

    # ---------- escena 8: un soplo por cada vela ----------
    for i, a in enumerate(M["s08"].APAGONES):
        tr.add(sfx.candle_puff(i), T["s08"] + a, 0.38 - 0.02 * i, 0.0)

    # ---------- escena 9: el grito ----------
    g9 = M["s09"].GRITO
    tr.add(thump(44, 2.2, 0.7) + 0.4 * band(noise(2.2, 4), None, 220) * env_exp(int(2.2 * SR), 0.3), T["s09"] + g9, 0.9)

    # ---------- escena 10: pasos y la flor ----------
    s10 = M["s10"]
    t, k = T["s10"] + 0.15, 0
    while t < T["s10"] + s10.CAMINA_HASTA:
        tr.add(sfx.step_dirt(k), t, 0.42 - 0.02 * k, -0.2)
        t += 0.34
        k += 1
    tr.add(sfx.petal_touch(1), T["s10"] + s10.T_SUELTA, 0.45)

    # ---------- escena 11: silencio, mano fría, negro y agua ----------
    s11 = M["s11"]
    tr.add(sfx.cold_touch(1.8), T["s11"] + s11.MANO[0], 0.5, 0.4)
    tr.add(thump(46, 1.2, 0.5), T["s11"] + s11.TOQUE, 0.5)
    tr.add(sfx.water_close(1.8), T["s11"] + s11.NEGRO, 0.55)

    # ---------- escena 12: cincel letra por letra y golpe grave ----------
    s12 = M["s12"]
    for i, a in enumerate(s12.LETRAS):
        tr.add(sfx.chisel(i), T["s12"] + a, 0.5)
    tr.add(thump(42, 2.4, 0.9), T["s12"] + s12.LETRAS[-1] + 0.15, 0.7)

    # ---------- escena 13: cierre ----------
    tr.add(sfx.bell(261.6, 5.0, 5), T["s13"] + 0.15, 0.24, -0.2)

    return master(tr.buf, total_out, voices, 0.5), total_out
