# Propiedad de escena: tres datos diferentes

Origen y referencias D/S: [COMPARATIVE_AUDIT](COMPARATIVE_AUDIT.md), Dawnlight `9bb214d`, Dusklight oficial `40457c6`, base DEVF `545b2d1`. **PASS_STATIC** de los flujos descritos; ejecución y limpieza Windows/DX12 de DEVF **NOT_VERIFIED**.

| Dato | Qué selecciona / qué no demuestra |
|---|---|
| Stage + room | Lugar/registro y contexto de datos. El `room_no` del append no fija el dueño del proceso. |
| Layer lógico de escenario | `getLayerNo(0)` filtra las ediciones Stage y los grupos ACT0…ACTe. No es un layer_class ni el padre del proceso. |
| Layer del motor | `layer_class*` y layer_id en request/layer_tag. Determina árbol de procesos, contexto de llamadas, recorridos y destrucción. No es ownership del mod. |

## Captura y construcción asíncrona

Cadena A2, sin ejecutarla: S1 create_actor220–236 → S2 fopAcM_create258–268 → S3 fpcM_Create45–48 → S4 fpcSCtRq_Request140–177 → S5 fpcCtRq_Create132–145. `fpcM_Create` pasa **fpcLy_CurrentLayer()**, y Create almacena ese puntero en `request->layer`, asigna ID y añade request a la cola y a la cancel_list de esa capa. Restaurar el contexto del caller después no cambia el request ya copiado.

En frames posteriores, S4 phase_CreateProcess49–64 y phase_SubCreateProcess67–85 seleccionan **request->base.layer**. S6 fpcBs_Create133–163 consulta perfil, reserva su process_size y resuelve layer_tag/priority del perfil. Los perfiles seleccionados E_SB, E_RD y B_TN usan **fpcLy_CURRENT_e** (S15/S16/S18, perfiles). Un perfil que fijara otra capa exigiría su propio análisis: pasar un layer al request no acredita el propietario final de cualquier perfil.

Así, un enemigo CURRENT solicitado desde root puede terminar root-owned aunque `room_num` sea correcto. ID válido es solo aceptación de request. La visibilidad en cola de actores empieza antes de completar Create (revisión previa S17); `fpcM_IsCreating` consulta cola de requests (S3:48–50/S5:18–33). False también puede significar fallo o cancelación, y no asegura presencia, recursos posteriores, modelo visible o DX12. Una comprobación futura necesita ID propio + perfil esperado + contexto + fase nativa completa/ejecución + componentes requeridos del enemigo; sin post-callback DLL y sin un único flag universal de readiness.

## El fallo de raíz y el alcance de su evidencia

S3 cpp36–38 limita fpcM_DrawIterater al árbol root. S12 dScnPly_Draw659–662 recorre la cola global de actores y vuelve a solicitar sus draws. Por eso un enemigo root-owned puede participar en ambos recorridos; la escena de juego, que sí debe estar bajo root, dibuja sus actores. S12 J3DDrawBuffer::entryImm202–208 religa el next del mismo paquete. Reinsertar el mismo nodo intrusivo puede formar un ciclo o perder enlaces. **PASS_STATIC** de los recorridos y de la mutación de enlaces; **PARTIAL** para la cadena completa de corrupción concreta, que aquí no se reprodujo en renderer/Windows.

D2:8–34 documenta Link invisible, ciclos de material, abort de staging buffer y SIGSEGV de Bomskit contra jugador ausente, y reporta que la selección de propietario resolvió el problema en un dispositivo. Se conservan como **reporte externo**, no como crashes o PASS de DEVF. No se aumentan buffers, fuerzan flags de visibilidad ni introducen los antiguos hooks de reparación de ciclos; D2:44–48/127–130 reconoce sus límites.

En destrucción, S11 fpcDt_ToDeleteQ63–105 inspecciona el nodo, verifica delete timing, cancela su lista y recorre sus procesos; S8:66–104 puede esperar a que terminen creaciones bajo el nodo. Un actor root-owned queda fuera del árbol de la escena eliminada. Su siguiente execute puede seguir accediendo al jugador retirado. Pertenecer al árbol adecuado fundamenta la limpieza nativa; **no garantiza terminación inmediata de recursos/request o ausencia de todo fallo parcial**. No se presenta fpcLy_Cancel como cancelación ilimitada y automática: el guard de creación puede aplazar la llegada a ese paso.

## A1 — contexto natural de sala

S10 objectSetCheck198–243 llama al reloader tras preparar bancos y BG. Esa función se invoca durante phase_3/phase_4 de dScnRoom_Create474–505 y desde dScnRoom_Execute267–288. El perfil ROOM_SCENE usa g_fpcNd_Method y crea un nodo de sala (S10:514–524). S8 fpcNd_Create107–124 / Execute45–61 seleccionan **la capa interna del nodo de sala** antes de ejecutar sus submétodos y restauran la anterior después.

Dentro de ese contexto: S9 roomReLoader2816–2835 → Stage helper2611–2633 → actorCreate1635–1662 → fopAcM_Create → fpcM_Create. Por tanto A1 **adquiere naturalmente la capa de sala** para los perfiles CURRENT revisados en el flujo nativo normal. El filtro stage/room/layer lógico ocurre aparte en S14:139–155. El StageService no se llama para crear inmediatamente dentro de add_actor.

**PASS_STATIC condicionado al call path nativo y perfil CURRENT.** No se extrapola el fallo de UI A2 a A1. No hay garantía si un consumidor invoca manualmente roomReLoader fuera de ese contexto: no hacerlo, pues además puede duplicar actores originales. Ni room_num ni getLayerNo prueban por sí solos esa capa; una futura observación deberá registrar el layer_id del proceso creado y su nodo padre.

S10:244–262 muestra limpieza selectiva de contenidos de la capa de sala por status flags y espera a creaciones de esa capa; la eliminación del nodo/escena también recorre sus descendientes. Una transición de room no necesariamente destruye todas las salas cargadas al instante. Un perfil puede cambiar de dueño: E_RD scene_no=2 llama setStageLayer en Create, y su ruta de montura puede hacerlo en Execute (S16:7384–7391,2196–2209). A1 no puede prometer limpieza de room de cualquier modo de enemigo que migre al stage.

Persistencia/duplicados: el registro se consume cada vez que se cumple roomReLoader, no exactamente una vez por sesión. S10 field_0x1d4/status evita invocación rutinaria cada frame en su flujo normal, pero permite borrar/recrear contenidos. S14 no deduplica instancias por handle/setID. Retirar el edit no destruye las creadas; hot reload/reenable en sala ocupada queda **NOT_VERIFIED**. Conservar la política pasiva del checkpoint anterior, sin deletion por primer match de perfil.

## A2 — helper Dawnlight y vía compatible

D1 create_test_actor_in_player_layer211–230:

1. Rechaza player nulo y transición habilitada.
2. Lee `player->layer_tag.layer`; rechaza null, root y fpcLy_IsDeletingMesg.
3. Guarda fpcLy_CurrentLayer en un objeto local con restauración en destructor.
4. Selecciona capa del jugador, encola con ActorService y restaura al salir, incluso ante error/exception.

La selección de contexto mediante **funciones oficiales exportadas** no parchea instrucciones ni se usa para simular un atributo individual. S7 muestra un setter simple de contexto global, y S13 commands/ImGui del original usa el mismo principio con la capa interna PLAY_SCENE. No se llama desde DEVF a ese código interno de UI; sirve de contraste estático. La disponibilidad concreta de las funciones está acreditada en COMPARATIVE_AUDIT. El wrapper de selección es separable de install_test_hooks de Dawnlight; **create_standalone_actor/spawn_enemy_for_testing enteros no son reutilizables** porque instalan hooks de admisión, proceso y descendientes.

Límites de los guards:

| Condición | Contrato exacto y riesgo pendiente |
|---|---|
| isEnableNextStage | Indicación de next stage, no lock/reserva contra todos los cambios de room, menús o destrucciones. |
| Player/layer vivos | Punteros prestados. Getter/header no aporta lifetime refcount. Validar en el mismo tick/contexto, no conservar para una tarea posterior. |
| IsDeletingMesg | S7:43–51 lee **delete_count > 0**. No es un flag exhaustivo del nodo en transición; también puede rechazar una capa viva donde se elimina un hijo. |
| Restauración | Normal/error/throw restaura el puntero previo; no deshace requests ya encoladas ni reserva la vida del puntero previo. |
| Reentrada | Scopes LIFO son una estrategia válida; los stubs no prueban callbacks anidados, cambio/destrucción de capas dentro del servicio o interacción con otros mods. Nunca yield ni lanzar creación desde workers/render callbacks. |
| Hilo | S21 tick llama mod_update sin escoger escena; su sitio está en fapGm_Execute. SDK UI exige game thread (ui.h:19–22). Game thread ≠ capa correcta. |
| Owner escogido | Capa de Link puede ser capa de juego o de sala según contexto: observarla. El precedente original usa play layer explícita. Capa no-root ≠ propiedad de la room solicitada. |

**B / NOT_VERIFIED** de seguridad completa del helper en DEVF. Una solicitud desde mod_update/UI ha de resolver escena/sala viva compatible, validar perfil/room/layer lógico, guardar/restaurar contexto sin ejecución anidada destructiva y encolar con create_function NULL. El propietario se fija **antes** de solicitar. Reubicar un actor ya creado con setRoomLayer/setStageLayer no protege el request anterior y tampoco garantiza la transferencia instantánea de su prioridad.

Una alternativa B existe en el header oficial `f_pc_stdcreate_req.h`: fpcSCtRq_Request permite especificar layer explícitamente. Está exportada en Windows. Exigiría asumir correctamente append/allocation/error ownership y readiness, de modo que no se aprueba un reemplazo directo de ActorService ni se implementa aquí. Se registra la posibilidad para no declarar imposible A2 sin hooks.

## IDs, cancelación, DLL y descendientes

ActorId no es un handle con generación/owner DEVF garantizados. Registrar la relación con una colocación propia al retorno, descartar IDs al fin de contexto y volver a resolver punteros cada tick. get_actor_id(profile) no identifica la instancia propia. ActorService.delete_actor solo busca actores visibles: MOD_OK sin match no cancela una solicitud pendiente.

**Matiz nuevo respecto del checkpoint anterior:** el ABI sí declara y exporta fpcCtIt_Judge, la base pública create_request, fpcCtRq_IsDoing y fpcCtRq_Cancel (S5/S19). Hay una vía **B / NOT_VERIFIED** para investigar una cancelación por request propio, sin private offsets ni hooks. No basta con tener la función: Cancel61–74 fija is_cancel antes de ciertos fallos, puede devolver FALSE y puede liberar el request cuando termina. No cachear/reutilizar pointers de requests ni borrar nodos/manipular métodos; validar lookup, ID/contexto, no estar is_doing y los fallos parciales en un laboratorio antes de habilitar esta vía. No se amplía aquí la auditoría antigua de descarga DLL ni se declara resuelta.

Para native requests con NULL callback, sobrevivir a desactivar DEVF no introduce por sí mismo un callback DLL en el enemigo. Sigue siendo un riesgo de colocaciones tardías, duplicación y semántica de desactivación. Los perfiles personalizados/recursos dependientes de la DLL mantienen su bloqueo independiente; el return de shutdown no puede vetar unload (evidencia anterior/S21).

S2 createChild303–312 copia parent_id pero **captura la capa actual**, sin derivarla del padre. S6 Execute59–81 restablece la capa del proceso durante execute, y S4 lo hace durante create: hijos solicitados sincrónicamente en estos métodos CURRENT normalmente capturan el contexto del padre. Esto es **PASS_STATIC condicionado**, no regla universal de cualquier callback externo. E_RD crea flechas mediante createChild (S16:6909), pero también puede crear E_WB por create sin parent ID (7140); E_SB crea un efecto DISAPPEAR por fastCreate en su muerte. El hook Dawnlight createChild no cubre todos esos caminos. parentActorID no implica cascada de destrucción al eliminar solo el padre: la capa común sí es fundamental en el teardown de escena. No prometer tracking ni admisión de toda descendencia por conocer únicamente el ID del enemigo.

## Qué demuestra el test Dawnlight

D3:6–16 extrae **solo** el helper. Las reglas de engine están simuladas: Layer es un bool, ActorService agrega a vector, draw religa paquetes locales y delete_play_scene elimina elementos de actors (18–78). Assertions80–129 comprueban owner capturado, rooms0/51, tres capas caller, retorno de ID, restauración en éxito/error/throw, rechazo null/root/deleting/nextStage y limpieza del vector. Es una prueba pertinente del helper **bajo esas premisas**.

No usa structs/layouts, colas, resource phases, renderer, threading ni loader reales. En106 borra `pending` antes de simular eliminación de escena; **no prueba cancelación de solicitudes pendientes**. No ejecuta reentrada anidada, descendientes reales, transición entre frames, fallo tras encolar o que create completó. Esta auditoría lo inspeccionó sin ejecutar g++/script. D2 reporta prueba in-game, pero tampoco valida DEVF 2.0.3 Windows/DX12. Próximos gates: [NEXT_VALIDATION_GATES](NEXT_VALIDATION_GATES.md).
