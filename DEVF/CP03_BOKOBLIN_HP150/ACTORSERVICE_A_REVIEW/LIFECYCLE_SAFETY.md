# Lifetime específico de A0/A1

Referencias C03/C07/C08 en [source-references.json](evidence/source-references.json). No se repiten las auditorías de perfiles personalizados ni se modifica el host.

## Secuencia real del loader

`deactivate_mod` ejecuta modules_mod_deactivating → mod_shutdown **solo si initialized** → quita servicios publicados → modules_mod_detached → unload_native; después baja active/enabledApplied. Un retorno de error o excepción de shutdown se registra, pero no veta el unload (loader.cpp 296–338).

**Descarga diferida, no lease de actor:** `unload_native` mueve la imagen a retiredNatives. `apply_pending_requests` del próximo tick drena esas imágenes antes de procesar nuevos eventos; `NativeModule` termina llamando FreeLibrary en Windows. La espera protege código todavía en el stack del tick anterior, no garantiza que create_function de una petición haya concluido. Shutdown global también drena las imágenes (natives.cpp 563–583; loader.cpp 1100–1105/1268–1282; native_module.cpp 18–19/70–73).

ActorService registra ownership de perfiles propios, pero `create_actor` nativo no usa ctx para asociar una solicitud/ID a LoadedMod. actor_remove_mod solo recorre esos perfiles registrados. Para E_OC sin perfil nuevo, no hay un cleanup automático de solicitudes/actores poseídos por CP03 (actor.cpp 220–236/359–400).

## Precisión sobre delete_actor y cancelación

No debe interpretarse MOD_OK como «solicitud cancelada». Si no existe aún actor en la cola, `delete_actor` retorna MOD_OK sin tocar la petición. Si existe un actor parcial, la búsqueda inline sí puede devolverlo; `fopAcM_delete`→fpcDt_Delete puede terminar en fpcCt_Abort→fpcCtRq_Cancel. Es decir, **hay un abort indirecto posible tras materialización**, no una cancelación pública total de una solicitud (C03/C08).

Ese camino puede devolver MOD_UNAVAILABLE si no puede encolar/abortar; fpcDt_Delete devuelve 0 si la creación está en ejecución o se encuentra en state 3, y cancel puede fallar. Un borrado aceptado suele encolar destrucción nativa: no equivale a desaparecer/sincronizar todos los recursos en la misma llamada. No se accede a create_request por pointer, no se fuerzan timers/colas ni se cancela la capa completa que contiene otros actores.

## Matriz

| Situación | A0: NULL callback | A1: callback DLL | Resultado |
|---|---|---|---|
| Solicitud antes de actor/antes de cola | Ningún código del mod retenido; delete puede ser no-op y actor aparecer después de disable. | Además conserva dirección de DLL en create_post_method. | G6 BLOCKED; A1 G5 BLOCKED. |
| Actor parcial, recursos loading | Puede localizarse por ID, pero no listo para HP; delete puede abortar o ser rechazado. | Abort aceptado puede evitar callback, sin garantizar todos los casos/tiempos. | Sin confirmación total de cancelación por API. |
| Native create completado | Sin callback; código nativo ejecuta, HP pendiente hasta próximo update. | PostMethod recibe el proceso de esa petición; retorno 0 repite, retorno 1 avanza. | A0 G3 BLOCKED; A1 timing mejor pero lifetime sin contrato. |
| Native create falla/heap/resource error | Engine cancela/destruye por fase; IsCreating false sin actor no es READY. | Puede no alcanzar PostMethod; no confiar en callback para enterarse o limpiar estado. | SOURCE-VERIFIED rutas de error; runtime NOT_TESTED. |
| Inicialización del mod falla tras solicitar | Shutdown puede omitirse si initialized false; no ownership automático de ID nativo. | Posible puntero pendiente sin shutdown; descarga sigue. | Ambas rutas sin cleanup total. |
| Disable/hot reload / fallo de update | Mod deja de actualizar; nativo puede sobrevivir pendiente/vivo. Nueva DLL puede solicitar otro al resetear estado. | Dirección antigua puede sobrevivir en petición y ser invocada tras drenaje. | No política «no hot reload» ni error de shutdown cierran esto. |
| Cambio de sala/escena | La cancelación nativa por capas puede ocurrir si la petición pertenece a esa capa; room 3 no prueba propiedad de su capa de procesos. | Posible abort nativo, sin vinculación a la vida del mod. | Contexto/cleanup NOT_VERIFIED, no garantía universal. |
| Muerte/destrucción temprana | No guardar pointer; invalidar ID terminal y no respawn. Destrucción es nativa. | La muerte tras callback no deja callback per frame, pero no resuelve pending/errores anteriores. | Diseño plausible, sin GO global. |
| Shutdown global limpio | No callback mod; host/nativo pueden completar eliminación normal del juego. | Drenaje DLL no es prueba de todas las peticiones resueltas. | No inferir seguridad de disable a partir de cierre limpio. |

A0 resuelve específicamente **G5 de código de DLL pendiente**. No se exagera: un E_OC nativo que permanezca no implica callback colgante ni use-after-free de DLL. La continuidad del actor después de desactivar sigue vulnerando el cleanup requerido. A1 añade un riesgo de llamada tardía real por fuente; no se afirma que haya ocurrido un crash runtime.

## Ampliación upstream mínima (solo propuesta)

Para cerrar la ruta sin callbacks: (1) crear una solicitud nativa propiedad de ModContext en contexto stage/room/layer validado; (2) token opaco con estado pending/ready/failed/gone y cancelación por token, idempotente, confirmada antes de unload, incluso antes de asignar actor; (3) aplicar una configuración HP inicial copiada por host, a esa solicitud únicamente, después de selección/cargas nativas y antes de la primera acción/combate; (4) eliminar/cancelar solo esa instancia al detach y ofrecer lectura de estado/HP para observabilidad. El host no debe retener un pointer a datos/código del mod para el override.

Esto es **DESIGN-PROPOSAL**, no API de 2.0.3. Exigiría autorización distinta, cambio de host/SDK/versionado y pruebas, incompatibles con ejecutable oficial intacto actual. No se implementa, no se parchea, no se entrega un plan de prototipo CP03 mientras el gate siga BLOCKED.
