"""Banda sonora de "El río de los perros" — SIN narrador: el sonido cuenta la historia.

Capas (de abajo hacia arriba):
  1. Camas continuas: viento, río, grillos o pájaros según la escena + un zumbido grave que cambia de color
     (frío en el Mictlán, tibio en la calle y la ofrenda).
  2. Sonido de acción sincronizado con lo que se ve: pasos, pedradas, ladridos, olfateo, masticar, agua.
  3. Instrumentos de leyenda: huehuetl (tambor), caracol y una frase de ocarina (el "tema del perro").
Los tiempos de cada escena salen de las constantes en MAYÚSCULAS de su módulo, para que no se desfasen.
"""
import numpy as np
from motor.config import SR
from motor.audio import sfx, ambient, animales as A, agua as W, instrumentos as I
from motor.audio.synth import pad, reverb, norm, fade
from motor.audio.master import master
from motor.audio.mixing import scene_offsets, new_track

# Tema del perro: descendente y triste (frío) / ascendente y esperanzado (final)
TEMA_TRISTE = [(329.6, 0.0, 0.9), (293.7, 0.9, 0.9), (246.9, 1.8, 0.9), (220.0, 2.7, 2.4)]
TEMA_TIERNO = [(440.0, 0.0, 0.8), (392.0, 0.8, 0.8), (329.6, 1.6, 1.8)]
TEMA_ESPERANZA = [(220.0, 0.0, 0.9), (293.7, 0.9, 0.9), (329.6, 1.8, 0.9), (440.0, 2.7, 2.8)]


def build():
    sc, total = scene_offsets("ep1")
    tr, total_out, voices = new_track("ep1")
    S = {k: v[0] for k, v in sc.items()}          # inicio de cada escena
    M = {k: v[1] for k, v in sc.items()}          # módulo de cada escena (para leer sus constantes)
    add = tr.add

    def cama(esc, sig, g, extra=0.0):
        add(sig(M[esc].DURATION + extra), S[esc], g)

    def pasos(t0, t1, cada, fn, g, pan0=0.0, pan1=0.0, seed=0):
        """Pasos repartidos entre t0 y t1 (tiempo absoluto del video), con paneo que se mueve."""
        n = int((t1 - t0) / cada)
        for i in range(n):
            u = i / max(n - 1, 1)
            add(fn(seed + i), t0 + i * cada, g * (0.85 + 0.3 * ((i * 7) % 3) / 2), pan0 + (pan1 - pan0) * u)

    frio = lambda d: pad([55.0, 82.4, 110.0], d, 1.2, 1.2, 700, 3)
    tibio = lambda d: pad([196.0, 246.9, 293.7], d, 1.5, 1.5, 1100, 5)
    viento = lambda d: ambient.wind(d, seed=5)
    rio = lambda d: ambient.water(d, seed=9)
    grillos = lambda d: ambient.crickets(d, seed=7, voices=3)

    # ---------- s01 gancho: silencio, tres golpes de tambor y los ojos que se abren ----------
    s1 = S["s01_gancho"]
    cama("s01_gancho", viento, 0.10)
    for i, T in enumerate(M["s01_gancho"].GOLPES):
        add(I.huehuetl(fuerza=1.0 + 0.3 * i, seed=i, grave=60 - 4 * i), s1 + T, 0.62 + 0.14 * i)
    add(A.grunido(1.5, 90, seed=1), s1 + M["s01_gancho"].OJOS - 0.15, 0.40, 0.0)
    add(sfx.heartbeat(), s1 + M["s01_gancho"].OJOS + 0.05, 0.55)

    # ---------- s02 título: caracol + golpe grande ----------
    s2 = S["s02_titulo"]
    add(I.caracol(233.0, 3.2, 1), s2 + M["s02_titulo"].CARACOL, 0.50)
    add(I.huehuetl(fuerza=1.5, seed=9, grave=52, dur=2.8), s2 + M["s02_titulo"].GOLPE, 0.85)
    add(sfx.whoosh(0.7, 200, 2400, 4), s2 + M["s02_titulo"].GOLPE - 0.25, 0.22)
    cama("s02_titulo", frio, 0.14)

    # ---------- s03 el río: agua, viento, aullido lejano y primer tema ----------
    s3, m3 = S["s03_rio"], M["s03_rio"]
    cama("s03_rio", rio, 0.34)
    cama("s03_rio", viento, 0.16)
    cama("s03_rio", frio, 0.16)
    add(A.aullido(3.4, 330, 620, 2, lejano=True), s3 + m3.AULLIDO, 0.42, 0.3)
    add(I.melodia(TEMA_TRISTE, 0.45, 2.4), s3 + 3.5, 0.22)
    add(sfx.heartbeat(), s3 + m3.OJOS_LEJOS, 0.40, -0.3)
    add(A.grunido(1.2, 100, seed=3), s3 + m3.OJOS_LEJOS + 0.1, 0.18, -0.3)

    # ---------- s04 calle de día: pájaros, pedradas, perros que huyen, cachorro ----------
    s4, m4 = S["s04_calle_dia"], M["s04_calle_dia"]
    cama("s04_calle_dia", lambda d: ambient.dawn_birds(d, seed=21, chirps=20), 0.13)
    cama("s04_calle_dia", lambda d: ambient.wind(d, seed=8, lo=150, hi=600, gust=0.25), 0.07)
    cama("s04_calle_dia", tibio, 0.10)
    add(A.ladridos(3, 0.55, 360, 4, 0.3), s4 + 0.3, 0.10, -0.7)                       # perros de otras calles, lejos
    for i, T in enumerate(m4.TIROS):
        add(sfx.whoosh(0.28, 500, 4200, 10 + i), s4 + T - 0.05, 0.40, 0.2)             # el brazo corta el aire
        add(sfx.tap(i), s4 + T + 0.55, 0.30, -0.4 - 0.1 * i)                           # la piedra pega en la tierra
        add(A.quejido(900 + 90 * i, 0.22, i), s4 + T + 0.14, 0.50, -0.5 + 0.2 * i)     # el perro se asusta
        pasos(s4 + m4.HUYEN[i], s4 + m4.HUYEN[i] + 1.2, 0.11, A.pata, 0.30, -0.4, -0.9, i)
    add(A.quejido(1100, 0.3, 7), s4 + m4.CACHORRO_SALE + 0.3, 0.26, 0.4)
    add(I.melodia(TEMA_TRISTE[:3], 0.4, 1.8), s4 + 5.3, 0.14)

    # ---------- s05 calle de noche: grillos, pasos a escondidas, la tortilla, masticar ----------
    s5, m5 = S["s05_calle_noche"], M["s05_calle_noche"]
    cama("s05_calle_noche", grillos, 0.22)
    cama("s05_calle_noche", lambda d: ambient.wind(d, seed=12, lo=140, hi=500, gust=0.3), 0.07)
    cama("s05_calle_noche", frio, 0.10)
    pasos(s5 + m5.LLEGA[0], s5 + m5.LLEGA[1], 0.48, sfx.step_dirt, 0.22, -0.8, 0.0, 30)
    add(sfx.tap(5), s5 + m5.DEJA, 0.22, 0.1)                                          # la tortilla toca el piso
    pasos(s5 + 1.2, s5 + 2.3, 0.30, A.pata, 0.22, 0.7, 0.4, 50)                        # el cachorro se acerca con miedo
    pasos(s5 + m5.DEJA + 0.5, s5 + m5.COME[0], 0.26, A.pata, 0.24, 0.4, 0.15, 60)
    pasos(s5 + m5.SE_VA, s5 + m5.DURATION - 0.4, 0.50, sfx.step_dirt, 0.18, -0.2, -0.9, 80)
    add(A.olfateo(3, 5), s5 + m5.COME[0] - 0.3, 0.30, 0.15)
    add(A.masticar(1.6, 2), s5 + m5.COME[0] + 0.1, 0.34, 0.15)
    add(I.melodia(TEMA_TIERNO, 0.4, 2.0), s5 + m5.COME[0] + 0.2, 0.18)

    # ---------- s06 muerte: latidos que se espacian, último aliento, vela, silencio ----------
    s6, m6 = S["s06_muerte"], M["s06_muerte"]
    cama("s06_muerte", lambda d: ambient.crickets(d, seed=3, voices=2), 0.07)
    cama("s06_muerte", tibio, 0.08)
    for T, g in ((0.7, 0.50), (1.9, 0.42), (2.55, 0.30)):                             # latidos cada vez más lentos
        add(sfx.heartbeat(), s6 + T, g)
    add(sfx.breath(1.1, inhale=False, seed=52), s6 + m6.ULTIMO_ALIENTO - 0.05, 0.42)
    add(sfx.candle_puff(3), s6 + m6.APAGA, 0.60)
    add(I.huehuetl(0.8, 4, 56, 3.0, 0.4), s6 + m6.APAGA + 0.05, 0.50)
    add(frio(2.4), s6 + m6.APAGA, 0.20)
    add(ambient.wind(2.4, seed=14, lo=150, hi=700), s6 + m6.APAGA + 0.1, 0.16)

    # ---------- s07 orilla: despierta; las manos suben y se hunden ----------
    s7, m7 = S["s07_orilla"], M["s07_orilla"]
    cama("s07_orilla", rio, 0.34)
    cama("s07_orilla", viento, 0.15)
    cama("s07_orilla", frio, 0.20)
    add(sfx.breath(0.9, inhale=True, seed=60), s7 + m7.DESPIERTA + 0.1, 0.30)
    for i, (x, y, t0) in enumerate(m7.MANOS):
        pan = (x - 540) / 540 * 0.8
        add(W.agua_sube(1.8, i), s7 + t0 - 0.1, 0.34, pan)
        add(sfx.cold_touch(1.6), s7 + t0 + 0.2, 0.10, pan)
        add(sfx.water_close(1.6), s7 + t0 + 1.9, 0.26, pan)
    add(W.gota(1), s7 + 2.0, 0.16, 0.3)
    add(I.melodia(TEMA_TRISTE[:3], 0.45, 2.2), s7 + 0.8, 0.14)

    # ---------- s08 blanco y negro: pasos, resoplido, excusa, se van ----------
    s8, m8 = S["s08_blanco_negro"], M["s08_blanco_negro"]
    cama("s08_blanco_negro", rio, 0.26)
    cama("s08_blanco_negro", viento, 0.12)
    cama("s08_blanco_negro", frio, 0.16)
    for ts, brillo, seed in ((m8.BLANCO_T, True, 70), (m8.NEGRO_T, False, 90)):
        t_in, t_stop, t_hab, t_out = ts
        pasos(s8 + t_in, s8 + t_stop, 0.30, A.pata, 0.26, 0.8, 0.2, seed)
        pasos(s8 + t_out, s8 + t_out + 1.5, 0.28, A.pata, 0.24, 0.3, 0.9, seed + 20)
        if brillo:                                                                   # perro blanco: campana clara y ladrido seco
            add(sfx.bell(660.0, 3.0, 8), s8 + t_stop - 0.1, 0.20, 0.3)
            add(A.ladrido(520, 0.22, 12), s8 + t_hab, 0.34, 0.3)
            add(A.resoplido(0.4, 3), s8 + t_out - 0.2, 0.26, 0.3)
        else:                                                                        # perro negro: gruñido grave y tambor
            add(I.huehuetl(1.0, 6, 50, 2.6, 0.35), s8 + t_stop - 0.05, 0.55)
            add(A.grunido(1.4, 85, seed=7), s8 + t_hab - 0.1, 0.38, 0.3)
            add(A.ladrido(300, 0.3, 13), s8 + t_hab + 0.7, 0.30, 0.3)
    add(A.quejido(700, 0.25, 9), s8 + 8.3, 0.12, -0.2)                               # Celso solo: un suspiro del mundo

    # ---------- s09 otra orilla: ojos que miran, ladridos lejanos, latidos ----------
    s9, m9 = S["s09_otra_orilla"], M["s09_otra_orilla"]
    cama("s09_otra_orilla", rio, 0.24)
    cama("s09_otra_orilla", lambda d: ambient.wind(d, seed=15, lo=120, hi=800, gust=0.5), 0.18)
    cama("s09_otra_orilla", frio, 0.20)
    for k, (x, y, s_, sep, t0) in enumerate(m9.PARES):
        add(A.ladridos(1 + k % 2, 0.5, 400 + 25 * k, k, 0.35), s9 + t0 + 0.2, 0.10, (x - 540) / 540)
    add(A.aullido(3.0, 300, 560, 5, lejano=True), s9 + 1.2, 0.30, -0.4)
    for T in (1.0, 2.3, 3.6, 4.5):
        add(sfx.heartbeat(), s9 + T, 0.36)
    add(A.ladridos(2, 0.45, 390, 9, 0.5), s9 + m9.LADRIDO_LEJOS, 0.34, 0.7)           # anuncia al perro rojizo

    # ---------- s10 rojizo: ladrido desde la niebla, llega, huele la mano ----------
    s10, m10 = S["s10_rojizo"], M["s10_rojizo"]
    cama("s10_rojizo", rio, 0.22)
    cama("s10_rojizo", viento, 0.10)
    cama("s10_rojizo", frio, 0.12)
    add(A.ladridos(2, 0.45, 380, 11, 0.45), s10 + m10.LADRIDO, 0.55, 0.6)
    add(I.huehuetl(1.0, 11, 58, 2.6, 0.35), s10 + m10.LADRIDO + 0.05, 0.45)
    pasos(s10 + m10.LLEGA[0] + 0.1, s10 + m10.LLEGA[1], 0.33, A.pata, 0.24, 0.8, -0.1, 110)
    add(A.olfateo(4, 12), s10 + m10.OLFATEA[0] + 0.1, 0.36, -0.1)
    add(A.jadeo(1.6, 0.28, 13), s10 + m10.OLFATEA[0] + 0.6, 0.20, -0.1)
    add(A.quejido(1000, 0.3, 14), s10 + 5.6, 0.22, -0.1)
    add(tibio(m10.DURATION - 2.4), s10 + 2.4, 0.16)                                  # la calidez regresa poco a poco
    add(I.melodia(TEMA_TIERNO, 0.4, 2.0), s10 + 4.6, 0.24)

    # ---------- s11 cruce: chapoteo, nado, tema de esperanza, caracol de despedida ----------
    s11, m11 = S["s11_cruce"], M["s11_cruce"]
    cama("s11_cruce", rio, 0.26)
    cama("s11_cruce", lambda d: ambient.wind(d, seed=18, lo=140, hi=700, gust=0.4), 0.12)
    add(W.chapoteo(1.2, 1, 1.2), s11 + m11.SE_ECHA, 0.60, 0.3)
    add(W.nado(5.6, 0.62, 2), s11 + m11.NADA[0], 0.34, 0.0)
    add(I.melodia(TEMA_ESPERANZA, 0.45, 2.6), s11 + 1.6, 0.34)
    for T in (2.0, 3.6, 5.2):
        add(I.huehuetl(0.7, int(T * 3), 56, 2.4, 0.4), s11 + T, 0.40)
    add(tibio(m11.DURATION - 1.5), s11 + 1.5, 0.20)
    add(I.caracol(196.0, 3.4, 3), s11 + 5.4, 0.34)

    # ---------- s12 ofrenda: campana, ofrenda tibia y un ladrido contento a lo lejos ----------
    s12, m12 = S["s12_ofrenda"], M["s12_ofrenda"]
    add(sfx.bell(392.0, 5.0, 3), s12 + m12.CAMPANA, 0.45)
    cama("s12_ofrenda", grillos, 0.10)
    cama("s12_ofrenda", tibio, 0.20)
    add(I.melodia(TEMA_TIERNO, 0.4, 2.2), s12 + 1.0, 0.24)
    add(A.ladridos(1, 0.3, 480, 15, 0.5), s12 + 3.2, 0.20, 0.4)
    add(A.jadeo(1.0, 0.3, 16), s12 + 3.7, 0.08, 0.4)

    # ---------- s13 tarjeta: pad tibio, campana alta y tecleo ----------
    s13, m13 = S["s13_tarjeta"], M["s13_tarjeta"]
    cama("s13_tarjeta", tibio, 0.20)
    add(sfx.bell(784.0, 3.5, 4), s13 + 0.2, 0.28)
    for i in range(12):                                                              # tecleo mientras se "escribe" el nombre
        add(sfx.tick(1500 + 90 * (i % 3), 0.06), s13 + 2.2 + i * 0.1, 0.10)

    # ---------- nivelación: las escenas tranquilas suben para que nunca se sienta vacío ----------
    # (el clímax del cruce y el título siguen siendo lo más fuerte; el arco de volumen es intencional)
    refuerzo = {"s04_calle_dia": 1.45, "s05_calle_noche": 1.8, "s06_muerte": 1.25, "s07_orilla": 1.25,
                "s08_blanco_negro": 1.6, "s09_otra_orilla": 1.35, "s10_rojizo": 1.35, "s12_ofrenda": 1.5,
                "s13_tarjeta": 1.8}
    curva = np.ones(len(tr.buf))
    for esc, g in refuerzo.items():
        a, b = int(S[esc] * SR), int((S[esc] + M[esc].DURATION) * SR)
        curva[a:b] = g
    k = int(0.35 * SR)                                   # transiciones suaves entre escenas (sin saltos de volumen)
    curva = np.convolve(curva, np.ones(k) / k, mode="same")
    tr.buf *= curva[:, None]

    return master(tr.buf, total_out, voices, 0.5, bed_peak=0.85), total_out
