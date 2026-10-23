# Matriz de integración .dusk

Fuente fijada: `40457c6adb381928e4b5fef6ed459ed291edd5e2`. Clasifica mecanismos observados en contrato/fuente; no certifica instalación de un target Windows. Orden preferido cuando cubre la necesidad: servicio oficial, recursos/overlays, y después hooks que requieran ABI de juego. Las opciones no son intercambiables sin conocer precondiciones.

| Área | Mecanismo | Condiciones y límite observado | Evidencia/rollback |
| --- | --- | --- | --- |
| Datos propios por slot | OFFICIAL_SERVICE SaveService | set_blob copia/marca dirty; callback de guardado antecede flush; no transacción conjunta CARD+sidecars | WORLD-011/012; [save/load](systems/save_load.md). Versionar esquema; liberar memoria propia, no editar saves vanilla. |
| Registros actor de stage/sala | OFFICIAL_SERVICE StageService | Se aplican durante decodificación/reload, tamaño 0x20/0x23; handle de edición no es actor vivo | WORLD-004/005/033; [stages](systems/stages_rooms_layers.md). Retirar registro evita aplicación futura, no deshace instancias ya cargadas. |
| Perfiles/creación de actores propios | OFFICIAL_SERVICE ActorService | ID de creación asíncrona; pointer/lifecycle no garantizados por MOD_OK; unregister puede fallar | SDK-001, HOOK-029; [actores](systems/actors_ai_npcs.md). Demostrar fin de callbacks antes de unload. |
| Recursos propios / reemplazo DVD o textura | OFFICIAL_SERVICE o ASSET_OVERLAY | ResourceService res/ propio; overlays afectan futuras lecturas y consumidores cacheados conservan estado | PRES-001..006/018; [recursos](systems/resources_archives_overlays.md). Retirar ownership y recargar consumidores cuando proceda. |
| Cámara/GPU/UI | OFFICIAL_SERVICE Camera/Gfx/Ui | Callbacks y handles con fase/hilo/vigencia concreta; Gfx expone WebGPU y objetos prestados | PRES-009..013; [render](systems/cameras_rendering.md). Retirar callbacks, drenar trabajo propio y liberar solo objetos propios. |
| Consultas/eventos de mensaje | OFFICIAL_SERVICE Flow/Message | Grafos comprometidos y resolvers con ownership; no sustituye todo el event manager | SDK-006, WORLD-023/024/025; [diálogo](systems/cutscenes_dialogue.md). Retirar registros no revierte flags ya escritos. |
| Función enlazable con firma conocida | TYPED_HOOK | Helpers y metadata implementados; export/resolve/target Windows no observados aquí | HOOK-001..012/027/028; [ABI](HOOKING_AND_ABI.md). No asumir firma negociada entre candidatos ni pila de replace. |
| Símbolo por nombre/manifiesto | SYMBOL_HOOK | Nombre inequívoco, manifiesto compatible, firma manual exacta y target con entrada parcheable | HOOK-010..012/026; resolución/instalación real pendientes. Retirar hooks propios y mutaciones externas propias por separado. |
| Script mediante runtime | SCRIPT_API (DOC_CONTRACT) | El contrato describe Luau limitado a servicios expuestos por su runtime; no acceso C++ arbitrario | [docs/modding.md L4-L14](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/docs/modding.md#L4-L14), HOOK-024. Inventario de bindings específicos sigue pendiente. |
| Símbolo solo localizado / mecanismo sin contrato suficiente | POTENTIAL_REQUIRES_VERIFICATION | Declaración no prueba export, ABI, seguridad o cobertura inline | Cada ficha señala el mínimo pendiente. No proponer modificar EXE/SDK/ROM para obtenerlo. |
| Hook de función con stack de toda la sesión y hot unload | NOT_SUPPORTED_BY_CURRENT_EVIDENCE | El contrato advierte que el boundary entre frames no da seguridad de retirada | HOOK-022; no prometer rollback por esperar un tick. |

Los IDs remiten al [ledger](EVIDENCE_LEDGER.json), con enlaces al SHA/rango real. Esta matriz expresa elecciones de mecanismo, no funcionalidades concretas ni diseño de un mod. Sin compilación ni juego ejecutado.

Presencia del port: POTENTIAL_REQUIRES_VERIFICATION como interfaz C++ interna, sin PresenceService público auditado. ConfigService solo gestiona variables propias; no otorga control/lifetime del backend host. PORT-010..013, [ficha de presencia](systems/port_presence.md). No se certifica hook, ACK ni rollback remoto.

Matrices interpoladas: OFFICIAL_SERVICE InterpService (SDK-013 aclarado,PRES-094..097). recordMOD_OK no confirma muestra fuera de ventana; valores copiados,key global compartida. Forget/detach borra muestras,no restaura anterior ni confirma GPU; [ownership](systems/callback_ownership_and_cancellation.md).

WebSocketService polling: SDK-024/CALLBACK-028..031,slots oficiales poll_event/close. Snapshot de handles no prolonga payload permod; closeaceptado no CLOSED ni cupo liberado. WrapperC++detach solo local; backend/drain sin certificar. [Ownership](systems/callback_ownership_and_cancellation.md).

CP-R91: FlowService patch_node/remove_graph son OFFICIAL_SERVICE;la reversión retira patches para futuros lookups, no restaura efectos de un nodo ya consumido. WORLD-047..050, [flujos](systems/cutscenes_dialogue.md). Ganador por clave/posiciónmod/commitsequence;sin coexistencia Windows probada.
