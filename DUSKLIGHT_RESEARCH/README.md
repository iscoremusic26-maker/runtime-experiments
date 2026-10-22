# Atlas técnico general de Dusklight 2.0.3 para mods .dusk

Fuente fijada: `40457c6adb381928e4b5fef6ed459ed291edd5e2` (`v2.0.3`); objetivo Windows x64 / DirectX 12 / GZ2E01 USA. **CP-R35: Consola host fija,rate y ownership UI; sin mod objetivo.** La cobertura es selectiva y se declara por sistema, sin afirmar comprensión completa del juego.

## Acceso rápido

- [Continuación exacta](CONTINUATION.md), [cobertura real](RESEARCH_COVERAGE.md), [métricas](RESEARCH_METRICS.json) y [checkpoints](CHANGELOG.md).
- [Arquitectura y tick](ARCHITECTURE.md), [SDK y 25 servicios](SDK_AND_SERVICES.md), [hooks/ABI](HOOKING_AND_ABI.md), [matriz de integración .dusk](DUSK_INTEGRATION_MATRIX.md) y [dependencias](SYSTEM_DEPENDENCIES.md).
- [Índice de sistemas](SYSTEM_INDEX.json), [306 registros de símbolos](SYMBOL_INDEX.json), [318 evidencias](EVIDENCE_LEDGER.json) y [validación de referencias](VALIDATION_REPORT.json).
- [Riesgos](RISK_REGISTER.md), [preguntas pendientes](OPEN_QUESTIONS.md) y [hallazgos históricos reutilizables](PRIOR_RESEARCH.md).
- [Pin y excepciones](SOURCE_PIN.md), [inventario R00](INVENTORY.md), [archivos](FILE_INVENTORY.tsv), [directorios](DIRECTORY_INDEX.tsv) y [siete erratas de clasificación](INVENTORY_ERRATA.json). El inventario original se conserva; no se duplica.

## Fichas por sistema

| Área | Informes |
| --- | --- |
| Ejecución y ownership | [Runtime/loader](systems/runtime_and_lifecycle.md), [memoria/heaps](systems/memory_ownership.md), [cancelación de callbacks](systems/callback_ownership_and_cancellation.md) |
| Jugador y mundo | [Jugador/controles](systems/player_and_controls.md), [física/colisión](systems/movement_physics_collision.md), [combate](systems/combat_damage.md), [actores/IA/NPC](systems/actors_ai_npcs.md), [stages/salas/capas](systems/stages_rooms_layers.md) |
| Estado y narrativa | [Inventario/equipamiento](systems/inventory_equipment.md), [flags/eventos/progreso](systems/flags_events_progression.md), [save/load](systems/save_load.md), [secuencias/diálogos](systems/cutscenes_dialogue.md) |
| Presentación | [Recursos/ARC/overlays](systems/resources_archives_overlays.md), [cámaras/render](systems/cameras_rendering.md), [modelos/animación/materiales](systems/models_animations_materials.md), [HUD/UI/texto](systems/hud_ui_text.md), [audio/partículas](systems/audio_particles_effects.md), [entorno/clima/tiempo](systems/environment_weather_time.md) |
| Rutas menos comunes | [Caballo, canoa, Midna, pesca, ganado, puzzles y pendientes](systems/other_systems.md) |

## Cómo usarlo

Partir del sistema o símbolo, leer sus condiciones y evidence_ids, abrir el ledger y seguir el enlace permanente al SHA/rango. Las clasificaciones OFFICIAL_SERVICE/TYPED_HOOK/etc. describen mecanismos; no prueban resolución o instalación de un target Windows. READ y CROSSCHECKED se refieren a rutas citadas; los 19367 archivos inventariados no son archivos comprendidos.

Los 26 candidatos de módulo incluyen dos versiones de UiService y dependen de disponibilidad; las 209 ranuras públicas no fueron auditadas una por una. No se ejecutó el juego ni se verificó el backend DX12. Cuatro submódulos faltan; el histórico CI conserva su procedencia y no se promueve a runtime.

Mantenimiento: [AGENTS.md](AGENTS.md). Validación editorial: `python DUSKLIGHT_RESEARCH/tools/validate_atlas.py RUTA_FUENTE_CERTIFICADA`. Esta utilidad comprueba JSON, IDs, relaciones, enlaces relativos y rangos disponibles; no ejecuta el juego ni certifica compatibilidad binaria.

**NO MOD IMPLEMENTED / NO GAME RUNTIME CLAIMED / NO PRODUCTION MODIFIED.** Sin PR nuevo, merge, tag ni release. No hay ejecución de fondo.

Soporte PC: [logros internos, señales y persistencia](systems/port_achievements.md), con cobertura parcial del soporte general.

Soporte adicional: [Speedrun/LiveSplit,contador y conexión](systems/port_speedrun_livesplit.md),con límites del backend ausente.

Soporte adicional: [presencia del port, gates y lifecycle](systems/port_presence.md), sin conexión externa ni backend certificado.

Soporte adicional: [comandos host,parser y lifecycle de consola](systems/port_commands.md),sin ejecución ni CommandService público acreditado.
