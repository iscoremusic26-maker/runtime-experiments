# POST02 — Contrato de identidad por instancia y ciclo de vida

Fuente nativa: Dusklight v2.0.3 `40457c6adb381928e4b5fef6ed459ed291edd5e2` (árbol verificado contra el ZIP en POST00/POST01). Citas `ruta:línea`.
Etiquetas: **[S]** fuente leída · **[C]** comprobado al compilar con MSVC (CI) · **[B]** binario oficial (POST00) · **[R]** pendiente de runtime humano.
Esta numeración es la del plan maestro de 14 checkpoints: aquí POST02 = identidad/ciclo de vida, sin gameplay. La numeración comprimida de `POST00/ARCHITECTURE_DECISION.md` (donde «POST02» era suprimir daño) **está superada**; solo se reutilizó su investigación (R08, identidad).

## 1. Qué se verificó en la fuente (investigación §3.2 del encargo)

| Pregunta | Hallazgo |
|---|---|
| **A. ¿Qué API resuelve un ID vivo?** | `fopAcM_SearchByID(id, &out)` (no inline, `f_op_actor_mng.cpp:152-162`): si `fpcM_IsCreating(id)` → devuelve 1 con `out=NULL`; si no, `fopAcIt_Judge(fpcSch_JudgeByID, &id)` recorre `g_fopAcTg_Queue` (`f_op_actor_iter.cpp:22-31`) y devuelve 0 si no hay actor. `fpcSch_JudgeByID` solo compara `->id` (`f_pc_searcher.cpp:15-20`). `cLsIt_Judge`/`cTgIt_JudgeFilter` solo recorren (`c_list_iter.cpp:17-22`, `c_tag_iter.cpp:13-15`). `fpcM_IsCreating` → `fpcCtRq_IsCreatingByID`, recorrido de la cola de creación (`f_pc_manager.cpp:48`). **Ninguno escribe**. La variante `fpcEx_SearchByID` rechaza `fpcM_UNK_PROCESS_ID_e`/`fpcM_ERROR_PROCESS_ID_e` (`f_pc_executor.cpp:17-22`); `fopAcM_SearchByID` no los filtra, por eso el ledger rechaza antes 0, `0xFFFFFFFE` y `0xFFFFFFFF` (`f_pc_manager.h:17-18`). Contraste: `dCcD_GAtTgCoCommonBase::GetAc()` **sí** escribe una caché (`d_cc_d.cpp:26-37`) y sigue prohibido. |
| **¿Qué significa «ausente»?** | Todo actor entra en `g_fopAcTg_Queue` en su primera llamada a `fopAc_Create` (`f_op_actor.cpp:447,453-454`) y sale en `fopAc_Delete` justo después de que el método de borrado del actor devuelva TRUE (`f_op_actor.cpp:404-421`). Un ID que ya vimos ejecutar `damage_check` (por tanto ya creado) y que ahora no está en la cola **y** no está en creación ya no existe. |
| **B. Hilo y orden** | `fapGm_Execute` llama a `duskExecute()` (`f_ap_game.cpp:824`) → `ModLoader::tick()` (`:807`) → `mod_update` de cada mod (`loader.cpp:1237-1270`) **antes** de `fpcM_Management` (`f_ap_game.cpp:828`), que es donde se ejecutan y borran los actores. Es el hilo del juego y no hay ejecución ni borrado de actores a mitad de `mod_update`. Los callbacks del hook corren en el hilo del juego (`hook.h:56-57`). Hot-unload: `mod_shutdown` y luego el host retira los hooks (`hook_remove_mod`, `hook.cpp:888-923`) [S]. Que el orden sea ese en el EXE real es [R] hasta el log. |
| **C. Campos para «vivo/creación/borrado»** | `state.init_state` (`f_pc_base.h:18`, comentado «maybe inaccurate name») solo se usa como filtro de seguridad: `>=0 && !=3` (3 = borrando, patrón DEVF). **No** basta para concluir borrado. Perfil (`profname`), `mName`, `actor_status` y salud son datos de admisión y de «muerte vista», no de existencia. La única prueba de existencia es la consulta del punto A. |
| **D. Imports nuevos** | `?fopAcM_SearchByID@@YAHIPEAPEAVfopAc_ac_c@@@Z` (exportado por la lib oficial, verificado con `grep -a` sobre `sdk/windows-amd64.lib`) y `?dComIfGp_getStartStageName@@YAPEBDXZ` (devuelve un puntero a miembro, `d_com_inf_game.h:1567`). Ambos de solo lectura. Auditoría PE fija el conjunto exacto (3 símbolos del juego) con una razón por símbolo. |
| **E. Epoch de contexto** | `epoch` = contador propio que sube cuando cambia el hash FNV de los primeros 8 bytes de `dComIfGp_getStartStageName()` (stage de inicio). **No** detecta cambios de sala dentro del mismo stage ni reentradas al mismo stage consecutivas sin otro stage entre medias; para eso está la consulta de existencia por ID. El epoch solo etiqueta (`context_changed`) y habilita `CONTEXT_RETIRED`; jamás implica borrado. |
| **F. Cola PRE/POST** | Cada `CallFrame` guarda `(actor, id, generation, slot)`. En POST se exige que `valid(slot, generation)` y que el `id` del slot coincida; si no, `post_generation_mismatch++` y el snapshot no se usa. Un frame de una instancia anterior no puede aplicarse a un actor nuevo con la misma dirección o ID. |

## 2. Clave de instancia
| Campo | Origen | Uso |
|---|---|---|
| `id` (`fpc_ProcID` = `unsigned int`) | `fopAcM_GetID(a)`; centinelas rechazados: 0, `0xFFFFFFFE`, `0xFFFFFFFF` | identidad nativa; los IDs crecen con `fpcBs_MakeOfId` (`f_pc_base.cpp:54-57`) pero **no se supone** unicidad ni no-reciclaje |
| `ptr` (`uintptr_t`) | dirección del actor en el hook | solo comparación; **nunca** se desreferencia ni se registra |
| `generation` (u64, ≥1) | contador monotónico PROPIO del ledger; se asigna en cada nueva vida; nunca se reutiliza; 0 reservado (wrap simulado en el lab) | identifica la vida en logs y valida los frames |
| `epoch_first/last` (u32) | epoch de contexto (arriba) | etiquetado; comparación segura ante wrap |
| `adm` | `admit()` | estado de admisión, separado del origen |
| origen | siempre `UNDETERMINED` para `E_OC_CANDIDATE` (`NA` para el resto) | sin NATIVE/BLUE por conjetura |
`id` y `generation` no persisten entre arranques. HP, variante de DEVF, posición, orden de spawn, escena o color **no** forman parte de la clave.

Los cuatro casos de reciclaje (todos probados en el lab):
1. ID nuevo + dirección nueva → instancia nueva (`FIRST_SEEN`).
2. ID nuevo + dirección vieja → la instancia anterior se retira como `ADDRESS_REUSED_BY_OTHER_ID` (dos actores no pueden vivir en la misma dirección) y la nueva no hereda estado.
3. ID viejo + dirección distinta → conflicto: la antigua se retira como `IDENTITY_CONFLICT_SAME_ID_OTHER_ADDRESS`, nueva generación, sin trasladar estado.
4. ID y dirección iguales tras un retiro → generación nueva y estado limpio (no se «resucita» el registro).

## 3. Máquina de estados
| Estado | Cómo se entra | Qué NO significa |
|---|---|---|
| `ACTIVE` | `FIRST_SEEN` (primera llamada al hook, **no** `SPAWN_CONFIRMED`) o `REVALIDATED` | — |
| `DEATH_SEEN` | POST con `health<=0` o modo nativo DEATH 9 / WATER_DEATH 10 / FALL_DEAD 13 | **no** es borrado; el actor puede seguir animando o pendiente de eliminar |
| `UNVERIFIED` | consulta con `PRESENT_MISMATCH_PTR/PROFILE`, `CREATING`, o 3 consultas seguidas `UNAVAILABLE/FAILED` | no es borrado; el siguiente `damage_check` del mismo (id, ptr) o una consulta `PRESENT_MATCH` lo devuelve a `ACTIVE` |
| `RETIRED` | motivo explícito (abajo) | solo `LOOKUP_ABSENT_VERIFIED` afirma borrado (`delete_claim=1`) |

Motivos de retirada: `LOOKUP_ABSENT_VERIFIED` (ausente y no en creación; **único con delete_claim**), `ADDRESS_REUSED_BY_OTHER_ID`, `IDENTITY_CONFLICT_SAME_ID_OTHER_ADDRESS`, `CAPACITY_EVICTED` (solo para `UNVERIFIED`), `CONTEXT_RETIRED` (instancia no verificada de un epoch anterior; sin afirmar borrado nativo). `SESSION_SHUTDOWN` no consulta ni desreferencia nada (`instances_dereferenced=0`).
Un cambio de epoch **no** retira a una instancia verificada como presente. Un cambio transitorio de admisión (p. ej. `AtAtp` ≠ 1) emite `ADMISSION_CHANGED` y **conserva** la identidad; no hay reset por HP, animación o estado.

## 4. Capacidad, evicción y barrido
- **64 entradas fijas** (sin `new`, mapas ni vectores en el camino caliente). Justificación: los 32 encuentros de DEVF (no todos vivos a la vez: se cargan por sala) más nativos y E_OC2; las sesiones reales de POST01 llegaron a 27 inserciones con wrap en 16 entradas. No hay evidencia de más de ~30 vivos simultáneos, pero el contador `max_active` lo medirá.
- **Asignación**: libre → retirada más antigua → `UNVERIFIED` más antigua (`CAPACITY_EVICTED`, explícito y contado, no es borrado) → si no hay nada: `CAPACITY_EXHAUSTED`, el candidato se omite (sin detalle), `capacity_drops++` y el original sigue intacto. **Nunca** se expulsa un `ACTIVE` ni un `DEATH_SEEN`.
- **Barrido** en `mod_update`: cada 10 llamadas, hasta 2 consultas de existencia en round-robin (cada instancia se consulta como mucho una vez por barrido; un `Pick` guarda `generation` y se descarta si el slot cambió: `stale_picks`). Coste O(nº de actores) por consulta, ≤ 2 consultas por 10 ticks; nunca dentro del hook; nunca sobre punteros guardados. El puntero `out` devuelto por la consulta es el único que se lee (`profname`, `id`) y es un actor vivo recién obtenido.
- **Log**: 2000 líneas por sesión (ciclo de vida 700, golpes 900, otros 300, resumen 100) y tope adicional para eventos ruidosos (admisión 40, revalidación 40, no verificado 40, capacidad 20, clave inválida 10). Sin logs por frame.

## 5. Lo que POST02 NO hace
No escribe en actores, colliders ni Link; no hay segundo hook; no `HOOK_SKIP_ORIGINAL`/`replace`; no postura, HUD, supresión ni Finish. El conteo robusto de impactos (dos TG, múltiples hitboxes, deduplicación) es de POST03: aquí se conservan las etiquetas de POST01 (`TG_CANDIDATE` = bit TG crudo, `ACCEPTED_LIKELY`, etc.) añadiendo `generation` y `life`.

## 6. Blue de DEVF (D1)
Un E_OC nativo y un Blue de DEVF dan la misma firma (perfil, `mName`, bit `0x10000`, `AtAtp==1`). No hay señal certificada: `origin=UNDETERMINED`. No se usan HP inicial, color, coordenadas, ID, orden de creación ni presencia del servicio DEVF. D1–D5 siguen pendientes.

## 7. Riesgos abiertos [R]
1. Que `fopAcM_SearchByID` no reporte «ausente» para un actor vivo (la fuente lo descarta; el log lo confirmará: un ID retirado con `LOOKUP_ABSENT_VERIFIED` que vuelve a aparecer con el mismo ID sería un **fallo crítico**).
2. Coste real de la consulta con muchos actores.
3. Que el epoch de stage no cubra reentradas sin stage intermedio (cubierto por la consulta por ID).
4. Orden real con los hooks de DEVF y HM (heredado de POST01; sin hooks compartidos).
5. Ledger lleno de vivos en sesiones muy largas: el diseño omite y cuenta, no sobrescribe.
