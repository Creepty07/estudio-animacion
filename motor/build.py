"""Une las escenas renderizadas de un episodio y les agrega la banda sonora.

Se ejecuta desde producir.py (requiere las escenas renderizadas y la banda sonora del episodio).
"""
import subprocess
import sys
from motor import config


def main(ep="ep1"):
    info = config.EPISODES[ep]
    lst = config.OUT / f"concat_{ep}.txt"
    lst.write_text("".join(f"file '{config.SCENES_DIR / (n + '.mp4')}'\n" for n in info["scenes"]))
    video_only = config.OUT / f"video_sin_audio_{ep}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c", "copy", str(video_only)], check=True)
    final = config.final_path(ep)
    tmp = final.with_suffix(".tmp.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video_only),
                    "-i", str(config.audio_path(ep)),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                    "-shortest", "-movflags", "+faststart", str(tmp)], check=True)
    tmp.rename(final)
    print(final)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "ep1")
