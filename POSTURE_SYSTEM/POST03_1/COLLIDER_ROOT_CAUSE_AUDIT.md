# POST03.1 — Auditoría de causa raíz: `SELECTED_COLLIDER_IMPLAUSIBLE`

Fuente: Dusklight v2.0.3 `40457c6adb381928e4b5fef6ed459ed291edd5e2`. Etiquetas: **[R]** juego real (logs aportados por el usuario y leídos por Claude, `POST03/RUNTIME_EVIDENCE_A_B.md`) · **[S]** fuente · **[B]** binario oficial · **[C]** MSVC/PE/CI · **[L]** laboratorio con dobles · **[P]** pendiente.

## 0. Dictamen
**`ROOT_CAUSE_RUNTIME_INSTRUMENTED_PENDING`.** La fuente demuestra que la guarda de POST03 era **incorrecta para este anfitrión** (exigía alineación de 8 donde el heap del juego solo garantiza 4) y la corrección es mínima y segura; el log de POST03 no contiene el residuo del puntero, así que la causa **no está confirmada en runtime**. POST03.1 la sustituye por una guarda justificada y añade diagnósticos que la confirmarán (o refutarán) con un log. No se declara «arreglado».

## 1. Síntoma [R]
20 de 24 `HIT_CONFIRMED` con `collider=SELECTED_COLLIDER_IMPLAUSIBLE` / `family=UNAVAILABLE` (A 6/6, B 14/18); 4 con `MATCHES_CC1` / `SWORD` / `at=0x04000002` (todos id=562 gen 19). Aparece sin HM/Bars/DEVF (sesión A). El resultado es **constante por instancia de Link** (`daAlink_c` recreado en cada carga de stage): A pid 434 → 6/6 fallan; B pid 105 → 14/14 fallan, pid 506 → 4/4 aciertan. Ningún evento rompe esa regularidad [R].

## 2. Qué hace el juego [S][B]
1. `damage_check` asigna `mAtInfo.mpCollider = mSphs_cc[0].GetTgHitObj()` y luego, si `cc[1]` también tiene hit, `= mSphs_cc[1].GetTgHitObj()` (`d_a_e_oc.cpp:656-666`): prevalece cc1. En el EXE: `mov %rax,0x1398(%rbx)` tras cada llamada (dos veces) [B].
2. Tras ese punto la llamada pone `field_0x6cc` (673-681) y desreferencia `mpCollider` varias veces (673-754, 757): `ChkAtType`, `GetAtSpl` [S]; en el EXE `testl $0xd8000000,0x20(%rcx)` lee el tipo de ataque en `+0x20` de `cCcD_Obj` [B].
3. `GetTgHitObj` (derivada) devuelve el mismo valor que la base cruda salvo que el hit no tenga actor, en cuyo caso devuelve NULL (`d_cc_d.cpp:236-243`) — y la fuente no lo toleraría (desreferencia inmediata). Por tanto, en una llamada **procesada** (cooldown 0→≠0), `mpCollider` es uno de los hit obj crudos de las dos esferas y apunta a un objeto vivo que el propio juego acaba de desreferenciar [S] (invariante P1 de `POST03/HIT_PATH_AUDIT.md`).
4. `offTgSph()` limpia el hit obj de las esferas (`ClrObj`, `c_cc_d.h:228`), por eso POST03/03.1 lo capturan en el PRE.
5. **HM** (en B) lee `info->mpCollider->GetAtType()` en su hook de `cc_at_check` sin guarda de alineación (`hm_203/core8/src/game_read.cpp:153,173`) y clasifica SWORD de forma consistente en la misma sesión [R]: los colliders eran objetos legibles.

## 3. Qué hacía POST03 (código compilado, no editado) [S]
`POST03/src/hit_core.hpp`: `plausible_ptr(p) = p >= 0x10000 && (p & 7) == 0` se evaluaba **antes** de comparar `sel` con `raw0/raw1`; si fallaba, `reason=SELECTED_COLLIDER_IMPLAUSIBLE` y `src=none`. Esa razón **no distingue** `sel==0` (que tiene su propia razón), `sel < 0x10000` ni `sel` con bits bajos ≠ 0, y el comparador nunca llegaba a ejecutarse. El log no permite saber cuál fue.

## 4. ABI y layout [C][B][S]
- `cCcD_Obj : cCcD_ObjHitInf` con funciones virtuales (`c_cc_d.h:445-470`) ⇒ **declarado** con alineación 8 en x64. `static_assert(alignof(cCcD_Obj) == 8)` **compila con MSVC** (CI 41313246091) [C]. El tamaño real Win64 no es el `STATIC_ASSERT(0x58)` de GameCube; POST03.1 lo registra en `POST03_1_INIT` (`sizeof_cCcD_Obj`, `alignof_cCcD_Obj`) [P].
- `#pragma pack(1)`…`#pragma pack()` envuelve **solo** `cCcD_ObjAt` (`c_cc_d.h:235-261`); MSVC honra `pack` e ignora `push/pop` (avisos C4068 en el build, observados en el CI) [C]. Eso hace que el subobjeto `mObjAt` tenga alineación 1, pero no cambia la alineación del `cCcD_Obj` completo ni la de `mType` leído por `GetAtType()` (int de 4 bytes en `+0x20`, confirmado por el desensamblado [B]).
- La única lectura de POST03/03.1 es `GetAtType()` (inline `const`, `c_cc_d.h:329`): `static_assert(sizeof(GetAtType()) == 4)` [C]. Un `mov eax,[rcx+0x20]` **solo necesita alineación de 4**, y x86-64 no falla por acceso de 4 bytes en dirección 4-alineada.
- `fopAc_ac_c::health 0x656`, `actor_status 0x580`, `mActionMode 0x8c8`, `mOldActionMode 0x8cc`, `mOcState 0x8d0`, `field_0x6cc 0x8ec`, `mAtInfo 0x1398`: todos `static_assert` en MSVC [C], medidos en el EXE, no en comentarios retail.

## 5. Por qué un collider legítimo puede estar a 4 mod 8 [S]
- Los actores se crean con `cMl::memalignB(-4, size)` (`f_pc_base.cpp:152`) → `JKRHeap::alloc(size, -4)` → `JKRExpHeap::do_alloc`: con `-alignment <= 4` llama a `allocFromTail(size)` (`JKRExpHeap.cpp:195-199`), que hace `size = ALIGN_NEXT(size, 4)` (`:449-450`) y reparte desde el final del bloque libre **sin alinear a más de 4**. La cabecera `CMemBlock` es de 0x20 bytes en 64 bits (`JKRHeap.h:23`).
- Cualquier asignación previa con tamaño ≡ 4 (mod 8) del heap del juego desplaza las siguientes 4 bytes. `procSize` de Link es 18912 (múltiplo de 8) y el de E_OC 5104 (múltiplo de 8) [R], pero la **dirección base** depende de todo lo asignado antes en ese heap, que cambia con cada carga de stage.
- Los colliders de ataque de Link son miembros de `daAlink_c` (`mAtSph`, `mAtCyl`, `mAtCps[3]`, `mGuardAtCps`; `include/d/actor/d_a_alink.h:4021-4024`); su dirección = base de Link + offset múltiplo de 8. Si Link cae a 4 mod 8, **todos sus colliders** quedan a 4 mod 8 durante esa instancia de Link, y a 0 mod 8 si cae alineado. Esto predice exactamente la regularidad «constante por instancia de Link» de §1.
- Esto es una **explicación compatible y probable, no una prueba** [P]: el log no tiene el residuo. Otras propiedades fijas por instancia de Link también encajarían; los diagnósticos de §8 las separan.

## 6. Decisión de diseño de POST03.1
| Gate | POST03 | POST03.1 | Justificación |
|---|---|---|---|
| `sel == 0` | `NO_SELECTED_COLLIDER` | igual | — |
| `sel < 0x10000` | mezclado en «implausible» | `SELECTED_TOO_LOW`, sin leer | puntero imposible |
| igualdad con hit obj crudo de `cc0/cc1` | solo después de «plausible» | **siempre**, con `src` registrado | la coincidencia con un valor capturado en el PRE de la misma llamada es lo que prueba frescura |
| alineación para desreferenciar | múltiplo de **8** | múltiplo de **4** (`kReadAlignBytes`, constante del tamaño del campo leído, no configurable) | el heap del anfitrión solo da 4 (§5) y se lee un int de 4 bytes |
| coincide pero no múltiplo de 4 | rechazado antes | `SELECTED_ALIGNMENT_UNSUPPORTED`, sin leer | `mod4_bad` no puede ser un `cCcD_Obj` |
| autorización de leer | `plausible ∧ src≥0` | `HIT_CONFIRMED` (P1+P2) ∧ `sel == raw cc1/cc0` ∧ ≥0x10000 ∧ múltiplo de 4 | — |
Se **mantiene**: una sola lectura por evento (`read_at_type`), nada de `IsBadReadPtr`/`VirtualQuery`/SEH (el source audit los rechaza), ninguna lectura de `mHitType/mAttackPower/mpActor`, ni `GetAc`. Una desreferencia sigue siendo justificada solo porque (a) el valor es idéntico a un puntero que el hit-test del juego guardó para esta llamada, (b) la llamada **procesó** el golpe y (c) el juego acaba de desreferenciar ese mismo objeto. La alineación de 4 es un filtro de cordura, no la garantía de validez.

## 7. Lo que NO se hizo y por qué
Restar o enmascarar el puntero, aceptar cualquier valor ≥0x10000, leer el collider no seleccionado, clasificar por HP/modo/reacción, leer Link (`getCutType`), añadir un hook en `cc_at_check`/`at_power_check` o importar símbolos nuevos: ninguna es necesaria ni está justificada (el PE audit confirma que no se añade ningún import).

## 8. Diagnóstico pasivo (para confirmar o refutar §5 con UN log)
Por cada `HIT_CONFIRMED` se acumulan **clases**, nunca direcciones:
`reason` ∈ {`NO_SELECTED_COLLIDER`, `SELECTED_TOO_LOW`, `SELECTED_ALIGNMENT_UNSUPPORTED`, `RAW_TG_HIT_OBJ_NULL`, `SELECTED_NOT_EQUAL_TO_RAW_CC0_CC1`, `SELECTED_FRESH_MATCH_CC0`, `SELECTED_FRESH_MATCH_CC1`}; `sel_class`, `raw_cc0_class`, `raw_cc1_class` ∈ {`null`, `too_low`, `mod8_0`, `mod8_4`, `mod4_bad`}; `deref_ok_mod8_0` / `deref_ok_mod8_4` (lecturas realizadas por clase). Cada evento `POST03_HIT_EVENT` lleva `collider=<reason> sel_class=… raw_class=cc0/cc1`; `POST03_1_COLLIDER_DIAG` resume. Las líneas están acotadas por el presupuesto de log (2000) y no contienen ningún literal hex de 9 o más dígitos (verificado en el laboratorio y por el source audit).
**Cómo se leerá el resultado:**
- `deref_ok_mod8_4 > 0` y familias SWORD en instancias de Link donde POST03 fallaba ⇒ causa confirmada.
- `sel_class=mod8_4` con `reason=…FRESH_MATCH…` pero `family=UNAVAILABLE` (`AT_TYPE_READ_REFUSED`) ⇒ la lectura fue rechazada por otra causa.
- `reason=SELECTED_NOT_EQUAL_TO_RAW_CC0_CC1` dominante ⇒ el defecto no es de alineación: `mpCollider` no es el hit obj crudo (hipótesis de reasignación) y la clasificación **seguirá UNAVAILABLE** (STOP_NO_SAFE_COLLIDER_CLASSIFICATION para esa clase).
- `sel_class=mod4_bad`/`too_low` ⇒ el valor no es un puntero a `cCcD_Obj`; sin lectura.

## 9. Límites
No hay prueba formal de validez de memoria ni de que el residuo sea el supuesto; el laboratorio usa punteros opacos (`[L]`, no memoria real); el comportamiento real de la lectura con `mod8_4` es `[P]` hasta el log de POST03.1.
