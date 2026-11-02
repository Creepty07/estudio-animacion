# Sesiones del estudio — quién hace qué

> **Nota (2026-11-02):** este doc ahora vive en el repo. Donde dice "doc del Proyecto `claude/<x>.md`", léase `docs/estudio/<x>.md`. La regla de §5 ("leer justo antes porque se reemplaza completo") se cumple con `git pull` antes de editar y commit + push después (ver CLAUDE.md §8).

Diseño del 2026-11-02, a pedido de Alejandro: el estudio trabaja con varias sesiones (conversaciones) dentro del mismo Proyecto, cada una con una función. Las sesiones no se ven entre sí. **Lo único que comparten son los docs del Proyecto y el repo.** Por eso todo lo que una sesión decide o entrega queda escrito ahí antes de terminar.

## 1. Las 5 sesiones

| # | Sesión | Función | Modelo | Por qué ese modelo |
|---|---|---|---|---|
| 1 | **Investigación** (investigador + historiador) | Proponer ideas de cualquier tipo y verificar los datos reales (leyendas, historia, lugares, fechas) con fuentes | Opus 5.5 | Leer fuentes, separar lo verificado de lo inventado y no fabricar datos exige el mejor juicio |
| 2 | **Guion** | Convertir la ficha de investigación en un guion por escenas aprobado | Opus 5.5 | El gancho, el ritmo y el tono deciden el video. Un guion flojo no lo salva ninguna animación |
| 3 | **Animación** (producción) | Del guion aprobado al MP4 verificado: dibujo, escenas, sonido, render, portada | Sonnet 5.5 | Es código largo y repetitivo sobre el motor. Sonnet lo hace bien, más rápido y gastando menos del límite de uso |
| 4 | **Redes** (publicación y crecimiento) | Paquete de subida, calendario, perfil, métricas, comentarios y post-mortems | Sonnet 5.5 (Opus para la revisión de cada 4 semanas) | Textos cortos y lectura de métricas. La decisión de rumbo de cada 4 semanas pesa más |
| 5 | **Laboratorio** (voz y motor) — temporal | Piloto de voz (TTS) y mejoras del motor que no son de una historia | Sonnet 5.5 (Opus si hay que decidir arquitectura o el piloto se atora) | Trabajo técnico de código y audio |

### Cambios respecto a la propuesta de Alejandro (y por qué)

- **Investigador + Historiador = una sola sesión.** El contenido es variado (Alejandro, 2026-11-02: no solo leyendas): leyendas y hechos reales, pero también ficción original. La parte "historiador" (verificar fuentes) solo se activa cuando la pieza toca datos reales. Separarla en otra sesión dejaría una sesión casi vacía y duplicaría búsquedas.
- **Se agrega Laboratorio (temporal).** El TTS sigue pendiente y es trabajo técnico que no pertenece a ninguna historia. Si se mete en Animación, se mezcla con la producción y se atrasan los videos. Cuando termine el piloto de voz, Laboratorio puede cerrarse y sus tareas pasan a Animación.
- **No hay sesión de "dirección".** El director es Alejandro y el tablero común es `context.md`. Una sesión más solo para coordinar sería burocracia.
- **El sonido no tiene sesión propia.** Depende de los tiempos de cada escena (constantes en MAYÚSCULAS) y se hace junto con la animación.

## 2. Responsabilidades y alcance

### 1 · Investigación
- **Hace:**
  - Mantener el banco de ideas, que es variado: leyendas y folclore (incluido Querétaro), misterios e historia real, ficción original de suspenso, terror o ciencia ficción, efemérides del calendario y temas que pidan los comentarios. Todo en el mismo estilo de animación. Proponer seguido piezas **interactivas (elige 1, 2 o 3)**, porque es lo que promete la bio.
  - Si la pieza es ficción pura, la ficha es corta (premisa, giro, 3 finales si es interactiva, riesgos) y no lleva verificación.
  - Para la historia elegida, verificar la versión tradicional, las variantes y los datos con búsqueda web (modo *extended*) o con la skill `deep-research` si el tema es grande.
  - Priorizar fuentes primarias y académicas: Sahagún, INAH, universidades, Secretaría de Cultura, museos.
  - Separar en tres columnas: **verificado** (con fuente), **versión popular** (sin fuente primaria) y **libre para ficción**.
  - Revisar que todo sea de dominio público u original.
  - Dejar listo el texto de fuentes para el comentario fijado.
- **Entrega:** doc del Proyecto `claude/investigacion_<historia>.md` (plantilla en §4) y 3-5 ideas en `context.md` §6.
- **No hace:** guion, código ni publicación.

### 2 · Guion
- **Hace:**
  - Brief: tipo (`unico`, `lineal`, `interactiva`), duración, tono, paleta, narrador (por defecto ninguno).
  - Guion por escenas: tabla con #, duración, texto en pantalla, visual clave y sonido.
  - Gancho en el primer segundo; texto a ≤ 2.9 palabras por segundo; diálogos de personajes como subtítulos con etiqueta; cierre con llamado a comentar.
  - Iterar con Alejandro **hasta que lo apruebe**.
  - Solo usa datos de la ficha de investigación. Lo que no esté ahí se marca como ficción o se le pide a Investigación.
- **Entrega:** doc del Proyecto `claude/guion_<historia>.md`, con la línea `ESTADO: APROBADO (fecha)` y las notas para Animación (qué dibujos nuevos hacen falta, momentos de susto o golpe, duración estimada). Además, una fila nueva en `context.md` §3.1.
- **No hace:** código ni render. No cambia datos verificados.

### 3 · Animación
- **Hace:**
  - Antes de empezar: protocolo de CLAUDE.md §4 (conectar y clonar el repo, `git fetch`, `./setup.sh`).
  - Copiar el guion aprobado a `historias/<h>/GUION.md`.
  - Producir: dibujos, escenas, sonido, gradación y sustos.
  - Cuadros clave antes del render, render completo y verificación (duración, audio en LUFS y pico, hoja de contacto).
  - Recomprimir con `-crf 26`, hacer la portada con `motor.portada`, entregar el MP4 y la portada.
  - Commit y push; actualizar `context.md` §3.
  - Correcciones que pida Alejandro.
- **Entrega:** MP4 + portada al chat, commit en `origin/main` y fila en §3.2.
- **No hace:**
  - Cambiar la historia: si algo del guion no funciona en pantalla, propone el ajuste y Alejandro decide.
  - Textos de publicación.
  - Herramientas grandes de motor sin pasar por Laboratorio. Las pequeñas sí: si una pieza sirve para todos los videos, va en `motor/`.

### 4 · Redes
- **Hace:**
  - Paquete de subida por video en `publicacion/<historia>.md` del repo (o doc del Proyecto si no hay repo): descripción, hashtags (3-6), comentario fijado con la fuente, ajustes y fecha y hora sugeridas.
  - Calendario de publicación (`context.md` §6) y perfil (bio, foto).
  - Leer métricas de capturas de TikTok Studio y anotarlas en §4: vistas, retención media, % que vio todo, comentarios, compartidos, seguidores ganados.
  - Escribir post-mortems en §9, separando "la idea o el formato no funcionó" de "fue el día, la hora o el algoritmo".
  - Sugerir respuestas a comentarios y pasar a Investigación los comentarios que piden historias.
  - Cada 4 semanas (con Opus): revisar el objetivo de 12 videos y decidir qué formato repetir.
- **No hace:** publicar por Alejandro, prometer viralidad, inventar métricas ni usar programadores de pago.

### 5 · Laboratorio
- **Hace:**
  - Piloto de voz: Chatterbox latino según `claude/herramientas.md` §2.3. Si no sirve, la opción de la voz grabada.
  - Herramientas generales del motor, por ejemplo personajes y escenarios verticales reutilizables o la pantalla de elección en vertical para las interactivas.
  - Rendimiento.
  - Mantener al día `docs/GUIA_MOTOR.md` y el README del repo.
- **Entrega:** código en `motor/` con commit y push, notas en `context.md` §3.3 y §5, y muestras de audio para que Alejandro decida.
- **No hace:** videos de historias.

## 3. Cómo pasa el trabajo de una sesión a otra

```
Investigación ──ficha──► (Alejandro elige) ──► Guion ──guion APROBADO──► Animación ──MP4 + portada──► (Alejandro revisa audio)
      ▲                                                                                                │
      └──── ideas de comentarios ◄──── métricas y post-mortem ◄──── Redes ◄──── paquete de subida ◄────┘
Laboratorio: en paralelo; entrega herramientas a Animación.
```

- **Columna "Etapa" en `context.md` §3.1:** cada historia tiene una etapa. Cada sesión la avanza al terminar su parte.
  - Etapas: `idea` → `investigada` → `guion en revisión` → `guion aprobado` → `en animación` → `entregada` → `aprobada por Alejandro` → `publicada` → `con métricas`.
- **Cómo se presenta Alejandro en cada sesión:** pone el nombre a la conversación ("Estudio · Guion") y en el primer mensaje dice `Sesión: Guion` (o la que sea), más la historia si aplica. La sesión lee CLAUDE.md, context.md y este doc, y trabaja solo dentro de su función. Si no dice la sesión, se deduce de lo que pide. Si no se puede deducir, se pregunta en una línea.
- **Cuando una sesión se hace muy larga** (el contexto se llena), se abre otra con la misma función. Como todo está en los docs, no se pierde nada.
- **Al terminar cada tarea**, la sesión deja escrito: qué entregó, dónde quedó y cuál es el siguiente paso (y de qué sesión).

## 4. Plantilla de la ficha de investigación (`claude/investigacion_<historia>.md`)

```
# Investigación — <Título>
Fecha · Estado: lista / incompleta
## Resumen de la versión tradicional (5-8 líneas)
## Verificado (dato → fuente con enlace)
## Versión popular (sin fuente primaria; usar como "se cuenta que")
## Variantes regionales
## Libre para ficción (personajes, nombres, lugares inventados)
## Fechas útiles para publicar
## Riesgos (temas sensibles, derechos, datos dudosos que NO se usan)
## Texto de fuentes para el comentario fijado (≤ 300 caracteres)
## Fuentes (lista con enlaces)
```

## 5. Reglas para editar `context.md` entre varias sesiones

`context.md` se reemplaza completo cada vez que alguien lo escribe. Si dos sesiones lo editan al mismo tiempo, la última borra lo de la otra. Por eso:

1. Leer `context.md` **justo antes** de escribir (nunca desde una copia leída al inicio de la sesión), cambiar solo lo necesario y escribirlo de inmediato.
2. Cada sección tiene una sesión dueña; las demás solo agregan:

| Sección | Dueña |
|---|---|
| §1 Perfil, §2 Reglas, §7 Decisiones | Cualquiera, cuando Alejandro confirme algo |
| §3.1 Historias | Guion crea la fila; Animación y Redes avanzan la etapa |
| §3.2 Videos | Animación |
| §3.3 Recursos | Animación y Laboratorio |
| §4 Métricas, §9 Post-mortems | Redes |
| §5 Patrones | Todas (solo agregar) |
| §6 Calendario e ideas | Investigación y Redes |
| §8 Pendientes | Todas (marcar con la sesión responsable) |

3. Lo largo (fichas, guiones, paquetes, investigación de herramientas) va en su propio doc. En `context.md` queda una línea con el enlace. Así el archivo no crece sin control.
4. Actualizar "Última actualización" con la fecha y la sesión que escribió.
