# POST06 0.6.0 — ruptura real, castigo x1,20 fijo, derribo nativo, Finish nativo y rearme

Etiquetas: **[S]** fuente exacta · **[B]** binario `dusklight.exe` 2.0.3 · **[L]** laboratorio · **[C]** CI/PE · **[R]** observación del usuario · **[P]** pendiente de prueba humana.

## Base y ramas
- **Base:** POST05 0.5.4, fuente compilada `3053a75113024335cf583ed14474ddc2a4a62839` (rama `feature/posture-post05-general-anti-stagger`, documentos `4a85810`). El usuario la validó con 8 mods [R].
- **Rama nueva:** `feature/posture-post06-break-punish`, creada desde `4a85810`. La rama 0.5.4, su `.dusk` y su CI no se tocan.
- **Paquete:** el código sigue en `POSTURE_SYSTEM/POST05/` (mismo paquete, mismo ID `dev.posture.post05_selective_reactions`, versión **0.6.0**), así que POST05 y POST06 no pueden cargarse a la vez. Esta carpeta solo contiene documentación.

## Cadena nativa que se reutiliza [S] (`d_a_e_oc.cpp`)
- **`damage_check`** se llama **una vez por ejecución** del actor, al inicio de `action()` (:2415-2418). Allí corren `cc_at_check` (vida), la rama letal (`health <= 1` ⇒ `attention_info.flags = 0` y BIG_DAMAGE) y `setActionMode(DAMAGE|BIG_DAMAGE)`.
- **`executeDamage`** (:1534-1602): tambaleo; al terminar, `FIND 0` (o `MOVE_OUT`).
- **`executeBigDamage`** (:1603-1724):
  - **0..2:** `offTgSph`, impulso y voz.
  - **3:** vuelo.
  - **4:** aterrizaje; si `health < 1`, pasa a DEATH.
  - **5:** `onDownFlg`, `setStabPos`, `field_0x6c0 = 35..55`. Ahí está el Finish (`CUT_TYPE_DOWN`; `damage_check` → `checkCutDownHitFlg` → DEATH).
  - **6:** `offDownFlg` y animación de levantarse.
  - **Al terminar:** `setActionMode(FIND, 5)`.

## Respuestas a las preguntas A–G
- **A. Instante de ruptura.** Es el `crossed` de POST04 (golpe ponderado con postura antes < 100 y después ≥ 100). Es único por ciclo gracias al latch y va ligado al token slot + generación + id del ledger.
  - POST06 reinicia su estado si cambia la generación o el id.
  - Un latch visto sin el cruce (p. ej. el mod cargado a mitad de ciclo) abre el castigo desde ese momento, para no dejar la postura enganchada para siempre.
- **B. Derribo ya en marcha.** Se observa el modo o estado **final** de cada llamada. Si es BIG_DAMAGE (giro, 4.º corte, salto, letal…), la fase pasa directamente a FALLING y POST06 no escribe nada.
- **C. Caída al vencer el castigo.** Se escribe **exactamente** el resultado de `setActionMode(BIG_DAMAGE, 0)`: modo 6, estado 0, modo previo = actual, timers 0, bits Tg/Co activos y HeadLock fuera.
  - Ocurre en el POST de `damage_check`, el mismo punto donde el juego la llama. `executeBigDamage` hace todo lo demás en ese mismo tick.
  - Sin daño, sin `cc_at_check`, sin SE de impacto, sin postura.
  - Es el mismo escritor verificado de 0.5.4, con offsets comprobados en el EXE [B].
  - La dirección del salto es la de `mAtInfo.mHitDirection`, que el juego guardó en el último golpe.
  - Solo se escribe en un tick sin golpe y desde un modo desde el que el nativo también puede entrar en BIG_DAMAGE. Si no hay punto seguro durante 60 ejecuciones (2 s), el ciclo se aborta y la postura se rearma sin caída falsa.
- **D. Suelo, levantamiento y control.** BIG 5 es DOWN_FINISH y BIG 6 es GETTING_UP.
  - **El rearme ocurre solo cuando el actor sale vivo de BIG_DAMAGE**, en la llamada siguiente a `setActionMode(FIND, 5)`: control normal confirmado.
  - Durante FALLING, DOWN y GETTING_UP la postura sigue enganchada en 100, sin recuperación.
  - DEATH (Finish o muerte) cierra el ciclo sin escribir.
- **E. x1,20.** POST06 compara la vida PRE y POST de la **misma** llamada a `damage_check`, que es el daño efectivo final.
  - Enemy Health Multiplier CP11 aplica su escalado **dentro** de `cc_at_check` (pre-compensación, verificada en su propio POST de `cc_at_check`, `hm_203/core8/src/mod.cpp`) [S]. Por eso la diferencia observada ya incluye HM y el +20 % se calcula una sola vez sobre ese efectivo, sin doble escalado.
  - **Regla de redondeo:** acumulador de quintos por actor y castigo: `frac += base; extra = frac / 5; frac %= 5`. Daño 10 → 12, 12, 12; daño 3 ×5 → +0, +1, +0, +1, +1 = +3 (20 %). Nunca se acumula un multiplicador.
  - **Solo espadazos confirmados de Link** (familia ESPADA verificada por el collider procesado de POST03.1), con daño real (> 0) y no letal en nativo.
  - **Nunca:** el golpe de ruptura, el Finish, ni flecha, escudo, bumerán, bola o bomba.
  - **Si el +20 % lo vuelve letal:** misma rama letal que `damage_check`: `attention_info.flags = 0` y BIG_DAMAGE 0. Muere al aterrizar con la lógica nativa.
  - **Escritor nuevo y acotado `write_vitality`:** solo `health` (+0x656) y, en la rama letal, `attention_info.flags` (+0x650, verificado en el EXE: `cmpw $0x1,0x656(%rbx); jg …; mov %esi,0x650(%rbx)` en 0x140e065bd) [B]. Hace relectura previa y verificación posterior.
- **F. Vida máxima.** Es el **máximo observado de la misma generación** (vida PRE/POST en cada llamada).
  - Expansion escribe la vida de variante en su PRE de `execute`, antes del primer `damage_check` [S]. HM no cambia la vida máxima: escala el daño.
  - Si el máximo es desconocido o incoherente, la tasa es la base de 5/s (fallback).
  - El robo de vida o la regeneración del Red suben el porcentaje, y la recuperación de postura se acelera según la banda.
- **G. Tiempo.** El castigo usa **ejecuciones propias del actor**: 30 = 1 s y 90 = 3 s a 30 Hz de simulación. No avanza en pausa, menús ni cambio de sala.
  - La recuperación de postura sigue en el reloj de POST04 (`mod_update`, 120 ticks de retardo) con un acumulador exacto de *rate* puntos cada 30 ticks.
  - **Límite heredado:** ese reloj de `mod_update` no se ha verificado en pausa (`TIMEBASE_PAUSE_UNVERIFIED`, POST04).

## Máquina de estados (`src/break_core.hpp`, por actor y generación)
| Fase | Entrada | Comportamiento | Salida |
|---|---|---|---|
| TRACKING | inicio / rearme | POST05 0.5.4: sin tambaleo por debajo de 100 | cruce a 100: PUNISH, o FALLING si la reacción nativa ya es BIG |
| BROKEN_PUNISH | ruptura de pie | reacciones **nativas**; espadazos ×1,20 fijo; latch 100 | BIG nativo, o caída por 30 ejecuciones sin espadazo o 90 desde la ruptura |
| FALLING | caída nativa (propia o de POST06) | nativo | BIG 5 → DOWN; DEATH → DEAD |
| DOWN_FINISH | BIG 5 | Finish nativo disponible | BIG 6 → GETTING_UP; Finish → DEAD |
| GETTING_UP | BIG 6 | nativo; **sin rearme** | sale vivo de BIG (FIND 5): **REARM → postura 0** |
| DEAD | DEATH / vida 0 | nada | generación nueva |

## Recuperación de postura por vida (`posture_core.hpp`)
- **Tasa por banda:** más de 75 % → 5/s; más de 50 % → 4; más de 25 % → 3; más de 10 % → 2; más de 0 → 1. La comparación es exacta (`hp*100 > X*max`).
- **Cómo avanza:** tras 120 ticks elegibles se acumula *rate* por tick y se recupera 1 punto cada 30 acumulados. Con 5/s coincide exactamente con el periodo 6 de POST04: `posture_lab` conserva sus conteos.
- **Sin cambios en los pesos:** espada +25 y bola +50.

## Escrituras al juego (todas en el POST de `damage_check`, del actor de esa llamada)
| Escritor | Campos | Cuándo |
|---|---|---|
| `restore_reaction` (0.5.4) | modo, estado, previo, timers, HeadLock, bits Tg/Co | supresión POST05 por debajo de 100; **caída** POST06 (= `setActionMode(BIG_DAMAGE, 0)`); conversión letal (modo 6/0) |
| `write_vitality` (nuevo) | `health`; `attention_info.flags = 0` solo en la rama letal | bonus ×1,20 de POST06 |

Mismo hook único (`daE_OC_c::damage_check`), PRE siempre `HOOK_CONTINUE`, sin imports nuevos, sin HUD, sin sonidos ni efectos nuevos. Las animaciones, sonidos, caída, Finish y levantamiento son los nativos.

## Pruebas [L]
- **`break_lab`** (nuevo, motor completo en el orden de `mod.cpp` sobre un modelo nativo de `damage_check` + `executeDamage` + `executeBigDamage`):
  - ciclo completo con 3 golpes sin tambaleo, ruptura sin bonus, 12/12/12, caída exacta a 30 ejecuciones, suelo, levantamiento, rearme a 0 solo tras FIND y segunda ruptura;
  - techo de 3 s (caída en la ejecución 90, o 91 si la 90 trae un golpe);
  - derribo nativo en la ruptura o en el castigo (sin segunda caída);
  - bonus letal, que muere al aterrizar con la rama letal nativa;
  - Finish nativo en el suelo, sin rearme;
  - flecha sin bonus ni renovación;
  - fracciones (daño 1/2/3/4/5/10);
  - bandas 5/4/3/2/1 exactas sin deriva, con sus límites;
  - modo sin punto seguro → aborto a los 2 s;
  - reciclado de id;
  - gemelo sin POST06: en el castigo solo cambia la vida, exactamente en el +20 %;
  - varios actores;
  - escritura que no verifica (sin cambio de fase, aborto por límite).
- **Labs heredados:** hit/lifecycle/collider/posture/reaction/compat/rb/general con sus conteos.

## CI y binario [C][B]
- **Run:** https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41376998495. `build` e `independent-download` en éxito al primer intento.
- **Origen del build:** espejo `ci/posture-post06-break-punish` @ `3b17ac8762ebba250ffba891009f0e4e9634e15a`; fuente compilada `a0a81535639459275702371324448e96a5d17575`; libro de control de 43 archivos.
- **Compilador y labs:** MSVC 19.51. Los 9 labs dan los mismos conteos que con g++.
- **Auditorías:** `SOURCE_AUDIT_PASS` (reglas nuevas de `write_vitality` y de los tres sitios de `restore_reaction`), `PE_AUDIT_PASS` y 11/11 negativas PE.
- **Imports y exports:** los mismos 3 imports del juego y los mismos 5 exports.
- **Descarga:** https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41376998495/artifacts/13111921457 (ZIP `POST06_TEST_41376998495_1`, 42960 bytes, `c1aef421…a9e3`).
- **`.dusk`:** `POSTURE_POST06_0_BREAK_PRIVATE_TEST_windows-amd64_a0a815356394.dusk`, **41519 bytes**, SHA-256 **`fcc61396736c38591d4bca803386d975427a09cc3f30e7d026ad177bd504e94e`**. Caduca el 2026-12-02 02:20 UTC.
- **DLL:** 83456 bytes, `89065ad66ff619c70fc16d551969e71eedd311ab19c04b04ac948de9fda64042`. `mod.json` es idéntico al de la fuente.
- **Descarga independiente por ID:** coincide con el digest y con `SHA256SUMS`. El job lo marca `ARTIFACT_DOWNLOADED_VERIFIED`.
- **DLL descargada:**
  - **Caída de POST06** (0x18000c3ef–435): `0x8cc ← modo`, `0x8c8 ← 6`, u32 `0x8e0 ← 0`, `and $0xff7f` en `0x69a`, `0x8d0 ← 0` y `orl $1` en `0xce8/0xd08/0xea0/0xec0`. Es la misma secuencia que `setActionMode` del EXE (0x140e0d260). La máscara de modos compilada, `0x181bb`, es {0,1,3,4,5,7,8,15,16}.
  - **Bonus:** solo `mov %si,0x656` (vida) y `movl $0,0x650` (atención, en la rama letal).
  - **Restauración de 0.5.4:** sin cambios.
  - 0 stores a cooldown, `mName`, `mAtInfo`, `mpMorf`, `speedF` o AtAtp.

## Matriz de requisitos
| Requisito | Estado |
|---|---|
| Por debajo de 100, sin tambaleo (0.5.4) | IMPLEMENTED, LAB_PASS, CI_PASS; 0.5.4 visto por el usuario [R]; 0.6.0 HUMAN_RUNTIME_PENDING |
| Ruptura única por ciclo | IMPLEMENTED, LAB_PASS, CI_PASS, HUMAN_RUNTIME_PENDING |
| Castigo con reacciones nativas | IMPLEMENTED, LAB_PASS, CI_PASS, HUMAN_RUNTIME_PENDING |
| x1,20 fijo en espadazos (no en la ruptura, Finish ni otras familias) | IMPLEMENTED, LAB_PASS (12/12/12, fracciones, letal), CI_PASS, HUMAN_RUNTIME_PENDING |
| Caída a 1 s sin espadazo / 3 s máximo | IMPLEMENTED, LAB_PASS, CI_PASS, HUMAN_RUNTIME_PENDING |
| Derribo nativo previo sin doble caída | IMPLEMENTED, LAB_PASS, CI_PASS, HUMAN_RUNTIME_PENDING |
| Finish nativo en el suelo | sin escrituras de POST06 (nativo); LAB_PASS en el modelo; HUMAN_RUNTIME_PENDING |
| Levantamiento nativo y rearme solo tras FIND | IMPLEMENTED, LAB_PASS, CI_PASS, HUMAN_RUNTIME_PENDING |
| Recuperación 5/4/3/2/1 por banda de vida | IMPLEMENTED, LAB_PASS (exacta), CI_PASS, HUMAN_RUNTIME_PENDING |
| Sin HUD ni efectos o sonidos nuevos | cumplido |
| Expansion (x2, cadena, chip, robo de vida) | sin cambios de contrato con Expansion; HUMAN_RUNTIME_PENDING. Límite x2 de 0.5.4 sin empeorar |

## Lo que no se puede saber sin jugar [P]
- Que la caída provocada por POST06 se vea como la nativa: es la misma rama de BIG_DAMAGE, pero la dirección del salto es la del último golpe.
- Que el Finish aparezca y funcione en el suelo.
- Que el levantamiento y la vuelta a la persecución se vean normales.
- Que la vida y las barras (HM y Bars) cuadren con el +20 %.
- El audio y los FPS.

## Pendiente / límites
1. **x2 de Expansion:** sigue el límite de 0.5.4 (golpes en el tick de arranque o en el frame 1 de un x2). POST06 no lo empeora: durante el castigo, las reacciones son nativas.
2. **Reloj de recuperación de POST04:** se mantiene; su comportamiento en pausa no está verificado.
3. **Bumerán y escudo:** siguen sin aturdir por debajo de 100 (decisión de 0.5.4).
