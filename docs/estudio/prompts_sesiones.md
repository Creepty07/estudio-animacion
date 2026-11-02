# Prompts iniciales de las 5 sesiones

Cómo se usan: en la app de escritorio, **Code → sesión nueva → WSL → carpeta `~/estudio-animacion`**. Ponle el nombre de la sesión (por ejemplo "Estudio · Guion"), cambia el modelo con `/model` y pega el prompt como primer mensaje. El resto del contexto (reglas, historias, pendientes) ya está en `CLAUDE.md` y `context.md`, que la sesión lee sola; por eso los prompts son cortos.

Una sesión por conversación. Cuando se llena el contexto, se abre otra con el mismo prompt: no se pierde nada porque todo queda en el repo.

| Sesión | Modelo (`/model`) | Cuándo abrirla |
|---|---|---|
| Investigación | `claude-opus-5-5` | Ahora: faltan ideas para la siguiente pieza (20 nov, Revolución Mexicana) |
| Guion | `claude-opus-5-5` | Cuando Alejandro elija una idea de la ficha de Investigación |
| Animación | `claude-sonnet-5-5` | Cuando un guion tenga `ESTADO: APROBADO` |
| Redes | `claude-sonnet-5-5` (Opus en la revisión de las 4 semanas) | 4-5 nov, con las capturas de TikTok Studio |
| Laboratorio | `claude-sonnet-5-5` (Opus si hay que decidir arquitectura) | En la PC del tío, para el piloto de voz (GPU) |

## 1 · Investigación

```
Sesión: Investigación.
Lee CLAUDE.md, context.md y docs/estudio/sesiones.md. Hazme el banco de ideas para las siguientes piezas: 5 ideas variadas (no solo leyendas: folclore, hechos reales, ficción original de suspenso, terror o ciencia ficción), con al menos 2 en formato interactiva (elige 1, 2 o 3), porque es lo que promete la bio. Una de ellas debe aprovechar el 20 de noviembre (Revolución Mexicana). Revisa también las ideas guardadas de context.md §6.
Dame una ficha corta de cada una (premisa, giro, 3 finales si es interactiva, riesgos, duración estimada) y tu recomendación principal. Yo elijo; con la elegida haces la ficha completa con fuentes (usa el subagente verificador-fuentes si toca datos reales).
```

## 2 · Guion

```
Sesión: Guion. Historia: <nombre de la idea elegida>.
Lee CLAUDE.md, context.md, docs/estudio/sesiones.md y la ficha docs/estudio/investigacion_<historia>.md (si no existe, es ficción original y la ficha va en context.md §6).
Escribe el brief y el guion por escenas (tabla con #, duración, texto en pantalla, visual clave y sonido), sin narrador salvo que yo diga lo contrario. Pásalo por el subagente revisor-guion antes de enseñármelo. Itera conmigo hasta que lo apruebe y entonces guarda docs/estudio/guion_<historia>.md con ESTADO: APROBADO, crea la fila en context.md §3.1 y deja las notas para Animación (dibujos nuevos, momentos de susto, duración estimada).
```

## 3 · Animación

```
Sesión: Animación. Historia: <nombre de la historia con guion aprobado>.
Haz el protocolo de CLAUDE.md §4 (git pull; setup.sh solo si cambió) y lee el guion aprobado en docs/estudio/guion_<historia>.md. Sigue el método de §5.2: copia el guion a historias/<h>/GUION.md, reutiliza el motor antes de dibujar algo nuevo, y revisa 2-3 cuadros clave con el subagente revisor-cuadros antes del render completo. Al terminar verifica el MP4 con verificador-video, haz la portada, commit y push, y actualiza context.md (§3.1 y §3.2).
Entrégame el archivo, qué conviene revisar y el siguiente paso. Yo valido el audio, tú no puedes oírlo.
```

## 4 · Redes

```
Sesión: Redes.
Lee CLAUDE.md, context.md y docs/estudio/sesiones.md. Te adjunto capturas de TikTok Studio de los 2 videos publicados (La Tumba de la Llorona y El río de los perros) a las 48-72 h: vistas, retención media, % que vio todo, comentarios, compartidos y seguidores ganados.
Anótalo en context.md §4, escribe los primeros post-mortems en §9 separando "la idea o el formato no funcionó" de "fue el día, la hora o el algoritmo", y dime qué cambiar en los siguientes paquetes de subida. Sin prometer viralidad. Si hay comentarios que piden historias, pásalos a Investigación en context.md §8. Después arma el calendario de publicación hasta el 29 de nov (tabla con fecha, video, tipo, gancho y estado).
```

## 5 · Laboratorio (PC del tío)

```
Sesión: Laboratorio. Estoy en la PC del tío (GPU RTX 2060 Super).
Lee CLAUDE.md, context.md y docs/estudio/herramientas.md §2.3. Haz el piloto de voz: confirma con nvidia-smi que la GPU se ve desde WSL, crea .venv-tts aparte de .venv, baja los pesos de Chatterbox Multilingual y el paquete es-mx-latam a ~/modelos/ (fuera del repo), escribe motor/audio/tts_chatterbox.py con la configuración centralizada, mide la velocidad en GPU y genera 3 muestras de audio en un tono natural, humano y tétrico. Yo las escucho y decido; tú no puedes oírlas.
Guarda las muestras (WAV de pocos MB) en el repo, anota resultados en context.md §3.3 y §5, y haz commit y push. Si algo falla, dímelo antes de insistir. Al terminar: gh auth logout solo si te lo pido.
```
