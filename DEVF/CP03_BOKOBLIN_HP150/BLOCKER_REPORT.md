# Bloqueo material CP03

**BLOCKED_WITH_EVIDENCE**: faltan una operación HP autorizada por instancia y, para el camino StageService probado, una correlación pública entre edición y ActorId/instancia lista. No falta acceso a SDK, GitHub, MSVC o un ARC de ubicación. Repetir un build de CP02 no resolvería este contrato.

## Firmas y límites concretos

- `StageService::add_actor(ModContext*,const char*,uint8_t,int8_t,const void*,size_t,StageActorHandle*)` devuelve el handle del registro almacenado. `register_edit` incrementa `s_nextHandle` y guarda owner/seq/record (stage.cpp 158–165); no recibe ActorId del engine. `stage_add_actor` copia el payload (189–197). La creación posterior no retorna identidad al mod (d_stage.cpp 1635–1662, 2611–2635). No es válido convertir ese handle a ID o pointer mediante un cast.
- `ActorService::create_actor(ModContext*,ProfileName,const ActorSpawnParams*,ActorId*)` sí devuelve ID de una solicitud de creación. El parámetro `int (*create_function)(void*)` existe, pero no cambia HP por sí mismo y no se aplica al stage edit existente. `get_actor_id(ModContext*,ProfileName,ActorId*)` usa SearchByName, sin un owner/token de StageService.
- `GameService` solo contiene ServiceHeader. `ConfigService::set_int(ModContext*,ConfigVarHandle,int64_t)` modifica una variable de configuración propia, sin puente con E_OC. `ActorProfileDesc` exige callbacks create/delete/execute/is_delete/draw; no ofrece herencia de perfil nativo con overrides declarativos.
- El header de GameABI expone `s16 field_0x560; s16 health;` en `fopAc_ac_c`. Poder compilar una asignación a estos datos no la convierte en un setter documentado de salud ni en una escritura autorizada por R8. Los comentarios 0x560/0x562 son anotaciones del source; **no se usan como offsets Windows x64**.

Las citas con commit, líneas y hashes completos están en [FEASIBILITY_GATE.md](FEASIBILITY_GATE.md) y [source-provenance.json](evidence/source-provenance.json).

El bloqueo no depende de interpretar toda escritura tipada como arbitraria. Incluso si una autorización posterior acepta la asignación a la instancia entregada por la callback, falta acreditar su ciclo de vida. ActorService no ofrece cancelación de solicitud pendiente por ActorId: `delete_actor` busca un actor mediante SearchByID y retorna MOD_OK si no aparece (actor.cpp 309–318), sin cancelar esa solicitud. El engine sí tiene `fpcCtRq_Cancel(create_request*)`, pero exige una referencia a su estructura interna y puede devolver FALSE si la eliminación no termina (create_req.cpp 61–74); no es una cancelación pública por el ID devuelto por ActorService. `fpcM_IsCreating(id)` solo consulta. No se obtuvo un contrato para revocar la callback o mantener la DLL cargada mientras la solicitud persiste. Esto es una limitación concreta de la alternativa nueva; no una repetición de la auditoría histórica de perfiles G5.

Se reutilizó la revisión histórica `DEVF/CP01_OFFICIAL_ARCHITECTURE/FEASIBILITY_MATRIX.md` y `ROUTES_AND_CONTRACTS.md`: su clasificación de vida por instancia como PARTIAL describe campos del GameABI y oportunidades de adaptación, no un setter de servicio ni una garantía de identidad, momento o lifetime. No habilita una escritura ahora prohibida por R8. Los documentos previos no incorporan una adaptación HM a E_OC 2.0.3 que cierre esas garantías; no se reabrió HM/Bars/Magic de 1.3.1 ni se investigó otra versión.

## Salud efectiva y daño: alcance semántico

`daE_OC_c::create` interpreta todos los bytes de parameters: modo, selector de búsqueda, defeated switch y field_0x6e1. Los bytes de angle.x controlan rango y archivo E_OC/E_OC2 (2706–2738). Al completarse ambas cargas, siempre elige la pareja 40 o 220 (2771–2779), sin lectura de HP configurable desde ACTR, ConfigService o modelo. Cambiar un parámetro no introduce un valor 150.

`health` es el campo que consume el combate: `damage_check` llama `cc_at_check` (756) y evalúa health ≤ 1 (764); `cc_at_check` resta AttackPower y limita a 0 (d_cc_uty.cpp 441–448). También existen ramas nativas health=0 y compensaciones de suma/resta (E_OC 638–780); contar golpes no mide de forma unívoca el HP inicial. La interpretación de SetAtAtp 2 no implica daño 2× medido.

`field_0x560` se inicializa junto con health; no se encontró una lectura de ese campo en los archivos E_OC/create/damage ni en d_cc_uty revisados. **Su semántica como HP máximo no queda acreditada** por el nombre ni por la asignación. Una futura adaptación debe decidir con evidencia si basta health o requiere mantener la pareja coherente. El informe no inventa un límite, setter ni protocolo de medición.

Hipótesis descartadas: reetiquetar E_OC2, configurar 150 sin consumidor, codificar 150 en angle.x, cambiar HIO/global, adoptar el primer E_OC o el más cercano, convertir StageActorHandle, interceptar creación mediante hooks y replicar/delegar métodos nativos con un perfil nuevo. Las primeras no aplican 150; las restantes vulneran aislamiento o restricciones. No se hicieron escrituras de prueba ni inspección de memoria real.

## Opciones condicionadas, ordenadas por cambios necesarios

| Opción | Cambio de decisión necesario | Lo que aporta y coste/pendientes |
|---|---|---|
| 1. Adaptación tipada de una solicitud ActorService propia en su post-creación oficial | Autorizar explícitamente una escritura única de health del actor recién creado y exclusivamente correlacionado (excepción acotada R8); aceptar creación directa por ActorService en lugar del stage edit CP02. | Es el camino más pequeño aparente: la callback recibe ESA instancia tras native create, sin hook ni cambiar perfil E_OC/global. **Viabilidad completa NOT_VERIFIED**, sin aprobación implícita. Antes de implementarlo deben cerrarse disponibilidad real de stage/room/layer al crear, aplicación única, errores/cancelación/recarga, coherencia de field_0x560 y vida útil de la callback hasta completarse/cancelarse. En actor.cpp 220–236 el ctx no se usa para registrar propiedad de la solicitud; la API no expone un handle cancelable o bloqueo de unload de esa callback. No basta prohibir hot reload en una guía para demostrarlo. No se reabre ahora G5 ni la auditoría de perfiles. |
| 2. Contrato oficial ampliado en una futura versión del host/SDK | Permitir una versión/host distinto y desarrollo upstream (cambiar R6 y el pin 2.0.3), fuera de esta tarea. | Conservar StageService, pero añadir correlación opaca owner/edit→instancia y un override inicial validado/copiado por el host. Aplicar 150 tras las cargas/selección nativa, antes del primer Execute, sin retener pointer o callback de DLL; permitir lectura verificable para prueba humana. Este es un diseño propuesto, **no una API existente**. Exige host nuevo, contrato de ciclo de vida, pruebas y distribución; rompe el requisito de ejecutable oficial intacto 2.0.3. |

No se propone un perfil propio que copie E_OC: carece de una ventaja compatible con el contrato y su coste sería una nueva implementación completa. Mantener 2.0.3 intacto y R8 sin excepciones deja únicamente 40/220 nativos, lo que **no cumple 150**.

**Decisión mínima posterior:** mantener el bloqueo, o autorizar una investigación acotada de la opción 1 con la excepción de escritura tipada y creación directa. Esa autorización por sí sola no concede GO: la siguiente revisión tendría que resolver los pendientes de identidad, contexto y lifetime antes de generar un mod. Si no es posible garantizarlos en 2.0.3, la opción 2 requeriría cambiar el objetivo de compatibilidad. Ninguna opción se implementó en esta ejecución.

## Estados separados

| Evidencia | Estado |
|---|---|
| Root 40457c6, Aurora 3227d76, manifest CP02 y 52 entradas del ledger | PASS estático; comprobado de nuevo para recuperación |
| Callback post-creación ActorService y ausencia de esa callback en StageService | PASS estático de lectura de fuente; runtime NOT_TESTED |
| Setter 150 por instancia en las superficies autorizadas | BLOCKED |
| Identidad StageActorHandle→ActorId | NOT_VERIFIED; no contrato público encontrado en la ruta revisada |
| Nueva implementación, tests fake, Windows build, PE, .dusk y descarga CP03 | NOT_RUN_GATE_BLOCKED; ninguno generado |
| HP 150, render, combate y retirada CP03 dentro del juego | NOT_TESTED; HP numérico NOT_VERIFIED |
| CP01/CP02 aparición, comportamiento y retirada | USER_REPORTED_RUNTIME_PASS; sin ejecución de Codex ni lectura del nuevo log CP02 |
| CP02 220 HP o multiplicador de daño en runtime | NOT_VERIFIED; sin medición humana reportada |
| Gate CP03 / avance CP04 | NO-GO / NOT_AUTHORIZED |

No se emite protocolo de instalación: no existe un paquete CP03 técnicamente justificado. CP01/CP02, sus tags, PRs y artefactos siguen preservados.
