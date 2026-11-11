# Light Fades Twice 0.12.5: prueba humana (Windows / DX12)

Estado: **HUMAN_RUNTIME_PENDING**.

## Instalación (juego cerrado)
1. En tu carpeta de mods, sustituye **solo** el `.dusk` 0.12.4 de Light Fades Twice.
2. Coloca únicamente `LIGHT_FADES_TWICE_LIZALFOS_FIX05_0_12_5_PRIVATE_TEST_windows-amd64_eade22d6b94d.dusk`, SHA-256 `8d62780bc0782ce68dc88cd86b930915933892eb2f25919791a9edfed21c6775`.
3. No dejes dos versiones.

## Rollback (juego cerrado)
`.dusk` 0.12.4, SHA-256 `e75a3ff05db32042a12c7abb2dde1218cf7e84585ebffb371cd41dd745fa7330`, run 42950612778, artifact 13826757793. La opción de Z-target se conserva.

## Pasadas
- **A:** solo Light Fades Twice 0.12.5.
- **B:** 0.12.5 más los otros ocho mods.

Guarda un log de cada una.

## Primero en el log
- `PARRY_FX event=INSTALL ... enabled=1 spark=1 sound=1 ... pitch=1.22`
- Ningún `funchook failed`.
- `PARRY_FX event=RESOURCE` para `0x0117` y `0x0118`.
- Al cerrar: `LIZ_SUMMARY part=FIX05`, `part=FIX05_CUTS`, `PARRY_FX_SUMMARY part=FIX05`, SHUTDOWN limpio.

## Lista priorizada
| # | Prueba | Esperado | Log |
|---|---|---|---|
| 1 | Machaca B de frente, combo completo, varias veces | Tras dos bloqueos, a menudo te desvía en mitad del combo, también en el corte izquierdo y el remate | `COMBO_LINK event=REVERSE_CHECK ... rebound=1`, `part=FIX05_CUTS` |
| 2 | Observa ese rebote | Sin deslizarse, girar de golpe ni congelarse. Un solo rebote | `COMBO_LINK event=REBOUND_STATE reverse=1` |
| 3 | Tras el parry | +25 a Link, contraataque N o D defendible, vuelven los combos | `LIZ_COUNTER`, `LIZ_COMBO event=START` |
| 4 | Racha sin parry | Debe ser azar, enfriamiento o flanco | `LIZ_RESPONSE result=`, sin `WINDOW_LATE` repetido |
| 5 | Parry del Lizalfos | No pierde HP con ese tajo | `LIZ_TRACE verdict=ENEMY_PARRY hp=X->X`, sin `LIZ_CONFLICT` |
| 6 | Golpe mientras sube o baja el escudo, flanco, espalda, rotura | Daño real | `verdict=BODY_DAMAGE` |
| 7 | Parry tuyo y del Lizalfos | Arma y escudo enteramente naranjas | `FX_PAIR`, tu vista |
| 8 | Parry a Bokoblin | Igual, naranja | tu vista |
| 9 | Bloqueos normales | Chispa original | `block_spark_original` |
| 10 | Sonido del parry | Mismo sonido, claramente más agudo, una vez | `NATIVE_AUDIO_PITCHED`, tu oído |
| 11 | Z-target, R+B, HUD, Finish, Helm Splitter | Sin cambios; la opción persiste al reabrir | tu percepción |
| 12 | FPS con varios enemigos, escenas, pausa, cerrar | Sin caída nueva, SHUTDOWN limpio | tu medición |

Si queda algo azul, pásame el log: `RESOURCE` y `PARRY_SPARK_BLUE_RISK` dicen por qué.

La telemetría prueba que la ruta se ejecutó. No prueba cómo se ve ni cómo suena.
