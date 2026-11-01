# POST04 — Contrato de eventos, contadores y registro

Etiquetas: **[S]** fuente · **[L]** laboratorio · **[P]** pendiente de log real. Política y pesos: `POST04_POSTURE_POLICY.md`. Arquitectura: `POST04_ARCHITECTURE_AND_LIFECYCLE.md`.
Las líneas de POST03/03.1 (`POST03_*`, `POST03_1_*`) se conservan sin cambio de contenido; solo cambia el literal de versión (`v=0.4.0`) y los topes de presupuesto (§6). El ID del módulo es `dev.posture.post04_numeric_observer`.

## 1. Líneas nuevas (todas `[INFO]`, sin punteros, sin rutas; `at=0x%08x` es una máscara de 8 dígitos)
| Línea | Campos | Cuándo |
|---|---|---|
| `POST04_INIT` | `id version source_commit policy_id passive=1 writes_to_game=0 game_actions=NONE hook_target hook_pre=HOOK_CONTINUE_ALWAYS hook_post=passive capacity=64 key=slot+generation+id max_posture threshold weights(sword/iron/all_other) recover_delay_ticks recover_period_ticks timebase=MOD_UPDATE_SIM_TICK timebase_nominal_hz=30 timebase_basis=… TIMEBASE_PAUSE_UNVERIFIED balance=PROVISIONAL log_budget_posture` | una vez, tras `POST03_1_INIT` |
| `POST04_POSTURE_BIND` | `id generation initial=0 tick reason=FIRST_OBSERVATION_NOT_SPAWN` | alta del sidecar de una generación admitida (`FIRST_SEEN` no es spawn nativo) |
| `POST04_POSTURE_HIT` | `id generation event family at eligible=CONFIRMED lethal before delta after action=APPLY\|SKIP reason tick` | un golpe confirmado: aplicado, u omitido con razón estable (las primeras 8 omisiones por razón; el resto solo en contadores) |
| `POST04_POSTURE_REGEN` | `id generation from to ticks cause tick` | **por carrera**, no por tick: se cierra al llegar a 0 (`REACHED_ZERO`), al golpear (`INTERRUPTED_BY_HIT`), congelar (`FROZEN`), morir (`DEATH_SEEN`), retirar o cerrar (`SHUTDOWN_FLUSH`) |
| `POST04_BREAK_READY` | `id generation before after=100 threshold=100 cause game_action=NONE tick` | **una** por ciclo y generación; solo diagnóstico |
| `POST04_POSTURE_RETIRE` | `id generation reason final latched dead delete_claim tick` | el ledger retiró la instancia; `delete_claim=1` solo con `LOOKUP_ABSENT_VERIFIED` |
| `POST04_SUMMARY` | contadores completos y matrices por familia (§3) | `PERIODIC` (cada 18000 llamadas, como POST03) y `SHUTDOWN` |
| `POST04_CONSERVATION` | `ok e1_consumable e2_reports e3_binds e4_threshold e5_units invariants` + magnitudes | junto a cada resumen; independiente de `POST03_CONSERVATION` |

`delta` es lo **efectivamente aplicado** tras saturar. `tick` es el contador monótono del observador (no segundos). El resumen es acumulativo (no por ventana), por lo que las líneas periódicas no se suman entre sí.

## 2. Razones de omisión (mutuamente excluyentes; orden en la política §2)
`STALE_GENERATION · NOT_ADMITTED_OR_UNBOUND · ACTOR_DEAD · LETHAL · UNKNOWN_FAMILY · AMBIGUOUS · ZERO_WEIGHT_POLICY · FROZEN_UNVERIFIED · BREAK_READY_LATCHED`. Separadas, además, de los informes que no son golpes confirmados: `finish_events` y `not_confirmed`.
`E_OC2` y `PROFILE_OTHER` nunca generan informe (el observador no los detalla): se cuentan como `excluded_generations` (una vez por generación) y jamás reciben sidecar.

## 3. Contadores
Entrada: `consume_calls dup_consume_calls reports_new finish not_confirmed confirmed_consumable weighted skipped(9) fam_confirmed(11) fam_weighted(sword/iron)`.
Sidecar: `binds rebinds retired latched_retired death_closed excluded_generations divergence_repairs` y estado actual `bound_now latched_now dead_now frozen_now`.
Umbral y unidades: `crossings saturations units(added/recovered/closed/live) regen_runs freeze_thaw frozen_entry_ticks latched_entry_ticks ticks`.
Invariantes (deben ser 0): `underflow overflow generation_leak multi_consume`. Registro: `ring_dropped log(written/dropped)`.

## 4. Ecuaciones de conservación (`POST04_CONSERVATION`)
- **E1** `confirmed_consumable = weighted + Σ skipped[9]`.
- **E2** `reports_new = finish + not_confirmed + confirmed_consumable` y `consume_calls = reports_new + dup_consume_calls`.
- **E3** `binds = retired + bound_now`, `bound_now ≤ 64`, `rebinds ≤ binds`.
- **E4** `crossings ≤ weighted` y `crossings = latched_now + latched_retired` (un cruce por ciclo, ninguno perdido ni duplicado).
- **E5** `units_added = units_recovered + units_closed + units_live` (toda unidad añadida se recupera, se cierra al retirar o sigue viva).
- **Invariantes** `underflow = overflow = generation_leak = multi_consume = 0`.
`ok = E1 ∧ E2 ∧ E3 ∧ E4 ∧ E5 ∧ invariantes`. Independiente de `POST03_CONSERVATION` (que sigue exigiendo `pending=0`). Además, `POST04.confirmed_consumable` debe coincidir con `POST03.confirmed` y `POST04.finish` con `POST03.finish`: el extractor lo comprueba [L].

## 5. Clave y aislamiento
La clave válida es `slot + generation + id`. La generación es un contador `uint64_t` global y monótono del ledger (única por creación); el sidecar compara además `slot` e `id`. No se guarda ningún puntero a actor ni a collider: el sidecar no contiene `uintptr_t`. Una generación nueva nunca hereda `P`, `k`, latch ni contadores individuales (`generation_leak` lo vigila). Con el ledger lleno (64 vivos) un candidato nuevo se rechaza de forma explícita (`capacity_drops`) y no recibe sidecar ni expulsa a un vivo.

## 6. Presupuesto de log
El techo global por sesión sigue siendo **2000 líneas**: observador 1500 (vida 450, golpes 700, otros 250, resumen 100; antes 600/1000/300/100) + postura 500 (con topes por tipo: bind 120, hit 250, regen 100, break 50, retire 120). No hay líneas por tick ni por frame; las métricas no se pierden en los resúmenes aunque se agote el presupuesto de líneas.

## 7. Qué NO significa
`HIT_CONFIRMED` ≠ HP perdido. `POST04_BREAK_READY` ≠ derribo. `family=OTHER_VERIFIED` ≠ arma conocida (y `at=0x00080000` no es «bomba»). `FIRST_SEEN` ≠ spawn. La muerte observada ≠ borrado. Ninguna cifra de postura se deriva de HM ni de la cantidad de daño.
