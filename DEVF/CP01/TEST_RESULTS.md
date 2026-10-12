# CP01 — matriz incremental de seguridad
Resultados originales 16 PASS/build Windows conservados en tag DEVF_CP01 (092c1e6) y evidence/windows-verification.json. Esta revisión no ejecuta la suite completa original.

| Área | Estado actual | Evidencia/límite |
|---|---|---|
| Binarios de escenario/suelo/modelo disponibles | BLOCKED | Inventario: cero .dzs/.dzr/.arc/.dzb/.bmd en los ZIP; assets son encabezados e imágenes |
| Stage/room/layer/XYZ seguros | NOT_VERIFIED | Referencia demo no acredita suelo/eventos; guía LOCATION_EVIDENCE lista capturas y archivos exactos |
| Funciones de cierre exactas del host | PASS auditoría/reproducción acotada | Cinco cuerpos sin modificar compilados con colas/slots/backends simulados; hashes en exact-host-functions.json |
| Guardas de activación antes de registro | PASS laboratorio | Falta de cada requisito/default no produce llamadas de registro; cierre repetido sin ownership |
| Propiedad de slot de colisión tras scene teardown/reutilización | PASS lógica propia, seis casos | No retira slot ajeno; referencia propia única exige índice/actor correctos; tabla sin referencia propia solo retira ID local; adaptador nativo compilado/enlazado, no ejecutado en motor |
| Retirada de colisión fallida | PASS lógica propia | No libera archivo ni referencias; ready=false y estado closing; retry ordenado/idempotente |
| Liberación de archivo fallida/pendiente | PASS lógica propia | No borra referencias ni reinicia load; solo release nativo phase.id==2; pending real no ejecutado |
| Cancelación y callbacks de actor en cierre | PASS lógica propia | UNK3 terminal; no execute/draw hasta ready; no reactivación tras intento de destroy |
| Callback opcional en request runtime | PASS laboratorio | Rechazado antes de create_actor; no puntero extra sin lifetime token |
| Request antes del primer callback en unregister | PASS reproducción de limitación | Cuerpo exacto devuelve OK sin drenar una cola pendiente no inspeccionada; no prueba de crash real |
| Force-delete ignora fallo de callback | PASS reproducción de limitación | actor_delete exacto devuelve 1 con forceDelete aunque deleteFunction retorna 0 |
| Retirada con actor restante | PASS reproducción | MOD_UNAVAILABLE conserva slot; no barrera del loader por ese retorno |
| FreeLibrary tras shutdown fallido | PASS Windows real, DLL fixture propia | La fixture se descarga; nunca se invoca un puntero después del unload |
| PIN de imagen DLL | PASS Windows real, DLL fixture propia | Conserva imagen propia hasta salir; no preserva slot/contexto del host; no aplicado en producción |
| MSVC, SDK, PE, imports/exports, paquete/servicios | PASS | Run final 38189000074, metadata y hashes nuevos |
| Aparición, recursos/mount, J3D, colisión, room/layer y cleanup real | NOT_TESTED | No se ejecutó Dusklight ni se conectó perfil/actor |
| DX12 y progreso/save | NOT_TESTED | Ninguna prueba de juego ni modificación de partida |
| TEST de actor | NOT_APPROVED | Bloqueos de ubicación y host persisten |
| CP02 | NOT_STARTED | Fuera de alcance |

Run 38187449685: PASS de la primera revisión incremental (11 casos nuevos + 9 regresiones). La auditoría posterior descubrió el contrato específico de dComIfG_resDelete en fase pendiente; se corrigió y añadieron tres casos de archivo/cierre.

Run de recursos/cierre 38187694002: 14 casos nuevos + 9 regresiones afectadas PASS. Regresiones seleccionadas: seis casos de recursos y tres de runtime que usan el lifecycle modificado. No se ejecutaron los siete casos originales de Stage/registro/rollback/orden de pre-hook no afectados. La ejecución del grupo de seguridad final verifica el programa incrementado y sus fixtures de cierre; no se declara ejecución del motor.

Compilador MSVC 19.51.36260.0 / Windows SDK 10.0.26100.0, x64 RelWithDebInfo. Warnings originales de headers/placement new se conservan en logs, no se ocultan ni se convierten en prueba de recuperación de excepción de constructor. Ver safety-review-build-and-tests.log; los hashes binarios finales están en collision-review-verification.json.

Run final 38189000074: seis casos nuevos de propiedad de colisión PASS, sin repetir las suites 14/9/16. Ver collision-review-build-and-tests.log y collision-review-verification.json. El laboratorio usa una tabla simulada para demostrar la política; no certifica la ejecución del adaptador cBgS en una sala real. Total de esta revisión: 20 casos nuevos distintos y nueve regresiones afectadas.
