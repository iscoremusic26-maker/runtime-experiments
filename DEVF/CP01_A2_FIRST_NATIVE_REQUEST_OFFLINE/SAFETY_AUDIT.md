# Auditoría de superficie experimental

El módulo **contiene creación** y el setter oficial. No es el observador READ_ONLY ni usa su identidad/paquete. Admission NONE bloquea el callback antes de mutación, pero no se distribuye este módulo como un producto desarmado ni se demuestra comportamiento runtime cargándolo.

Host2.2/Log1/Game2 + Actor1.0 reales. Metadata ABI1; exactamente cinco exports mod_ctx/mod_meta/mod_initialize/mod_update/mod_shutdown; no hooks/exported services. Create indirecto por slot32 y get_actor_room_num slot64 del ActorService80. ABI verificada en headers oficiales, sin sizeof del opaco ModContext.

Los imports del juego conservan la superficie G4B revisada y añaden exclusivamente fpcLy_SetCurrentLayer y fpcCtIt_Judge. PE AMD64, modmeta y whitelist de bases revisadas; exports, dumpbin imports/headers/disasm y map se conservan como texto. El mapa verifica anchor y setter/visitor; el disassembly debe contener llamada indirecta slot32. La revisión estática es acotada al código y grafo compilados; no prueba seguridad general de toda la DLL o del motor.

Cero register/unregister, delete_actor, create_child_actor, create_actor_from_name, StageService, hooks, detours, forced room/load, flags/save writes, fpcCtRq_Cancel, fpcLy_Cancel, fopAcM_delete, cambios de host/perfiles/SDK/recursos. No workers, deferred callbacks propios ni archivos runtime. NativePresetcallbackNULL. Mutatorunits sin guardas históricas; puente separado con guardas intactas.

CI solo ejecuta nuevos EXE de laboratorio con Fake Backend; no carga la DLL ni inicia Dusklight. No utiliza add_mod ni mod.json y no hay target .dusk. Solo se sube evidence/ con .log/.json saneados. Import library privada se extrae exactamente y se queda en runner temp. DLL/EXE/lib/ZIP originales no se publican ni se incluyen en el repo de código.

No lifetime lease/cancel seguro ni prueba de cleanup nativo. STOP conserva ID escalar e intento consumido, no altera actores. No garantía de descarga/reload durante una solicitud. Bloqueo custom-profile unloading independiente preservado. Identidad generacional y recursosGPU READY no acreditados. Cada límite se documenta en REQUEST_ID_AND_READINESS.
