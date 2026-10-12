# Integración incremental — contratos efectivos del árbol completo

Esta revisión contrasta el parche conservado con sus consumidores reales. No sustituye las auditorías anteriores ni declara seguridad runtime. Las referencias de líneas corresponden al checkout exacto 40457c6 después de aplicar el parche de eea4742.

## Interfaces y ownership

- standard_create_request_class existe únicamente en src/f_pc/f_pc_stdcreate_req.cpp. El nuevo mod_owner pertenece a TARGET_PC y sizeof() en fpcSCtRq_Request determina su reserva. No se aplican offsets PPC de los comentarios a Windows x64. Todos los consumidores del árbol completo se recompilan juntos; el layout nativo se medirá en la prueba dirigida.
- LoadedMod, ActorSlot y ServiceModule son layouts internos del host; el parche no modifica los layouts ni versiones del SDK público ActorService/StageService. No es ABI compatible con insertar bytes en un EXE original. Los in-tree mods/consumidores se construyen con el preset original.
- Las inicializaciones de los módulos usan designadores de miembros, incluidas las que omiten modDrained. Debe verificarse su compilación completa; omitir ese callback significa ausencia de prueba de drenado para el servicio, no una garantía añadida.
- El contexto sigue siendo propiedad de LoadedMod; la DLL, bundle y contexto se conservan juntos cuando deactivationPending o teardownPoisoned vetan el cierre. Las operaciones de reload/forget/uninstall propagan el veto antes de retirar ese ownership. El laboratorio previo conserva sus 25 PASS, con alcance sintético; aquí no se repite como certificación del host.
- La captura del dueño ocurre después de reservar/encolar pero antes de devolver fpcSCtRq_Request. No hay llamada a código de mod entre esas operaciones; la prueba presupone exclusivamente el hilo del motor. El perfil y el dueño solicitante se consultan por separado. Las solicitudes opacas bloquean conservadoramente.
- El predrenado conserva perfiles para mod_shutdown. Solo el detach posterior retira registros de Actor/Stage. El fallo del callback delete sigue siendo un fallo y no permite liberar el proceso como si hubiera éxito.

## Cola y fases reales

La prueba dirigida usa headers del checkout, el typedef estándar extraído sin transcribirlo, el escáner exacto y cuerpos efectivos de fpcCtRq_Cancel/Delete. Enlaza las TUs originales c_node/c_list/c_tree/c_tag/f_pc_create_tag/f_pc_method. Profile ownership, fase, capa, heap y proceso son adaptadores declarados; no ejecuta fpcCtRq_Handler completo, mounts o Dusklight.

Comportamientos que requieren distinguir:

1. fpcCtRq_Cancel fija is_cancel antes de intentar borrar el proceso. Si ese intento falla, la siguiente llamada devuelve TRUE aunque la solicitud siga en la cola. Comprobar la cola evita tomar ese retorno como una barrera.
2. fpcCtRq_Delete retira la solicitud antes de invocar delete_method. Si ese callback falla, queda memoria sin liberar fuera de la cola. El delete estándar del host devuelve siempre 1; extender la garantía a solicitudes arbitrarias o recursos de otros servicios sería incorrecto.
3. fpcDtTg_Do retira el tag antes del callback y lo reencola si devuelve 0. La retirada efectiva y el proceso deben comprobarse, no solamente un retorno del wrapper.
4. Los mounts y colisiones/J3D no participan en este laboratorio. Errores de carga, cancelaciones asíncronas, transiciones reales y destructores de los actores siguen NOT_TESTED.

## Riesgos graves que bloquean una prueba activa

**R1 — reentrancia durante el recorrido de destrucción (BLOCKED por revisión estática; prueba dirigida ampliada pendiente).** finish_delete_all_actors_of_name conserva NODE_GET_NEXT antes de llamar fpcDtTg_Do, que ejecuta código del mod. unregister_actor comprueba callbacks del perfil objetivo, no de los demás perfiles. Por ello un destructor de A puede desregistrar B, con otro perfil y sin callback propio pendiente. Ese cierre puede retirar/liberar el nodo B guardado como siguiente: la siguiente iteración desreferencia un puntero obsoleto. actor_drain_mod también guarda una lista de handles y desreferencia find(handle) sin revalidarlo después de callbacks anteriores; retirar B durante A puede invalidar ese handle. fpcBs_Delete libera el proceso si el método devuelve 1, por lo que el riesgo no se limita a una mutación inocua de una lista.

Se conserva el parche exacto para evaluar la integración y se bloquea su adopción; no se improvisa una corrección amplia ni se fuerza GO. Hace falta una barrera de mutaciones/reentrancia y una estrategia de recorrido que no conserve pointers/handles invalidables por callbacks, con pruebas de esos escenarios y recompilación afectada.

**R2 — teardown global fuera del loader (BLOCKED para garantía terminal).** src/m_Do/m_Do_main.cpp llama ModLoader::shutdown y después dusk::ui::shutdown incondicionalmente. La retención terminal del loader no controla ese cierre posterior ni el orden de destructores estáticos del resto del motor. Conservar LoadedMod/DLL no acredita que los registros, componentes o pointers externos sigan siendo válidos hasta el final. No se modifica ese orden sin una etapa específica y evidencia de integración/runtime.

**R3 — otros servicios y mods (NOT_VERIFIED).** Solo g_actorModule implementa modDrained. Las predeactivaciones/detaches legacy no adquieren automáticamente un contrato de callbacks, workers ni recursos por recompilar ServiceModule. No se declara compatibilidad general de HTTP/net/UI/hooks, runtimes delegados o mods con threads ajenos al hilo del motor.

StageService puede retirar sus registros futuros, pero no revierte modificaciones ya aplicadas a datos cargados ni demuestra cómo quedan las instancias en un cambio de escena. Tampoco prueba la ubicación candidata; los resultados previos se conservan sin nueva investigación.

## Condición de salida

PATCHED_HOST_BUILD_PASS acreditaría compilación/enlace del host modificado y PE AMD64; INTEGRATION_TEST_PASS solo las comprobaciones dirigidas descritas. Ninguno concede GO de seguridad del ciclo de vida. DEVF DISARMED_NO_REGISTRATION; CP02 NO-GO. Una prueba activa Windows/DX12 sigue bloqueada por R1/R2 y los requisitos runtime/ubicación documentados anteriormente.
