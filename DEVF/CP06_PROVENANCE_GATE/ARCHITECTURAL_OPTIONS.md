# Decisión posterior: opciones verificables, no implementadas

## A. .dusk-only bajo la API actual
Se midió el punto register_edit, no sólo su nombre en fuente. Un hook de observación de sus referencias es plausible si se certifica el ABI; **no hay un accessor comprobado owner/handle→allocation**. No se presenta otra fábrica como solución ni se declara una vía .dusk-only lista.
Cualquier continuación de esta opción necesita aportar primero un punto nativo comprobable que exponga esa allocation con owner/handle sin layout privado, mutación, tokens nativos o emparejamiento por orden/bytes. Una compilación nueva de un fake no constituye ese input. Pros: preservaría EXE/SDK oficiales; contras: el contrato actual pierde la etiqueta y no hay puente demostrado. No se justifica enganchar allocators/memcpy globales.

## B. Extensión mínima StageService/SDK — SÓLO PROPUESTA
Requiere autorización explícita para trabajar sobre host/SDK y una build distinta; NO se implementa aquí ni se ofrece como mod compatible con EXE2.0.3 intacto.
Propuesta C ABI de observación por propietario, añadida al final de StageService con versión minor1 y prefix1.0 intacto, si la política de compatibilidad del host lo permite:
- suscripción por ModContext y StageActorHandle propio; handles de otro mod rechazados;
- evento con struct_size/version, edit_handle, actor_id de solicitud, generación de spawn, scene_epoch, stage/room/layer y fase (requested/ready/cancelled/failed/destroyed);
- asignar etiqueta dentro del host donde ActorEditRecord aún conserva owner+handle; propagar por el scope de creación REAL (no enumeración Link) hasta solicitud y proceso;
- READY antes del primer execute sólo si el orden nativo se comprueba; request!=actor creado; error/cancelación no admite;
- invalidación explícita en unload/reload/remove/detach, sin pointers STL ni LoadedMod expuestos; callbacks sólo del dueño, juego thread, desregistro/drenaje probado;
- quitar edición no borra actor vivo: destrucción/teardown y política de descarga fría siguen contratos separados, no promesa automática.

Nuevos mods exigirían StageService≥1.1 y host que lo soporte; en2.0.3 sin extensión deben rechazar/desarmar. Los mods1.0 conservan el prefix bajo verificación de compatibilidad, no se garantiza sin pruebas. No cambiar EXE del usuario ni sustituir baseline, no asumir que un SDK nuevo funciona con EXE antiguo.
Pros: conserva provenance exactamente donde existe; evita hooks de contenedores y claves falsas. Contras: implica host/SDK distintos, revisión upstream, lifecycle/ABI y mantenimiento; exige decisión de arquitectura y pruebas independientes.

## C. Mantener single-site actual
Sin autorización nueva ni cambios: conservar CP06 parcial v0.6.0, max1 y sitio1, dos presets alternativos por JSON en frío y rollback observado. Pros: conserva paquete humano probado. Contras: no satisface MVP multiinstancia/segundo sitio.
La tarea presente termina con checkpoint y evidencia; no requiere pruebas del usuario. **NO PROBAR NADA.**
