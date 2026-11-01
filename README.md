# Estudio de animación

Motor para producir videos animados y narrados (TikTok y otras redes) con código: escenas dibujadas en Python, voces neuronales locales, efectos de sonido sintetizados y render con ffmpeg. Todo es gratis y corre sin servicios externos (solo descarga el modelo de voz una vez).

Sirve para tres tipos de historia:

| Tipo | Qué es | Ejemplo |
|---|---|---|
| `unico` | Un solo video completo | Leyenda de La Llorona |
| `lineal` | Capítulos en orden | Serie narrada por episodios |
| `interactiva` | Capítulos que terminan en una elección + video de finales | *La rebelión de las máquinas* |

## Arranque rápido

```bash
./setup.sh                                          # dependencias + modelo de voz
python producir.py rebelion_maquinas ep1            # produce un episodio completo
python producir.py --nueva llorona --formato vertical   # crea una historia nueva desde la plantilla
```

El video final queda en `out/<historia>/`.

## Comandos

| Comando | Para qué |
|---|---|
| `python producir.py <historia> <ep>` | Todo: voces → sonido → escenas → video final |
| `... --voces` | Solo genera voces y muestra cuánto se alarga cada escena |
| `... --sonido` | Voces + banda sonora |
| `... --escenas ep1.s2 ep1.s3` | Re-renderiza solo esas escenas y vuelve a unir |
| `... --cuadros ep1.s2 1.5 4.0` | Guarda cuadros PNG para revisar antes de renderizar |

## Estructura

```
motor/            lo reutilizable (no sabe nada de ninguna historia)
  config.py       valores globales + carga la historia activa
  primitives.py   formas, luz, texto, easing, cámara
  kit.py          piezas genéricas: título con falla, niebla, partículas, lluvia, velas
  subtitles.py    subtítulos (se adaptan a vertical/horizontal)
  timeline.py     alarga cada tramo de escena para que quepa la voz
  render.py       escena -> MP4 (y cuadros sueltos)
  build.py        une escenas + banda sonora
  audio/          síntesis, efectos, voz (Kokoro), narración, mezcla final
historias/
  _plantilla/     punto de partida de cualquier historia nueva
  rebelion_maquinas/
    historia.py   formato, episodios, voces, pronunciación, paleta
    dibujo/       personajes, escenarios y tarjetas propias
    escenas/epN/  una escena por archivo
    sonido/       mezcla de cada episodio
docs/GUIA_MOTOR.md  cómo funciona por dentro y cómo escribir escenas
```

Detalles en [docs/GUIA_MOTOR.md](docs/GUIA_MOTOR.md).
