"""Punto de entrada único del estudio.

  python producir.py <historia> <episodio>                 # todo: voces -> sonido -> escenas -> video final
  python producir.py <historia> <episodio> --voces         # solo genera voces y muestra la línea de tiempo
  python producir.py <historia> <episodio> --sonido        # voces + banda sonora
  python producir.py <historia> <episodio> --escenas a b   # re-renderiza solo esas escenas y vuelve a unir
  python producir.py <historia> <episodio> --cuadros ep1.s2_ciudad 1.5 4.0   # cuadros PNG para revisar
  python producir.py --nueva <historia> [--formato vertical|horizontal]      # crea una historia desde la plantilla

<historia> es la carpeta dentro de historias/ (por ejemplo rebelion_maquinas).
"""
import argparse
import importlib
import os
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def nueva(slug, formato):
    dst = ROOT / "historias" / slug
    if dst.exists():
        sys.exit(f"Ya existe historias/{slug}")
    shutil.copytree(ROOT / "historias" / "_plantilla", dst)
    hist = dst / "historia.py"
    hist.write_text(hist.read_text().replace('FORMATO = "vertical"', f'FORMATO = "{formato}"'))
    print(f"Creada historias/{slug}. Edita historia.py y escribe tus escenas en escenas/ep1/.")


def run(cmd, env):
    t0 = time.time()
    r = subprocess.run(cmd, env=env, cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"Falló {' '.join(cmd)}\n{r.stderr[-2000:]}")
    return r.stdout.strip(), time.time() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("historia", nargs="?")
    ap.add_argument("episodio", nargs="?")
    ap.add_argument("--nueva")
    ap.add_argument("--formato", default="vertical")
    ap.add_argument("--voces", action="store_true")
    ap.add_argument("--sonido", action="store_true")
    ap.add_argument("--escenas", nargs="*")
    ap.add_argument("--cuadros", nargs="+")
    a = ap.parse_args()

    if a.nueva:
        return nueva(a.nueva, a.formato)
    if not (a.historia and a.episodio):
        ap.error("indica <historia> <episodio>")

    os.environ["HISTORIA"] = a.historia
    sys.path.insert(0, str(ROOT))
    from motor import config, timeline
    from motor.audio import narration
    from motor.audio.master import write_wav
    env = {**os.environ, "PYTHONPATH": str(ROOT), "PYTHONWARNINGS": "ignore"}
    ep = config.EPISODES[a.episodio]

    if a.cuadros:
        from motor.render import stills
        stills(a.cuadros[0], [float(x) for x in a.cuadros[1:]])
        return

    # 1) voces y línea de tiempo
    print("Voces…")
    narration.build()
    timeline._manifest.cache_clear()
    timeline.knots.cache_clear()
    for name in ep["scenes"]:
        d = config.scene_module(name).DURATION
        o = timeline.out_duration(name)
        print(f"  {name:22s} {d:5.1f}s -> {o:5.1f}s")
    if a.voces:
        return

    # 2) banda sonora
    print("Sonido…")
    mix = importlib.import_module(f"historias.{a.historia}.sonido.{ep['mix']}")
    data, total = mix.build()
    write_wav(config.audio_path(a.episodio), data)
    print(f"  {config.audio_path(a.episodio)}  {total:.1f}s")
    if a.sonido:
        return

    # 3) escenas en paralelo
    names = a.escenas if a.escenas else ep["scenes"]
    print(f"Escenas ({len(names)})…")
    with ThreadPoolExecutor(config.WORKERS) as pool:
        for out, secs in pool.map(lambda n: run([sys.executable, "-m", "motor.render", n], env), names):
            print("  " + out)

    # 4) unión final
    from motor.build import main as build
    build(a.episodio)


if __name__ == "__main__":
    main()
