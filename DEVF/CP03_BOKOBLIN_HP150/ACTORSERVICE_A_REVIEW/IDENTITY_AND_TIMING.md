# A0 primero: identidad, contexto y momento

Fuente fija 40457c6; referencias C01–C06/C09–C11 en [source-references.json](evidence/source-references.json). Se reutilizan alias, selector E_OC2, ubicación y análisis de recursos/terreno de CP02 sin repetirlos.

## ActorId y readiness

ActorService pasa el descriptor a `fopAcM_create`, que solicita `fpcSCtRq_Request` en `fpcLy_CurrentLayer`. El ID se genera en `fpcCtRq_Create`; luego `fpcBs_Create` lo asigna al proceso. No hay conversión StageActorHandle→ActorId. El allocator usa un contador estático que incrementa: no recicla IDs por cada muerte/fallo normal. No ofrece una garantía de generación para overflow/reinicio; no se conserva identidad entre sesiones o generaciones del mod (C01/C02).

**Distinción nueva:** `fopAcM_SearchByID(id)` inline itera la cola de actores sin consultar `fpcM_IsCreating`. `fopAc_Create` incorpora el actor a esa cola antes de llamar a native create. ActorService emplea precisamente esa búsqueda simple. Su `get_actor_room_num` puede tener éxito en creación parcial; no demuestra que heap/modelo/colliders estén listos. El overload `fopAcM_SearchByID(id,&actor)` comprueba IsCreating y da pointer NULL mientras siga pendiente, aunque devuelve 1; por tanto ni su retorno 1 solo basta (C03).

Predicado conceptual más estricto para un futuro acceso — **no implementado ni suficiente para GO**:

- Conservar únicamente el ID que devolvió nuestra solicitud; nunca buscar por perfil/proximidad. Un latch de intento debe preceder la llamada, sin retries ni nuevo spawn al morir.
- `fpcM_IsCreating(id)==false` **y** búsqueda tipada de ese ID no nula. False solo puede significar también error, cancelación o inexistencia.
- En el mismo hilo/punto de simulación, validar ID, perfil nativo E_OC, room y estado ejecutable/no eliminación. `fpcEx_ToLineQ` fija init_state 2; delete lo mueve a 3. Los campos del GameABI ayudan a distinguir estados, pero no son un servicio de ownership ni garantizan contexto completo.
- No conservar pointer entre updates; soltar ID al terminal, pérdida de contexto o generación. Tras aplicación única, no volver a escribir HP, ni rearmar por daño o muerte. El problema de cancelar un ID aún pendiente no queda resuelto por descartarlo localmente.

No hay una carrera multihilo demostrada entre estas consultas en la ruta síncrona del main loop. No se presume que cualquier callback/worker tenga el mismo contrato; no se acepta invocar desde un hilo creado por el mod. El principal hueco aquí es estado/fase, no una supuesta carrera ya observada.

## Contexto de solicitud y recursos

`ActorSpawnParams` ofrece room, parameters, position, angle y scale, sin stage ni capa de datos. La capa de scheduling capturada por `fpcLy_CurrentLayer` no es el layer 6 del DZR. `room_num=3` se copia a home/current, pero no selecciona automáticamente F_SP121/layer 6 ni mueve la solicitud a la capa de procesos de esa sala (C09).

Existe base tipada para leer `dComIfGp_getStartStageName`, `dComIfGp_roomControl_getStayNo`, `dComIfG_play_c::getLayerNo(0)` y los IDs de procesos stage/room. getLayerNo calcula la capa efectiva usando stay room o fallback start room. StartStageRoom es el room de entrada, no una prueba de habitación actual. Deben existir escena/sala activas y datos cargados, sin transición; un getter con valor 3/6 no acredita toda esa conjunción. La pareja stage/room/layer debe mantenerse hasta terminar create o abortarse la solicitud; no hay transacción pública que la fije para ActorService.

La ruta nativa comprueba FileList/switches de sala y puede rechazar enemigos; E_OC carga E_OC2 y E_ocb mediante fases, con posible error heap. CP02 humano acredita la ubicación y recursos para stage-load, no la creación directa desde un update ni disponibilidad en todos los instantes (C04/C09). No se fuerzan assets, flags, escenas ni capas. G2 sigue NOT_VERIFIED.

## Orden exacto: ventana 220 en A0

En una iteración ordinaria de Windows/TARGET_PC (C05):

1. `fapGm_Execute` llama `duskExecute`; este invoca ModLoader::tick → mod_update.
2. Después llama `fpcM_Management`: delete/priority → create-handler → preExecute → execute → draw.
3. Si nuestra solicitud termina en create-handler, E_OC2 asigna `field_0x560=health=220`, llama a Execute dentro de create y retorna COMPLETE.
4. PostMethod NULL no ejecuta código del mod. Se incorpora el proceso a execute queue; puede ejecutarse y dibujarse en esta iteración, antes del próximo mod_update.
5. Solo en el siguiente tick del mod se podría reconocer completion y aplicar 150 conceptualmente. Si creación/simulación está pausada, la espera puede durar más; no se garantiza un deadline.

La primera acción nativa llama damage_check y registra colisiones. No afirmamos un golpe real en el fotograma inicial. La fuente tampoco ofrece al mod un gate que pruebe «ningún daño/combate entre create y mi próxima escritura». Escribir 150 si health ya bajó podría regenerar vida; comprobar solo health==220 no demostraría identidad ni ausencia de otros cambios. A0 no acredita G3. Hacer busy-wait en mod_update impediría avanzar el create que ocurre después; llamar manualmente create-handler/Execute cambiaría el control global y no está permitido.

## health y field_0x560

La documentación oficial 126–127 sí incluye lectura/escritura de campos por mods nativos. El soporte técnico de GameABI no reemplaza la autorización del usuario: aquí únicamente se evalúa la operación conceptual. Una eventual excepción debe permitir **una sola asignación tipada de `health=150` al actor de esa solicitud**, validado y listo antes del daño; ninguna escritura a otros actores, HIO, perfil, health por frame o offsets (C06/C10).

health es s16 y 150 está en rango. El source inicializa field_0x560 conjuntamente, pero no lo usa en los métodos E_OC ni en cc_at_check revisados. Eso no demuestra semántica global «máximo HP»; no se propone escribirlo. Acreditar salud actual 150 posteriormente no sería probar salud inicial 150 ni ausencia de una ventana 220 (C06).

## Observabilidad futura, sin prototipo

DESIGN-PROPOSAL (C11): correlacionar REQUEST_SUBMITTED con ID devuelto y una generación del mod; READY solo cuando el predicado autorizado se cumpla; HP_APPLIED solo tras operación real, con valor previo/posterior leído y una vez. Registrar error/cancelado/room change y completitud de cleanup. Nunca logs por frame, nombre/manifest 150 como prueba, o identificar ActorId usando el primer E_OC. La medición numérica 150 runtime y el comportamiento/retirada seguirían pendientes de un log/prueba humana autorizados. No se prescribe instalación de un paquete inexistente.
