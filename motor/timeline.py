"""Línea de tiempo con voz: alarga cada tramo de escena lo justo para que quepa su línea hablada.

Cada escena se dibuja en su tiempo "local" (el de su código). Con narración, el tiempo de salida
avanza más despacio en los tramos que lo necesitan. Este módulo traduce entre ambos tiempos y
da los subtítulos ya colocados en tiempo de salida.
"""
import json
from functools import lru_cache
import numpy as np
from motor import config


@lru_cache(maxsize=1)
def _manifest():
    if not config.NARRATION or not config.VOICE_MANIFEST.exists():
        return {}
    return json.loads(config.VOICE_MANIFEST.read_text())


def _module(name):
    return config.scene_module(name)


@lru_cache(maxsize=None)
def knots(name):
    """Puntos (tiempo local, tiempo de salida) de la escena; entre ellos el mapeo es lineal."""
    dur = _module(name).DURATION
    lines = sorted(_manifest().get(name, []), key=lambda ln: ln["start"])
    loc, out = [0.0], [0.0]
    for i, ln in enumerate(lines):
        s = ln["start"]
        b = lines[i + 1]["start"] if i + 1 < len(lines) else dur
        if s > loc[-1]:
            out.append(out[-1] + (s - loc[-1]))
            loc.append(s)
        room = b - s
        need = ln["dur"] + config.VOICE_PAD
        f = min(config.MAX_STRETCH, max(1.0, need / room)) if room > 0 and not ln.get("mudo") else 1.0
        out.append(out[-1] + room * f)
        loc.append(b)
    if loc[-1] < dur:
        out.append(out[-1] + (dur - loc[-1]))
        loc.append(dur)
    return tuple(loc), tuple(out)


def out_duration(name):
    return knots(name)[1][-1]


def to_out(name, t_local):
    loc, out = knots(name)
    return float(np.interp(t_local, loc, out))


def to_local(name, t_out):
    loc, out = knots(name)
    return float(np.interp(t_out, out, loc))


def subtitles(name):
    """Subtítulos en tiempo de salida: (inicio, fin, texto, hablante)."""
    mod = _module(name)
    lines = _manifest().get(name)
    if not lines:
        return [(to_out(name, a), to_out(name, b), txt, spk) for a, b, txt, spk in mod.SUBS]
    starts = [to_out(name, ln["start"]) for ln in lines]
    total = out_duration(name)
    subs = []
    for i, ln in enumerate(lines):
        nxt = starts[i + 1] - 0.05 if i + 1 < len(lines) else total
        extra = 0.0 if ln.get("mudo") else 0.4
        subs.append((starts[i], min(starts[i] + ln["dur"] + extra, nxt), ln["text"], ln["speaker"]))
    return subs


def episode(ep):
    """Mapeo global del episodio: tiempo sin voz -> tiempo con voz, y duración final."""
    names = config.EPISODES[ep]["scenes"]
    starts_local, starts_out = [], []
    a = b = 0.0
    for n in names:
        starts_local.append(a)
        starts_out.append(b)
        a += _module(n).DURATION
        b += out_duration(n)

    def tmap(g):
        i = max(0, min(len(names) - 1, int(np.searchsorted(starts_local, g, side="right")) - 1))
        return starts_out[i] + to_out(names[i], g - starts_local[i])

    voices = []
    for n, so in zip(names, starts_out):
        for ln in _manifest().get(n, []):
            if ln.get("wav"):
                voices.append((so + to_out(n, ln["start"]), ln["wav"], ln["speaker"]))
    return tmap, b, voices
