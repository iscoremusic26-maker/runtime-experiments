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

CP-R29: KYTAG07 posee LIGHT_INFLUENCE→kankyo presta puntero→selector por posición→settingTevStruct tipo0/J3D; IsDelete/room/overlap→cola framework→Delete/cut antes de liberar actor. PRES-074..077; no registro owned ni servicio de luz dedicado.

CP-R30: B_DS2/colliders→daño/cc_at_check→DEAD→potential event/INDEMO→cámara/timers→switches/progreso/reward PC→delete/resource/audio. PLAYER-052..056; IO save y concesión diferida fuera de esa llamada. Véase combat_damage.

CP-R31: PLAY Draw/Execute→resetToOpening→card command/SaveSync→nextStage/audio/restart→ChangeReq/ReRequest→perfil OPENING compartido→resource/audio gates→startStage/TITLE/reset cleanup. ARCH-012..016; sidecar/IO no confirmados por esta cadena.

CP-R32: archive→ModelData prestado→modelo Sakuita(heap actor) y dummy(heap gestor)→lista temporal500→room gate/J3D→reset lista; bajas balanceadas y teardown scene separados del archive. PRES-078..081. dMdl_mng_c es otro gestor,no alias del simple-model.

CP-R33: HttpService→task owned/handle→registry frameBegin→ready handles/relookup→snapshot prestado/callback→erase; deactivating take_all distinto de cancel. Descarga incluye publicación local,con Task/atomic_replace Borealis sin garantía interna disponible. CALLBACK-023..027.

CP-R34: Link collider tipo/material→FireWood Tg hit→lit/timer→switch home room y luz/partículas; emitterID renueva actividad→particle calc3D→retiro bajo event gate. PLAYER-057..060. Switch RAM,actor,luz,emitter y audio tienen vidas diferentes; sin apagado por switchOFF en actor vivo.

CP-R35 PORT-014..017: port_support→hud_ui_text (evento/documento/mensajes)→runtime_and_lifecycle (ownership de consola y reloj). rate→Aurora time queda frontera external_dependencies,sin backend ni frecuencia comprobados. Comandos host fijos,distintos de SDK-015 LogService.

CP-R36 PRES-082..085: hud_ui_text (dMw captura)→cameras_rendering (drawlist/Painter)→runtime_and_lifecycle (gate ticks/pause). Interpolación tiene sync local,no fence; external_dependencies Aurora pendiente. Retorno void de registro2D no confirma aceptación.

CP-R37 PLAYER-061..064: other_systems(tag/shop)→actors_ai_npcs(solicitud/actor display)→cutscenes_dialogue(event024)→flags_events_progression(save-switch RAM)→inventory_equipment(ItemService previo). Oculto,índice sold-out,requestID y venta/persistencia son estados distintos; tabla tags presta punteros,sin ownership de hijo por parent.

CP-R38 PRES-086..089: environment_weather_time(KYTAG08)→models_animations_materials(MA11/TexMtx) y player_and_controls(FogFade); audio_particles_effects recibe radio/emisores/trigger. Kankyo presta puntero a actor; Delete de efectos no equivale a limpiar referencia del consumidor.

CP-R39 PRES-090..093: models_animations_materials→actors_ai_npcs(contexto userArea),audio_particles_effects(BAS/sound prestado),memory_ownership(heap/ModelData/arrays) y runtime_and_lifecycle(fase exec/draw/cleanup). Callback joint y morph temporal no son callbacks SDK ni pesos de audio continuos.

CP-R40 PRES-094..097: sdk_services(InterpService)→runtime_and_lifecycle(ventana)→cameras_rendering(sombra fallback). Registro por mod y muestras globales tienen identidades/vidas distintas; owner-key no es namespace aislado. SDK-013 aclara buffer copiado,no userdata retenida.

CP-R41 PLAYER-065..068: other_systems(StartAndGoal)→cutscenes_dialogue(cut caller,MsgTime formatter)→hud_ui_text(Timer screen/msg)→runtime_and_lifecycle(borrado tras closeAnime). Global modo/puntero/tiempo no son propiedad de actor por requestID ni save durable.

CP-R42 PORT-018..021: port_support(iso wrapper/worker)→hud_ui_text(prelaunch modal/progreso)→runtime_and_lifecycle(join/publication); external_dependencies Borealis aporta verify/inspect/Progress sin backend disponible. Config save nominal y metadata no equivalen a hash nuevo ni juego ejecutando.

CP-R43 ROOT-011..013: runtime_and_lifecycle(msg wrapper)→memory_ownership(heap propio específico)→hud_ui_text(Timer screen/drawtag). Drawtag corta publicación visual,no destruye storage ni adopta ownership de actor. Gate scenePause distinto de pauseFlag/talk.

CP-R44 PRES-098..101: models_animations_materials(McaMorf BAS)→audio_particles_effects(Z2Creature/evento/pool)→memory_ownership(posición/evento prestados). AudioResService suministra recursos por otro contrato; retirar handle no confirma voz detenida ni mixer drenado.

CP-R45 PRES-102..105: models_animations_materials(deformer/índices)→memory_ownership(buffers vs ModelData compartido)→cameras_rendering(packet arrays)→resources_archives_overlays(ARC). Instalación parcial y punteros swapped impiden equiparar overlay/retorno con actualización completa de modelo vivo.

CP-R46 CALLBACK-028..031: sdk_services(WebSocket)→callback_ownership_and_cancellation(vistas de polling permod,sin callback)→runtime_and_lifecycle(take_all/pollstate); external_dependencies(BorealisConnection) pendiente. FrameBeginHTTP no aplica a WebSocket.

CP-R47 PRES-106/107: environment_weather_time(controladorKANKYO)→runtime_and_lifecycle(gates/proceso) y memory_ownership(global distinto de proceso). Retirar drawtag controlador no prueba retiro del consumidorMA11 en fondo separado; PRES-089 sigue condicionado.

CP-R48: cápsula At→callback flecha→ID/offset joint→matriz objetivo reconsultada→flag/cola delete. PLAYER-069..072; actor,modelo y colisionador tienen vidas distintas. [Combate](systems/combat_damage.md).

CP-R49 WORLD-041/042: ground/RTBL→room flags8/20→iterador layer→delete requests→BG cleanup cuando se ejecuta. Flags y retorno del iterador no prueban drenaje;PRES-089 sigue parcial. [Salas](systems/stages_rooms_layers.md).

CP-R50 PRES-108..111: ARC BTP→wrapper/frameCtrl→descriptor material prestado→TevBlock texNo. Remove desactiva slot,sin restauración previa;callback de heap usa bool,no fases. [Modelos](systems/models_animations_materials.md).

CP-R51 CALLBACK-032..034: Ui descriptor→shared ModControlSpec→Button Confirm→guard pane/active→mod callback→SlotDetach/modDetached. Hostclosure no mantiene userdata/DLL;guard no drena llamada iniciada. [Callbacks](systems/callback_ownership_and_cancellation.md).

CP-R52 PLAYER-073..076: E_RD request→E_ARROW→colisiónescudo→Link lista16/contador→flagreset→delete específico. IDs y offset prestados no son ownership;item solicitado/contador no garantizan recompensa durable. [Combate](systems/combat_damage.md).

CP-R53 CALLBACK-035/036,PORT-022: GameMode callback→state prestadofile-select→gates/nameinput;modDeactivating→modo vanilla/reset solicitado. No saveACK ni rollback de callbacks. [Runtime](systems/runtime_and_lifecycle.md).

CP-R54 PRES-112..114: home room switch→KYTAG02 camposglobales→KANKYO wind_set/suavizado→Kita poses/audio. Sin registroowner ni rollbackprevio;no transferencia de puntero actor. [Ambiente](systems/environment_weather_time.md).

CP-R55 PRES-115..118: vectoractor→emisor userWork→JPA trace→levelrenewal/cleanup. Callbackglobal no posee Vecactor;orden global de free/calc pendiente. [Efectos](systems/audio_particles_effects.md).

CP-R56 ARCH-017..020: CLI→SaveRequested→LoadSync→RAMsave/init→gameStart→PLAYrequest/ff. Log y ff no son ACKescena ni sidecar. [Runtime](systems/runtime_and_lifecycle.md).

CP-R57 PLAYER-077..080: switch→GateEND→modelomatriz→MoveBG mBgMtx→CrrFunc→poscorregida;DeleteARC→ReleaseBG→heap. Punterosprestados/retornossonfronterasdistintas. [Puzzle](systems/other_systems.md).

CP-R58 PRES-119..122: TextureSDK→ownedbytes/handle→registroAurora→lifecycleprioridad/reregistro→unregister/keepalive. Contratobarreraexterna no es backendleído;selectorfinalBLOCKEDlocal. [Recursos](systems/resources_archives_overlays.md).

CP-R59 PORT-023..025: UIretry→operaciónPending→lote/coalescingporID→lifecycle→estadoUI;failuretoast esflujo histórico aparte. Operaciónshared no retieneDLL. [Runtime](systems/runtime_and_lifecycle.md).

CP-R60 PLAYER-081..084: BoomerangAt→CarryTg→offsetmiembro→relookupBoom→Acch/reoffset→Linkcarry/wait. Fintransporte noactordelete/Itemgrant;helpercheckmutante. [Otros](systems/other_systems.md).

CP-R61 ROOT-014..016: direcciónthis→heapowner→listaDisposer→destructorvirtual→resetarena/heapchild. No destrucción universal de cada allocation ni cleanupdecallbacksexternos. [Memoria](systems/memory_ownership.md).

CP-R63 PRES-123..126: perfil/procesos→TagWaterFall→camera0/AllJudge→gather y fog compartidos→KANKYO/setLight. Boolean maestro e ID tienen duraciones diferentes;Delete local no prueba reset de unidad o restauración ambiental. [Ambiente](systems/environment_weather_time.md).

CP-R64 PLAYER-085..088: Acch→BG propietario/rider→Ice_s campos→Mtx modelo/BG→draw;resDelete específico precede Release del wrapper. No switch/guardado ni rotura en esta muestra. [Otros sistemas](systems/other_systems.md).

CP-R65 PORT-026..028: LogService→contextID→bufferhost mutex/copias→LogsWindow/elementos y clear lógico;por separado report Borealis. Datos host propios,no callbacks retenidos. [Diagnóstico](systems/port_commands.md).

CP-R66 PRES-127..130: bloqueBRK→TevRegKey prestado→IDs de material→slots CReg/KReg→MaterialAnmcalc→TevBlock;wrapper/FrameCtrl propio no posee bloque completo. DeleteARC/BG y retirotracks son fronteras distintas. [Modelos](systems/models_animations_materials.md).

CP-R67 CALLBACK-037..039: FileService→Borealis ListResultlocal→FileEntry prestado→callback/sentinel;wrapperSDKcopia→vectorpropio. Sin registroretenido ni frameBeginlist;estadoactive y retorno terminal distintos. [Ownership](systems/callback_ownership_and_cancellation.md).

CP-R68 ARCH-021..024: switchroom→KYTAG04→orderqueueevent→timerexecute→selectorPLAYER/Linkgate→SCLS→nextstage→callerPLAY;drawtimer/partículas son faseaparte. Deleteemisores no rollbackglobal. [Runtime](systems/runtime_and_lifecycle.md).

CP-R69 PRES-131..134: parámetros de demo→BLS/DeformData y BLK/pesos→deformer→arrays locales del modelo→calc antes de joints/skin. Heap del actor no posee por sí solo todo bloque de archive ni referencias externas de demo. [Modelos](systems/models_animations_materials.md).

CP-R70 PLAYER-089..092: Link/animación→Keep/señalDigpl→switchhomeRAM→peticiónitem→delete. Ownership de actor/item y persistencia del switch son fronteras distintas. [Otros sistemas](systems/other_systems.md).

CP-R71 PRES-135..139: parámetros/pathroom+olor→KYTAG03→copiasenpool ambiental→weather/update/draw;audioacumula valores de cámara/path,emisor84ED y handshakeLinkson ramaaparte. Limpieza global no pertenece exclusivamente altag. [Partículas](systems/audio_particles_effects.md).

CP-R72 CALLBACK-040..042: Filepicker→reserva global/sharedpending→backendcallback uoverrideframeBegin→guardowner→callbackprestado→copiasSDK;modDetachednulifica compartido,no cancela backend demostrado. [Callbacks](systems/callback_ownership_and_cancellation.md).

CP-R73 PLAYER-093..095: Linkstart/end→actorarena→GroundCross/timer→posemodelo/BG→switchRAM/delete. Sin CrrFuncTypicalRotY en esta muestra;retirada ARC/BG distintas. [Otros](systems/other_systems.md).

CP-R74 PRES-140..142: slotGfx→callbackrenderworker→WorkerFailure(ID/string)→frameBeginloader→retiradaGfx→fail_mod. Mutexcola y backend synchronize cubren fronteras distintas. [Render](systems/cameras_rendering.md).

CP-R75 PLAYER-096..098: BGMóvil/agua→identidadOnsen→Linkgates/timer→deltaLifecompartido→Meter/SaveRAM. Retiraractor oBG no revierte delta yaemitido. [Jugador](systems/player_and_controls.md).

CP-R76 CALLBACK-043..046: TCPrequest→handleclosedgate→pollCONNECTED→sendqueue→pollCLOSED/erase;ModState posee payloadhost,NetEventC posee endpointarray yhelperC++solo views. [Ownership](systems/callback_ownership_and_cancellation.md).

CP-R77 PRES-143..146: montaje DVD→archive prestado a JAU→descriptor copiado con punteros prestados→región de audio→JAISeq→reciclaje por isUsingSeqData. Cache archive y buffer caller poseen vida distinta. [Recursos](systems/resources_archives_overlays.md).

CP-R78 PLAYER-099..102: Hena/dialogue→timer6→controlador/tabla/bola→cam73/76→eventReg/rewardpending→reset cámara/reentrada. Estado repartido entre actores, globals, timer y eventRAM. [Otros sistemas](systems/other_systems.md).

CP-R79 PORT-029..031: logging options.divert —backend no disponible→ callback matcher→StubLogBuffer/offsets→ImGui→PostDraw clear salvo pausa. Es otra política que LogService ring2048. [Diagnóstico](systems/port_commands.md).

CP-R80 PRES-147..150: parámetros/room→KYTAG13 escribe nieve prestada→weather posee packet→lista translúcida→GX;countnormal y counttag separados. Cleanup global KYEFF distinto de Delete tag. [Ambiente](systems/environment_weather_time.md).

CP-R81 ARCH-025..028: atenciónKYTAG05→orden/eventSTART→Linklatch→SCLS/NextStage→mode6peep→input→mode7→posición/cámara TurnRestart. Estado porvalor sobrevive a actor;no rollback transaccional. [Lifecycle](systems/runtime_and_lifecycle.md).

CP-R82 CALLBACK-047..049: descriptorcopiado→UiSlotmenu/documento→dismiss/oncloseerase→anchorlive+active→callback→transitionend/closed/UIerase. Moddetach toma slots y forcehide;ownership distintos. [Callbacks](systems/callback_ownership_and_cancellation.md).

CP-R83 PRES-151..153: MidnaARC/heap→modelo prestado+packets porjoint→posiciónsortconsumida→Zxlu lista con punteros→paseZ→resetbucket/heapactor. [Modelos](systems/models_animations_materials.md).

CP-R84 PLAYER-103..106: LinkPlayerFly/Tmp31→NpcTeventOrder→staffcutJump→tagsArea+pareja→GOAL→door.open/Execute/Destroyed→SW2/cutEnd→Createposterior. [Otros sistemas](systems/other_systems.md).
