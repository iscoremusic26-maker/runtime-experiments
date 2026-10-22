# Checkpoints documentales

## CP-R00 — auditoría e inventario

Campaña iniciada el 20 de octubre de 2026 (zona del usuario: America/Panama; registros de herramientas en UTC del día 21). Se verificaron repositorios, rama base privada, commit/tag upstream y bytes de los árboles locales. Se creó una rama aislada desde CP00 y se inventariaron 19367 archivos sin modificar fuente. Se identificaron cuatro submódulos ausentes y una discrepancia Android explícitamente excluida de afirmaciones técnicas. Los informes profundos se incorporarán en checkpoints posteriores, conservando sus niveles de evidencia.

No se ejecutaron compilaciones, CI nuevas ni el juego. No se creó un mod, tag, release ni merge. El prompt no forma parte de estos documentos.

## CP-R01 — recuperación y primer contenido técnico (21 de octubre de 2026)

Continuación desde HEAD remoto CP-R00 verificado. Recuperados informes de hooks/loader y SDK, contrastados y publicados con evidencia y símbolos. Se precisó la métrica: 26 candidatos de módulo, sujetos a disponibilidad; 25 contratos C y 209 ranuras públicas actuales. Se documentan rollback de init fallida, replace de slot único, orden de ticks y límite de cleanup de actores propios. Sin repetir inventario, compilar ni ejecutar juego; sin PR nuevo.

## CP-R02 — escenas, guardado, bancos de estado y narrativa

Integrados borradores recuperados tras revisión de SaveService/StageService y consumidores. Cinco fichas, 33 evidencias nuevas y símbolos; correcciones sobre TGSC (assert histórico inactivo PC) y rangos acumulados de switches. No se equipara callback de guardado con durabilidad de sidecars ni retirada de edición con borrado de actor vivo.

CP-R02a: validación de relaciones detectó sistema de física no declarado para un símbolo KCL; índice corregido y referencias,IDs y rangos comprobados. Se consolidó el handoff acumulado.

## CP-R03 — recuperación de fichas y síntesis de integración

Integrados13 informes recuperados de jugador/actores/presentación/memoria/histórico y matriz .dusk. Revisadas invalidaciones ARC,expectativas externas de texturas,sincronización Gfx condicionada y punteros de viento. Se conserva profundidad selectiva; no se promueve CI a runtime.

## CP-R04 — cancelación de callbacks y precisión de citas

Nueva lectura transversal: Save copia registros completos, Host revalida handles y Camera revalida handle+owner activo. Se documenta inferencia condicionada de userdata vencida sin afirmar fallo runtime. Cuatro evidencias y dos slots nuevos; corregido anclaje histórico CP00 de L15 a L12 tras consultar archivo exacto.

## CP-R05 — síntesis, dependencias y handoff

Añadidos ARCHITECTURE, SYSTEM_DEPENDENCIES, RISK_REGISTER, OPEN_QUESTIONS y métricas. ARCH-001 contrasta el orden del scheduler con sus gates. SYSTEM_INDEX incluye rutas, dependencias y estados; soporte inventariado se mantiene separado de áreas leídas. Siete erratas nominales corrigen branding/MemCard sin duplicar FILE_INVENTORY. Se precisa la diferencia entre ocurrencias y rangos únicos de referencias, y la fila AudioRes no afirma sync BST por frame frente a PRES-024. Índice maestro y handoff reescritos alrededor del estado publicado.

Esta continuación tuvo checkpoints cortos R01, R02/R02a, R03, R04 y R05, sin crear PR ni modificar producción. El intervalo inactivo entre sesiones no cuenta como investigación. Ver RESEARCH_METRICS para tiempo de sesión observado y límites de medición.

## CP-R06 — Item resolvers, snapshots y consumidor cofre

Contrastados contrato 2.3, registro/retirada, copia PendingResolve sin handle, orden por mod/vector, active-check y efectos de detach. Consumidor TARGET_PC daTbox_c::create1st enlaza la resolución a parámetros del cofre. Cuatro evidencias y tres símbolos nuevos. La cancelación tardía es inferencia condicionada; el contrato exige ausencia de efectos secundarios y no se promete reentrancia. Sin runtime, builds ni mod.

## CP-R07 — fuente BFN, ownership J2D y consumidor file-info

Contrastados provider logo/font archive, initFontCommon y rama PC, refcount mDoExt, JUTResFont con backing prestado, binding J2DTextBox y release del consumidor. Cuatro evidencias y cuatro símbolos netos. HUD mantiene READ global con una cadena CROSSCHECKED; no validación de glifos, overlay ni rendering runtime.

## CP-R08 — logros internos del port y persistencia

Cadena señal de menú→check→progress/unlock→UI/JSON contrastada, con gates vanilla/speedrun y loaded/dirty. Un retorno de save no confirma IO ni conserva retry bajo fallo capturado. Cinco evidencias y cuatro símbolos; nueva ficha real, port_support READ parcial. Sin leer datos personales ni registrar un supuesto AchievementService inexistente.

## CP-R09 — reloj ambiental,tag y rollover

Contrastadas condiciones del avance normal,ruta KYTAG11,parametrización y flag de control por actualización,helper DayProc y clasificación día/noche. Se precisa salida Time→audio→Date y estado en memoria frente a CARD. Cuatro evidencias y dos símbolos; entorno permanece READ global. Sin manipular tiempo ni save del usuario.

## CP-R10 — file-select → PLAY, fases y ownership

Desde CP-R09 remoto 03f2a405fbab7f8d2caed286bffd37728eaf07d4. Se contrastan caller/gates PC, aceptación, cola delete-before-create, destructor UI/heap, entrada PLAY, overlap/pausa y cancelación/ReRequest. Seis evidencias y seis símbolos nuevos; cero documentos nuevos. Se deduplica la referencia repetida ARCH-001 en runtime del SYSTEM_INDEX, sin borrar evidencia. Q-09 permanece parcial; sin mod,build o ejecución.

## CP-R11 — J3D/morf/BCK/BTK con consumidor y teardown

Padre CP-R10 e44139795c4e0beb1e1bf608bd894d0656a06c4b. Cuatro evidencias y cuatro símbolos nuevos,+0 documentos. Cadena AutoMata resLoad/heap→setAnm→execute/draw→resDelete/heap teardown; setAnm puede fallar después de cambiar BCK. Models conserva READ global; sin assets modificados ni runtime.

## CP-R12 — MessageService y lifetime de dispatch/texto

Padre CP-R11 b90b9ebef217c8fd21510e152819e0570271d92d. Cinco evidencias nuevas (cuatro contrastadas,una inferencia condicionada),cuatro símbolos,+0 documentos. Se distingue snapshot sin revalidación,retirada por dueño y texto compartido retenido por control/processor; consumidores JMessage y selección dMsgObject. No repetir prioridades de WORLD-025/PRES-020 ni prometer reentrancia.

## CP-R13 — soporte interno speedrun/LiveSplit

Padre CP-R12 893106a330b128d4743f51de54e03d7cb84f8f4c. Ficha real nueva,cuatro evidencias y tres símbolos; evento SaveLoaded→modo/contador y UI→conexión/envío/cierre separados. Sin LiveSplitService público,ACK ni backend Borealis auditados. Ninguna conexión ni dato personal abierto. Neto desde CP-R09:+19 evidencias,+17 símbolos,+1 documento; cuatro cadenas representativas de familias distintas.

## CP-R14 — swpush contacto,debounce,switch y cleanup

Padre remoto verificado 36c71128be0cda32b4ee5ef30dd0ace49ff92404. +5 evidencias,+5 símbolos,+0 informes/+0 archivos frente a CP-R13; una cadena nueva de puzzle/colisión. CP-R14 completo en systems/other_systems.md: PLAYER-035..039 y cinco símbolos daObjSwpush::Act_c. Dispatcher Acch/dBgS/dBgW→rideCB→contadores/modos→switch al finalizar recorrido→colisión/recarga→Release/heap. Sin prueba de wiring entre colocaciones ni durabilidad CARD. RELEASE/error/create parcial conservan límites; other_systems sigue READ global. Sin mod,build ni runtime; solo atlas.

## CP-R15 — patrones ambientales por layer y fog consumidor

Padre remoto verificado 9a1e2434daaa1c32faa48f3db32aba028ef85e26. +4 evidencias,+3 símbolos,+0 informes/+0 archivos frente a CP-R14; una cadena ambiental nueva. CP-R14: swpush PLAYER-035..039,cadena contacto/switch/cleanup. CP-R15 completo en environment_weather_time: PRES-048..051 y tres símbolos,type11 KYTAG06→gather→paletas/fog→partículas. Cambio solicitado y aplicado son fases distintas; Delete tipo11 no revierte estado global. Ambiente sigue READ; otras variantes/agua/orden exacto y backend pendientes. Sin mod,build ni runtime; solo atlas.

## CP-R16 — sidecars: error,reintento y vida de caché

Padre remoto verificado 25d8a4f2b45d4ed3d88ecbeeb0c6d6345384ab60. +4 evidencias,+3 símbolos,+0 informes/+0 archivos frente a CP-R15; corrección de integración de un símbolo interno (OFFICIAL_SERVICE→POTENTIAL_REQUIRES_VERIFICATION),sin borrar evidencia. CP-R14 swpush PLAYER-035..039; CP-R15 KYTAG06/paletas/fog PRES-048..051; CP-R16 completo en save_load,WORLD-034..037,helpers flush/write/invalidate. Fallo conserva dirty hasta siguiente evento/vida de caché; JSON usa estado actual de3slots. Invalidate elimina store,sin flush. Menú/autosave no recibe resultado de sidecar. Corrección trazable del símbolo save_slot_written a integración interna; no cambio de contrato público ni producción. Sin mod,build ni runtime; solo atlas.

## CP-R17 — BST: publicación de mapas,retirada y consumidor SE

Padre remoto verificado 904e7f1d59e09752fa418e5a7b6dc79cc299a540. +4 evidencias (3 contrastadas,1 inferencia condicionada),+3 símbolos,+0 informes/+0 archivos frente a CP-R16; una cadena audio nueva. CP-R14 swpush PLAYER-035..039; CP-R15 KYTAG06/paletas/fog PRES-048..051; CP-R16 retry sidecar/caché WORLD-034..037 y corrección de clasificación save_slot_written. CP-R17 completo en audio_particles_effects,PRES-052..055,tres símbolos BST. FrameEnd llama WSYS; única sync BST localizada entra por lifecycleApplied (init/requests). Retiro no marca dirty ni publica mapa; consumidor SE captura shared_ptr. Edición posterior a init sin nuevo lifecycle puede diferirse (inferencia condicionada). Q-08 parcial,no bug/audio runtime probado. Cadenas nuevas de esta continuación:4;sin promoción global,documentos nuevos0. Sin mod,build ni runtime; solo atlas.

## CP-R18 — ActorService: solicitudes, borrado forzado y teardown

Padre remoto verificado 1ca9ccbd38dc6e266e4ba39d9a15680caa6f9f43. +6 evidencias (5 STATIC_CROSSCHECKED,1 STATIC_INFERRED),+4 símbolos internos; 0 fichas nuevas; Q-03 parcial. PLAYER-040..045 contrastan request-only, publicación temprana del actor, forceDelete, cancelación/profile lookup y consumidor stage. No todas las creaciones pendientes escapan; no se acredita drenaje ni unload seguro. HOOK-029/PLAYER-023 ampliados, sin invalidar sus límites. Sin mod,build ni runtime; solo atlas.

## CP-R19 — TextBoxEx: loader, material prestado y texto propio

Padre remoto verificado 3d0de345494491cf417601bdb794f8f4cfc4618c. +4 evidencias STATIC_CROSSCHECKED,+3 símbolos;0 fichas nuevas; HUD sigue READ parcial. PRES-056..059: ruta TextBoxEx condicionada por tag/flags, copia de texto y ownership de material/TevBlock; loader falla con bool no comprobado por file-info. No se afirma que el asset concreto use TBX2 ni que setString devuelva ACK de allocation/dibujo. Sin mod,build ni runtime; solo atlas.

## CP-R20 — ConfigService: notificación, snapshots y consumidor UI

Padre remoto verificado d565c3ad7b93badeaa116702c994d479be99656a. +5 evidencias (4 STATIC_CROSSCHECKED,1 STATIC_INFERRED),+4 símbolos (2 slots oficiales,2 localizadores);0 fichas nuevas. CALLBACK-014..018 contrastan notificación Config síncrona, orden de snapshot, retiro sin revalidación, mutación recursiva y toggle UI con relookup. SDK-004 ampliado; MOD_OK no certifica flush ni snapshot agotado. Sin configuración personal consultada. Sin mod,build ni runtime; solo atlas.

## CP-R21 — Agua: fondo móvil, consulta y recarga

Padre remoto verificado 1e50777525d111ec86f650f427ba961efcbdf983. +5 evidencias STATIC_CROSSCHECKED,+4 símbolos;0 fichas nuevas; ambiente sigue READ parcial. PRES-060..064 contrastan Obj_Lv3WaterB, escritor externo, transformación de fondo, consulta Acch/Link y cleanup/reload. Malla concreta/orden entre perfiles condicionan resultado; modelo oculto no prueba registro retirado. Sin agua/clima universal ni efecto runtime demostrado. Sin mod,build ni runtime; solo atlas.

## CP-R22 — TGSC: stride, CRC, endian y adiciones

Padre remoto verificado d5545fee53df860ac9ed2dc07890648bb2ec5f35. +3 evidencias STATIC_CROSSCHECKED,+2 localizadores;0 fichas nuevas; Q-07 parcial y redacción histórica de símbolo rectificada. WORLD-038..040 contrastan TGSC stride frente a tramo CRC/edición, BE y transporte de adición a append. Entrada stage_tgsc_data_class rectificada para no afirmar sizeof Windows0x24; WORLD-033 conserva validez. Sin nuevo layout medido ni serializer/mod generado. Sin mod,build ni runtime; solo atlas.

## CP-R23 — MYNA2: activador, NPC, evento y retirada

Padre remoto verificado 105ea48f71ea29909c0700a7376b88f2d6da548f. +6 evidencias (5 STATIC_CROSSCHECKED,1 STATIC_INFERRED),+4 localizadores;0 fichas nuevas; Q-12 READ selectivo. PLAYER-046..051: Tag pide tipo1 y marca switch en aceptación; tipo1 selecciona FIRST_TALK y tiene retirada por distancia; failure/goal/success son variantes separadas. Efecto demo/cut/reset contrastado; assets y recompensa final no probados. Fuente MYNA2 local contrastada con cuatro blobs remotos exactos. Sin mod,build ni runtime; solo atlas.

## CP-R24 — Escenas: error de overlap, cancelación y exclusión

Padre remoto verificado 24bc5eda073dffddfd7079c11a62874694770316. +4 evidencias (3 STATIC_CROSSCHECKED,1 STATIC_INFERRED),+3 localizadores;0 fichas nuevas; Q-09 parcial. ARCH-008..011 distinguen rechazo inicial, task overlap ausente y fallo destino; managerNULL no equivale a señal de error al wait ni limpieza de exclusión scene. Logo StageRequested consume flags sin comprobar ChangeReq. Sin deadlock ni rollback runtime demostrado. Sin mod,build ni runtime; solo atlas.

## CP-R25 — Overlay ganador: lectura JKR frente a cache dRes

Padre remoto verificado b568395f73122d467fae22d6b3b923713174c428. +3 evidencias (2 STATIC_CROSSCHECKED,1 STATIC_INFERRED),+3 localizadores;0 fichas nuevas; Q-14 parcial. PRES-065..067 añaden consumidor JKRMemArchive y cache dRes: getObjectRes no relee tras cambio de generación, mientras fetch JKR puede resolver nuevo recurso o backingARC. Precedencia SDK-018 no se duplica; backend selector y coexistencia siguen sin certificar. Sin mod,build ni runtime; solo atlas.

## CP-R26 — Presencia del port: gates, payload y shutdown

Padre remoto verificado 4f45eafa7c96f828ce9f71cefde42346fca07716. +4 evidencias (3 STATIC_CROSSCHECKED,1 STATIC_INFERRED),+3 localizadores,+1 ficha nueva; soporte sigue READ. PORT-010..013 y nueva ficha port_presence: configuración/UI, init, mainloop/15s, payload y shutdown. bool/local log no es ACK; Borealis faltante impide certificar ownership/reconexión. Sin cuenta/red/configuración personal consultada. Sin mod,build ni runtime; solo atlas.

## CP-R27 — Localización: mount BMG, grupo, consumo y cleanup

Padre remoto verificado a750edfa56d6a4d6c80b0621d0180b03c2e0c08d. +6 evidencias (5 STATIC_CROSSCHECKED,1 STATIC_INFERRED),+4 localizadores;0 fichas nuevas; Q-10 parcial. PRES-068..073 contrastan idioma/carpeta, archivo99→grupo9/zel_99, comandoDone distinto de mountOK, parse/bind y Explain, cleanup y reinicio requerido UI. Sin asset BMG ni refresh/Windows probado. Sin mod,build ni runtime; solo atlas.

## CP-R28 — WindowService: evento dirigido, consumo y retirada

Padre remoto verificado 4fca4d1963d8808456766152787b7b92ae1eed0b. +4 evidencias CALLBACK-019..022 y +3 símbolos; ningún documento nuevo. CALLBACK-019..022 contrastan contrato,caller main/launchUI,consumo por SDL ID,event prestado,error y teardown Gfx→Window. Sin entrega Aurora ni unload Windows probados. Sin mod,build ni runtime; solo atlas.

## CP-R29 — KYTAG07: influencia prestada, selección y retirada diferida

Padre remoto verificado 75606d6e033d0d498320003fb47dd370189a4442. +4 evidencias PRES-074..077 y +4 símbolos; ningún documento nuevo. PRES-074..077 contrastan KYTAG07→puntero pointlight→selección/settingTevStruct y retirada99/room/overlap→cut. La pista dungeonlight se descarta; fallo de capacidad/índice,orden/visibilidad Windows pendientes. Sin mod,build ni runtime; solo atlas.

## CP-R30 — B_DS fase2: daño, permiso de demo, progreso y cleanup

Padre remoto verificado b54c598a2ec269ceacf15c390e4d075cb400fad6. +5 evidencias PLAYER-052..056 y +3 símbolos; ningún documento nuevo. PLAYER-052..056 contrastan B_DS fase2: SPINNER knockdown≠HP,weak hit→DEAD,potential request≠INDEMO,máquina de salida→flags/cola PC→delete. Geometría,concesión posterior,cleanup externo completo y Windows no probados. Sin mod,build ni runtime; solo atlas.

## CP-R31 — Reset PLAY→OPENING: gates,preparación y aceptación de cola

Padre remoto verificado 74d7eecf7528867aa1fe43d47652a44f33e2b9bc. +5 evidencias ARCH-012..016 (4 contrastadas,1 inferencia condicionada),+4 localizadores,+0 documentos. ARCH-012..016 contrastan reset y entrada OPENING compartida con PLAY. Next-stage se reactiva,SaveSync consulta sin IO,request/retarget ignorados; se delimita elegibilidad de ID previo. Sin runtime/ABI Windows ni rollback global comprobados. Sin mod/build/runtime; solo documentación.

## CP-R32 — Modelos simples: clave compartida,lista temporal y baja

Padre remoto verificado 85e959b8b558fa7be6bf558699101d0003f7fa15. +4 evidencias PRES-078..081,+3 localizadores,+0 documentos. PRES-078..081 contrastan Sakuita→simple-model(ModelData+room)→lista raw→draw→remove/scene cleanup. Dos capacidades8/500,fallos sin abort actor y bajas sin ACK. dMdl_mng es distinto;sin LOD/skin ni render Windows probado. Sin mod/build/runtime; solo documentación.

## CP-R33 — HttpService: finalización,datos prestados y cancelación

Padre remoto verificado 0459f0a4b16097a950c1e4d3e84cc5a62622e41a. +5 evidencias CALLBACK-023..027 (4 contrastadas,1 inferencia),+3 símbolos (1 slot oficial,2 localizadores),+0 documentos. CALLBACK-023..027 contrastan Http request→task→ready handles→callback snapshot→erase/cancel/take_all y publicación local de descargas. Backend Borealis,destructor/join/atomic_replace/headers internos BLOCKED; sin request de red,ABI/runtime Windows ni integración Claude. Sin mod/build/runtime; solo atlas.

## CP-R34 — FireWood: contacto,latch,switch diferido y vida de efectos

Padre remoto verificado f7f247b8e6ca9db4110424fbb470a5a2bed4a8a9. +4 evidencias PLAYER-057..060,+3 localizadores,+0 documentos. PLAYER-057..060 contrastan FireWood→contacto→lit/timer→switch y efectos→cleanup. Se descarta hipótesis de apagado por switch: relectura no cambia lit. Partículas se retiran por actividad/eventos,no Delete directo; sin efectos runtime ni propagación universal. Sin mod/build/runtime; solo atlas.

## CP-R35 — Consola host fija,rate y ownership UI

Padre remoto verificado 077d6a77036dd41c3f8a2d3870c6f61ff995f4bb. PORT-014..017: startup/atajo→gates→parser→rate→reloj→respuesta→lifetime de mensajes/listeners. Tres símbolos potenciales; nueva ficha systems/port_commands.md. Sin registro dinámico público acreditado; ocultar no revierte estado del reloj. Backend Aurora y ejecución efectiva NOT_VERIFIED. Neto de esta sesión frente a CP-R34:+4 evidencias,+3 símbolos,+1 fichas. Solo atlas,sin build ni runtime.

## CP-R36 — Captura menú,gate de ticks,presentación y cleanup

Padre remoto verificado 502d0592b3cb543e478fdbf0f42576ea58e2a2d5. PRES-082..084 contrastan collect→captura1→gate separado→draw2D→flag3/pause→salida condicionada; PRES-085 inferencia sobre inserción rechazada sin consumidor. Tres símbolos potenciales; ficha cameras_rendering ampliada,sin documento nuevo. Aurora/GPU/alcanzabilidad del bloqueo NOT_VERIFIED. Neto de esta sesión frente a CP-R34:+8 evidencias,+6 símbolos,+1 fichas. Solo atlas,sin build ni runtime.

## CP-R37 — Stock tienda,tag,display y evento024

Padre remoto verificado 4d85697544f5259267fec34a740671be91a4f048. PLAYER-061..064: tag→solicitud display/visibilidad→evento024→índice sold-out→switch RAM→ocultación/retirada y ARC cleanup. Tres símbolos potenciales; other_systems ampliado. No se certifica cobro,entrega,persistencia ni recuperación global de hijo fallido. Neto de esta sesión frente a CP-R34:+12 evidencias,+9 símbolos,+1 fichas. Solo atlas,sin build ni runtime.

## CP-R38 — KYTAG08,referencia ambiental y consumidor MA11

Padre remoto verificado fa820dbe77c0e04aa02c007828d4a28c1a5a8b38. PRES-086..088 contrastan KYTAG08 carga→puntero ambiental único→radio/timer→MA11 matrix y flag jugador→cleanup de efectos; PRES-089 riesgo condicionado de referencia retenida. Tres símbolos potenciales; ficha ambiental ampliada,sin documento nuevo. Assets/backend y orden real de teardown NOT_VERIFIED. Neto de esta sesión frente a CP-R34:+16 evidencias,+12 símbolos,+1 fichas. Solo atlas,sin build ni runtime.

## CP-R39 — McaMorf2,mezcla A/B,morph temporal y callbacks joint

Padre remoto verificado fefe1bbbb9c0a694875a11859c181d53caed6a03. PRES-090..093: Coach caballo→McaMorf2 A/B y morph temporal→joint callback→modelo/draw→cleanup/fallo de heap. Tres símbolos potenciales; ficha modelos ampliada,sin documento nuevo. Peso de mezcla,frame,sound BAS y pose son estados distintos; sin skin/LOD,assets o runtime acreditados. Neto de esta sesión frente a CP-R34:+20 evidencias,+15 símbolos,+1 fichas. Solo atlas,sin build ni runtime.

## CP-R40 — InterpService,ventana,copias y conflicto de claves

Padre remoto verificado 5f20c5cb3a2ef46009de148686730c281160644a. PRES-094..096: InterpService registro→ventana/copias→mapas→sombra/RAII→forget/detach; PRES-097 conflicto condicionado de claves globales. SDK-013 y símbolo servicio aclarados; dos slots oficiales y helper potencial nuevos. No callback nuevo ni prueba de coexistencia; matrices y keys tienen vidas distintas. Neto de esta sesión frente a CP-R34:+24 evidencias,+18 símbolos,+1 fichas. Solo atlas,sin build ni runtime.

## CP-R41 — StartAndGoal,timer global y resultadoRAM

Padre remoto verificado 7cdce813a49f86e140382486f1bc773f5fdbf9d9. PLAYER-065..068: cut→StartAndGoal→creación/inicio Timer→ready/running→meta→MsgTime formatter→DeleteRequest/cleanup. Tres símbolos potenciales; other_systems ampliado. Wrappers no propagan rechazo interno; resultadoRAM no es récord/premio/save; backend y assets no certificados. Neto de esta sesión frente a CP-R34:+28 evidencias,+21 símbolos,+1 fichas. Solo atlas,sin build ni runtime.

## CP-R42 — Diagnóstico disco,worker,cancelación y estado UI

Padre remoto verificado af63c280ce7ed33066c1aa47944d07a533847145. PORT-018..021: selector→inspect/verify wrapper→worker release/acquire→resultado/modal/cancel→config/metadata y flags UI. Tres símbolos potenciales,nueva ficha port_disc_validation.md. Borealis/cancel latency/formato/hash real BLOCKED/NOT_VERIFIED; sin imágenes ni datos personales abiertos. Neto de esta sesión frente a CP-R34:+32 evidencias,+24 símbolos,+2 fichas. Solo atlas,sin build ni runtime.

## CP-R43 — Lifecycle msg,drawtag y heap específico

Padre remoto verificado 098550baa2123de36fb4e93b3bb83f9a070c8591. ROOT-011..013: msg Create→drawtag,gate scenePause,IsDelete/Delete→cleanup específico de Timer/heap/screen. Dos símbolos potenciales; memoria/runtime ampliados,sin documento nuevo. No copiar garantías de actor ni confundir corte visual con destrucción. Fallos parciales/GPU/disposers pendientes. Neto de esta sesión frente a CP-R34:+35 evidencias,+26 símbolos,+2 fichas. Solo atlas,sin build ni runtime.

## CP-R44 — BAS,eventos de sonido,handles y stop/release

Padre remoto verificado 0fbe36a58c222c7d7e495a98a250598080b9df68. PRES-098..101: BAS/frame→filtros/evento→pool/handle→SoundStarter→lifetime/stop/release. Tres símbolos potenciales; ficha audio ampliada. Índice consumido no sonido entregado,release no stop/mixer drain; sin audio ejecutado ni backend/ABI probados. Neto de esta sesión frente a CP-R34:+39 evidencias,+29 símbolos,+2 fichas. Solo atlas,sin build ni runtime.

## CP-R45 — Skinning explícito,buffers y packet consumidor

Padre remoto verificado 7cc9666e608e6a3f46c7ecbaeeb530018b9b6203. PRES-102..105: candado→skin deformer/alloc parcial→pose/vértices→packet arrays→heap/ARCcleanup. Tres símbolos potenciales; ficha modelos ampliada. Instalación no atómica y ruta fast compartida condicionada; sin asset/formato/LOD universal ni render Windows. Neto de esta sesión frente a CP-R34:+43 evidencias,+32 símbolos,+2 fichas. Solo atlas,sin build ni runtime.

## CP-R46 — WebSocket polling,views y cierre diferido

Padre remoto verificado 328ca089c7efb02c07d5ffb91b624d2137393c39. CALLBACK-028..031: WebSocket connect→poll/OPEN→payload prestado→close/CLOSED→take_all. Pista frameBegin corregida: no callback de mod. Dos slots oficiales y helperSDK potencial nuevos; ficha ownership ampliada. Backend/drain/ACK/runtime NOT_VERIFIED,sin red; SDK-024 conserva evidencia previa. Neto de esta sesión frente a CP-R34:+47 evidencias,+35 símbolos,+2 fichas. Solo atlas,sin build ni runtime.

## CP-R47 — PARCIAL lifetime KANKYO,global y gates de cleanup

Padre remoto verificado fa64df683686e0c15cb84fec7042b7d1d887b2b7. PRES-106/107: stage→proceso KANKYO→global compartido→gates execute/draw→cleanup seleccionado. Dos símbolos potenciales; limitación PRES-089 ampliada con trazabilidad. Checkpoint PARCIAL respecto a orden room unload; no UAF ni cleanup global garantizados,fuente disponible sin runtime. Neto de esta sesión frente a CP-R34:+49 evidencias,+37 símbolos,+2 fichas. Solo atlas,sin build ni runtime.

## CP-R48 — Flecha tipo0,At/joint,adhesión y borrado diferido

Padre remoto verificado 705264cd6bc3d142c4fde327e2fe5b9e2f9be861. PLAYER-069..072 (+4 STATIC_CROSSCHECKED),tres localizadores internos;0 fichas nuevas. Cadena seleccionada Link→flecha→colisión→adhesión joint→flag→solicitud/delete específico;HP y todas las variantes excluidos. Sin mod,build ni runtime; solo atlas.

## CP-R49 — PARCIAL retiro room8/20,solicitud y conservación BG

Padre remoto verificado 60a6e417b81fe181573c626788b1826c15099585. WORLD-041/042 (+2 STATIC_CROSSCHECKED),dos localizadores;0 fichas. Nueva fuente real de solicitudes de retiro de room y filtros;PRES-089 recibe limitación trazable,sigue STATIC_INFERRED sin UAF ni cierre de orden. Sin mod,build ni runtime; solo atlas.

## CP-R50 — BTP,binding por slot,texNo y fallo de protocolo condicionado

Padre remoto verificado ff402f2451a2ca2291c6199db5c7906a5f631242. PRES-108..111:3 STATIC_CROSSCHECKED y1 STATIC_INFERRED,tres localizadores;0 fichas. Wflag→BTP→material descriptor→texNo→remove/ARC;error5 convertido a bool documentado con condiciones,sin fallo runtime. Sin mod,build ni runtime; solo atlas.

## CP-R51 — UiService BUTTON,guard pane y rebuild/detach

Padre remoto verificado 7edf053ae53ae45272d06285aa49ecd82a1711a2. CALLBACK-032..034 (+3 STATIC_CROSSCHECKED),un slot OFFICIAL_SERVICE ya existente y un helper potencial;0 fichas nuevas. Se descartó pistaInputService inexistente;se contrastó BUTTON→Confirm→guard de registro→callback→detach,sin UI ni runtime. Sin mod,build ni runtime; solo atlas.

## CP-R52 — Flecha enemiga,escudo madera,lista16 y reset

Padre remoto verificado c1cf24d56a4695b22695f2f9c483dddd1c8bf623. PLAYER-073..076 (+4 STATIC_CROSSCHECKED),tres localizadores;0 fichas. E_RD→E_ARROW→escudo→listaLink16→contador/itemsolicitado→reset→delete específico,distinto de joint de flecha jugador. Entrega/persistencia,resto de variantes y runtime no demostrados. Sin mod,build ni runtime; solo atlas.

## CP-R53 — GameMode,selección PENDING,consumidor y fallback

Padre remoto verificado 67d2e834790a8ec885a811159ac8c8ab96d80d9f. CALLBACK-035/036,PORT-022 (+3 STATIC_CROSSCHECKED),tres localizadores;0 fichas. CallbackOK→estado prestadoPENDING/PROCEED/RETURN→file-select inputnombre;modoactivo retirado solicita reset y fallbackvanilla,sin guardado ni rollback universal. Sin mod,build ni runtime; solo atlas.

## CP-R54 — KYTAG02,viento global,suavizado y consumidor Kita

Padre remoto verificado b63fc59d03aca7a8821277073d1cbd68e005286b. PRES-112..114 (+3 STATIC_CROSSCHECKED),dos localizadores;0 fichas. Switchhome→ciclo/override→wind_set→poses/sonidoKita→Delete parcial,sin transferencia de ownershipactor ni efecto audiovisual observado. Sin mod,build ni runtime; solo atlas.

## CP-R55 — Partícula trace,userWork y retiro por renovación

Padre remoto verificado d26a3cf70c34f8be9d75ce108ae52e430cbeed53. PRES-115..118:3 STATIC_CROSSCHECKED y1 STATIC_INFERRED,dos localizadores;0 fichas. E_ARROWvector→emisor→JPAtrace→levelcleanup;vida del callbackglobal≠vida del Vecactor. Ordenfree/calc pendiente,sin UAFobservado. Sin mod,build ni runtime; solo atlas.

## CP-R56 — Direct-save logo,statusCARD,fallbackRAM y consumo ff

Padre remoto verificado 0868e14d4acb7ae15097cec0d95ee05f10da6c13. ARCH-017..020:3 STATIC_CROSSCHECKED y1 STATIC_INFERRED,doslocalizadoresmás ampliación del existente nextSceneChange;0 fichas. SolicitudCLI→LoadSync→RAMsave/init→requestPLAY/ff,log≠éxito,noIOreal. Sin mod,build ni runtime; solo atlas.

## CP-R57 — Gate latched,Mtx** y wrapperMoveBG

Padre remoto verificado 5985d5510dc665e1a6a70bb150a7a6ce70d0ec7a. PLAYER-077..080 (+4 STATIC_CROSSCHECKED),treslocalizadores;0 fichas. LV4Gate switch→END→matrizmodelo→BG/correccióngateada→retirada;ret0 no es abortowrapper yswitchnoinviertepose. Sin mod,build ni runtime; solo atlas.

## CP-R58 — Texturefrontend,prioridad,reregistro y keepalive

Padre remoto verificado 88705aceed5c22ae1b9c2c781bd86d3b985eb997. PRES-119..122:3 STATIC_CROSSCHECKED y1 STATIC_INFERRED,dos slotsSDKexistentes+unlocalizador;0 fichas. Ownershipraw→backendregistro→lifecycleprioridad/reregistro→unregister;selector/finlecturasAurora BLOCKEDlocal,sinGPU/runtime. Sin mod,build ni runtime; solo atlas.

## CP-R59 — Reactivación,loteLifecycle,operaciónUI y toast

Padre remoto verificado d66d64221337f7abc8b202a677f7c1a4360260fc. PORT-023..025 (+3 STATIC_CROSSCHECKED),doslocalizadores;0 fichas. Nueva pregunta arbitrajesolicitudesporID→estadooperación→UIfrente aaviso históricofallo;no se repite teardownbase ni red/instalación. Sin mod,build ni runtime; solo atlas.

## CP-R60 — ObjCarry,boomerang,offset corregido y transferencia Link

Padre remoto verificado 83ac62f838bd2dbc2fb549996370e9f5e3e6d07b. PLAYER-081..084 (+4 STATIC_CROSSCHECKED),treslocalizadores;0 fichas. AtBoom→TgCarry→offset/relookup→Acch→Linkgrab/wait;fintransporte≠delete/entregainventario ycheckhelpermutante. Sin mod,build ni runtime; solo atlas.

## CP-R61 — Disposers,destructorvirtual y reset de solid heap

Padre remoto verificado 3f7e19320ebfb3e77393213341ab47e01c276127. ROOT-014..016 (+3 STATIC_CROSSCHECKED),doslocalizadores;0 fichas. Registro por dirección→lista→destructorvirtual→solidfreeAll/freeTail/heapchild;disposeboolfalse fijo no significa ausencia deefectos. Sin mod,build ni runtime; solo atlas.

## CP-R62 — Precisión de gate RotY y trazabilidad de destroy

Padre remoto verificado 591d7faf724085a360afa4c41dda25748dbdecff. Rectificación explícita PLAYER-079: RotY requiere shapeAngle noNULL para sumar yaw también a angle. ROOT-016 añade puente JKRDestroySolidHeap. +0 evidencias,+0 símbolos,+0 fichas; no se cuenta como otra cadena completa del motor. CP-R48..61 contienen14 bloques técnicos,CP-R62 es revisión editorial con fuente adicional. Sin mod,build ni runtime; solo atlas.

## CP-R63 — TagWaterFall: región de cámara y maestro persistente — PARCIAL

Padre remoto verificado f5e707e1cc52483b9ac9add841d49ef2fd9ba398. PRES-123..125 contrastan create/perfil→camera/AllJudge→blend/custom_colset→KANKYO y fog condicionado;PRES-126 inferencia de reelección al conservar estáticos. Tres localizadores internos nuevos,no hooks acreditados. PARTIAL en recarga/orden/ID;sin cambio de niveles canónicos. Sin mod,build ni runtime; solo atlas.

## CP-R64 — Ice_s: apoyo continuo y matriz de plataforma

Padre remoto verificado a8cc59cdeab98b6b74618589e483df61fc34876f. PLAYER-085..087 STATIC_CROSSCHECKED:V_Ice_s/ridecallback→latch/inclinación/hundimiento→modelo/BG y retirada. PLAYER-088 STATIC_INFERRED:precedencia ! y fVar1 condicionado. CERRADO SELECTIVO para cadena de apoyo;no rotura/assets/runtime demostrados. Sin mod,build ni runtime; solo atlas.

## CP-R65 — LogService: copias, retención y consumidor diagnóstico

Padre remoto verificado 815a418fbce69d1425716165df0fe4ee80f9c401. PORT-026..028 STATIC_CROSSCHECKED extienden SDK-015:write copia→ring2048/seq→LogsWindow y clear lógico;backendfile/durabilidad NOT_VERIFIED. Un slot oficial exacto y dos localizadores internos nuevos;CERRADO SELECTIVO frontend,ninguna API de lectura pública añadida. Sin mod,build ni runtime; solo atlas.

## CP-R66 — BRK: registros de color TEV y lifetime del recurso

Padre remoto verificado 5bd69e12b052cdaa51e165ea1b48f2bdf45e5c00. PRES-127..130 STATIC_CROSSCHECKED trazan BRK/TevRegKey→enlace nombres/slots→lectura CReg/KReg y cleanup explícito/ausente;Obj_Bef consumidor fuente sin colocación/runtime acreditados. Tres localizadores internos. CERRADO SELECTIVO;sharing,assets y cleanup parcial siguen abiertos. Sin mod,build ni runtime; solo atlas.

## CP-R67 — FileService list: llamadas síncronas y lifetime del sentinel

Padre remoto verificado e4b1da9d4533ceb1bcc0553172f028ec7b2dca78. CALLBACK-037/038 STATIC_CROSSCHECKED y039 STATIC_INFERRED:ListResult→entradasprestadas→callback/checkactive→sentinel→copiasSDK y erroresparciales. Un slotoficial,dos localizadores/consumidores fuente. CERRADO SELECTIVO;backend/listorden/unloadWindows pendientes. Sin mod,build ni runtime; solo atlas.
