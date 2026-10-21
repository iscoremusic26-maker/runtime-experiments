# Continuidad — CP-R17

Rama research/dusklight-203-dusk-atlas en iscoremusic26-maker/Mods-Duskligh; escritura solo DUSKLIGHT_RESEARCH. Upstream 40457c6adb381928e4b5fef6ed459ed291edd5e2,árbol e4b79b565b2842f711f7c9f2390f56ef11063157; Windows x64/DX12/GZ2E01 USA. Padre verificado 904e7f1d59e09752fa418e5a7b6dc79cc299a540; consultar HEAD para SHA propio.

## Resultado y alcance

CP-R14 swpush PLAYER-035..039; CP-R15 KYTAG06/paletas/fog PRES-048..051; CP-R16 retry sidecar/caché WORLD-034..037 y corrección de clasificación save_slot_written. CP-R17 completo en audio_particles_effects,PRES-052..055,tres símbolos BST. FrameEnd llama WSYS; única sync BST localizada entra por lifecycleApplied (init/requests). Retiro no marca dirty ni publica mapa; consumidor SE captura shared_ptr. Edición posterior a init sin nuevo lifecycle puede diferirse (inferencia condicionada). Q-08 parcial,no bug/audio runtime probado. Cadenas nuevas de esta continuación:4;sin promoción global,documentos nuevos0.

Baseline de esta continuación CP-R13 36c71128be0cda32b4ee5ef30dd0ace49ff92404:220 evidencias,232 símbolos,21 fichas,48 archivos. Actual:237 evidencias,246 símbolos,21 fichas,48 archivos. Neto:+17 evidencias,+14 símbolos,+0 documentos. Checkpoints de esta continuación:CP-R14, CP-R15, CP-R16, CP-R17. No repetir campañas anteriores:CP-R10 escenas,11 AutoMata,12 Message,13 LiveSplit; seguir CHANGELOG y evidencias.

28 entradas canónicas:18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED. Las cadenas nuevas son muestras,ninguna promoción global. Inventario R00 y siete erratas intactos. Cuatro submódulos ausentes,diferencia Android y falta de ABI/export/runtime Windows mantienen límites. Duración N/D,no sumar sesiones/pausas ni CPU ficticia.

## Primera acción exacta siguiente

CP-R18: alternar Q-03 ActorService con creación pendiente. Leer actors_ai_npcs/runtime y HOOK-029,PLAYER-019..023 sin repetir advertencia general. En src/dusk/mods/svc/actor.cpp localizar unregister_actor y seguir recuento/borrado de instancias frente a solicitudes de creación aún en cola; verificar funciones reales con rg antes de seguir profile registry/f_pc. Delimitar qué conserva al retornar UNAVAILABLE y qué hace detach posterior,con una ruta de creación pendiente. Sin implementar actor ni inducir unload.

Antes de nueva función: consultar ficha,ledger y símbolo actuales. OPEN_QUESTIONS tiene prioridad. Si ya cubierto en nuevo HEAD,saltar a otro hueco; no repetir inventario/scheduler/fonts/AutoMata/Item/Message/LiveSplit ni implementar mods.

## Reproducibilidad y operación

Rutas efímeras:work/source/dusklight-2.0.3 certificada y work/atlas/DUSKLIGHT_RESEARCH solo si existen. Leer SOURCE_PIN/AGENTS/HEAD remoto. Comando revisado: `python work/atlas/DUSKLIGHT_RESEARCH/tools/validate_atlas.py work/source/dusklight-2.0.3`. Solo escribe VALIDATION_REPORT en atlas; fallo bloquea publicación. Valida JSON,IDs,relaciones,enlaces y rangos; no semántica,ABI,exports,build o runtime.

Diff exclusivo DUSKLIGHT_RESEARCH; HEAD/tree/padre actuales,expected_sha sin force,verificar ref y archivos remotos. Reconciliar concurrencia antes de escribir. No subir INVENTORY_SUMMARY/tools/inventory.py locales divergentes de R00. Checkpoint breve antes de otra lectura extensa.

Sin fuente/SDK/EXE/ROM/assets/saves/configuración ni producción/otros proyectos. Sin PR80/81,CI65/66,PR nuevo,issue,merge,release,tag o force. No prompts,fuentes completas ni datos personales en commits. NO MOD IMPLEMENTED / NO BUILD PERFORMED / NO GAME RUNTIME CLAIMED / NO PRODUCTION MODIFIED. Sin trabajo de fondo.
