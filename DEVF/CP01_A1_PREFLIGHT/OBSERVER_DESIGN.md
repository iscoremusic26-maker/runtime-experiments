# G1 — observador independiente de solo lectura

**Compilación/enlace Windows PASS_LAB; surface/metadata PASS_STATIC. Ejecución en host y DX12 NOT_VERIFIED.** El módulo no reemplaza CP01. Se importa Host2.2, Log1.0 y Game epoch2 automáticamente con `FEATURES game` del SDK oficial. Windows x64 MSVC; `/Zc:__cplusplus` preserva la selección correcta de tipos oficiales.

`mod_initialize` exige headers suficientes, versiones major/minor compatibles, write de Log presente y host.version exactamente2.0.3 o2.0.3.0. Rechaza prefijos/custom y epoch1. Copia build_id a hex acotado32bytes; longitud/puntero inválido se omiten. La versión **no autentica por sí sola el ejecutable original**: build_id/checksum deben contrastarse en el procedimiento G2 con el release ya acreditado. No se accede al Game ABI antes de inicialización aprobada.

## Contrato de lectura

| Dato | Superficie pública utilizada | Condición/límite |
|---|---|---|
| Transición | dComIfGp_isEnableNextStage | Si está activa, omite la captura |
| Stage/room | dComIfGp_getStartStageName; dStage_roomControl_c::getStayNo | Copia8chars; room0..63; captura detallada solo F_SP121/R3 |
| Current engine layer | fpcLy_CurrentLayer, fpcLy_RootLayer, layer_class/node_class públicos | Candidate pointer opaco hasta coincidencia en registro completo, máximo128, sin ciclos |
| Link owner/XYZ/yaw | dComIfGp_getPlayer(0), fopAcIt_Judge | Comparación de direcciones sin dereferenciar Link hasta match en cola; máximo256; perfil ALINK, init_state2, !IsCreating, condición INIT y layer registrado |
| ROOM_SCENE y child layer | getStatusProcID, fopScnM_SearchByID; scene_class/process_node_class públicos | ID/perfil ROOM_SCENE confirmados; init_state2/!IsCreating; layer del nodo registrado; creates/deletes0 |
| Layer lógico | dComIfG_play_c::getLayerNo(0) | Consulta después de validar sala/Link/nodo; distinto de IDs de layer; admite0..14 |
| Recursos mínimos | dComIfG_getObjectResInfo("E_OC"/"E_ocb") | Copia solo bool; no dereferencia dRes_info, no phase/model/anim/archivo cargado garantizado |
| Baseline E_OC | fopAcIt_Judge, campos públicos de actor | Perfil E_OC completo, room actual3; máximo256visitados/8registros; copia ID/owner/params/home.angle.x/XYZ; señal truncation |
| Renderer, readiness de modelo, FILI runtime, switches, flags, otros mods | No se añaden getters ni recorridos de objetos para rellenar columnas | NOT_VERIFIED; screenshot/configuración/evidencia privada y futura revisión dirigida |

La identidad de layer utiliza **tipos originales**, herencia original MSVC y sizeof/offsetof por compilador; no offsets históricos de GameCube ni estructuras privadas. No hay setter, downcast a la clase privada de Link, consulta de modelo ni dereferencia de puntero no encontrado en el registro correspondiente. Los nodos del registro y actores de la cola se leen bajo el contrato público de registros vivos del motor; no se pretende tolerar corrupción de memoria del host.

La fuente `f_pc_executor.cpp:55/68` distingue init_state2 en cola de ejecución y3 al salir. Esto más !IsCreating filtra observaciones prematuras; **no prueba la readiness completa de un enemigo**. `fopAcIt_Judge` conserva su filtro/data en stack y devuelve sin registrarlos (`f_op_actor_iter.cpp:28`, `c_tag_iter.cpp:14`). Las visitas son síncronas dentro del tick de ModLoader; no se invoca código mutador ni se cede ejecución durante la captura. `f_ap_game.cpp:807` y loader.cpp:1237 fundamentan el contexto de tick. Coherencia/lifetime efectivos frente a cargas/transiciones del juego permanecen NOT_VERIFIED hasta G2.

Todos los native pointers son locales a `capture_native`, incluidos registry, visitantes y préstamos. Snapshot contiene exclusivamente arrays propios, números y bool; State solo active/contador/cadencia. No se almacena Snapshot ni referencia del engine después del tick. Los slots de servicios/contexto son los del SDK/loader, no ownership de actores. `mod_shutdown` emite como máximo una línea y borra State; es idempotente. Sin tareas, threads, callbacks registrados, watcher, handles ni recursos adquiridos. El laboratorio prueba ese estado propio; no resuelve el bloqueo independiente de descarga de perfiles personalizados.

## Desarmado y presupuesto

No ActorService, StageService, HookService o ResourceService. No registros, create/delete, hooks, ediciones ni escrituras al engine/globales/save/archivo. No spawner, encode/Add ni opción armable en este módulo. `DEVF_READ_ONLY=1` obligatorio; definir ENABLE_SPAWN/ENABLE_MUTATION o READ_ONLY0 impide compilar. Constants de registro/mutación false. Auditoría de llamadas/imports nativos y metadata exacta de tres servicios; ningún hook/export de servicio.

Máximo64 llamadas LogService por inicialización: inicio1, hasta62capturas, shutdown1. Intervalo120 **updates**, no segundos. Cada mensaje ≤2047chars, terminado en NUL. Tras llegar al límite no se realizan más capturas nativas. Nueva inicialización solo después de shutdown; no se recomienda hot reload en G2. Los fallos conservadores son `SKIP_*`, sin tratar valores parciales como admisión. Censo truncado o layer UNKNOWN no permiten cerrar G2. El checker de texto/imports es una ayuda de revisión específica de este código, no una prueba general de no mutación para C++ arbitrario.

La CI compila únicamente DLL y laboratorio; el target package del SDK queda fuera de ALL. El workflow no ejecuta packaging/install, no arranca el juego ni sube DLL/EXE/LIB/.dusk. No se distribuye un paquete de observación ahora.
