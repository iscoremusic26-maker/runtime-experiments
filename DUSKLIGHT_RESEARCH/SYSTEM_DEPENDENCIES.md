# Dependencias entre sistemas

Mapa de rutas seleccionadas del commit `40457c6adb381928e4b5fef6ed459ed291edd5e2`. Las flechas representan consumo de estado o una llamada observada en las evidencias citadas; no son un grafo exhaustivo de todos los includes ni una garantía de orden universal.

| Proveedor → consumidor | Qué cruza la frontera | Invariante o riesgo | Evidencia / ficha |
| --- | --- | --- | --- |
| Loader → servicios/otros mods | Contexto, exports, imports, orden de activación y retirada | Required import suspende consumidor si falta; optional necesita NULL check | HOOK-002/015/020; [runtime](systems/runtime_and_lifecycle.md) |
| Metadata/manifest → HookService | Target, firma declarada, trampoline y original slot | Un backend compartido por dirección no negocia firmas entre candidatos | HOOK-001..012/027/028; [ABI](HOOKING_AND_ABI.md) |
| Gestor de procesos → escena/actor | IDs, profile, fases de crear/ejecutar/borrar/draw | Crear es diferido; cleanup y callbacks deben terminar antes de unload | ARCH-001, HOOK-029; [actores](systems/actors_ai_npcs.md) |
| Recursos/room → StageService → actor | Bytes del registro, room/layer, nombre/profile, parámetros | Edición no equivale a entidad viva; retirar handle afecta aplicación futura | WORLD-001..005/033; [stages](systems/stages_rooms_layers.md) |
| Progreso/flags → stage/layer/NPC/evento | Banco activo, SaveTbl y condiciones narrativas | Banco persistente y copia activa pueden diferir; reglas por contexto | WORLD-007..009/016/017; [flags](systems/flags_events_progression.md) |
| Input/estado → Link → física/colisión | Stick, procedimiento, modo, velocidad/posición y resultados At/Tg | Cambiar solo ID/posición no reproduce transición ni posición final corregida | PLAYER-001..016; [jugador](systems/player_and_controls.md), [física](systems/movement_physics_collision.md) |
| Colisión → daño → eventos/audio/drops | Hit object, material/guardia, política de daño local y side effects | No hay un health/HP handler universal para jugador y todos los enemigos | PLAYER-014..019; [combate](systems/combat_damage.md) |
| ItemService → actor/evento/inventario | Solicitud en cola y entrega bajo estado aceptable | Detach no cancela evento de entrega que ya es dueño del trabajo | WORLD-018..022; [inventario](systems/inventory_equipment.md) |
| Flow/Message → diálogo/estado | Nodos, edges, queries, eventos y texto por idioma | Remove retira registros; no revierte flags ya escritos | WORLD-023..027; [narrativa](systems/cutscenes_dialogue.md) |
| Guardado vanilla → observers → sidecars | Slot activo, callback y flush de dirty mods | Confirmación vanilla no implica sidecar durable; no atomicidad conjunta observada | WORLD-010..014, CALLBACK-001; [save](systems/save_load.md) |
| Bundle/DVD/ARC → modelo/HUD/audio/entorno | Buffers, archive refcount y objetos decodificados | Reemplazo no reconstruye consumidor cacheado; lifetime de archive/heap manda | PRES-001..006/014..018; [recursos](systems/resources_archives_overlays.md) |
| Heap JKR/actor → modelos/animaciones | Heap actual por hilo, solid heap y allocations | Callback de heap puede repetirse; liberar con el allocator propietario | ROOT-001..006; [memoria](systems/memory_ownership.md) |
| Cámara/interpolación → Gfx/UI | Estado temporal de cámara, matrices y handles GPU prestados | Game thread y render worker tienen contratos distintos | PRES-007..018; [cámara/render](systems/cameras_rendering.md) |
| Reloj/clima/room → ambiente/audio/partículas | Daytime, tablas de color, weather y punteros de influencia | Controlador puede sobrescribir cambio puntual; influencia requiere storage vivo | PRES-027..034; [entorno](systems/environment_weather_time.md) |
| Save/Host/Camera/Item resolver → callback del mod | Callback, userData, ownership y snapshot del dispatch | Cancelación difiere según revalidación; no liberar userdata por analogía entre servicios | CALLBACK-001..008; [callbacks](systems/callback_ownership_and_cancellation.md) |

## Cobertura nominal restante

El [índice de directorios](DIRECTORY_INDEX.tsv) conserva todos los módulos del árbol principal y el [índice de sistemas](SYSTEM_INDEX.json) añade estado y límites. Las categorías de soporte no se consideran comprensión técnica: herramientas/build, documentación, PCH y auxiliares de juego, configuración/logging/achievements/Discord/LiveSplit del port, y submódulos externos siguen con profundidad nominal donde no hay ficha contrastada.

Los encabezados de recursos regionales localizan IDs; no son miles de implementaciones de subsistemas. Los cuatro gitlinks están fijados en [SOURCE_PIN](SOURCE_PIN.md), sin internals auditados. JSystem se sigue selectivamente en memoria/J3D/J2D/audio; bibliotecas de compatibilidad de consola, debugger stubs y dependencias transitivas no se confunden con gameplay investigado.

Para ampliar una arista: abrir la evidencia citada, confirmar proveedor y consumidor en el mismo SHA, seguir estado/error/cleanup, actualizar ledger y cobertura, y publicar un checkpoint antes de ampliar el siguiente flujo.

FontArchive → JUTResFont (backing prestado/tablas propias) → J2DTextBox (font prestado) → owner file-info (referencia global): PRES-036..039. Hay dos niveles de ownership; destruir un pane no equivale a liberar la referencia mDoExt ni los bytes BFN. La ruta completa seleccionada está en HUD, sin promover todas las pantallas a CROSSCHECKED.

GameMode/scheduler + señales de menús/actores → AchievementSystem → snapshots/toasts UI y archivo propio: PORT-001..005. El circuito no es SaveService por slot ni un AchievementService público. port_support pasa a READ por esta cadena; otras familias siguen nominales. Ver [logros internos](systems/port_achievements.md).

Event/switch/room/message → avance normal o KYTAG11 → PlayerStatusB en memoria → hora/weekday de audio y serialización vanilla posterior: PRES-040..043. Los dos controladores tienen gates distintos y el flag tag se limpia por actualización; no es un reloj de pared ni un guardado CARD por cada setTime.

CP-R10: runtime_and_lifecycle → HUD/fileSel → recursos/heaps; framework f_op/f_pc coordina overlap,delete-before-create y PLAY por fases (ARCH-002..007). Sin dependencia de un SceneService público ni auditoría de todos los actores hijos.

CP-R11: models_animations_materials → archive/refcount → actor solid heap → morf/BCK/BTK → execute/draw → actor wrapper teardown. PRES-044..047; luz/audio son consumidores auxiliares,no nuevos contratos SDK.

CP-R12: MessageService → estado compartido flow.cpp → JMessage/TControl y dMsgObject selección → ActiveBinding → reset/destructor. CALLBACK-009..013 separa registro/callback/userData de bytes copiados; FlowModule realiza detach conjunto.

CP-R13: file-select SaveLoaded→GameMode Speedrun→onGameFrame/overlap y,por separado,UI Overlay→LiveSplit Context→send/poll. PORT-006..009; Borealis ausente bloquea entrega/cierre/copias de transporte.

CP-R14: Acch GroundCheck→dBgS/dBgW ride→swpush flags/timers/modo→switch RAM y vértices→lector al recargar→Release/heap. PLAYER-035..039; no wiring de stage concreto ni persistencia CARD inferida.

CP-R15: KYTAG06 tipo11 darkworld/layer/stay room→colpat gather→exeKankyo→drawKankyo/setLight/paletas→fog global→partículas6..11/GX. PRES-048..051; no ownership por tag ni orden universal/external DX12 probado.

CP-R16: éxito vanilla→notificación→flush IDs dirty→IO por mod→dirty conservado/reintento por evento; invalidación save manager borra caché sin flush. WORLD-034..037. No transacción conjunta ni ACK de sidecar en servicio.

CP-R17: registro BST→(sync lifecycle,NO sync BST en frameEnd observado)→mapa activo shared_ptr→Z2SoundMgr/JAISe/JAISound. PRES-052..055; retirada del SlotMap no prueba fin de mapa ni reproducción.

CP-R18: stage record → lookup profile → create request por nombre → actor queue → delete queue → slot/profile. ActorHandle generacional no viaja en la petición; unregister barre las dos últimas colas de instancia, no toda petición pendiente (PLAYER-040..045). Loader deactivation no aporta veto al resultado.

CP-R19: screen/archivo prestado → MAT1 material propio → TBX2 Ex condicionado → texto propio y font prestado → dibujo → clean y pane destructor. Flags del consumidor no prueban contenido del asset (PRES-056..059).

CP-R20: UiService binding toggle → ConfigVar::setValue → copia core subscriptions → bridge snapshots SDK; unsubscribe/unregister retiran registro vivo, no la copia en curso. Valor efectivo → dirty → save es una ruta distinta (CALLBACK-014..018).

CP-R21: escritor de estado B_OB → actor de agua → matriz prestada de modelo/fondo → Move → consulta registrada SplGrpChk → Acch → Link.mWaterY; colisión y visibilidad se retiran por rutas diferentes. Recarga consulta flag stage, no altura persistida (PRES-060..064).

CP-R22: TGSC puntero tipado/stride → tramo base+escala → CRC de bytes → patch/append; adición SDK vector owned → temporal → append → request. Registro binario endian, stride y longitud pública son magnitudes distintas (WORLD-038..040).

CP-R23: Tag MYNA2 gates→request ID/switch→NPC tipo1/fases→daNpcF acción→orderEvent→staff/cut→estado demo→reset; salida normal→switchOFF/delete→destructor. Variantes2/3 tienen otro origen y no son continuación automática del tag (PLAYER-046..051).

CP-R24: logo stage-request→scene waits→overlap task; error task→managerNULL no se propaga como error al wait booleano. Cancel de destino y Done scene tienen cleanup distinto de exclusión; no reconstruyen previo (ARCH-008..011).

CP-R25: tabla overlay/generación→JKRMemArchive fetch→decodificación→mRes→getObjectRes; cambiar tabla no hace el recorrido inverso ni redecodifica cache. Prioridad de fuentes y actualización del consumidor son fronteras separadas (PRES-065..067).

CP-R26: CVar/callback UI explícito→discord.initialize→initialized→main01 callbacks/update gate15s→payload de último stage/estado→clear/shutdown. CVar registrada sin handler automático no activa backend por toda escritura; backend Borealis/ACK externo pendientes (PORT-010..013).

CP-R27: idioma→msg_folder→PLAY mount archive1→HUD zel_XX.bmg→stage pointer→changeGroup parse/bind→getString/Explain. Archivo99→índice lógico9; commandDone,parseOK y texto listo son fases distintas (PRES-068..073).

CP-R28: m_Do_main/Aurora SDL→Window lookup→callback game-thread; teardown inverso Gfx→Window libera claim antes de destruir SDL window (CALLBACK-019..022). Entrega/backend externo sin verificar.
