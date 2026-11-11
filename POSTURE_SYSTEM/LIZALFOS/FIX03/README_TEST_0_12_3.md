# Light Fades Twice 0.12.3: prueba humana (Windows / DX12)

Estado: **HUMAN_RUNTIME_PENDING**. Color de la chispa, tono del sonido, entrada física, colisión real y FPS solo se confirman aquí.

## Instalación (juego cerrado)
1. En tu carpeta de mods, sustituye **solo** el `.dusk` de Light Fades Twice.
2. Coloca únicamente `LIGHT_FADES_TWICE_LIZALFOS_FIX03_0_12_3_PRIVATE_TEST_windows-amd64_2aa4abe2e3b4.dusk`, SHA-256 `f3bab58159aa270ad72cec721523bee8ec675cef476aad8f7b151f7d9b4c94a8`.
3. No dejes dos versiones. Conserva los otros mods. No toques partidas.

## Rollback (juego cerrado)
`.dusk` 0.12.2, SHA-256 `87725c176e595b7c69e20fff5bdd4b44764d050f2cb6b248a8b8dd32092f94ad`, run 42556628271, artifact 13649337870. Sustituye el 0.12.3 por ese archivo. La opción `sekiro_lockon` queda en `config.json` sin efecto.

## Primero en el log
- `LIZ_POSTURE event=INSTALL ... enabled=1 ... gains=6/12/30/5/25`
- `PARRY_FX event=INSTALL ... enabled=1 ... pitch=1.12`
- `LOCKON event=INSTALL ... detail=MOD_PANEL_TOGGLE_BOUND_TO_CONFIG_VAR a=1 b=1`
- Al cerrar: `LIZ_SUMMARY part=FIX03`, `PARRY_FX_SUMMARY`, `LOCKON_SUMMARY` y un SHUTDOWN limpio.

## Lista priorizada
| # | Prueba | Esperado | Log |
|---|---|---|---|
| 1 | Parry del **segundo golpe de un doble** (D2): pulsa R+B otra vez justo tras parar D1 | D2 también es parry, con su propio movimiento de escudo | `chain_buffered>0`, `double_rearms>0`, `dpair>0` en `part=FIX03` |
| 2 | Primer golpe de **P3** | Parry con pulsación algo anticipada. La preparación es corta y la ventana no se ensanchó | `LIZ_SWING event=CONTACT pattern=3 impact=1`, mira `link_delta` |
| 3 | Combos enteros con parry en cada impacto (4/7/9/6) | Cada golpe admite parry. En P3, ruptura justo en el noveno | `LIZ_PARRY`, `LIZ_BREAK` |
| 4 | Bloquea sin pulsar R+B | Nunca hay parry automático. Chispa azul y sonido original | Sin línea `PARRY_FX` |
| 5 | Lizalfos en guardia: golpéalo de frente | Sin HP, +5 una vez, sin rebote | `LIZ_SHIELD event=CONTACT covered=1`, `LIZ_GUARD event=BLOCK` |
| 6 | Guardia: rodéalo por su lado descubierto y por la espalda | Se gira hacia ti de forma natural. Si llegas antes de que gire, sí hay daño | `LIZ_SHIELD event=CONTACT covered=0` |
| 7 | Parry de Link a Lizalfos y a Bokoblin | **Misma chispa en naranja** y mismo choque más agudo, una vez | `CONFIRMED_NATIVE_EMITTER_RECOLORED`, `NATIVE_AUDIO_PITCHED` |
| 8 | Parry del Lizalfos sobre Link | Naranja y agudo, +0 para él, +25 para Link, rebote nativo | `kind=LIZALFOS_PARRY_LINK` |
| 9 | Fíjate en si la chispa sale **toda** naranja | Si queda azulada, dímelo: el azul estaría en la textura | Tu vista |
| 10 | Fijación: toca el botón de fijar | Fija y sigue fijado al soltar. Otra pulsación suelta | `LOCKON event=TOGGLED`, `event=CANCELLED` |
| 11 | Con varios enemigos, mueve el stick derecho a un lado | Cambia una vez por gesto. Vuelve al centro para repetir | `LOCKON event=SWITCH` |
| 12 | Desactiva "Fijación de objetivos estilo Sekiro" en el panel del mod y reinicia | Sigue desactivada. Fijación nativa exacta | `LOCKON event=OPTION_CHANGED`, `INSTALL a=0` |
| 13 | Ritmos de los combos | Igual que 0.12.2 | Tu percepción |
| 14 | Muchos enemigos | FPS sin caída nueva | Tu medición |
| 15 | Pausa, cambio de sala, cerrar | Sin atascos, SHUTDOWN limpio | Fin del log |

`UNCONFIRMED` o `NATIVE_UNMODIFIED_SAFE` significan que ese parry conservó el efecto original o se revirtió. Si aparecen a menudo, pásame el log.

Haz una pasada **A** solo con Light Fades Twice y otra **B** con los demás mods si puedes. Si algo falla, dime patrón, impacto y distancia, y pásame el log.
