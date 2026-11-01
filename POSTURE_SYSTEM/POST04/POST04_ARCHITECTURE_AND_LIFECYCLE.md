# POST04 — Arquitectura y ciclo de vida

Etiquetas: **[S]** fuente · **[C]** MSVC/CI · **[L]** laboratorio · **[P]** pendiente de log real.

## 1. Capas y responsabilidades
```
  juego (daE_OC_c::damage_check)                         ← único hook; PRE siempre HOOK_CONTINUE, POST pasivo
        │ valores por copia (PreReads / PostReads)
        ▼
  POST02  ledger de 64 slots: (id, ptr opaco, generation), vida, admisión          [identidad / ciclo de vida]
  POST03  engine: un evento por procesamiento, dedup por serial, veredicto          [detección / clasificación]
  POST03.1 colisionador: igualdad con el hit obj crudo + alineación 4, UNA lectura  [familia nativa]
        │ HitReport {event, slot, id, generation, kind, elig, lethal, at, family, life, post.health}
        ▼
  POST04  Posture (sidecar de 64 entradas) ← consume cada HitReport UNA vez         [matemática pasiva]
        │ cola de 128 PItem  →  mod.cpp formatea y registra (presupuesto 500 líneas)
        ▼
  logs  (POST04_*)                 POST05–08 (futuros consumidores): PROHIBIDOS aquí
```
`src/posture_core.hpp` es lógica **pura**: incluye solo la biblioteca estándar y `engine.hpp`; no contiene ningún puntero a actor ni a collider (el auditor de fuente lo comprueba) ni asigna memoria. `mod.cpp` solo lee el juego, pasa valores y escribe líneas de log.

## 2. Cambios respecto al código compilado de POST03.1 (`cab6778`)
| Archivo | Cambio |
|---|---|
| `src/lifecycle_core.hpp` | `kModVersion = "0.4.0"`; literal `v=0.4.0` en los formateadores; presupuesto de log del observador 1500 (450/700/250/100) para dejar 500 a la postura sin superar 2000 en total; `HitReport.slot` (el consumidor ubica la entrada sin buscar por ID) |
| `src/engine.hpp` | una línea: `rep.slot = fr.slot;` |
| `src/hit_core.hpp` | sin cambios |
| `src/posture_core.hpp` | **nuevo**: política, sidecar, `PostureEngine`, formateadores |
| `src/mod.cpp` | envoltura `PostureEngine`; `drain_posture()`; `POST04_INIT`; el tick matemático en `do_update`; cierre ordenado; ID/nombres |
| `tests/` | `hit_lab`, `lifecycle_lab`, `collider_lab` heredados (dos aserciones de contrato actualizadas: presupuesto 1500 y `v=0.4.0`; mismos 1660 / 29558 / 12826 comprobaciones que en POST03.1); `posture_lab` nuevo |

## 3. Sidecar de postura
- **Estructura:** `Entry ent_[64]` paralelo al ledger. Entrada = `{bound, latched, dead, frozen, in_run, posture(u8), id, generation(u64), k, last_hit_tick, last_applied_event, last_adv_seq, …}`. Memoria fija O(64); sin heap, sin locks, sin E/S en el gancho.
- **Clave:** `slot + generation + id`. La generación del ledger es global y monótona (única por vida); el sidecar guarda además `handled_gen_[slot]` para no volver a ligar una generación ya cerrada.
- **Estado derivado** (`PState`): `UNBOUND`, `TRACKING`, `BREAK_READY_LATCHED`, `FROZEN_UNVERIFIED`, `INACTIVE_DEATH`. Prioridad de lectura: muerto › congelado › latched › en seguimiento. **La fuente de verdad de la validez es el ledger**; el enum solo la refleja y se re-sincroniza.
- **Alta:** al sincronizar, un slot con instancia viva, `adm = E_OC_CANDIDATE` y generación aún no tratada recibe una entrada con `P = 0`, `k = 0`, sin latch. Si la admisión es `E_OC2_EXCLUDED`/`PROFILE_OTHER` la generación se marca como tratada **sin** sidecar (`excluded_generations`). Si es `UNKNOWN_UNSAFE` se espera a que pase a candidata.
- **Retiro:** si el ledger la retira, el slot se reutiliza, o la admisión pasa a excluida, la entrada se cierra (`units_closed += P`), se emite `POST04_POSTURE_RETIRE` y se vuelve a `Entry{}`. `delete_claim` solo con `LOOKUP_ABSENT_VERIFIED`. Un slot reutilizado antes de sincronizar se repara y se cuenta (`divergence_repairs`); nunca se hereda estado.
- **Capacidad:** el sidecar nunca supera al ledger (64). Con 64 vivos, el 65.º candidato lo rechaza el ledger (`capacity_drops`); sin sidecar, sin expulsar a un vivo.

## 4. Orden de operaciones
Por cuadro de simulación [S]: `duskExecute()` → `mod_update` → `fpcM_Management` (actores, `damage_check`).
- **`mod_update`** (`do_update`): época de contexto → barrido de existencia (solo cada 10 llamadas, cuota 2, `fopAcM_SearchByID` en `lookup_actor`) → `g.pe.on_update()` = `sync(ledger)` + `advance()` (**un** tick por llamada, **después** del barrido: una retirada no recupera en ese tick).
- **Gancho PRE** (`on_pre`): observa y, si el ledger cambió (alta, cambio de admisión, retiros), `sync`.
- **Gancho POST** (`on_post`): cierra el frame del observador; si hay informe, `consume` **antes** de sincronizar la muerte de ese mismo golpe (así un golpe letal se omite como `LETHAL` y no como `ACTOR_DEAD`); luego `sync`.
- **Disabled / fallo de gancho / excepción:** `PostureEngine` es inerte si el observador está deshabilitado (`on_pre/on_post/on_update` vuelven de inmediato): no acumula ni avanza el reloj. Un fallo de instalación deja los callbacks sin efecto y el original sigue.
- **`mod_shutdown`:** `on_shutdown()` (sync + cierre de carreras abiertas, solo aritmética) → resumen. No se consulta ni se desreferencia ninguna instancia.

### Auditoría del orden `do_update` / `emit_summary` / reloj (exigida por el encargo)
Texto de `mod_update` en `src/mod.cpp`: `emit_disabled_once()` → si el observador está deshabilitado, **sale** (ni barre ni avanza el reloj) → `do_update()` → `if (summary_due()) emit_summary("PERIODIC")`.
- `do_update()`: (1) `epoch.update(...)`; (2) `if (sweep_due())` → barrido (cuota 2, `fopAcM_SearchByID`); (3) **siempre** `g.pe.on_update()` = `sync` + `advance()`; (4) `drain_posture()`.
- `sweep_due()` incrementa **su propio** contador `tick` y devuelve `true` cada 10 llamadas. Ese contador **no** es el reloj de postura: el reloj es `Posture::now_` y se incrementa en `advance()`, incondicionalmente, una vez por `mod_update`. Un barrido irregular o un cupo agotado no omite ni multiplica unidades de recuperación (T20: el ritmo con 1 y con 20 actores es idéntico).
- `summary_due()` depende de `calls` (llamadas al gancho), no del reloj; el resumen se emite **después** del tick de esa llamada, de modo que `audit()` ve el estado ya sincronizado y avanzado. Los resúmenes son acumulativos: ninguna línea periódica suma dos veces.
- En `mod_shutdown`: `on_shutdown()` (sync + cierre de carreras) → `drain_posture()` → `emit_summary("SHUTDOWN")`; el `audit()` del resumen no desreferencia nada.

## 5. Coste y límites
Gancho: sin trabajo extra en las llamadas sin golpe (excepto `sync` O(64) cuando el ledger cambió); un golpe confirmado cuesta un `consume` O(1). `mod_update`: `sync` + `advance` = 2 × O(64) aritmética por tick, sin lecturas del juego. Estructuras fijas: ledger 64 + sidecar 64 + cola 128 + contadores. Sin consultas `fopAcM_SearchByID` adicionales (siguen siendo ≤ 2 cada 10 `mod_update`). El rendimiento real **no está medido** [P].

## 6. Garantías de pasividad (auditadas)
Un solo `DEFINE_HOOK` (`daE_OC_c::damage_check`), un `add_pre` y un `add_post`; PRE siempre `HOOK_CONTINUE`; ningún `HOOK_SKIP_ORIGINAL`; ninguna escritura por puntero del juego; una sola desreferencia (`GetAtType`, 4 bytes) tras `HIT_CONFIRMED` con igualdad frente al hit obj crudo y alineación 4; sin `IsBadReadPtr`/`VirtualQuery`/SEH; sin importar servicios de HM/Bars/DEVF/Expansion (solo Host/Log/Hook); sin memoria dinámica, E/S, red ni hilos; imports de `dusklight.exe` = los mismos 3 de POST03.1.

## 7. Lo que POST04 no hace
No suprime reacciones, no derriba, no provoca Finish, no dibuja HUD, no cambia HP/IA/colisiones/audio. No hay API de consumo de `BREAK_READY` (la definirá POST06). No usa `cc_at_check`. No mide rendimiento. No resuelve D1–D5. G2/G3 siguen `NOT_STARTED`.
