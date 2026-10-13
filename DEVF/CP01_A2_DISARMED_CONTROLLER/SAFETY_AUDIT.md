# Auditoría de seguridad: separación, ownership y binario

Alcance: nuevo código propio, reutilización G2 intacta, MSVC y binarios propios. No se audita de nuevo el host entero, los recursos/G4 ni descarga de perfiles personalizados.

## Desarme estructural

| Control | Evidencia y conclusión |
|---|---|
| Sin backend nativo de solicitud | La DLL compila tres unidades propias+dos G2+SDK game_feature. FakeEngine y LayerScope solo en ejecutables de laboratorio. No existe implementación de ActorService request en `src/`. |
| Sin activación runtime | No config/env/UI/comando/export de spawn; lifecycle solo diagnóstico y disarm. Sin Stage/Actor/Hook/Resource service import. |
| Separación de compilación | `DEVF_A2_DISARMED=1` obligatorio; guards rechazan missing/0/spawn/armed/mutation. simulation exige LAB_ONLY. CMake no presenta opción armada ni target armado. |
| Sin creación por ABI alternativo | No fopAcM_create/fpcSCtRq_Request/setCurrentLayer/delete/cancel en el módulo; scope nativo tampoco implementado. El probe ABI offline retiene direcciones del setter sin invocar, separado y no distribuido. |
| Callbacks | Única llamada indirecta propia externa: Log.write. Visitors G2 synchronous match/census no quedan registrados. No callbacks DLL de Create/post-create ni tareas diferidas. |
| Efectos | Solo estado propio, stack buffers y LogService; ninguna escritura propia de archivo/save/progreso/HIO o thread/patch. El host controla dónde escribe sus logs; eso no es una nueva escritura directa de nuestro módulo. |

## Contratos de borrowing y escena

El reader G2 valida puntero Link por identidad en cola antes de leerlo y node por búsqueda de escenas. Registry solo dereferencia miembros registrados, rechaza exceso/ciclo. Adapter nuevo usa estos datos y vuelve a resolver node/play en el mismo tick. Los vínculos se comparan con direcciones de objetos públicos validos; no dereferencia un `process_node` desconocido ni usa offsets privados. Solo devuelve IDs/booleans/contadores/array propio de stage.

Se rechaza root target, child ausente/unregistered, child==parent, parent distinto de play layer, perfil/ID/init incorrectos, transición/retirada y pending incompatible. Root como previous es válido y se restaura solo en fake. No usar Link layer, current layer del caller o logical6 como owner. IsDeletingMesg lee delete_count y sigue siendo una señal parcial; no garantiza vida ni orden concurrente.

Precondiciones: caller original game thread sin destructiva reentrada, APIs/listas sanas y host/version/servicios compatibles. El desarme garantiza ausencia de solicitud; **no constituye certificación universal de cualquier lectura frente a un host ya corrupto o mod conflictivo**. Adaptación todavía no ejecutada in-game.

## Errores, latch y recuperación

Latch se consume antes de FakeEngine.request. Scope restaura contexto incluso si hay return/throw, comprueba retorno y no interpreta restore como cancelación. ID inválido, éxito ambiguo y excepción después de aceptar llevan a STOP_SESSION sin retry. Fallo antes de consumir mantiene terminal si se desconoce resultado del adaptador; desarmar/reactivar no lo borra. Reentrada no permite sobrescribir STOP por success externo.

Previous destruido/fallo de restore no se repara: fail closed. Pendiente con timeout o aparición tardía no se cancela. IDs no tienen generación acreditada; reuse en fixture solo comprueba respuesta conservadora a esa información. Para la futura creación real, contexto/continuidad y solución de identidad siguen pendientes; no manipular procesos originales por coincidencia de perfil.

Desactivar DLL no elimina enemigo/pending. La política futura es cerrar todo el proceso, no hot reload; cierre no prueba G6 ni revierte saves escritos. En esta etapa no hay actor ni instalación que retirar.

## Auditoría del binario, evidencia a contrastar

La aceptación exige conjuntamente: fuente/ledger idénticos al mirror compilado; seis compile units del módulo sin `tests`; link map sin backend fake/setter/request; PE32+AMD64; exports exactamente lifecycle/mod_ctx/mod_meta; metadata ABI1 y únicamente Host2.2/Log1.0/Game2; IAT exacto read-only revisado; disassembly/map correlacionados con el grafo lifecycle y única llamada Log. No se deduce seguridad por buscar strings de spawn.

Grafo propio: initialize→headers/version/error; update→guardia→capture_owner→G2 capture + vínculos/getters→Controller.disarm→validate_owner→snprintf→Log.write; shutdown→estado escalar/disarm. El SDK game_feature solo emite el import GameService. Core simulado puede quedar como funciones escalares no exportadas en map, pero no posee backend ni función de creación. No hay mecanismo indirecto de obtener ActorService mediante Host porque no se invocan tales miembros, y el GameService import no se usa para mutar.

La evidencia MSVC definitiva y hashes se registran en TEST_RESULTS/evidence; una DLL que no satisfaga esa superficie mantiene BLOCKED. No se distribuye DLL, probe ni ejecutables, incluso si pasan: artefacto CI solo textual. `_package` está excluido y nunca se construye.

## Límites conservados

Runtime owner/creación/render NOT_VERIFIED/NOT_TESTED. G4 sin punto seguro y G5/CP02 NO-GO. Cleanup/transiciones/desregistración de actor nativo no se ejecutaron. Descarga DLL personalizada BLOCKED independiente. Ningún PASS de lab/binario resuelve esos gates.
