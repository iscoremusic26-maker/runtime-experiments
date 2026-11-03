# LNK SESSION02 FIX01 (0.11.1): defensa manual + vulnerabilidad extendida tras la ruptura

**Estados por componente:** ver `RESULTS.json`. Ninguno está observado en el juego: `HUMAN_RUNTIME_PENDING`.

**Procedencia:** `SOURCE_PROVENANCE.md`.

**Origen de la petición.** En la prueba humana de 0.11.0 (`HUMAN_RUNTIME_OBSERVED_ACOTADO`, log `dusklight-20261102-172208`, resumen del encargo; Claude no lo abrió) todo funcionó, pero la ruptura castigaba poco en el uno contra uno.
- Cancelación en 28-29 ticks; fin nativo en 36.
- La guardia por fijación con L volvía inmediatamente.

## 1. Orden nativo usado (2.0.3, fuente + EXE)

```
daAlink_c::execute
  setStickData            (18020)  PAD_1 -> mItemTrigger/mItemButton   <- POST FX: muestra R/A/B; consumo contextual de B
  checkDamageAction       (18262)  bloqueo/daño/rupturas nativas         <- POST LNK05 (0.11.0): procGuardBreakInit + inicio de penalización
  setShieldGuard          (18281)  FLG2_UNK_8000000 (guardia)            <- POST FX: apaga la guardia de fijación sin R / en penalización / sin rearme
  (this->*mpProcFunc)()   (18308)  procedimiento:
      checkItemAction: espada (mItemTrigger&B) ... sitio del Shield Attack: setRStatus(0x3a) + spActionTrigger()
                                                                       <- PRE FX setRStatus: oferta (omite el estado R); POST FX spActionTrigger: R+B
      checkMoveDoAction: A + DoStatus JUMP (0x19) / 0x79                <- PRE FX: veto de la admisión de esquivas en penalización
      procGuardBreak: setUpperGuardAnime() en cada frame; salida a cancel 28 / fin 35; ERFLG1_UNK_20 solo si no hay fijación
  setCollision            (18642)  escudo Tg si checkPlayerGuardAndAttack() && !ERFLG1_UNK_20
                                                                       <- PRE FX: apaga la bandera residual en penalización/rearme
```

## 2. Máquina defensiva (`src/lnks2fix_core.hpp`, pura, compartida con el laboratorio)

| Estado | Entrada | Restricciones | Salida |
|---|---|---|---|
| `READY` | — | ninguna; guardia solo con R + fijación | ruptura física confirmada |
| `NATIVE_BREAK_ACTIVE` | `procGuardBreakInit` verificado (LNK05), ruptura nativa adoptada con saturación o ruptura nativa observada sin saturación (solo latch) | sin guardia ni Shield Attack; sin esquivas si es extendida | `mProcID != PROC_GUARD_BREAK` observado |
| `POST_BREAK_VULNERABLE` | salida nativa antes del presupuesto (solo extendida) | sin guardia, Shield Attack, parry, backflip, sidehop ni rodadas. Libres: andar, correr, girar, fijar, espada | `active_ticks >= 75` |
| `REARM_REQUIRED` | presupuesto cumplido (y salida nativa) | sin guardia ni Shield Attack (esquivas libres) | R soltado **después** del desbloqueo y vuelto a pulsar |

**Reloj:**
- `kTotalPenaltyTicks = 75` ticks de simulación **activos** (`mod_update`; 30 Hz nominal = 2,5 s), contados **desde la entrada nativa confirmada**.
- Es la única constante; la auditoría exige una sola definición.
- La pausa y el menú congelan el reloj.
- Muerte, lobo, Link nueva o ausente, cambio de epoch o evento: `ABORTED_SAFE` → `READY`. Nunca deja el escudo bloqueado para siempre.

**Fin efectivo:** `max(fin nativo, 75)`. Si `GUARD_BREAK` dura más, la guardia sigue bloqueada; el watchdog de 150 ticks es solo diagnóstico.

**Reinicio de postura:** una sola vez, en la salida nativa (LNK06 de 0.11.0, sin cambios). Al terminar la penalización no hay otro reinicio.

**Rupturas en cascada:**
- Durante `NATIVE_BREAK_ACTIVE` y `POST_BREAK_VULNERABLE`, `lnk05_request` rechaza (`REQUEST_BLOCKED`) cualquier nueva solicitud.
- La postura sigue acumulándose, pero sin cola ni reinicio del reloj.
- En `REARM_REQUIRED` un **nuevo** impacto válido a 100 puede romper de nuevo: es un ciclo nuevo y completo.

**Ruptura nativa sin saturación** (4.º bloqueo con la barra baja, at_spl 9/10/11): solo latch de rearme, sin extensión a 2,5 s.

## 3. Defensa manual (adaptada de Lazy Shield Rework, solo la parte manual)

- **Guardia:** el juego calcula la bandera. Con fijación (L), su rama 3 la enciende; el POST la **apaga** si no hay R (`DENIED_NO_R`), si hay penalización (`BLOCKED_BY_PENALTY`) o si falta el rearme (`REARM_REQUIRED`).
  - `GUARD_SLIP` (sin bola de hierro) y la guardia pequeña son reacciones nativas y nunca se tocan.
  - R sin fijación no hace nada: la rama nativa exige `checkGuardActionChange`. No hay defensa agachada.
- **Shield Attack:** el juego ofrece el Shield Attack (todas sus condiciones nativas) llamando a `setRStatus(0x3a)` y luego a `spActionTrigger()`.
  - El PRE marca la oferta y omite el estado R.
  - El POST devuelve **R+B**, con B muestreado antes del consumo, o FALSE en penalización o rearme.
  - El `procGuardAttackInit` es el nativo: fotogramas, `mGuardAtCps`, voz y POST08 sin cambios.
- **B:** se quita de `mItemTrigger` solo si R está pulsado, la defensa está en READY y el juego ofreció el Shield Attack en el execute anterior.
  - Así R+B no produce también la espada.
  - Si la técnica no está aprendida, no hay escudo o la defensa está en penalización, B es la espada normal.
- **HUD:** «Shield Attack» en B mientras R está pulsado en READY (`setBStatus`, solo etiqueta).

## 4. Veto de esquivas

`checkMoveDoAction` es el **único** punto de admisión de las esquivas voluntarias:
- A con `DoStatus` JUMP: sidehop, salto atrás (`procSideStepInit` → `procBackJumpInit`) y rodada lateral (`checkSideRollAction`).
- A con `DoStatus` 0x79: rodada frontal.

Las demás llamadas a esos `procInit` son forzadas y no pasan por aquí: aterrizaje, buceo, demo, caballo, colgado y corte.

Durante la penalización extendida, el PRE devuelve FALSE sin ejecutar el original. La siguiente comprobación de botones (`checkSubjectAction`, `checkItemChangeFromButton`) no usa A, así que A no se pierde hacia otra acción. Hablar, abrir y trepar se deciden antes, en `checkNormalAction`.

## 5. LNK04 adaptado

`lnkfx::regen_bonus(native_guard_safe, fx_enabled, manual_accepted, phase)` es la misma función en `mod.cpp` y en el laboratorio.
- x1,5 solo con guardia nativa segura **y** guardia manual aceptada en el último execute **y** READY.
- L sin R, R sin escudo o sin fijación, penalización o rearme: x1.
- Valores 10/8/5/2, x1,5 y retardo de 30 sin cambios.
- Eventos `LNK_FIX01_REGEN` `GUARD_X1_5_ACCEPTED` / `GUARD_BONUS_REFUSED` con su motivo.

## 6. Escrituras (tabla formal)

| Escritura | Owner | Dónde | Condición | Restauración / límite |
|---|---|---|---|---|
| `procGuardBreakInit()` (0.11.0) | LINK_NATIVE_TRANSITION | POST de `checkDamageAction` | puerta LNK05 | sin cambios en 0.11.1 |
| `offNoResetFlg2(FLG2_UNK_8000000)` | MANUAL_SHIELD | POST de `setShieldGuard` | la bandera la encendió la rama de fijación y la defensa no la admite | la operación nativa de la rama `else`; el juego la recalcula en el siguiente execute |
| `offNoResetFlg2(FLG2_UNK_8000000)` | PENALTY | PRE de `setCollision` | penalización o rearme, proc distinto de `GUARD_BREAK`/`SLIP`/`ATTACK`, bandera encendida | ídem; nunca se enciende |
| `mItemTrigger &= ~BTN_B` | SHIELD_ATTACK_INPUT | POST de `setStickData` | R pulsado, READY, Shield Attack ofrecido | es el disparador de este execute; el juego lo reescribe cada execute |
| Retorno de `spActionTrigger` | SHIELD_ATTACK | POST, solo tras la oferta | R+B en READY (si no, FALSE) | — |
| Retorno de `checkMoveDoAction` = FALSE (sin original) | DODGE_VETO | PRE | penalización extendida y A con JUMP/0x79 | — |
| `setRStatus(0x3a)` omitido | SHIELD_ATTACK | PRE | solo el estado 0x3a | — |
| `setBStatus(SHIELD_ATTACK)` | HUD | POST de `spActionTrigger` | R pulsado y READY | solo etiqueta |

**Ninguna** escritura de `mProcID`, `field_0x2fd5`, `mModeFlg`, `mDamageTimer`, vida, velocidad, animación, timers ni hitstun. La auditoría de código fuente lo exige por texto y número, y la auditoría binaria lo verifica en la DLL.

**Instalación todo o nada:**
- Se instalan seis hooks. Si uno falla, se desinstalan los seis y el mod sigue siendo 0.11.0 exacto: guardia nativa por L, Shield Attack con R, sin penalización extra.
- Nunca queda medio escudo.
- `lf.enabled` solo pasa a true después de las seis instalaciones.

## 7. Telemetría nueva (la antigua se conserva)

| Línea | Contenido |
|---|---|
| `LNK_FIX01_INIT` | versión, origen LazyTweaks, ruta de R, ruta de entrada, reglas, `native_anim_speed=1.0`, `native_cancel=28`, `native_end=35`, `native_proc=31`, `total_penalty_ticks=75`, resultados de los hooks, `hooks_old=10 hooks_new=6 hooks_total=16` y la lista de escrituras |
| `LNK_FIX01_SHIELD` | `R_DOWN`/`R_UP` (con tope), `GUARD_ENABLED`, `DENIED_NO_R`, `BLOCKED_BY_PENALTY`, `REARM_REQUIRED` (por flanco), `REARMED` |
| `LNK_FIX01_SHIELD_ATTACK` | `R_B_ACCEPTED`, `DENIED_DURING_PENALTY`, `B_WITHOUT_R` |
| `LNK_FIX01_PENALTY` | `ENTER_NATIVE`, `POST_VULNERABLE`, `NATIVE_EXIT`, `COMPLETE`, `SHIELD_REARMED`, `ABORTED_SAFE`, `NATIVE_WATCHDOG`, `DUPLICATE_BEGIN_IGNORED`, `REQUEST_BLOCKED`; con `link_id`, `epoch`, `entry_tick`, `tick`, `active_ticks`, `native_ticks` y `remaining` |
| `LNK_FIX01_DODGE` | `BACKFLIP_DENIED`, `SIDEHOP_DENIED`, `SIDE_ROLL_DENIED`, `FRONTROLL_DENIED` |
| `LNK_FIX01_REGEN` | `GUARD_X1_5_ACCEPTED`, `GUARD_BONUS_REFUSED` (con motivo) |
| `LNK_FIX01_SUMMARY` | contadores, ventana min/máx **medida**, ticks nativos min/máx, latch (`held_through_unlock`, `released_after_unlock`), denegaciones por tipo, anomalías (slip, Shield Attack o guardia pequeña durante la penalización), invariantes y líneas descartadas |

## 8. Riesgos residuales (para la prueba humana)

1. **R en el mando real.** R es `getHoldLockR(PAD_1)` (el clic digital de R del perfil GameCube), muestreado por el juego. No lo he observado con el mapeo del usuario; si R no se reconoce, el escudo no subirá (línea `LNK_FIX01_SHIELD event=R_DOWN`).
2. **Vulnerabilidad real.** Durante la ventana no hay escudo Tg (invariante S1 del modelo y cierre en `setCollision`). La invulnerabilidad nativa de 30 ticks tras recibir un golpe sigue existiendo (`mDamageTimer`) y **no** se toca: en 2,5 s un enemigo puede conectar como mucho unos 2 golpes. Es comportamiento nativo y no se ha confirmado visualmente.
3. **Primer tick de R+B.** Si R, B y la fijación empiezan en el mismo tick, la oferta del Shield Attack aún no se ha visto: B será espada ese tick.
4. **Guardia pequeña:** `checkSmallUpperGuardAnime`, que solo ocurre con at_spl 8 o modo `0x70C52` y con el escudo ya activo. Si estuviera en curso al comenzar una penalización, el escudo podría seguir un instante; se cuenta como anomalía `small_guard`.
5. **Coexistencia con Lazy Shield Rework:** **no** se deben cargar ambos mods. Enganchan los mismos métodos y la misma bandera.
6. Las cifras del modelo (ventanas de 75, invariantes) son `LAB_MODEL_ONLY`.
