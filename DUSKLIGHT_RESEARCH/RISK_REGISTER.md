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
