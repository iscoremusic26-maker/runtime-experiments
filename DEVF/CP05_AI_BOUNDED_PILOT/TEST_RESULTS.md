# CP05 — Resultados reales y límites

**CP05_AI_BOUNDED_PRIVATE_TEST_READY / HUMAN_RUNTIME_NOT_TESTED**.

| Gate | Estado | Evidencia y límite |
| --- | --- | --- |
| Fuente exacta/propiedad/campo | GO_SOURCE_ONLY | SOURCE_AND_AI_GATE; record efectivo percepción5000/move600; modificación temporal propia mPlayerRange. No runtime heredado. |
| MSVC AMD64 | BUILD_PASS | [run38672691356](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38672691356), job116219222220; cl19.51.36260/VCTools14.51.36231/SDK10.0.26100.0; CMake/Ninja, host/CP03/CP04 no compilados. |
| Core de IA nuevo | LAB_PASS29 / OFFLINE_ONLY | ai_lab.exe ejecutado en Windows y LAB_PASS cases=29 exigido por el runner; mismo ai_core.hpp que DLL. |
| Identidad/retail/shared aliasing | PASS OFFLINE_ONLY | Dos actores con mismo puntero fake de model/textura/HIO; sólo rango del elegido cambia/restaura. No prueba de GPU/IA real. |
| Gen/epoch/contexto/no crear/modelo nulo | PASS OFFLINE_ONLY | Casos de snapshot no-ready y generación equivocada; rama nativa null model inspeccionada/compilada. No provocación real de fallo de heap del juego. |
| Entry1200/retención1400/grace30/reset/retorno500 | PASS OFFLINE_ONLY | Fronteras estrictas y contador saturado; no modificación ni wrap de timers nativos. WALK/pathfinding del juego NO ejecutado. |
| Daño/hit/stun/ataque/demo/fall/death/event | PASS OFFLINE_ONLY + fuente | Overrides sólo en WAIT/WALK/FIND seguro; pérdida HP/estado cancela; native damage_check primero conserva prioridad. No equivalencia con animación real. |
| Callback/nested/overflow/missingPOST/null/otro writer | PASS OFFLINE_ONLY | Restauración exterior, sentinel inicial, stack8/overflow, recuperación por identidad y rechazo de writer ajeno. HookService backend real no ejecutado por laboratorio. |
| PE/ABI/imports/export/typed hooks | PE_ABI_PASS | AMD64/PE32+,8 metadata records/5 services/2 PMFs8bytes unidos a imports exactos,5 exports; TLS/delay imports ausentes. Tres queries nuevas revisadas, sin nuevo target hook. |
| Negativos | PASS6 | x86, hook target, hook service, export, ARC extra, traversalZIP: rechazados sin cargar DLL. |
| Paquete oficial | PACKAGE_VERIFIED | Dusk 18929 bytes; manifest/DLL idénticos al build, CRC y miembros exactos. |
| Descarga real nueva | DOWNLOAD_VERIFIED | [run38672879974](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38672879974), job116219818583; artifacts realmente descargados, digest/CRC de todas las capas, SourceZip/ledger/manifiesto/DLL/PE comprobados, sin build ni game. |
| Fuente principal↔CI | REPO_VERIFIED | Los16 blobs del commit compilado y espejo CI son idénticos por Git; todos los blobs/modes del baseline f7 se conservan. |
| Negro150/guardia/persecución/desistimiento/retorno/combate/muerte/reentrada/rollback CP05 | HUMAN_RUNTIME_NOT_TESTED | Necesita prueba del usuario; CP04 humano no demuestra IA CP05. |
| E_OC2 retail idéntico simultáneo / terceros / FPS / otras GPU | NOT_TESTED / PENDING | No aislamiento universal, compatibilidad o performance general. |

## Incidencias y correcciones CP05

- Checkpoint temprano c01bb2e9 documentó5000/600 antes de implementar.
- Revisión incremental propia corrigió admisión dentro del sentinel PRE, recuperación con sentinel nested y cierre de interés al observar WAIT nativo; añadió3 casos, total29. Estas correcciones son CP05, sin tocar host ni CP04.
- Runs38672308497/38672430131 compilaron/laboratorio pero PE bloqueó query ChkTgHit no revisada. Run38672586306 exigió owner ABI derivado exacto. Se contrastaron include/d/d_cc_d.h283–295 y src/d/d_cc_d.cpp221–229: wrapper dCcD_GObjInf::ChkTgHit(), retorna u32 y consulta el hit nativo. Allowlist final exacto, no se desactivó auditoría.
- Run38672691356 pasó build29/PE/6 negativos/package. Ningún TEST de esos runs fallidos se entregó como listo.
- Run38672879974 pasó descarga independiente, sin reconstruir.

No20 pruebas de render CP04 ni17 CP03 repetidas. xf_scope.hpp y bloque visual son idénticos salvo ID/versión del nuevo mod. No ARC/32fuentes/render investigados de nuevo. El core no tiene allocation dinámica; no hay prueba de OOM/abort fatal del host ni promesa de recuperar esos errores.
Logs AI_EVENT_OBSERVED significan transiciones lógicas, no BEHAVIOR_VISUALLY_VERIFIED. Código/logs/paquete CP04 sin cambios.
