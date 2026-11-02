# context.md — Memoria del estudio

Última actualización: 2026-11-02 14:05 · sesión de organización (Opus 5.5): **Fase 4 hecha**: subagentes en `.claude/agents/`, permisos y hook de `git pull` en `.claude/settings.json` (CLAUDE.md §10.1). Antes, 12:40: **migración a Claude Code iniciada** (Alejandro aprobó; arranca en la PC del tío). La memoria del estudio pasa al repo: este archivo, CLAUDE.md y `docs/estudio/`. `setup.sh` ya funciona como usuario normal en WSL (sudo + `.venv`). Antes, 12:20: equipo de cómputo; 12:15: evaluación de la migración; 10:35: estudio por sesiones, herramientas, cuenta y concepto.

## 0. Mapa de documentos (empieza aquí)

| Documento | Dónde | Para qué |
|---|---|---|
| `CLAUDE.md` | Repo (raíz) | Cómo se trabaja: método, reglas, dos máquinas (§8.1) y las 5 sesiones (§10). Claude Code lo carga solo |
| `context.md` (este) | Repo (raíz) | Estado del estudio: perfil, bitácora, recursos, métricas, decisiones y pendientes. **Fuente única desde 2026-11-02**; el `context.md` del Proyecto de claude.ai solo apunta aquí |
| `docs/estudio/sesiones.md` | Repo | Función, alcance, modelo y entregables de cada sesión; traspasos; plantilla de la ficha de investigación; quién edita qué sección de este archivo |
| `docs/estudio/herramientas.md` | Repo | Skills, plugins y modelos evaluados el 2026-11-02, con fuentes; plan del piloto de voz (Chatterbox) |
| `docs/estudio/migracion_claude_code.md` | Repo | Plan de la migración a Claude Code de escritorio (WSL), por fases; §5: la PC del tío. **En curso** |
| `docs/estudio/investigacion_<historia>.md`, `docs/estudio/guion_<historia>.md` | Repo | Fichas y guiones nuevos (formato en `docs/estudio/sesiones.md` §2 y §4) |
| `README.md`, `docs/GUIA_MOTOR.md` | Repo | Cómo usar el motor, cómo escribir escenas, sin narrador, gradación, portadas y límites del entorno |
| `historias/<h>/GUION.md` | Repo | Guion de cada historia tal como se produjo (el de El río de los perros es el mismo del doc del Proyecto `claude/guion_rio_de_los_perros.md`) |
| `publicacion/paquete_subida.md` | Repo | Textos de subida de La Llorona y El río de los perros |

Las rutas `claude/<x>.md` que aparecen más abajo (escritas antes de la migración) son los docs del Proyecto; su copia está en `docs/estudio/<x>.md`.

Las conversaciones anteriores (en las que se hizo todo lo del 1 y 2 nov) se van a borrar: **todo lo necesario está en estos documentos**.

## 1. Perfil operativo

| Dato | Valor |
|---|---|
| Persona | Alejandro, Querétaro, México |
| Plataforma | TikTok |
| Cuenta de TikTok | **Activa: @relatos.en.penumbra** (nombre visible "relatos.en.penumbra"), confirmado por Alejandro el 2026-11-02 con una captura. Foto de perfil: el logo de la vela. La Llorona y El río de los perros ya están publicados con sus portadas |
| Concepto de la cuenta | Bio actual: **"Historias animadas en la sombra. Tú decides el final: comenta 1, 2 o 3."** Alejandro (2026-11-02): **no serán solo leyendas**; el contenido será variado (leyendas, ficción original, suspenso, ciencia ficción como La rebelión, etc.) con **el mismo estilo de animación**. La bio promete finales a elegir: el formato `interactiva` (elige 1, 2 o 3) es el sello de la cuenta |
| Formato por defecto | Vertical 9:16 (1080×1920) |
| Subtítulos | Siempre |
| Narrador | **Por defecto, sin narrador** (regla de Alejandro, 2026-11-01 ~19:06): "hasta que se diga lo contrario o encontremos una mejor voz, natural, humana y tétrica si aplica". Ya no hay que preguntarle historia por historia. Si una historia lleva voz, es un solo narrador fijo. Aplica a La Llorona y El río de los perros. Tendencia clara: no le gustan los narradores TTS |
| Presupuesto | $0, todo gratis y local |
| Objetivo medible | Confirmado 2026-11-01: publicar 12 videos en las primeras 4 semanas de la cuenta y, a partir de ahí, decidir qué formato repetir según retención y comentarios de cada video |
| Ritmo de publicación | Confirmado 2026-11-01: 2-3 videos por semana |
| Revisión del guion antes de animar | Confirmado 2026-11-01: **sí**. Se le muestra el guion y no se anima hasta que lo apruebe (reemplaza el "de corrido" por defecto) |
| Límites de contenido | Ninguno propio, "mientras convenga" |
| Equipo de cómputo | **Principal: laptop Dell Latitude 5430**, Windows 11, **12 GB de RAM** (confirmado 2026-11-02), SSD de 256 GB, WSL2 con Ubuntu, sin GPU NVIDIA. **Ocasional: PC del tío**, NVIDIA 2060 Super (RTX, 8 GB VRAM) y 16 o 32 GB de RAM DDR4 (sin confirmar cuál); útil sobre todo para generar voz en GPU. Cómo se reparte el trabajo: `claude/migracion_claude_code.md` §5 |
| Repositorio del motor | `Creepty07/estudio-animacion` (https://github.com/Creepty07/estudio-animacion), creado el 2026-11-01. Contiene el motor, La rebelión y La Tumba de la Llorona (`origin/main` en `9dcaf4c`). El río de los perros se subió el 2026-11-01 (commit `b1185fc`). Portadas, logo y herramienta de portadas: `665c586`. Paquete de subida: `a911902`. Docs del motor y guion v3 de la Llorona: `b53efda` (2026-11-02). Memoria del estudio y `setup.sh` para WSL: ver `git log` (2026-11-02) |

## 2. Reglas del método vigentes

1. Protocolo antes de producir: repo + `setup.sh`, leer este archivo y verificar datos reales con búsqueda web.
2. Vertical 9:16, subtítulos siempre y **sin narrador por defecto** (si una historia lleva voz, un narrador fijo por historia).
3. Guion por escenas → **aprobación de Alejandro** → cuadros clave → render → verificación → entrega.
4. Lo genérico va en `motor/` y lo de cada historia en `historias/<nombre>/`.
5. Narración a velocidad 0.95-1.1 (más lenta = más sombría, pero alarga el video); si no cabe, se alarga la escena o se recorta el texto. Sin narrador, los subtítulos se leen a ≤ 2.9 palabras por segundo.
6. Nada con derechos de autor; folclore y diseños propios sí.
7. Commit y push al repo con cada video entregado.
8. **Estudio por sesiones (desde el 2026-11-02):** Investigación (Opus), Guion (Opus), Animación (Sonnet), Redes (Sonnet) y Laboratorio (Sonnet, temporal). Cada una trabaja solo en su función y deja todo escrito en los docs. Detalle en `claude/sesiones.md`. Alejandro cambia el modelo de cada sesión.
9. Voces: efectos mínimos. Los efectos que apilan cambio de tono, vibrato y reverb suenan mal (Alejandro rechazó así la v1). Los gritos y lamentos no se generan con TTS.
10. Antes de escribir `context.md`: `git pull` (otras sesiones y la otra máquina lo escriben), tocar solo la sección propia (tabla en `docs/estudio/sesiones.md` §5) y luego commit + push.
11. **Dos máquinas (desde 2026-11-02):** laptop (principal) y PC del tío (voz en GPU). El repo es lo único que viaja: `git pull` al llegar, commit + push al irse (CLAUDE.md §8.1).

## 3. Bitácora

### 3.1 Historias

Etapas: `idea` → `investigada` → `guion en revisión` → `guion aprobado` → `en animación` → `entregada` → `aprobada por Alejandro` → `publicada` → `con métricas`.

| Historia (carpeta) | Tipo | Formato | Narrador | Otras voces | Etapa y estado |
|---|---|---|---|---|---|
| La rebelión de las máquinas (`rebelion_maquinas`) | interactiva, 5 capítulos | horizontal 16:9 (caps. hechos) | `em_alex`, velocidad 1.05 | Tito `em_santa`+robot · Ágora `ef_dora` 0.9+agora · Voz en la radio `ef_dora`+radio | **Etapa: entregada** (cap. 1, 2 videos en 16:9, no publicados). Falta decidir si sigue en 16:9 o pasa a vertical. Guion de los 5 capítulos en `historias/rebelion_maquinas/GUION.md` y en el doc "La rebelión de las máquinas" |
| La Tumba de la Llorona (`tumba_llorona`) | único | vertical 9:16, 67 s | **Ninguno** (`NARRATION = False` en `historia.py`; el texto en pantalla cuenta la historia) | Sin voces habladas. El grito es un efecto de sonido: `historias/tumba_llorona/audio/grito_llorona.wav` si existe, si no lamento sintetizado. El susurro "¿Eres tú... mi niño?" es solo texto + murmullos | **Etapa: publicada** (confirmado el 2026-11-02; la fecha y hora exactas no se registraron, probablemente la noche del 1 nov). v3 sin narrador, con sustos y mucho sonido. Guion, fuentes y texto en pantalla de la v3 en `historias/tumba_llorona/GUION.md` (sección "Versión 3"). Portada y textos de subida listos. Commit `9dcaf4c` |
| El río de los perros (`rio_perros`) | único | vertical 9:16, 84.7 s | **Ninguno** (`NARRATION = False`; Alejandro lo pidió el 2026-11-01 tras aprobar el guion) | Sin voces. Los diálogos de los perros salen como subtítulos con etiqueta ("Perro blanco: «Ya me lavé.»") | **Etapa: publicada** (confirmado el 2026-11-02; ya estaba en el perfil a las 10:31). Portada y textos de `publicacion/paquete_subida.md`. 13 escenas. Guion v2 con fuentes en `historias/rio_perros/GUION.md` y en el doc del Proyecto `claude/guion_rio_de_los_perros.md`. Commit `b1185fc` ya en `origin/main` |

### 3.2 Videos

| Fecha | Historia | Episodio | Contenido | Formato | Duración | Archivo | Estado |
|---|---|---|---|---|---|---|---|
| 2026-11-01 | rebelion_maquinas | ep1 | Cap. 1 "El apagón" hasta la elección | 16:9 | 64 s | `capitulo1_el_apagon.mp4` | Terminado, no publicado |
| 2026-11-01 | rebelion_maquinas | ep2 | Los 3 finales del cap. 1 (malo → regular → bueno) + "Comenta 1, 2 o 3" | 16:9 | 96 s | `capitulo1_los_tres_finales.mp4` | Terminado, no publicado |
| 2026-11-01 | tumba_llorona | ep1 v1 | La Tumba de la Llorona, primera versión con narrador | 9:16 | 60.5 s | `la_tumba_de_la_llorona.mp4` | Descartada: Alejandro dijo que la voz sonaba "horrible", sobre todo el grito |
| 2026-11-01 | tumba_llorona | ep1 v2 | Más sombría, con narrador más lento y grito sintetizado | 9:16 | 68.3 s | `la_tumba_de_la_llorona_v2.mp4` | Reemplazada por la v3: Alejandro pidió quitar al narrador |
| 2026-11-01 | tumba_llorona | ep1 v3 | **Sin narrador**: subtítulos más lentos, glitch con separación de color y destello rojo en los sustos, figura que asoma (escenas 4 y 8), pulso con el latido, tinte frío con grano, mezcla nueva (drones, tecolote, aullido, murmullos, crujidos, stingers, silencios previos a los golpes, tinnitus) | 9:16 | 67.35 s | `la_tumba_de_la_llorona_v3.mp4` (11 MB, recomprimida) | **Publicada** en TikTok (1-2 nov 2026) |
| 2026-11-01 | rio_perros | ep1 v1 | **Sin narrador**: gancho con 3 golpes de huehuetl, título, río del Mictlán, Don Celso y los perros (calle de día y de noche), muerte, orilla con manos-sombra, perro blanco y negro, perro rojizo, cruce a nado, ofrenda y tarjeta "¿Y a ti, quién te cruzaría?". Sonido 100 % sintetizado (tambor, caracol, ocarina, ladridos, agua) | 9:16 | 84.7 s | `el_rio_de_los_perros_final.mp4` (9.7 MB, `-crf 26`) | **Publicada** en TikTok (antes del 2 nov 10:31) |

### 3.3 Recursos reutilizables

| Recurso | Dónde | Notas |
|---|---|---|
| Título con falla, niebla, partículas, lluvia, vela | `motor/kit.py` | Funciona en vertical y horizontal |
| Dani (de pie, trabajando, corriendo, jadeando, gateando, con o sin mochila) | `rebelion_maquinas/dibujo/characters.py`, `dani_poses.py` | Personaje original |
| Tito (robot de limpieza), Centinela (con brazo que alcanza) | `rebelion_maquinas/dibujo/characters.py` | Personajes originales |
| Escenarios: sótano, ciudad con torre, pasillo, elevador y cubo, escalera, calle, azotea, ducto, radio | `rebelion_maquinas/dibujo/env_*.py`, `environments.py` | Diseñados para 16:9 |
| Pantalla de elección, tarjetas de opción y de resultado | `rebelion_maquinas/escenas/ep1/s6_eleccion.py`, `dibujo/cards.py` | Diseñadas para 16:9 |
| Efectos de sonido | `motor/audio/sfx.py` | Golpes, puertas, pasos, choque, latido, radio, stings; soplo de vela, campana, `wail`, pasos en tierra, flor sobre piedra, agua que se cierra, cincel, toque helado; nuevos: `creak` (crujido), `owl` (tecolote), `susto` (golpe disonante), `riser` (subida de tensión), `tinnitus`, `crackle` (velas) |
| Ambientes de fondo | `motor/audio/ambient.py` | Viento, grillos, agua de canal, pájaros del amanecer, zumbido grave, `murmullos` (voces susurradas que no se entienden) |
| Instrumentos de leyenda mesoamericana (sintetizados) | `motor/audio/instrumentos.py` | `huehuetl` (tambor grave), `caracol`, `flauta`/`melodia` (ocarina: frase de notas), `sonaja`. Sin samples |
| Sonidos de perro | `motor/audio/animales.py` | `ladrido(s)`, `aullido` (con `lejano=True`), `quejido`, `grunido`, `olfateo`, `resoplido`, `jadeo`, `pata`, `masticar`. Sintetizados con formantes; no se pudo comprobar de oído |
| Sonidos de agua | `motor/audio/agua.py` | `chapoteo`, `nado`, `agua_sube`, `gota` |
| Reverb por convolución | `motor/audio/synth.py` (`reverb`) | Da espacio (río, cueva, noche abierta) |
| Mezcla sin voz | `motor/audio/master.py` (`bed_peak`) | Con `NARRATION=False` se sube el pico del fondo (0.85-0.9). La mezcla de `rio_perros` aplica una curva de refuerzo por escena para que las partes tranquilas no se sientan vacías |
| Efectos de voz | `motor/audio/voice.py` | `tetrico` (narración sombría limpia), `susurro_suave`, `grito` / `grito_sintetico` (lamento cantado con formantes), `aullido` (perro lejano). `espectro` y `susurro` quedan en el motor pero se descartaron por sonar mal |
| Voz desde archivo | `motor/audio/narration.py` (`line_audio`) | Si un personaje trae `"file"` y existe, usa esa grabación en vez de TTS. Con `"voice": None` usa el sonido sintetizado del efecto |
| Video sin narrador | `NARRATION = False` en `historia.py` | `narration.build` no genera voces; los subtítulos usan sus tiempos tal cual y nada se estira |
| Portadas (frame del video + título con glitch + kicker) | `motor/portada.py` | `python -m motor.portada <historia> <escena> <t> "L1|L2" salida.png ["KICKER"]`; deja el título en y≈1180-1500 para que el recorte 3:4 del perfil no lo corte |
| Investigación de herramientas (TTS, skills, plugins) | doc del Proyecto `claude/herramientas.md` | Antes de instalar algo o probar otra voz, revisar ahí qué ya se evaluó y por qué se descartó |
| Logo del perfil | `marca/logo.py` → `marca/logo_relatos_en_penumbra.png` | Vela con niebla, estrellas, placa de piedra; 1080×1080 |
| Gradación de color final | `motor/grade.py` + `GRADE` en `historia.py` + hook en `motor/render.py` | Desaturar, enfriar, viñeta, grano y parpadeo por escena, sin tocar los dibujos |
| Sustos visuales | `grade.glitch` (separa rojo/azul y desplaza franjas), `grade.rojo` (destello rojo en bordes); tiempos en `SUSTOS` de `historia.py` | Se sincronizan con los golpes de sonido de la mezcla |
| Capas estáticas en caché | `motor/layers.py` (`paint_layer`) | Fondos pesados se dibujan una vez; baja mucho el tiempo de render |
| Cámara centrada en un punto del mundo | `motor/primitives.py` (`camera_center`) | Acercarse a un punto sin salirse del cuadro (limitar el centro a lo visible) |
| Dibujos de la Llorona (vertical): panteón, tumbas, velas, cempasúchil, Tomás, la abuela, la Llorona, Tenochtitlan, canal, primer plano de la flor, tarjeta de cierre | `tumba_llorona/dibujo/` | Personajes y diseños originales; reutilizables en otras historias de folclore |
| Dibujos de El río de los perros (vertical): perros (rojizo, blanco, negro, nadando), Don Celso (de pie, agachado, arrodillado, a cuestas), calle de pueblo día/noche, cuarto con vela, río del Mictlán con estela de perro, manos-sombra, ojos ámbar, ofrenda con perrito de barro, tarjeta de cierre | `rio_perros/dibujo/` | Diseños originales. El perro negro necesita halo frío para no perderse en la noche |

## 4. Métricas acumuladas

Se actualizan cuando Alejandro comparta capturas de TikTok Studio (vistas, retención media, % que vio todo, comentarios, compartidos y seguidores ganados por video).

| Fecha de corte | Cuenta | La Tumba de la Llorona | El río de los perros | Fuente |
|---|---|---|---|---|
| 2026-11-02 10:31 | 5 seguidores · 18 likes en total · 0 seguidos | 106 vistas | 50 vistas | Captura del perfil enviada por Alejandro. Todavía sin retención ni comentarios; menos de 24 h desde la publicación, así que no sirve para sacar conclusiones |

## 5. Patrones y aprendizajes

- 2026-11-01: La narración natural tarda 1.3-1.6 veces más que el tiempo que tenía el subtítulo. Por eso existe la línea de tiempo con voz.
- 2026-11-01: Las voces de espeak-ng suenan demasiado robóticas para narrar; se usa Kokoro. Tito suena mejor con Kokoro + efecto robot.
- 2026-11-01: Revisar cuadros antes del render evitó repetir renders: los subtítulos tapaban a los personajes y la viñeta fallaba en vertical.
- 2026-11-01: Medido con Kokoro: `em_alex` a 1.05 lee unas 3.3 palabras por segundo. Los tiempos del guion se calculan con la voz real, no a ojo. Bajar la velocidad a 0.93-0.95 alarga un único de 60 s a ~68 s.
- 2026-11-01: Alejandro aprobó el estilo visual (vector plano, iluminación dramática con luz de color, falla en los títulos). Es el estilo fijo de la cuenta para cualquier tipo de contenido (2026-11-02).
- 2026-11-01: En vertical, los subtítulos ocupan aprox. de y 1264 a 1440 (2 líneas, ~34 caracteres por línea). Lo importante va entre 12 % y 70 % de la altura y lejos de la columna derecha. Todo texto o botón de una tarjeta debe quedar por encima de y ~1200.
- 2026-11-01: En Cairo, escalar a 0 (`ctx.scale(0, 0)`) truena con "matriz no invertible": las animaciones que crecen desde cero deben empezar en 0.001.
- 2026-11-01: Con las capas en caché, un único de 60-70 s tarda 4-8 min en renderizar completo; los cuadros sueltos (`--cuadros`) salen en segundos, así que conviene revisar las escenas así antes del render final. El grano de película infla el archivo (18 → 73 MB): se recomprime al final con `-crf 26` (queda en ~10 MB sin pérdida visible).
- 2026-11-01: **La v1 de la Llorona falló en la voz.** El grito pasaba por TTS + cambio de tono + vibrato + reverb apilados y sonó "súper raro"; el susurro con fase al azar se volvía ruido. Lección: un grito no se hace con TTS; usar una grabación real con licencia libre o un lamento sintetizado directamente; y dejar la narración con efectos mínimos. Alejandro terminó prefiriendo **quitar al narrador** y apoyarse en sonido, color y texto.
- 2026-11-01: Sin narrador, el miedo lo llevan el silencio y el contraste: los fondos se "apagan" casi del todo justo antes de cada golpe (escenas 4, 9 y 11), el zumbido agudo (tinnitus) cae después y cada golpe de sonido coincide con un glitch visual. Un tinte muy desaturado y frío con grano hace que el cempasúchil sea el único calor.
- 2026-11-01: Sin narrador conviene mostrar el texto a ≤ 2.9 palabras por segundo; varias frases de la v2 iban a 3.5 y se alargaron las escenas (60 s → 67 s).
- 2026-11-01: Un sonido real (p. ej. el lamento de la Llorona) no se puede descargar desde el entorno de trabajo: ni YouTube (la página no abre) ni bancos de sonido. Alejandro tiene que adjuntar el archivo. Además, el clip "conocido" de YouTube que quiere usar probablemente no es de licencia libre: antes de publicarlo en TikTok conviene confirmarlo.
- 2026-11-01: Claude no puede escuchar el audio: solo verifica sincronía y niveles, no el carácter del sonido ni si "suena bien". Para que Alejandro decida entre opciones conviene mandarle muestras cortas.
- 2026-11-01: Verificación de la v3: 67.35 s, 1080×1920 a 30 fps, AAC estéreo, -13.3 LUFS, pico -0.6 dBFS, sin recortes.
- 2026-11-01: Para leyendas prehispánicas, la fuente primaria útil es Sahagún (*Historia general*, libro III), citada en revistas académicas (Anales del INAH, UAM, tesis UNAM). Muchas notas de prensa mezclan versiones modernas (p. ej. colores del xolo con otro significado); se separan en el guion como "versión popular".
- 2026-11-01: En una conversación el sistema bloqueó conectar el repo con permiso de escritura (`add_repo` con push). Si vuelve a pasar, el guion se guarda como doc del Proyecto y se pasa al repo en la fase de animación.
- 2026-11-01: **Regla fija:** sin narrador por defecto (Alejandro). Solo se vuelve a usar voz si él lo pide o aparece una voz natural, humana y tétrica que apruebe; hasta entonces no se le pregunta historia por historia.
- 2026-11-01: Portadas: el frame con el susto (Llorona S9) y el cruce a nado (perros S11) funcionan mejor que el primer cuadro; los que tienen el gancho en grande esconden los ojos del personaje detrás del título. TikTok recorta la cuadrícula del perfil a ~3:4, por eso el título va en el tercio central-bajo.
- 2026-11-01: **Sin narrador, el sonido tiene que cubrir cada segundo.** En El río de los perros se hizo por capas: cama continua (río, viento, grillos o pájaros + zumbido grave que cambia de color), sonido de acción sincronizado con lo que se ve (pasos, pedradas, ladridos, olfateo, masticar, agua) e instrumentos de leyenda (huehuetl, caracol, ocarina con un tema que baja al principio y sube al final). Los tiempos salen de constantes en MAYÚSCULAS de cada escena para que no se desfasen.
- 2026-11-01: La primera mezcla de El río de los perros salió con las escenas del medio 6-10 dB más bajas que el clímax y valles de -30 dB: se "sentiría vacío". Se corrigió con una curva de refuerzo por escena (con transiciones de 0.35 s). Resultado: -13.6 LUFS, pico -0.7 dBFS, ninguna escena por debajo de -20 dB de promedio y ningún silencio de más de 0.4 s.
- 2026-11-01: Sin narrador, los diálogos de personajes que no hablan (los perros) funcionan como subtítulos con etiqueta ("Perro blanco: «Ya me lavé.»"), y el texto grande sincronizado con golpes de tambor es un gancho que no necesita voz.
- 2026-11-01: Un personaje negro (el perro negro) desaparece contra una noche azul oscuro: necesita un halo frío detrás y borde de luz; los ojos ámbar ayudan.
- 2026-11-01: Un clon de la sesión puede estar desfasado del remoto (el clon traía la v2 de la Llorona, el remoto ya tenía la v3). Antes de producir, hacer `git fetch` y comparar; si no, el rebase al final trae conflictos (en `narration.py` coincidieron dos soluciones al mismo problema).
- 2026-11-01: `add_repo` con push fue bloqueado dos veces por el clasificador automático, pero funcionó al tercer intento, cuando Alejandro pidió explícitamente reintentarlo. Si vuelve a bloquearse: avisarle y esperar su orden; mientras tanto se deja un `git bundle` del commit como respaldo.
- 2026-11-01: Render completo de El río de los perros (13 escenas, 84.7 s) tardó 7.5 min con escenas en paralelo; 57 MB sin recomprimir, 9.7 MB con `-crf 26`.
- 2026-11-02: **Red del entorno en la nube de Claude:** llega a PyPI, npm y GitHub (las descargas de releases funcionan), pero no a Hugging Face, ModelScope, hf-mirror, download.pytorch.org ni a los servidores de Whisper. Un modelo de HF hay que bajarlo fuera (computadora de Alejandro) y subirlo como release del repo. La máquina tiene 2 núcleos, 7 GB de RAM y no tiene GPU.
- 2026-11-02: La versión de PyPI de chatterbox-tts (0.1.7) solo trae Multilingual V2; V3 y el paquete de español latino están en el código de GitHub. Fija `numpy<2`, `torch==2.6` y `librosa==0.11`, así que va en un entorno aparte. Se puede cargar sin internet con `ChatterboxMultilingualTTS.from_local(dir, device)`.
- 2026-11-02: Las skills de terceros "de TTS" que hay en los registros (p. ej. `voice-chatterbox-tts`) no se pueden auditar bien o dependen de servicios de pago. Es más seguro escribir el módulo de voz dentro del motor.
- 2026-11-02: Social Media Skills (MIT) es de buena calidad (no inventa métricas, no promete viralidad, gancho de ~1 s, retención, búsqueda), pero empuja a WoopSocial, ElevenLabs y Veo (de pago): esas partes se ignoran.
- 2026-11-02: En WSL/Ubuntu como usuario normal, el `setup.sh` original fallaba: `apt-get` necesita `sudo` y Ubuntu no deja usar `pip` en el Python del sistema. Ahora, si no es root, usa `sudo` y crea `.venv/` (instala además `python3-venv`, `python3-dev` y `build-essential` para compilar pycairo). Probado en la nube con `ESTUDIO_VENV=1`: instala en ~2.5 min y `--cuadros` renderiza bien. En la nube (root) sigue igual que antes.
- 2026-11-02: `project_write` reemplaza el doc completo. Con varias sesiones, escribir `context.md` desde una copia vieja borra lo que escribió otra sesión: siempre se lee justo antes de escribir.

## 6. Calendario y contexto

| Fecha | Ocasión | Idea |
|---|---|---|
| 1 nov 2026 | Día de Muertos (Todos Santos) | La Tumba de la Llorona: **publicada** |
| 2 nov 2026 | Día de Muertos (fieles difuntos) | El río de los perros: **publicada** (antes de las 10:31) |
| 4-5 nov 2026 | Primera lectura de métricas | Redes: capturas de TikTok Studio de los 2 videos a las 48-72 h |
| ~29 nov 2026 | Fin de las primeras 4 semanas | Redes (con Opus): revisar la meta de 12 videos y decidir qué formato repetir. Van 2 videos verticales listos; faltan ~10 a ritmo de 2-3 por semana |
| 20 nov 2026 | Revolución Mexicana | PENDIENTE: Investigación propone ideas (no tienen que ser leyendas: puede ser ficción original ambientada en la época, idealmente interactiva) |
| 12 dic 2026 | Día de la Virgen de Guadalupe | PENDIENTE (tema sensible: tratar con respeto) |
| 24-25 dic 2026 | Navidad | PENDIENTE |
| Por definir | Ideas guardadas | Candidatas descartadas por ahora el 2026-11-01: leyenda del cempasúchil (Xóchitl y Huitzilin), La Planchada (buena para una interactiva de 3 finales), el Acueducto de Querétaro y Sor Marcela (300 años del inicio de la obra; no hay prueba del amorío), origen de la Catrina (dato curioso, no relato) |

## 7. Decisiones y ajustes del método

- 2026-11-01: El motor vive en un repositorio de GitHub (`Creepty07/estudio-animacion`) y cada conversación lo clona.
- 2026-11-01: Formato por defecto vertical 9:16. La rebelión se hizo en 16:9; falta decidir si sigue así desde el cap. 2.
- 2026-11-01: El narrador se fija por historia y no cambia entre capítulos.
- 2026-11-01: Voces con Kokoro (gratis, local), con efectos mínimos.
- 2026-11-01: **Guion de la Llorona aprobado** ("me gusta, dale"): final oscuro (TOMÁS en la lápida). Alejandro cambió el modelo a Sonnet para la animación.
- 2026-11-01: **Modelo por fase.** Alejandro cambia el modelo y da la orden de arranque de cada fase:

| Fase | Modelo | Por qué |
|---|---|---|
| 1. Historia, guion, investigación de la leyenda | Opus | Aquí la calidad del texto manda: el gancho de los primeros 2 segundos, el ritmo, el tono, los giros y no inventar datos de una leyenda real. Un guion flojo no lo arregla ninguna animación. |
| 2. Animación (escenas, voces, sonido, render, correcciones) | Sonnet | Es trabajo de código largo y repetitivo con la plantilla del motor. Sonnet lo hace bien (así se hizo todo lo de La rebelión), es más rápido y gasta menos del límite de uso. |

- 2026-11-01: Tras ver la v1, Alejandro pidió: voces que "se escuchen bien o se descarten", el grito de la Llorona como grabación real (no generado con un modelo de voz) y un toque más tétrico en narración, ambiente y colores. Se hizo la v2. Alejandro compartió como referencia el clip conocido del grito (https://www.youtube.com/watch?v=_JvypWJ4FfU); no se puede descargar desde aquí.
- 2026-11-01 (18:18): Tras la v2, Alejandro decidió: **La Llorona sin narrador**, con bastantes efectos de sonido y de color para el toque tétrico. Se hizo la v3 (el susurro quedó como texto + murmullos; el grito como efecto).
- 2026-11-01: Alejandro eligió el nombre de cuenta **Relatos en Penumbra** (@relatos.en.penumbra) en lugar de la propuesta "Elige tu final".
- 2026-11-01: Segunda historia de temporada: Alejandro eligió **el xoloitzcuintle y el río del Mictlán** (propuesta 1 de 5). Se escribió como `unico` con un final emotivo y llamado a comentar el nombre de su perro, para variar del final oscuro de La Llorona.
- 2026-11-02: **El estudio trabaja por sesiones** (pedido de Alejandro). Propuso investigador, guionista, historiador, animador y redes. Se recomendó juntar investigador e historiador, agregar un Laboratorio temporal para la voz y el motor, y no tener sesión de dirección (el director es Alejandro y el tablero es este archivo). La tabla de "modelo por fase" de abajo queda como antecedente; ahora manda la tabla de sesiones de CLAUDE.md §10.
- 2026-11-02: **Concepto de la cuenta (Alejandro):** contenido variado, no solo leyendas, con el mismo estilo de animación; la bio promete "Tú decides el final: comenta 1, 2 o 3". Los 2 videos publicados son `unico` (piden comentar "sí/no" o un nombre): conviene que las próximas piezas incluyan pronto interactivas de 3 finales para cumplir lo que promete la bio.
- 2026-11-02: **Herramientas:** se mantiene el motor propio (no se instalan plugins de animación). No se usan skills de TTS de terceros. Se publica a mano (sin programadores de pago). Social Media Skills: solo 12 skills sueltas, opcionales. El TTS pasa a un piloto con Chatterbox Multilingual + paquete es-mx-latam (MIT); la alternativa es grabar una voz humana. Todo en `claude/herramientas.md`.
- 2026-11-02: **Migración a Claude Code de escritorio aprobada y en curso** (Alejandro: "ahorita usaremos la PC de mi tío", tiene ≥ 25 GB libres). El repo pasa a ser la fuente única de la memoria (CLAUDE.md, context.md, `docs/estudio/`). Plan: `docs/estudio/migracion_claude_code.md`. Primera máquina: PC del tío; luego la laptop.
- 2026-11-02: **Subagentes y permisos (Fase 4, skill `code-architect`).** Las 5 sesiones siguen siendo conversaciones principales; los subagentes son tareas cerradas que solo reportan (tabla en CLAUDE.md §10.1). Se crearon 4 por necesidad (`verificador-fuentes`, `revisor-guion`, `revisor-cuadros`, `verificador-video`) y 2 **por política** de la skill, aunque el estudio casi no escribe código nuevo (`code-reviewer`, `architecture-verifier`). No se hizo un subagente por sesión porque un subagente no puede conversar con Alejandro. Permisos: render, ffmpeg y git sin preguntar; `rm`, `sudo` y `git reset` preguntan; `git push --force` prohibido.
- 2026-11-01: **El río de los perros va sin narrador**, con mucho efecto de sonido "que no se sienta vacío" y toque de leyenda. Alejandro: "son los únicos cambios, me gusta lo demás". El guion pasó a v2: gancho de texto con golpes de tambor, subtítulos cortos y diálogos de los perros como subtítulos con etiqueta. Se animó con Sonnet y quedó en 13 escenas y 84.7 s (el guion estimaba ~70 s; el cruce a nado se separó en su propia escena para que el clímax respire).

## 8. Pendientes

- [x] Crear el repo en GitHub y anotarlo en §1 (2026-11-01: `Creepty07/estudio-animacion`).
- [x] Clonar el repo y correr `./setup.sh`.
Cada pendiente indica quién lo hace: (Alejandro) o (sesión).

- [x] (Alejandro) Cuenta confirmada (@relatos.en.penumbra) y los 2 videos publicados (2026-11-02).
- [x] (Alejandro) Decidir la migración a Claude Code de escritorio: **sí** (2026-11-02).
- [x] (organización) Memoria del estudio al repo (CLAUDE.md, context.md, `docs/estudio/`) y `setup.sh` compatible con WSL (2026-11-02).
- [ ] (Alejandro) **PC del tío:** permiso, WSL2 + Ubuntu, driver de NVIDIA al día (`nvidia-smi` en Ubuntu), app de escritorio de Claude → Code → sesión WSL. Pasos en `docs/estudio/migracion_claude_code.md` §5.
- [ ] (primera sesión local, PC del tío) Fase 1-2: `gh auth login`, clonar en `~/estudio-animacion`, `./setup.sh`, render de prueba de El río de los perros midiendo tiempo y LUFS; anotar en §5.
- [ ] (Laboratorio, PC del tío) Fase 5: piloto de voz Chatterbox en GPU.
- [x] (organización) Fase 4: 6 subagentes en `.claude/agents/`, permisos y hook de `git pull` en `.claude/settings.json` (2026-11-02). Falta probarlos en la PC del tío (`/agents`, `/status`).
- [ ] (después) Laptop (Fases 1-2) y Fase 7 (celular). Confirmar si la PC del tío tiene 16 o 32 GB. Opcional: Social Media Skills en `.claude/skills/`.
- [ ] (Alejandro) Abrir las sesiones conforme se necesiten. Ahora tocan Redes (métricas 4-5 nov), Investigación (siguiente historia) y Laboratorio (voz). Se nombran "Estudio · <Sesión>" y el primer mensaje dice `Sesión: <nombre>`.
- [ ] (Alejandro, opcional) Instalar las 12 skills de Social Media Skills: ZIP sueltos del release v1.0.1, en Customize → Skills. Lista en `claude/herramientas.md` §3.
- [ ] (Alejandro, opcional) En las instrucciones del Proyecto, cambiar "un narrador fijo por historia" por "sin narrador por defecto (si hay narrador, uno fijo por historia)". Claude no puede editarlas; CLAUDE.md y este archivo ya tienen la regla nueva.
- [ ] (Laboratorio + Alejandro) **Piloto de voz** con Chatterbox es-mx-latam (`claude/herramientas.md` §2.3): Alejandro baja los pesos de Hugging Face (o vincula su computadora) → se suben como release `modelos-tts-v1` → `.venv-tts` + `motor/audio/tts_chatterbox.py` → medir la velocidad en CPU → 3 muestras → decide Alejandro. (Si se aprueba la migración a Claude Code, este piloto se hace en la laptop y ya no hace falta el release: ver `claude/migracion_claude_code.md` Fase 5.)
- [ ] (Investigación) Siguientes piezas: 3-5 ideas variadas (no solo leyendas), con al menos 1-2 en formato **interactiva (elige 1, 2 o 3)**, como pide la bio. Ficha corta de cada una para que Alejandro elija (calendario: 20 nov; ideas guardadas en §6; La Planchada ya se marcó como buena para interactiva).
- [ ] (Alejandro → Guion/Animación) Decidir si La rebelión (interactiva, cap. 1 ya hecho en 16:9) se rehace en vertical para publicarla: encaja con la bio.
- [ ] (Redes) Leer las métricas de los 2 primeros videos a las 48-72 h y escribir los primeros post-mortems.
- [x] (Alejandro) Crear la cuenta de TikTok @relatos.en.penumbra (hecho).
- [x] Foto de perfil: `marca/logo_relatos_en_penumbra.png` (1080×1080, vela en la oscuridad con niebla; se regenera con `python marca/logo.py`). Entregado el 2026-11-01.
- [x] Portadas de los dos videos: `portadas/portada_la_tumba_de_la_llorona.png` y `portadas/portada_el_rio_de_los_perros.png` (1080×1920; herramienta `python -m motor.portada`). Entregadas el 2026-11-01.
- [x] Paquete de publicación (descripción, hashtags, comentario fijado, orden) de los dos videos: `publicacion/paquete_subida.md`. Entregado el 2026-11-01.
- [x] (Alejandro) Portadas y logo puestos en TikTok (visto en la captura del 2026-11-02).
- [x] Confirmar el objetivo medible y el ritmo de publicación (2026-11-01, ver §1).
- [x] Confirmar si revisa el guion antes de animar (2026-11-01: sí).
- [x] Guion v1 de "La Tumba de la Llorona" con Opus y aprobación de Alejandro (2026-11-01).
- [x] Animar "La Tumba de la Llorona" con Sonnet: v1 (voz rechazada), v2 (más sombría) y v3 sin narrador (2026-11-01, commit `9dcaf4c`).
- [ ] (Alejandro → Animación) **Ver y escuchar la v3 de La Llorona** y dice qué ajustar (volumen de los sustos, grito sintetizado, ritmo del texto, color). Claude no puede oír el audio.
- [ ] (Alejandro → Animación) **Grito real (opcional):** si Alejandro adjunta un archivo con el "¡Aaay, mis hijos!" (WAV, MP3 u OGG), se guarda como `historias/tumba_llorona/audio/grito_llorona.wav` y se re-renderiza; el motor lo usa solo. Confirmar antes que se puede usar (licencia libre o de su propiedad). Mientras tanto va el lamento sintetizado.
- [x] (Alejandro) Publicar La Tumba de la Llorona.
- [x] Guion v1 de "El río de los perros" con Opus y aprobación de Alejandro (2026-11-01).
- [x] Decidir si El río de los perros lleva narrador: **sin narrador** (2026-11-01).
- [x] Copiar el guion al repo (`historias/rio_perros/GUION.md`, versión sin narrador con fuentes).
- [x] Ladrido para El río de los perros: sintetizado (`motor/audio/animales.py`), sin TTS.
- [x] Animar "El río de los perros" con Sonnet: v1 sin narrador, 84.7 s (2026-11-01).
- [ ] (Alejandro → Animación) **Ver y escuchar El río de los perros v1** y dice qué ajustar. Hay que mirar sobre todo: si los ladridos y el aullido sintetizados suenan a perro (Claude no puede oírlos), el volumen de los golpes de tambor, y si 84 s se sienten largos (se puede recortar la calle de día y de noche).
- [x] Push de `b1185fc` y `665c586` a `origin/main` (2026-11-01).
- [x] (Alejandro) Publicar El río de los perros.
- [ ] (Alejandro) Escuchar las voces de La rebelión y decir si el acento y el tono convencen (la v1 de la Llorona mostró que los efectos de voz pueden fallar).

## 9. Post-mortems y lecciones

Sin entradas todavía de videos publicados. Se agregan después de publicar, separando "el formato o la idea no funcionó" de "fue el día, la hora o el algoritmo".
