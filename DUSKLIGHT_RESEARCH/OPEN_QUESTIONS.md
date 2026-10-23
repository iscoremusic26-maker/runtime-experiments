# Preguntas abiertas y siguiente comprobación mínima

Todas se refieren al SHA fijado. Se evita repetir lo ya respondido; cada pregunta tiene una acción limitada. El atlas sigue siendo estático y la existencia de una pregunta no autoriza implementar ni compilar un mod.

| ID / estado | Qué falta y por qué importa | Próximo paso mínimo |
| --- | --- | --- |
| Q-01 · PARCIAL | Item,Message,Config,Window y Http contrastados en CALLBACK-005..027; otros dispatchers pendientes | Elegir otro dispatcher con hueco concreto; no repetir Save/Host/Camera/Item/Message ni inferir barrera universal. |
| Q-02 · PARCIAL | Item exige side-effect-free; Message copia sin revalidar handle/active y conserva texto separado de callback; Config copia callbacks sin revalidar token, suprime notify del mismo nombre pero aplica escritura (CALLBACK-014..018); Window usa callback dirigido y event local, consume aun sin invocarlo (CALLBACK-019..022); Http revalida handles y usa completing/snapshot prestado;cancel conserva slot y take_all no prueba worker drenado (CALLBACK-023..027); sin garantía general de reentrancia | Contrastar encabezado y bucle concreto de un servicio; documentar límites de colección y vigencia. |
| Q-03 · PARCIAL | CP-R18 PLAYER-040..045 distingue request-only, actor publicado, forceDelete y fallo reentrante; unregister no drena create queue | Falta probar reutilización de nombre, reentrada y vida de callbacks/biblioteca Windows; revisar ownership de append en fallo temprano solo si otra cadena lo exige. No repetir barrido básico. |
| Q-04 · NOT_VERIFIED | Símbolos exportados/resolubles y layouts en imagen Windows x64 concreta | Consultar evidencia histórica exacta o manifest/import library ya disponible sin recompilar; si no existe, mantener límite binario. |
| Q-05 · BLOCKED local | Aurora/Borealis internos, incluidos DX12, DVD/CARD y garantías externas de unregister | Consultar solo archivo necesario al SHA del gitlink si hay acceso; no instalar ni auditar todo el tercero antes de avanzar en fuente principal. |
| Q-06 · PARCIAL | Retry por save-written/copy/erase y vida de dirty/caché contrastados en WORLD-034..037; backend,crash consistency y migración completos pendientes | Revisar atomic_replace exacto de Borealis si disponible; si falta,conservar bloqueo local y no inventar ACK/garantía de reinicio. |
| Q-07 · PARCIAL | WORLD-038..040 contrastan stride tipado frente a tramo CRC, BE/copia y adiciones. sizeof/offsetof/packing Windows sigue NOT_VERIFIED | Consultar solo manifest/layout histórico exacto ya disponible si aparece; sin build. No repetir fórmula del caller ni usar assert GC como medida. |
| Q-08 · PARCIAL | Cadena BST lifecycle/mapa/consumidor y retiro contrastada en PRES-052..055; edición tras init puede diferirse sin lifecycleApplied posterior | Mantener diferencia estática y runtime; faltan fin de reproducción,adiciones/allocators y backend Windows. No repetir búsqueda frameEnd ni modificar host. |
| Q-09 · PARCIAL | File-select→PLAY contrastado en ARCH-002..007; logo stage-request y fallos overlap/destino contrastados en ARCH-008..011; reset PLAY→OPENING/gates/SaveSync/retarget contrastados en ARCH-012..016; captura menú→gate separado→draw/pause→cleanup contrastada PRES-082..084 y rechazo condicionado PRES-085; quedan load-save directo,recuperación global y otras rutas captura/presentación | Elegir otro consumidor de direct-load o gate captura; no repetir reset/opening,nominal ni fallos overlap ya acotados; no prometer rollback. |
| Q-10 · READ parcial | Fuentes y cadena AutoMata morf/BCK/BTK contrastadas (PRES-036..039,044..047); TextBoxEx loader/material/buffer/cleanup contrastado en PRES-056..059 con tags de asset condicionados; BMG por idioma/grupo→Explain/cleanup contrastado en PRES-068..073; Sakuita/simple-model registro/listas/cleanup contrastado en PRES-078..081; quedan formatos/LOD/skin,otros morf,refresh/charsets y lifetime por archive | Elegir una ruta transversal de adquisición→uso→liberación; conservar resto como muestreo. |
| Q-11 · READ parcial | Avance normal/KYTAG11 y salida save/audio contrastados (PRES-040..043); KYTAG06 tipo11→paletas/fog/partículas contrastado (PRES-048..051); agua Obj_Lv3WaterB/consulta Acch→Link contrastada en PRES-060..064 con geometría condicionada; KYTAG07 influencia puntual/selección/retiro contrastado en PRES-074..077; KYTAG08→radio/material MA11/flag jugador/cleanup contrastado PRES-086..088,retención condicionada PRES-089; saturación/índice de fallo,otros escritores y orden/lifetime global pendientes | Seguir un controlador y consumidores de sus datos; no diseñar un mod climático. |
| Q-12 · READ parcial | Swpush contrastado (PLAYER-035..039); MYNA2 tipo1/evento/cleanup y comparación de variantes contrastados (PLAYER-046..051), con assets de cuts/flow sin verificar; B_DS fase2 daño→demo→progreso/cleanup contrastado en PLAYER-052..056; FireWood contacto/latch/switch diferido/partículas contrastado en PLAYER-057..060 (sin apagado por switch); stock tienda/tag→display→evento024→flag/visibilidad/cleanup contrastado PLAYER-061..064,sin cobro/entrega/durabilidad completa; resto de NPC,bosses,puzzles,pesca/minijuegos conserva profundidad selectiva | Alternar familias y mecanismos comunes; la ficha other_systems localiza rutas, no estudia exhaustivamente cada actor. |
| Q-13 · READ parcial | Logros y cadena speedrun/LiveSplit contrastados en PORT-001..009; presencia host gated→mainloop→shutdown contrastada en PORT-010..013; consola host→rate→respuesta/cleanup contrastada PORT-014..017; diagnóstico disco metadata/worker/modal/cancel/config contrastado PORT-018..021; backend/ACK/timeouts/reset,otros diagnostics y configuración completa pendientes | Alternar familia; backend Borealis puntual si disponible o presence/diagnostics. No conectar LiveSplit ni tratar contador UI/tick como tiempo real medido. |
| Q-14 · PARCIAL | Prioridad overlay del contrato/orden emitido y consumidor JKRMemArchive→cache dRes contrastados (PRES-065..067); retirar ganador no actualiza mRes vivo | Faltan selector Aurora exacto y coexistencia Windows; elegir política de otro mecanismo solo con hueco nuevo, sin repetir orden SDK-018. |

Bloqueos que no impiden continuar: submódulos ausentes y falta de runtime Windows. Git/gh no fueron la vía operativa; el conector GitHub permite continuar documentación con HEAD comprobado y lease. No hay tarea programada ni promesa de trabajo desatendido.

CP-R39 Q-10: PRES-090..093 contrastan McaMorf2/Coach A-B frente a morph temporal,callback joint/sonido/cleanup. No implica skin/LOD ni compatibilidad universal; faltan árbol asset,sharing y disposers ante fallo. Mantener pregunta parcial.

CP-R40 Q-14/ownership: PRES-094..097 aclaran InterpService,ventana,copia3x4,lookup/fallback y conflicto de keys globales; SDK-013 precisado. No contiene callbacks de mod: Q-01/Q-02 no se cierran por esta API. Falta coexistencia real,otros arbitrajes y runtime.

CP-R41 Q-12: PLAYER-065..068 contrastan StartAndGoal/Timer,caller cut,ready/running,wrappers que no propagan rechazo,meta→MsgTime y cleanup diferido. No carrera integral,récord,recompensa ni persistencia; resto de temporizadores sigue pendiente.

CP-R43 Q-05/lifecycle: ROOT-011..013 contrastan wrapper msg y heap/screen Timer explícitos,comparado con fopAc_Delete previo. No resuelve disposers globales,alloc fallidos ni actor unregister; msg no hereda cleanup ActorService. Siguiente familia distinta.

CP-R44 Q-08: PRES-098..101 contrastan BAS→frame/evento→handle→SoundStarter→stop/release/pool. No reproducción audible ni cambio BST nuevo; persisten mixer/backend,assets,seek y duración de userdata tras otras rutas.

CP-R45 Q-10: PRES-102..105 contrastan skin explícito del candado,buffers/flags parciales,deform y packet consumidor. Falta asset real/fastpath completo,fallos de alloc/disposers,sharing y DX12; no promoción global de skin/LOD.

CP-R46 Q-02/ownership: CALLBACK-028..031 extienden SDK-024 con polling WebSocket,views permod,OPEN publicado antes de send,close/CLOSED y retiro. No frameBegin/callbackdeusuario: pista anterior corregida,backend/drain/ACK pendientes,sin tráfico real.

CP-R47 PARCIAL Q-11/PRES-089: PRES-106/107 separan KANKYO proceso de g_env_light global y gates/cleanup; sigue sin resolver secuencia room unload KYTAG08→MA11. Consultar room remove/consumidor real antes de elevar hipótesis; no UAF observado.

CP-R48 Q-12: PLAYER-069..072 contrastan flecha tipo0→At/joint→adhesión→flag/borrado; no certifican HP,objetivo asset ni proyectiles enemigos/agua/materiales/resto de variantes. Alternar Q-11 antes de otro proyectil.

CP-R49 PARCIAL Q-11/PRES-089: WORLD-041/042 localizan retiro8 y20,BG excluido en parcial y gates de NODRAW. Siguiente consulta ambiental mínima: consumidor que fija20 para una sala concreta y su condición NODRAW de KYTAG08;requiere colocación/assets si se afirma alcanzabilidad. No repetir loadRoom ni KANKYOinit. Alternar otro dominio.

CP-R50 Q-10: PRES-108..111 contrastan BTP/texNo,Wflag y retiro por slot;discordancia error5→bool es inferencia condicionada. Faltan assets/sharing/ownership completo,LOD y runtime;no repetir wrapper/descriptor. Alternar servicio u otro dominio.

CP-R51 Q-01/Q-02: CALLBACK-032..034 contrastan BUTTON UiService2.3,guard de pane y generación/rebuild/detach;InputService no se deduce de ruta inexistente. Reentrancia,otros tipos UI y bibliotecaWindows siguen pendientes;alternar gameplay.

CP-R52 Q-12: PLAYER-073..076 contrastan flecha enemiga normal→escudo madera→lista16→recuperaciónRAM/reset/delete. No reusar parámetros de daArrow ni afirmar daño/recompensa duradera;FIRE/BOMB,SPIN y resetglobal completos pendientes. Alternar Q-13.

CP-R53 Q-01/Q-02/Q-13: CALLBACK-035/036,PORT-022 contrastan GameMode selecciónPENDING→consumer/nameinput y fallback/retirada. Quedan reentrada/cambio de modo durante selección,otros callbacks y resetfinal;no repetir scheduler o guardado. Alternar ambiente independiente.

CP-R54 Q-11: PRES-112..114 contrastan KYTAG02/vientoefectivo/Kita y cleanup parcial;no slotpuntual ni drenajeaudio. Faltan vec_overrideownership,otrosescritores/capas/ordenreal;PRES-089 continúa abierto. Alternar audio/recursos.

CP-R55 Q-08/lifetime: PRES-115..118 contrastan traceuserWork y retirolevel,errorcapacidad128. Primera consulta de cierre del riesgo:caller calc3D frente a deletequeue/actorheapfree y guardsJPA;no inferir UAF de ausencia de NULLcheck. Alternar escenas.

CP-R56 Q-09: ARCH-017..020 contrastan direct-save1..3/status/fallbackRAM y consumoff aun sin revisarChangeReq;espera0sin timeout es riesgo condicionado,no hangobservado. BackendCARD/progresoyrecuperaciónglobalpendientes;no repetirlogo. Alternar gameplay distinto deproyectiles.

CP-R57 Q-12: PLAYER-077..080 contrastan LV4Gate latched y wrapperMoveBG/corrección/cleanup. No todoscontactos/actores ni retorno0comorollback;assets/fallosparciales/reentranciayruntimependientes. Alternar recursos.

CP-R58 Q-14/Q-10: PRES-119..122 contrastan Texturefrontend handle/priority/reregistro/keepalive. Falta selectorAurora yfinlecturasreal;no instalar/descargarsubmódulo. BackendID0trasreregistro esriesgocondicionado,nofalloobservado. Alternar port/memoria.

CP-R59 Q-13/Q-14: PORT-023..025 contrastan coalescingLifecycleporID/operaciones ytoastconsumido,distinto de teardownHOOK019. Faltan otrascolas,intercalaciónconcallbacks yruntime;no repetir loadergeneral. Alternar interacción de actores/colisiónsicontextopermite.

CP-R60 Q-12: PLAYER-081..084 contrastan ObjCarryadmitido→boomerang→offset/colisión→Linkgrab/wait yDeleteseparado. Faltanroturainicial/otrosobjetos/eventKeepglobal/lifetimeKeepbajoborrado;no repetirItemService. Alternar memoria/recursos o conservardetalle exactoparacontinuar.

CP-R61 Q-05/memoria: ROOT-014..016 contrastan Disposer ySolidfreeAll/freeTail/destructorheapchild,con disposefalsefijo. No resuelve fallbackporclase,derivedcleanupconcreto ni concurrencia/unloadWindows. Alternar familia;no rehacerTLSoheaps.

CP-R62 precisa PLAYER-079: yaw de angle depende también de shapeAngle noNULL. ROOT-016 gana cita del puente destroy. Sin IDs nuevos; siguen abiertos PRES-089,111,118,122 y ARCH-020 en sus condiciones. Próxima cadena nueva: tag_waterfall, no otra revisión del mismo MoveBG.

CP-R63 PARCIAL Q-11: PRES-123..126 separan flag maestro/ID,región de cámara y gather/fog de TagWaterFall. Falta demostrar una retirada→reentrada concreta con conservación o reinicio de estáticos e identidad. Consultar ruta de carga del perfil/unidad antes de afirmar reelección o bloqueo;no repetir geometría ni PRES-089. Alternar otra familia.

CP-R64 Q-12: PLAYER-085..087 contrastan Ice_s apoyo→latch/pose→MoveBG/modelo→cleanup;no rotura. PLAYER-088 recoge precedencia ! y lectura fVar1 condicionada;alcanzabilidad/assets/runtime pendientes. No otra variante MoveBG inmediata:alternar soporte/servicio.

CP-R65 Q-13: PORT-026..028 extienden SDK-015 con ring2048→copy_since→LogsWindow/clear lógico. No callback de mod ni dispatcher nuevo;Q-01/Q-02 no se cierran. Sink Borealis,flush/errores y límites efectivos pendientes;no leer logs personales ni abrir backend ausente. Alternar modelos/recursos.

CP-R66 Q-10: PRES-127..130 contrastan BRK→TevRegKey/materialIDs→slotsCReg/KReg→calc/retirada con Obj_Bef como consumidorfuente. Assets/colocación,sharing y cleanup parcial siguen pendientes;init1 no confirma entry,wrappervoid oculta ret2/1. Alternar dominio;no repetir BTP/BRK para sumar variantes.

CP-R67 Q-01/Q-02: CALLBACK-037..039 amplían SDK-005 con list síncrono→entry prestado→checkactive→sentinel y consumidor C++copiado. No cancelhandle;sentinel puede omitirse por error y terminal no revalidaactive. Faltan backend/orden/lifetimeWindows;no repetir picker/stream como si ya se hubieran auditado. Alternar ambiente uotra familia.

CP-R68 Q-09/Q-12: ARCH-021..024 contrastan KYTAG04tipo4 switch→ordenencolada→timer/Linkgate→SCLS→PLAY y cleanup. No es weatherQ-11 pese a nombre. Assets WITHWARP_OPEN/SCLS,colocación y orden de eventualrollbackglobal pendientes;ARCH-023 es inferencia sin softlock observado. Alternar otrafamilia.

CP-R69 Q-10: PRES-131..134 contrastan Demo00→BLS/BLK→pesos→arrays→calc y retirada. BVA3D no tuvo consumidor actor en búsqueda acotada;no se concluye imposibilidad. Assets,sharing,referenciasJStudio y ruta missingBLK(PRES-134) pendientes. Alternar gameplay.

CP-R70 Q-12: PLAYER-089..092 contrastan Digpl tipo0/LinkWolfDig→señal→switchRAM→requestitem/delete;entrega y durabilidad pendientes. Precisión de PRES-127/131 y ARCH-024:guard init==0 no es fallo0 observado ni ruta normal demostrada. Alternar Q-11 en siguiente bloque.

CP-R71 PARCIAL Q-11/Q-08: PRES-135..139 contrastan KYTAG03 rail→pool/estados/draw/audio y separan emisor/handshakeLink. Falta secuencia room/path unload,assets cardinalidad/ciclos y adquisición completa de olor. No reset de pool enDelete no pruebaUAF;hay ownerweather y escritorKYTAG10. Alternar servicios.

CP-R72 Q-01/Q-02/Q-14: CALLBACK-040..042 precisan picker global,sharedpending,revalidación y detach distinto de list. Backendbusy/hilo/dialogcancel/drain y helperfunción pendiente tras supresión siguen pendientes;sin selector real ni datos personales. Alternar gameplay.

CP-R73 Q-12: PLAYER-093..095 contrastan Lv4DigSand start/endLink→GroundCross→timer/llegada→switch/Delete. Faltan interrupciones/placement y fallbackrelease sin suelo(P095inferido);no repetir DigPlace ni generalizar MoveBG. Alternar gráficos/servicios.

CP-R74 Q-10/Q-13: PRES-140..142 contrastan Gfxdraw→excepciónC++→colafallos→frameBegin/detach/fail_mod. Faltan backenddrain,ordenreload porID y efectosGPU;no repetir retirementbásico PRES-012. Alternar ambiente/gameplay.

CP-R75 Q-11/Q-12: PLAYER-096..098 contrastan OnsenBG→timerLink→deltaLife→MeterRAM/cleanup. Assetsagua,otrosproductores y orden durante unload pendientes;no curaciónvisible o saveobservado. Alternar servicio/port.

CP-R76 Q-01/Q-02/Q-13: CALLBACK-043..046 precisan TCPpoll/backpressure/close y wrapper;CALLBACK-045 endpointviewrawlocal esinferenciacondicionada. BackendACK/drain/userdatasampling sinfuente;no redreal. Alternar otra familia.

CP-R77 Q-05/Q-08/Q-10: PRES-143..146 contrastan mountDVD→lectura en bloque→JAISeq/reciclaje. PRES-146 enqueue fallido sin rollback local es inferencia condicionada. Pendiente teardown global archive/lecturas y backend DVD; no repetir cache MemArchive CP25.

CP-R78 Q-12: PLAYER-099..102 cierran muestra Rollgoal Fshop/controlador→bola→Hena→progreso/reentrada. Pesca/alquiler, teardown abrupto, fallos de hijos y assets siguen pendientes; no duplicar stock CP37 ni timer CP66.

CP-R79 Q-13: PORT-029..031 añaden diagnóstico stub→buffer temporal→ImGui/PostDraw. Backend que invoca divert y su interpretación de true siguen BLOCKED; otros logger/LogService ya cubiertos no repetir. Sin logs/UI reales.

CP-R80 Q-11: PRES-147..150 contrastan KYTAG13→subrango→packet nieve→draw/cleanup. PRES-150 rango especial sin clamp final es inferencia condicionada,assets no consultados. Orden multitag/interp/ground/salida de room siguen parciales. KYTAG05 no era ruta ambiental.

CP-R81 Q-09: ARCH-025..028 añaden KYTAG05/PEEP_HOLE→Link→mode6/7→TurnRestart/cámara. RechazoSCLS tras latch es inferencia condicionada;assets/eventcuts y recuperación global pendientes. No repetir helper/cola nominal ya auditados.

CP-R82 Q-01/Q-02/Q-14: CALLBACK-047..049 precisan contextmenu dismiss→retirarhandle→revalidarancla/active→acción→destrucción diferida. Reentrancia durantefocus/callback,DLL y backendRml siguen NOT_VERIFIED. No repetir controles/button ni documentos generales.

CP-R83 Q-10: PRES-151..153 contrastan Midna/invisibleModel→arraypacket→Zsort→paseprofundidad yreset. Modelo prestado distinto de posiciónstack consumida;GPUdrain/ordenheap/otrasramas siguen pendientes. No repetir skin/BTP/BRK.

CP-R84 Q-12: PLAYER-103..106 añaden SekizoaTYPE0/1→eventJUMP/GOAL→SekiDoor→SW2/recarga. Assets/cutprms yparejas siguenpendientes. PLAYER-106 condiciónfunciónsinllamada esinferenciaconfuente,no falloobservado. No atribuirCopyRod ni repetirRollgoal.

CP-R85 Q-01/Q-02: CALLBACK-050..052 contrastan Flow register_query→PROBE/EXECUTE→arista y retiro. No asumir pureza, exactly-once, owner.active gate o drenaje; graph mutation/reentrada/DLL permanecen NOT_VERIFIED. Alternar Q-11; no repetir Message resolver.

CP-R86 Q-11: PRES-154..156 contrastan KYTAG01 variante0 dos switches→fade→fog/gather→consumo→delete/no-op. Campo59c2 sin productor local, variantes2/otros tags,composición de stage y último escritor quedan pendientes. No afirmar niebla residual observada ni reauditar fog de TagWaterFall. Alternar modelos/formatos.

CP-R87 Q-10: PRES-157..159 contrastan Title/BPK→MatColor0 y retiro, distinto de TEV/BRK. BVA tiene loader localizado sin consumidor cerrado;no crear evidencia de compatibilidad. Quedan assets,sharing,parser/fallos parciales y GPUdrain;no repetir BLS/BLK. Alternar gameplay.

CP-R88 Q-12: PLAYER-107..109 contrastan Bombf/NBOMB fastCreate→crecimiento/carry→lookup ausente→reposicion150. Recolección no inicia por sí sola reposición;Delete padre no borra hijo. Unload/room,otros estados de bombas y callbacks de daño completos pendientes. Alternar servicio/soporte;no reauditar scheduler.

CP-R89 Q-02/ownership/Q-13: SDK-026..028 precisan streams owned→read count/status→close consumehandle→detach y wrapper RAII. No callback nuevo:Q-01 sigue parcial. Backend,cursor/EOF/durabilidad y teardown completo NOT_VERIFIED;no datos personales ni I/O del juego. Alternar stage/restart.

CP-R90 Q-09/stages: WORLD-043..045 contrastan Tag_ChgRestart→RAM/latch→Link restart→playerInit(-1);WORLD-046 inferencia condicionada de ID PLAYER ausente tras assert. Quedan composición,scopes/durabilidad,Tag_SetRestart y recuperación de toda cola;no repetir reset/opening. Alternar arbitraje del SDK.

CP-R91 Q-14: WORLD-047..049 contrastan arbitraje Flow patch por posiciónmod/commitsequence y retiro para lookup futuro;WORLD-050 inferencia condicionada de nodo copiado y arista retirada durante callback. Faltan combinaciones reales,recursos/idiomas y reentrada/DLL;no prometer rollback jugable o coexistencia Windows. Alternar diagnóstico/configuración interna.

CP-R92 Q-13/controles: PORT-032..034 amplían PLAYER-004 con UIcaptura→CVar→polling/trigger→cámara y cancel/save. Escape desasigna;cancel solo referencias;savevoid sin ACK. Quedan reconexión,captura/visibilidad,reentrada y backend PADSerializeMappings;sin configuración/dispositivos personales. Alternar gameplay pesca.

CP-R93 Q-12: PLAYER-110..112 amplían PLAYER-031 con pesca LURE ordinaria hookset→CATCH→flow/registro→health keep-release→cleanup. No cubre UKI,premios,alquiler,fishKind4/5,assets ni durabilidad. Compañeros vivos son precondición en catch;sin crash/runtime. Alternar ambiente/controlador nuevo.

CP-R94 Q-10: KYTAG09 film gráfico→selección por DarkClearLV→Draw BTK/BG→resDelete, PRES-160/161 CERRADO_SELECTIVO. La pista Q-11 de CP-R93 se reclasifica;no había evidencia ambiental que borrar. Próximo bloque:auditoría de brechas V1 de seis áreas READ,priorizada por impacto;no otro actor arbitrario.

CP-R95 prioriza cierre documental en V1_READINESS:V1-C01 auditoría semántica de alto riesgo,V1-C02 guía de consulta/propiedad y V1-C03 consistencia/publicación final. No se cierran Q-01..14 ni se exige resolver todos los READ. La investigación técnica nueva se justifica por impacto, no por actor o contador.
