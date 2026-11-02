"""Banda sonora de La Tumba de la Llorona (sin narrador): el sonido cuenta el miedo. Todo se sincroniza con las
constantes de cada escena (momentos de susto, apagones, latidos, letras grabadas)."""
import numpy as np
from motor import config
from motor.config import SR
from motor.audio import sfx
from motor.audio import ambient
from motor.audio.synth import noise, band, norm, env_exp, fade, tt, thump, pad
from motor.audio.voice import grito_sintetico, aullido
from motor.audio.master import master
from motor.audio.mixing import scene_offsets, new_track

GRITO_ARCHIVO = config.ROOT / "historias/tumba_llorona/audio/grito_llorona.wav"     # grabación real (si Alejandro la aporta)


def _grito(seed, lejano=False):
    """El grito de la Llorona como efecto de sonido: la grabación real si existe; si no, el lamento sintetizado."""
    if GRITO_ARCHIVO.exists() and not lejano:
        from motor.audio.narration import _desde_archivo
        return _desde_archivo(GRITO_ARCHIVO)
    return grito_sintetico(1.6, seed, lejano=lejano)


def build():
    sc, total = scene_offsets("ep1")
    cam, total_out, _ = new_track("ep1")                      # fondos (se pueden "apagar" antes de un susto)
    ev, _, _ = new_track("ep1")                               # eventos (golpes, gritos, pasos)
    T = {k.split("_")[0]: v[0] for k, v in sc.items()}
    M = {k.split("_")[0]: v[1] for k, v in sc.items()}
    fin = {k: T[k] + M[k].DURATION for k in T}
    D = {k: M[k].DURATION for k in M}
    r = np.random.default_rng(7)

    # =============== FONDOS ===============
    cam.add(ambient.wind(fin["s11"] - T["s01"] + 1.0, 5, 90, 650, 0.5), T["s01"], 0.28)                 # viento frío de toda la noche
    cam.add(pad([41.2, 61.7, 82.4, 87.3], fin["s11"] - T["s02"], 2.5, 0.3, 450, 6), T["s02"], 0.24)     # drone grave con segunda menor
    cam.add(pad([55.0, 58.3, 110.0], fin["s08"] - T["s05"], 3.0, 1.0, 380, 4), T["s05"], 0.14)          # capa extra: crece con la advertencia
    cam.add(ambient.crickets(D["s03"] + 0.4, 7), T["s03"], 0.07)                                         # grillos solo en el panteón (y se callan)
    cam.add(ambient.lamp_hum(fin["s05"] - T["s04"], 43.0), T["s04"], 0.12)
    cam.add(ambient.water(D["s06"] + 0.6, 9), T["s06"] - 0.3, 0.22)
    cam.add(ambient.water(D["s07"] + 0.6, 10), T["s07"] - 0.3, 0.26)
    cam.add(pad([73.4, 110.0, 146.8], D["s07"] + 0.8, 1.5, 1.2, 600, 2), T["s07"] - 0.4, 0.14)
    cam.add(sfx.crackle(D["s03"], 3), T["s03"], 0.16)                                                    # velas que crepitan
    cam.add(sfx.crackle(D["s08"], 4, 9), T["s08"], 0.14)
    cam.add(ambient.murmullos(fin["s05"] - T["s03"] - 2.0, 11, 3), T["s03"] + 2.0, 0.07, -0.5)          # voces que no se entienden, cada vez más cerca
    cam.add(ambient.murmullos(D["s05"], 12, 3), T["s05"], 0.10, 0.5)
    cam.add(ambient.murmullos(D["s08"], 13, 4), T["s08"], 0.12, -0.3)
    cam.add(ambient.dawn_birds(D["s12"] + 0.6, 11, 6), T["s12"] - 0.2 + 1.0, 0.16)
    cam.add(ambient.wind(D["s12"] + D["s13"], 6, 150, 700, 0.3), T["s12"], 0.12)

    # silencios que preparan los golpes: los fondos se apagan casi del todo
    env = np.ones(len(cam.buf))
    def dip(a, b, c, d, nivel=0.04):
        ia, ib, ic, id_ = (int(x * SR) for x in (a, b, c, d))
        env[ia:ib] = np.linspace(1, nivel, ib - ia)
        env[ib:ic] = nivel
        env[ic:id_] = np.linspace(nivel, 1, id_ - ic)
    dip(T["s04"] + M["s04"].SUSTO - 0.5, T["s04"] + M["s04"].SUSTO - 0.3, T["s04"] + M["s04"].SUSTO, T["s04"] + M["s04"].SUSTO + 1.5)
    dip(T["s09"] - 0.7, T["s09"] - 0.4, T["s09"] + M["s09"].GRITO, T["s09"] + 2.2, 0.0)
    dip(T["s11"] + M["s11"].TOQUE - 0.1, T["s11"] + M["s11"].TOQUE + 0.05, T["s11"] + M["s11"].NEGRO + 0.9, T["s12"] + 1.2, 0.0)
    cam.buf *= env[:, None]

    # =============== EVENTOS ===============
    # --- escena 1: campana grave y pétalos al viento ---
    ev.add(sfx.bell(196.0, 6.0), T["s01"] + 0.15, 0.30, 0.2)
    ev.add(sfx.riser(1.6, 1), T["s01"] + D["s01"] - 1.6, 0.10)

    # --- escena 2: la vela se apaga, negro, grito, título ---
    s2 = M["s02"]
    ev.add(sfx.candle_puff(0), T["s02"] + s2.APAGA, 0.5)
    ev.add(thump(40, 1.2, 0.5), T["s02"] + s2.APAGA, 0.4)
    ev.add(_grito(1), T["s02"] + 1.6, 0.85)
    ev.add(sfx.riser(0.9, 2), T["s02"] + s2.TITULO - 0.9, 0.18)
    boom = thump(48, 3.0, 1.1) + 0.3 * band(noise(3.0, 1), None, 180) * env_exp(int(3.0 * SR), 0.4)
    ev.add(boom, T["s02"] + s2.TITULO, 0.9)
    for i in range(12):
        at = T["s02"] + s2.TITULO + r.uniform(0, 0.9) * (i / 12)
        d = r.uniform(0.02, 0.06)
        blip = band(noise(d, i), 1500, 9000) if i % 2 else np.sign(np.sin(2 * np.pi * r.uniform(300, 1600) * tt(d)))
        ev.add(fade(blip, 0.002, 0.01), at, 0.12 * (1 - i / 14), r.uniform(-0.6, 0.6))

    # --- escena 3: reja que cruje, perro lejano, tecolote ---
    ev.add(sfx.creak(1.4, 1), T["s03"] + 0.8, 0.28, -0.4)
    ev.add(aullido(3.0, 2), T["s03"] + 1.6, 0.16, 0.5)
    ev.add(sfx.owl(1), T["s03"] + 3.7, 0.24, -0.7)

    # --- escenas 4 y 5: latido, susto de la figura, aire frío ---
    for sc_name in ("s04", "s05"):
        for k, b in enumerate(M[sc_name].LATIDOS):
            ev.add(sfx.heartbeat(), T[sc_name] + b, min(0.5, 0.26 + 0.02 * k + (0.12 if sc_name == "s05" else 0)))
    s4 = M["s04"]
    ev.add(sfx.susto(), T["s04"] + s4.SUSTO, 0.55)
    ev.add(sfx.breath(0.7, True, 52), T["s05"] + 0.9, 0.12, 0.3)
    ev.add(sfx.owl(2), T["s05"] + 1.2, 0.16, 0.7)
    ev.add(sfx.riser(1.2, 3), T["s05"] + M["s05"].LLORONA - 1.0, 0.12)
    ev.add(sfx.cold_touch(1.8), T["s05"] + M["s05"].LLORONA, 0.22, -0.5)                              # corriente helada al nombrarla
    ev.add(sfx.creak(1.2, 2), T["s05"] + 5.0, 0.2, 0.4)

    # --- escena 6: el presagio, grito lejano ---
    ev.add(sfx.riser(1.6, 4), T["s06"] + M["s06"].GRITO - 1.6, 0.14)
    ev.add(_grito(9, lejano=True), T["s06"] + M["s06"].GRITO, 0.3, 0.5)
    ev.add(sfx.water_close(1.2), T["s06"] + M["s06"].APARECE, 0.25)

    # --- escena 7: perro, tecolote, agua ---
    ev.add(aullido(3.0, 5), T["s07"] + 0.3, 0.14, -0.6)
    ev.add(sfx.owl(3), T["s07"] + 3.9, 0.22, 0.7)
    ev.add(sfx.cold_touch(1.8), T["s07"] + 1.0, 0.18)

    # --- escena 8: un soplo por cada vela, y alguien al final del pasillo ---
    s8 = M["s08"]
    for i, a in enumerate(s8.APAGONES):
        ev.add(sfx.candle_puff(i), T["s08"] + a, 0.40 - 0.02 * i)
    ev.add(sfx.riser(s8.FIGURA - 2.6, 5), T["s08"] + 2.6, 0.18)
    ev.add(sfx.susto(), T["s08"] + s8.FIGURA, 0.55)

    # --- escena 9: silencio total, y el grito ---
    g9 = M["s09"].GRITO
    ev.add(thump(44, 2.2, 0.7) + 0.4 * band(noise(2.2, 4), None, 220) * env_exp(int(2.2 * SR), 0.3), T["s09"] + g9, 0.95)
    ev.add(_grito(2), T["s09"] + g9, 1.0)
    ev.add(sfx.susto(), T["s09"] + g9, 0.4)
    ev.add(sfx.tinnitus(3.0), T["s09"] + g9 + 0.3, 0.06)

    # --- escena 10: pasos en la tierra y la flor ---
    s10 = M["s10"]
    t, k = T["s10"] + 0.15, 0
    while t < T["s10"] + s10.CAMINA_HASTA:
        ev.add(sfx.step_dirt(k), t, 0.42 - 0.02 * k, -0.2)
        t += 0.34
        k += 1
    for j, b in enumerate((0.3, 1.5, 2.65)):
        ev.add(sfx.heartbeat(), T["s10"] + b, 0.28)
    ev.add(sfx.petal_touch(1), T["s10"] + s10.T_SUELTA, 0.5)
    ev.add(sfx.cold_touch(1.8), T["s10"] + s10.T_SUELTA + 0.2, 0.16, 0.3)

    # --- escena 11: aire helado en el oído, el roce, negro, zumbido y agua ---
    s11 = M["s11"]
    ev.add(sfx.breath(0.9, False, 61), T["s11"] + 1.5, 0.22, 0.6)
    ev.add(ambient.murmullos(1.8, 21, 3), T["s11"] + s11.TOQUE - 1.3, 0.16, 0.2)                      # el "¿eres tú... mi niño?" sin palabras
    ev.add(sfx.cold_touch(1.8), T["s11"] + s11.MANO[0], 0.5, 0.4)
    ev.add(sfx.susto(), T["s11"] + s11.TOQUE, 0.55)
    ev.add(sfx.tinnitus(3.2), T["s11"] + s11.TOQUE + 0.2, 0.08)
    ev.add(sfx.water_close(1.8), T["s11"] + s11.NEGRO, 0.6)

    # --- escena 12: cincel letra por letra, golpe grave, y un eco lejano ---
    s12 = M["s12"]
    for i, a in enumerate(s12.LETRAS):
        ev.add(sfx.chisel(i), T["s12"] + a, 0.55)
    ev.add(thump(42, 2.4, 0.9), T["s12"] + s12.LETRAS[-1] + 0.15, 0.7)
    ev.add(_grito(5, lejano=True), T["s12"] + s12.BRILLO[0] + 0.2, 0.12, -0.6)

    # --- escena 13: campana y último murmullo ---
    ev.add(sfx.bell(130.8, 6.0, 5), T["s13"] + 0.1, 0.30, -0.2)
    ev.add(ambient.murmullos(2.4, 31, 3), T["s13"] + 1.0, 0.08, 0.5)

    # =============== MEZCLA FINAL ===============
    bed = cam.buf + ev.buf
    bed = np.tanh(bed * 1.1)                                                  # compresión suave: sube lo flojo sin romper los golpes
    out = master(bed, total_out, [], 0.6)
    out = np.tanh(out * 1.8) / np.tanh(1.8)                                   # volumen de TikTok
    return out, total_out
