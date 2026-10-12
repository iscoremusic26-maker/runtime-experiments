# G5 — criterios de una autorización futura

**NO_GO. No `.dusk` activo ni llamada StageService::add_actor en esta tarea.** El preflight proporciona herramientas/contexto, no una autorización automática por compilar. G3/G7 de A2 no se añaden como prerrequisitos.

Antes de proponer una sola aparición deben cerrarse G0/G1/G2/G4 para **E_OC normal**, recursos y punto concreto: contexto oficial Windows/DX12 estable, perfil/argumento/params y angle.x acreditados, suelo/envolvente/arma/movimiento sin conflictos, switches/eventos/entrada/salida seguros, y baseline completo. Además, nueva autorización explícita y paquete TEST independiente revisado con reversión. El observador actual no conoce ActorId de una adición inexistente.

| Comprobación futura | Preparación disponible | Evidencia requerida en G5/G6 |
|---|---|---|
| Una sola definición Add | Arquitectura A1 y preset documental; no registro implementado | Una entrada antes de carga natural; handle registrado una vez, sin A2 paralela ni reenable |
| Perfil y recursos | E_oc/0x1FE/-1, E_OC/E_ocb; phase/heap/Execute nativos | Create completo y recursos/modelos realmente disponibles, sin inferirlo solo de IsCreating=false |
| Owner y posición | Distinción room/layer lógico/current/room child; punto todavía pendiente | Actor observado en owner de ROOM_SCENE verificado, no root, XYZ/yaw aprobados y contacto/colisión/render reales |
| Identidad sin afectar vanilla | Siete registros authored y censo read-only con IDs/copias | Preservar originales, correlacionar antes/después y única adición; no asignar ownership por primer match/perfil/posición solamente. Ambigüedad bloquea ensayo |
| Render y comportamiento | Contratos de modelo/arma/colliders; no doble dibujado manual | Link y enemigo visibles, sin doble draw, comportamiento básico, sin interferir eventos/progreso |
| Duplicados/recarga | Retirar definición no mata instancia; recarga puede ejecutar Add otra vez | Cantidad/IDs distinguibles en cada carga, evitar reenable/recargas que produzcan duplicados no atribuibles |
| Cambio de sala/stage | Secuencia natural por acreditar en G2 | Lifetime del actor, descendientes/efectos y propietarios observados en transición real |
| Retiro en carga posterior | StageActorHandle distinto de ActorId; no auto-kill | Definición retirada, ausencia de reaparición en siguiente carga; no exigir desaparición inmediata en sala residente |
| Cleanup | Delete nativo documentado, sin callback del mod en el actor | Sin huérfanos ni pendientes tras salida real; recursos/colliders/descendientes limpiados con evidencia, no con un stub |

Se detiene inmediatamente ante identificación ambigua, actor root, recursos incompletos, carga pendiente, duplicados, Link invisible, doble draw, colisión anómala o progreso/eventos inesperados. No se amplía el caso, no se mata un match vanilla, no se parchea host ni se compensa con flags. Evitar combate/muerte en la primera secuencia; el preset no elimina efectos nativos de DISAPPEAR/recompensas.

Recuperación futura: preservar logs/identidad, cerrar proceso, retirar solo el TEST autorizado antes del siguiente arranque. No modificar originales ni confiar en remove-edit para eliminar la instancia existente o en shutdown fallido para impedir unload. No hot reload, custom profiles, callbacks nativos del mod ni setters A2. El bloqueo independiente de descarga DLL sigue BLOCKED; CP02 NO_GO.
