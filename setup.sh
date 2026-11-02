#!/bin/bash
# Prepara una máquina nueva (Linux) para producir videos. Se puede correr las veces que sea.
#
# Dos modos:
#   - Nube de claude.ai (corre como root): instala con apt y pip del sistema, como siempre.
#   - Computadora propia (WSL/Ubuntu, usuario normal): usa sudo para apt y un entorno
#     virtual .venv/ para Python (Ubuntu no deja instalar con pip en el Python del sistema).
#     Para forzar el modo .venv aunque seas root: ESTUDIO_VENV=1 ./setup.sh
set -e
cd "$(dirname "$0")"

if [ "$(id -u)" -eq 0 ]; then SUDO=""; else SUDO="sudo"; fi
USE_VENV=0
if [ "$(id -u)" -ne 0 ] || [ "${ESTUDIO_VENV:-0}" = "1" ]; then USE_VENV=1; fi

need_apt=()
command -v ffmpeg >/dev/null || need_apt+=(ffmpeg)
command -v espeak-ng >/dev/null || need_apt+=(espeak-ng)          # Kokoro lo usa para fonética
command -v curl >/dev/null || need_apt+=(curl)
command -v git >/dev/null || need_apt+=(git)
fc-list 2>/dev/null | grep -qi "Inter Display" || need_apt+=(fonts-inter)
fc-list 2>/dev/null | grep -qi "DejaVu Sans Mono" || need_apt+=(fonts-dejavu-core)
pkg-config --exists cairo 2>/dev/null || need_apt+=(libcairo2-dev pkg-config)
if [ "$USE_VENV" = "1" ]; then
  # pycairo se compila al instalarlo en un .venv: hacen falta compilador y cabeceras de Python
  python3 -m venv --help >/dev/null 2>&1 && python3 -c "import ensurepip" 2>/dev/null || need_apt+=(python3-venv)
  command -v gcc >/dev/null || need_apt+=(build-essential)
  [ -f "/usr/include/python3.$(python3 -c 'import sys; print(sys.version_info.minor)')/Python.h" ] || need_apt+=(python3-dev)
fi
if [ ${#need_apt[@]} -gt 0 ]; then
  echo "Instalando: ${need_apt[*]}"
  ($SUDO apt-get install -y -q "${need_apt[@]}" || ($SUDO apt-get update -q && $SUDO apt-get install -y -q "${need_apt[@]}")) >/dev/null
fi

if [ "$USE_VENV" = "1" ]; then
  [ -x .venv/bin/python ] || python3 -m venv .venv
  PY=.venv/bin/python
  $PY -m pip install -q --upgrade pip
  $PY -m pip install -q -r requirements.txt
else
  PY=python3
  pip install -q -r requirements.txt 2>/dev/null || pip install -q --break-system-packages -r requirements.txt
fi

# Modelo de voz Kokoro (~350 MB, se descarga una sola vez desde GitHub)
mkdir -p models
BASE=https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0
[ -f models/kokoro-v1.0.onnx ] || curl -sSL -o models/kokoro-v1.0.onnx $BASE/kokoro-v1.0.onnx
[ -f models/voices-v1.0.bin ] || curl -sSL -o models/voices-v1.0.bin $BASE/voices-v1.0.bin

$PY -c "import cairo, numpy, librosa, soundfile, kokoro_onnx; print('Listo: motor de animación preparado.')"
if [ "$USE_VENV" = "1" ]; then
  echo "Usa el entorno con: source .venv/bin/activate   (o llama directo a .venv/bin/python)"
fi
