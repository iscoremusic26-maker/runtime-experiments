# Light Fades Twice 0.12.4: prueba humana (Windows / DX12)

Estado: **HUMAN_RUNTIME_PENDING**. Color de la chispa, tono del sonido, cobertura real del escudo, entrada física y FPS solo se confirman aquí.

## Instalación (juego cerrado)
1. En tu carpeta de mods, sustituye **solo** el `.dusk` 0.12.3 de Light Fades Twice.
2. Coloca únicamente `LIGHT_FADES_TWICE_LIZALFOS_FIX04_0_12_4_PRIVATE_TEST_windows-amd64_334ec89ad84d.dusk`, SHA-256 `e75a3ff05db32042a12c7abb2dde1218cf7e84585ebffb371cd41dd745fa7330`.
3. No dejes dos versiones. No toques partidas, EXE ni otros mods.

## Rollback (juego cerrado)
- `.dusk` 0.12.3, SHA-256 `f3bab58159aa270ad72cec721523bee8ec675cef476aad8f7b151f7d9b4c94a8`, run 42932174664, artifact 13820291574.
- Respaldo 0.12.2, SHA-256 `87725c176e595b7c69e20fff5bdd4b44764d050f2cb6b248a8b8dd32092f94ad`.
- La opción `sekiro_lockon` se conserva y 0.12.3 la sigue usando. No hay que tocar la configuración.

## Pasadas
- **A:** solo Light Fades Twice 0.12.4.
- **B:** 0.12.4 más los otros ocho mods de la prueba B original.

Guarda un log de cada una.

## Primero en el log
- `PARRY_FX event=INSTALL ... enabled=1 spark=1 sound=1 reason=ALL_HOOKS_INSTALLED`
- Ocho líneas `PARRY_FX event=HOOK ... result=0`.
- **Ningún** `funchook failed`.
- Al cerrar: `LIZ_SUMMARY part=FIX04`, `PARRY_FX_SUMMARY`, `LOCKON_SUMMARY` y un SHUTDOWN limpio.

## Lista priorizada
| # | Prueba | Esperado | Log |
|---|---|---|---|
| 1 | Machaca B de frente a un Lizalfos | Uno o varios golpes hieren, y luego levanta el escudo | `LIZ_TRACE verdict=BODY_DAMAGE`, `LIZ_GUARD event=ENTER` |
| 2 | Sigue con B contra el escudo levantado | Sin HP, +5 por tajo, sin rebote, Link sigue atacando | `verdict=BLOCK hp=X->X` |
| 3 | Dos bloqueos seguidos | A menudo (80 %) prepara un parry | `pairs>0`, `rolls80>0`, `LIZ_DEFLECT event=PREPARE_ROLL` |
| 4 | El siguiente tajo | Re-alza el escudo, parry, **rebote nativo** de la espada | `verdict=ENEMY_PARRY`, `link_gain=+25 liz_gain=+0` |
| 5 | Tras el parry | Contraataque normal o doble, defendible. Luego vuelven los combos | `LIZ_COUNTER event=ATTACK_COMMITTED`, `AT_OPEN`, `LIZ_COMBO event=START` |
| 6 | Parry del Lizalfos y tuyo (a Lizalfos y a Bokoblin) | **Misma chispa en naranja**, una vez | `CONFIRMED_NATIVE_EMITTER_RECOLORED` |
| 7 | Escucha esos choques | Mismo sonido, más agudo | `NATIVE_AUDIO_PITCHED`, `AUDIO_PITCH_READBACK_OK`, tu oído |
| 8 | ¿La chispa sale toda naranja? | Si queda azulada, dímelo | `EMITTER_CAPTURED` o `EMITTER_NEUTRAL_NOT_RECOLORABLE`, tu vista |
| 9 | Bloqueos normales | Chispa azul y sonido original | Sin línea `PARRY_FX` de ese golpe |
| 10 | Golpea por su espalda y por su derecha | Daño real. Se gira hacia ti sin saltos | `verdict=BODY_DAMAGE covers=0` |
| 11 | Golpéalo mientras sube o baja el escudo | Daño real | `presented=0` |
| 12 | Muchos bloqueos | La postura sube y puede romperse. Sin escudo infinito | `LIZ_BREAK` |
| 13 | Tus parries, dobles incluidos | Igual que en 0.12.3 | `dpair>0` |
| 14 | Bokoblins, HUD, Finish, Helm Splitter | Sin cambios | Tu percepción |
| 15 | Z-target; cierra el juego y reabre | Igual que 0.12.3. La opción se conserva | `LOCKON event=INSTALL`, valor `a=` |
| 16 | FPS con varios enemigos, escenas, pausa, cerrar | p50/p95/p99 sin caída nueva, SHUTDOWN limpio | Tu medición |

Si un golpe frontal con el escudo arriba hace daño, pásame el log: `LIZ_TRACE` registra la posición real del escudo y de Link en ese contacto.

La telemetría prueba que la ruta se ejecutó. No prueba cómo se ve ni cómo suena.
