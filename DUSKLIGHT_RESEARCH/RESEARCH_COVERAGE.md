# Cobertura real — CP-R08

## Alcance y denominadores

Se conservan **19367 archivos y 488 directorios** del inventario CP-R00. Esta continuación no recalculó hashes ni reconstruyó ese inventario. Las siete erratas nominales se aplican desde INVENTORY_ERRATA.json, sin duplicar el TSV. Los encabezados regionales no se cuentan como implementaciones leídas.

Se publican **20 fichas de sistemas, 197 evidencias y 213 registros de símbolos**. El índice canónico tiene 28 entradas: 18 CROSSCHECKED selectivas, 6 READ y 4 exclusivamente INVENTARIED. Incluye SDK, soporte y evidencia histórica, por lo que no representa 28 sistemas gameplay independientes.

Los 25 contratos C del SDK se contrastaron con fronteras seleccionadas de implementación. Hay 26 candidatos de módulo (UiService 1.5 y 2.3), sujetos a disponibilidad; 209 ranuras públicas localizadas no equivalen a 209 métodos auditados. El índice de símbolos mezcla tablas/slots, tipos y funciones; no afirma haber seguido la cadena completa de llamadas de los 213 registros.

## Estado por área

| Sistema | Nivel | Alcance / informe |
| --- | --- | --- |
| `actors_ai_npcs` | CROSSCHECKED | [systems/actors_ai_npcs.md](systems/actors_ai_npcs.md) |
| `audio_particles_effects` | CROSSCHECKED | [systems/audio_particles_effects.md](systems/audio_particles_effects.md) |
| `cameras_rendering` | CROSSCHECKED | [systems/cameras_rendering.md](systems/cameras_rendering.md) |
| `cutscenes_dialogue` | CROSSCHECKED | [systems/cutscenes_dialogue.md](systems/cutscenes_dialogue.md) |
| `hooking_abi` | CROSSCHECKED | [HOOKING_AND_ABI.md](HOOKING_AND_ABI.md) |
| `hud_ui_text` | READ | [systems/hud_ui_text.md](systems/hud_ui_text.md) |
| `inventory_equipment` | CROSSCHECKED | [systems/inventory_equipment.md](systems/inventory_equipment.md) |
| `models_animations_materials` | READ | [systems/models_animations_materials.md](systems/models_animations_materials.md) |
| `resources_archives_overlays` | CROSSCHECKED | [systems/resources_archives_overlays.md](systems/resources_archives_overlays.md) |
| `runtime_and_lifecycle` | CROSSCHECKED | [systems/runtime_and_lifecycle.md](systems/runtime_and_lifecycle.md) |
| `save_load` | CROSSCHECKED | [systems/save_load.md](systems/save_load.md) |
| `sdk_services` | CROSSCHECKED | [SDK_AND_SERVICES.md](SDK_AND_SERVICES.md) |
| `stages_rooms_layers` | CROSSCHECKED | [systems/stages_rooms_layers.md](systems/stages_rooms_layers.md) |
| `flags_events_progression` | CROSSCHECKED | [systems/flags_events_progression.md](systems/flags_events_progression.md) |
| `movement_physics_collision` | CROSSCHECKED | [systems/movement_physics_collision.md](systems/movement_physics_collision.md) |
| `player_and_controls` | CROSSCHECKED | [systems/player_and_controls.md](systems/player_and_controls.md) |
| `combat_damage` | CROSSCHECKED | [systems/combat_damage.md](systems/combat_damage.md) |
| `other_systems` | READ | [systems/other_systems.md](systems/other_systems.md) |
| `environment_weather_time` | READ | [systems/environment_weather_time.md](systems/environment_weather_time.md) |
| `memory_ownership` | CROSSCHECKED | [systems/memory_ownership.md](systems/memory_ownership.md) |
| `platform_backend` | READ | [systems/memory_ownership.md](systems/memory_ownership.md) |
| `prior_research` | CROSSCHECKED | [PRIOR_RESEARCH.md](PRIOR_RESEARCH.md) |
| `callback_ownership_and_cancellation` | CROSSCHECKED | [systems/callback_ownership_and_cancellation.md](systems/callback_ownership_and_cancellation.md) |
| `build_tooling` | INVENTARIED | [SYSTEM_DEPENDENCIES.md](SYSTEM_DEPENDENCIES.md), [INVENTORY.md](INVENTORY.md) |
| `documentation` | INVENTARIED | [SYSTEM_DEPENDENCIES.md](SYSTEM_DEPENDENCIES.md), [INVENTORY.md](INVENTORY.md) |
| `game_support` | INVENTARIED | [SYSTEM_DEPENDENCIES.md](SYSTEM_DEPENDENCIES.md), [INVENTORY.md](INVENTORY.md) |
| `port_support` | READ | [SYSTEM_DEPENDENCIES.md](SYSTEM_DEPENDENCIES.md), [INVENTORY.md](INVENTORY.md) |
| `external_dependencies` | INVENTARIED | [SYSTEM_DEPENDENCIES.md](SYSTEM_DEPENDENCIES.md), [INVENTORY.md](INVENTORY.md) |

CROSSCHECKED: declaraciones/contrato, implementación y usos seleccionados contrastados con límites explícitos. READ: implementación consultada con flujo/dependencias todavía parciales. INVENTARIED: rutas localizadas; no prueba comprensión. Cada evidencia conserva su propio nivel y puede ser más limitado que una parte ya contrastada del mismo sistema.

## Calidad y límites

Se validan estructura JSON, unicidad, IDs cruzados, dependencias, enlaces relativos y rangos de código del pin. El reporte distingue ocurrencias de citas de rangos únicos. Las referencias históricas usan metadatos de archivos recuperados por SHA; CI observada se limita a estados/jobs. Esta verificación editorial no certifica semántica completa, exportaciones, compilación ni runtime.

Cuatro submódulos no disponibles localmente; diferencia Android excluida de afirmaciones; offsets/STATIC_ASSERT históricos no miden ABI Windows. Pendientes concretos en OPEN_QUESTIONS, incluidos Message y garantías pendientes de callbacks, fallos de sidecar, teardown de perfiles, símbolos binarios y profundidad de modelos/HUD/clima/NPC/minijuegos.

Todas las fichas recuperadas de subtareas están integradas en los checkpoints remotos; no se computa un mensaje finished como artefacto. Sin pruebas nuevas de Windows/juego ni mods producidos.

## Tiempo observado

Continuación observada desde 2026-10-21T13:48:44Z hasta 2026-10-21T14:15:46Z antes de publicar: 1622 segundos de sesión. No equivale a CPU ni a suma de trabajo paralelo; tiempo efectivo de investigación N/D. La pausa entre sesiones se excluye. La sesión anterior duró aproximadamente 13 minutos según el encargo, sin añadirla como horas medidas.

CP-R06 añade cuatro evidencias y tres símbolos sobre Item resolvers, con consumidor TARGET_PC del cofre. No amplía el número de servicios auditados ni acredita todas las rutas Item. El snapshot no revalida handle; no se atribuye permiso de reentrancia al contrato. Q-01/Q-02 siguen parcialmente abiertos.

CP-R07 contrasta adquisición, uso y liberación de fuente BFN/JUTResFont en file-info. Cuatro evidencias y cuatro símbolos nuevos; HUD permanece READ global y la cadena citada es CROSSCHECKED. Ninguna sustitución gráfica fue ejecutada.

CP-R08 añade una ficha real de soporte (logros), cinco evidencias y cuatro símbolos. Port_support pasa a READ global por la cadena seleccionada; otros auxiliares no se declaran estudiados. Se leyó código de IO sin abrir achievements.json ni datos del usuario.
