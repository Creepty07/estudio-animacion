# Guion — Las reglas del Silbón

ESTADO: APROBADO (Alejandro, 2026-11-02: "Excelente. Me gusta", con dos reglas de viralidad: gancho inicial y "lo que oyes, lo ves")

| Dato | Valor |
|---|---|
| Tipo / formato | `unico`, vertical 9:16, ≈ 90-99 s (depende de la voz real) |
| Estilo | Animación tipo "reglas" (referencia: TikTok que Alejandro adjuntó): cabezas redondas de ojos enormes, contorno grueso, subtítulo blanco con contorno negro y palabra clave amarilla que aparece palabra a palabra, caja HUD roja, tarjetas "REGLA Nº X" |
| Narrador | **ElevenLabs**, voz `DdKbXdRlBmj7Ty7N0FVr`, modelo `eleven_v4`, efecto `tetrico` (excepción a "sin narrador por defecto": lo pidió Alejandro). Un narrador fijo |
| Personajes (sin voz, solo subtítulo con etiqueta) | Llanero, Ramiro |
| Gancho (0-2 s) | Silbido de siete notas visible (♪ que suben) + silueta diminuta en el horizonte → corte seco al ojo gigante en la rendija de la puerta con glitch (3.0 s) |
| Regla "lo que oyes, lo ves" | Cada sonido tiene su imagen: notas del silbido, ondas de ladrido, "+4 HORAS" con reloj, corcho, UNO/DOS/TRES al caer cada hueso, "FALTAN 3→2→1" al ritmo de los huesos |
| Cierre | Dilema CONTAR • CALLAR, "Comenta 1 para contar, o 2 para callar", apagón y silbido que vuelve al gancho (bucle) |

## Escenas y texto en pantalla (lo que va en `SUBS`)

| # | Escena | Texto (amarillo = *palabra clave*) |
|---|---|---|
| 1 | s01_gancho | Si oyes este *silbido*… / alguien en tu casa *no amanece*. |
| 2 | s02_llegas | Imagina que la *noche* te alcanza en los llanos. / Un viejo llanero te jala del brazo. / Llanero: «¡Entra, muchacho! ¡Ya!» |
| 3 | s03_letrero | Adentro, un letrero con *cuatro reglas*. |
| 4 | s04_regla1 | Regla uno: si el silbido suena *cerca*, está lejos. / Si suena *lejos*… ya está aquí. |
| 5 | s05_regla2 | Regla dos: nadie bebe *aguardiente* de noche. |
| 6 | s06_regla3 | Regla tres: los *perros* nunca se callan. |
| 7 | s07_regla4 | Regla cuatro: si caen *huesos* junto a la puerta… / cuéntalos en *voz alta*. |
| 8 | s08_tiempo | Cuatro horas después, Ramiro *destapa* su botella. / Los perros ladran. Alguien los manda a *callar*. |
| 9 | s09_silencio | *Silencio*. / El silbido suena *cerca*. Todos sonríen. / Pero ahora suena… *lejísimos*. |
| 10 | s10_puerta | Algo se sienta junto a la *puerta*. / Un saco cae… y empieza a *contar huesos*. |
| 11 | s11_tu | Solo tú estás *despierto*. / Si cuentas en voz alta, sabrá que lo *oyes*. / Si callas… alguien no *amanece*. |
| 12 | s12_cierre | ¿Cuentas los huesos… o te *callas*? / Comenta *1* para contar, o *2* para callar. |

## Verificado vs. ficción

**Verificado (leyenda popular llanera de Venezuela y Colombia):** el Silbón es un espectro alto con sombrero que carga un saco de huesos y se anuncia con un silbido; el silbido "cerca / lejos" engaña (si suena cerca está lejos y al revés); aparece de noche en los llanos, asusta a los bebedores y hace ladrar a los perros; cuenta los huesos de sus víctimas. Fuentes consultadas en la sesión: culturagenial.com/es/el-silbon y el artículo de la leyenda en teleamazonas.com.

**Ficción del guion (no es tradición):** el letrero de cuatro reglas, el hato "La Esperanza", Ramiro, el llanero que te recibe, el "+4 horas", "cuéntalos en voz alta" como regla (en la leyenda se cuentan los huesos pero la regla es invento) y el dilema final.

## Pendientes de esta historia

- La voz real de ElevenLabs está generada (23 tomas, flujo `kw6IURnEQwHjp30mVq60`) pero **no se pudo bajar a la sandbox** (dominio bloqueado). Hasta entonces `audio/narrador/` tiene tomas provisionales (silencio con tono) y el video salió como PRUEBA. Cuando lleguen los MP3: copiarlos a `historias/silbon/audio/narrador/<clave>.mp3`, `python -m historias.silbon.narracion`, `producir.py silbon ep1`, normalizar a -13.5 LUFS y recomprimir `-crf 26`.
- Revisar de oído: sincronía del silbido con las notas, volumen de la voz sobre el fondo y ritmo (la duración final depende de la voz).
