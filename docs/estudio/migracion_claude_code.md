# Migración del estudio a Claude Code (escritorio)

Fecha: 2026-11-02 · Sesión de organización (Opus 5.5) · **Estado: aprobada y en curso (2026-11-02). Arranca en la PC del tío; ya hechos: memoria al repo (Fase 3, pasos 1-3) y `setup.sh` compatible con WSL.**

## 1. Veredicto

**Sí conviene migrar**, con una recomendación clara: **todo el estudio pasa a Claude Code de escritorio, en una sesión WSL (Ubuntu) dentro de la laptop de Alejandro**, y el repo `Creepty07/estudio-animacion` se vuelve la **única fuente de verdad** (código + CLAUDE.md + context.md + guiones + fichas). El Proyecto de claude.ai queda congelado como respaldo de solo lectura.

No se recomienda un esquema mixto (unas sesiones en la web y otras en escritorio) porque `context.md` viviría en dos lugares y se desincronizaría.

## 2. Por qué (lo que hoy frena al estudio y cómo cambia)

| Problema actual (nube de claude.ai) | En Claude Code de escritorio (local) |
|---|---|
| **Sin acceso a Hugging Face**: el piloto de voz (Chatterbox) está trabado; hay que bajar pesos fuera y subirlos como release | La laptop sí llega a Hugging Face: los pesos se bajan directo. El piloto se destraba |
| **2 núcleos, 7 GB, sin GPU**: un único de 85 s tarda ~7.5 min en renderizar | La laptop (Dell Latitude 5430) tiene más núcleos; el render debería bajar varias veces. **Hay que medirlo** (Fase 2). Tampoco hay GPU NVIDIA, así que la voz sigue en CPU |
| **`add_repo` con push bloqueado** varias veces por el clasificador | `git push` con las credenciales de Alejandro, sin intermediario |
| **Revisar un video = descargar el MP4** desde el chat | El MP4 queda en la carpeta; Alejandro lo abre y lo escucha al momento. Un audio que él tenga (p. ej. un grito con licencia libre) se copia a la carpeta, sin adjuntar |
| **`context.md` se reemplaza completo** con `project_write`: dos sesiones pueden borrarse entre sí | Vive en git: cada cambio es un commit, los choques se ven y se resuelven, y hay historial |
| Cada conversación clona el repo, corre `setup.sh` y puede quedar desfasada | El clon es permanente; basta `git pull` |
| CLAUDE.md se lee "a mano" desde los docs del Proyecto | Claude Code carga `CLAUDE.md` del repo solo, en cada sesión |
| Las 5 sesiones dependen de que Alejandro elija el modelo a mano | Se pueden definir como subagentes en `.claude/agents/` con su modelo fijo (Opus para Investigación y Guion, Sonnet para Animación, Redes y Laboratorio) |
| Las conversaciones se van a borrar | Las sesiones quedan guardadas en la laptop y todo lo importante en git |

## 3. Lo que se pierde o cambia (riesgos)

| Riesgo | Qué tan grave | Mitigación |
|---|---|---|
| **Celular**: hoy se trabaja desde el teléfono sin depender de la laptop | Medio | **Remote Control**: desde la app del celular (pestaña Code) se maneja la sesión que corre en la laptop, con notificaciones al terminar. Requiere la laptop prendida, conectada y sin suspenderse. Si está apagada, una **sesión en la nube** (pestaña Code) sirve para Guion, Investigación y Redes (solo texto), trabajando sobre el repo de GitHub |
| **RAM de la laptop: 12 GB** (confirmado 2026-11-02). WSL usa por defecto la mitad (~6 GB), un poco menos que la nube (7 GB) | Bajo | Fijar `memory=8GB` en `.wslconfig` (Windows se queda con ~4 GB; cerrar el navegador pesado mientras renderiza). Alcanza para el motor y para Chatterbox en CPU (~2-3 GB) |
| **Disco de 256 GB** | Medio | Hacen falta ~25 GB libres: entorno de voz con torch (~4-5 GB), pesos de Chatterbox (~3-4 GB), renders y caché. Los MP4 viejos se borran o se mueven fuera |
| **Sesiones WSL todavía sin algunas funciones**: terminal integrada, conectores y plugins, el panel de archivos y las sugerencias con `@` | Bajo | El estudio no usa conectores. Para la terminal se usa la de Ubuntu o VS Code (Remote - WSL). Las skills del estudio van como archivos en `.claude/skills/` del repo |
| Límite de uso del plan | Igual que hoy | Claude Code usa el mismo plan. Sonnet para el trabajo largo, como ya se hace |
| Claude sigue sin poder escuchar el audio | Igual que hoy | La diferencia es que Alejandro escucha al instante y responde más rápido |
| Configuración inicial | ~1-2 h una sola vez | Fases 0-2 abajo |

## 4. Plan de migración

Cada paso dice quién lo hace. "Claude" = la primera sesión de Claude Code en la laptop.

### Fase 0 — Requisitos (Alejandro, 10 min)
1. Confirmar que el plan de claude.ai incluye Claude Code (pestaña **Code** en la app de escritorio o en claude.ai).
2. ~~Ver la RAM~~ Hecho: 12 GB.
3. Ver el espacio libre en `C:`: que haya **≥ 25 GB**.
4. WSL2 con Ubuntu ya está instalado; comprobar en PowerShell: `wsl -l -v` (debe decir VERSION 2).

### Fase 1 — Instalar y conectar (Alejandro + Claude, 30 min)
1. (Alejandro) Instalar o actualizar la app de escritorio de Claude en Windows e iniciar sesión.
2. (Alejandro) En la pestaña Code, nueva sesión → selector de entorno → sección **WSL** → Ubuntu. Carpeta: `/home/<usuario>/` (el disco de Linux, **no** `/mnt/c`, que es lento).
3. (Claude, en esa sesión) Instalar lo del sistema dentro de Ubuntu: `git`, `ffmpeg`, `python3-venv`, `libcairo2-dev`, `pkg-config`, `gh` (lo que `setup.sh` no instale).
4. (Alejandro) `gh auth login` para que `git push` funcione con su cuenta de GitHub.
5. (Claude) Crear `C:\Users\<usuario>\.wslconfig` con `memory=8GB` y `processors=` todos los hilos de la laptop. Reiniciar WSL (`wsl --shutdown`).

### Fase 2 — Motor en local y prueba de velocidad (Claude, 30-45 min)
1. `git clone` del repo en `~/estudio-animacion`, `./setup.sh`, `python producir.py --help`.
2. `--cuadros` de El río de los perros (3 momentos) y comparar con los de la nube.
3. **Render completo de El río de los perros** y medir el tiempo (en la nube: 7.5 min) y los niveles (debe dar ~-13.6 LUFS). Si algo sale distinto, se arregla antes de seguir.
4. Anotar el resultado en `context.md` §5.

### Fase 3 — Traer la memoria al repo (Claude, 30 min)
1. Copiar al repo los docs del Proyecto: `CLAUDE.md` y `context.md` en la raíz; `claude/sesiones.md`, `claude/herramientas.md`, `claude/guion_*.md` e `investigacion_*.md` en `docs/estudio/`.
2. Ajustar `CLAUDE.md` al entorno nuevo (cambios mínimos):
   - §4 Protocolo: quitar `add_repo` y la nota de red de la nube; poner `git pull` + `./setup.sh` solo si cambió algo.
   - §8 Memoria: `context.md` se edita en el repo y se hace commit; se quita la regla de "leer justo antes por `project_write`" y se cambia por `git pull` antes de editar.
   - §10 Sesiones: cómo se abre cada una en Claude Code (Fase 4).
   - Mantenerlo corto: el detalle se queda en `context.md` y `docs/estudio/`.
3. Commit + push ("Migración: memoria del estudio al repo").
4. En el Proyecto de claude.ai: reemplazar `context.md` por una nota de 3 líneas: "MIGRADO el <fecha>. La fuente única es el repo `Creepty07/estudio-animacion`. No editar aquí". Los demás docs se dejan como respaldo.

### Fase 4 — Las 5 sesiones en Claude Code (Claude, 30 min) — **HECHA 2026-11-02**
> Se cambió el punto 1 al diseñarla con la skill `code-architect`: un subagente no puede conversar con Alejandro (solo devuelve un resultado), así que una sesión completa como Guion o Redes no cabe en uno. Las 5 sesiones siguen siendo conversaciones principales (CLAUDE.md §10) y los subagentes son 4 tareas cerradas que esas sesiones delegan (CLAUDE.md §10.1): `verificador-fuentes`, `revisor-guion`, `revisor-cuadros` y `verificador-video`. (La skill también genera `code-reviewer` y `architecture-verifier`; se quitaron porque son para proyectos de código.) Se agregó un hook que hace `git pull` al abrir cada sesión. El punto 4 (Social Media Skills) queda pendiente y opcional.

1. ~~Crear `.claude/agents/` con un archivo por sesión: `investigacion.md`, `guion.md`, `animacion.md`, `redes.md`, `laboratorio.md`.~~ Reemplazado por los 4 subagentes de arriba.
2. Forma de trabajo: Alejandro abre una sesión con nombre ("Estudio · Guion · La Planchada") y le dice `Sesión: Guion`; esa sesión trabaja con su rol. Para tareas pesadas puede delegar en el subagente del rol.
3. `.claude/settings.json` con permisos: permitir sin preguntar `python producir.py`, `python -m motor...`, `ffmpeg`, `ffprobe`, `git add/commit/pull/push`; prohibir `git push --force` y borrar fuera del repo.
4. (Opcional) Las 12 skills de Social Media Skills como carpetas en `.claude/skills/` del repo (son Markdown; las partes de pago se siguen ignorando).
5. `.gitignore`: `out/`, `.venv*`, modelos de voz, renders.

### Fase 5 — Destrabar el piloto de voz (Laboratorio)
0. **De preferencia en la PC del tío** (GPU con CUDA, ver §5). Si no está disponible, en la laptop en CPU.
1. Bajar directo de Hugging Face los pesos de Chatterbox y el paquete `es-mx-latam` (lista en `herramientas.md` §2.3) a `~/modelos/` (fuera del repo).
2. `.venv-tts` aparte, instalar desde el código de GitHub, `motor/audio/tts_chatterbox.py`, medir velocidad y hacer las 3 muestras.
3. Alejandro las escucha ahí mismo y decide. El release de GitHub con los pesos pasa a ser opcional (solo si alguna vez se quiere voz en una sesión en la nube).

### Fase 6 — Primer video 100 % local
1. La siguiente historia aprobada se anima completa en la laptop.
2. Comparar con la nube: tiempo total por video, número de idas y vueltas, problemas.
3. Si sale bien, la migración se da por cerrada en `context.md` §7.

### Fase 7 — Celular
1. En la sesión de la laptop: `/remote-control` y vincular desde la app del celular (pestaña Code). Activar las notificaciones.
2. Windows: que la laptop no se suspenda cuando está conectada a la corriente.
3. Para trabajo de texto con la laptop apagada: sesión en la nube desde la pestaña Code sobre el repo (lo que haga se sube a GitHub y la laptop lo trae con `git pull`).

## 5. Segunda máquina: la PC del tío (uso ocasional)

Datos (Alejandro, 2026-11-02): tarjeta gráfica NVIDIA 2060 Super (es RTX, 8 GB de VRAM, con CUDA) y 16 o 32 GB de RAM DDR4 (sin confirmar cuál).

**Para qué sirve y para qué no:**

| Tarea | ¿Gana con la PC del tío? | Por qué |
|---|---|---|
| Voz (Chatterbox, y Qwen3-TTS 1.7B si Chatterbox no convence) | **Sí, mucho** | Estos modelos corren en GPU con CUDA; en CPU son lentos. Es el mejor lugar para el piloto de voz y para generar las voces de una historia |
| Render de video | Poco | Cairo dibuja en CPU; la GPU solo podría acelerar la codificación final (NVENC). Ayuda que tenga más RAM y núcleos, nada más |
| Guion, investigación, redes, escenas, sonido | No | Son trabajo de texto y CPU: la laptop basta |

**Regla de oro: el repo es lo único que viaja entre máquinas.** Las sesiones de Claude Code viven en cada computadora; lo que no esté en git no existe en la otra.
- Al llegar a la PC del tío: `git pull`. Al irse: commit + push de todo, sin excepción.
- Las voces generadas allá se guardan en el repo (o como release si pesan mucho), para que la laptop renderice sin volver a generarlas. Los WAV de narración de una historia pesan pocos MB.
- Los pesos de los modelos (~3-4 GB) no van al repo: se bajan en cada máquina a `~/modelos/`.

**Cómo prepararla (una vez, con permiso del tío):**
1. Instalar WSL2 + Ubuntu (pide permisos de administrador y reiniciar).
2. Actualizar el driver de NVIDIA en Windows; el soporte de CUDA en WSL viene con el driver. Comprobar dentro de Ubuntu con `nvidia-smi`.
3. App de escritorio de Claude → pestaña Code → sesión WSL, igual que en la laptop (Fase 1). Clonar el repo y `./setup.sh`; en `.venv-tts`, torch con CUDA.
4. Medir: misma muestra de voz en GPU vs. CPU de la laptop.

**Cuidados por ser una PC prestada:**
- Cerrar sesión de Claude y de GitHub al terminar (`gh auth logout`), o usar un token de GitHub con permiso solo para este repo y fecha de vencimiento.
- No dejar renders ni modelos ocupando su disco si él no quiere: `~/modelos` y `out/` se pueden borrar al final.
- Remote Control desde el celular funciona igual, mientras esa PC esté prendida.

## 6. Vuelta atrás
Si algo falla, no se pierde nada: el repo tiene todo y el Proyecto de claude.ai sigue ahí. Se puede volver a trabajar desde la web clonando el repo, como hasta hoy.

## 7. Fuentes
- Claude Code en WSL (requisitos y funciones disponibles): https://code.claude.com/docs/en/desktop-wsl.md
- Claude Code desde el celular (sesiones en la nube, Remote Control, notificaciones): https://code.claude.com/docs/en/mobile.md
- Mapa de la documentación (desktop, subagentes, memoria, skills): https://code.claude.com/docs/en/claude_code_docs_map.md
