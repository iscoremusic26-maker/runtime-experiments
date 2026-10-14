# Matriz de resultados del diagnóstico

| Gate | Estado | Evidencia / límite |
|---|---|---|
| Baseline v0.3.0 en Windows/DX12 | USER_REPORTED | 220→150 para147/581/784, combate/muerte/respawn normales; no medición por impacto |
| Política/payload/única escritura preservados | SOURCE_VERIFIED | policy.hpp byte-exact, stage_record igual, una sola asignación health150 |
| Vida entre PRE y POST | SOURCE_VERIFIED | Eliminación en cola; free en handler externo. No fallo real provocado |
|17 casos nuevos de Observer/Registration | PASS TEST_FAKE | Run 38540468476, procesos separados, exit0; no actor real, DLL o backend |
| Reutilización de esos 17 casos | PASS | Hashes de seis archivos, SDK/Aurora/lib/toolchain verificados |
| Compilación MSVC y metadata/imports reales | BUILD_PASS / PE_PASS | Run 38541018826, AMD64, cinco exports, siete records, 29 imports |
| Cuatro negativos PE | PASS | Copias x86/servicio/target/export rechazadas, no cargadas |
| Paquete oficial y DLL igual a loose | PACKAGE_VERIFIED | CRC/rutas/manifest0.3.1/SHA/miembros |
| Descarga real de TEST y TEXT | DOWNLOAD_VERIFIED | Fuente/CI/manifest/ledger/PE/DLL/ZIPs cotejados |
| HP_DELTA real, orden y pérdida por ventana | HUMAN_RUNTIME_NOT_TESTED | Requiere nuevo log Windows/DX12 |
| Golpe mortal, incrementos y ausencia de reset | HUMAN_RUNTIME_NOT_TESTED | No atribución de ataque o potencia bruta |
| Recursos/render/combate/retirada de v0.3.1 | HUMAN_RUNTIME_NOT_TESTED | Baseline humano no sustituye diagnóstico nuevo |
| CP03_DIAGNOSTIC_PASS_RUNTIME / estable | NO-GO pendiente evidencia humana | Piloto offline listo para prueba controlada |
| CP04 / CP06 | NOT_AUTHORIZED | No iniciados |

Casos: initial_baseline, hits_and_unchanged, zero_unknown, readonly_increase, originals_silent, new_generation, nested_ignored, reentrancy_failclosed, depth_failclosed, post_identity_failclosed, queued_deletion, shutdown, cap_and_between, registration_pair_order, post_partial_failures, missing_post, stage_partial_failures.

Cobertura fake: inicial220→150 sin pérdida 70, cambios150→115→100 con ventana sin cambio, truncado20→0 UNKNOWN_OR_SPECIAL, incremento sin escritura/curación, originales no coincidentes y llamada ignorada anidada, generaciones 147→581, reentrada propia y profundidad excesiva rechazadas, POST inválido, eliminación en cola con memoria aún viva hasta POST, shutdown, límite 32/aviso único y cambios entre executes. Registro PRE+POST antes de Stage, errores/excepciones de instalación POST, servicio POST ausente, stage error/handle cero y rollback. El mock no prueba el backend real; su seguridad se fundamenta por fuente.

Run 38540468476: BUILD y17/17 PASS, gate de imports detuvo TEST por __std_terminate nuevo. Se revisó proveedor VCRUNTIME140 y superficie exacta; solo cambió auditoría/CI. Run 38541018826: SUCCESS, negativos/package PASS, descarga real posterior PASS. Código C++/headers/tests/CMake no cambian desde107dbdf.

No se ejecutan suites CP00/CP01/CP02/CP03 históricas, A0/A1, G5, KCL/WRock/Digpl o SDK Linux. Logs de CI propio se conservan byte a byte y saneados; no raw logs personales. El bridge real se compila/audita pero no se invoca en CI. Eventos fake no son mediciones del juego. No clasificación FORCED_ZERO/SPECIAL sin ruta observada; aquí cero siempre UNKNOWN_OR_SPECIAL.
