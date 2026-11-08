# Light Fades Twice 0.12.0: prueba humana (Windows / DX12)

Estado: **HUMAN_RUNTIME_PENDING**.

## Instalación (con el juego cerrado)
1. En la carpeta de mods, quita **todos** los `.dusk` anteriores de Light Fades Twice (el log del 8 de noviembre mostraba también un archivo 0.11.11 en esa carpeta).
2. Coloca solo `LIGHT_FADES_TWICE_LIZALFOS_0_12_0_PRIVATE_TEST_windows-amd64_03111c85b449.dusk`.
3. No toques los otros ocho mods.

## Rollback
Quita el 0.12.0 y vuelve a poner el `.dusk` 0.11.12 aprobado: SHA-256 `82f678a8ffacf197d7828721513597fe1b4d3c6752ca07ce2d6a6c9c2797d2ed`.

## Qué mirar primero en el log
- `LIZ_POSTURE event=INSTALL ... enabled=1`. Con `enabled=0` el Lizalfos es original.
- `LIZ_POSTURE event=ADMITTED ... arg0= arg1=` o `EXCLUDED_VANILLA reason=`. Si un Lizalfos normal sale excluido como `DYNALFOS_ARG1`, la inferencia de identidad está mal: envía esa línea.
- `LIZ_SUMMARY` al cerrar, y cualquier `LIZ_CRITICAL`.

## Matriz
| # | Prueba | Esperado | Línea de log |
|---|---|---|---|
| 1 | P1, P2, P3 y P4 sin defenderte, sin atacar | 4/7/9/6 golpes; ritmos distintos; nunca un quinto patrón | `LIZ_COMBO`, `LIZ_SWING event=OPEN` |
| 2 | ¿Se reconocen los ritmos? ¿La entrada recortada entre acciones se ve bien? | juicio visual tuyo; es la parte más nueva | `LIZ_COMBO event=ACTION start_frame` |
| 3 | R mantenido contra todo un combo | ningún golpe cancela; el doble hace sus dos golpes; termina `COMPLETED` | `result=GUARD`, `cause=COMPLETED` |
| 4 | R+B a tiempo en N y en cola | parry, +22; el combo sigue | `LIZ_PARRY event=LINK_PARRY` |
| 5 | D1 y D2 con dos R+B físicos | dos parries, dos seriales | dos `LINK_PARRY` en un doble |
| 6 | D1 con un solo R+B | un parry; D2 bloqueo normal o golpe | `result=GUARD` o `DIRECT` |
| 7 | R+B tardío | bloqueo, no parry | `MISSED_WINDOW_GUARD` |
| 8 | Golpes al cuerpo sin defensa | daño nativo, reacción de Link, ni fantasmas ni golpes atravesados | `result=DIRECT` |
| 9 | Alejarte durante un combo | fallo limpio sin daño inventado | sin `CONTACT` |
| 10 | Espadazos con postura <100 | baja la vida, no tambalea, no se cancela su ataque | `event=GAIN source=SWORD` |
| 11 | Ruptura desde postura baja (cinco parries) y alta | derribo una vez; remate posible; sin remate se levanta con postura 0 | `LIZ_BREAK LATCH` y `REARM` |
| 12 | 370 HP | la barra de vida arranca llena; varios golpes; no se cura nunca | `event=HP_SET`, vida en cada `GAIN` |
| 13 | Regeneración de postura | tras 2 s sin ganar postura baja la barra; más lenta con menos vida | barra; `LIZ_POSTURE` |
| 14 | Pocos espadazos sueltos, de frente | a veces bloquea (+5) | `ORDINARY_BLOCK` |
| 15 | 3 espadazos en 2,5 s | más intentos de parry | `LIZ_DEFENSE event=ROLL level=B pct=35` |
| 16 | Presión sostenida sin defenderte | nivel C | `level=C pct=45` |
| 17 | Parry enemigo | espada desviada, +25 a tu postura, 0 de daño directo, sin efectos nuevos | `LIZ_PARRY event=ENEMY_PARRY`, `LIZ_LINK` |
| 18 | Tras un parry enemigo | a veces contraataca o se reposiciona; puedes defender | `LIZ_TURN` |
| 19 | 4 s tras un parry enemigo | no repite parry | `cooldown_until` |
| 20 | Espadazos por el lateral y la espalda | sin parry | sin `ENEMY_PARRY` |
| 21 | Tu postura de 99 a 100 durante tu ataque | sin congelarte; ruptura de guardia solo en un estado seguro | `LNK05_EVENT` |
| 22 | Guardia prolongada, R mantenido frente a él | no se queda «pensando» | ninguna `LIZ_CRITICAL code=3` |
| 23 | Varios Lizalfos, y mezcla con Bokoblins | cada barra y cada parry van a su actor; Bokoblins como en 0.11.12 | `actor=` |
| 24 | HUD | barra 0..100 bien alineada; sin solapes; prompts ocultos | visual |
| 25 | FPS con 1 y con varios Lizalfos | sin bajada apreciable frente a 0.11.12 | visual |
| 26 | Cambio de sala, pausa, muerte, salir del juego | sin cuelgues; `LIZ_SUMMARY` al cerrar | `LIZ_SUMMARY` |

## Si algo falla
Indica el número de la prueba y envía el log. Los golpes atravesados dejan rastro en `LIZ_SWING` (distancia y `max_center_step`) y `LIZ_CRITICAL event=AT_SAMPLE_GAP`.
