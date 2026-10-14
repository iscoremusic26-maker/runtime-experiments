# Matriz CP04

| Gate | Estado | Evidencia / límite |
|---|---|---|
| CP03 humano heredado | CP03_HUMAN_RUNTIME_PASS conservado | Checkpoint139d932; ningún archivo CP03 editado |
| Política HP/observer/registro heredados | SOURCE_VERIFIED | Tres headers copiados byte a byte; único health=150 |
| Propiedad de emisor/color/posición y lifetime | SOURCE_VERIFIED | Native pool + key/owner-tag/callbacks NULL; sin material J3D modificado |
| Contenido concreto common.jpc y aceptación del recurso0x29D | NOT_VERIFIED | No archivo físico inspeccionado; guard obligatorio real en el juego |
|13 casos nuevos de lógica visual/registro | TEST_FAKE_PASS | Run 38584533623 MSVC, mocks/snapshots, no render o adaptador nativo |
| Reutilización sin drift del laboratorio | PASS | Cinco hashes y toolchain/SDK/Aurora/lib idénticos |
| Módulo final Windows/metadata/imports | BUILD_PASS / PE_PASS | Run 38585920329,38 imports, cinco exports y siete records |
| Cuatro negativos PE | PASS | Copias propias rechazadas sin cargar |
| Package oficial/CRC/SHA/DLL igual | PACKAGE_VERIFIED | .dusk y DLL interna propios |
| Descarga real de TEST/TEXT | DOWNLOAD_VERIFIED | Hashes, manifests, source ledger y PE cotejados |
| Aspecto púrpura distinguible en quieto/marcha/combate | HUMAN_RUNTIME_NOT_TESTED | Config readback no es pixels; textura/tonalidad final pendiente |
| Un E_OC2 original, mismo recurso/modelo, inalterado | PENDING / HUMAN_RUNTIME_NOT_TESTED | No reemplazar por E_OC40 ni un mock |
| CP04 HP150, daño/muerte/recarga/reversión | HUMAN_RUNTIME_NOT_TESTED | Herencia CP03 no sustituye ejecución CP04 |
| Recursos reales/rendimiento/eventos y pausas | HUMAN_RUNTIME_NOT_TESTED | Fuente acota recursos; no benchmark/garantía universal |
| CP04_APPEARANCE_RUNTIME_PASS | NO-GO pendiente prueba humana | Offline TEST listo, sujeto al gate de recurso |
| CP05 / CP06 | NOT_AUTHORIZED / NOT_STARTED | No investigados/implementados |

Casos: matching_and_original, shared_asset_private_emitters, single_emitter_anchor, resource_gates, resource_missing, pool_failure, model_missing, config_failure, death_and_reload, next_generation, recycled_handle, shutdown_no_game_access, registration_rollback.

Se prueban identidad/health one-shot sin heal, originales40/220 ajenos, dos emisores con recurso compartido sin escribir asset, mil updates con una creación y un APPLIED, reject de recurso/curvas/luz/model/pool/config, muerte/ID nuevo, key reciclado sin escribir al ajeno, shutdown sin acceso a motor y orden PRE+POST antes de único Stage edit con rollback/reentry/errores. Asset/emitter falsos no prueban renderer real o disponibilidad common.jpc. El adaptador de GameABI se compila/audita, no se invoca en laboratorio.

Primer run 38584533623 SUCCESS completo. Se conservó su texto; TEST de ese run no se declara descargado/verificado. Después se fijó rateStep0 privado para continuidad; segundo run 38585920329 SUCCESS compila esa revisión y verifica PE/negativos/package, reutilizando solo el laboratorio no afectado. Descarga real final posterior PASS. No suites anteriores, ActorService, KCL/WRock/Digpl, build de host o SDK Linux.

Eventos: ARMED=registro y gate aún pendiente; APPLIED=private emitter config readback, no PASS visual; RELEASED en muerte/generación=cut propio o key gone; RELEASED en shutdown=refresh relinquished, no destrucción inmediata en pausa/evento. REJECTED exige STOP y cerrar; nunca vender HP-only como apariencia. Control humano con E_OC2 original requerido antes de runtime PASS.
