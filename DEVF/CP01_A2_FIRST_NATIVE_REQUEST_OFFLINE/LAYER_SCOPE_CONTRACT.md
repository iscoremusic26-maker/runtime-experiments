# Contrato del scope de capa

Autoridad: fuente oficial `TwilitRealm/dusklight@40457c6adb381928e4b5fef6ed459ed291edd5e2`:

- `include/f_pc/f_pc_layer.h` y `src/f_pc/f_pc_layer.cpp:101`: `void fpcLy_SetCurrentLayer(layer_class*)`, asignación de un puntero global; `fpcLy_CurrentLayer` y RootLayer.
- `include/f_pc/f_pc_manager.h:45`: fpcM_Create toma CurrentLayer y llama fpcSCtRq_Request.
- `src/f_pc/f_pc_create_req.cpp`: fpcCtRq_Create almacena layer/id y aumenta su contador; eliminar la solicitud de la cola disminuye ese contador.
- `src/f_pc/f_pc_stdcreate_req.cpp:51` y `:68`: fases posteriores CreateProcess/SubCreateProcess seleccionan nuevamente la capa guardada en la solicitud.
- `src/f_ap/f_ap_game.cpp:807/:828` y ModLoader::tick (src/dusk/mods/loader/loader.cpp): update del mod en hilo del juego antes de la gestión de procesos. No se autoriza llamar este adaptador desde otro hilo.

## Invariantes implementadas

Preflight Host/thread, F_SP121/room3/logical6, ROOM_SCENE y PLAY_SCENE completos, bindings públicos, registro vivo, Link, no transición/retiro/evento y ningún create/delete ajeno. La ubicación/sesión se admiten por separado; la consulta parcial del medio nunca concede admisión.

Registry local, máximo128 capas, detecta ciclo y IDs duplicados; solo préstamos de punteros en stack durante una operación. Se identifica la hija desde la ROOM_SCENE viva, no desde Link, root o IDs5/6. En cada operación se resuelve de nuevo el ID en el registro; ningún actor/layer pointer persiste en el controlador. Previous real debe estar registrado antes del setter y antes de restaurarlo.

El scope guarda solo previous ID y restaura una sola vez, aun con error, excepción o early return. Comprueba current==previous. Si previous desaparece o falla el setter, STOP/Restore, sin fallback a root. Un setter fallido o reentrada también consume el intento; el destructor no hace un segundo setter tras un intento de restauración fallido.

Los fixtures usan tanto los IDs observados como otros IDs para descartar constantes accidentales. La selección y su restauración se prueban en éxito, fallos, excepciones y reentrada. Estas pruebas demuestran el algoritmo del scope, no un lease de escena runtime.

## Límites

El setter oficial no es lock, lease ni primitiva atómica. Los cambios se realizan en el callback del hilo del juego; no se afirma atomicidad frente a hooks/mods externos. RAII restaura el contexto inmediato, no asegura lifetime de ROOM_SCENE durante creación asincrónica. La ruta estándar vuelve a usar request.layer, pero no podemos garantizar que todo código nativo/hijo o un mod conflictivo preserve esa capa. Counters/owner inesperados se observan y provocan STOP; no se corrigen.

No se retiene create_function: NULL, por lo que el motor no guarda un callback de creación de esta DLL. No hay política de descarga dinámica demostrada ni cancelación segura de una solicitud ya encolada. El bloqueo independiente de DLL con perfiles custom permanece BLOCKED y no se reinvestiga.
