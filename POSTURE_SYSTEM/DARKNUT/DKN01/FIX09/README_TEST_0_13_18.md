# Prueba humana — LIGHT FADES TWICE 0.13.18 (DKN01 FIX09)

Archivo a usar: `LIGHT_FADES_TWICE_DARKNUT_MINIBOSS_FIX09_0_13_18_PRIVATE_TEST_windows-amd64_3221981c18f3.dusk` (419 376 bytes, SHA-256 `b3d54656…bf97ff7`). **Un solo LFT activo**: quita el .dusk de 0.13.17 de la carpeta `mods` (guárdalo aparte como rollback) y pon el de 0.13.18. No cambies dificultad ni ajustes. Para confirmar que cargó la versión correcta, el log debe contener `found 'Light Fades Twice ...' v0.13.18` y `DKN01 event=INSTALL_FIX09`.

No hace falta precisión de ticks: el log la tiene. Anota fase (F1/F2/F3), ataque/combo y hora aproximada de lo raro; un clip corto ayuda solo si algo persiste.

## Sesión A — 0.13.18 solo (Enemy Spawner Standalone solo si lo necesitas para invocar al Darknut normal; es el único auxiliar mínimo)
Primero en terreno llano, luego cerca de bordes, paredes, pendientes y agua.

1. **Ataque con salto de Link** (frontal, lateral, por la espalda; cerca y lejos; con el Darknut quieto, en guardia, atacando y esquivando). Cada salto debe acabar en una de tres cosas: **daño real** (barra de vida baja), **bloqueo con la espada/escudo de frente** (chispa + choque) o **esquiva real** (el Darknut ya no está ahí). Nunca un golpe que "atraviesa" sin efecto. Por la espalda o el lateral en F2/F3 debe hacer daño. En F1 el escudo y la armadura siguen protegiendo de frente. No confundas con el Helm Splitter.
2. **Esquivas del Darknut (F2/F3)**: golpéalo justo al empezar a saltar, en pleno vuelo y al aterrizar. Al principio del salto (≈0,2 s) no le haces nada y **no** debe sonar ni verse ningún choque; después sí recibe daño. Nunca debe "bloquear" en el aire. Prueba también junto a paredes/bordes/agua: si no hay sitio no salta.
3. **Golpes que te dañan** (F1, F2, F3; incluidos el primer y el segundo corte del espadazo doble, contraataques y combos tras su salto): cuando de verdad pierdas vida, el Darknut termina ese golpe con naturalidad y **no** lanza el siguiente (si te alcanza el primer corte del doble, el segundo no llega). Luego se queda en guardia o salta hacia atrás; no te persigue mientras te recuperas. Si solo bloqueas, haces parry o esquivas, el combo sigue como antes. Comprueba la ruptura de tu postura y el daño ×2.
4. **Cautela**: lucha con él con mucha vida/postura, luego medio y luego casi roto o con poca vida. Con poca reserva debe esquivar y retroceder algo más a menudo, pero no huir sin parar ni encadenar saltos (como mucho una maniobra cada 3 s). Aléjate de verdad: debe volver a acercarse (o su salto ofensivo + combo). F1 nunca salta.
5. **FX (prioridad)**: parry de los dos cortes de un doble, parry del 1.º y bloqueo del 2.º, bloqueo del 1.º y parry del 2.º, bloqueo/bloqueo, varios dobles seguidos, estocadas, mazazos, golpe de escudo/patada, B1, maza lanzada y parry del Darknut. En cada **parry**: todo naranja y choque agudo. En cada **bloqueo**: chispa azul y sonido normal (correcto). Recuerda: cada corte del doble necesita su propio Shield Attack; si solo hiciste uno, el segundo corte es un bloqueo y será azul. Si ves azul o no oyes agudo en un parry auténtico, anota fase, combo, qué corte (1.º/2.º) y la hora.
6. **Lo que ya funcionaba**: Helm Splitter F1 (mira a Link), F1-C3, B1, ejecuciones, Finish F2 → resurrección, F3 Finish y muerte por vida a 0 (la espada se oscurece con el cuerpo, solo el Darknut), reposicionamiento tras levantarse, HUD, Manual Shield, cancelación ataque→guardia, tus esquivas (9/6/6) y Bokoblins/Lizalfos/Chilfos sin cambios.

## Sesión B — mods habituales + 0.13.18 (único LFT)
Repite sobre todo los puntos 1-5 y comprueba la convivencia. Si algo empeora, prueba lo mismo con 0.13.17 (nunca los dos a la vez).

Envía los logs **completos** de `%APPDATA%\TwilitRealm\Dusklight\logs`, uno por sesión, diciendo cuál es cuál y tus impresiones. No borres ni edites los anteriores.
