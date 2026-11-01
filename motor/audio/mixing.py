"""Ayudas para escribir la mezcla de un episodio."""
from motor import config, timeline
from motor.audio.synth import Track


def scene_offsets(ep):
    """{nombre corto de escena: (inicio sin voz, módulo)} y duración total sin voz."""
    off, out = 0.0, {}
    for name in config.EPISODES[ep]["scenes"]:
        mod = config.scene_module(name)
        out[name.split(".")[-1]] = (off, mod)
        off += mod.DURATION
    return out, off


def new_track(ep):
    """Pista ya conectada a la línea de tiempo con voz: coloca sonidos en tiempo 'sin voz'."""
    _, total = scene_offsets(ep)
    tmap, total_out, voices = timeline.episode(ep)
    return Track(total, tmap, total_out), total_out, voices
