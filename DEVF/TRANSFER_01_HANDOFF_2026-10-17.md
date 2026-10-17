# DEVF — Handoff canónico TRANSFER-01 (2026-10-17)

Referencia persistente para futuras sesiones. Etiquetas de fuente: **SOURCE** (código/documento inspeccionado), **CI** (resultado de GitHub Actions consultado), **USER_TESTIMONY** (aportado por el usuario; no abierto por Claude), **PENDING** (no probado). Los estados históricos de otros documentos fueron correctos en su fecha y no se reescriben; este documento y las notas fechadas añadidas los actualizan.

## 1. Objetivo
Editor Windows (.NET 8 WinForms) que coloca encuentros E_OC2 (Bokoblin nativo) sobre geometría importada localmente del juego GZ2E01 rev0, y dos mods (`.dusk`) que los registran al arrancar Dusklight 2.0.3 (Windows x64 / DX12). Sin cambios de HP, apariencia ni IA.

## 2. Estado por checkpoint

| Hito | Estado | Fuente |
|---|---|---|
| CP08 | 3 Bokoblins E_OC2 vistos en F_SP121 / sala 3 / capa 6; el usuario comprobó que el mod causaba las apariciones | USER_TESTIMONY |
| CP09 | Importación local real de CISO sparse GZ2E01 rev0: 79 escenarios, 305 salas únicas, 384 recursos, 282 con geometría. Geometría vista en F_SP121/R03_00, F_SP113/R01_00, F_SP117/R01_00. Compatibilidad CP08 y reapertura del catálogo OK. **No** implica enemigos en F_SP113 ni F_SP117 | USER_TESTIMONY; build/descarga CP09 en CI: `CP09_UNIVERSAL_GAME_DATA_IMPORTER/TEST_RESULTS.md` |
| CP10 compatibilidad | `CP10_CP08_COMPATIBILITY_HUMAN_RUNTIME_PASS_WINDOWS_DX12`, limitado a F_SP121 / R03 / L6 (sesión A) | USER_TESTIMONY |
| CP10 primera multi-room | `CP10_FIRST_MULTIROOM_HUMAN_RUNTIME_PASS_WINDOWS_DX12`, limitado a F_SP121 / R01 / L6 (sesión B) | USER_TESTIMONY |
| CP10 cierre integral | `CP10_FULL_SCOPE_PENDING` (ver §8) | PENDING |
| CP10.1 | No iniciado ni autorizado | — |
| CP11 | No iniciado ni autorizado | — |

CI CP10: run 38988277707, completed/success, intento 1, jobs `build` e `independent-download` success, head `aff0b5d9f522a1944a15e5cd522a187a5f9b9a6b` (CI, consultado por API GET el 2026-10-17). Un success de CI no prueba gameplay.

## 3. Arquitectura de extremo a extremo
1. CISO/ISO legítimo y local del usuario → `DEVF/CP09_UNIVERSAL_GAME_DATA_IMPORTER/app/Disc.cs` (CISO sparse/ISO), `Archive.cs` (RARC/Yaz0), `Catalog.cs` (descubre `Stage/<id>/R<nn>_<vv>.arc` por ruta).
2. Geometría KCL/PLC/DZR → `Geometry.cs` (CP09) y `DEVF/CP10_MULTI_ROOM_BOKOBLIN_EXPANSION/app/PlacementGeometry.cs` (suelo estático: margen 100, pendiente ≤50, pared ≥200, `y = suelo + 5`).
3. Editor CP10 → `app/Editor.cs` (compatibilidad CP08) y `app/MultiEditor.cs` (schema2): marcador nace desactivado, capa explícita 0–14, habilitar exige confirmación QA.
4. JSON → schema1 (`CP08_MAP_EDITOR_BOKOBLIN_EXPANSION/shared/config.hpp`, sala 3 / capa 6) y schema2 (`app/MultiConfig.cs` ↔ `shared/config.hpp`: tabla de recursos + encuentros con `layer`, `layer_state`, `qa_confirmed`).
5. Consumidor `expansion/` (`dev.bokoblin.expansion` 0.3.0): lee `encounters.json` (≤16384 bytes) en arranque frío, envía el lote de encuentros `enabled`; si uno falla, retira sus tickets en orden inverso.
6. Proveedor `provider/` (`dev.devf.cp06_native_config_dual` 0.10.0): `encounter_broker.hpp` valida, aplica capacidad 8 y llama `StageService.add_actor(stage, room, layer, record)`.
7. Host (`src/dusk/mods/svc/stage.cpp`): guarda la edición; el actor se crea cuando el juego carga la sala y llama `stage_create_new_actors`.

**Edición ≠ actor.** `StageActorHandle`, ticket DEVF y `REQUEST_ACCEPTED` solo prueban que se registró una edición. Los logs DEVF llevan `evidence=STAGE_EDIT_ONLY actor_id=NOT_OBSERVED`, que es esperable y no contradice la observación humana. La aparición solo la prueba la observación en juego. Retirar una edición (`remove edit`, shutdown) no destruye actores vivos.

## 4. Repositorios y construcción
- **Fuente**: `Mods-Duskligh` (privado). **CI/insumos**: `codex-cp00-inputs` (privado).
- La CI compila el **espejo** `codex-cp00-inputs/DEVF/CP10_MULTI_ROOM_BOKOBLIN_EXPANSION/` (idéntico al directorio del repo fuente salvo `SOURCE_CI.json`). `SOURCE_CI.json` fija `source_commit=42fc874…` y 107 blobs git (30 CP10, 40 CP07_2B, 19 CP08, 14 CP09, 2 CP01, 2 CP06); `ci/run_windows.py` comprueba cada blob. **Modificar el repo fuente no actualiza el espejo ni la CI.** No tocar espejo ni pins sin encargo.
- Workflow: `codex-cp00-inputs/.github/workflows/devf-cp10-map-editor.yml` (PR head `ci/devf-cp10-multi-room`, base `ci/devf-cp09-universal-importer` con SHA `c6e20919e0f0d9ae3139879974c4e50220b1e429`; runner windows-latest; .NET 8; MSVC x64).
- `.lib` oficial: se extrae de `Dusklight-v2.0.3-win32-x86_64.zip` (LFS, repo CI, commit de insumos `9f95a34…`): `sdk/windows-amd64.lib`, 9 400 986 bytes, SHA256 `4dc4a511d761e6eb52541733fa31919a2234ed9cd5b2f16f8fea91c468f30ca4`.
- Salida: `DEVF Map Editor CP10.exe` (self-contained win-x64), `DEVF_Provider_0.10.0_TEST.dusk`, `BokoblinExpansion_0.3.0_TEST.dusk`, `SOURCE_COMPILED.zip`, `MANIFEST.json`, `SHA256SUMS.txt`, dentro de `DEVF_CP10_MAP_EDITOR_TEST.zip`. El job `independent-download` rebaja el artefacto y verifica tamaños, SHA256, CRC, PE/ABI y ledger de fuentes.
- En Ubuntu no hay MSVC ni .NET: solo lectura, `gh` y revisión. No se compila aquí. No descargar LFS ni modificar el host.

## 5. Referencias fijadas (SHA completos)
| Elemento | Valor | Origen |
|---|---|---|
| Fuente CP10 (base congelada) | `42fc87455624bde8b898a26a0512f708f02a3b26` | git; PR #50 draft, base `feature/devf-cp09-universal-importer` |
| CI CP10 (base congelada) | `aff0b5d9f522a1944a15e5cd522a187a5f9b9a6b` | git; PR #36 draft, base SHA `c6e20919e0f0d9ae3139879974c4e50220b1e429` |
| Dusklight oficial | `TwilitRealm/dusklight@40457c6adb381928e4b5fef6ed459ed291edd5e2` | workflow |
| Aurora | `encounter/aurora@3227d76c60e1e782ca576610bce61c9e7744d8be` | workflow |
| CI run | `38988277707` | API GET, 2026-10-17 |
| Artefacto TEST | id `12083854081`, `DEVF_CP10_MAP_EDITOR_TEST_38988277707`, 65 714 979 bytes | API GET, 2026-10-17 |
| Rama documental | `docs/devf-transfer-01` (parte de 42fc874) | rama separada; no sustituye a las bases |

Las referencias HEAD son bases congeladas a la fecha; el worktree documental es una rama aparte con solo documentación.

**Caducidad.** El artefacto TEST expira el 2026-11-16T00:54:16Z (informado por la API). Cuando el usuario lo decida, debería descargarlo y archivarlo localmente junto con su `MANIFEST.json` y SHA. No se descargó ni se copió a Git en esta etapa. El `MANIFEST.json` empaquetado dice `HUMAN_RUNTIME_PENDING` porque se generó en la build, antes de la QA humana; no se altera.

## 6. Invariantes
- IDs de mod `dev.devf.cp06_native_config_dual` y `dev.bokoblin.expansion`; servicios @1.0; structs C ABI de 80 bytes (solicitud) y 24 bytes (servicio) según `CP10/IMPLEMENTATION.md`. No mezclar dos versiones del mismo ID.
- E_OC2 nativo, perfil 510, parámetros `0xFFFF0100`. Sin cambios de HP, apariencia ni IA.
- Capacidad global 8 incluyendo placements legacy del proveedor (tres legacy = tres slots). El 8 vive en el broker DEVF, en los arrays del cliente y en el límite de 16384 bytes del JSON; no en el host.
- Separación 300 entre activos del mismo room/layer; ids globales únicos; posición igual en distinto contexto no es duplicado.
- Paridad schema1/schema2 C#↔C++ (`MultiConfig.cs` ↔ `shared/config.hpp`); el corpus C#→C++ de la CI lo ejercita.
- Recursos: ruta normalizada + hashes ARC/KCL/PLC + bounds, autorización `STATIC_QA_NOT_RUNTIME_VERIFIED`. El JSON es autorización local de QA, no un certificado firmado.
- Arranque frío; sin hot reload; rollback = cerrar el juego, retirar la pareja CP10, restaurar la pareja CP08 (provider 0.8.0 / expansion 0.2.0) y los JSON respaldados (`CP10/RECOVERY.md`). La instalación del editor hace respaldo verificado.

## 7. Regresión FLOOR_AMBIGUOUS (no perder)
El primer intento de CP10 (run 38960997596) falló con `FLOOR_AMBIGUOUS` al migrar las posiciones CP08. Corrección (commit `e2e44c0`, `PlacementGeometry.cs`): la ruta `layer_state == "CP08_OBSERVED"` exige R03_00.arc auténtico (`Geometry.Hash` = `dc53106667811c4cde18b35edb5279357f00ebecaef2f9de546aea9a5a2b06af`), F_SP121 / sala 3 / capa 6 / variante 00, y delega en `Config.Validate` + `Config.GeometryCheck` del CP08 con `Geometry.LoadBytes` histórico, sin reescribir sus cálculos ni tolerancias. **No aplicar ese bypass a puntos `QA_CANDIDATE`**, ni siquiera en la sala 3 (lo cubre el test `new-QA-room3-does-not-use-legacy-bypass`).

Coordenadas originales CP08 (transcritas del reporte del usuario):
- bokoblin-001: (-1334.75342, -6339.34229, 60011.2109)
- bokoblin-002: (-1805.60547, -6375.58301, 60777.1289)
- bokoblin-003: (-1039.68616, -6316.24902, 61329.5977)

## 8. Evidencia humana CP10 (dos sesiones, Windows / Dusklight 2.0.3 / D3D12)
Logs aportados por el usuario y resumidos; **Claude no los abrió** (están en AppData de Windows). Todo lo siguiente es USER_TESTIMONY / análisis aportado.

- **Sesión A** — `dusklight-20261016-200848.log`: provider 0.10.0 + expansion 0.3.0 (fuente 42fc874); 3 `REQUEST_ACCEPTED` (bokoblin-001/002/003, F_SP121 / R03 / L6, tokens 1–3). El usuario vio los tres Bokoblins aparecer y comportarse normalmente. 0 entradas `[ERROR`/`[FATAL` según la revisión comunicada.
- **Sesión B** — `dusklight-20261016-201248.log`: mismas versiones; cuatro `REQUEST_ACCEPTED`; bokoblin-004 en F_SP121 / R01 / L6, XYZ=(-25050.2812, -8097.86523, 80595.0703), yaw 0, token 4. El usuario vio aparecer ese cuarto enemigo correctamente. 0 `[ERROR`/`[FATAL`. La sesión B **no** es prueba visual independiente de los otros tres.
- Los logs solo prueban ediciones aceptadas; el PASS de aparición es testimonio humano. Cero ERROR/FATAL no equivale a ausencia universal de problemas.

**CP10_FULL_SCOPE_PENDING** (no forzar ahora): desactivación individual de bokoblin-004 y reinicio; una segunda sala nueva distinta de R01 y R03; otras capas, estados de juego y cambios de etapa. Ninguna capa es "certificada" por `_00` ni por chunks ACTn. No existe PASS universal.

## 9. StageService oficial (host 40457c6, SOURCE)
`src/dusk/mods/svc/stage.cpp`: `s_edits` es un mapa por nombre de escenario (L41); `current_stage_edits()` busca por `dComIfGp_getStartStageName()` (L57–67); `stage_create_new_actors` exige `room` exacta y usa `layer_matches`, que admite `-1` (L73–75, L139–154); `stage_add_actor_` rechaza `room == 0xFF` y valida nombre ≤8 (L270–289). `sdk/include/mods/svc/stage.h`: comodines `0xFF`/`-1` solo para patch/delete; `add_actor` requiere sala específica. DEVF prohíbe además el comodín de capa. El host ya contempla varios nombres de escenario; **el funcionamiento multi-stage de DEVF no está demostrado en runtime** y no se asume que haya que parchear el host. El bloqueo actual está en literales DEVF (`F_SP121`, salas 1–5, variante 00) en `MultiConfig.cs`, `shared/config.hpp` y `PlacementGeometry.cs`, más el validador `scene()` del broker (no inspeccionado a fondo). `getStartStageName()` en distintas transiciones: INCIERTO.

## 10. Riesgos conocidos
1. Pérdida de la delegación legacy (ver §7).
2. Divergencia C#↔C++ al generalizar escenas/salas (literales en tres sitios).
3. Subir el límite 8 toca broker, arrays, tamaño de JSON, separación y pruebas.
4. Capa: depende del estado de juego (`getLayerNo(0)`); R03/L6 y R01/L6 funcionaron en las sesiones observadas, sin generalizar.
5. Suelo estático ≠ colisión dinámica; ni catálogo ni log prueban aparición.
6. Espejo CI y fuente pueden divergir si se edita uno solo.
7. Caducidad del artefacto (§5).

## 11. Continuidad con gates humanos
Transfer-01 (esto) → aprobación del diff → commit/push/PR solo con autorización → cierre CP10 (ensayos pendientes, decididos por el usuario) → CP10.1 (nombres de stages/rooms) → CP11 (multi-stage).

- **CP10.1** (futuro, no autorizado): catálogo de nombres con tres columnas: documentado (con fuente), inferido (con confianza) y sin determinar. Conservar el ID interno. No inventar nombres; no usar el sufijo ARC como capa.
- **CP11** (futuro, no autorizado): comprobar restricciones DEVF, disponibilidad de E_OC2, recursos y capas por escenario; regresiones CP08/CP09/CP10 y primera QA humana antes de cualquier GO.

## 12. Índice de documentos
- Este archivo y `CLAUDE.md` (raíz): estado y reglas.
- `DEVF/CP10_MULTI_ROOM_BOKOBLIN_EXPANSION/`: README, IMPLEMENTATION, HUMAN_TEST, TEST_RESULTS, RECOVERY, CP11_HANDOFF (con notas fechadas del 2026-10-17).
- `DEVF/CP09_UNIVERSAL_GAME_DATA_IMPORTER/`: TEST_RESULTS, CP10_HANDOFF.
- `DEVF/CP08_MAP_EDITOR_BOKOBLIN_EXPANSION/`: contrato schema1 y validadores.
- Evidencia CI: página del run 38988277707 (Actions, repo `codex-cp00-inputs`); artefactos `DEVF_CP10_TEXT_*` y `DEVF_CP10_DOWNLOAD_VERIFIED_*`.
- Historia: `DEVF/RESUME_INSTRUCTIONS.md`, `GO_NO_GO.md`, `CHANGES.md` son de CP00 (con nota de navegación).
