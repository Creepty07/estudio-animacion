"""Lleva una banda sonora (WAV) al nivel de la casa: ~ -13.5 LUFS integrado y pico verdadero por debajo de -1 dBTP.

  python -m motor.audio.normalizar out/<historia>/audio/banda_ep1.wav [objetivo_lufs] [techo_dbtp]

Mide con ffmpeg (ebur128), aplica la ganancia que falta y limita los picos; sobrescribe el WAV. Luego se une con
`python -m motor.build <ep>` (con HISTORIA en el entorno) sin volver a renderizar las escenas.
"""
import json
import re
import subprocess
import sys
from pathlib import Path


def medir(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=peak=true", "-f", "null", "-"],
                       capture_output=True, text=True)
    i = float(re.findall(r"\n\s+I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])
    return i


def a_lufs(path, objetivo=-13.5, techo=-1.0):
    path = Path(path)
    antes = medir(path)
    gan = objetivo - antes
    tmp = path.with_suffix(".norm.wav")
    lim = 10 ** (techo / 20)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(path), "-af", f"volume={gan:.2f}dB,alimiter=limit={lim:.3f}:level=disabled",
                    "-c:a", "pcm_s16le", str(tmp)], check=True)
    tmp.replace(path)
    return antes, medir(path)


if __name__ == "__main__":
    a = sys.argv
    antes, despues = a_lufs(a[1], float(a[2]) if len(a) > 2 else -13.5, float(a[3]) if len(a) > 3 else -1.0)
    print(f"{a[1]}: {antes:.1f} -> {despues:.1f} LUFS")
