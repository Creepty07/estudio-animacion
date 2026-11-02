# Guion — La Planchada

ESTADO: APROBADO (2026-11-02, Alejandro: "Aprobado") · v1.1, corregida tras `revisor-guion`

Fuente de datos: `docs/estudio/investigacion_planchada.md`. Premisa y finales: `docs/estudio/banco_ideas.md` (idea 2).

## Brief

| Campo | Valor |
|---|---|
| Carpeta | `planchada` |
| Tipo | `interactiva`: **ep1** "La enfermera de las 3:00" (termina en la elección) + **ep2** "Los tres finales" (malo → regular → bueno/canónico) |
| Duración objetivo | ep1 ≈ 60.5 s · ep2 ≈ 90.7 s |
| Formato | Vertical 9:16 (1080×1920), subtítulos siempre |
| Narrador | **Ninguno** (`NARRATION = False`). Diálogos como subtítulos con etiqueta (`Enfermera: «…»`) |
| Tono | Suspenso frío y ambiguo: un fantasma que da miedo pero viene a **cuidar**. Menos golpe que la Llorona, más tensión sostenida. El final canónico es tierno e inquietante a la vez |
| Paleta | Noche azul-verdosa de hospital, fluorescente cian que parpadea; **el uniforme blanco es la única luz limpia** (halo frío). Rojo solo en el timbre y en los sustos. Amanecer ámbar en el final bueno |
| Look (`GRADE`) | Desaturado, frío, grano y viñeta como la Llorona; parpadeo de fluorescente por escena |
| Hospital | **Sin nombre y ficticio** (no se dibuja ni se nombra el Hospital Juárez; nada de ruinas ni sismo) |
| Llamado | ep1: "Comenta 1, 2 o 3" · ep2: "¿Qué final elegiste? Comenta 1, 2 o 3" |

**Verificado / popular / ficción en pantalla**
- Lo único de la leyenda que se dice como tal va en ep2 escena 15 y empieza con "Se cuenta que…" (versión popular: Eulalia, el amor que la engañó, los pacientes descuidados, vuelve a cuidarlos de noche).
- Señales tomadas de la versión popular: viento frío que abre la ventana, pasos que no se oyen, silbido en el oído (tinnitus), uniforme planchado y almidonado, el remate "Aquí no trabaja nadie así".
- Ficción del guion: Rafa, su edad, el hospital, el cuarto, las 3:00, la pastilla, el timbre, el reflejo que no aparece, las luces que se apagan, el expediente y la nota firmada "E.", el olor a almidón, la enfermera de turno (dormida en ep1; de uniforme azul y con su frase en ep2), el diseño de la capa y la cofia.
- "Eulalia" aparece en ep2 esc. 11-14 antes de que la esc. 15 la presente como leyenda: el comentario fijado debe llevar el texto de fuentes de la ficha ("Ficción inspirada en la leyenda… No hay registro de que Eulalia existiera…").
- No se usa: ninguna fecha, el nombre del médico, asfixia ni sobredosis (el final malo solo sugiere, con corte a negro).

## Ep1 — La enfermera de las 3:00

Tiempos de texto relativos al inicio de cada escena.

| # | Escena | Dur. | Texto en pantalla | Visual clave | Sonido |
|---|---|---|---|---|---|
| 1 | `s01_gancho` | 3.0 | 0.2-2.8: **Esta enfermera no trabaja aquí.** | Puerta del cuarto entreabierta; a contraluz, la silueta blanca de una enfermera con cofia, inmóvil. Glitch al entrar el texto | Zumbido de fluorescente desde el cuadro 0 + golpe `susto` en 0.2 con glitch; tinnitus que se apaga |
| 2 | `s02_titulo` | 4.0 | Título con falla: **LA PLANCHADA** · kicker: **Tú eliges el final** | Tarjeta de título (`kit.title_card`), acento cian frío | `riser` corto que corta en seco al final |
| 3 | `s03_hospital` | 5.5 | 0.2-2.6: Rafa, 19 años.<br>2.7-5.2: Su primera noche en el hospital. | Fachada de un hospital sin nombre, de noche, una sola ventana encendida; acercamiento a esa ventana | Viento, grillos lejanos, zumbido, un perro lejano (sin sirenas) |
| 4 | `s04_cuarto` | 6.5 | 0.2-2.8: La fiebre no bajaba.<br>3.0-6.2: En el pasillo, la enfermera de turno dormía. | Rafa en la cama, sudando, suero que gotea, reloj de pared 2:59. Por la puerta: el pasillo, una enfermera de turno dormida en su silla bajo un fluorescente que parpadea | Cama: zumbido + goteo del suero (`gota`) + tic-tac del reloj (`tick` grave, 1 por s) + monitor (pitido suave cada ~1 s, nuevo) |
| 5 | `s05_ventana` | 4.5 | 0.3-1.3: **3:00**<br>1.8-4.2: La ventana se abrió sola. | Reloj marca 3:00 (primer plano). Silencio. La ventana se abre de golpe, la cortina vuela, el vaho de Rafa se ve en el aire | Todo se apaga en 1.2-1.6 (silencio previo) → golpe de ventana + ráfaga de viento en 1.6 con glitch y destello rojo (**susto 1**) |
| 6 | `s06_entra` | 8.0 | 0.5-3.2: No se oyeron sus pasos.<br>3.8-7.6: Su uniforme no tenía ni una arruga. | La enfermera ya está dentro, junto a la cama, sin haber caminado. Uniforme blanco almidonado, cofia, capa oscura; la cara en sombra, solo la barbilla iluminada por su propio halo | **Sin pasos**: al aparecer ella se caen el reloj y el monitor; solo quedan el goteo y un drone grave. Silbido en el oído (tinnitus suave) |
| 7 | `s07_frio` | 5.5 | 0.3-2.3: El cuarto se heló.<br>2.8-5.2: Olía a almidón. | Primer plano: la manga blanca, perfecta; escarcha que crece en el vidrio de la ventana; el vaho de Rafa | Viento frío por la ventana, crujido de hielo (`creak` agudo), drone |
| 8 | `s08_pastilla` | 8.0 | 0.3-3.4: Enfermera: «Tranquilo. Ya estoy aquí.»<br>3.9-7.7: Enfermera: «Esto te va a bajar la fiebre.» | Se inclina sobre Rafa (la cara sigue en sombra, se ve una sonrisa amable). Abre la mano: una pastilla blanca que brilla apenas | `murmullos` muy bajos bajo cada línea (no se entienden); tela almidonada al moverse (`cloth_rip` suave); latido de Rafa entra |
| 9 | `s09_reflejo` | 5.0 | 0.4-2.0: Rafa miró la ventana.<br>2.3-4.8: En el reflejo, ella no estaba. | El vidrio de la ventana refleja a Rafa en la cama y la silla vacía a su lado; corte a ella, que sigue ahí, con la pastilla | Latido que acelera → silencio en 1.9-2.2 → `susto` en 2.2 con glitch (**susto 2**) |
| 10 | `s10_eleccion` | 10.5 | 0.2-1.6: ¿Qué hace Rafa?<br>1.8-8.0 (las 3 a la vez): **1** Fingir que duerme · **2** Tocar el timbre · **3** Preguntarle su nombre<br>8.2-10.2: Comenta 1, 2 o 3. (en la banda de subtítulos, y 1264-1440) | Pantalla de elección **vertical** (nueva): 3 tarjetas apiladas con número grande; al fondo, la enfermera desenfocada con la pastilla. Cada tarjeta entra con su golpe | Drone + latido; 3 golpes graves (uno por tarjeta, 1.8 / 2.6 / 3.4); el latido se corta en seco a negro en 10.3 |

**Total ep1: 60.5 s.**

## Ep2 — Los tres finales

| # | Escena | Dur. | Texto en pantalla | Visual clave | Sonido |
|---|---|---|---|---|---|
| 1 | `s01_gancho` | 4.0 | 0.2-1.8: **1, 2 o 3.**<br>2.0-3.8: Esto le pasó a Rafa. | La mano de la enfermera con la pastilla, en primer plano; glitch | `susto` en 0.2 + zumbido de fluorescente |
| 2 | `s02_f1_titulo` | 2.5 | **1 · Fingir que duerme** (final malo) | Tarjeta de final (nueva, vertical) | Golpe grave sobre cama de zumbido de fluorescente + drone |
| 3 | `s03_f1_ojos` | 6.0 | 0.2-2.6: Rafa cerró los ojos.<br>2.8-5.8: Ella dejó la pastilla y se fue. | Rafa con los ojos apretados; ella espera, deja la pastilla en el buró y desaparece (sin caminar: el halo se apaga) | Goteo, drone; sin pasos; tinnitus que se va |
| 4 | `s04_f1_fiebre` | 6.0 | 0.2-2.8: La fiebre subió toda la noche.<br>3.0-5.8: Nadie más entró. | El reloj gira de 3:00 a 5:40 (manecillas rápidas); Rafa empapado; la pastilla en el buró, fuera de su alcance | Tic-tac acelerado, latido que sube, monitor que pita más rápido |
| 5 | `s05_f1_amanecer` | 7.0 | 0.3-2.6: Al amanecer, la pastilla seguía ahí.<br>3.0-6.7: Ella era la única que venía a este cuarto. | Luz gris de madrugada; la pastilla en el buró; la cama en sombra. Corte a negro antes de ver a Rafa | El monitor pita rápido → se queda en un tono largo **muy bajo** que se corta a negro en 6.7 (sugerido, no mostrado) |
| 6 | `s06_f2_titulo` | 2.5 | **2 · Tocar el timbre** (final regular) | Tarjeta de final | Golpe grave sobre cama de zumbido + drone |
| 7 | `s07_f2_timbre` | 6.0 | 0.2-2.4: Rafa tocó el timbre.<br>2.6-5.8: Ella lo miró… y bajó la mano. | Primer plano del botón rojo; la luz roja se prende sobre la puerta. Ella cierra la mano con la pastilla, triste | Zumbador del timbre (nuevo: buzz eléctrico) en el pasillo, 2 veces; el fluorescente parpadea |
| 8 | `s08_f2_turno` | 7.0 | 0.2-2.2: Entró la enfermera de turno.<br>2.4-4.7: Enfermera de turno: «¿De blanco almidonado?<br>4.8-6.8: «Aquí ya nadie viste así.» | Se prende la luz del cuarto; la enfermera de turno (uniforme moderno, azul) en la puerta; junto a la cama no hay nadie; la cortina se mueve | Pasos normales (`step_concrete`) que contrastan con el silencio de la otra; viento leve |
| 9 | `s09_f2_pasillo` | 6.0 | 0.3-3.6: Las luces del pasillo se apagaron, una por una.<br>3.9-5.8: La fiebre seguía ahí. | Desde la cama se ve el pasillo: los fluorescentes se apagan uno a uno hacia el fondo; al fondo, un instante, una figura blanca de espaldas | Un clic eléctrico por cada luz que se apaga (`tick` + `radio_click`), lamento lejano muy bajo (`wail`, lejano) |
| 10 | `s10_f3_titulo` | 2.5 | **3 · Preguntarle su nombre** (final bueno) | Tarjeta de final | Golpe grave + campana suave (`bell`) sobre cama de zumbido + drone |
| 11 | `s11_f3_nombre` | 6.0 | 0.2-2.4: Rafa: «¿Cómo se llama?»<br>2.6-3.4: (silencio)<br>3.6-5.8: Enfermera: «Eulalia.» | Ella se detiene. Por primera vez se le ve la cara: joven, cansada, amable. El fluorescente deja de parpadear | Todo baja en 2.4-3.6 menos el goteo del suero y un drone muy bajo; en 3.6 una nota grave cálida (`bell` bajo) bajo el nombre |
| 12 | `s12_f3_pastilla` | 5.5 | 0.2-2.4: Rafa se tomó la pastilla.<br>2.7-5.3: Su mano estaba helada. | Rafa traga; ella le pone la mano en la frente; él se duerme. Escarcha en la ventana que se deshace | `cold_touch` en 2.7; latido que se calma; goteo |
| 13 | `s13_f3_amanecer` | 7.5 | 0.3-3.4: Rafa: «Gracias por mandar a Eulalia.»<br>3.8-7.2: Enfermera de turno: «Aquí no trabaja nadie así.» | Amanecer ámbar por la ventana; Rafa sentado, sano. La enfermera de turno, con el expediente en la mano, se queda quieta | Pájaros del amanecer (`dawn_birds`), zumbido apagado; silencio corto antes de la segunda línea |
| 14 | `s14_f3_nota` | 6.5 | 0.3-3.0: En el expediente había una nota.<br>3.2-6.2: «Fiebre bajó. 3:00 a. m. — E.» | Primer plano del expediente: la nota con letra antigua, tinta sepia, entre anotaciones modernas. Glitch en la "E." | Papel; silencio previo en 3.0 → glitch suave + tinnitus en 3.2 (**susto 3**, leve) |
| 15 | `s15_f3_leyenda` | 9.5 | 0.3-3.3: Se cuenta que Eulalia descuidó a sus pacientes<br>3.4-5.6: por un amor que la engañó.<br>5.9-9.2: Desde entonces, vuelve de noche a cuidarlos. | Pasillo largo de hospital, de noche: la silueta blanca se aleja entre las puertas, cada puerta se ilumina un instante al pasar ella | Drone cálido-frío, `murmullos` muy bajos, viento; sin pasos |
| 16 | `s16_cierre` | 6.2 | 0.2-2.8: ¿Tú le habrías preguntado su nombre?<br>3.0-6.0: ¿Qué final elegiste? Comenta 1, 2 o 3. | Tarjeta de cierre: cofia blanca sobre una silla vacía, en la penumbra; logo de la vela | El fluorescente parpadea y se apaga en 6.0; tinnitus final |

**Total ep2: 90.7 s.**

## Notas para Animación

**Dibujos nuevos** (en `historias/planchada/dibujo/`; nada de esto existe aún):
- Rafa: en la cama (acostado, sudando, ojos cerrados/apretados, mirando a un lado, tragando), sentado sano al amanecer.
- La enfermera (Eulalia): de pie a contraluz (silueta), inclinada, de espaldas alejándose; uniforme blanco con halo frío, cofia, capa oscura; cara en sombra en todo el ep1 y visible solo en ep2 esc. 11. Mano abierta con la pastilla.
- Enfermera de turno: dormida en silla (ep1) y de pie en la puerta con expediente (ep2), uniforme moderno azul para que no se confunda con la de blanco.
- Escenarios: fachada de hospital sin nombre; cuarto (cama, suero, buró, reloj de pared, ventana con cortina, puerta al pasillo, timbre); pasillo largo con fluorescentes y puertas.
- Primeros planos: reloj 2:59/3:00, ventana con escarcha y reflejo, botón rojo del timbre, expediente con la nota "E.".
- **Pantalla de elección vertical** y **tarjetas de final** verticales (pendiente de §8; sirve para todas las interactivas: mejor en `motor/`).
- Tarjeta de cierre (cofia en la silla).

**Se reutiliza:** `kit.title_card` (título con falla), `kit.fog`/`particles` (vaho y escarcha), `grade.glitch` y `grade.rojo`, `GRADE` de la Llorona como base, capas en caché para el cuarto y el pasillo.

**Sustos** (glitch + golpe, en `SUSTOS`): ep1 esc. 1 (0.2 s), esc. 5 (1.6 s, con destello rojo), esc. 9 (2.2 s), esc. 10 (corte a negro 10.3 s). ep2 esc. 1 (0.2 s), esc. 5 (corte a negro 6.7 s), esc. 14 (3.2 s, leve).

**Sonido nuevo** (en `motor/audio/sfx.py`, sintetizado): pitido de monitor, zumbador de timbre, zumbido de fluorescente (variante de `lamp_hum` en `ambient.py`, con parpadeo). El goteo es `gota` de `motor/audio/agua.py`. **La regla de la enfermera: nunca suenan sus pasos**; cuando aparece, el reloj y el monitor se caen y queda el goteo.

**Zona segura:** reloj, pastilla, timbre, nota, texto del gancho, tarjetas y cierre entre y ≈ 230 y 1200; la columna derecha libre. En la elección, pregunta + 3 tarjetas caben justas en 970 px: probar en cuadros clave. El llamado va en la banda de subtítulos (1264-1440), nunca entre 1200 y 1264. Los diálogos largos ya van partidos para no pasar de 2 líneas.

**Duración estimada:** ep1 ≈ 60.5 s · ep2 ≈ 90.7 s.
