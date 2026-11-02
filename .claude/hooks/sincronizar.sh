#!/bin/bash
# Hook de inicio de sesión: trae lo último del repo (regla "dos máquinas", CLAUDE.md §8.1).
# Lo que imprime aquí lo lee Claude al empezar. Nunca bloquea la sesión.
cd "${CLAUDE_PROJECT_DIR:-$(dirname "$0")/../..}" || exit 0

if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "AVISO de sincronización: hay cambios sin commit en esta máquina; no se hizo git pull. Revísalos antes de trabajar."
  exit 0
fi

if salida=$(timeout 25 git pull --ff-only -q 2>&1); then
  echo "Repo sincronizado con origin ($(git log -1 --format='%h %s' | cut -c1-80))."
else
  echo "AVISO de sincronización: git pull falló; resuélvelo antes de editar context.md. Detalle: $(echo "$salida" | tail -2)"
fi
exit 0
