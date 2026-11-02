# LNK SESSION02 (LNK05 + LNK06): implementación, versión 0.11.0 PRIVATE TEST

**Estados:**
- LNK05 y LNK06: `SOURCE_IMPLEMENTED`, `LAB_PASS (LAB_MODEL_ONLY)`.
- CI, PE y artefacto: ver `RESULTS.json`.
- Ejecución en el juego: `HUMAN_RUNTIME_PENDING`. Nada de esto está observado aún en el juego.

**Procedencia:**
- **Base:** 0.10.1 FIX01:
  - rama `feature/posture-lnks1-fix01-direct-hit-ai-liveness`;
  - commit `5454f32e0bb1fbdfde6ac866e94104e1b56df6be`;
  - `.dusk` `e7b8d5df…397d`.
- **Rama fuente:** `feature/posture-lnk05-lnk06-native-link-guard-break`.
- **Rama CI:** `ci/posture-lnk05-lnk06-native-link-guard-break`.
- **ID del mod (sin cambios):** `dev.posture.post05_selective_reactions`.

## 1. Hechos nativos usados

Fuente: host `40457c6` y EXE 2.0.3.

| Hecho | Dónde |
|---|---|
| `daAlink_c::checkDamageAction` se ejecuta una vez por execute de Link, fuera de demo y sin cambio de ropa. Su retorno solo se usa para `PROC_LARGE_DAMAGE` con las botas magnéticas. | `d_a_alink.cpp:18262` |
| El propio juego entra en la ruptura **desde esa función**: `return procGuardBreakInit();` (at_spl 9/10/11) y `procGuardSlipInit` → `field_0x2fd5++ == 4` → `procGuardBreakInit()` | `d_a_alink_damage.inc`, `d_a_alink_guard.inc:244-246` |
| `procGuardBreakInit`: `commonProcInit(PROC_GUARD_BREAK)`, `setSingleAnimeParam(ANM_GUARD_BREAK, mGuardBreakAnm)`, `mNormalSpeed = 0`, vibración, `Z2SE_AL_V_GUARD_BROKEN`; devuelve 1. Es pública y está exportada como `?procGuardBreakInit@daAlink_c@@QEAAHXZ`. | `d_a_alink_guard.inc:494` |
| `procGuardBreak`: al terminar la animación llama a `checkNextAction(0)`; si `frame > mCancelFrame`, a `onModeFlg(4)` + `checkNextAction(1)` (cancelación legítima del jugador) | `d_a_alink_guard.inc:509` |
| `mGuardBreakAnm` = {fin 35, velocidad 1.0, inicio 0, interpolación 3, cancelación 28} (datos const de release) | `d_a_alink_HIO_data.inc:930` |
| `PROC_GUARD_SLIP` 0x1d, `PROC_GUARD_ATTACK` 0x1e, `PROC_GUARD_BREAK` 0x1f | `static_assert` en `mod.cpp` |
| `mModeFlg` está en +0x42fc (u32). La ruptura nativa sin escudo exige `!checkModeFlg(0x70C52)` y `!checkModeFlg(0x4000000)`. | `static_assert offsetof` en `mod.cpp` |

## 2. Diseño

### LNK05: activación nativa

1. **Solicitud.** La crea solo un impacto **válido**: un bloqueo ordinario confirmado (`lnk01_contact`, `Verdict::Confirmed`) o un golpe directo confirmado (`lnk01_update`, `DirectResult::Confirmed`). La postura posterior debe ser `≥ 100`.
   - Nunca por regeneración ni sin impacto.
   - Un parry no llega a solicitar: es `RejectedParry` y suma +0.
   - Cada solicitud es un `lnk05::Episode`: Link, epoch, tick, atacante, generación, token, postura antes y después.
   - Si ya hay una ruptura pendiente o activa, la solicitud se rechaza (`duplicate_requests`). No hay cola.
2. **Disparo.** Se hace en un **segundo POST** del objetivo YA existente `LinkDamageFix01` (`daAlink_c::checkDamageAction`). No hay objetivo de hook nuevo: siguen siendo 10. El disparo ocurre dentro del execute de Link, después de su propia decisión de daño y guardia del tick, en el mismo punto desde el que el juego rompe.
   - La puerta pura `lnk05::Machine::gate` exige todo esto:

     | Condición | Rechazo |
     |---|---|
     | Hay una solicitud pendiente | — |
     | Dentro del plazo: bloqueo 3 ticks, directo 24 ticks | `EXPIRED` |
     | Misma Link y epoch | `LINK_MISMATCH` |
     | Humano | `NOT_HUMAN` |
     | Vivo | `DEAD` |
     | Sin pausa ni menú | `SIM_INACTIVE` |
     | Sin evento | `EVENT_RUNNING` |
     | No está ya en `GUARD_BREAK` (se **adopta**, nunca se reinicia) | `ALREADY_BREAKING` |
     | Origen permitido: espera, movimiento, fijado, giro, paso, agachado o `GUARD_SLIP`. Se rechazan Shield Attack, rodar, saltar, caer, cortes, daño, caballo, nado, etc. | `PROC_NOT_ALLOWED` |
     | `!(mModeFlg & 0x70C52)` y `!(mModeFlg & 0x4000000)` | `MODE_FLAGS` |
     | Sin daño nativo en **este** execute: `mDamageTimer` no subió respecto al `timer_before` capturado por el PRE de FIX01 | `DAMAGE_THIS_CALL` |
3. **Llamada única.** `lnk05_native_break(link)` hace `link->procGuardBreakInit()` y devuelve `link->mProcID == PROC_GUARD_BREAK`.
   - Es la **única** escritura de estado de Link del mod, de propiedad `LINK_NATIVE_TRANSITION`.
   - La entrada solo se da por confirmada con esa relectura. Si no, se registra `TRIGGER_FAILED` y la postura no cambia.
4. **Bloqueo.** Según el orden de los actores, la ruptura ocurre en el mismo execute de Link (enemigo antes que Link) o en el siguiente, desde `GUARD_SLIP`. Es la misma ventana que usa el juego en su 4.º bloqueo.
5. **Golpe directo.** Mientras dura la reacción nativa de daño (`PROC_DAMAGE` y similares), la puerta da `PROC_NOT_ALLOWED`. La ruptura se dispara en cuanto Link vuelve a un origen libre, dentro de 24 ticks; si no, `EXPIRED` sin ruptura. Nunca se sobrescribe la reacción nativa de daño.
6. **Parry.** Un parry confirmado mientras hay una solicitud pendiente la cancela (`CANCELLED_BY_PARRY`). A 100, un parry nunca rompe: +0 a Link y +40 al enemigo, sin cambios.
7. **Coexistencia con la ruptura nativa.** Si el juego entra solo en `GUARD_BREAK` (contador `field_0x2fd5` o at_spl 9/10/11) con una solicitud pendiente o con la postura saturada, se **adopta** (`NATIVE_BREAK_ADOPTED`): hay una sola ruptura, la nativa. Sin saturación solo se cuenta (`NATIVE_BREAK_OBSERVED`) y la postura no se toca.

### LNK06: vulnerabilidad y recuperación nativas

- Una observación por `mod_update` (`lnk05::Machine::observe`) sigue `mProcID` y el frame de `mUnderFrameCtrl[0]`. No hay temporizador fijo: la duración es la de la animación nativa.
- La salida de `GUARD_BREAK` se clasifica según el último frame visto:

  | Último frame | Resultado | Reinicio |
  |---|---|---|
  | `≥ 33,5` | `RECOVERED_NATIVE_END` | sí |
  | `≥ 26,5` | `RECOVERED_NATIVE_CANCEL` | sí |
  | menor | `INTERRUPTED_NATIVE_PRIORITY` (por ejemplo, Link golpeada durante la vulnerabilidad) | sí: el ciclo terminó |
  | Link muerta, perdida o distinta | `ABORTED_SAFE` | no: la identidad de la postura ya la reinicia |
  | 150 ticks activos | `STUCK_ANOMALY` | solo registro: el mod nunca fuerza la salida |

  El margen de 1,5 frames se debe a que se observa una vez por tick.
- **Reinicio único.** `Posture::break_reset()` lleva la postura a 0 una sola vez, tras la salida observada y nunca al solicitar. Se contabiliza en `break_reset_milli`, y el invariante de conservación lo incluye.
- **Regeneración retenida.** `Posture::hold()` está activa mientras la máquina está en `TRIGGER_PENDING` o `NATIVE_BREAK_ACTIVE` (`hold_ticks`). En pausa no avanza nada.
- **HUD.** `PlayerHud::break_flash()` reutiliza el pulso de saturación al entrar o adoptar. La barra baja a 0 con el reinicio.

## 3. Garantías estáticas

`ci/source_audit.py` falla si se incumple cualquiera de estas reglas:

- Solo hay una llamada a `procGuard*`: `link->procGuardBreakInit()`, dentro de `lnk05_native_break`. Su texto es exacto y verifica `mProcID`.
- `lnk05_native_break` se llama una sola vez, desde `on_link_damage_post_lnk05`, después de `if (gate != lnk05::Gate::Ok)` y solo con `TriggerPending`.
- Hay un solo `add_post<LinkDamageFix01>(on_link_damage_post_lnk05)`, y el veto de daño del mismo execute aparece con su expresión completa.
- Hay un solo `break_reset()`, condicionado a `bo.reset_posture`, y una sola `observe`, `triggered`, `request` y `parry`. La cancelación por parry va en la rama del parry confirmado.
- `lnk05_request` aparece exactamente tres veces (definición, bloqueo y directo), y la retención de la regeneración refleja solo `lb.m.hold()`.
- No se escriben `mProcID`, `field_0x2fd5`, `mModeFlg` ni `mDamageTimer` (tampoco con `|=` ni similares). No se llama a `on/offModeFlg`, `on/offNoResetFlg`, `commonProcInit` ni `setDamagePoint`.
- `lnks2_core.hpp` es puro: sin direcciones ni tipos del juego.

`ci/pe_audit.py`:
- La única importación nueva del juego es `?procGuardBreakInit@daAlink_c@@QEAAHXZ` (40 importaciones).
- Se prohíben `procGuardSlipInit`, `commonProcInit`, `setDamagePoint`, `procDamageInit` y `procCoLargeDamageInit`.
- La negativa N14 rechaza un nombre alterado.
- Hooks: HOOK_MEM 8 + HOOK_MEM_EXT 2, sin cambios.

## 4. Telemetría (nueva; la antigua se conserva)

| Línea | Cuándo |
|---|---|
| `LNK_S2_INIT` | Arranque: estado ON / OFF_HOOK_FAILED, `PROC_GUARD_BREAK`, cancelación y fin, plazos, máscara de modo |
| `LNK05_EVENT` | Solicitud, rechazo, caducidad, cancelación por parry |
| `LNK05_GATE` | Rechazo de la puerta, salvo el caso normal de `GUARD_SLIP` en espera |
| `LNK05_NATIVE_BREAK` | Entrada verificada, `TRIGGER_FAILED`, ruptura nativa adoptada u observada |
| `LNK06_EVENT` | Ventana de vulnerabilidad abierta (entrada o adopción) y `STUCK_ANOMALY` |
| `LNK06_RECOVERY` | Salida: `RECOVERED_NATIVE_CANCEL`, `RECOVERED_NATIVE_END`, `INTERRUPTED_NATIVE_PRIORITY` o `ABORTED_SAFE` |
| `LNK_S2_SUMMARY` | Contadores completos, rechazos de la puerta por motivo, `native_calls`, `hud_break_flashes`, `invariants` y presupuestos de líneas |

Cada evento lleva: episodio (Link, epoch, tick, atacante, generación, token), postura antes, después y actual, `proc`, `next_proc`, `last_frame`, cancelación 28, fin 35, `active_ticks`, `by_mod` y `reset`.

## 5. Pruebas (LAB_MODEL_ONLY)

`tests/lnks2_lab.cpp` suma 103 431 comprobaciones y usa la `lnk05::Machine`, `lnk01::Posture` y `post08::Parry`/`ArmTrack`/`LinkTrack` **reales**, conectadas como en `mod.cpp`, sobre un modelo por ticks de la ruta nativa: `checkDamageAction` con el contador de 4 bloqueos, `GUARD_SLIP`, invulnerabilidad, `procGuardBreak` con cancelación y fin, y daño durante la ruptura.

| Familia | Qué prueba |
|---|---|
| B01 | Solicitud única y sin cola; cada motivo de la puerta; entrada verificada; fallo sin efectos; espera acotada del golpe directo |
| B02 | Cancelación por parry; adopción de la ruptura nativa (pendiente o saturada); ruptura nativa solo observada; caducidad; Link sustituida |
| B03 | Clasificación de la salida (cancelación, fin, interrupción, muerte); reinicio único; pausa; atasco solo registrado; segunda ruptura tras la recuperación |
| B04 | Bloqueo que satura → una llamada nativa → postura a 100 durante la ruptura → reinicio después de la cancelación o el fin; duración 28..35; sin daño artificial; segunda ruptura; ambos órdenes de actores |
| B05 | Parry a 100 sin ruptura; parry +0; el siguiente bloqueo a 100 rompe; golpe directo que espera a la reacción nativa; coincidencia con el 4.º bloqueo nativo; Blue, Red, Black y furia; grupos |
| B06 | Lobo, nado, evento, pausa en mitad de la ruptura, muerte, cambio de sala o Link nueva |
| B07 | Barra llena sin impacto: no hay ruptura; veredictos POST08 iguales; conservación; versión y balance sin cambios; línea de log acotada |
| B08 | Barrido de 8 064 escenarios con 14 invariantes, entre ellos «idéntico bit a bit a 0.10.1 sin saturación» y «LNK05 desactivado: nada» |

**Mutaciones:**
- 35 lógicas sobre `lnks2_lab`.
- 22 negativas de código fuente sobre `source_audit.py`, incluido el núcleo impuro.
- Total: **293/293** detectadas (236 heredadas + 57 nuevas).

**Laboratorios:**
- 15 laboratorios, con 1 149 363 comprobaciones.
- Los 14 heredados suman 1 045 932, el mismo número que antes.

## 6. Riesgos residuales (para la prueba humana)

1. Los frames de cancelación y fin (28 y 35) salen de los datos const de release de HIO. Si el juego los cambiara, la clasificación cancelación/fin se desplazaría, pero el reinicio sigue ocurriendo tras la salida real.
2. **Ruptura por bloqueo:** en el orden «Link antes que el enemigo», la ruptura llega un execute después de `GUARD_SLIP`. Es posible oír o sentir el inicio del deslizamiento antes del sonido de ruptura.
3. **Ruptura por golpe directo:** espera a que termine la reacción nativa de daño (hasta 24 ticks, unos 0,8 s). Si Link no vuelve a un estado libre a tiempo (rodando, saltando), caduca sin ruptura y la barra queda a 100 hasta regenerarse.
4. La adopción de una ruptura nativa con la barra saturada reinicia la postura tras esa ruptura nativa. Es intencionado: hay una sola ruptura.
5. Una ruptura nativa sin saturación (4.º bloqueo con la barra baja) no retiene la regeneración ni reinicia la postura (comportamiento 0.10.1).
6. En el barrido, la cancelación por parry de una solicitud pendiente aparece 0 veces. Requiere un bloqueo saturante y un parry confirmado en el mismo tick; queda cubierta por B02 (máquina) y por la auditoría de código fuente, no por el modelo de combate.
