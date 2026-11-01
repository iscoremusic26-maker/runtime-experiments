# POST03 — Evidencia

Fecha: 2026-11-01. Entorno local: WSL2/Linux, sin MSVC, sin Windows y sin juego. Todo lo de Windows salió del workflow privado. **No se ha ejecutado el juego ni cargado la DLL.**
Etiquetas de evidencia: [S] fuente · [B] binario · [C] MSVC/PE/CI · [L] laboratorio con dobles · [U] resumen humano recibido (bytes no leídos por Claude) · [P] pendiente.

## 1. Etiquetas
| Etiqueta | Estado | Respaldo |
|---|---|---|
| `SOURCE_IMPLEMENTED` | sí | `src/mod.cpp`, `engine.hpp`, `hit_core.hpp`, `lifecycle_core.hpp` |
| `SOURCE_AUDIT_PASS` | sí | `ci/source_audit.py` (local y CI) |
| `LAB_PASS` / `DEDUP_LAB_PASS` | sí [L] (modelo derivado de la fuente, no runtime) | `hit_lab` 1660 comprobaciones y `lifecycle_lab` 29558, 0 fallos, en g++ ASAN+UBSAN y en MSVC (CI) |
| `WINDOWS_MSVC_PASS` | sí [C] | MSVC 19.51.36260 x64, ejecución 41280823158 |
| `PE_AUDIT_PASS` | sí [C] | imports fijados y razonados |
| `ARTIFACT_DOWNLOADED_VERIFIED` | sí | descarga independiente en CI y mía, con SHA-256 |
| `CLASSIFICATION_COVERAGE` | por rama nativa, solo [L]: 8 familias + `OTHER_VERIFIED`, `AMBIGUOUS`, `UNAVAILABLE`. En juego real: [P] | `HIT_PATH_AUDIT.md` §4 |
| `HUMAN_RUNTIME_PENDING` | **cerrado de forma acotada** (actualizado el 2026-11-01) | dos sesiones reales A/B; ver `RUNTIME_EVIDENCE_A_B.md` |
| `POST03_RUNTIME_SCOPED_OBSERVED` | sí | 26 eventos, 0 duplicados, `CONSERVATION ok=1`, cierres limpios [R] |
| `CLASSIFICATION_RUNTIME_PARTIAL` | sí (4/24 SWORD; 20/24 `UNAVAILABLE`) | **no** es `CLASSIFICATION_RUNTIME_PASS` |
| `POST03_1_FIX_PENDING` | sí | corrección en `POSTURE_SYSTEM/POST03_1` |
| `HUMAN_PASS`, `COMPATIBILITY_PASS`, `UNIVERSAL_COMPATIBILITY_PASS` | NO | solo las dos configuraciones observadas |
| POST02 | `SCOPED_RUNTIME_PASS` [U] | `POST02/EVIDENCE.md` §7 |
| G1 (POST01) | `SCOPED_RUNTIME_PASS` [U] | `POST01/EVIDENCE.md` §8 |
| G2, G3 | `NOT_STARTED` | |

## 2. Base y Git
- SDK `40457c6adb381928e4b5fef6ed459ed291edd5e2`; Aurora `3227d76c60e1e782ca576610bce61c9e7744d8be`; ZIP Windows `ac63514e…2caf`; `sdk/windows-amd64.lib` `4dc4a511…ca4`; `dusklight.exe` `ffa99203…0049`. Fijados en `ci/build_windows.py` y verificados en cada ejecución.
- Verificado con `git ls-remote` antes de escribir: POST02 `70266db733b323e76469bcc83f35a7037154ea9a`, CI POST02 `ececd6f83df875835f6a0c8efefe560737165677`, `main` del CI `9f95a34`; PR #81 sin cambios (`fe47c8b`). Worktrees y repos principales intactos.
- Fuente: rama `feature/posture-post03-hit-classification-dedup` (desde `70266db`). Código compilado por la ejecución final: **`f350522fc2097cbbe786c57df2f005ba0b4981b3`**; el commit documental posterior se registra en `VERIFICATION.json`/git log.
- CI: rama `ci/posture-post03-hit-classification-dedup` (desde `main` @ `9f95a34`), workflow nuevo `posture-post03-hit-classification-dedup.yml` (disparo `push` solo en esa rama), `POST03_CI_SOURCE.json` con el SHA-256 de cada archivo (15). Commit de CI de la ejecución final: **`64cb2464d1da65fc18639e522045f47469830ca3`**.
- Fuera de `POSTURE_SYSTEM/POST03/**` solo se tocaron `POST02/EVIDENCE.md` y `POST02/VERIFICATION.json` (documentales: cierre humano acotado con el resumen de §3 del encargo, sin logs crudos). POST01/POST02 compilados, DEVF, HM, Bars, SDK, host, partidas, PR #80/#81 y workflows previos: sin cambios. Sin PR, merge, tag ni release.

## 3. Ejecuciones de CI
| Run | Espejo de | Resultado | Motivo |
|---|---|---|---|
| 41280645366 | `205402e` | fallo | compila a la primera (todos los `static_assert`, incluidos `mOldActionMode=0x8cc` y `mAtInfo=0x1398`) y ambos labs MSVC pasan; `pe_audit` rechazó el **texto** `cc_at_check` de una etiqueta de log (`cc_at_check=UNDETERMINED`). La regla se afinó a símbolos MSVC decorados (`?nombre@`), sin relajar imports ni exports |
| **41280823158** | **`f350522`** | **éxito (build + descarga independiente)** | https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41280823158 |

## 4. Ejecución final (41280823158, CI head `64cb2464…830ca3`)
- Toolchain: MSVC 19.51.36260 (VCTools 14.51.36231), Windows SDK 10.0.26100.0, CMake 4.4.4, Ninja 1.13.2, `-std:c++20 /O2 /Zc:inline- /GL-`. 9 avisos, todos de cabeceras oficiales; ninguno de `src/`. Unidades: `mod.cpp` y `sdk/src/game_feature.cpp`.
- DLL 44032 bytes, SHA-256 `90733da156f41ce897de54f011b7ea02c6e34a84b8097d9208b4a8b966fff267`.
- `.dusk`: `POSTURE_POST03_HIT_CLASSIFICATION_windows-amd64_f350522fc209.dusk`, **19688 bytes**, SHA-256 `59c8145e6c29914ef4b602b892d35d73ba6f0946923270ab278387f992ad3c9f`; miembros `mod.json` (idéntico a la fuente) y `lib/windows-amd64/mod.dll` (idéntica a la suelta). ID `dev.posture.post03_hit_classification`, versión `0.3.0`.
- Artefactos (expiran 2026-12-01): `POST03_TEST_41280823158_1` id **13073232413** (ZIP 20565 bytes, digest `2bc8a12f…aa83`), `POST03_TEXT_41280823158_1` id 13072819133, `POST03_DOWNLOAD_VERIFIED_41280823158_1` id 13073232477. Enlace directo: https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41280823158/artifacts/13073232413 — la API de Actions confirma que ese id pertenece a ese run y se llama `POST03_TEST_41280823158_1`; la página web es privada y no la abrí.
- PE: AMD64; sin TLS/delay-import; exports `mod_ctx, mod_initialize, mod_meta, mod_shutdown, mod_update`; 1 HEADER + 4 IMPORT + **1 HOOK_MEM** (`daE_OC_c::damage_check`, thunk ligado a `?damage_check@daE_OC_c@@QEAAXXZ`). Únicos imports de `dusklight.exe` (los mismos 3 de POST02): el hook, `fopAcM_SearchByID` (existencia, solo lectura, solo `mod_update`) y `dComIfGp_getStartStageName`. POST03 **no añade ningún import**: todo lo nuevo es inline.
- Verificación local: `sha256sum -c` OK, `unzip` a carpeta vacía, DLL `90733da1…f267`, `mod.json == fuente`, `pe_audit.py -I` PASS, `objdump -p` (otra herramienta) confirma los 3 imports. La DLL **no se cargó**.

## 5. Laboratorio y mutaciones [L]
- `hit_lab.cpp` (1660): T01–T22 sobre un **modelo de `damage_check` derivado de la fuente** (cooldown, `cc[1]` sobrescribe, tirachinas letal con retorno anticipado, bomba, bola de hierro, firma P2…). Incluye cómputo de verdad terreno: en el flujo sin perturbar `confirmed + processed_mismatch ≤ procesados nativos` y `finish ≤ finish nativos`; flujo perturbado (POST perdidos/duplicados) de 12000 llamadas con reutilización de direcciones; jamás se desreferenció un puntero que no fuera un hit obj (`bad_derefs==0`).
- `lifecycle_lab.cpp` (29558): heredado de POST02 (18 casos + paseo aleatorio) adaptado a frames obsoletos y contadores nuevos.
- Cobertura T01–T22: T01–T05, T07, T09–T18, T21, T22 en `hit_lab`; T06 (POST faltante/duplicado/replay del mismo token por `finalize`) y T08 (generación entre PRE y POST) en `hit_lab`; T19 (fallos de instalación) en ambos; T20 (auditorías negativas) abajo.
- **Mutaciones reales sobre copias temporales (`tests/run_mutations.py`): 16/16 detectadas** (sin puerta de serial, cooldown como candidato, `mpCollider` obsoleto aceptado, generación constante, sin validar generación, todo = espada, confirmar sin proceso, leer collider sin autorización, Finish ignorado, frames obsoletos retenidos, firma sin `mOldActionMode`, serial `<` en vez de `<=`, dedup global, evicción de ACTIVE, dirección reciclada sin retiro, `pair_distinct` siempre). Las dos primeras ejecuciones dejaron **2 supervivientes** (puerta de serial inalcanzable por la ruta normal; contador `pair_distinct`) y obligaron a refactorizar `finalize()` público y añadir comprobaciones: ahora ninguna sobrevive.
- **Negativos de auditoría de fuente: 10/10 rechazados** (escribir `health`, escribir `mpCollider`, `GetTgHitAc`, `HOOK_SKIP_ORIGINAL`, lookup dentro de `do_pre`, leer `mHitType`, segunda desreferencia de collider, `ChkTgHit` derivado, `setActionMode`, escritura vía `out`).
- **Negativos de PE (locales sobre la DLL descargada): 8/8 rechazados** (import mutador plantado, x86, servicio de hook alterado, import `fopAcM_SearchByID` renombrado, nombre del hook alterado, export alterado, import del hook renombrado, símbolo decorado mutador plantado). El PE audit de CI solo ejecuta la auditoría y la comparación con la fijación; estos negativos son locales.
- g++ ASAN/UBSAN limpio. No se usó Clang.

## 6. Límites
- LAB_PASS valida el motor contra un **modelo de la fuente**, no contra el juego. El nombre «HIT_CONFIRMED» significa reacción comprometida (P1+P2), no daño aplicado.
- Las familias reales (`at=0x…`) y el comportamiento de la lectura del collider son [P] hasta tu log. Subtipo de espada, atacante, potencia y ejecución de `cc_at_check`: no disponibles desde este hook.
- Epoch por nombre de stage, `FIRST_SEEN` ≠ spawn, Blue indistinguible (D1), `CalcDivideInfo` sin atribuir, HM/Bars sin reconstrucción byte a byte (heredado). Coexistencia con DEVF/HM/Bars de POST03: no probada.
- El source audit y el PE audit no son una prueba formal de no mutación.

## 8. Cierre humano acotado (añadido el 2026-11-01; solo documental)
Dos logs reales de Windows/DX12 (A: POST03 + Zora Swim, 2/2; B: 8/8 con HM, Bars, DEVF y Expansion) fueron **leídos completos por Claude Code** y verificados por SHA-256; el análisis completo, los 26 eventos saneados, la correlación con la instancia de Link y los criterios de las incidencias están en [`RUNTIME_EVIDENCE_A_B.md`](RUNTIME_EVIDENCE_A_B.md). No se versionan los logs. Resultado: observación, identidad, ciclo de vida y deduplicación en `SCOPED_RUNTIME_PASS`; clasificación de familia **parcial** (`SELECTED_COLLIDER_IMPLAUSIBLE` en 20/24 golpes confirmados, también sin HM/Bars/DEVF). La corrección se desarrolla en `POSTURE_SYSTEM/POST03_1` (`ROOT_CAUSE_RUNTIME_INSTRUMENTED_PENDING`). El código y el artefacto de POST03 no se tocaron.
