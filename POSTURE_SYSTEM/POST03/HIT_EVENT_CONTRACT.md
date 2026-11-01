# POST03 — Contrato del evento de impacto

Etiquetas: **[S]** fuente · **[B]** binario · **[C]** MSVC/CI · **[L]** laboratorio con dobles · **[P]** pendiente. Detalle de rutas y líneas en `HIT_PATH_AUDIT.md`. Identidad y ciclo de vida: contrato de POST02 (`POST02/IDENTITY_LIFECYCLE_CONTRACT.md`), portado sin cambio de semántica. El mod **solo observa**; ninguna señal de este contrato se consume todavía (POST04 es futuro).

## 1. Unidad y token
- **Un procesamiento = un evento lógico.** Cada llamada a `damage_check` apila **un** `CallFrame` con `serial` monótono, `(id, generation, slot)` y las lecturas PRE. El POST lo desapila una vez y pasa por `Ledger::try_emit(slot, generation, serial)`: si la generación ya no es válida → `cross_generation_drops`; si el serial no es nuevo para la instancia → `dup_serial_gate`. No hay ventana temporal ni dedup por HP/arma/tick.
- `event` = contador monótono del observador; `call` = contador de llamadas. Ninguno persiste entre sesiones. Direcciones: solo se comparan internamente, nunca se registran.
- Un POST sin frame se cuenta como duplicado (`dup_post_orphan`, si ese actor acaba de cerrar un frame) o huérfano (`unmatched_post`). Un PRE sobre un actor que ya tiene frame (damage_check no es recursivo) o un frame con más de 1000 serials descarta el anterior como **obsoleto** (`stale_frames`), contando los candidatos perdidos.

## 2. Veredictos (`kind`)
| `kind` | Condición exacta | NO significa |
|---|---|---|
| `FINISH_NATIVE_OBSERVED` | PRE `CutDownHit`=1 y POST `health==0 ∧ mode==9` | que POST03 provocara el Finish; ni un golpe regular |
| `FINISH_UNEXPECTED_STATE` | PRE `CutDownHit`=1 pero el estado final no es ese | (se registra anomalía) |
| `HIT_CONFIRMED` | PRE `TG_CANDIDATE` (cooldown 0, bit TG crudo) ∧ `cooldown 0→≠0` ∧ `mode∈{5,6}` ∧ `mOldActionMode==modo PRE` (P1+P2) | que se restara HP: `hp_delta` puede ser 0 |
| `HIT_PROCESSED_SIGNATURE_MISMATCH` | cooldown puesto pero la firma de reacción no coincide | confirmado; sin familia (`elig=UNDETERMINED`) |
| `HIT_CANDIDATE_NOT_PROCESSED` | bit TG crudo, cooldown sigue en 0 (el juego retornó antes: p. ej. el TG crudo no tenía actor del impacto) | un golpe |
Sin evento (solo contador): `COOLDOWN_NO_PROCESS` (`cooldown_blocked`, y `cooldown_with_tg` si había bits TG), `NO_TG_CANDIDATE` (`no_tg`), actores excluidos o `UNKNOWN_UNSAFE` (`excluded`, `unknown_unsafe`). `ACCEPTED_LIKELY` de POST01/02 **desaparece**: se sustituye por estos veredictos y `ACCEPTED_CONFIRMED` no existe en POST03 (el invariante demuestra «reacción comprometida», no «daño aceptado»).
La admisión sigue siendo `E_OC_CANDIDATE` (perfil, vivo, `mName=="E_OC"`, bit `0x10000`, `AtAtp==1`): `origin=UNDETERMINED` siempre (Blue de DEVF indistinguible). Un cambio transitorio de `AtAtp` pasa a `UNKNOWN_UNSAFE` **sin** perder la identidad (`ADMISSION_CHANGED identity=KEPT`) y sin eventos mientras dure.

## 3. Campos de `POST03_HIT_EVENT`
`event call id generation life kind branch cc_at_check origin tg dual distinct collider_src collider family native_first basis at hp lethal mode old_mode state cd cutdown eligible reason`
- `branch`: `FINISH`, `PROCESSED`, `UNPROCESSED_EARLY_EXIT`. `cc_at_check=UNDETERMINED` siempre (no se puede saber desde este hook si se ejecutó; R5 lo salta).
- `tg`: `cc0`, `cc1`, `cc0+cc1` (evidencia de las dos esferas; **no** son dos golpes). `dual`=1 si ambos; `distinct`=1 si los dos hit obj eran colliders distintos.
- `collider_src`/`collider`: esfera cuyo hit obj crudo coincide con `mAtInfo.mpCollider` (`cc1` prevalece, `:662-666`), o `none` + razón (`COLLIDER_NOT_FROM_TG_SPHERES`, `NO_SELECTED_COLLIDER`, `SELECTED_COLLIDER_IMPLAUSIBLE`).
- `family` ∈ `SWORD, SHIELD_ATTACK, ARROW, BOMB, IRON_BALL, BOOMERANG, AT_TYPE_40, SLINGSHOT, OTHER_VERIFIED, AMBIGUOUS, UNAVAILABLE`; `basis` = `NATIVE_BRANCH_ORDER`, `MULTIPLE_FAMILY_BITS`, `BITS_OUTSIDE_NATIVE_CHAIN` o, si no disponible, la razón (`TYPE_ZERO`, `AT_TYPE_READ_REFUSED`, `SIGNATURE_MISMATCH`, `NOT_PROCESSED`, …); `native_first` = la rama que habría elegido el juego. `at` = máscara cruda `0x%08x` o `UNAVAILABLE` (**nunca 0 inventado**).
- `hp a>b`, `lethal`: HP nativo visible en el POST (con HM es el HP tras su reconciliación, no la vida efectiva). `eligible` ∈ `CONFIRMED` (solo `HIT_CONFIRMED`), `UNDETERMINED`, `NO`: capacidad de la API pura, **sin consumidor**; la incertidumbre nunca debe alimentar postura por defecto.

## 4. Lecturas y seguridad
Solo accesores `const`/inline: bit TG crudo y hit obj crudo (valores opacos), `health/mode/state/old_mode/cooldown/CutDownHit`, `mAtInfo.mpCollider` como **valor**, y **una** desreferencia (`read_at_type`) que el motor permite únicamente tras `HIT_CONFIRMED` con `mpCollider` igual al hit obj crudo de una esfera de la misma llamada y puntero plausible (`≥0x10000`, alineado a 8). Prohibidos y auditados: `GetTgHitAc/GetAc`, `dCcD_GObjInf::ChkTgHit/GetTgHitObj`, `mHitType/mAttackPower/mpActor/...`, escrituras por puntero, `HOOK_SKIP_ORIGINAL/replace`, segundo hook, `getCutType`/Link. Un fallo de cualquier cosa degrada a `UNAVAILABLE`/contador y el original sigue (`HOOK_CONTINUE`).

## 5. Contadores y conservación
`cand_started + finish_started == judged + dup_serial_gate + cross_generation_drops + cand_discarded + finish_discarded + pending`, con `judged = confirmed + processed_mismatch + not_processed + finish + finish_unexpected`. `POST03_CONSERVATION ok=1` se emite en cada resumen; el laboratorio lo exige tras cada flujo sin perturbar y con tolerancia explícita bajo POST perdidos. `frame_overflow` (pila llena) y `capacity_drops` (ledger lleno de vivos) omiten el candidato **antes** de contarlo.

## 6. Qué cierra POST03 y qué no
Cierra: detección, deduplicación y clasificación **conservadora** por rama nativa, sobre la identidad/ciclo de vida de POST02. No cierra: subtipo de espada, atacante, potencia, ejecución de `cc_at_check`, y toda validación de juego real de POST03 (`HUMAN_RUNTIME_PENDING`). D1–D5 siguen pendientes.
