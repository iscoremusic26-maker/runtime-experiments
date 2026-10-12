# Rutas del SDK oficial 2.0.3

Fuente autoritativa: `TwilitRealm/dusklight@40457c6adb381928e4b5fef6ed459ed291edd5e2`. Los hashes y líneas concretas de cada referencia están en [source-references.json](evidence/source-references.json). Se reutilizan la equivalencia ZIP/árbol de CP00 y las revisiones CP01; no se ha aplicado el parche experimental ni repetido la compilación del host.

## A1 — definiciones persistentes con StageService 1.0

**PASS estático:** `add_actor(ctx, stage, room, layer, bytes, size, &handle)` añade una definición sin reemplazar un registro original. El servicio copia los bytes a un `vector<uint8_t>` y conserva el propietario `LoadedMod*`; no conserva el buffer del llamador ni una función de DEVF. El handle identifica la edición, no un actor.

Contrato de entrada, verificado en `sdk/include/mods/svc/stage.h` y `src/dusk/mods/svc/stage.cpp`:

| Dato | Contrato efectivo |
|---|---|
| stage | Nombre no vacío, máximo 8 caracteres. Comparación con `dComIfGp_getStartStageName()`. |
| room | `uint8_t`; `add_actor` rechaza 255. Para el prototipo se limita a 0–63: `dStage_roomControl_c::mStatus[0x40]`. |
| layer | `int8_t`; -1 es comodín. Se compara con `dComIfG_play_c::getLayerNo(0)`, no con una capa deducida del nombre de archivo. El servicio no valida todo el rango; el prototipo exige 0–15 explícito. |
| bytes | ACTR **32**, TGSC **35**; cualquier otro tamaño se rechaza. `stage_tgsc_data_class` de C++ ocupa **36**, con padding: no pasar `sizeof` como tamaño del registro TGSC. |
| resultado | `MOD_OK` y un handle acreditan registro, sin ID de instancia ni señal de inicialización. |
| conflictos | Otros mods pueden modificar registros por CRC, eliminar registros y sobreescribir la búsqueda de nombres. El orden de mods importa; añadir no demuestra aislamiento frente a otros mods. |

Formato de los bytes, según `stage_actor_data_class`, `stage_tgsc_data_class` y `fopAcM_prmBase_class`:

| Offset | Tamaño | Codificación |
|---|---:|---|
| 0 | 8 | Nombre canónico con padding cero; no número de perfil. |
| 8 | 4 | Parámetros `u32` big endian. |
| 12, 16, 20 | 4 cada uno | XYZ `float32` big endian. |
| 24, 26, 28 | 2 cada uno | Ángulos `s16` big endian. |
| 30 | 2 | `setID` `u16` big endian; prototipo usa `0xFFFF`. |
| 32, 33, 34 | 1 cada uno | Solo TGSC: escala en décimas, `u8`. ACTR conserva el default 10/10/10 del append. |

No se serializa un argumento libre: `dStage_actorCreate` busca el nombre y fija `append->argument` desde la tabla original. La escala TGSC no es un control universal de tamaño ni garantiza escalado de colisión.

Creación efectiva: `dStage_dt_c_roomReLoader` decodifica registros comunes, llama `dusk_stage_svc_new_actor_create` y después carga actores de capa. El helper solo acepta ediciones Add del stage actual, mod activo, room y layer compatibles. Copia el registro a un objeto temporal, reserva un append del host, copia base/escala y llama `dStage_actorCreate`. Esta resuelve el perfil y usa `fopAcM_Create(profile, NULL, append)`: **post-create callback nulo**. No hay creación inmediata dentro de `add_actor`. No se debe asumir que registrar con la sala ya cargada ejecutará ese helper. `stageLoader` y `roomLoader` tienen funciones diferentes; la inclusión se ha comprobado en `roomReLoader`.

**PASS estático sobre ausencia de callbacks DEVF en esa cadena, condicionado a que el nombre resuelva al perfil nativo original.** Las funciones create/execute/draw/delete del enemigo provienen del host; también sus callbacks internos de animación. Un override de otro mod del nombre puede romper esta condición. Un entorno de prueba futuro deberá tener solamente DEVF y comprobar la identidad del perfil.

Persistencia: la definición permanece en memoria mientras el mod siga activo, y se vuelve a consumir cuando el flujo de recarga de sala compatible pasa por el helper. No escribe DZS/DZR, ROM ni saves. Tras cerrar el proceso desaparece; para persistir configuración entre sesiones se necesita reconstituirla desde datos propios del mod. Ni `setID=0xFFFF` ni el handle garantizan unicidad entre múltiples invocaciones del reloader: duplicación y cantidad exacta quedan **NOT_VERIFIED runtime**.

`remove_actor_edit` y `stage_remove_mod` borran definiciones. **No destruyen instancias ya creadas, no cancelan solicitudes y no modifican actores originales.** No existe una asociación StageActorHandle→ActorId en este servicio. Desactivar o recargar el `.dusk` retira sus registros, pero un enemigo ya creado puede seguir vivo hasta su destrucción nativa. Reaplicar un registro con la sala ocupada no acredita que la instancia anterior desapareció.

## A2 — solicitudes identificables con ActorService 1.0

**PASS estático:** `create_actor_from_name` puede solicitar un perfil original sin `register_actor`. Para `E_SB`, la tabla original contiene `fpcNm_E_SB_e=0x1C1`, argumento -1; para `E_rd`, `fpcNm_E_RD_e=0x1D4`, argumento -1. El nombre distingue mayúsculas. La variante por número `create_actor(ctx, ProfileName, ...)` evita el override nominal; obliga a fijar y verificar el ABI/perfil exacto 2.0.3. Las variantes child añaden dependencia de parent ID, innecesaria para el experimento mínimo.

`ActorSpawnParams` lleva parámetros, argumento, room con signo, posición, ángulos, escala y **callback opcional `create_function`**. Este último debe ser `nullptr`. La operación por nombre sustituye el argumento recibido por el de la tabla; por número conserva el argumento. `createAppend` copia los datos; convierte escala float a bytes en décimas. No acepta stage/layer como argumentos: un controlador futuro debe verificar previamente el contexto del juego, y no tratar esa comprobación como una reserva de escena.

El resultado es un **ID de solicitud encolada**, no una instancia lista. En el primer paso `fopAc_Create` ya introduce el actor en la cola visible antes de completar su create/resLoad. Consultar `get_actor_room_num` con éxito tampoco acredita recursos, heap, modelo o colisión inicializados. Un adaptador ABI futuro deberá distinguir request pendiente, actor en creación, actor listo y desaparición; la consulta oficial `fpcM_IsCreating` es una señal a evaluar, no una promesa universal de compatibilidad del enemigo con la escena.

`get_actor_id(profile)` devuelve el primer match; **no enumera, no filtra propietario y no identifica cuál fue añadido por DEVF**. `delete_actor(id)` busca actores visibles y solicita su eliminación; si no los encuentra devuelve `MOD_OK`. Por tanto no cancela de manera acreditada solicitudes anteriores al primer create. El host no atribuye al mod las instancias nativas solicitadas: el ownership de ActorService cubre perfiles nuevos y sus handles, no un inventario de actores nativos por caller.

A2 ofrece un ID individual que A1 no entrega, y es la base preferible de futuros adaptadores por instancia. No aporta por sí solo persistencia de sala ni cancelación de requests pendientes. La arquitectura no debe ejecutar A1 y A2 simultáneamente para la misma colocación: se crearían duplicados.

## Recursos y parámetros concretos, sin investigación ARC nueva

El prototipo define `E_SB`, parámetros `0x000000FF`, argumento nativo -1, setID `0xFFFF`. `daE_SB_c::Create` carga **`E_SB`**, espera `cPhs_COMPLEATE_e`, crea heap/modelo y configura suelo/colisión. Su campo `field_0x61a` es `u8`, recibe los parámetros y consulta/escribe un switch de room únicamente cuando no vale `0xFF`. El sentinel evita **ese** contrato de switch; no prueba ausencia de todos los efectos, recompensas o condiciones de aparición.

Además, `fopAc_Create` aplica flags de aparición del grupo ENEMY en FILI: puede devolver ERROR según switches de sala aunque el parámetro propio sea FF. La colisión de suelo y el ajuste de Y nativos no acreditan una colocación segura. No se ha verificado disponibilidad de `E_SB` en una instalación ni idoneidad de un escenario concreto; no se reutiliza la caja WRock/F_SP121 como ubicación aprobada para este enemigo.

Contraste acotado de `E_rd`, para demostrar que params no son stats universales:

| Bits/estado | Uso comprobado en su Create |
|---|---|
| 0–7 | arg0/arg1; ciertos valores seleccionan modos especiales/boss, y arg0=10 puede consultar coach-game y fallar. |
| 8–11 | weapon_type; 15 significa none, otros rangos pueden fallar. |
| 12–15 | arg2; 15 se normaliza a 0; algunos valores cambian acción/one-hit-kill. |
| 16–23 | scene_no; FF se normaliza a 0; puede modificar selección de layer. |
| 24–31 | switch de room; FF suprime esa consulta. |
| actor_set | Cambia archivo entre `E_RD` y `E_rdb` y otras dependencias. |

No se publica un preset `E_rd` supuesto seguro. Los archivos, heap, animaciones, armamento, condiciones de escena y comportamiento precisan evaluación por enemigo antes de una aparición real.

## B — adaptadores por instancia, todavía sin implementación

ActorService no tiene setters universales de atributos. Eso **no demuestra que el SDK carezca de acceso por instancia**: `FEATURES game` importa GameService **2.0**, cuya major es el epoch del ABI, y expone headers/funciones oficiales del juego. `GameABIConfig.cmake` fija definiciones e includes; en Windows el SDK enlaza al import library oficial. La prueba adicional solo compila tipos del ABI: no enlaza funciones ni escribe campos del juego.

Datos públicos de `fopAc_ac_c`: health, speed/speedF, scale y model. `fopAcM_SearchByID`, `fopAcM_SetSpeedXYZ/SetSpeedF`, `fopAcM_GetScale_p/GetModel` existen en el header oficial. Los colliders tienen `SetAtAtp`, `SetAtType`, `OnTgShield/OffTgShield`; `e_rd_class` expone sus esferas y `at_info`. Son oportunidades reales para un adaptador **específico**, no una API universal ni autorización de seguridad derivada solo de que compile.

Las escrituras propuestas para investigación futura serían datos de una instancia validada, no páginas de código, vtables, funciones internas ni HIO global. No se han implementado. Un ID/pointer prestado no es ownership: resolver cada tick, validar perfil/escena/readiness y descartar referencias al cambio de contexto, sin guardar punteros del actor en trabajo asíncrono ni punteros de la DLL en el actor.

La viabilidad y las alternativas de cada función están separadas en [FEASIBILITY_MATRIX.md](FEASIBILITY_MATRIX.md). La ruta B mantiene el objetivo completo y no hereda automáticamente la seguridad estática de A1.
