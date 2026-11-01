# POST03.1 — Evidencia

Fecha: 2026-11-01. Local: WSL2/Linux; el juego **no** se ejecutó y la DLL **no** se cargó. Etiquetas: [R] juego real (logs del usuario leídos por Claude) · [S] fuente · [B] binario · [C] MSVC/PE/CI · [L] laboratorio con dobles · [P] pendiente.

## 1. Etiquetas
| Etiqueta | Estado | Respaldo |
|---|---|---|
| Evidencia humana POST03 A/B | **incorporada** (26 eventos) | `POST03/RUNTIME_EVIDENCE_A_B.md` + `evidence/` saneada; logs originales leídos completos y verificados por SHA-256 |
| `ROOT_CAUSE_RUNTIME_INSTRUMENTED_PENDING` | causa **plausible por fuente**, sin residuo en el log | `COLLIDER_ROOT_CAUSE_AUDIT.md` |
| `SOURCE_IMPLEMENTED` / `SOURCE_FIX_IMPLEMENTED` | sí | gate de collider con alineación de 4 + diagnósticos |
| `SOURCE_AUDIT_PASS` | sí | CI y local |
| `LAB_PASS` / `DEDUP_LAB_PASS` | sí [L] | `hit_lab` 1660, `lifecycle_lab` 29558, `collider_lab` 12826 (0 fallos) en g++ ASAN+UBSAN y en MSVC; 6 pruebas Python del extractor |
| `WINDOWS_MSVC_PASS` | sí [C] | MSVC 19.51.36260 x64, run 41313246091 |
| `PE_AUDIT_PASS` | sí [C] | los mismos 3 imports de `dusklight.exe` que POST02/03; ninguno nuevo |
| `ARTIFACT_DOWNLOADED_VERIFIED` | sí | descarga independiente en CI y descarga mía |
| `HUMAN_RUNTIME_PENDING` | pendiente | nadie ha cargado POST03.1 |
| `CLASSIFICATION_FIXED`, `CLASSIFICATION_RUNTIME_PASS`, `POST031_RUNTIME_PASS`, `COMPATIBILITY_PASS` | **NO** | requieren log posterior |
| POST03 | `SCOPED_HIT_OBSERVATION_PASS`, `CLASSIFICATION_RUNTIME_PARTIAL` (4/24) | `POST03/RUNTIME_EVIDENCE_A_B.md` |
| G1 · POST02 | `SCOPED_RUNTIME_PASS` | documentos previos |
| G2, G3 | `NOT_STARTED` | |

## 2. Material humano y extractor
- Logs: `dusklight-20261101-081057.log` (325190 bytes, 4250 líneas, SHA-256 `e495427a…b1bb5`) y `dusklight-20261101-080341.log` (875205 bytes, 5396 líneas, SHA-256 `92495e73…47a06`). Coinciden con los valores declarados sin transformación. Se leyeron del disco del usuario con su autorización expresa para esos dos archivos; se copiaron a una carpeta temporal **fuera del repositorio**.
- `tests/extract_runtime_evidence.py` (lista blanca de campos, rechazo explícito de líneas de evento fuera de la lista, escáner de privacidad: rutas, nombres de cuenta, IP, hex largo, direcciones) → `evidence/POST03_AB_EVENTS_SANITIZED.tsv` (26 filas) y `POST03_AB_SUMMARY_SANITIZED.json`. Determinista (dos ejecuciones idénticas byte a byte). Resultado: 26 eventos = 24 `HIT_CONFIRMED` + 2 `FINISH_NATIVE_OBSERVED`; 20 `UNAVAILABLE`, 4 `SWORD`; por instancia de Link: A pid 434 → 6/6 fallan; B pid 105 → 14/14 fallan, pid 506 → 4/4 `SWORD`.
- Diferencias con el resumen recibido: **ninguna** en los números del encargo. Una corrección menor: el extractor inicial leía `inline_sites_flag=1` de la leyenda «(inline_sites_flag=1 => NOT_APPROVED)»; se arregló (valor real: 0) y se añadió una prueba.
- Seguridad: no hay `.log` en el repositorio, ni rutas locales, ni nombres de cuenta ni direcciones; el `.gitignore` de la carpeta excluye `*.log`.

## 3. Git
- Base: `feature/posture-post03-hit-classification-dedup` @ `0a67b19687b5cbaadc4e851ecd7cf4e1340e1b40` (verificado con `ls-remote`; sin avances). Rama de trabajo `feature/posture-post03-1-collider-classification`.
- Código compilado por el run final: **`cab67784e418fbcca0dd99d145eaf7168c50ea4a`**; commit documental posterior en `VERIFICATION.json`/git log. CI: rama `ci/posture-post03-1-collider-classification` (desde `main` @ `9f95a34`), workflow nuevo `posture-post03-1-collider-classification.yml` (solo esa rama), espejo **`ad637a4805a64e69262933325a9d02c989e8f468`** con `POST031_CI_SOURCE.json` (18 archivos con SHA-256).
- `POST03/src`, `POST03/ci`, `POST03/tests`, `mod.json` y el artefacto de POST03: **intactos**. Únicos cambios fuera de `POST03_1/`: `POST03/RUNTIME_EVIDENCE_A_B.md` (nuevo) y metadatos de `POST03/EVIDENCE.md` y `POST03/VERIFICATION.json`. POST01/02, DEVF, HM, Bars, SDK, host, PR #80/#81 y workflows previos: sin cambios. Sin PR, merge, tag ni release.

## 4. Ejecuciones de CI
| Run | Espejo | Resultado | Nota |
|---|---|---|---|
| 41312672161 | `592f123` | éxito | **no ejecutaba `collider_lab`** (faltaba su target); se detectó al revisar los registros y se descartó como candidato |
| 41312890342 | `6ac8a7d` | éxito | con `collider_lab`; sustituido por el siguiente porque el extractor aún no registraba la instancia de Link |
| **41313246091** | **`cab6778`** | **éxito (build + descarga independiente)** | https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41313246091 |

## 5. Ejecución final (41313246091, CI head `ad637a48…e468f`)
- Toolchain: MSVC 19.51.36260 (VCTools 14.51.36231), Windows SDK 10.0.26100.0, CMake 4.4.4, Ninja 1.13.2, `-std:c++20 /O2 /Zc:inline- /GL-`. 9 avisos, todos de cabeceras oficiales. Todos los `static_assert` compilan, incluidos `alignof(cCcD_Obj)==8`, `sizeof(GetAtType())==4`, `mOldActionMode=0x8cc`, `mAtInfo=0x1398`.
- DLL 46080 bytes, SHA-256 `9c50ab0c9703017b918501a9da5528aba2678bc899550b019891055eb7a19517`.
- `.dusk` `POSTURE_POST031_COLLIDER_CLASSIFICATION_windows-amd64_cab67784e418.dusk`: **20534 bytes**, SHA-256 `1f140011a20c4d28bc790af358ccb26d4247f69c3d69399ac72756475ed89cbd`; miembros `mod.json` (idéntico a la fuente) y `lib/windows-amd64/mod.dll`. ID `dev.posture.post03_1_collider_classification`, versión `0.3.1`.
- Artefactos (expiran 2026-12-01): `POST031_TEST_41313246091_1` id **13085797554** (ZIP 21431 bytes, digest `1d1522d3…d813`), `POST031_TEXT_41313246091_1` id 13086017309, `POST031_DOWNLOAD_VERIFIED_41313246091_1` id 13085727877. Enlace directo: https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41313246091/artifacts/13085797554 — la API de Actions confirma que ese id pertenece a ese run y se llama `POST031_TEST_41313246091_1`; la página es privada y no la abrí.
- PE: AMD64; exports `mod_ctx, mod_initialize, mod_meta, mod_shutdown, mod_update`; 1 HOOK_MEM; thunk ligado a `?damage_check@daE_OC_c@@QEAAXXZ`; imports de `dusklight.exe` = `?damage_check…`, `?fopAcM_SearchByID…`, `?dComIfGp_getStartStageName…` (los tres de POST02/03). Verificación local: `sha256sum -c` OK, `unzip` a carpeta vacía, `mod.json == fuente`, `pe_audit.py` PASS, `objdump -p` confirma los tres imports. DLL no cargada.

## 6. Laboratorio, mutaciones y negativos [L]
- `collider_lab` (T01–T10 del encargo + propiedad aleatoria de 6000 casos con un **oráculo independiente**): `reads` exactamente igual a lo que el oráculo exige, `reads ≤ 1` por evento, y la lectura recae siempre en `mAtInfo.mpCollider` (nunca en el otro collider). Casos: `sel=0`, bajo umbral, bien alineado pero distinto del crudo, `sel==raw0` solo cc0, `sel==raw1` solo cc1, dos colliders distintos (cc1 gana, un solo collider leído), mismo collider, doble con `sel` sin coincidencia, `4 mod 8` que coincide (se lee) y que no (no), `mod4≠0` que coincide (no se lee, razón `SELECTED_ALIGNMENT_UNSUPPORTED`), sin `HIT_CONFIRMED` (cooldown, Finish, firma, `mOldActionMode`) y `mpCollider` obsoleto.
- `hit_lab` y `lifecycle_lab` (heredados): T01–T22 de POST03 sobre el modelo de `damage_check`, sin regresión.
- **Mutaciones sobre copias: 25/25 detectadas** (las 16 de POST03 + 9 nuevas: alineación no exigida, alineación de 8 —regresión de POST03—, coincidencia sin igualdad con el crudo, umbral eliminado, cc1 deja de prevalecer, se lee el collider equivocado, doble lectura, lectura sin autorización, desalineado coincidente se lee). **Negativos de auditoría de fuente: 14/14 rechazados** (escrituras, `GetTgHitAc`, `HOOK_SKIP_ORIGINAL`, lookup en el PRE, `mHitType`, segunda desreferencia, `ChkTgHit` derivado, `setActionMode`, `IsBadReadPtr`, `VirtualQuery`, `%p`, hex de 16 dígitos…). **Negativos de PE locales sobre la DLL descargada: 7/7 rechazados** (x86, import/ nombre del hook/ export alterados, símbolo decorado mutador plantado…).
- Límites: punteros opacos, no memoria real; no sustituye a MSVC ni al juego.

## 7. Límites
No hay residuo de puntero en los logs actuales: la causa sigue sin confirmar [P]. La nueva lectura con `mod8_4` es [P] hasta el log. Subtipo de espada, atacante, potencia y `cc_at_check` siguen sin disponibilidad; D1–D5 abiertos; `CalcDivideInfo`/texturas/`PERF_WINDOW` no atribuidos; rendimiento no medido; G2/G3 sin empezar.
