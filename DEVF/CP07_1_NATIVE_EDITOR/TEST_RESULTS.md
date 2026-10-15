# Matriz CP07.1

| Gate | Resultado |
| --- | --- |
| CP06 BOTH/FIELD/NORTH/NONE humano anterior0.6.2 | PASS USER_HUMAN_REPORTED, cierre separado |
| Core CP06/parser/IO/records/Stage,109casos copiados intactos | PASS Windows |
| Toggle FIELD/NORTH, borrador/guardado, Guardar/Descartar, cerrar/reabrir | PASS OFFLINE, callbacks reales de la nueva clase UI con servicio doble |
| Persistencia4modos y reinicio simulado, IDs compatibles | PASS OFFLINE |
| Archivo ausente/creación explícita, inválido/corrupto/acceso fallido | PASS OFFLINE; nunca fallback de aparición |
| Backup exclusivo/verificado, capacidad32, no sobrescribir backup | PASS OFFLINE |
| Fallos create/open/write/flush/close/readback y excepciones | PASS OFFLINE; original intacto o restauración, respaldo conservado |
| Recuperación fallida | PASS OFFLINE: error visible y guardado bloqueado; no garantía de recuperar bajo fallo persistente |
| Cambio externo antes/después de backup | PASS OFFLINE: rechaza overwrite |
| UI ausente/versión/API errónea, handles/callbacks/cleanup | PASS OFFLINE; core conservado |
| Getters/predicados, close/shutdown sin IO/spawn | PASS OFFLINE |
| Total tests | **109 base +55editor =164 PASS** |
| MSVC Windows AMD64 / PE/ABI / package oficial | PASS |
| Negativos PE/ZIP | **11 PASS** |
| Descarga REAL independiente y SHA/CRC/DLL/fuentes/ejemplos | DOWNLOAD_VERIFIED |
| Menú visible, interacción y guardado en juego0.7.0 | HUMAN_RUNTIME_PENDING |
| Reinicio real BOTH→FIELD→BOTH con editor | HUMAN_RUNTIME_PENDING |
| FPS/terceros/universalidad/power loss atomicidad | NOT_VERIFIED; atomicidad NO OFRECIDA |
| CP07.2/CP08/identidad personalizada | NO IMPLEMENTADOS |

Laboratorio sobre los headers reales usados en la DLL, dobles sólo de Host/File/Stage/UI. IO de editor usa archivos Windows reales en carpeta temporal del runner; fallos de permisos/servicios se inyectan en los adaptadores, no son ensayos de ACL del PC del usuario. No simulación del juego/GPU ni prueba visual por eventos.

[Build38770105933](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38770105933) SUCCESS; [descarga38770449006](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38770449006) SUCCESS. Nombres/tiempos de todos los casos y resultados completos en evidence/. No DLL ni juego ejecutados.

Primer run38769637138 FAILURE tras164PASS por imports nuevos detectados. Se retiró guard estático innecesario, se justificó delta exacto CRT y se volvió a ejecutar. No cambios al host ni al auditor histórico. Los11negativos cubren x86, export/servicios incorrectos, Stage/File majors, asset extra/traversal y UiService versión/ID/flag requerido en lugar de opcional.

Estado **CP07_1_EDITOR_QA_BUILD_READY**. El PASS humano de0.6.2 no se transfiere al editor. No repetir sus cuatro ensayos para esta tarea: HUMAN_TEST propone sólo flujo nuevo de edición.
