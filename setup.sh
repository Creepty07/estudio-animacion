#!/bin/bash
# Prepara una máquina nueva (Linux) para producir videos. Se puede correr las veces que sea.
set -e
cd "$(dirname "$0")"

need_apt=()
command -v ffmpeg >/dev/null || need_apt+=(ffmpeg)
command -v espeak-ng >/dev/null || need_apt+=(espeak-ng)          # Kokoro lo usa para fonética
fc-list | grep -qi "Inter Display" || need_apt+=(fonts-inter)
fc-list | grep -qi "DejaVu Sans Mono" || need_apt+=(fonts-dejavu-core)
pkg-config --exists cairo 2>/dev/null || need_apt+=(libcairo2-dev pkg-config)
if [ ${#need_apt[@]} -gt 0 ]; then
  echo "Instalando: ${need_apt[*]}"
  (apt-get install -y -q "${need_apt[@]}" || (apt-get update -q && apt-get install -y -q "${need_apt[@]}")) >/dev/null
fi

pip install -q -r requirements.txt 2>/dev/null || pip install -q --break-system-packages -r requirements.txt

# Modelo de voz Kokoro (~350 MB, se descarga una sola vez desde GitHub)
mkdir -p models
BASE=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
[ -f models/kokoro-v1.0.onnx ] || curl -sSL -o models/kokoro-v1.0.onnx $BASE/kokoro-v1.0.onnx
[ -f models/voices-v1.0.bin ] || curl -sSL -o models/voices-v1.0.bin $BASE/voices-v1.0.bin

python3 -c "import cairo, numpy, librosa, soundfile, kokoro_onnx; print('Listo: motor de animación preparado.')"
