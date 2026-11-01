# POST03.1 — Contrato del evento de impacto (delta sobre POST03)

Rige `POST03/HIT_EVENT_CONTRACT.md` y `POST03/HIT_PATH_AUDIT.md` sin cambios, salvo lo siguiente. Etiquetas: [S] fuente · [C] MSVC/CI · [L] laboratorio · [P] pendiente.

## Qué NO cambia
Un procesamiento = un frame = como máximo un evento; veredictos (`FINISH_NATIVE_OBSERVED`, `HIT_CONFIRMED`, `HIT_PROCESSED_SIGNATURE_MISMATCH`, `HIT_CANDIDATE_NOT_PROCESSED`, `FINISH_UNEXPECTED_STATE`); `HIT_CONFIRMED` = P1 (cooldown 0→≠0) ∧ P2 (modo 5/6 y `mOldActionMode == modo PRE`); `cc_at_check=UNDETERMINED`; identidad por `(id, dirección opaca, generation)`, 64 slots, barrido de existencia solo en `mod_update`; `origin=UNDETERMINED`; `eligible` sin consumidor. Un `HIT_CONFIRMED` con familia no disponible **no** se convierte en SWORD ni en «golpe elegible de espada».

## Qué cambia: la autorización de la única desreferencia de collider
`read_at_type` solo se invoca si, a la vez:
1. el veredicto es `HIT_CONFIRMED` (P1+P2);
2. `mAtInfo.mpCollider` (valor del POST) es **igual** al hit obj crudo de `cc1` (si su bit TG estaba) o, si no, al de `cc0`, capturados en el PRE de **esta** llamada (comparación entre valores opacos, sin desreferenciar);
3. `sel >= 0x10000` y `sel` es múltiplo de **4** (`kReadAlignBytes`: el campo leído es un int de 4 bytes, y el heap del anfitrión solo garantiza 4; POST03 exigía 8).
Siempre como máximo **una** lectura por evento (`reads <= 1`), sobre `mAtInfo.mpCollider` (`+0x1398`), nunca sobre el otro collider. Sin `GetAc`, `IsBadReadPtr`, `VirtualQuery` ni SEH.

## Campos nuevos de `POST03_HIT_EVENT`
`collider=<razón>` con el conjunto: `NO_SELECTED_COLLIDER`, `SELECTED_TOO_LOW`, `SELECTED_ALIGNMENT_UNSUPPORTED` (coincide con el crudo pero no es múltiplo de 4), `RAW_TG_HIT_OBJ_NULL`, `SELECTED_NOT_EQUAL_TO_RAW_CC0_CC1`, `SELECTED_FRESH_MATCH_CC0`, `SELECTED_FRESH_MATCH_CC1`; `sel_class=` y `raw_class=<cc0>/<cc1>` ∈ `null, too_low, mod8_0, mod8_4, mod4_bad` (clases de residuo, **nunca direcciones**). `collider_src` sigue indicando la esfera que coincide.

## Líneas nuevas
- `POST03_1_INIT` (id `dev.posture.post03_1_collider_classification`, versión `0.3.1`, `deref_gate=eq_raw_hit_obj+align4`, `sizeof_cCcD_Obj`, `alignof_cCcD_Obj`).
- `POST03_1_COLLIDER_DIAG v=0.3.1 tag=…`: `reason(...)`, `sel_class(...)`, `raw_cc0_class`, `raw_cc1_class`, `deref_ok_mod8_0`, `deref_ok_mod8_4`, `classification_unavailable`. Invariante: la suma de `reason(...)` y la de `sel_class(...)` es igual a `confirmed` [L].
- `POST03_SUMMARY`, `POST03_HIT_SUMMARY` y `POST03_CONSERVATION` llevan `v=0.3.1`.

## Estados de la corrección
`SOURCE_FIX_IMPLEMENTED` [C]; `CLASSIFICATION_FIXED` **no** se declara: requiere un log real posterior (`RUNTIME_PENDING`). Si en ese log `sel_class=mod8_4` no aparece o `reason=SELECTED_NOT_EQUAL_TO_RAW_CC0_CC1` domina, la clasificación sigue `UNAVAILABLE` (fail-closed) y el diagnóstico decide el paso siguiente.
