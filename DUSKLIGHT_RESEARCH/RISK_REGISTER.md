# Riesgos transversales y rollback

Riesgos derivados del commit fijado. No son fallos observados durante ejecución; se distingue contrato, fuente e inferencia en el [ledger](EVIDENCE_LEDGER.json). La mitigación es una condición para estudiar una futura integración .dusk, sin implementar un mod en esta campaña.

| ID | Riesgo y disparador | Evidencia | Mitigación / límite del rollback |
| --- | --- | --- | --- |
| R-01 | Usar offsets/tamaño GameCube o un STATIC_ASSERT histórico como ABI Windows | PLAYER-009 y HOOK-001/027; WORLD-033 | Verificar tipos/época/target exactos. No asumir padding, PMF ni vtables por comentarios. |
| R-02 | Init parcial cambia estado y devuelve error esperando shutdown | HOOK-016 | Revertir pasos propios antes de devolver fallo; shutdown solo corre si initialized quedó true. |
| R-03 | Replace takeover destruye el ganador previo; uninstall no lo restaura | HOOK-005/007 | Política de conflicto explícita; no prometer pila ni rollback al replace anterior. |
| R-04 | Actor propio no termina destrucción y mantiene callbacks mientras se retira DLL | SDK-001, HOOK-029 | Demostrar fin de instancias/callbacks; cleanup que registra un fallo no es barrera. No certificada estrategia universal de hot unload. |
| R-05 | Retirar observer libera userdata que un snapshot aún conserva | CALLBACK-001..004 y CALLBACK-007 | Separar retirada, fin de dispatch y liberación; no extrapolar cancelación Host/Camera a Save. |
| R-06 | Guardado vanilla confirmado pero sidecar falla o queda dirty | WORLD-011/012 | Datos propios versionados e idempotentes; tratar los errores de cada archivo, sin prometer transacción CARD+mods. |
| R-07 | Cambio de room/layer/escena invalida puntero de actor/path/model/archive | WORLD-003, PLAYER-025, PRES-004/006 | Revalidar identidad y contexto; limpiar caches; ownership del heap/archive define vigencia. |
| R-08 | Overlay retirado deja consumidor ya cargado con estado anterior | PRES-002..006 | Retirar registro propio y recargar consumidor cuando proceda; no borrar buffers ajenos ni prometer reversión instantánea. |
| R-09 | Tipo de registro TGSC/padding no coincide con tamaño aceptado por servicio | WORLD-033 | Usar contrato de bytes real y comprobar tamaño concreto del caller; sizeof Windows no medido aquí. |
| R-10 | Ejecutar servicio o usar GPU prestada fuera de callback/fase/hilo | PRES-010..013, HOOK-030 | Respetar game thread/render worker, no liberar device/queue prestados; detener trabajo propio antes de unload. |
| R-11 | Liberar con allocator/CRT incorrecto o mantener puntero al destruir solid heap | ROOT-001..006 y PRES-037/038/039 | Usar la pareja de ownership; JKR token/fallback no justifica liberar memoria de otro servicio. |
| R-12 | Booleano de ResourceService se interpreta como validación de argumentos | SDK-019, PRES-035 | Validar parámetros antes; retorno enum=5 se vuelve true en ramas inválidas. Solo discrepancia estática, sin fix productivo. |
| R-13 | Símbolo/target solo declarado se presenta como hook operativo | HOOK-010..012/026/028 | Verificar manifest, firma, dirección, aliases y entrada parcheable en la imagen concreta. Ningún target nuevo probado aquí. |
| R-14 | Singleton no nulo se confunde con recursos/audio listos | HIST-005/007/011 | Comprobar fase y recursos reales; informes históricos no certifican todos los estados ni observación audible actual. |
| R-15 | Actualización “por frame” usa tiempo de presentación para política de actor | ARCH-001, ROOT-007, HOOK-018 | Separar tick de simulación, execute de actor y presentación; pausa/captura/errores alteran rutas. |

Un rollback de registros no deshace mutaciones arbitrarias de inventario, flags, posiciones, archivos o servicios externos. Restaurar únicamente estado propio y aún compatible con el contexto; reingreso/reinicio puede ser necesario cuando un consumidor conserva objetos. No se propone modificar host, SDK, EXE, ROM ni saves como mecanismo de implementación .dusk.

R-16 — Persistencia interna del port no debe confundirse con SaveService: AchievementSystem fija loaded antes de IO, captura errores y tick limpia dirty después de save. No interpretar snapshot UI o toast como confirmación durable. PORT-004/005; sin fallo reproducido ni acceso a archivos del usuario.

R-17 — Cambiar un único valor de tiempo no controla todos los escritores: avance normal y KYTAG11 tienen condiciones distintas, y el flag de control se limpia. El rollover modifica fecha y un bit temporal; setters escriben estado en memoria, no confirman guardado CARD. PRES-040..043; sin efecto runtime probado.

R-18 — Aceptación de cambio no significa destino ejecutándose: file-select ignora retorno y continúa mutando estado; delete-before-create destruye UI/heap antes de conocer éxito de PLAY. Cancelación/ReRequest no prueban rollback. ARCH-002..007; riesgos de punteros de R-07 ahora contrastados para esta escena, sin afirmar invalidación universal ni fallo runtime.

R-19 — Animación parcialmente aplicada y estado compartido: AutoMata instala BCK antes de validar BTK; entry/remove BTK mutan tabla y remove no restaura animator anterior. PRES-044..047. Retorno0 no equivale a sin efectos; no hay coexistencia/runtime demostrado.

R-20 — Message retira registro pero candidatos copiados no revalidan handle/active; bytes seleccionados sobreviven por binding,NO por ello userdata/DLL. Callback debe entregar texto legible durante copia posterior al retorno. CALLBACK-009..013; ninguna liberación segura universal ni coexistencia/runtime certificada.

R-21 — Conexión LiveSplit/toast no confirma comandos ni timer remoto: send ignora retorno,startPending se consume antes de comandos y no se rearma al reconectar; retry cuenta llamadas UI,no segundos. PORT-006..009. Backend Borealis ausente,no transporte ni fallo observado.

R-22 — Presión detectada,flag filtrada,recorrido terminado,switch RAM y save duradero son hitos distintos. Swpush Delete devuelve1 incluso si Release informa error; no acredita drenaje de callback ni reversión de switch. PLAYER-035..039; sin fallo runtime inducido.

R-23 — Solicitar colpat no aplica color inmediatamente: gather compartido puede diferirse o ser sobrescrito; tag tipo11 no restaura estado al borrar/salir del gate. El fog global y por tevstr son distintos. PRES-048..051; sin render/runtime ni rollback probado.

R-24 — Retry de sidecar depende de evento futuro y vida de SaveStore; invalidate_save borra dirty sin flush. Menú/toast vanilla no recibe resultado del flushvoid. WORLD-034..037; sin IO personal ni crash reproducido. Corrección índice save_slot_written: API interna,POTENTIAL_REQUIRES_VERIFICATION,contrato observe_saves sigue oficial.

R-25 — BST: alta/baja de registro y mapa activo difieren; frameEnd invoca WSYS y remove_sound_table no marca dirty. Sin lifecycleApplied posterior,edición puede quedar pendiente o retirada seguir publicada. Sonido captura shared_ptr de datos. PRES-052..055; inferencia condicionada,sin audio runtime ni fix de host.

CP-R18 · R-26: unregister OK no prueba create queue vacía; forceDelete transforma Delete=0 en finalización y UNAVAILABLE no revierte borrados. Request-only sin profile sustituto falla al resolverlo; reutilización numérica y perfiles retenidos durante unload son riesgos condicionados (PLAYER-040..045), no crash observado.

CP-R20 · R-27: Config unsubscribe no cancela callbacks capturados; la escritura recursiva del mismo nombre altera valor sin notificación anidada y el actual se lee por callback. Destruir variable/userdata en notify no queda cubierto por copia de la lista. CALLBACK-015..018; sin fallo runtime observado.

CP-R21 · R-28: modelo visible, fondo registrado y resultado de consulta de agua son estados distintos; no inferir retiro de collision por puntero de modelo nulo ni persistencia por cambio de altura. Matriz/backing deben sobrevivir al fondo registrado; orden entre perfiles y geometría DZB no probados. PRES-060..064.

CP-R23 · R-29: switch del tag MYNA2 se activa al aceptar petición, sin comprobar fallo posterior. Clear de NPC usa room actual y destructor no revierte switch; puede inhibirse reentrada o duplicarse solicitud al apagarlo externamente bajo gates. PLAYER-046/050/051; inferencia condicionada, sin fallo runtime.

CP-R24 · R-30: dos estados overlap (puntero manager y exclusión scene) no se limpian por las mismas rutas. Error temprano puede dejar wait y cancelación tardía puede conservar exclusión. ARCH-009..011; inferencia condicionada, sin bloqueo runtime probado ni garantía de permanencia.

CP-R25 · R-31: reconsultar getObjectRes no relee overlay si dRes_info sigue cargado; retirar ganador no restaura objeto decodificado. Fetch JKR puede caer a backingARC al fallar lectura, sin demostrar fallback al mod anterior. PRES-065..067; sin coexistencia runtime certificada.

CP-R26 · R-32: initialized es estado del wrapper de presencia, no ACK ni conexión lista; cambio CVar sin callback UI no equivale a iniciar/cerrar backend. Shutdown no demuestra drenaje de handlers en Borealis ausente. PORT-010..013; sin conexión ni datos personales observados.

CP-R27 · R-33: mount sync indica Done aun con archiveNULL; cambiar ID ignora parse/bind y no prueba backing válido. Mismo ID/idioma nuevo no recarga bytes; s_resources no posee archive. PRES-069/070/072/073; sin fallo runtime ni fallback inglés observado.

CP-R28 · R-34: consumo no acredita callback; close no destruye, destroy con claim retorna CONFLICT. Copiar fn/userdata no drena llamada ni mantiene biblioteca; WindowEvent local no puede retenerse. CALLBACK-019..022; sin fallo runtime.

CP-R29 · R-35: registro prioritario void puede saturarse aun con Create COMPLEATE; cut depende de índice y no comprueba identidad. IsDelete rechazado ya marca99 y solo desvanece fuera de home room; overlap permite retirar con potencia alta. PRES-074..077; riesgos condicionados,sin fallo visual/runtime observado.

CP-R30 · R-36: HP letal,ACT_B2_DEAD,mDead,flags,reward encolado y destructor son hitos distintos. Borrado anticipado no ejecuta restauración de cámara/progreso del modo28; callback de joint presta this y cleanup total de externos no certificado. PLAYER-052..056; inferencia condicionada,sin fallo runtime.

CP-R31 · R-37: reset helper1 no confirma cola; next-stage se reactiva antes de request y audio/restart no se revierten. ReRequest puede redirigir request previo SOLO si sigue vivo,tipo2,mismo ID y creating_id−2; no revive objeto liberado. SaveSync0 no es ACK. ARCH-012..016; inferencias condicionadas,sin fallo runtime.

CP-R32 · R-38: add fallido no aborta Sakuita; envío sin matching consume capacidad y remove wrapper no confirma baja. Punteros modelo prestados hasta draw,count de altas no es count de instancias,room/primer drawBG forman restricciones distintas. PRES-078..081; riesgo de lifetime condicionado,sin fallo runtime.

CP-R33 · R-39: cancelOK conserva slot y no garantiza CANCELED; completing mantiene handle pero ya tomó resultado. Snapshot/userdata/código tienen vidas distintas; take_all no prueba worker drenado ni staging eliminado. CALLBACK-023..027; hipótesis reentrantes condicionadas,sin fallo runtime ni tráfico de prueba.

CP-R34 · R-40: switch y latch FireWood divergen; Delete previo a timer0 no escribe progreso pendiente,255 no deja switch. Emisión visible y registro de luz pueden fallar sin cambiar lit; partículas dejan de renovarse pero retiro depende de evento/calc. PLAYER-057..060; inferencias condicionadas,sin fallo runtime.

CP-R35 PORT-014..017: respuesta de consola no mide efecto/runtime; ocultar conserva estado y no revierte reloj global. Listeners UI retirados no prueban callback en curso drenado. Comandos host no son LogService ni API de registro; no certificado Windows/hook.

CP-R36 PRES-085 STATIC_INFERRED: con flag1,inserción2D rechazada y sin consumidor alternativo,el gate separado puede mantenerse; alcanzabilidad no demostrada. capture_delete depende de pause y no acredita retirar captura pendiente sin pintar. flag3 precede copia GPU,sin ACK ni prueba Windows.

CP-R37 PLAYER-061..064: tag conserva ID aun sin actor y no acredita respawn postfallo; hide no descarga recursos. Evento024 retorna1 tras marcar índice,sin prueba de cobro/switch/entrega. SaveSwitch es RAM; delete display solicitado no finalizado,tabla estática de tags presta pointers y cleanup global no auditado.

CP-R38 PRES-089 STATIC_INFERRED: KYTAG08 publica fog_avoid_tag y Delete no lo limpia. Si consumidor MA11 sobrevive al actor,checkNULL no acredita lifetime; no UAF/crash ni alcanzabilidad observados. Puntero único se sobrescribe sin arbitraje local; sin garantía de coexistencia/rollback Windows.

CP-R39 PRES-090..093: mAnmRate interno sin clamp; tracks comparten frame y callback cambia animación durante árbol,con assets compatibles como precondición. ModelData posee callback común,userArea actor por instancia. ERROR_EXIT nulifica,no acredita frees; heap/ARC/sound separados,sin leak ni Windows coexistencia observados.

CP-R40 PRES-097 STATIC_INFERRED: keys globales compartidas entre conjuntos de mods; forget/detach de uno puede borrar muestra del otro. MOD_OK registro fuera de recording no prueba muestra; lookup copia/no garantiza out en fallo. Sin prioridad/refcount/rollback previo ni runtime certificado.

CP-R41 PLAYER-066/067: TimerStart/End wrappers descartan retorno interno; true no acredita running/resultado actualizado. Meta copia RAM aun si End falla; DeleteRequest difiere a closeAnime. Modo compartido no da ownership por actor; sin bloqueo,récord ni runtime observados.

CP-R42 PORT-018..021: cancelRequested no confirma Canceled; destructor/join espera retorno backend sin plazo certificado. Estado cachedUnknown tras inspectSuccess puede permitir UI; verifyUnknown nuevo toma error distinto. Misma ubicación no certifica bytes actuales; no fallo observado ni disco personal abierto.

CP-R43 ROOT-012/013: subDelete0 aún puede retirar drawtag en msg; no observado con Timer,que retorna1. fopMsgM_Deletevoid no confirma encolado. No asumir limpieza actor heap/audio/owned_samples ni drenaje GPU en msg; cleanup concreto debe rastrearse.

CP-R44 PRES-099..101: eventoBAS avanza índice antes de filtros/pool/fallo,sin retry local; userData presta evento. Cambio de animación puede dejar sonido estado2; dispose distingue release de stop y ambos de mixer drain. Sin sonido/audibilidad/fallo runtime observados.

CP-R45 PRES-103/105: setSkinDeform descarta initMtxIndexArrayret y cambia flags/buffers por etapas,sin rollback completo; no fallo runtime declarado. Fastpath puede mutar arrays ModelData; destructor vacío no acredita frees ni leak. Asset/índices/ABI/export y GPUdrain pendientes.

CP-R46 CALLBACK-029..031: copiar Event no copia payload; siguientepoll del mismo mod acota vistas incluso de otra conexión. CloseC++handle0 no retira entrada host; CLOSED/deactivation sí. take_all no prueba workerdrain/handshake sin backend; ningún tráfico/fallo runtime observado.

CP-R47 precisa PRES-089: KANKYODelete no destruye g_env_light ni limpia fog_avoid_tag explícitamente. Orden room/actor/fondo sigueNOT_VERIFIED; no se concluye UAF ni seguridad global de teardown. Listpriority no certifica orden de borrado.

CP-R48 PLAYER-069..072: tipo alto,byte de estado,ID de objetivo e índice joint no son intercambiables; hit At no acredita daño HP. Flag93f precede solicitud/destructor y no drena partículas. Matrices/modelo objetivo prestados; sin fallo ni hook Windows observado.

CP-R49 WORLD-041/042: clearRoomSwitch/Item se ejecutan después de pedir deletes,sin comprobar cada retorno;BG puede conservarse por rama20. No se declara seguridad de referencias globales ni UAF por ello. PRES-089 permanece condicionado;sin orden de destrucción probado por perfil/lista.

CP-R50 PRES-110/111: removeBTP no verifica identidad ni restaura texNo;riesgo condicionado si hay escritor compartido. useHeapInit Wflag devuelve5 en fallosBTP,caller convierte a bool;no fallo runtime observado ni patch. Recursos de animación prestados deben seguir vivos durante calc.

CP-R51 CALLBACK-032..034: closure host copia fn/userdata pero no posee DLL ni datos usuario. Guard pane/active previo no valida Control individual ni callback ya iniciado;detach invalida futuros accesos,no acredita drenaje. Sin fallo UI/runtime observado.

CP-R52 PLAYER-073..076: listallena expulsaID mediante delete sin confirmar;contador,itemdemo,reset y destructor son hitos distintos. E_ARROW Delete no limpia listaLink ni todos los emisores explícitamente;solicitar delete no corta todo Execute. Sin fallo ni reentrancia/runtime observados.

CP-R53 CALLBACK-035/036,PORT-022: state prestado válido hasta seleccióncompleta,no hasta unload arbitrario;MOD_OK no imponePROCEED. Unregister solicitareset y cambia modo antes de finalizar escena;fallbackfilename/config no revierte side effects ni drena código. Sin fallo/runtime observados.

CP-R54 PRES-112..114: switchoff conserva timer/ciclo/custompower y sonido se solicita segúnvariante;Delete no restaura escritor previo. Vientoefectivo es suavizado,no setter inmediato;riesgo condicionado de escriturasglobales múltiples,sin fallo observado.

CP-R55 PRES-118 STATIC_INFERRED: callbacktraceglobal puede usar Vecactor prestado;DeleteE_ARROW limpia field9ec,no demuestra retiro de binding mFireEMKeys0. Riesgo solo si freeactor precede calcage>0 con bindingvivo;orden/alias/alcanzabilidad pendientes,no UAFobservado.

CP-R56 ARCH-020 STATIC_INFERRED: status2 y requestrechazada aún pueden producirLoadedSave/ff;siLoadSyncsiempre0,looplocalnoavanza. No se afirma fallo backend/hang ni save cargadoobservado;sinrollback/retrylocal probado.

CP-R57 PLAYER-078..080: Execute0 no impidecopiamatriz/Move;Delete0 no impideRelease;Releaseerror no modificaret. Matriz/BG/ARCvidasdistintas,switchno revierteEND. Sin choque,fallo o hookWindowsobservados.

CP-R58 PRES-122 STATIC_INFERRED: handleSDKestable puede sobrevivir reregistrorechazadoID0 sin rollbacklocal. UnregisterliberadatossegúncontratoAuroracomentado,no garantiza visual/GPUdrain auditados;keypointer no posee GXoriginal. Sinfalloobservado.

CP-R59 PORT-023..025: Superseded no es activaciónfallida;Succeededoperación/toastno certifican estadovigenteni DLLdrain. Flushconsumeavisos aun sinmostrarlos conModsWindowvisible;nofalloobservado.

CP-R60 PLAYER-082..084: posMove0 puede mutarpos/rotaciónograb;checkBoomerangCarry altera equipo/flag/anime,no es querypura. Waitrestauracamposconcretos,nocleanupdeactor ni recompensaduradera. Keepsprestados/noownership;sinfalloobservado.
