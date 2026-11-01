"""Banda sonora de ejemplo: música de fondo + golpe de título. producir.py llama a build()."""
from motor.audio import sfx
from motor.audio.synth import pad
from motor.audio.master import master
from motor.audio.mixing import scene_offsets, new_track


def build():
    sc, total = scene_offsets("ep1")
    tr, total_out, voices = new_track("ep1")
    T1, s1 = sc["s1_ejemplo"]
    tr.add(pad([110.0, 164.8, 220.0], total + 0.5, 1.0, 1.0, 900), 0.0, 0.2)   # se estira solo con la voz
    tr.add(sfx.boom(), T1 + 0.4, 0.5)
    return master(tr.buf, total_out, voices, 0.4), total_out
