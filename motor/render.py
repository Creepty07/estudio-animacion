"""Renderiza una escena a MP4 (tubería directa a ffmpeg) o guarda cuadros sueltos para revisar.

Normalmente se usa a través de producir.py. Uso directo (con HISTORIA en el entorno):
  HISTORIA=rebelion_maquinas python -m motor.render ep1.s3_sotano
  HISTORIA=rebelion_maquinas python -m motor.render ep1.s3_sotano --stills 2 11.5
"""
import argparse
import subprocess
import sys
import time

import cairo
from motor import config, timeline
from motor.subtitles import draw_subs


def frame(name, scene, t_out, surface):
    """Dibuja el cuadro del instante t_out (tiempo de salida, ya con los tramos alargados por la voz)."""
    ctx = cairo.Context(surface)
    ctx.set_source_rgb(0, 0, 0)
    ctx.paint()
    scene.draw(ctx, timeline.to_local(name, t_out))
    if config.SUBTITLES and scene.SUBS:
        ctx.identity_matrix()
        draw_subs(ctx, t_out, timeline.subtitles(name))
    surface.flush()


def stills(name, times):
    scene = config.scene_module(name)
    config.STILLS_DIR.mkdir(parents=True, exist_ok=True)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, config.W, config.H)
    paths = []
    for t in times:
        frame(name, scene, t, surf)
        path = config.STILLS_DIR / f"{name}_{t:.1f}.png"
        surf.write_to_png(str(path))
        paths.append(path)
        print(path)
    return paths


def video(name):
    scene = config.scene_module(name)
    config.SCENES_DIR.mkdir(parents=True, exist_ok=True)
    final = config.SCENES_DIR / f"{name}.mp4"
    tmp = config.SCENES_DIR / f"{name}.tmp.mp4"
    n = round(timeline.out_duration(name) * config.FPS)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra",
           "-s", f"{config.W}x{config.H}", "-r", str(config.FPS), "-i", "-",
           *config.X264, "-r", str(config.FPS), str(tmp)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, config.W, config.H)
    t0 = time.time()
    for i in range(n):
        frame(name, scene, i / config.FPS, surf)
        proc.stdin.write(bytes(surf.get_data()))
    proc.stdin.close()
    if proc.wait() != 0:
        sys.exit(f"ffmpeg falló en {name}")
    tmp.rename(final)   # solo se renombra si ffmpeg terminó bien
    print(f"{final}  {n} cuadros en {time.time() - t0:.0f}s")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("scene")
    ap.add_argument("--stills", nargs="*", type=float)
    a = ap.parse_args()
    if a.stills is not None:
        stills(a.scene, a.stills)
    else:
        video(a.scene)
