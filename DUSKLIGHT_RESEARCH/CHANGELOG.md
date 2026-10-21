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
