# Guía del motor

Cómo funciona el estudio por dentro, cómo escribir escenas y qué aprendimos produciendo *La rebelión de las máquinas*.

## 1. Flujo de producción

```
historia.py ──► escenas (SUBS + draw) ──► voces (Kokoro) ──► línea de tiempo ──┬─► render de escenas (Cairo → ffmpeg)
                                                                                 └─► banda sonora (numpy) ──► master (voz + ducking)
                                                                                                         └──► build: une todo en el MP4 final
```

1. **Voces** (`motor/audio/narration.py`): cada línea de `SUBS` de cada escena se convierte en audio con la voz de su hablante (`VOICES` de la historia) y el efecto de ese personaje. Se guarda `out/<historia>/audio/voces.json` con la duración real de cada línea.
2. **Línea de tiempo** (`motor/timeline.py`): si una línea dura más que el hueco que tenía su subtítulo, ese tramo de la escena se alarga (hasta `MAX_STRETCH`). Así la animación se adapta a la voz y no al revés.
3. **Render** (`motor/render.py`): cada cuadro se dibuja con Cairo en memoria y se manda directo a ffmpeg (sin PNG intermedios). Se escribe a un `.tmp.mp4` y solo se renombra si ffmpeg terminó bien.
4. **Sonido** (`historias/<h>/sonido/mix_epN.py`): efectos y música sintetizados, colocados con los tiempos de la escena. La pista (`Track`) traduce esos tiempos a la línea de tiempo con voz, y estira sin cambiar de tono los sonidos largos (fondos, alarmas).
5. **Master** (`motor/audio/master.py`): agrega las voces, baja la música cuando alguien habla (ducking) y limita picos.
6. **Build** (`motor/build.py`): concatena escenas con `-c copy` y agrega el audio.

## 2. Contrato de una escena

Cada archivo en `historias/<h>/escenas/epN/` define:

```python
DURATION = 8.0          # segundos sin voz
SUBS = [                # (inicio, fin, texto, hablante|None) — None = narrador
    (0.4, 3.6, "Por el pasillo suenan pasos metálicos.", None),
    (4.3, 6.8, "Instrucción recibida de Ágora.", "TITO"),
]
def draw(ctx, t):       # t = tiempo local de la escena; dibuja a config.W x config.H
    ...
```

- Las constantes de tiempo importantes (apagón, portazos, entrada de un personaje) van en MAYÚSCULAS dentro de la escena para que la mezcla de sonido las use: `T5 + s5.SLAMS[i]`. Así imagen y sonido nunca se desfasan.
- El texto de `SUBS` es lo que se ve; si se debe pronunciar distinto (números, siglas, "-1"), se pone en `SAY` de `historia.py`.
- Para revisar antes de renderizar: `--cuadros <escena> <t1> <t2>…` (t en tiempo de salida).

## 3. Formatos y zonas seguras

| Formato | Tamaño | Uso |
|---|---|---|
| `vertical` (por defecto) | 1080 × 1920 | TikTok, Reels, Shorts |
| `horizontal` | 1920 × 1080 | YouTube, *La rebelión* caps. 1 |

En vertical, TikTok tapa la parte baja (descripción) y la columna derecha (botones). Los subtítulos ya se colocan al 75 % de la altura. Mantén lo importante en el centro, entre 12 % y 70 % de la altura, y lejos de los ~140 px de la derecha.

## 4. Voces

| Voz Kokoro | Tipo | Uso hasta ahora |
|---|---|---|
| `em_alex` | Hombre | Narrador de *La rebelión* |
| `em_santa` | Hombre | Tito (con efecto `robot`) |
| `ef_dora` | Mujer | Ágora (`agora`), voz de la radio (`radio`) |

Efectos (`motor/audio/voice.py`): `none`, `robot` (anillo + eco metálico), `agora` (coro + eco de sala), `radio` (banda estrecha + estática). Para un efecto nuevo, agrega una función `fx_*` y regístrala en `FX`.

Regla de la casa: **el narrador se fija una vez por historia** y no cambia entre capítulos. Velocidad recomendada 1.0–1.1.

## 5. Piezas reutilizables

- `motor/primitives.py`: `seg/smooth/ease_*` (tiempo), `rrect/poly/line/circle`, `glow` (luz), `tint` (luz de color multiplicada), `darken`, `vignette`, `camera` (zoom/temblor), texto con `font/text_center/wrap`.
- `motor/kit.py`: `title_card`, `glitch_text`, `fit_size`, `fog`, `particles`, `rain`, `candle`.
- `motor/audio/sfx.py`: golpes, ding, puertas, pasos (concreto/metal), choque, chasquido de cable, respiración, latido, estática, radio, *stings* de resultado.
- En `historias/rebelion_maquinas/dibujo/` hay piezas que se pueden copiar a otra historia: personajes con poses (correr, gatear, jadear), tarjetas de opción y de resultado, pantalla de elección.

## 6. Patrones que funcionaron

- **Iluminación por capas:** dibujar la escena normal → `darken` → `tint` (color de la luz) → luces con `glow` en modo SCREEN → redibujar encima lo que emite luz (ojos, pantallas) para que no se tiña. Ver `tito_glow`.
- **Luz que no tiñe un hueco** (puerta de elevador abierta): recorte con regla par-impar (`set_fill_rule(1)`) antes de `tint`.
- **Atmósfera barata y efectiva:** viñeta + partículas + un glow grande en SCREEN.
- **Elección interactiva:** pantalla "¿Qué haces?" con 3 tarjetas y barra de tiempo → video aparte con los 3 finales (malo → regular → bueno/canónico), cada uno con tarjeta de resultado y cierre "Comenta 1, 2 o 3".

## 7. Errores que ya cometimos (no repetir)

- Subtítulos tapando pies y objetos: dejar libre la franja de subtítulos o subir la acción.
- Viñeta pensada para horizontal rompía el vertical: todo lo que dependa del tamaño se calcula con `config.W/H` al momento de dibujar.
- Formas sin `fill()` dejan el trazo "pegado" al siguiente `fill` (Cairo acumula el path).
- Voces de `espeak-ng` suenan muy robóticas: se usa Kokoro; espeak solo queda como dependencia de fonética.
- Narración natural tarda más que el subtítulo: por eso existe el estiramiento de la línea de tiempo; no acelerar la voz por encima de 1.1.
- Renderizar todo sin ver cuadros primero: siempre revisar 2-3 cuadros clave con `--cuadros`.

## 8. Rendimiento

~6-10 cuadros por segundo por proceso en 1080p. Un video de 60 s (1800 cuadros) tarda unos 4-5 min con 2 procesos (`WORKERS`). Las voces se guardan en `out/_tts_cache/` y no se regeneran si el texto no cambia.
