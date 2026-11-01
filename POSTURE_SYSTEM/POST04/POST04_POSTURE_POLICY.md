# POST04 — Política de postura (TEST, PROVISIONAL)

Etiquetas: **[S]** fuente · **[C]** MSVC/CI · **[L]** laboratorio con dobles · **[R]** log real · **[P]** pendiente.
**Los números de este documento (25 / 50 / 100 / 120 / 6) son una política de laboratorio, no un balance aprobado.** POST09 decidirá la política jugable. Nada aquí garantiza que un Bokoblin normal de 40 HP llegue al umbral antes de morir, ni que lo contrario sea deseable.
El sistema matemático (acumulación, tope, retardo, recuperación, cruce de umbral, aislamiento por generación) sí es lo que POST04 implementa y valida; los valores viven en un único bloque `post04::policy` de `src/posture_core.hpp` (constantes `constexpr`, sin números mágicos dispersos).

## 1. Unidades y tabla de pesos
Unidad interna: `posture_units` enteras (`uint8_t`), `0 ≤ P ≤ 100`. Una generación nueva empieza en `P = 0`.

| Familia confirmada (`HIT_CONFIRMED`, lectura de tipo válida) | Peso | Nota |
|---|---|---|
| `SWORD` | **+25** | no letal; el HP perdido no interviene |
| `IRON_BALL` | **+50** | no letal |
| `BOOMERANG` | **+0** | excluido expresamente aunque sea `HIT_CONFIRMED` (en B1 hubo uno con `hp=55>55`) |
| `OTHER_VERIFIED` (p. ej. `at=0x00080000`), `SHIELD_ATTACK`, `ARROW`, `BOMB`, `AT_TYPE_40`, `SLINGSHOT` | +0 por defecto | sin política confirmada; **no** significa «mala»: quedan abiertas para POST09 |
| `AMBIGUOUS`, `UNAVAILABLE` | +0 | jamás se reducen a `SWORD` (ni siquiera por `native_first`) |
| `FINISH_NATIVE_OBSERVED`, `FINISH_UNEXPECTED_STATE`, `HIT_PROCESSED_SIGNATURE_MISMATCH`, `HIT_CANDIDATE_NOT_PROCESSED`, cooldown/sin TG, `E_OC2`, `UNKNOWN_UNSAFE` | +0 | no son impactos confirmados consumibles |

Reglas que **no** cambian el peso: la cantidad de HP perdido (con HM ×2 o sin él), el subtipo de espada, la fuerza del ataque y el origen Blue: el gancho no los conoce. Un `SWORD` confirmado y no letal con `hp_delta = 0` sigue sumando +25.

## 2. Elegibilidad de un evento (orden de evaluación; exactamente UNA salida)
Cada informe de impacto del observador de POST03.1 se consume **una sola vez** (por número de evento):
1. Informe repetido (mismo evento o anterior): `dup_consume_calls`, no cuenta como evento nuevo.
2. `FINISH_*` → `finish_events` (nunca pesa; no es un golpe).
3. Cualquier otro `kind` distinto de `HIT_CONFIRMED`, o `eligible ≠ CONFIRMED` → `not_confirmed`.
4. `HIT_CONFIRMED` → `confirmed_consumable` y **una** de estas salidas, por este orden:

| # | Salida | Condición |
|---|---|---|
| 1 | `STALE_GENERATION` | `slot/generation/id` ya no son vigentes en el ledger |
| 2 | `NOT_ADMITTED_OR_UNBOUND` | instancia viva sin sidecar (excluida, aún no admitida o fuera de cupo) |
| 3 | `ACTOR_DEAD` | la entrada ya estaba cerrada por muerte vista |
| 4 | `LETHAL` | este golpe es letal: `lethal=1`, o HP POST ≤ 0, o el ledger ya vio la muerte (la muerte prevalece sobre cualquier ruptura) |
| 5 | `UNKNOWN_FAMILY` | sin lectura fiable del tipo AT |
| 6 | `AMBIGUOUS` | varios grupos de bits |
| 7 | `ZERO_WEIGHT_POLICY` | familia fiable sin peso (OTHER_VERIFIED, BOOMERANG, …) |
| 8 | `FROZEN_UNVERIFIED` | instancia no verificada o `UNKNOWN_UNSAFE`: sin acumulación |
| 9 | `BREAK_READY_LATCHED` | ya marcó el umbral: acumulación congelada |
| — | **`WEIGHTED`** | ninguna de las anteriores |

## 3. Acumulación y umbral
`P' = min(100, P + w)`. Si `P < 100` y `P' = 100` hay **un** cruce: `latched = 1`, `crossings++`, una línea `POST04_BREAK_READY … game_action=NONE`. `delta` registrado = unidades **efectivamente aplicadas** tras saturar (`99 → 100` con peso 25 da `delta = 1`; `saturations++` cuando se recortó).
Tras el latch la entrada queda congelada hasta su retiro o muerte: no acumula ni se recupera. **Es una decisión matemática provisional** para conservar un marcador consumible por POST06; **no** representa la recuperación tras un derribo real ni implementa una API de cambio de modo. `POST04_BREAK_READY` es solo una línea de diagnóstico: ningún código de POST04 reacciona a ella ni la transfiere a otra generación.

## 4. Tiempo y recuperación (ticks del observador)
- **Tick** = un `mod_update` = un `advance()`. Se cuenta con un contador `uint64_t` propio (`now`) y un sello `adv_seq` con protección de wrap; **no** es el contador de barridos de existencia (que cuenta cada 10 `mod_update`) ni una llamada al gancho.
- Orden dentro del cuadro: `mod_update` (barrido de existencia opcional → sincronizar ledger → `advance()`) **antes** de `fpcM_Management`, donde corre `damage_check`. Un golpe del cuadro N se sella con el tick N; el primer `advance()` posterior (N+1) cuenta `k = 1`. El propio tick del golpe nunca recupera.
- `k` = ticks **elegibles** desde el último golpe ponderado. Un tick es elegible solo si la entrada está viva, admitida (`E_OC_CANDIDATE`), verificada, no latched y con `P > 0`.
- Recuperación: `unidades recuperadas = (k > 120) ? (k − 120) / 6 : 0`, aplicada de una en una (`k > 120 ∧ (k − 120) mod 6 = 0` ⇒ `P ← P − 1`).

| k (ticks elegibles) | 119 | 120 | 121 | 125 | **126** | 127 | 131 | **132** |
|---|---|---|---|---|---|---|---|---|
| unidades recuperadas | 0 | 0 | 0 | 0 | **1** | 1 | 1 | **2** |

  Desde `P = 25` se llega a 0 en `k = 270`; desde 100 (si no hubiera latch) harían falta 720 ticks. Un nuevo golpe ponderado pone `k = 0` (reinicia el retardo). Nunca hay `P < 0` (la guarda `P = 0 ⇒ sin recuperación` y un `uint8_t` hacen visible cualquier underflow en la auditoría).
- **Congelación** (instancia `UNKNOWN_UNSAFE`, p. ej. un `AtAtp` transitorio de Blue, o no verificada): `k` y `P` se **detienen** (pausa, no reinicio). Al revalidar se continúa donde se dejó: **no** se aplican de golpe los ticks transcurridos congelados. La identidad se conserva (`identity=KEPT`).
- Muerte vista (`DEATH_SEEN`): la entrada se cierra (no acumula ni recupera) pero **no** se retira ni se afirma borrado. Retiro (`RETIRED`): solo `LOOKUP_ABSENT_VERIFIED` lleva `delete_claim = 1`.

## 5. Base de tiempo: lo que se sabe y lo que no
- **[S]** `mod_update` se invoca desde `ModLoader::tick()`, llamado por `duskExecute()` dentro de `fapGm_Execute()` (`f_ap_game.cpp`), una vez por **tick de simulación** del reloj del juego; el bucle principal (`m_Do_main.cpp`) ejecuta `numSimTicks` por cuadro de render según `dusk::game_clock`, con `kSimPeriod = 1/30 s` (`game_clock.h`) a escala 1. Puede haber 0, 1 o varios ticks por cuadro renderizado, y la escala de tiempo del anfitrión es modificable.
- **[R]** Respaldo de B1: las 27 ventanas `PERF_WINDOW` de Expansion suman 8100 ticks en 270,6 s (media 33,41 ms por tick, ≈29,9 ticks/s; medias por ventana 33,3–35,6 ms; un intervalo máximo de 778 ms en una ventana, sin atribuirle causa). Es la medición de otro mod; no es un perfil de POST04.
- Por tanto 120 ticks ≈ 4,0 s y 6 ticks ≈ 0,2 s **solo a escala 1 y sin cargas**. **No se afirma «60 FPS» ni segundos fijos.**
- **`TIMEBASE_PAUSE_UNVERIFIED`**: `fapGm_Execute` no está condicionado a la pausa de los actores, así que `mod_update` (y la recuperación) pueden seguir avanzando con un menú o pantalla de pausa abiertos mientras `damage_check` no se invoca. No se puede declarar correcto ni incorrecto sin una prueba real; no se añaden hooks ni lecturas para detectarlo. Un cambio de escena retira las instancias por la vía del ledger (sin recuperación de actores retirados).

## 6. Qué predice esta política sobre los eventos reales (A1/B1, solo acumulación) [L]
Repetición de los 36 eventos reales saneados por el núcleo (`posture_lab`, T29); la decisión esperada la calcula un generador independiente (`tests/gen_real_trace.py`). Los logs no registran ticks, así que **no** valida la recuperación.

| Sesión | Ponderados | Omitidos | Cruces |
|---|---|---|---|
| A1 (sin HM; actores de 40 HP) | 0 | 8 `LETHAL`, 4 `ZERO_WEIGHT_POLICY` (OTHER_VERIFIED) | 0 |
| B1 (con HM; actores de 187–220 HP) | 12 | 6 `BREAK_READY_LATCHED`, 2 `ZERO_WEIGHT_POLICY` (OTHER_VERIFIED y BOOMERANG), 1 `LETHAL`, 3 Finish | 3 (161/8, 162/9, 868/18), 1 saturación |

Lectura honesta: con actores de 40 HP la política **no se alcanza** (mueren antes: en A1 los únicos impactos no letales fueron `OTHER_VERIFIED`); con los HP de HM, 3 de 4 actores golpeados alcanzan el umbral. Esto es un dato del conjunto de pruebas, no un criterio de aceptación de POST04.
