# POST02 — Evidencia

Fecha: 2026-11-01. Entorno local: WSL2/Linux, sin MSVC, sin Windows y sin juego. Todo lo de Windows salió del workflow privado. **No se ha ejecutado el juego ni cargado la DLL.**

## 1. Etiquetas
| Etiqueta | Estado | Respaldo |
|---|---|---|
| `SOURCE_IMPLEMENTED` | sí | `src/mod.cpp`, `src/lifecycle_core.hpp`, `src/hit_core.hpp` |
| `SOURCE_AUDIT_PASS` | sí | `ci/source_audit.py` (CI y local); 6 negativos rechazados |
| `LAB_PASS` | sí (dobles, no runtime) | g++ 20 con ASAN+UBSAN local y MSVC en CI: 29557 comprobaciones, 0 fallos |
| `WINDOWS_MSVC_PASS` | sí | MSVC 19.51.36260 x64, ejecución 41277388694 |
| `PE_AUDIT_PASS` | sí | `pe_audit.py` con imports fijados y razonados |
| `ARTIFACT_DOWNLOADED_VERIFIED` | sí | descarga independiente en CI y descarga mía a carpetas nuevas con SHA-256 |
| `HUMAN_RUNTIME_PENDING` | **cerrado de forma acotada** (actualizado el 2026-11-01, §7) | dos sesiones reales; resumen recibido (`USER_SUPPLIED_RUNTIME_LOG_SUMMARY`) |
| `HUMAN_PASS`, `LIFECYCLE_RUNTIME_PASS` | **`SCOPED_RUNTIME_PASS`** | solo las condiciones de §7; Claude no leyó los bytes de los logs |
| `COMPATIBILITY_PASS` | acotado a la configuración de §7; **no** `UNIVERSAL_COMPATIBILITY_PASS` | |
| G1 (POST01) | `SCOPED_RUNTIME_PASS` | `POST01/EVIDENCE.md` §8, resumen aportado por el usuario |
| G2, G3 | `NOT_STARTED` | |

## 2. Base y Git
- SDK oficial `40457c6adb381928e4b5fef6ed459ed291edd5e2`; Aurora `3227d76c60e1e782ca576610bce61c9e7744d8be`; ZIP Windows `ac63514e…2caf` (56037777 bytes); `sdk/windows-amd64.lib` `4dc4a511…ca4`; `dusklight.exe` `ffa99203…0049`. Fijados en `ci/build_windows.py` y verificados en cada ejecución.
- Verificado con `git ls-remote` antes de escribir: POST00 `7fa57ef…`, POST01 `0d58080c0d76fbedbca8a4005622fadd3c7a760f`, CI POST01 `037f29a1ee7f53b6b36919dde3d4e675fb4a9329`. Worktrees POST00/POST01 y repos principales sin cambios.
- Fuente: rama `feature/posture-post02-instance-lifecycle` (desde `0d58080`). Commit compilado por la ejecución final: **`3d6539010fb29038ea9ee7704592400fe33a4eba`**; el commit documental posterior se indica en `VERIFICATION.json`/git log.
- CI: rama `ci/posture-post02-instance-lifecycle` (desde `main` @ `9f95a34`), workflow nuevo `posture-post02-instance-lifecycle.yml` (disparo `push` solo en esa rama), `POSTURE_SYSTEM/POST02_CI_SOURCE.json` con el SHA-256 de cada archivo de producción. Commit CI de la ejecución final: **`ececd6f83df875835f6a0c8efefe560737165677`**.
- No se tocaron: fuente/CI/.dusk de POST01 (salvo `POST01/EVIDENCE.md` y `POST01/VERIFICATION.json`, **solo documentales**), DEVF, HM, Bars, SDK, host, partidas; PR #80/#81; workflows previos. Sin PR, merge, tag ni release.

## 3. Ejecuciones de CI
| Run | Espejo de | Resultado | Motivo |
|---|---|---|---|
| 41277289817 | `3cb2cc7` | fallo (solo fijación PE) | compila a la primera (todos los `static_assert`, incluida la firma de `fopAcM_SearchByID`); el lab MSVC pasa; imports del juego = exactamente los 3 revisados; la fijación tenía el orden alfabético y `__std_terminate` mal |
| **41277388694** | **`3d65390`** | **éxito (build + descarga independiente)** | https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41277388694 |

## 4. Ejecución final (41277388694, CI head `ececd6f8…5677`)
- Toolchain: MSVC 19.51.36260 (VCTools 14.51.36231), Windows SDK 10.0.26100.0, CMake 4.4.4, Ninja 1.13.2, `-std:c++20 /O2 /Zc:inline- /GL-`. Los 9 avisos son de cabeceras oficiales; ninguno de `src/`.
- Unidades de producción: `mod.cpp` y `sdk/src/game_feature.cpp`.
- DLL: 38400 bytes, SHA-256 `a6bb6b39f01511d5da972781e03a3bee7b2dbbfd1b25ec771a35ef3792712b54`.
- `.dusk`: `POSTURE_POST02_INSTANCE_LIFECYCLE_windows-amd64_3d6539010fb2.dusk`, **16883 bytes**, SHA-256 `addeb770324f931947023d98fc804a4aab96f34637cd4114d6a9a5f26c5fff59`. Miembros: `mod.json` (idéntico a la fuente) y `lib/windows-amd64/mod.dll` (idéntica a la suelta). ID `dev.posture.post02_instance_lifecycle`, versión `0.2.0`.
- Artefactos (expiran 2026-12-01): `POST02_TEST_41277388694_1` id **13071996061** (ZIP 17715 bytes, digest `0641137b…f5fcf`), `POST02_TEXT_41277388694_1` id 13071956370, `POST02_DOWNLOAD_VERIFIED_41277388694_1` id 13070999352. Enlace directo: https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41277388694/artifacts/13071996061. La API de Actions confirma que ese id pertenece a ese run y se llama `POST02_TEST_41277388694_1`; la página web es privada y no la abrí.
- PE: AMD64; sin TLS ni delay-import; exports `mod_ctx, mod_initialize, mod_meta, mod_shutdown, mod_update`; metadata 1 HEADER + 4 IMPORT (`game 2.0`, `hook 1.1`, `host 2.2`, `log 1.0`) + **1 HOOK_MEM** (`daE_OC_c::damage_check`, thunk ligado a `?damage_check@daE_OC_c@@QEAAXXZ`). Imports de `dusklight.exe` (los únicos del juego): `?damage_check@daE_OC_c@@QEAAXXZ` (hook), `?fopAcM_SearchByID@@YAHIPEAPEAVfopAc_ac_c@@@Z` (existencia, solo lectura, solo `mod_update`), `?dComIfGp_getStartStageName@@YAPEBDXZ` (epoch). Ninguno mutador; el resto es arranque CRT/EH.
- Verificación local independiente: `sha256sum -c` OK, `unzip` a carpeta vacía, DLL `a6bb6b39…2b54`, `mod.json == fuente`, `pe_audit.py -I` PASS y `objdump -p` (otra herramienta) muestra exactamente esos 3 imports de `dusklight.exe`.

## 5. Laboratorio: casos exigidos → pruebas (`tests/lifecycle_lab.cpp`)
| Caso | Prueba |
|---|---|
| 01–02 | `t_first_and_reobserve` |
| 03 | `t_same_ptr_new_id` |
| 04 | `t_same_id_new_ptr` |
| 05 | `t_retire_then_reappear` |
| 06 | `t_death_is_not_delete` |
| 07 | `t_absent_reuses_slot` |
| 08 | `t_unavailable_never_deletes` |
| 09 | `t_lookup_mismatch` |
| 10 | `t_context_change` (incluye wrap de epoch) |
| 11 | `t_full_table_no_silent_overwrite` |
| 12 | `t_many_encounters` (32 encuentros, más vidas que slots, direcciones reutilizadas, generaciones únicas) |
| 13 | `t_frames` (reentrada, POST faltante/duplicado, anidado, overflow, retirada entre PRE y POST) |
| 14–16 | `t_admission_and_origin` |
| 17 | `t_sessions_and_sentinels` (sesiones, wrap de generación, IDs inválidos, `Pick` obsoleto) |
| 18 | `t_fail_open` (deshabilitado, resumen, presupuesto de log, throttle, instalación con 4 fallos) |
| extra | `t_format`, `t_random_walk` (6000 pasos deterministas); `invariants()` tras cada operación: ids/ptrs/generaciones únicos entre vivos, motivo de retirada siempre presente, conteo de vivos coherente |
Mutaciones deliberadas del ledger (8) todas detectadas por el lab: sin detección de dirección reciclada, comparación de dirección siempre verdadera, generación constante, evicción de ACTIVE, muerte sin HP, `CONTEXT_RETIRED` sin exigir UNVERIFIED, límite de `UNAVAILABLE` a 1, `mark_death` sobre retirados. Una novena mutación no compiló y se descartó.

## 6. Límites
- **LAB_PASS no prueba runtime.** La consulta de existencia está justificada por la fuente ([S]) y su firma/símbolo por MSVC/PE ([C]); su comportamiento en el juego real es [R].
- Epoch por nombre de stage: no cubre reentradas sin stage intermedio ni cambios de sala; para eso está la consulta por ID.
- `FIRST_SEEN` no es `SPAWN_CONFIRMED`. Un actor que nunca ejecute `damage_check` no se ve.
- Dos TG simultáneos, múltiples hitboxes y deduplicación de impactos son de POST03; aquí `TG_CANDIDATE` sigue siendo el bit TG crudo y el tipo de AT sigue omitido (sin guarda segura de actor).
- Blue de DEVF: `origin=UNDETERMINED`. D1–D5 pendientes. `CalcDivideInfo` (incidencia de POST01 no atribuida) no se investigó.
- HM/Bars: fuentes sin demostración de reconstrucción byte a byte (heredado). Coexistencia con DEVF/HM/Bars **no probada** con POST02.

## 7. Cierre humano acotado de POST02 (añadido el 2026-11-01; solo documental)
**Procedencia: `USER_SUPPLIED_RUNTIME_LOG_SUMMARY`** (`[U]`). Los dos logs los analizó otro asistente; Claude **no ha leído sus bytes** y **`RAW_LOG_IN_REPO` = no**. Se registran solo nombres, tamaños, SHA-256 y cifras, sin rutas ni datos personales. Todo lo anterior de este documento (build, CI, artefacto) queda como estaba.

| Sesión | Log · SHA-256 · tamaño · líneas | Mods | Resultado reportado |
|---|---|---|---|
| Aislada de combate | `dusklight-20261101-004538.log` · `82572f583500fd909b367e464a1575a6793209302d5cbcf42c88f60caaa05c17` · 332521 bytes · 4377 líneas (`splitlines()`; un visor puede mostrar 4378) | POST02 + Zora Swim 1.3.0 (2/2) | Dusklight 2.0.3 D3D12; POST02 0.2.0; `resolve=MOD_OK`, `inline_sites_flag=0`, PRE/POST OK. `POST02_SUMMARY tag=SHUTDOWN`: calls=21122; adm(cand/e_oc2/other/unsafe)=9052/12070/0/0; records_created=20, active=6, max_active=9, death_seen=8, absent_verified=14; lookups=707, lookup_unavailable=0; admission_changes=0; pre(finish/cooldown/no_tg/tg/unknown)=0/54/8992/6/0; hits=6, processed=6, accepted_likely=6, finish=0; anomalies=0, identity_conflicts=0, capacity_drops=0, capacity_evictions=0; unmatched_post=0, discarded=0, frame_overflow=0, post_generation_mismatch=0; log dropped=0, errors=0. Cierre normal. Los 6 impactos fueron letales 40→0 sobre E_OC candidatos, varios con `tg=cc0+cc1` (una llamada con dos TG no se duplicó). `CalcDivideInfo` 544 y 108 avisos de texturas: diagnósticos del motor, sin atribución a POST02 |
| Combinada | `dusklight-20261101-004941.log` · `39662abbf7812aa63c9465197b734eaf15b7942dd1a8bbbedeaae7a32bfdb892` · 816979 bytes · 5271 líneas (`splitlines()`; un visor puede mostrar 5272) | POST02, HM, Bars, DEVF, Expansion, Zora Swim, Randomizer, Luau (8/8) | Hook instalado sin inline; cierre normal; sin anomalías internas. `POST02_SUMMARY tag=SHUTDOWN`: calls=40429; adm=12148/25731/0/2550; records_created=22, active=5, max_active=10, death_seen=12, absent_verified=17; lookups=1132, lookup_unavailable=0; admission_changes=24; pre(finish/cooldown/no_tg/tg/unknown)=5/216/11903/24/0; hits=29, processed=24, accepted_likely=24, finish=5; anomalies=0, identity_conflicts=0, capacity_drops=0, capacity_evictions=0; unmatched_post=0, discarded=0, frame_overflow=0, post_generation_mismatch=0; log dropped=0, log_errors=0. Blues de DEVF (actor 221 gen 3, actor 222 gen 4, otros): `E_OC_CANDIDATE → UNKNOWN_UNSAFE → E_OC_CANDIDATE` con `identity=KEPT` y **sin** generación nueva; no se usa como clasificación de origen. HM CP11 ×2: `cc_at_check` PRE/POST 50/50, events=50, HP match=50, diff=0, identityMismatch=0, threadMismatch=0 (tipos HM: SWORD 47, STUN 2, …; **los 50 de HM no tienen por qué igualar los 24 de POST02**: perfiles y condiciones distintos; no hay correlación 1:1 inventada). Bars CP06: queries=108316, ok=62858, use-native=45456, unavailable=2, invalid=0, rejected=0, barsDrawn=8056, packetDraws=6666. `CalcDivideInfo` 376; 108 avisos de texturas; 20 eventos `PERF_WINDOW` de DEVF como `MEASUREMENT_NOT_AN_ERROR` |

- **Alcance:** `SCOPED_RUNTIME_PASS` para identidad por generación, retirada verificada por consulta (`absent_verified` > 0 sin `lookup_unavailable`), convivencia con HM/Bars/DEVF/Expansion en esas dos configuraciones y cierre limpio. **No** es `UNIVERSAL_COMPATIBILITY_PASS` ni una medición de sobrecarga. Un Finish nativo observado no es un Finish generado por ruptura: G2/G3 siguen `NOT_STARTED`.
- **Incidencia no atribuida:** `CalcDivideInfo`/texturas aparecen también sin POST02 en sesiones anteriores; no se culpa ni se absuelve a POST02.
- **Pendiente tras este PASS:** el instante exacto de `create` no es observable (`FIRST_SEEN` ≠ spawn); D1 (Blue) sigue abierto.
