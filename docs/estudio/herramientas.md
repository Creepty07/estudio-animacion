# Herramientas evaluadas — skills, plugins y modelos

> **Nota (2026-11-02):** este doc ahora vive en el repo. La restricción de red de abajo es **solo de la nube de claude.ai**: en la laptop y en la PC del tío (Claude Code local en WSL) sí se llega a Hugging Face, así que el piloto de voz baja los pesos directo y el release `modelos-tts-v1` pasa a ser opcional. El piloto va de preferencia en la PC del tío (GPU RTX 2060 Super, CUDA). Ver `docs/estudio/migracion_claude_code.md` §5 y Fase 5.

Investigación hecha el 2026-11-02 (sesión con Opus 5.5). Criterios: que aporte valor real al estudio, que sea gratis y local (o gratis y sin dar acceso a la cuenta), que sea seguro (código revisable, sin `curl | bash`, sin llaves de servicios de pago), que esté mantenido y que funcione con Claude en este entorno.

**Restricción del entorno de trabajo (comprobada el 2026-11-02):** desde la nube de Claude se llega a PyPI (pip), npm y GitHub (clonar y descargar *releases*), pero **no** a Hugging Face, ModelScope, hf-mirror, download.pytorch.org ni a los servidores de modelos de Whisper. Cualquier modelo que solo viva en Hugging Face hay que subirlo una vez como *release* del repo `Creepty07/estudio-animacion` (así se baja Kokoro, desde un release de GitHub). La máquina tiene 2 núcleos de CPU, 7 GB de RAM y no tiene GPU.

## 1. Resumen por función

| Función | Recomendación | Estado |
|---|---|---|
| Investigación / historia | Lo que ya hay: búsqueda web (modo *extended* para fechas y fuentes) y la skill `deep-research`, que ya está en la cuenta. No hace falta instalar nada | Listo |
| Guion | 4 skills de **Social Media Skills** (MIT): `hook-writer`, `short-form-video-script`, `tiktok-script` y `storytelling-and-narrative`. Son opcionales: el método de CLAUDE.md ya cubre lo esencial | Por instalar (opcional) |
| TTS (voz) | **Piloto con Chatterbox Multilingual, paquete de español latino (MIT)**. Alternativa: la voz de Alejandro o de alguien que dé permiso. No se encontró ninguna skill de TTS lista que sea segura y sirva | Pendiente: piloto en la sesión Laboratorio |
| Animación | Seguir con el motor propio. Ningún plugin ni skill lo mejora sin cambiar todo el estilo o meter servicios de pago | Listo |
| Sonido / música | Seguir sintetizando en el motor. Opcional: efectos CC0 que Alejandro descargue y adjunte | Listo |
| Redes sociales | 8 skills de **Social Media Skills**: `tiktok-growth`, `caption-writer`, `hashtag-strategy`, `analytics-and-reporting`, `content-calendar`, `profile-optimization`, `reply-and-comment-writer` y `platform-specs-and-validation`. Publicar a mano: con 2-3 videos por semana no conviene un programador de publicaciones | Por instalar |
| Revisión del video | Lo que ya hace el motor: cuadros sueltos, hoja de contacto, duración y niveles (LUFS) | Listo |

## 2. Voz (TTS): el pendiente principal

Lo que pide Alejandro: una voz "natural, humana y tétrica si aplica", gratis y local. Kokoro se descartó: en español suena plana, y los efectos encima la empeoraron (v1 de La Llorona).

### 2.1 Candidatos

| Modelo | Español | Licencia | Control de emoción | ¿Corre aquí? | Veredicto |
|---|---|---|---|---|---|
| **Chatterbox Multilingual V3** (Resemble AI) + paquete **es-mx-latam** | Sí; hay un *fine-tune* dedicado a español latino/mexicano | MIT (permite uso comercial y redistribuir) | `exaggeration` (expresividad) y `cfg_weight` (ritmo). Para tono dramático: exaggeration ≈ 0.7, cfg ≈ 0.3. Clona una voz de referencia | Pesos solo en Hugging Face (bloqueado aquí) → hay que subirlos como release del repo. ~500 M de parámetros; no hay datos de velocidad en CPU, así que hay que medirla | **Primera opción para el piloto** |
| **Qwen3-TTS** 0.6B / 1.7B (Alibaba, ene 2026) | Sí (10 idiomas) | Apache 2.0 | *VoiceDesign* (solo 1.7B): se describe la voz en texto ("voz grave, susurrante, de anciano"). También clona con 3 s de audio | Ejemplos pensados para GPU (CUDA). En 2 núcleos de CPU probablemente es muy lento. Pesos en HF y ModelScope (los dos bloqueados) | Segunda opción, solo si el piloto 1 falla y hay GPU disponible |
| **Grabar la voz de una persona** (Alejandro o alguien que dé permiso) | Nativo | Propia | Total: la persona actúa | El motor ya lo soporta (`"file"` en `VOICES`) | **La más humana, sin depender de ningún modelo.** Cuesta grabar cada guion |
| Kokoro (actual) | Sí, pero plano | Apache 2.0 | No | Sí | Rechazado por Alejandro |
| Piper | es_MX / es_ES | MIT; el repo nuevo es GPL | No | Sí (rápido en CPU); voces en HF | Natural pero plano; no es "tétrico" |
| MeloTTS | Sí | MIT | No | Sí, en CPU | Plano |
| XTTS-v2 (Coqui) | Sí | Coqui Public Model License: **no comercial**. Coqui cerró en 2024 | Limitado | Lento en CPU | Descartado por la licencia (la cuenta puede monetizar) |
| F5-TTS, Fish Speech / OpenAudio S1-mini | Sí | Pesos **CC-BY-NC** (no comercial) | Etiquetas | Lento | Descartado por la licencia |
| Supertonic 3 | 31 idiomas | No está claro | Las emociones son de pago (solo en su API) | Sí, en CPU | Descartado |
| Pocket TTS (Kyutai) | Según la fuente, 6 idiomas | Sin confirmar | No | Sí, en CPU | Sin confirmar que haya español de calidad; no se usa |
| Orpheus, Dia, Sesame CSM, Bark, Higgs Audio | Español débil o nulo | Varias | Sí | Necesitan GPU | Descartados |
| ElevenLabs y otros servicios | Sí | De pago | Sí | — | Fuera: rompe la regla de $0 |

### 2.2 Skills de TTS que se revisaron

- `voice-chatterbox-tts` (oyi77/1ai-skills, en claudskills.com): es un solo SKILL.md dentro de una colección enorme y no auditada; no se pudo revisar qué ejecuta. **No se instala.** Es más seguro escribir un módulo propio en el motor (código revisable y con la interfaz de `motor/audio/tts.py`).
- `ai-voiceover` (Social Media Skills): gira alrededor de ElevenLabs (de pago). **No sirve.**
- No apareció ninguna skill de TTS en el catálogo de plugins de la cuenta ni en las skills de Alejandro.

### 2.3 Plan del piloto (sesión Laboratorio)

1. **Conseguir los pesos.** Desde aquí no se llega a Hugging Face. Hay dos caminos:
   - (a) Si la sesión está vinculada a la computadora de Alejandro, bajar desde ahí `ResembleAI/chatterbox` (archivos `ve.pt`, `t3_mtl23ls_v2.safetensors`, `s3gen.pt`, `grapheme_mtl_merged_expanded_v1.json`, `conds.pt`, `Cangjie5_TC.json`) y el paquete `ResembleAI/Chatterbox-Multilingual-es-mx-latam`.
   - (b) Que Alejandro los baje él mismo (con el navegador o con `huggingface-cli download`).
   - En los dos casos, subirlos a un release `modelos-tts-v1` del repo, con el archivo LICENSE (MIT). Si algún archivo pasa de 2 GB (el límite de GitHub), se parte con `split` y `setup.sh` lo vuelve a unir.
2. **Instalar aparte.** Crear `.venv-tts` (un entorno de Python separado) e instalar desde el código fuente de GitHub, no desde PyPI: la versión de PyPI (0.1.7) todavía no trae V3 ni el paquete latino. Va aparte porque chatterbox fija versiones (`numpy<2`, `torch==2.6`, `librosa==0.11`) que podrían romper el motor.
3. **Conectarlo al motor.** Crear `motor/audio/tts_chatterbox.py` con la misma interfaz que `tts.py`. Por dentro llama al entorno separado con `subprocess`, carga el modelo con `from_local(ckpt_dir, device="cpu")` y respeta la caché `out/_tts_cache/`. Se elige el motor de voz en `historia.py` (`TTS_ENGINE = "chatterbox"`).
4. **Medir y hacer muestras.** Medir la velocidad en CPU. Si 60 s de voz tardan más de ~15 min, se considera inviable aquí. Generar 3 muestras cortas del mismo texto (narrador grave; susurro; anciana) con 2 ajustes de `exaggeration`/`cfg`. Pasárselas a Alejandro: Claude no puede oírlas.
5. **Decide Alejandro.** Si aprueba una voz, la regla "sin narrador por defecto" se cambia solo si él lo dice. Si no, se queda sin narrador y se prueba con la grabación de una persona.

Nota: Chatterbox marca cada audio con una marca de agua inaudible (Perth). No afecta el sonido; solo permite detectar que es voz sintética.

## 3. Social Media Skills (redes y guion)

- **Qué es:** 106 skills con licencia MIT, de Frank Heijdenrijk y el equipo de WoopSocial (https://github.com/social-media-skills/skills). Release v1.0.1 de julio de 2026; último commit el 2026-10-15. Está en el Anthropic Directory (revisión del directorio, *tier* comunidad).
- **Seguridad:** se clonó y se revisó el 2026-11-02. Son instrucciones en Markdown y no traen hooks ni servidores MCP. Los únicos scripts (`scripts/*.sh`) sirven para construir los ZIP; no se ejecutan al usar las skills.
- **Ojo:** muchas skills mandan a herramientas de pago: WoopSocial para publicar y medir (aparece en ~1600 líneas), ElevenLabs, Veo, HeyGen, CapCut. **Esas partes se ignoran.** Aquí manda CLAUDE.md: $0 y publicación manual. También piden un `brand-profile` y una `voice`; en este estudio eso equivale a context.md §1 y al tono de la cuenta.
- **Lo bueno:** no inventan métricas, no prometen viralidad y ya incluyen cómo funciona TikTok en 2026 (gancho de ~1 s, retención, rewatch, búsqueda por palabras clave).
- **Cómo instalar solo lo útil:** no conviene instalar el plugin completo, porque son 106 skills que se activan por su descripción. Mejor bajar los ZIP sueltos del release v1.0.1 y subirlos en claude.ai → Customize → Skills. Se necesitan 12:
  - Guion: `hook-writer`, `short-form-video-script`, `tiktok-script`, `storytelling-and-narrative`.
  - Redes: `tiktok-growth`, `caption-writer`, `hashtag-strategy`, `analytics-and-reporting`, `content-calendar`, `profile-optimization`, `reply-and-comment-writer`, `platform-specs-and-validation`.

## 4. Animación: lo que se evaluó y por qué no se cambia

| Herramienta | Qué es | Veredicto |
|---|---|---|
| Motor propio (`Creepty07/estudio-animacion`) | Python + Cairo + audio sintetizado + ffmpeg, con escenas, sonido, gradación, sustos y portadas | **Se queda.** Ya produce el estilo que Alejandro aprobó |
| `animation-studio` (Anthropic Directory, Afaq Rashid, v1.1.0) | Cortos dibujados con código y sonido sintetizado, 9:16 | Hace lo mismo que el motor, pero con su propio método, y metería instrucciones en conflicto. No se instala |
| ClaudeAnimationBase (John Heibel, MIT, p5.js + p5.brush) | Caricaturas con textura de acuarela | Otro estilo y otra tecnología (necesita Node + Chrome, lento sin GPU). Solo como inspiración si algún día se quiere un look pintado |
| Remotion + sus skills oficiales | Video con React | Habría que reescribir todo el motor. No vale la pena ahora |
| Skill `video-making` (incluida en la cuenta) | Guía general para hacer videos | Se puede consultar. Si choca con CLAUDE.md, manda CLAUDE.md |
| Generadores de video con IA (Kling, Veo, Sora; ManyMotions "Horror Story Video Maker"; Abracadabrax) | Video generado por IA | Son de pago y no son "hecho con código ni original". Descartados |
| `watch-video` (Directory) | Saca cuadros clave y transcribe con Whisper | El motor ya saca cuadros y hojas de contacto. La transcripción necesita modelos de HF (bloqueado). Solo valdría si vuelve la narración: serviría para comprobar que la voz dijo bien cada palabra |

## 5. Publicación: programadores de publicaciones

Posty, Ayrshare, So-me Studio, WoopSocial, PostFast, Socialync y similares sirven para publicar en TikTok desde Claude. Todos son servicios de terceros: piden conectar la cuenta y casi todos tienen planes de pago. Con 2-3 videos por semana, publicar a mano cuesta 5 minutos y no expone la cuenta. **No se usan por ahora**; se puede reconsiderar si el ritmo sube mucho.

## 6. Fuentes

- Chatterbox: https://github.com/resemble-ai/chatterbox y https://huggingface.co/ResembleAI/chatterbox (README: V3, paquetes por idioma, MIT, consejos de exaggeration/cfg). Paquete de 0.1.7 revisado con `pip download`.
- Qwen3-TTS: https://github.com/QwenLM/Qwen3-TTS.
- Comparativas de TTS 2026: https://localclaw.io/blog/local-tts-guide-2026 · https://openvoxai.com/blog/best-free-local-tts-models-2026 · https://www.javadex.es/blog/mejores-modelos-open-source-texto-a-voz-tts-2026 · https://betterstack.com/community/guides/ai/supertonic-3.md
- Skill de TTS revisada: https://claudskills.com/skills/voice-chatterbox-tts/
- Social Media Skills: https://github.com/social-media-skills/skills (y su página de releases).
- ClaudeAnimationBase: https://alphasignal.ai/news/claudeanimationbase-turns-a-single-prompt-into-hand-painted-mp4-cartoons
- Remotion y skills: https://www.remotion.dev/docs/ai/skills
- Plugins del Anthropic Directory: búsqueda en el catálogo de la cuenta (2026-11-02).
