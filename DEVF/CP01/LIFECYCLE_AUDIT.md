# Auditoría exhaustiva dirigida del cierre 2.0.3

Referencias con hashes y líneas: evidence/targeted-source-audit.json. No se modificó el motor ni se usaron hooks, offsets antiguos o estructuras privadas como ABI de producción.

## Corrección de la interpretación de colas
La cola g_fopAcTg_Queue NO contiene solo actores completamente creados: fopAc_Create añade el actor al entrar por primera vez, antes del callback custom y antes de completar recursos. Un actor esperando Wrock después de ese callback puede ser visible para el barrido nativo. La afirmación anterior de que toda creación pendiente era invisible sería demasiado amplia.

La ventana anterior a ese primer callback sigue en g_fpcCtTg_Queue. fpcSCtRq_Request conserva process_name y create_post_method; unregister_actor no drena esa cola. fpcPf_Get comprueba límites y devuelve nullptr si falta el perfil: no se afirma acceso fuera de rango ni crash inevitable. Sin reutilización, una solicitud posterior puede fallar limpiamente al no encontrarlo. Sin embargo, los índices SlotMap se reutilizan, ProfileName no contiene generación y el post-callback opcional queda copiado en la solicitud. La API no ofrece un token de drenado que elimine ese riesgo de reutilización/callback pendiente. DEVF ahora rechaza create_function adicional.

## Contratos de servicios usados y alternativas revisadas
| Operación | Qué acredita su retorno | Qué no acredita |
|---|---|---|
| register_actor | Perfil y handle generacional de slot registrados; callbacks y tamaño verificados por host | Vida terminada de instancias futuras; ausencia de requests por ProfileName |
| create_actor / create_actor_from_name | Solicitud aceptada e ID; lookup por nombre también sustituye argument por el del objectName | Actor creado, recursos listos o cancelación/drain; caller debe inicializar/validar parámetros |
| create_child_actor y variante por nombre | Solicitud con parentID mediante la misma ruta | Barrera adicional de cierre; no se usan en CP01 |
| get_actor_id / get_actor_room_num | Encontrar un actor ya visible al buscador | Enumerar pending requests o demostrar perfil inexistente/cola vacía |
| delete_actor | Delete encolado, o incluso MOD_OK si no encuentra el ID | Destrucción terminada; si la solicitud aún no tiene actor visible, MOD_OK no la cancela |
| unregister_actor | Retirada según barrido activo/delete, con MOD_UNAVAILABLE si quedan actores | Drenado completo por perfil ni preservación DLL después de fallo |
| Stage add/patch/delete | Copia de registros de carga bajo ownership del mod | Spawn inmediato o eliminación de solicitudes/instancias ya creadas |
| Stage remove_actor_edit/detach | Retirada del registro de futuras cargas | Cancelación de actor pendiente o una instancia activa |

Los nombres de perfil custom son cortos y únicos; matching con nombre retail puede sustituir lookup y se evita. Stage exige sala específica para add, nombre <=8 y tamaño ACTR/TGSC validado; layer -1 coincide con cualquier capa. Los buffers se copian al registrar: no conserva el stack record del caller. ProfileName (int16) no es ActorHandle generacional (uint64), ni ActorId efímero (uint32).

Existen fpcCtRq_Cancel/iteradores de creación en código del juego y cancelación de requests que ya tienen process. No se usó un cast a standard_create_request_class privado ni sus offsets para enumerar por nombre solicitudes Stage antes de process. Una ruta de cancelación acotada por ID de request propio sería un experimento diferente que requeriría pruebas de identidad/cola; no aporta por sí sola el veto/force-delete ni la cobertura de Stage. No se presume inexistencia de todo mecanismo interno: la carencia es del contrato completo de servicios/lifetime que CP01 necesita.

## Destrucción real y orden
unregister_actor marca forceDelete, solicita eliminación de actores del perfil, procesa la cola de eliminación y borra el slot solo si no ve actores restantes. Para actores con create_req, fpcDt_Delete llama fpcCt_Abort/fpcCtRq_Cancel antes de la destrucción, y rechaza borrado mientras la solicitud está is_doing. Esto acredita rutas concretas de cancelación de instancias ya visibles; no una garantía global de cola vacía para todas las solicitudes por nombre.

ActorService modDeactivating ocurre antes de mod_shutdown; StageService modDetached después. La lógica conservada stop(true) distingue el perfil que ya retiró el pre-hook de un MOD_UNAVAILABLE. Retirar un Stage edit elimina futuras apariciones, no instancias ni solicitudes ya generadas. El cleanup explícito propio retira Stage antes del perfil cuando es posible. No se borran actores ajenos ni se retienen IDs para eliminar referencias posiblemente reutilizadas.

**Fallo de contrato confirmado:** actor_delete devuelve forceDelete ? 1 : resultadoDelCallback. En desregistro forzado un fallo de destroy puede quedar convertido en éxito. El engine fopAc_Delete/fpcBs_Delete puede liberar heap/instancia mientras el callback no consiguió liberar componentes. Un callback que retorna 0 no es una barrera eficaz en esa ruta.

## Recursos y colisión: correcciones propias
cBgS::Release devuelve 0 en éxito y 1 en fallo. ResourceLifecycle.release ahora verifica el resultado: si falla la retirada de colisión, conserva archivo y referencias; no continúa con liberaciones. El estado pasa a closing inmediatamente, bloquea execute/draw y cualquier nuevo avance de carga; un reintento no duplica una colisión ya retirada. Rock::destroy solo invoca el destructor tras release exitoso; nunca declara éxito local ante fallo.

fopAcM_entrySolidHeap puede destruir un heap fallido y repetir su callback. create_heap reinicia referencias en cada intento y el wrapper las limpia al retornar fracaso para no dejar direcciones de un heap destruido. execute público no accede a modelo/collider hasta ready; la transformación inicial se ejecuta por una ruta interna válida tras heap/registro exitosos. Cancelación cPhs_UNK3 es terminal además de cPhs_ERROR.

**Fase de archivo pendiente:** dComIfG_resDelete asserts si phase.id==1 y solo procesa id==2. cPhs_ERROR/UNK3 resetean id a 0; ese 0 no prueba que nunca se adquiriera una referencia antes del error. RockOps ahora rechaza liberar por esa API fuera de id 2, en vez de ignorar el resultado o afirmar limpieza. Se conserva ownership para informar el bloqueo. No se destruye a ciegas un comando DVD/mount pendiente, cuyo cancel/drenado seguro no está garantizado por esa API. Bajo forceDelete el host aún puede ignorar el retorno 0: esta corrección local no elimina el bloqueo del host.

## Slot de colisión reutilizado durante cambio de escena
cBgS::Dt limpia la tabla global, pero el ID local del collider puede seguir indicando un slot antiguo. Release solo comprueba la coincidencia de puntero en DEBUG; en una build de distribución un índice obsoleto podría retirar una colisión ajena si la tabla fue reutilizada. No basta con comprobar el retorno de Release después.

La política propia ahora busca referencias al collider en los 256 slots mediante GetBgWBasePointer. Comprueba identidad del actor con ChkPolySafe/cBgS_PolyInfo, índice local y uso antes de retirar la referencia global única. Una referencia ausente acredita únicamente que la tabla actual no lo referencia: retira solo su ID local con collider->Release, sin tocar una entrada ajena. Referencia duplicada, índice movido o actor distinto bloquean el cleanup. No se consultan polígonos: SetPolyIndex(0) se usa solo para formar identidad válida, sin query de geometría.

Seis pruebas de tabla simulada cubren propiedad correcta, tabla vaciada por escena, slot reutilizado por objeto ajeno, referencia propia en otro índice, identidad de actor incorrecta y duplicados. El adaptador nativo compila/enlaza con APIs exactas; su comportamiento dentro del motor queda NOT_TESTED. Esto evita una retirada ciega, pero forceDelete y la descarga sin barrera siguen fuera del control del callback.

## DLL y barrera conservadora
HostService 2.2 no tiene veto de Disable/Reload, pin del módulo ni await/drain de actores. watch_mod_lifecycle es observación de otros mods; fail solicita desactivar y no preserva vida. Loader registra fallo/excepción de shutdown y continúa a unload_native. Windows NativeModule llama FreeLibrary sin consultar un resultado de limpieza.

Los tests Windows con DLLs propias reproducen FreeLibrary tras shutdown=MOD_UNAVAILABLE. GET_MODULE_HANDLE_EX_FLAG_PIN conserva el código de una DLL propia hasta terminar el proceso, pero no retiene ModContext, perfiles/slots, solicitudes ni recursos del host. No implementamos pin como falsa solución al ciclo de vida ni hooks/parches al loader.

**Política implementada:** requirements de ubicación, drenado, colisión y barrera siguen sin acreditación y el módulo queda DISARMED_NO_REGISTRATION antes de registrar perfil alguno. No registra Actor/Stage, no crea actor, no expone callbacks al engine y no mantiene ownership tras initialize. Un cambio de configuración no abre ese estado. Se evita generar la situación insegura; no se pretende que mod_shutdown pueda impedir un FreeLibrary del host cuando existan actores.

## Qué permite cerrar el bloqueo
Se requiere una garantía real de host, demostrada en código/pruebas: cancelación/drenado de solicitudes por perfil antes de retirar el slot (sin reutilización prematura), resultados reales de destrucción sin convertir fallo en éxito, y retención del perfil/contexto/DLL cuando el drenado falle; o un contrato equivalente que elimine esos riesgos. No existe actualmente una API de servicios que aporte todo ello. Una futura corrección upstream o cambio explícitamente autorizado al host deberá probarse; esta tarea no lo implementa ni cambia el EXE original. Instrucciones de no pulsar Reload son útiles, pero no constituyen por sí solas una garantía técnica.

Las cinco funciones de cierre extraídas se compilan sin cambios de cuerpo en un laboratorio con colas/slot/backends simulados, claramente separados del ABI real. Las pruebas de loader usan FreeLibrary real sobre DLLs propias. Ninguno de esos PASS acredita el motor, colisión, J3D, escenas ni DX12 en ejecución.
