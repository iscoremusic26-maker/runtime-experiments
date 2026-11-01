# POST04 — Evidencia

Fecha: 2026-11-01. Local: WSL2/Linux; el juego **no** se ejecutó y la DLL **no** se cargó. Etiquetas: **[R]** juego real (logs del usuario) · **[S]** fuente · **[C]** MSVC/PE/CI · **[L]** laboratorio con dobles · **[P]** pendiente.
POST04 es un checkpoint **independiente** del cierre documental de POST03.1; su estado de ejecución es `HUMAN_RUNTIME_PENDING`.

## 1. Etiquetas
| Etiqueta | Estado | Respaldo |
|---|---|---|
| `POST04_SOURCE_IMPLEMENTED` | **sí** | `src/posture_core.hpp` + `mod.cpp` |
| `LAB_PASS` (g++ ASAN+UBSAN **y** MSVC) | **sí** [L][C] | §4 |
| `SOURCE_AUDIT_PASS` | **sí** | `ci/source_audit.py` (reglas nuevas §5) |
| `WINDOWS_MSVC_PASS` / `PE_AUDIT_PASS` | **sí** [C] | §6 |
| `POST04_WINDOWS_BUILD_VERIFIED` | **sí** [C] | §6 |
| `ARTIFACT_DOWNLOADED_VERIFIED` | **sí** | §6 (descarga independiente en CI + mía) |
| `POST04_HUMAN_RUNTIME_PENDING` | **true** | nadie ha cargado POST04 en Dusklight |
| `POST04_RUNTIME_PASS`, `COMPATIBILITY_PASS` | **NO** | requieren log posterior |
| `TIMEBASE_PAUSE_UNVERIFIED` | **sí** | `POST04_POSTURE_POLICY.md` §5 |
| POST03.1 | `POST031_A1/B1_SCOPED_RUNTIME_PASS`, `CLASSIFICATION_SCOPED_RUNTIME_PASS` (acotado) | `POST03_1/RUNTIME_EVIDENCE_A1_B1.md` |
| G2, G3 | `NOT_STARTED` | |

## 2. Procedencia
- Base: cierre documental de POST03.1 `509c6926fbba3d007bc3fba32bbb37c10436fa25` (rama `feature/posture-post03-1-collider-classification`); código compilado de POST03.1 `cab67784e418fbcca0dd99d145eaf7168c50ea4a`. Rama de POST04: `feature/posture-post04-numeric-core`.
- `POST00`–`POST03_1`: **0 diferencias** frente a `509c692`. Cambios de código respecto a POST03.1: ver `POST04_ARCHITECTURE_AND_LIFECYCLE.md` §2 (`hit_core.hpp` 0, `engine.hpp` +1 línea).
- Verificado al empezar: ramas remotas de POST03.1 (fuente `c63d05a`, CI `ad637a4`) sin movimiento; `main` del repo de CI `9f95a34`.

## 3. Evidencia real que respalda el diseño [R]
- Cierre humano A1/B1 de POST03.1 (36 eventos: 33 `HIT_CONFIRMED` + 3 Finish; SWORD 23, IRON_BALL 4, BOOMERANG 1, OTHER_VERIFIED 5, UNAVAILABLE 0; 21 colliders `mod8_4`): `POST03_1/RUNTIME_EVIDENCE_A1_B1.md`.
- De ella salen las decisiones de política: `OTHER_VERIFIED` (5) y el bumerán sin pérdida de HP (`hp=55>55`) pesan 0; los Finish (3) no son golpes; los actores de A1 (40 HP) mueren en 1–2 golpes; los de B1 (con HM) sobreviven a varios.
- Base de tiempo: `kSimPeriod = 1/30 s` en el código fuente y, en B1, 27 ventanas de Expansion con 8100 ticks en 270,6 s (33,41 ms de media por tick).

## 4. Laboratorios y mutaciones [L][C]
| Laboratorio | g++ ASAN+UBSAN | MSVC (CI) |
|---|---|---|
| `hit_lab` (heredado) | 1660 comprobaciones, 0 fallos | 1660, 0 fallos |
| `lifecycle_lab` (heredado) | 29558, 0 | 29558, 0 |
| `collider_lab` (heredado) | 12826, 0 | 12826, 0 |
| `posture_lab` (nuevo) | **556878, 0** | **556878, 0** |
Los tres heredados mantienen exactamente sus conteos de POST03.1 (sin regresión); solo cambian dos aserciones de contrato (presupuesto de log 1500 y `v=0.4.0`).
`posture_lab`: T01–T28 del encargo (T28 son las mutaciones; T21 **declara** el comportamiento del reloj, no mide pausas reales) más T00 (tabla de pesos exacta y techo de 2000 líneas), T29 y T30; **T27** compara **555 627** estados contra un oráculo independiente en 8 semillas fijas × 12000 cuadros (656 golpes ponderados, 108 cruces, 4393 unidades recuperadas, 240 carreras de recuperación, 757 congelaciones, 66 muertes; el propio lab exige cobertura mínima para no ser vacuo); **T29** repite los 36 eventos reales de A1/B1 contra la decisión esperada de un generador Python independiente (A1: 8 `LETHAL` + 4 `ZERO_WEIGHT`; B1: 12 ponderados, 6 `LATCHED`, 2 `ZERO_WEIGHT`, 1 `LETHAL`, 3 Finish, 3 cruces, 1 saturación) — **solo acumulación**, los logs no traen ticks; **T30** cubre rutas de defensa en profundidad.
- **Mutaciones: 80/80 detectadas** (25 de lógica heredadas, **28 de postura**, 27 de pasividad rechazadas por `source_audit`). Una mutación (N06) se detecta por tiempo límite (cuelga el laboratorio).
- Hallazgos propios del control de mutaciones, corregidos: 4 mutantes de postura sobrevivieron a la primera versión del laboratorio (rutas de defensa en profundidad y el orden PRE/POST con el mod deshabilitado) → se añadió T30; el extractor de POST04 tenía una aserción vacía (`… or True`) en su test de `delete_claim` → se reemplazó (8/8 mutaciones del extractor detectadas).
- Herramientas: `tests/test_post04_tools.py` (11 pruebas: generador determinista y actual, muestra del formateador idéntica entre g++ y MSVC, privacidad, hash/bytes/líneas, tags fuera de lista blanca, violaciones de invariantes, determinismo).

## 5. Auditoría de fuente [S]
Reglas heredadas más: sin memoria dinámica/E/S/hilos (`new`, `malloc`, `std::vector|map|string|function|mutex|thread|atomic`, `fopen`, `std::cout`, `printf`…), sin dependencias de HM/Bars/DEVF/Expansion, solo servicios `Host/Log/Hook`, núcleos puros con solo cabeceras estándar y locales, `posture_core.hpp` sin `uintptr_t` almacenado, un único `advance()` y un único `consume()`, un solo `g.pe.on_update()` dentro de `do_update`. 27 violaciones plantadas (S01–S27): **27/27 rechazadas**.

## 6. CI Windows, PE y artefacto [C]
- **Toolchain:** MSVC 19.51.36260 x64 (VCTools 14.51.36231, Visual Studio 18.0), Windows SDK 10.0.26100.0, CMake 4.4.4, Ninja 1.13.2. SDK oficial `40457c6adb381928e4b5fef6ed459ed291edd5e2`, Aurora `3227d76c60e1e782ca576610bce61c9e7744d8be`, ZIP de Windows y biblioteca de importación fijados por SHA-256; `dusklight.exe` `ffa99203…0049`. Todos los `static_assert` de ABI compilan (offsets de `health`, `actor_status`, `mActionMode`, `mOldActionMode`, `mOcState`, `field_0x6cc`, `mAtInfo`; `alignof(cCcD_Obj)==8`; `sizeof(GetAtType())==4`).
- **Run final `41320296108`** (https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41320296108): `build` e `independent-download` en **éxito**. Compila `ccf0f2d2b7b12092cf3407ae49bc8ba42a8ebd64`; espejo de CI `9578db97647e9f60a33ad779182af4519158f78b` (25 archivos; libro de control `POSTURE_SYSTEM/POST04_CI_SOURCE.json` verificado de forma independiente: libro = commit fuente = rama de CI, byte a byte, ningún archivo fuera del libro).
- **En el runner Windows:** `tool-tests` OK; `source-audit` PASS; 4 laboratorios con MSVC (1660 / 29558 / 12826 / **556878**, 0 fallos); la muestra del formateador de MSVC es **idéntica** a la de g++ y el extractor la acepta; DLL; **PE_AUDIT_PASS**; **11/11 negativas PE rechazadas** sobre la DLL real; paquete `.dusk`; entrega.
- **PE** (DLL 58368 bytes, SHA-256 `84c3fb46b7ee2e3791a7d4be6d090018c04ad0660e634c47f1ff9a26643b27d9`): AMD64; exports `mod_ctx, mod_initialize, mod_meta, mod_shutdown, mod_update`; 1 `HOOK_MEM` enlazado al thunk `?damage_check@daE_OC_c@@QEAAXXZ`; imports de `dusklight.exe` = **los mismos 3 que POST03.1** (`damage_check`, `fopAcM_SearchByID`, `dComIfGp_getStartStageName`; 0 nuevos); un import CRT nuevo respecto a POST03.1, `memset` de `VCRUNTIME140.dll`, generado por el compilador para poner a cero los arrays fijos (el auditor de fuente prohíbe escribirlo y pasa); sin TLS ni delay-imports.
- **Negativas PE (11)**: arquitectura i386, import del juego alterado, import mutador del sistema (`WriteProcessMemory`), import CRT nuevo, export alterado, registro `HOOK_MEM` con otro método (parcheado dentro de `modmeta`), hook reenlazado a otro símbolo, dependencia alterada, import del juego no revisado, archivo truncado, cabecera corrupta. Mi primer N6 parcheaba la primera aparición de la cadena en el archivo (una cadena de log) y pasaba; no era un hueco del auditor sino un caso mal apuntado, y se rehízo apuntando a `modmeta`.
- **Artefactos** (expiran 2026-12-01): `POST04_TEST_41320296108_1` id **13089436064** (ZIP 29018 bytes, digest `sha256:cc982b568f1468df27e9af4a37857b05a862530b675915e76b0613ce015b3ac3`, igual al SHA-256 que calculé al bajarlo por la API **por id**); `POST04_TEXT_41320296108_1` id 13089001397; `POST04_DOWNLOAD_VERIFIED_41320296108_1` id 13088767272.
- **Paquete** `POSTURE_POST04_NUMERIC_OBSERVER_windows-amd64_ccf0f2d2b7b1.dusk`: **28145 bytes**, SHA-256 `d43e46b37760f93090f162e3807f6b70640695dccda61870836000d1bf42f8f7`; miembros exactos `mod.json` (idéntico al del commit fuente) y `lib/windows-amd64/mod.dll`; ZIP íntegro; ID `dev.posture.post04_numeric_observer` v0.4.0. `DOWNLOAD_MANIFEST.json` y `SHA256SUMS.txt` coinciden.
- **Historial de runs (nada se oculta):**
| Run | Resultado | Motivo |
|---|---|---|
| 41319547787 | fallo | `PE_AUDIT_FAIL`: aparecía `memset` (CRT) respecto al pin de POST03.1; se revisó, se justificó y se fijó en `expected_pe.json` |
| 41319804337 | fallo (tras construir y auditar bien) | bug de MI script de cierre: un directorio dentro de `evidence/` rompía el cálculo de hashes; corregido |
| 41320016172 | éxito | candidato intermedio (`3183d83`); sustituido porque aún no ejecutaba las negativas PE |
| **41320296108** | **éxito (build + descarga independiente)** | candidato final `ccf0f2d` |
- **No se hizo:** instalar ni abrir Dusklight; cargar la DLL; PR, merge, tag ni release.

## 7. Límites
- Todo lo anterior es evidencia de **fuente, laboratorio y compilación**; ningún dato de juego de POST04 existe aún.
- El tiempo está en ticks del observador (1/30 s nominal a escala 1): la recuperación durante menús o pausas no está verificada (`TIMEBASE_PAUSE_UNVERIFIED`).
- Sin medición de rendimiento. Sin cobertura en juego de ARROW, BOMB, SHIELD_ATTACK, SLINGSHOT y AT_TYPE_40; `OTHER_VERIFIED` no identifica arma.
- Los valores de política son provisionales; que un Bokoblin de 40 HP no llegue al umbral no es un fallo de POST04.
- D1–D5 siguen abiertas. G2 y G3: `NOT_STARTED`. POST05–POST08: no iniciados.
