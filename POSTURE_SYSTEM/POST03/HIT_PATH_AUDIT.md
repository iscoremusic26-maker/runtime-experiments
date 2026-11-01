# POST03 — Auditoría de la ruta de impacto de `daE_OC_c::damage_check`

Fuente nativa: Dusklight v2.0.3 `40457c6adb381928e4b5fef6ed459ed291edd5e2`. Citas `ruta:línea` sobre ese árbol.
Etiquetas: **[S]** fuente leída · **[B]** binario oficial (`dusklight.exe` SHA `ffa99203…0049`, `damage_check` RVA `0xe06390`, desensamblado y thunks resueltos) · **[C]** MSVC/PE/CI · **[L]** laboratorio con dobles · **[U]** resumen humano recibido (bytes no leídos por Claude) · **[P]** pendiente/no observable.
La numeración POST00 «POST02 = suprimir daño» está superada; aquí POST03 = detección/clasificación/deduplicación, sin gameplay.

## 1. Ramas nativas de `damage_check` (`src/d/actor/d_a_e_oc.cpp`)
| # | Rama | Líneas | Señales observables | Qué escribe el juego | Lo que POST03 puede afirmar |
|---|---|---|---|---|---|
| R0 | **CutDownHit** (Finish): `health=0`, `setActionMode(DEATH,1)`, `offTgSph`, return | 639-647 | PRE: `CutDownHit`=1. POST: `health==0`, `mode==9` | `health`, modo, TG | `FINISH_NATIVE_OBSERVED`. No es golpe regular ni postura. No se induce |
| R1 | **Cooldown** `field_0x6cc != 0`: return | 649-651 | PRE: `cooldown>0` (con o sin bits TG) | nada | `COOLDOWN_NO_PROCESS`; TG presente = `cooldown_with_tg` (contador), **no** impacto |
| R2 | `mStts.Move()` y lectura de TG de `cc[0]`, `cc[1]` (la segunda **sobrescribe** `mAtInfo.mpCollider`); sin TG → return | 653-670 | PRE: bits TG crudos; POST sin cambio | `mAtInfo.mpCollider`, `mStts` | `NO_TG_CANDIDATE` sin evento. Con `cc0+cc1` hay **una** sola llamada y **un** collider final |
| R3 | **Cooldown set** 20 (`AT_TYPE_UNK`) o 10; `attack<=1` → 10 | 673-681 | POST: `cooldown` pasa de 0 a ≠0. **Solo** estas líneas y la 774 escriben un valor ≠0 en `field_0x6cc` (el resto lo decrementa `execute`, `:2599-2601`) [S] | `field_0x6cc` | **Invariante P1:** `cooldown 0→≠0` ⇒ la llamada llegó aquí ⇒ `mAtInfo.mpCollider` se asignó **en esta llamada** (657/663 preceden a 673) |
| R4 | Cadena de tipo: espada (684-703; `HEAD_JUMP` pone `health=0`), escudo (704), flecha (706), bomba (712; `health=0`), bola de hierro (715; `health+=80/140`), bumerán (722), `AT_TYPE_40` (724; `health+=10`) | 683-724 | tipo en `mpCollider->GetAtType()` | `health`, `my_val` | La rama que tomó el juego es la **primera coincidencia**; `classify_family` la replica |
| R5 | **Tirachinas, E_OC** (`mName=="E_OC"`): `health-=5`; si `<0` → SE, hit mark, `setActionMode(BIG_DAMAGE,0)`, `offTgSph`, **return sin `cc_at_check`** | 726-743 | cooldown ya puesto (R3); POST: modo 6 | `health`, modo | Procesado + firma de reacción ⇒ `HIT_CONFIRMED`; `cc_at_check` puede no haberse ejecutado (`cc_at_check=UNDETERMINED`) |
| R6 | **Tirachinas, E_OC2**: SE, aggro, return | 744-753 | cooldown puesto, **sin** cambio de modo | modo (WAIT/WALK/TALK→FIND) | Excluido por admisión (solo candidatos `E_OC`). De entrar como candidato sería `PROCESSED_SIGNATURE_MISMATCH`, no confirmado |
| R7 | `cc_at_check(this,&mAtInfo)`: `at_power_check`, dirección, potencia, `health -= power`, SE, hit-stop; `invincibleEnemies` pone potencia 0 | 756, `d_cc_uty.cpp:372-460` | `health` baja o no | `health`, `mAtInfo.*` | **No** hay hook propio (HM comparte ese objetivo). `mAttackPower/mHitType` solo son válidos si se llegó aquí y **no se leen** |
| R8 | `GetAtSpl()==1` → `my_val=5`; `health<=1` → `attention_info.flags=0`, `my_val>=5` | 757-769 | — | `attention_info` | — |
| R9 | **Cancel-turn** (salto + `checkCutJumpCancelTurn`): `setActionMode(DAMAGE,my_val)`, `field_0x6cc=3`, return | 771-776 | modo 5, cooldown 3 | modo, cooldown | Procesado + firma ⇒ `HIT_CONFIRMED` |
| R10 | Final: `my_val>=5` → `setActionMode(BIG_DAMAGE,my_val-5)`+`offTgSph`; si no `setActionMode(DAMAGE,my_val)` | 779-784 | modo 5 ó 6 | modo, estado, TG | Cierra **todas** las rutas procesadas de E_OC |

**Invariante P2 (firma de reacción comprometida)** [S]: para `mName=="E_OC"` toda ruta que supera R3 termina en `setActionMode(DAMAGE|BIG_DAMAGE)` (R5, R9, R10); `setActionMode` hace `mOldActionMode=mActionMode` (`:584-587`). Por eso `HIT_CONFIRMED` ⇔ `cooldown 0→≠0` ∧ `mode∈{5,6}` ∧ `mOldActionMode==modo PRE`.
Esto confirma que **el procesamiento llegó a comprometer una reacción**, no que se haya restado HP (potencia 0, `invincibleEnemies`, bloqueo de Midna o hookshot pueden dar `hp_delta=0`). Por eso `hp_delta` es solo diagnóstico y el nombre es `HIT_CONFIRMED`, no «daño aceptado».
Si P1 se cumple pero P2 no (otro mod tocó el modo, un segundo `setActionMode` ajeno), el veredicto es `HIT_PROCESSED_SIGNATURE_MISMATCH` y no hay clasificación de familia.

## 2. Qué se deduplica y por qué es seguro
- **Una llamada = un procesamiento** [S]: `damage_check` tiene un solo `had_hit` (`:654-668`); con `cc0+cc1` conserva el collider de `cc[1]` (`:662-666`) y sigue una sola ruta. `tg_mask=3` no son dos golpes ni dos armas.
- **Una llamada por actor y tick de ejecución** [S]: `action()` llama una vez a `damage_check` (`:2418`) y `execute()` una vez a `action()` (`:2631`).
- El cooldown nativo (10/20/3 ticks) ya bloquea el reprocesado; POST03 **no añade ventana propia**. Dos golpes legítimos separados por el cooldown son dos eventos.
- Un golpe de espada que alcance a dos Bokoblins son dos llamadas (una por actor) y dos eventos.
- **Qué no es dedup:** `serial` de frame + puerta por instancia (`try_emit`) solo evitan que el mismo token emita dos veces (POST duplicado, replay, reentrada). [L]

## 3. Tabla de CAPACIDAD de lecturas (campo · origen · instante válido · efectos · vida del objeto · ABI · evidencia · resultado)
| Campo | Origen | Instante válido | Efecto al leer | Vida | ABI Win64 | Evidencia | Resultado |
|---|---|---|---|---|---|---|---|
| bit TG crudo de cada esfera | `cCcD_ObjHitInf::ChkTgHit()` inline const (`c_cc_d.h:383`) | PRE | ninguno | miembro del actor | tipos del SDK [C] | POST01/02 [R][U] | **USADO** |
| hit obj crudo de cada esfera | `cCcD_ObjHitInf::GetTgHitObj()` inline const (`c_cc_d.h:386`) | PRE, solo si el bit TG está | ninguno; **no** se desreferencia, solo se compara | valor opaco de ESTA llamada | — | `ClrObj` lo pone a NULL en `offTgSph` (`c_cc_d.h:228`, `c_cc_d.cpp:720-723`), por eso se captura en PRE | **USADO (opaco)** |
| `dCcD_GObjInf::ChkTgHit()` / `GetTgHitObj()` / `GetTgHitAc()` / `dCcD_GAtTgCoCommonBase::GetAc()` | `d_cc_d.cpp:221-242`, `:26-37` | — | **GetAc escribe `mAc` y `mApid`** | — | import | — | **PROHIBIDO** (source audit y PE) |
| `mAtInfo.mpCollider` (valor) | miembro de `daE_OC_c` | POST, tras R3 | ninguno | puntero asignado **en esta llamada** (P1) | `mAtInfo` en `+0x1398` [B] `mov %rax,0x1398(%rbx)` tras cada `GetTgHitObj`; `static_assert` [C]; `mpCollider` primer campo (`d_cc_uty.h:21`) | `:657/663` [S], desensamblado [B] | **USADO como valor** |
| `GetAtType()` del collider seleccionado | inline const (`c_cc_d.h:329`), `mType` en `+0x20` del objeto [B] `testl $0xd8000000,0x20(%rcx)` | POST, **solo** si P1∧P2 y `mpCollider` == hit obj crudo de una esfera | ninguno | el mismo objeto que `damage_check` acaba de desreferenciar (`:673-754`, `:757`); ningún borrado síncrono ocurre dentro de la llamada | inline compilado por MSVC con las cabeceras del juego [C] | [S][B] | **USADO, una única desreferencia** (`read_at_type`) |
| `mAtInfo.mHitType / mAttackPower / mpActor / mHitBit` | `cc_at_check` | solo si se llegó a R7 | ninguno | pueden estar **obsoletos** (R5 letal, R9…) | — | `d_cc_uty.cpp:372+` | **OMITIDO** (frescura no demostrable desde un único hook) |
| `mOldActionMode` | miembro | POST | ninguno | — | `+0x8cc` [B] `mov %eax,0x8cc(%rcx)` en `setActionMode`; `static_assert` [C] | `:584-587` | **USADO** (firma P2) |
| subtipo de espada (corte/giro/salto) | `daPy_py_c::getCutType` (Link) | — | requiere importar y leer a Link | — | — | `:596-629` | **NO DISPONIBLE** (`[P]`) |
| atacante (`mpActor`) | `cc_at_check` | — | obsoleto/ cache de actor | — | — | — | **NO DISPONIBLE** |

## 4. Familias: nivel de confianza
`classify_family` replica **el orden de la cadena nativa** (`:684-726`): como la rama que ejecutó el juego es la primera coincidencia, la familia así obtenida es la decisión del propio juego, no una inferencia. Etiquetas: `NATIVE_BRANCH_ORDER` (un solo grupo de bits), `MULTIPLE_FAMILY_BITS` ⇒ `AMBIGUOUS` (se registra `native_first`), `BITS_OUTSIDE_NATIVE_CHAIN` ⇒ `OTHER_VERIFIED`, tipo 0 ⇒ `UNAVAILABLE reason=TYPE_ZERO`. Nunca se deduce de HP, animación o reacción (bomba, bola de hierro y otros convergen en BIG_DAMAGE).
Con `cc0+cc1` de colliders distintos solo se clasifica el que seleccionó la fuente (`cc[1]`) y se marca `distinct=1`; el otro **no** se desreferencia.
`[P]` Qué sigue sin saberse desde este hook: subtipo de espada, atacante, potencia real, si `cc_at_check` se ejecutó, y el instante de `create`.

## 5. Interacción con otros mods [S]
- **HM** engancha `cc_at_check` (PRE prioridad −1e9, POST +1e9; `hm_203/core8/src/mod.cpp:60-73,1014-1029`), que queda **anidado dentro** de `damage_check`: el POST de POST03 ve `health` ya reconciliado. No comparten objetivo.
- **DEVF** escribe en su hook de `execute` (antes/después de `action`), no dentro de `damage_check`: `field_0x6cc = 2` para duplicados de Helm Splitter y `setActionMode(FIND…)` (`CP19 expansion/mod.cpp:1539-1542`). Un `cooldown_with_tg>0` puede deberse a ese bloqueo y es **esperado**; no altera P1/P2 porque la ventana de POST03 es solo la llamada a `damage_check`.
- Un Blue de DEVF y un E_OC nativo son indistinguibles: `origin=UNDETERMINED`.

## 6. Limitaciones declaradas
Conjunto de mascaras `AT_TYPE_*` tomado de las cabeceras del juego [C]; en el laboratorio son sintéticas [L]. Las rutas exactas de cada arma real y los valores `at=0x…` observados son **[P] hasta el log humano de POST03**. Ni la auditoría de fuente ni la de PE son una prueba formal de no mutación.
