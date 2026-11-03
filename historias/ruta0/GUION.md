# Guion — Ruta 0 (título por decidir)

ESTADO: APROBADO (2026-11-02, Alejandro: "Aprobado") · v1.1, corregida tras `revisor-guion`. Se aprobaron las dos versiones (A principal, B alternativa) y los 6 elementos de puente del brief.

**Título:** sin confirmar. Recomendado: **"El camión sin número"**. En las tablas va como [TÍTULO]; Animación no hace la tarjeta de título ni la portada hasta que Alejandro lo confirme.

Fuente: `docs/estudio/investigacion_ruta0.md` (ficción original; no hay datos reales que verificar).

## Brief

| Campo | Valor |
|---|---|
| Carpeta | `ruta0` |
| Tipo | `lineal`, 3 episodios. Cada uno abre con un repaso de una línea para entenderse solo y cierra con un gancho al siguiente |
| Episodios | **Parte 1 · El último camión**: pierde el camión, sube al "0", nadie respira, «Tú todavía no te bajas aquí». **Parte 2 · Las paradas**: cada pasajero baja donde murió, su nombre en la ruta, el boleto con fecha de mañana. **Parte 3 · La última parada**: el giro, se baja antes, despierta, no sube al coche de su amigo. ¿O no? |
| Duración | **Versión A:** P1 56.5 s · P2 58.5 s · P3 64.5 s. **Versión B:** P1 ≈ 69.5 s · P2 ≈ 66.0 s · P3 ≈ 83.0 s |
| Versiones | **A, sin narrador (principal):** texto en pantalla, diálogos con etiqueta y sonido. **B, con narrador (alternativa):** narrador en tercera persona, uno solo y fijo en los 3 episodios. Los diálogos siguen como subtítulo con etiqueta, sin voz, para que la única diferencia sea el narrador |
| Tono | Terror quieto, de "algo no cuadra". Pocos golpes y mucha quietud; el miedo está en lo que no se mueve |
| Paleta | Noche de lluvia azul-negra. Dentro del camión, luz amarilla enferma que parpadea. **El letrero "0" en ámbar es la única luz cálida.** Rojo solo en el timbre de parada y en los sustos |
| Look (`GRADE`) | Frío, desaturado, grano, viñeta; parpadeo de la luz del camión |
| Lugar | Una ciudad del Bajío sin nombre. Paradas inventadas. Camión diseñado desde cero: ninguna empresa, ruta, color ni logotipo real |
| Llamado | P1 y P2: «Comenta "sigue" para la parte 2 / la parte final» · P3: «¿Iván despertó de verdad? Comenta sí o no» |

### Lo que viene de la ficha y lo que agregué (confírmalo)

**De la ficha, tal cual:**
- Iván pierde el último camión y pasa uno con un "0" en el letrero.
- Los pasajeros no se mueven ni respiran, y el camión para en lugares que Iván no conoce.
- «Tú todavía no te bajas aquí» es el cierre de la parte 1.
- Cada pasajero baja donde murió (una curva, un puente: Curva del Ahorcado y Puente Viejo).
- Iván ve su propia parada en la ruta, y la fecha del boleto es de mañana (cierre de la parte 2).
- Iván se baja antes y despierta en la parada real, a tiempo para no subirse al coche de su amigo. ¿O no?
- El giro: el camión no se lleva a los muertos, avisa a los que van a morir.
- La regla «no mires atrás» y los pasajeros arreglados y callados (folclore libre de Toluca).
- El timbre de parada, los frenos de aire, la lluvia y el silencio total cuando nota que nadie respira.

**Elementos de puente que agregué para que se entienda sin narrador; ninguno cambia lo que pasa:**
1. **Cómo ve su parada:** en el tablero de la ruta, arriba del chofer, la última parada dice **IVÁN**.
2. **Cómo sabe que bajan donde murieron:** en la curva hay una cruz con flores y la foto del mismo señor. En el puente, el barandal está roto. Las muertes no se muestran.
3. **Quién dice el giro:** lo dice la pasajera en la parte 3. Antes, en la parte 2, Iván le pregunta «¿Por qué yo?», ella no contesta y señala el boleto.
4. **Quién dice la regla:** el chofer, al abrir la puerta en la parte 3: «Al bajar, no mires atrás». Iván no voltea.
5. **El amigo** se llama **Beto** y aparece solo en un mensaje del celular («¿Te llevo? Ya voy en el coche»). Iván contesta que no.
6. **El "¿O no?":** el boleto sigue en su bolsillo y, en el vidrio de una tienda, su reflejo sigue sentado dentro del camión. Esto pone en duda si de verdad despertó, como pide la ficha, sin usar nada de *Destino final*.

**Título (decides tú):** la ficha avisa que ya existe *The Final Stop on Route 0* (audiolibro). Recomiendo **"El camión sin número"**: es distinto, describe al camión y deja el "0" en el letrero como imagen. En las tablas va como [TÍTULO].

---

## Versión A — Sin narrador (principal)

Tiempos de texto relativos al inicio de cada escena.

### Parte 1 · El último camión

| # | Escena | Dur. | Texto en pantalla | Visual clave | Sonido |
|---|---|---|---|---|---|
| 1 | `p1_s01_gancho` | 3.0 | 0.2-2.8: **No tenía número. Solo un 0.** | En la lluvia se acercan dos faros; arriba, el letrero con un "0" ámbar. Glitch al entrar el texto | Lluvia y motor viejo desde el cuadro 0; frenos de aire (nuevo) + `susto` en 0.2 |
| 2 | `p1_s02_titulo` | 4.0 | [TÍTULO] · kicker: **Parte 1 de 3** | Tarjeta de título con falla (`kit.title_card`), acento ámbar | `riser` que corta en seco; lluvia de fondo |
| 3 | `p1_s03_parada` | 6.0 | 0.3-2.6: Iván perdió el último camión.<br>3.0-5.6: Ya no pasaba ninguno. | Calle de noche con lluvia (base: calle de El río de los perros sin papel picado), parada con techito. Iván con sudadera y mochila. A lo lejos se van las luces traseras del último camión | Lluvia en lámina, motor que se aleja, charcos, perro lejano |
| 4 | `p1_s04_llega` | 6.0 | 0.3-2.0: Entonces llegó otro.<br>2.5-4.6: Iván subió. | De la neblina sale el camión: viejo, sin número, con el letrero "0". Las puertas se abren; el chofer está a contraluz y no se le ve la cara | Motor grave que se acerca, frenos de aire, puertas neumáticas (nuevo), lluvia |
| 5 | `p1_s05_dentro` | 7.0 | 0.3-2.6: El chofer le dio un boleto.<br>3.0-5.6: Nadie levantó la vista. | Pasillo del camión: filas de pasajeros muy arreglados (traje, vestido de fiesta, ropa de domingo), quietos. Luz amarilla que parpadea. La mano del chofer le da un boleto de papel sin voltear. Iván se sienta | Motor por dentro, lluvia en el vidrio, papel, la luz que zumba |
| 6 | `p1_s06_quietos` | 7.5 | 0.3-2.0: Nadie se movía.<br>4.0-5.8: **Nadie respiraba.** | Primer plano de los vidrios: el de Iván se empaña con su aliento y el del pasajero de al lado sigue limpio. Ojos que no parpadean | En 3.0-3.8 se va todo (motor, lluvia): **silencio total**. En 4.0 solo quedan la respiración de Iván (`breath`) y su latido, con un glitch suave |
| 7 | `p1_s07_paradas` | 8.0 | 0.3-2.6: No reconocía ninguna parada.<br>3.5-5.6: Iván tocó el timbre. | Por la ventana pasan paradas con letreros que no se leen y calles que no son de su ciudad. Primer plano: el dedo en el botón y el foco rojo de "parada" | Regresa el motor, más grave; timbre de parada (`ding` grave); frenos |
| 8 | `p1_s08_pasajera` | 9.0 | 0.3-2.0: Iván se levantó.<br>3.2-6.4: Pasajera: «Tú todavía no te bajas aquí.» | Se abre la puerta a una parada negra. Iván se levanta y una mano pálida lo agarra de la muñeca: la pasajera, la primera que se mueve, gira la cabeza despacio. Las puertas se cierran | Silencio en 2.0-3.0 → `susto` + glitch y destello rojo en 3.0 (**susto principal**) → `cold_touch`; puertas en 7.0 |
| 9 | `p1_s09_cierre` | 6.0 | 0.3-2.4: ¿Dónde se baja Iván?<br>2.8-5.8: Comenta «sigue» para la parte 2. | El camión se pierde en la neblina; solo queda el "0" ámbar, que se apaga | Motor que se aleja, lluvia, tinnitus; el "0" se apaga con un clic |

**Total parte 1 (A): 56.5 s**

### Parte 2 · Las paradas

| # | Escena | Dur. | Texto en pantalla | Visual clave | Sonido |
|---|---|---|---|---|---|
| 1 | `p2_s01_gancho` | 3.5 | 0.2-3.2: **Cada uno se baja donde murió.** | Un pie de pasajero baja del camión a la orilla de la carretera; al lado, una cruz con flores | Frenos de aire + `susto` en 0.2 |
| 2 | `p2_s02_titulo` | 4.0 | [TÍTULO] · kicker: **Parte 2 de 3** | Tarjeta de título | `riser` + motor de fondo |
| 3 | `p2_s03_repaso` | 6.0 | 0.3-2.8: Iván subió al camión sin número.<br>3.0-5.8: Nadie respira. Una pasajera no lo dejó bajar. | Repaso rápido: el letrero "0", el pasillo quieto, la mano de la pasajera en su muñeca | Motor por dentro, lluvia |
| 4 | `p2_s04_curva` | 9.0 | 0.3-2.9: Un señor se bajó en la curva.<br>3.6-6.4: En la cruz estaba su foto. | Letrero de parada: **CURVA DEL AHORCADO**. Un señor con ropa de trabajo baja. Afuera: barandal doblado, cruz con flores de plástico y una veladora; la foto de la cruz es su cara. Se queda parado ahí mientras el camión arranca | Frenos, puertas, viento, grillos. A lo lejos, un rechinido de llantas que se corta (**sugerido, no mostrado**); glitch en 3.6 |
| 5 | `p2_s05_puente` | 8.0 | 0.3-2.9: En el Puente Viejo bajó una muchacha.<br>3.5-5.6: Su asiento quedó vacío. | Letrero: **PUENTE VIEJO**. Una muchacha con vestido de fiesta baja al puente; el barandal está roto y abajo corre el río. Primer plano del asiento vacío | Frenos, agua de río (`water`), viento; el motor arranca |
| 6 | `p2_s06_ruta` | 8.0 | 0.3-2.6: Arriba del chofer estaba la ruta.<br>4.6-7.6: **La última parada tenía su nombre.** | Tablero luminoso de la ruta: CURVA DEL AHORCADO (apagada) · PUENTE VIEJO (apagada) · … · la última se prende: **IVÁN** | Zumbido del tablero; silencio en 3.8-4.6 → `susto` + glitch en 4.6 |
| 7 | `p2_s07_pasajera` | 7.0 | 0.3-2.4: Iván: «¿Por qué yo?»<br>3.0-5.6: Ella señaló su boleto. | Iván voltea hacia la pasajera. Ella no contesta y baja la mirada hacia la mano de él, que tiene el boleto | Motor, latido de Iván que acelera |
| 8 | `p2_s08_boleto` | 7.0 | 0.3-2.9: En el boleto había una fecha.<br>3.4-6.6: **Era la de mañana.** | Primer plano del boleto: "RUTA 0 · VÁLIDO: [fecha de mañana]". Corte al celular de Iván: "[fecha de hoy]". Glitch en la fecha del boleto | Silencio en 2.9-3.4 → `susto` en 3.4 (**susto principal**), tinnitus |
| 9 | `p2_s09_cierre` | 6.0 | 0.3-2.6: ¿Se puede bajar antes?<br>2.9-5.8: Comenta «sigue» para la parte final. | El tablero con IVÁN encendido; el camión entra a un túnel de neblina | Motor que se aleja, lluvia, timbre de parada lejano |

**Total parte 2 (A): 58.5 s**

### Parte 3 · La última parada

| # | Escena | Dur. | Texto en pantalla | Visual clave | Sonido |
|---|---|---|---|---|---|
| 1 | `p3_s01_gancho` | 3.0 | 0.2-2.8: **Iván tenía que bajarse antes.** | El dedo de Iván sobre el botón de parada; el tablero con IVÁN detrás, desenfocado | `susto` en 0.2 + motor |
| 2 | `p3_s02_titulo` | 4.0 | [TÍTULO] · kicker: **Parte 3 de 3** | Tarjeta de título | `riser` + motor |
| 3 | `p3_s03_repaso` | 6.5 | 0.3-3.0: Cada pasajero se bajó donde murió.<br>3.4-6.2: Su boleto tenía la fecha de mañana. | Repaso: la cruz de la curva, el puente, la pasajera que le agarra la muñeca, el tablero con IVÁN, el boleto | Motor, lluvia, latido |
| 4 | `p3_s04_giro` | 8.0 | 0.3-3.8: Pasajera: «Este camión no se lleva a los muertos.»<br>4.3-7.6: Pasajera: «Avisa a los que van a morir.» | La pasajera, de frente por primera vez, con una cara pálida y triste, sin respirar. Sus ojos en sombra | Todo baja: queda el motor muy grave y un drone; tinnitus suave |
| 5 | `p3_s05_timbre` | 7.0 | 0.3-2.4: Iván tocó el timbre.<br>3.0-5.6: Chofer: «Al bajar, no mires atrás.» | Se prende el foco rojo de parada; el camión frena en una parada a oscuras que no es la suya. Las puertas se abren. El chofer habla sin voltear (se le ve solo la nuca) | Timbre de parada, frenos de aire, puertas, lluvia afuera |
| 6 | `p3_s06_bajar` | 7.5 | 0.5-2.4: Iván bajó.<br>3.0-5.0: No miró atrás. | Iván camina hacia la cámara bajo la lluvia. Detrás de él, desenfocados, todos los pasajeros pegados a las ventanas **mirándolo** (él no los ve). Las puertas se cierran | Pasos en charcos, puertas, silencio en 5.0-5.6 → el motor se va de golpe y corte a blanco en 7.2 (**golpe**) |
| 7 | `p3_s07_despierta` | 8.0 | 0.3-2.8: Iván despertó en su parada.<br>3.2-7.4: Beto: «¿Te llevo? Ya voy en el coche.» | Iván abre los ojos en la banca de la misma parada de la parte 1. Ya no llueve. El celular vibra y muestra el mensaje de Beto (pantalla dentro de la zona segura) | Gota de techito, grillos, ciudad lejana; vibración del celular |
| 8 | `p3_s08_no` | 7.0 | 0.3-3.4: Iván: «No, gracias. Me voy a pie.»<br>4.0-6.6: Esa noche, no se subió. | Iván escribe la respuesta y se va caminando. Unos faros de coche pasan por la calle de atrás, sin detalle | Teclas, pasos, un coche que pasa y se aleja normal; la cama se calma |
| 9 | `p3_s09_o_no` | 7.5 | 0.3-2.8: En su bolsillo seguía el boleto.<br>4.6-7.3: **¿Se salvó? ¿O sigue en el camión?** | Iván saca el boleto. Pasa frente al vidrio de una tienda cerrada y **su reflejo sigue sentado dentro del camión**, entre los pasajeros. Él no lo ve | Silencio en 4.0-4.5 → timbre de parada + motor del camión que solo suena "en el reflejo" + `susto` y glitch en 4.5 (**susto final**) |
| 10 | `p3_s10_cierre` | 6.0 | 0.3-2.7: ¿Iván despertó de verdad?<br>3.0-5.8: Comenta: sí o no. | El "0" ámbar en la neblina, que parpadea y se apaga | Lluvia que vuelve, motor lejano, tinnitus final |

**Total parte 3 (A): 64.5 s**

---

## Versión B — Con narrador (alternativa)

- **Narrador:** uno solo, en tercera persona, sombrío y calmado, fijo en los 3 episodios. La voz está por definir: hoy ninguna convence, y sin la aprobación de Alejandro no se produce esta versión.
- **Visuales, escenas y sonido:** los mismos de la versión A. La cama de sonido baja (ducking) mientras habla el narrador.
- **Diálogos:** son los mismos y van como subtítulo con etiqueta, sin voz.
- **Golpes y glitch:** caen en los silencios del narrador, con ≥ 0.3 s de aire después de cada frase y antes de la siguiente; en los ganchos el golpe va en 0.1 y la voz entra en 0.6.
- **Ritmo:** la narración se planea a ≤ 2.6 palabras por segundo. Los subtítulos muestran la narración.
- **Cálculo de tiempos:** las ventanas se calcularon así. Con la voz real se recalculan con `--voces`, que puede alargar la escena hasta `MAX_STRETCH`.
- **Llamado:** el narrador dice el llamado y el texto en pantalla lo repite.

### Parte 1 · El último camión (B)

| # | Escena | Dur. | Narración (voz + subtítulo) | Texto en pantalla sin voz | Notas (visual y sonido = A) |
|---|---|---|---|---|---|
| 1 | `p1_s01_gancho` | 4.0 | 0.6-3.3: Esa noche pasó un camión sin número. | Letrero "0" | `susto` en 0.1, antes de la voz |
| 2 | `p1_s02_titulo` | 4.0 | (sin narración) | [TÍTULO] · Parte 1 de 3 | — |
| 3 | `p1_s03_parada` | 7.5 | 0.3-3.4: Iván perdió el último camión de la noche.<br>3.7-6.8: Bajo la lluvia esperó, y no pasó ninguno. | — | — |
| 4 | `p1_s04_llega` | 8.5 | 0.3-3.0: Hasta que, entre la neblina, apareció otro.<br>3.3-6.4: No traía número. Su letrero solo decía: cero.<br>6.7-7.9: Iván subió. | — | — |
| 5 | `p1_s05_dentro` | 10.0 | 0.3-4.2: El chofer le dio un boleto sin voltear a verlo.<br>4.5-7.6: Los pasajeros iban arreglados, como para una fiesta.<br>7.9-9.5: Ninguno levantó la vista. | — | — |
| 6 | `p1_s06_quietos` | 9.5 | 0.3-1.5: Nadie se movía.<br>1.8-6.5: El aliento de Iván empañaba el vidrio; el de los demás, no.<br>7.7-8.9: Nadie respiraba. | — | silencio total en 6.7-7.6 |
| 7 | `p1_s07_paradas` | 9.0 | 0.3-3.0: Pasaban paradas que Iván nunca había visto.<br>3.3-6.0: Calles que no eran de su ciudad.<br>6.3-8.3: Tocó el timbre para bajarse. | — | — |
| 8 | `p1_s08_pasajera` | 10.0 | 0.3-3.0: El camión se detuvo. Iván se levantó.<br>3.3-6.0: Y por primera vez, alguien se movió. | 6.8-9.5: Pasajera: «Tú todavía no te bajas aquí.» | `susto` en 6.3 |
| 9 | `p1_s09_cierre` | 7.0 | 0.3-1.9: ¿Dónde se baja Iván?<br>2.2-6.1: Comenta «sigue», y te lo cuento en la parte dos. | Comenta «sigue» para la parte 2. | — |

**Total parte 1 (B): ≈ 69.5 s**

### Parte 2 · Las paradas (B)

| # | Escena | Dur. | Narración (voz + subtítulo) | Texto en pantalla sin voz | Notas (visual y sonido = A) |
|---|---|---|---|---|---|
| 1 | `p2_s01_gancho` | 5.0 | 0.6-4.1: En este camión, cada pasajero se baja donde murió. | — | `susto` en 0.1 |
| 2 | `p2_s02_titulo` | 4.0 | (sin narración) | [TÍTULO] · Parte 2 de 3 | — |
| 3 | `p2_s03_repaso` | 9.5 | 0.3-3.4: Iván subió al último camión: uno sin número.<br>3.7-5.7: Ninguno de sus pasajeros respira.<br>6.0-8.7: Y una pasajera no lo dejó bajar. | — | — |
| 4 | `p2_s04_curva` | 11.5 | 0.3-3.8: En la Curva del Ahorcado, un señor se bajó.<br>4.1-7.6: Junto a la curva había una cruz con flores,<br>8.4-10.8: y en la cruz, su foto. | Letrero CURVA DEL AHORCADO | `susto` en 7.9 |
| 5 | `p2_s05_puente` | 8.5 | 0.3-4.2: En el Puente Viejo bajó una muchacha vestida de fiesta.<br>4.5-6.1: El barandal estaba roto.<br>6.4-8.0: Su asiento quedó vacío. | Letrero PUENTE VIEJO | — |
| 6 | `p2_s06_ruta` | 9.5 | 0.3-2.7: Arriba del chofer brillaba la ruta.<br>3.0-5.4: Las paradas que pasaban se apagaban.<br>6.3-8.7: La última tenía un nombre: Iván. | Tablero con IVÁN | `susto` en 5.7 |
| 7 | `p2_s07_pasajera` | 5.5 | 2.2-4.9: Ella no contestó. Solo señaló su boleto. | 0.3-1.9: Iván: «¿Por qué yo?» | — |
| 8 | `p2_s08_boleto` | 6.0 | 0.3-2.7: En el boleto había una fecha.<br>3.6-5.2: Era la de mañana. | Fechas del boleto y del celular | `susto` en 3.0 |
| 9 | `p2_s09_cierre` | 6.5 | 0.3-3.0: ¿Se puede bajar antes de su parada?<br>3.3-5.7: Comenta «sigue» para la parte final. | Comenta «sigue» para la parte final. | — |

**Total parte 2 (B): ≈ 66.0 s**

### Parte 3 · La última parada (B)

| # | Escena | Dur. | Narración (voz + subtítulo) | Texto en pantalla sin voz | Notas (visual y sonido = A) |
|---|---|---|---|---|---|
| 1 | `p3_s01_gancho` | 6.0 | 0.6-3.3: Iván ya sabía cuál era su parada.<br>3.6-5.2: Tenía que bajarse antes. | — | `susto` en 0.1 |
| 2 | `p3_s02_titulo` | 4.0 | (sin narración) | [TÍTULO] · Parte 3 de 3 | — |
| 3 | `p3_s03_repaso` | 8.0 | 0.3-4.6: En el camión sin número, cada pasajero se bajó donde murió.<br>4.9-7.3: Y su boleto era de mañana. | — | — |
| 4 | `p3_s04_giro` | 10.0 | 0.3-1.9: Entonces, la pasajera habló. | 2.2-5.7: Pasajera: «Este camión no se lleva a los muertos.»<br>6.0-9.1: Pasajera: «Avisa a los que van a morir.» | — |
| 5 | `p3_s05_timbre` | 10.5 | 0.3-1.9: Iván tocó el timbre.<br>2.2-5.3: El camión frenó en una parada a oscuras.<br>5.6-7.2: El chofer no volteó. | 7.5-9.9: Chofer: «Al bajar, no mires atrás.» | — |
| 6 | `p3_s06_bajar` | 8.0 | 0.3-1.5: Iván bajó.<br>1.8-4.2: A su espalda, todos lo miraban.<br>4.5-5.7: No miró atrás. | — | motor que se va y corte a blanco al final en 5.9-7.3 |
| 7 | `p3_s07_despierta` | 10.0 | 0.3-3.8: Abrió los ojos en la banca de su parada.<br>4.1-5.7: Entonces vibró su celular. | 6.0-9.1: Beto: «¿Te llevo? Ya voy en el coche.» | — |
| 8 | `p3_s08_no` | 7.5 | 3.3-6.8: Esa noche, Iván no se subió a ese coche. | 0.3-3.0: Iván: «No, gracias. Me voy a pie.» | — |
| 9 | `p3_s09_o_no` | 13.0 | 0.3-2.7: En su bolsillo seguía el boleto.<br>3.0-6.5: Y en el vidrio de una tienda, su reflejo<br>6.8-8.8: seguía sentado en el camión.<br>9.7-12.4: ¿Se salvó? ¿O sigue en el camión? | — | `susto` en 9.1 |
| 10 | `p3_s10_cierre` | 6.0 | 0.3-1.9: ¿Iván despertó de verdad?<br>2.2-3.8: Comenta: sí o no. | Comenta: sí o no. | — |

**Total parte 3 (B): ≈ 83.0 s**


---

## Notas para Animación

**Qué versión se produce:** la **A** (sin narrador). La B solo se produce si Alejandro aprueba una voz (hoy ninguna convence; ver `docs/estudio/tts_busqueda_2026-11.md`). Las dos comparten las mismas escenas, los mismos dibujos y el mismo sonido. Con la B se agregan `NARRATION = True`, `VOICES`/`SAY` y `--voces`.

### Dibujos y elementos nuevos (`historias/ruta0/dibujo/`)

- **El camión, por fuera:** viejo, diseñado desde cero (sin colores, logos ni rutas reales). Faros, letrero con el **"0" ámbar** que parpadea y puertas neumáticas que abren y cierran.
- **El camión, por dentro:** pasillo con filas de asientos, luz amarilla que parpadea, ventanas con lluvia y vaho, el botón de parada con su foco rojo y el **tablero luminoso de la ruta** arriba del chofer, con paradas que se apagan y la última que se prende: IVÁN.
- **Personajes:**
  - **Iván:** sudadera y mochila. Poses: de pie en la parada, sentado, levantándose, caminando, dormido o despertando en la banca y con el celular.
  - **Chofer:** a contraluz o de nuca; nunca se le ve la cara.
  - **Pasajera:** pálida y muy quieta. Su mano en la muñeca de Iván. De frente solo en la parte 3, con los ojos en sombra.
  - **Pasajeros arreglados:** traje, vestido de fiesta, ropa de domingo. Quietos y sin parpadear.
  - **El señor con ropa de trabajo** (parte 2) y **la muchacha con vestido de fiesta** (parte 2).
- **Exteriores:**
  - Parada con techito y banca (la base es la calle de noche de `rio_perros/dibujo/calle.py`, sin papel picado y con lluvia).
  - La curva: barandal doblado, cruz con flores de plástico, veladora y la foto del señor.
  - El puente: barandal roto y el río abajo.
  - La parada a oscuras de la parte 3 y el vidrio de una tienda cerrada con el reflejo de Iván sentado en el camión.
- **Primeros planos:**
  - El boleto: "RUTA 0 · VÁLIDO: [fecha]". La fecha del boleto es el día siguiente a la del celular; las dos se fijan con Redes según el día de publicación de la parte 2.
  - El celular: fecha de hoy en la parte 2 y mensaje de Beto en la parte 3.
  - El dedo en el botón de parada.
  - Los vidrios empañado y limpio.
- **Letreros de parada:** CURVA DEL AHORCADO, PUENTE VIEJO.
- **Se reutiliza:**
  - `kit.title_card` (título con falla y kicker "Parte N de 3"), `kit.rain` (lluvia), `kit.fog` (neblina y vaho).
  - `grade.glitch` y `grade.rojo`, y `GRADE` frío como en la Llorona.
  - Capas en caché para el interior del camión y la parada.

### Sustos, tensión e impacto (versión A; los segundos son relativos a cada escena)

| Parte | Escena | Momento | Qué pasa |
|---|---|---|---|
| 1 | s01 | 0.2 | Frenos de aire + `susto` + glitch al entrar el gancho |
| 1 | s06 | 3.0-3.8 → 4.0 | **Silencio total** (se va todo) → solo la respiración y el latido de Iván + glitch suave: "Nadie respiraba." |
| 1 | s08 | 2.0-3.0 → 3.0 | Silencio → `susto` + glitch + destello rojo con la mano de la pasajera (**susto principal de la parte 1**) |
| 2 | s01 | 0.2 | `susto` en el gancho |
| 2 | s04 | 3.6 | Glitch en la foto de la cruz; rechinido de llantas lejano que se corta (sugerido, nunca mostrado) |
| 2 | s06 | 3.8-4.6 → 4.6 | Silencio → `susto` + glitch cuando se prende IVÁN |
| 2 | s08 | 2.9-3.4 → 3.4 | Silencio → `susto` + tinnitus con la fecha de mañana (**susto principal de la parte 2**) |
| 3 | s01 | 0.2 | `susto` en el gancho |
| 3 | s06 | 5.0-5.6 → 7.2 | Pasajeros mirándolo detrás de Iván; el motor se va de golpe → **corte a blanco** |
| 3 | s09 | 4.0-4.5 → 4.5 | Silencio → timbre + motor que solo suena "en el reflejo" + `susto` y glitch (**susto final**) |

- **Regla visual:** los accidentes nunca se muestran. Solo cruz, barandal, rechinido lejano y corte.
- **Regla de sonido:** los pasajeros no hacen ningún ruido; los únicos que respiran y hacen ruido son Iván, el chofer al hablar y el camión.

### Sonido nuevo (sintetizado, en `motor/audio/`)

- Frenos de aire (siseo neumático) y puertas neumáticas.
- Lluvia: en lámina, en el vidrio y en charcos (`ambient.py`).
- Motor de camión viejo, por dentro y por fuera, que se acerca y se aleja (puede partir de `motor_hum`).
- Timbre de parada (puede partir de `ding`, más grave) y vibración de celular.
- Se reutilizan: `breath`, `heartbeat`, `susto`, `riser`, `tinnitus`, `cold_touch`, `wind`, `crickets`, `water`, `step_*`, `gota`.

### Zona segura

El letrero "0", el tablero de la ruta, el boleto con las fechas, los letreros de parada y el celular van **entre el 12 % y el 70 % de la altura** (y ≈ 230-1340) y lejos de la columna derecha: se encuadran a media pantalla, no arriba. Los subtítulos van en su banda (y 1264-1440). Comprobarlo con `revisor-cuadros` (paso 7), sobre todo en P1 s01, P2 s06, P2 s08 y P3 s07.

### Duración estimada

La duración de cada escena está en las tablas de arriba.

| Parte | Versión A (se produce) | Versión B (alternativa) |
|---|---|---|
| 1 · El último camión | 56.5 s (9 escenas) | ≈ 69.5 s |
| 2 · Las paradas | 58.5 s (9 escenas) | ≈ 66.0 s |
| 3 · La última parada | 64.5 s (10 escenas) | ≈ 83.0 s |
| **Total de la serie** | **179.5 s** | **≈ 218.5 s** |

- En la B, los tiempos se calcularon a 2.6 palabras por segundo; con la voz real se recalculan con `--voces`.
- La parte 3 de la B queda a 7 s del tope de 90 s: si la voz real la alarga, se recorta texto en s03 y s09.
- **Publicación (Redes):** las 3 partes en días seguidos o cada 2 días, sin chocar con La Planchada ni con Villa (20 nov). Comentario fijado: el texto de la ficha.
