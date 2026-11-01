# POST01 — Hook, ABI y pasividad

Fuente nativa: Dusklight v2.0.3, commit `40457c6adb381928e4b5fef6ed459ed291edd5e2`. Citas `ruta:línea` sobre ese árbol (verificado contra el ZIP en POST00 `SOURCE_INVENTORY.md`).
Etiquetas: **[S]** fuente leída · **[C]** comprobado al compilar con MSVC (CI) · **[B]** binario oficial (manifiesto/desensamblado de POST00) · **[R]** pendiente de runtime humano.

## 1. Hook
| Dato | Valor |
|---|---|
| Declaración | `DEFINE_HOOK(&daE_OC_c::damage_check, EocDamageCheckPost01)` — el único `DEFINE_HOOK` del módulo [S] `src/mod.cpp` |
| Firma | `void (daE_OC_c::*)()`; `static_assert(std::is_same_v<…>)` [C] |
| PMF | `sizeof == 8` (compacto, Win64): `static_assert` [C] |
| Registro PE | un solo `MOD_META_HOOK_MEM`, nombres `??_7daE_OC_c@@6B@` y `daE_OC_c::damage_check`; ningún `HOOK_FN`/`HOOK_NAME`/`HOOK_MEM_EXT`/`EXPORT` [C] `pe_audit` |
| Enlace | el PMF apunta al thunk de importación `ff 25` ligado a `?damage_check@daE_OC_c@@QEAAXXZ` de `dusklight.exe` [C] |
| Símbolo en el EXE | `daE_OC_c::damage_check` RVA `0xe06390`, flags `code,multi`, sin INLINE [B]; `action()` lo llama de verdad [B] |
| Callbacks | PRE `on_pre` devuelve siempre `HOOK_CONTINUE` (sin otro `return`: auditoría de fuente); POST `on_post` es `void`. Prioridad 0 (por defecto) |
| Orden de instalación | `install_sequence`: POST, luego PRE; si falla PRE, `mods::hook::uninstall`; si ese falla, no se declara limpio y los callbacks quedan apagados (`disable`). Probado con dobles (4 estados) [lab] |
| Contratos del SDK | prioridad mayor primero, empate por orden de registro (`hook.cpp:140-143`); un `HOOK_SKIP_ORIGINAL` de un PRE de mayor prioridad corta los PRE siguientes pero los POST corren (`hook.h:42`, `hook.cpp:605-610`); `uninstall` borra los callbacks del mod (`hook.cpp:518-574`); el host retira los hooks al descargar el mod (`hook_remove_mod`, `hook.cpp:888-923`) [S] |
| Salvaguardas de carga | host `2.0.3`/`2.0.3.0`, `HookService` ≥ 1.1 con todos los punteros, `LogService` ≥ 1.0 [S]; si no, el mod no instala nada |
| Aviso de inline | el host lo emite al instalar si el manifiesto marca `kFlagInlineSites` (`hook.cpp:433-437`). Además `POST01_TARGET` lee con `resolve()` (solo manifiesto, no es un hook) el flag `0x20` y lo registra. Cobertura incompleta ⇒ G1 NO_APROBADO [R] |

## 2. ABI Win64 de los miembros leídos
`static_assert(offsetof(...))` compilados con MSVC contra las cabeceras del SDK [C]. Los valores salen del **desensamblado del EXE oficial**, no de los comentarios `/* 0x… */` (que son de retail):
| Miembro | Offset | Cómo se obtuvo [B] |
|---|---|---|
| `fopAc_ac_c::health` | `0x656` | `mov %si,0x656(%rbx)` dentro de `damage_check` (`d_a_e_oc.cpp:643`) |
| `fopAc_ac_c::actor_status` | `0x580` | `orl $0x10000,0x580(%rdi)` en `create` (`d_a_e_oc.cpp:2798`) |
| `daE_OC_c::mActionMode` | `0x8c8` | `mov %edx,0x8c8(%rcx)` en `setActionMode` (`:584-594`) |
| `daE_OC_c::mOcState` | `0x8d0` | `mov %r8d,0x8d0(%rcx)` en `setActionMode` |
| `daE_OC_c::field_0x6cc` | `0x8ec` | `cmpw $0x0,0x8ec(%rcx)` al inicio de `damage_check` (`:649`) |
Tipos: `health` y `field_0x6cc` son `s16`; `mActionMode` y `mOcState` son `int` (`static_assert`). Las demás lecturas usan miembros tipados y accesores inline, sin offsets mágicos. `mName` no tiene `static_assert` de offset: se lee por miembro tipado y solo hasta 6 bytes. No se modificó ninguna cabecera oficial.

## 3. Lecturas (todas de solo lectura)
| Lectura | Justificación de que no muta |
|---|---|
| `a->profname`, `a->state.init_state`, `fopAcM_GetID(a)` | campos / inline simple |
| `a->mName` (≤ 6 bytes, solo si perfil y vida son correctos) | `classify_name`, puntero a literal del EXE. `damage_check` solo corre tras `create()` (`d_a_e_oc.cpp:2736`) |
| `a->actor_status & fopAcStts_UNK_0x10000_e` | lectura de bits |
| `a->mSphs_at[0/1].GetAtAtp()` | inline `const` (`c_cc_d.h:338`) |
| `a->health`, `mActionMode`, `mOcState`, `field_0x6cc` | miembros |
| `a->checkCutDownHitFlg()` | inline `const` (`f_op_actor.h:377`) |
| `mSphs_cc[0/1].cCcD_ObjHitInf::ChkTgHit()` | inline `const`: `mObjTg.ChkHit()` = `mRPrm & 1` (`c_cc_d.h:383`, `:278`) |
Importa del juego **únicamente** el thunk del hook [C] (`pe-audit.json`, y `objdump -p` independiente).

### Lecturas OMITIDAS a propósito
| Omitida | Motivo (código) |
|---|---|
| `dCcD_GObjInf::ChkTgHit()` / `GetTgHitAc()` / `dCcD_GAtTgCoCommonBase::GetAc()` | `GetAc()` **escribe** una caché (`mAc`) y puede poner `mApid = -1` (`d_cc_d.cpp:26-37`): getter no pasivo. La primera compilación (CI 41274001710) lo importaba y se retiró. `GAT_NOT_PASSIVE` |
| Tipo de AT del collider (`GetTgHitObj()->GetAtType()`) | desreferenciar el collider atacante sin la guarda de actor que da `GetAc()` no es seguro y `mGObjTg` es `protected`. Se registra `at=OMITTED` / `at_type=OMITTED_NO_SAFE_ACTOR_GUARD` |
| `mAtInfo.*` | puede quedar con valores de un golpe anterior si hay retorno temprano; se dejó para POST03 |
Consecuencia: `TG_CANDIDATE` = **bit TG crudo**, más amplio que el `ChkTgHit` nativo (que exige además actor del impacto). La diferencia aflora como `EARLY_RETURN_POSSIBLE` (el cooldown no se pone).

## 4. Escrituras
Solo memoria **privada** del mod (`g`: contadores, ledger, pila de 4 frames) y líneas de log por `LogService.write`. Cero escrituras en actor, collider, Link, `mAtInfo`, flags, timers o memoria del host.
Comprobaciones: auditoría de texto `ci/source_audit.py` (sin asignaciones por puntero, sin `setActionMode`/`offTgSph`/`cc_at_check`/`ClrTgHit`/`HOOK_SKIP_ORIGINAL`/`replace`/`memcpy`…; 5 negativos probados localmente), imports PE fijados en `ci/expected_pe.json`, símbolos prohibidos en el mapa de enlace. **Límite:** son redes contra regresiones, no una prueba formal; la pasividad real se corrobora con la prueba humana [R].

## 5. Correlación PRE/POST, reentrancia y saturación
- Pila acotada de 4 `CallFrame` con serie. PRE apila `(actor, id)`; POST busca desde arriba el frame del **mismo actor**, descarta los apilados encima (`discarded_frames`) y lo desapila. Sin frame: `unmatched_post` (p. ej. otro mod hizo SKIP).
- Pila llena: el PRE no almacena (`frame_overflow`), su POST no empareja. Nada se mezcla entre actores. Probado con dobles: anidado, POST perdido, saturación y reentrada del mismo actor.
- Fail-open: cualquier excepción desactiva solo el observador (`POST01_DISABLED`); el original y las demás extensiones siguen. Tres excepciones consecutivas de `LogService` también lo apagan.

## 6. Identidad y admisión
`E_OC_CANDIDATE` exige perfil `fpcNm_E_OC_e`, actor vivo (`init_state` ≥ 0 y ≠ 3), `mName == "E_OC"`, bit `0x10000` y `AtAtp == 1` en ambas esferas (`d_a_e_oc.cpp:2776-2802`). Otros resultados: `E_OC2_EXCLUDED`, `PROFILE_OTHER`, `UNKNOWN_UNSAFE` (con motivo). El HP solo se registra como `hp_info`. Un Blue de DEVF y un E_OC nativo dan la misma firma: `origin=UNDETERMINED` siempre, sin heurísticas. Ledger de 16 entradas (sobrescritura circular) solo para no repetir `ACTOR_SEEN`; la identidad completa es de POST02.

## 7. Qué no está probado
Instalación del hook en el host real y ausencia de inline en el log; que el POST se ejecute con el estado final esperado; orden con el hook `execute` de DEVF y el `cc_at_check` de HM; coste real; comportamiento idéntico al control. Todo **[R]** hasta que el usuario aporte log.
