"""Efectos de sonido reutilizables (devuelven señales mono a 48 kHz)."""
import numpy as np
from motor.config import SR
from motor.audio.synth import tt, noise, band, norm, env_exp, fade, sweep, tone, metal, thump, pad


def n(dur):
    return int(dur * SR)


def boom(dur=3.0):
    return thump(48, dur, 1.1) + 0.3 * band(noise(dur, 1), None, 180) * env_exp(n(dur), 0.4)


def glitch_blips(seed=3, count=14, span=1.2):
    """Lista de (desfase, señal, ganancia relativa, paneo)."""
    r = np.random.default_rng(seed)
    out = []
    for i in range(count):
        d = r.uniform(0.02, 0.07)
        if i % 2:
            s = band(noise(d, seed * 100 + i), 1500, 9000)
        else:
            s = np.sign(np.sin(2 * np.pi * r.uniform(300, 1600) * tt(d)))
        out.append((r.uniform(0, span) * (i / count), fade(s, 0.002, 0.01), 1 - i / (count + 2), r.uniform(-0.6, 0.6)))
    return out


def tick(freq=1320, dur=0.12):
    return np.sin(2 * np.pi * freq * tt(dur)) * env_exp(n(dur), 0.03)


def whoosh(dur=0.6, lo=300, hi=3000, seed=9):
    return norm(band(noise(dur, seed), lo, hi) * np.hanning(n(dur)))


def ding():
    t = tt(2.0)
    s = (np.sin(2 * np.pi * 1318.5 * t) + 0.4 * np.sin(2 * np.pi * 2637 * t) + 0.25 * np.sin(2 * np.pi * 3955 * t))
    return fade(s * env_exp(n(2.0), 0.55), 0.003, 0.3)


def door_slide(dur=0.7, seed=21):
    s = band(noise(dur, seed), 200, 1800) * np.hanning(n(dur))
    s += 0.4 * band(sweep(90, 70, dur, "saw"), None, 500) * np.hanning(n(dur))
    return norm(s)


def motor_hum(dur, seed=4):
    t = tt(dur)
    s = band(sweep(55, 62, dur, "saw"), None, 300) + 0.3 * band(noise(dur, seed), 60, 400)
    s *= 0.85 + 0.15 * np.sin(2 * np.pi * 7 * t)
    return fade(norm(s), 0.4, 0.3)


def jolt(seed=31):
    return norm(1.4 * thump(55, 1.0, 0.25) + metal([110, 187, 260, 410], 1.0, 0.3, seed))


def clang(seed=500):
    return norm(metal([92, 151, 233, 368, 522, 761], 1.6, 0.45, seed=seed) + 1.6 * thump(48, 1.6, 0.3))


def cable_snap():
    crack = band(noise(0.08, 77), 1500, 12000) * env_exp(n(0.08), 0.01)
    ping = metal([2100, 3300, 4700, 6100], 0.8, 0.18, 12)
    whip = whoosh(0.35, 800, 5000, 78)
    out = np.zeros(n(0.8))
    out[: len(crack)] += crack * 1.6
    out += ping * 0.6
    out[: len(whip)] += whip * 0.5
    return norm(out)


def falling(dur):
    s = band(noise(dur, 88), 200, 3000) * np.linspace(0.2, 1.0, n(dur)) ** 1.5
    s += 0.3 * sweep(80, 300, dur) * np.linspace(0, 1, n(dur))
    return norm(s)


def crash():
    dur = 2.5
    s = band(noise(dur, 99), 60, 6000) * env_exp(n(dur), 0.35)
    s += 2.0 * thump(40, dur, 0.6)
    s += 0.8 * metal([70, 113, 166, 240, 330], dur, 0.8, 5)
    return norm(s)


def step_concrete(seed=0):
    s = 1.3 * thump(85, 0.18, 0.04) + 0.5 * band(noise(0.18, 300 + seed), 900, 5000) * env_exp(n(0.18), 0.015)
    return norm(s)


def step_metal(seed=0, base=170):
    return norm(metal([base, 395, 710, 1120], 0.5, 0.12, seed=seed) + 1.4 * thump(62, 0.5, 0.09))


def cloth_rip(dur=0.35, seed=41):
    s = band(noise(dur, seed), 1200, 6000)
    jitter = (np.random.default_rng(seed).random(n(dur)) > 0.6).astype(float)
    jitter = np.convolve(jitter, np.ones(120) / 120, mode="same")
    return norm(s * jitter * np.hanning(n(dur)))


def breath(dur=0.5, inhale=True, seed=51):
    s = band(noise(dur, seed), 500 if inhale else 350, 2400 if inhale else 1600)
    env = np.hanning(n(dur)) ** (0.7 if inhale else 1.2)
    return norm(s * env)


def tap(seed=0):
    return norm(metal([310, 523, 870], 0.25, 0.05, seed) + 0.6 * thump(120, 0.25, 0.03))


def scan_hum(dur, freq=220):
    t = tt(dur)
    s = np.sin(2 * np.pi * freq * t) + 0.5 * np.sin(2 * np.pi * freq * 1.5 * t)
    s *= 0.6 + 0.4 * np.sin(2 * np.pi * 3.2 * t)
    return fade(norm(s), 0.3, 0.3)


def static(dur, seed=61):
    s = band(noise(dur, seed), 1200, 7000)
    r = np.random.default_rng(seed)
    crackle = np.zeros(n(dur))
    for _ in range(int(dur * 40)):
        i = r.integers(0, max(1, len(crackle) - 100))
        crackle[i:i + 100] += r.uniform(-1, 1) * np.exp(-np.arange(100) / 15)
    return norm(0.5 * s + crackle)


def radio_click():
    c = band(noise(0.03, 71), 500, 6000) * env_exp(n(0.03), 0.005)
    out = np.zeros(n(0.4))
    out[: len(c)] += c * 2
    st = static(0.35, 72) * np.linspace(1, 0, n(0.35))
    out[n(0.05): n(0.05) + len(st)] += 0.5 * st
    return norm(out)


def heartbeat():
    out = np.zeros(n(0.6))
    out += thump(52, 0.6, 0.09)
    b = thump(46, 0.36, 0.09)
    out[n(0.24): n(0.24) + len(b)] += 0.7 * b
    return norm(out)


def sting(kind):
    """Golpe musical de la tarjeta de resultado."""
    if kind == "malo":
        s = 1.2 * boom(3.5) + 0.5 * pad([36.7, 73.4, 77.8, 110.0], 3.5, 0.02, 1.5, 700, 7)
    elif kind == "regular":
        s = 0.6 * thump(55, 3.5, 0.6) + pad([110.0, 130.8, 164.8, 220.0], 3.5, 0.05, 1.6, 1400, 8)
    else:
        s = 0.5 * thump(60, 4.0, 0.5) + pad([146.8, 185.0, 220.0, 293.7, 370.0], 4.0, 0.08, 1.8, 2600, 9)
        s += 0.3 * pad([587.3, 740.0, 880.0], 4.0, 0.4, 1.8, 5000, 10)
    return norm(s)


# ---------- folclore y exteriores nocturnos ----------
def candle_puff(seed=0):
    """Soplo que apaga una vela: ráfaga corta de aire y un siseo."""
    puff = band(noise(0.28, 700 + seed), 500, 3500) * np.hanning(n(0.28)) ** 0.8
    hiss = band(noise(0.5, 800 + seed), 3000, 9000) * env_exp(n(0.5), 0.12) * 0.25
    out = np.zeros(n(0.6))
    out[: len(puff)] += puff
    out[: len(hiss)] += hiss
    return norm(out)


def bell(freq=392.0, dur=5.0, seed=3):
    """Campana lejana: parciales inarmónicos con caída larga."""
    parts = [freq * r for r in (1.0, 2.01, 2.4, 3.0, 4.18, 5.43)]
    return fade(norm(metal(parts, dur, 1.7, seed)), 0.005, 1.2)


def wail(dur=2.4, f0=430.0, f_peak=980.0, f1=520.0, seed=3):
    """Lamento largo y agudo: tono que sube y cae, con vibrato y aire. No es una voz: es el 'grito' del viento."""
    t = tt(dur)
    k = t / dur
    up = np.clip(k / 0.4, 0, 1)
    down = np.clip((k - 0.4) / 0.6, 0, 1)
    f = np.where(k < 0.4, f0 + (f_peak - f0) * up ** 1.5, f_peak + (f1 - f_peak) * down ** 0.8)
    f = f * (1 + 0.018 * np.sin(2 * np.pi * 5.6 * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    sig = sum(a * np.sin(h * ph) for h, a in enumerate((1.0, 0.6, 0.35, 0.2, 0.1), start=1))
    sig = band(sig, 400, 3800)
    sig += 0.25 * band(noise(dur, seed), 1500, 6000)
    env = np.minimum(1, t / 0.25) * np.exp(-np.maximum(t - dur * 0.55, 0) / (dur * 0.3))
    return fade(norm(sig * env), 0.02, 0.3)


def step_dirt(seed=0):
    """Paso sobre tierra suelta."""
    s = 1.0 * thump(70, 0.2, 0.04) + 0.5 * band(noise(0.2, 400 + seed), 200, 1800) * env_exp(n(0.2), 0.03)
    return norm(s)


def petal_touch(seed=0):
    """Una flor que se posa sobre piedra: toque casi inaudible."""
    return norm(0.6 * thump(130, 0.15, 0.03) + 0.3 * band(noise(0.15, 600 + seed), 1500, 6000) * env_exp(n(0.15), 0.02))


def water_close(dur=1.6):
    """El agua que se cierra: swell de agua y un 'plop' que se hunde."""
    swell = band(noise(dur, 910), 200, 2600) * np.hanning(n(dur)) ** 1.5
    plop = sweep(900, 180, 0.35) * env_exp(n(0.35), 0.1)
    out = swell * 0.7
    i = n(dur * 0.45)
    out[i:i + len(plop)] += plop
    return fade(norm(out), 0.05, 0.6)


def chisel(seed=0):
    """Golpecito de cincel sobre piedra."""
    return norm(metal([1800, 2900, 4100], 0.12, 0.03, seed) + 0.4 * thump(200, 0.12, 0.02))


def cold_touch(dur=1.8):
    """Roce helado: aire que se vuelve agudo y tiembla."""
    t = tt(dur)
    s = band(noise(dur, 940), 2500, 9000) * np.hanning(n(dur))
    s += 0.4 * np.sin(2 * np.pi * np.cumsum(3800 + 400 * np.sin(2 * np.pi * 7 * t)) / SR) * np.hanning(n(dur))
    return norm(s)


def creak(dur=1.3, seed=0):
    """Crujido de madera o reja: pulsos de fricción de frecuencia irregular, filtrados."""
    r = np.random.default_rng(seed)
    t = tt(dur)
    slow = np.convolve(r.standard_normal(n(dur)), np.ones(int(0.05 * SR)) / int(0.05 * SR), mode="same")
    f = 28 + 22 * np.abs(slow) / max(np.abs(slow).max(), 1e-6)
    saw = 2 * ((np.cumsum(f) / SR) % 1.0) - 1
    stick = saw * (0.5 + 0.5 * np.sin(2 * np.pi * (9 + 4 * np.sin(2 * np.pi * 0.7 * t)) * t))
    s = band(stick, 350, 1500) + 0.3 * band(noise(dur, seed + 9), 900, 2600) * np.abs(saw)
    return norm(s * np.hanning(n(dur)) ** 0.6)


def owl(seed=0):
    """Tecolote: 'hu, hu, huuu' grave y hueco (en la tradición mexicana, mal augurio)."""
    def hoot(d, f0, f1):
        t = tt(d)
        ph = 2 * np.pi * np.cumsum(np.linspace(f0, f1, len(t))) / SR
        return band((np.sin(ph) + 0.3 * np.sin(2 * ph)) * np.hanning(len(t)) ** 0.8, 200, 1500)
    out = np.zeros(n(1.9))
    for at, d, f0, f1 in ((0.0, 0.3, 400, 360), (0.45, 0.22, 400, 370), (0.85, 0.75, 390, 300)):
        h = hoot(d, f0, f1)
        out[n(at): n(at) + len(h)] += h
    return norm(out)


def susto():
    """Golpe de susto: racimo disonante de sierras, ráfaga de ruido y golpe grave."""
    d = 1.4
    t = tt(d)
    cluster = sum(2 * ((f * t) % 1.0) - 1 for f in (233.1, 246.9, 311.1, 329.6, 466.2, 493.9))
    env = np.minimum(1, t / 0.005) * env_exp(n(d), 0.35)
    s = band(cluster, 200, 5000) * env
    s += 0.6 * band(noise(d, 77), 2000, 9000) * env_exp(n(d), 0.08)
    s += 0.9 * thump(38, d, 0.4)
    return norm(s)


def riser(dur=2.0, seed=0):
    """Subida de tensión: ruido y tono que suben hasta cortarse."""
    k = np.linspace(0, 1, n(dur)) ** 2.5
    s = band(noise(dur, 300 + seed), 600, 7000) * k + 0.4 * sweep(150, 1800, dur) * k
    return norm(fade(s, 0.01, 0.02))


def tinnitus(dur=3.0):
    """Zumbido agudo en el oído después de un golpe."""
    t = tt(dur)
    s = 0.6 * np.sin(2 * np.pi * 6200 * t) + 0.4 * np.sin(2 * np.pi * 6230 * t)
    return norm(s * np.minimum(1, t / 0.4) * np.exp(-np.maximum(t - 1.8, 0) * 1.2))


def crackle(dur=3.0, seed=0, density=14):
    """Crepitar de velas: chasquidos secos muy cortos y espaciados al azar."""
    r = np.random.default_rng(seed)
    out = np.zeros(n(dur))
    for _ in range(int(density * dur)):
        d = r.uniform(0.004, 0.02)
        c = band(noise(d, int(r.integers(0, 9999))), 1500, 8000) * env_exp(n(d), d / 3)
        i = int(r.uniform(0, dur - 0.05) * SR)
        out[i:i + len(c)] += c * r.uniform(0.2, 1.0)
    return norm(out)


# ---------- hospital ----------
def monitor_pitido(freq=1040.0, dur=0.11):
    """Pitido suave de monitor cardiaco: tono casi puro, ataque rápido y caída corta."""
    t = tt(dur)
    s = np.sin(2 * np.pi * freq * t) + 0.18 * np.sin(2 * np.pi * freq * 2 * t)
    return norm(s * np.minimum(1, t / 0.004) * np.exp(-t / 0.045))


def timbre_buzz(dur=0.5, seed=0):
    """Zumbador eléctrico de llamado a enfermería: sierra grave dura, con armónicos y un temblor rápido."""
    t = tt(dur)
    f = 118.0
    saw = 2 * ((f * t) % 1.0) - 1
    s = band(saw + 0.5 * np.sign(np.sin(2 * np.pi * 2 * f * t)), 100, 3200)
    s *= 0.75 + 0.25 * np.sign(np.sin(2 * np.pi * 31 * t))
    s += 0.12 * band(noise(dur, 700 + seed), 2000, 7000)
    return fade(norm(s * np.minimum(1, t / 0.006)), 0.004, 0.05)


def tragar(seed=0):
    """Un trago: golpecito húmedo en la garganta."""
    d = 0.22
    t = tt(d)
    s = np.sin(2 * np.pi * np.cumsum(260 * (1 - 0.5 * t / d)) / SR) * np.exp(-t / 0.05)
    s += 0.5 * band(noise(d, 880 + seed), 300, 2200) * np.exp(-t / 0.04)
    return norm(s)


# ---------- camión y ciudad (Ruta 0) ----------
def frenos_aire(dur=1.4, seed=0):
    """Frenos de aire de un camión: golpe grave, siseo largo que decae y un último 'pshh'."""
    s = band(noise(dur, 1200 + seed), 1800, 10500) * env_exp(n(dur), 0.45) * np.minimum(1, tt(dur) / 0.01)
    s += 0.8 * thump(58, dur, 0.18)
    ultimo = band(noise(0.25, 1300 + seed), 2500, 9000) * np.hanning(n(0.25)) ** 0.7
    i = n(dur * 0.72)
    s[i:i + len(ultimo)] += 0.6 * ultimo[: max(0, len(s) - i)]
    return fade(norm(s), 0.004, 0.2)


def puertas_neumaticas(dur=1.1, seed=0):
    """Puertas plegables de camión: siseo, clac metálico y el roce de las hojas."""
    s = np.zeros(n(dur))
    sis = band(noise(0.35, 1400 + seed), 2000, 9500) * np.hanning(n(0.35)) ** 0.6
    s[: len(sis)] += sis
    clac = metal([230, 410, 690], 0.25, 0.05, seed) + 0.8 * thump(110, 0.25, 0.04)
    i = n(0.30)
    s[i:i + len(clac)] += 0.9 * clac[: max(0, len(s) - i)]
    roce = band(noise(0.5, 1500 + seed), 300, 1800) * np.hanning(n(0.5))
    j = n(0.45)
    s[j:j + len(roce)] += 0.35 * roce[: max(0, len(s) - j)]
    return fade(norm(s), 0.003, 0.15)


def timbre_parada(seed=0):
    """Timbre de 'se solicita parada': dos tonos graves de 'ding' con caída corta."""
    t = tt(1.6)
    a = np.sin(2 * np.pi * 523 * t) + 0.35 * np.sin(2 * np.pi * 1046 * t)
    b = np.sin(2 * np.pi * 415 * t) + 0.3 * np.sin(2 * np.pi * 830 * t)
    s = a * env_exp(n(1.6), 0.32)
    j = n(0.38)
    s[j:] += (b * env_exp(n(1.6), 0.45))[: len(s) - j]
    return fade(norm(s), 0.003, 0.3)


def llantas_rechinido(dur=1.6, seed=0):
    """Llantas que rechinan y se cortan de golpe (sugerido, lejano)."""
    t = tt(dur)
    f = np.linspace(1500, 3200, n(dur))
    s = band(noise(dur, 1400 + seed), 1200, 4200) * (0.5 + 0.5 * np.sin(2 * np.pi * np.cumsum(f * 0.004) / SR * 40)) * np.minimum(1, t / 0.2)
    corte = int(dur * 0.86 * SR)
    s[corte:] = 0
    return norm(s)


def celular_vibra(dur=1.1):
    """Celular que vibra sobre madera: dos zumbidos de 150 Hz con traqueteo."""
    t = tt(dur)
    z = np.sign(np.sin(2 * np.pi * 150 * t)) * 0.4 + np.sin(2 * np.pi * 150 * t)
    g = np.zeros_like(t)
    for a in (0.02, 0.5):
        g += ((t > a) & (t < a + 0.38)).astype(float)
    s = band(z, 80, 1800) * g + 0.25 * band(noise(dur, 1500), 300, 3000) * g
    return fade(norm(s), 0.004, 0.05)


def teclas(veces=18, seed=0, dur=2.2):
    """Teclado de celular: clics suaves y desiguales."""
    r = np.random.default_rng(seed)
    out = np.zeros(n(dur))
    for k in range(veces):
        i = int((0.05 + k * (dur - 0.2) / veces + r.uniform(0, 0.04)) * SR)
        c = band(noise(0.02, int(r.integers(0, 9999))), 1500, 7000) * env_exp(n(0.02), 0.005)
        out[i:i + len(c)] += c * r.uniform(0.4, 1.0)
    return norm(out)


def paso_charco(seed=0):
    """Paso sobre el pavimento mojado: golpe seco y chapoteo corto."""
    from motor.audio.agua import chapoteo
    s = 0.8 * step_concrete(seed)
    c = chapoteo(0.25, seed, 0.15)
    s = np.concatenate([s, np.zeros(max(0, len(c) - len(s)))])
    s[: len(c)] += 0.5 * c
    return norm(s)
