# POST08 FIX02 0.8.2: implementación

| Campo | Valor |
|---|---|
| Base | 0.8.1 compilado `d70f967` (rama `feature/posture-post08-fix01-contact-timing`) |
| Rama nueva | `feature/posture-post08-fix02-ai-recovery` |
| Commit de código compilado | **`62533c27730de14abcf65bf8d6d3ed409db2503f`** |
| CI | `ci/posture-post08-fix02-ai-recovery` (desde `e6d5a20`), espejo `4bd5553`, run **41458296635** (compilación e `independent-download` correctas) |

## Cambios

1. **`parry_core.hpp` → `ArmTrack`.** Registra en el POST de cada `damage_check` (tras **todas** nuestras escrituras) si la esfera quedará armada: ATTACK 1|2 con el clip en [14, 22], exactamente la condición nativa. El PRE del tick siguiente solo juzga el registro At si su `tick+1` coincide y la identidad (slot, id, generación) es la misma; si no, `STALE_CONTACT`, que no cuenta como contacto, no crea episodio y no resuelve nada.
2. **`deflect_plan`.**
   - `NativeContinues` (Link en `GUARD_ATTACK` o `GUARD_SLIP`): **ninguna escritura**.
   - `RestorePre`: deshace con `restore_reaction(PRE)` el mareo nativo del Shield Attack que POST05 no hubiera deshecho.
   - `ForceRecoil`: Link sin protección (p. ej. `GUARD_BREAK`); usa la ruta 0.8.1 (PRE con estado 3).
   - `Refuse`: cualquier otra forma; sin escritura y sin parry.
3. **`break_core.hpp`.** `View::parry_break_pending`: en la llamada del contacto POST06 **espera** (ni mareo ni rearme 50). La llamada siguiente del actor recibe `parry_crossed` → `BREAK_BY_PARRY`. Tabla por slot; caduca en 3 ticks, y en ese caso POST06 hace su recuperación segura a 50.
4. **`AiWatch`** (solo lectura). Se activa con:
   - un parry (`cause=PARRY`);
   - una supresión aplicada por POST05 (`SUPPRESSION`);
   - una ruptura de POST06 (`BREAK`).

   Vigila 300 ticks con lo que el PRE ya lee (modo, estado, frame, ritmo, `6c0`/`6c2`, `speedF`). Clasifica:
   - `NORMAL_NEXT_ATTACK_OBSERVED`, `NORMAL_AI_PROGRESS` o `NORMAL_AI_WAIT_NO_ATTACK`;
   - `AI_STALL_SUSPECTED_ABORTED_SWINGS` (≥ 3 golpes abortados sin ninguno armado);
   - `AI_STALL_SUSPECTED_FROZEN` (≥ 90 ticks sin cambios fuera de daño o caída; una espera nativa con temporizador **no** cuenta);
   - al final: `RESOLVED_NATIVELY` / `STILL_SUSPECTED`.

   Como mucho 8 vigilancias, 220 líneas y un historial de 6 muestras. Nunca corrige nada.
5. **Telemetría:**
   - `POST08_AI_TRACE event=START|SUSPECTED|END`;
   - `POST08_SUMMARY part=4/4` con `stale_contacts_ignored`, `deflect(native/restore_pre/force_recoil/break)`, contadores del monitor por causa y E_OC2, y rupturas `deferred/delivered/expired`.

## Escrituras, hooks e imports

- **Escrituras al actor:** el mismo conjunto que 0.8.1 [B]: los 10 campos de `restore_reaction`, ahora solo en `RestorePre`/`ForceRecoil`; la ruta habitual (`NativeContinues`) no escribe.
- **Sin cambios:** ninguna escritura nueva a Link, vida, cooldown, animación, ritmo, colisionadores ni Expansion; ningún hook nuevo (5); imports idénticos (`PE_AUDIT_PASS` con el mismo pin).
- **Falsos positivos de la heurística binaria:** 3 escrituras «nuevas» a offsets `0x650`/`0x668`/`0x8c8` dentro de `??0P8@Runtime`. Son el constructor de nuestra propia tabla `pending_break`, sobre `this` de `P8`, verificado en el desensamblado.

## Límites

- Todo lo del juego está **HUMAN_PENDING**.
- La simulación es `LAB_MODEL_ONLY`: modela la semántica de registro de la fuente y un solape por golpe (respaldado por 79 contactos para 74 bloqueos en el log de 0.8.0).
- Ruptura por espada coincidente con un contacto At: sin cambio; la vigila el monitor.
