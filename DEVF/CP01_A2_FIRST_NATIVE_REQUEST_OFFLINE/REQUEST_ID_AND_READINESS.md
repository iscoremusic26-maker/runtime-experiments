# ID, fase y readiness

ActorId es uint32; ProfileName es int16; un handle custom uint64 no se usa. El SDK copia vectores del preset, llama `fopAcM_create(...,0xFFFF,...)` y devuelve MOD_ERROR para ID0xFFFFFFFF; MOD_OK significa solicitud encolada. `fpcCtRq_Create` asigna ID antes de existir un actor y lo conserva al crear el proceso.

## Estados y evidencia

| Estado | Evidencia exigida | Alcance |
|---|---|---|
| BLOCKED/REJECTED | Falta admisión o falla precheck | No request |
| ATTEMPT_CONSUMED | Latch antes del setter | No retry incluso si el servicio falla |
| REQUESTED | MOD_OK exacto, ID válido, scope restaurado y contexto coherente | No actor ready |
| PENDING | Cola/cabecera/fase incompleta o ausencia transitoria | Puede cargar recursos/asignar proceso |
| ACTOR_READY_OBSERVED | ID único, profileE_OC, sin IsCreating, init_state2, actorINIT, campos derivados válidos, SDKroom3 y ownerchild correcto | Inicialización observable; no render/resourceGPU READY |
| STOP_SESSION | Contexto abandonado, error, ambigüedad, desaparición, timeout, límite o shutdown | Terminal; no cancel/delete/retry |

El monitor busca exclusivamente el ID devuelto, nunca get_actor_id(profile). Recorre sincrónicamente la cola de solicitudes y la cola de actores con cap256 cada una. Solo copia cabecera del target hasta init2 y no IsCreating. El SDK de room usa internamente una búsqueda que no comprueba fase: se invoca **después** de una membresía única, completa y acotada con actorINIT y profile correcto. La room SDK debe coincidir con la lectura nativa. No se retienen préstamos. Los helpers oficiales IsCreating/scene search tienen sus propios recorridos internos; los caps limitan nuestros visitors, no prueban recuperación ante corrupción arbitraria de colas del host.

Se atribuye exactamente un create_count de la hija a nuestra solicitud pendiente; cero en parent, cero deletes, y cero child creates una vez completada. Una creación nativa adicional/ajena que rompa esto fuerza STOP, sin inferir que sea inocua. La retirada de la solicitud o el cambio de contexto no se reparan. REGISTERED E_OC/E_ocb es precondición parcial; jamás READY por ese motivo. No existe ni se inventa un flag RENDERED.

Timeout inicial120 polls/update callbacks, no segundos ni garantía de plazo del motor. Ausencia sin cola tiene gracia de3 polls (el cuarto STOP); la desaparición tras haber observado READY para inmediatamente. El seguimiento READY dura máximo60 polls satisfactorios; el61 detiene observación. No se reintenta al agotar ninguna ventana. Todos los límites están cubiertos por fakes, aún no calibrados runtime.

`src/f_pc/f_pc_base.cpp` usa contador signed int monotónico en flujo normal, sin generation handle. Se rechazan ID0,0xFFFFFFFF y zona de overflow `>=0x7FFFFFFE`. Duplicados, mismatches, queue disagreement, fase de eliminación y regresión observables paran. El flag reused del fake demuestra la respuesta a evidencia explícita de reciclaje, **no** un detector universal del backend: un reemplazo mismo-ID/mismo-perfil/owner entre polls, un reset de contador/hook externo o overflow previo no es detectable con estos contratos. No afirmar protección generacional completa. Esto limita un futuro piloto y requiere sesión fría controlada.

E_OC Create carga E_OC/E_ocb, crea heap y puede llamar su execute antes de nuestro primer READY. Ningún poll puede impedir esa interacción ni convertir STOP en rollback. Ante incertidumbre después de encolar se abandona la sesión de prueba mediante salida completa futura autorizada, sin pretender cancelar desde el mod.
