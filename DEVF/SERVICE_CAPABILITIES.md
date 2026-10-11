# SDK, ABI y servicios — CP00
Fuente exclusiva: ZIP 2.0.3 verificado; rutas relativas al árbol fuente.

| Servicio | Versión | Capacidad y límite |
|---|---|---|
| ActorService | 1.0 | register/unregister, create/child por nombre o perfil, ID, sala, delete; no API de herencia IA, ni token de vida por instancia expuesto |
| StageService | 1.0 | patch/delete/add/remove registros en memoria; stage <=8 caracteres, add exige sala específica, layer -1 coincide con cualquier capa |
| ResourceService | 1.1 | load/free, file_exists/directory_exists; res/ propio de solo lectura; inicializar ResourceBuffer.struct_size |
| HostService | 2.2 | version/build_id y data_dir con retorno ModResult; guardar allí datos propios |
| FileService | 1.0 | I/O mediante ubicaciones opacas; no concatenar ubicaciones |
| UiService | 2.3 | superficie disponible para investigar en CP07; editor no implementado |
| GameService | 2.0 | epoch de ABI del juego; import automático con FEATURES game |

MOD_ABI_VERSION=1. ServiceHeader lleva struct_size, major_version y minor_version; las importaciones exigen versiones y tamaños compatibles. ActorProfileDesc incluye nombre[8], process_size y cinco callbacks; usar sizeof(clase) y nombre único corto, sin offsets copiados. Tipos: ProfileName int16, ActorId uint32, ActorHandle/StageActorHandle uint64. Los tamaños Win64 de estructuras completas aún deben obtenerse del compilador objetivo; no certificar cifras Linux.

GameABIConfig.cmake fija TARGET_PC=1, WIDESCREEN_SUPPORT=1, AVOID_UB=1, VERSION=0, MTX_USE_PS=1, PARTIAL_DEBUG=1; fuerza global.h. SDK/src/game_feature.cpp importa GameService. No definir estos flags manualmente ni usar comentarios de offsets retail como layout Win64.

src/dusk/mods/svc/actor.cpp: create_actor llama a fopAcM_create, devuelve solicitud/ID; no demuestra creación concluida. params debe ser válido, escala inicializada. unregister_actor fuerza eliminación y puede devolver MOD_UNAVAILABLE si no termina sincrónicamente; detach registra error si no puede retirar el perfil. No certificar hot reload seguro. Nombre retail coincidente puede reemplazar lookup de stage según contrato: prohibido para DEVF sin decisión posterior.

src/dusk/mods/svc/stage.cpp admite record_size 0x20/0x23 y registra copias por propietario; procesadas al cargar escenario, sin spawn inmediato garantizado. remove_actor_edit elimina registro, no demuestra eliminación de actor ya creado. Sin escritura de .dzs/.dzr originales.

mods/custom_actor_demo registra wrock/mine y los añade por StageService en F_SP108; shutdown solo registra log y confía en detach. Patrón de referencia, no prueba de enemigo nativo ni rollback suficiente para DEVF. CP01 deberá verificar errores, ciclo de vida y limpieza antes de producir TEST.

## Comprobación nativa Windows en CP00
El run final verifica en la DLL los ModMetaImport requeridos: tamaño 80 bytes, kind=2, flags=0, y major/min_minor Actor 1.0, Stage 1.0, Resource 1.1, Host 2.2, Log 1.0, Game 2.0. Exports lifecycle/mod_meta y el import real dusklight.exe/fopAcM_SearchByID confirmados por dumpbin. No se ha ejecutado el loader ni comparado tablas runtime del host: registro del requerimiento en el binario no acredita resolución real del servicio.
