# Dependencias entre sistemas

Mapa de rutas seleccionadas del commit `40457c6adb381928e4b5fef6ed459ed291edd5e2`. Las flechas representan consumo de estado o una llamada observada en las evidencias citadas; no son un grafo exhaustivo de todos los includes ni una garantía de orden universal.

| Proveedor → consumidor | Qué cruza la frontera | Invariante o riesgo | Evidencia / ficha |
| --- | --- | --- | --- |
| Loader → servicios/otros mods | Contexto, exports, imports, orden de activación y retirada | Required import suspende consumidor si falta; optional necesita NULL check | HOOK-002/015/020; [runtime](systems/runtime_and_lifecycle.md) |
| Metadata/manifest → HookService | Target, firma declarada, trampoline y original slot | Un backend compartido por dirección no negocia firmas entre candidatos | HOOK-001..012/027/028; [ABI](HOOKING_AND_ABI.md) |
| Gestor de procesos → escena/actor | IDs, profile, fases de crear/ejecutar/borrar/draw | Crear es diferido; cleanup y callbacks deben terminar antes de unload | ARCH-001, HOOK-029; [actores](systems/actors_ai_npcs.md) |
| Recursos/room → StageService → actor | Bytes del registro, room/layer, nombre/profile, parámetros | Edición no equivale a entidad viva; retirar handle afecta aplicación futura | WORLD-001..005/033; [stages](systems/stages_rooms_layers.md) |
| Progreso/flags → stage/layer/NPC/evento | Banco activo, SaveTbl y condiciones narrativas | Banco persistente y copia activa pueden diferir; reglas por contexto | WORLD-007..009/016/017; [flags](systems/flags_events_progression.md) |
| Input/estado → Link → física/colisión | Stick, procedimiento, modo, velocidad/posición y resultados At/Tg | Cambiar solo ID/posición no reproduce transición ni posición final corregida | PLAYER-001..016; [jugador](systems/player_and_controls.md), [física](systems/movement_physics_collision.md) |
| Colisión → daño → eventos/audio/drops | Hit object, material/guardia, política de daño local y side effects | No hay un health/HP handler universal para jugador y todos los enemigos | PLAYER-014..019; [combate](systems/combat_damage.md) |
| ItemService → actor/evento/inventario | Solicitud en cola y entrega bajo estado aceptable | Detach no cancela evento de entrega que ya es dueño del trabajo | WORLD-018..022; [inventario](systems/inventory_equipment.md) |
| Flow/Message → diálogo/estado | Nodos, edges, queries, eventos y texto por idioma | Remove retira registros; no revierte flags ya escritos | WORLD-023..027; [narrativa](systems/cutscenes_dialogue.md) |
| Guardado vanilla → observers → sidecars | Slot activo, callback y flush de dirty mods | Confirmación vanilla no implica sidecar durable; no atomicidad conjunta observada | WORLD-010..014, CALLBACK-001; [save](systems/save_load.md) |
| Bundle/DVD/ARC → modelo/HUD/audio/entorno | Buffers, archive refcount y objetos decodificados | Reemplazo no reconstruye consumidor cacheado; lifetime de archive/heap manda | PRES-001..006/014..018; [recursos](systems/resources_archives_overlays.md) |
| Heap JKR/actor → modelos/animaciones | Heap actual por hilo, solid heap y allocations | Callback de heap puede repetirse; liberar con el allocator propietario | ROOT-001..006; [memoria](systems/memory_ownership.md) |
| Cámara/interpolación → Gfx/UI | Estado temporal de cámara, matrices y handles GPU prestados | Game thread y render worker tienen contratos distintos | PRES-007..018; [cámara/render](systems/cameras_rendering.md) |
| Reloj/clima/room → ambiente/audio/partículas | Daytime, tablas de color, weather y punteros de influencia | Controlador puede sobrescribir cambio puntual; influencia requiere storage vivo | PRES-027..034; [entorno](systems/environment_weather_time.md) |
| Save/Host/Camera → callback del mod | Callback, userData, ownership y snapshot del dispatch | Cancelación difiere según revalidación; no liberar userdata por analogía entre servicios | CALLBACK-001..004; [callbacks](systems/callback_ownership_and_cancellation.md) |

## Cobertura nominal restante

El [índice de directorios](DIRECTORY_INDEX.tsv) conserva todos los módulos del árbol principal y el [índice de sistemas](SYSTEM_INDEX.json) añade estado y límites. Las categorías de soporte no se consideran comprensión técnica: herramientas/build, documentación, PCH y auxiliares de juego, configuración/logging/achievements/Discord/LiveSplit del port, y submódulos externos siguen con profundidad nominal donde no hay ficha contrastada.

Los encabezados de recursos regionales localizan IDs; no son miles de implementaciones de subsistemas. Los cuatro gitlinks están fijados en [SOURCE_PIN](SOURCE_PIN.md), sin internals auditados. JSystem se sigue selectivamente en memoria/J3D/J2D/audio; bibliotecas de compatibilidad de consola, debugger stubs y dependencias transitivas no se confunden con gameplay investigado.

Para ampliar una arista: abrir la evidencia citada, confirmar proveedor y consumidor en el mismo SHA, seguir estado/error/cleanup, actualizar ledger y cobertura, y publicar un checkpoint antes de ampliar el siguiente flujo.
