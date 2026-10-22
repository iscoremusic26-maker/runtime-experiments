# Cobertura real — CP-R83

## Alcance y denominadores

Se conservan **19367 archivos y 488 directorios** del inventario CP-R00. Esta continuación no recalculó hashes ni reconstruyó ese inventario. Las siete erratas nominales se aplican desde INVENTORY_ERRATA.json, sin duplicar el TSV. Los encabezados regionales no se cuentan como implementaciones leídas.

Se publican **24 fichas de sistemas, 488 evidencias y 427 registros de símbolos**. El índice canónico tiene 28 entradas: 18 CROSSCHECKED selectivas, 6 READ y 4 exclusivamente INVENTARIED. Incluye SDK, soporte y evidencia histórica, por lo que no representa 28 sistemas gameplay independientes.

Los 25 contratos C del SDK se contrastaron con fronteras seleccionadas de implementación. Hay 26 candidatos de módulo (UiService 1.5 y 2.3), sujetos a disponibilidad; 209 ranuras públicas localizadas no equivalen a 209 métodos auditados. El índice de símbolos mezcla tablas/slots, tipos y funciones; no afirma haber seguido la cadena completa de llamadas de los 427 registros.

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
| `port_support` | READ | [logros](systems/port_achievements.md), [speedrun/LiveSplit](systems/port_speedrun_livesplit.md), [presencia](systems/port_presence.md), [consola host](systems/port_commands.md), [diagnóstico disco](systems/port_disc_validation.md) |
| `external_dependencies` | INVENTARIED | [SYSTEM_DEPENDENCIES.md](SYSTEM_DEPENDENCIES.md), [INVENTORY.md](INVENTORY.md) |

CROSSCHECKED: declaraciones/contrato, implementación y usos seleccionados contrastados con límites explícitos. READ: implementación consultada con flujo/dependencias todavía parciales. INVENTARIED: rutas localizadas; no prueba comprensión. Cada evidencia conserva su propio nivel y puede ser más limitado que una parte ya contrastada del mismo sistema.

## Calidad y límites

Se validan estructura JSON, unicidad, IDs cruzados, dependencias, enlaces relativos y rangos de código del pin. El reporte distingue ocurrencias de citas de rangos únicos. Las referencias históricas usan metadatos de archivos recuperados por SHA; CI observada se limita a estados/jobs. Esta verificación editorial no certifica semántica completa, exportaciones, compilación ni runtime.

Cuatro submódulos no disponibles localmente; diferencia Android excluida de afirmaciones; offsets/STATIC_ASSERT históricos no miden ABI Windows. Pendientes concretos en OPEN_QUESTIONS, incluidas garantías pendientes de callbacks tras contrastar Message, fallos de sidecar, teardown de perfiles, símbolos binarios y profundidad de modelos/HUD/clima/NPC/minijuegos.

Todas las fichas recuperadas de subtareas están integradas en los checkpoints remotos; no se computa un mensaje finished como artefacto. Sin pruebas nuevas de Windows/juego ni mods producidos.

## Tiempo observado

Sesión histórica CP-R06..09: 2026-10-21T14:36:28Z a 2026-10-21T14:58:02Z antes de publicar; 1294 segundos de sesión observados, sin convertirlos en CPU ni sumar pausas o agentes. Tiempo efectivo de investigación N/D. Se publicaron CP-R06..09 con cuatro familias de mecanismos; neto +17 evidencias (184→201), +13 símbolos (202→215), +1 documento real (46→47 archivos). La sesión CP-R05 anterior tuvo1622 segundos observados propios y no se vuelve a sumar aquí.

CP-R06 añade cuatro evidencias y tres símbolos sobre Item resolvers, con consumidor TARGET_PC del cofre. No amplía el número de servicios auditados ni acredita todas las rutas Item. El snapshot no revalida handle; no se atribuye permiso de reentrancia al contrato. Q-01/Q-02 siguen parcialmente abiertos.

CP-R07 contrasta adquisición, uso y liberación de fuente BFN/JUTResFont en file-info. Cuatro evidencias y cuatro símbolos nuevos; HUD permanece READ global y la cadena citada es CROSSCHECKED. Ninguna sustitución gráfica fue ejecutada.

CP-R08 añade una ficha real de soporte (logros), cinco evidencias y cuatro símbolos. Port_support pasa a READ global por la cadena seleccionada; otros auxiliares no se declaran estudiados. Se leyó código de IO sin abrir achievements.json ni datos del usuario.

CP-R09 añade cuatro evidencias y dos símbolos del reloj ambiental/KYTAG11/rollover. Entorno conserva READ global con rutas seleccionadas contrastadas; los setters de tiempo/fecha no acreditan escritura a disco ni efecto de audio observado.

CP-R10: una cadena adicional file-select→PLAY contrastada (ARCH-002..007); +6 evidencias,+6 símbolos,+0 documentos desde CP-R09. Runtime conserva CROSSCHECKED selectivo; Q-09 parcial. No se cuenta como seis rutas independientes ni bootstrap completo.

Esta continuación CP-R10 se registra por separado; duración observada N/D. No se acumula el intervalo entre sesiones.

CP-R11 añade una cadena distinta de recursos gráficos (AutoMata→morf/BCK/BTK→cleanup): +4 evidencias,+4 símbolos,+0 documentos frente a CP-R10. Models permanece READ global. Neto CP-R09→11:+10 evidencias,+10 símbolos,+0 documentos; dos cadenas representativas nuevas,no familias completas.

CP-R12 añade cadena Message callback→copia de texto→binding→retirada/reset,con consumidor: +5 evidencias,+4 símbolos,+0 documentos. Neto CP-R09→12:+15/+14/+0; tres cadenas representativas. Sin promoción de cobertura global ni runtime.

CP-R13: una cadena de soporte speedrun/LiveSplit (evento/modo/contador→UI/red/cierre),+4 evidencias,+3 símbolos,+1 ficha. Neto CP-R09→13:+19 evidencias (201→220),+17 símbolos (215→232),+1 documento (47→48 archivos;20→21 fichas),cuatro cadenas representativas. Los estados28/18/6/4 no cambian; red/temporización externas no probadas.

CP-R14: +5 evidencias,+5 símbolos,+0 informes/+0 archivos frente a CP-R13; una cadena nueva de puzzle/colisión. Los niveles canónicos permanecen18 CROSSCHECKED selectivos,6 READ,4 INVENTARIED; no acreditan cobertura integral.

CP-R15: +4 evidencias,+3 símbolos,+0 informes/+0 archivos frente a CP-R14; una cadena ambiental nueva. Los niveles canónicos permanecen18 CROSSCHECKED selectivos,6 READ,4 INVENTARIED; no acreditan cobertura integral.

CP-R16: +4 evidencias,+3 símbolos,+0 informes/+0 archivos frente a CP-R15; corrección de integración de un símbolo interno (OFFICIAL_SERVICE→POTENTIAL_REQUIRES_VERIFICATION),sin borrar evidencia. Los niveles canónicos permanecen18 CROSSCHECKED selectivos,6 READ,4 INVENTARIED; no acreditan cobertura integral.

CP-R17: +4 evidencias (3 contrastadas,1 inferencia condicionada),+3 símbolos,+0 informes/+0 archivos frente a CP-R16; una cadena audio nueva. Los niveles canónicos permanecen18 CROSSCHECKED selectivos,6 READ,4 INVENTARIED; no acreditan cobertura integral.

CP-R18: +6 evidencias (5 STATIC_CROSSCHECKED,1 STATIC_INFERRED),+4 símbolos internos; 0 fichas nuevas; Q-03 parcial. Los niveles canónicos permanecen18 CROSSCHECKED selectivos,6 READ,4 INVENTARIED; no acreditan cobertura integral.

CP-R19: +4 evidencias STATIC_CROSSCHECKED,+3 símbolos;0 fichas nuevas; HUD sigue READ parcial. Los niveles canónicos permanecen18 CROSSCHECKED selectivos,6 READ,4 INVENTARIED; no acreditan cobertura integral.

CP-R20: +5 evidencias (4 STATIC_CROSSCHECKED,1 STATIC_INFERRED),+4 símbolos (2 slots oficiales,2 localizadores);0 fichas nuevas. Los niveles canónicos permanecen18 CROSSCHECKED selectivos,6 READ,4 INVENTARIED; no acreditan cobertura integral.

CP-R21: +5 evidencias STATIC_CROSSCHECKED,+4 símbolos;0 fichas nuevas; ambiente sigue READ parcial. Los niveles canónicos permanecen18 CROSSCHECKED selectivos,6 READ,4 INVENTARIED; no acreditan cobertura integral.

CP-R22: +3 evidencias STATIC_CROSSCHECKED,+2 localizadores;0 fichas nuevas; Q-07 parcial y redacción histórica de símbolo rectificada. Los niveles canónicos permanecen18 CROSSCHECKED selectivos,6 READ,4 INVENTARIED; no acreditan cobertura integral.

CP-R23: +6 evidencias (5 STATIC_CROSSCHECKED,1 STATIC_INFERRED),+4 localizadores;0 fichas nuevas; Q-12 READ selectivo. Los niveles canónicos permanecen18 CROSSCHECKED selectivos,6 READ,4 INVENTARIED; no acreditan cobertura integral.

CP-R24: +4 evidencias (3 STATIC_CROSSCHECKED,1 STATIC_INFERRED),+3 localizadores;0 fichas nuevas; Q-09 parcial. Los niveles canónicos permanecen18 CROSSCHECKED selectivos,6 READ,4 INVENTARIED; no acreditan cobertura integral.

CP-R25: +3 evidencias (2 STATIC_CROSSCHECKED,1 STATIC_INFERRED),+3 localizadores;0 fichas nuevas; Q-14 parcial. Los niveles canónicos permanecen18 CROSSCHECKED selectivos,6 READ,4 INVENTARIED; no acreditan cobertura integral.

CP-R26: +4 evidencias (3 STATIC_CROSSCHECKED,1 STATIC_INFERRED),+3 localizadores,+1 ficha nueva; soporte sigue READ. Los niveles canónicos permanecen18 CROSSCHECKED selectivos,6 READ,4 INVENTARIED; no acreditan cobertura integral.

CP-R27: +6 evidencias (5 STATIC_CROSSCHECKED,1 STATIC_INFERRED),+4 localizadores;0 fichas nuevas; Q-10 parcial. Niveles canónicos18 CROSSCHECKED selectivos,6 READ,4 INVENTARIED sin promoción global.

CP-R28: +4 evidencias CALLBACK-019..022 y +3 símbolos; ningún documento nuevo. Niveles canónicos18 CROSSCHECKED selectivos,6 READ,4 INVENTARIED sin promoción global.

CP-R29: +4 evidencias PRES-074..077 y +4 símbolos; ningún documento nuevo. Niveles canónicos18 CROSSCHECKED selectivos,6 READ,4 INVENTARIED sin promoción global.

CP-R30: +5 evidencias PLAYER-052..056 y +3 símbolos; ningún documento nuevo. Niveles canónicos18 CROSSCHECKED selectivos,6 READ,4 INVENTARIED sin promoción global.

CP-R31: +5 evidencias ARCH-012..016 (4 contrastadas,1 inferencia condicionada),+4 localizadores,+0 documentos. Los niveles18 CROSSCHECKED selectivos,6 READ,4 INVENTARIED no cambian; no cobertura global.

CP-R32: +4 evidencias PRES-078..081,+3 localizadores,+0 documentos. Los niveles18 CROSSCHECKED selectivos,6 READ,4 INVENTARIED no cambian; no cobertura global.

CP-R33: +5 evidencias CALLBACK-023..027 (4 contrastadas,1 inferencia),+3 símbolos (1 slot oficial,2 localizadores),+0 documentos. Niveles18 CROSSCHECKED selectivos,6 READ,4 INVENTARIED sin promoción global.

CP-R34: +4 evidencias PLAYER-057..060,+3 localizadores,+0 documentos. Niveles18 CROSSCHECKED selectivos,6 READ,4 INVENTARIED sin promoción global.

CP-R35: Consola host fija,rate y ownership UI. Cadena seleccionada; 18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED permanecen sin promoción global.

CP-R36: Captura menú,gate de ticks,presentación y cleanup. Cadena seleccionada; 18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED permanecen sin promoción global.

CP-R37: Stock tienda,tag,display y evento024. Cadena seleccionada; 18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED permanecen sin promoción global.

CP-R38: KYTAG08,referencia ambiental y consumidor MA11. Cadena seleccionada; 18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED permanecen sin promoción global.

CP-R39: McaMorf2,mezcla A/B,morph temporal y callbacks joint. Cadena seleccionada; 18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED permanecen sin promoción global.

CP-R40: InterpService,ventana,copias y conflicto de claves. Cadena seleccionada; 18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED permanecen sin promoción global.

CP-R41: StartAndGoal,timer global y resultadoRAM. Cadena seleccionada; 18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED permanecen sin promoción global.

CP-R42: Diagnóstico disco,worker,cancelación y estado UI. Cadena seleccionada; 18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED permanecen sin promoción global.

CP-R43: Lifecycle msg,drawtag y heap específico. Cadena seleccionada; 18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED permanecen sin promoción global.

CP-R44: BAS,eventos de sonido,handles y stop/release. Cadena seleccionada; 18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED permanecen sin promoción global.

CP-R45: Skinning explícito,buffers y packet consumidor. Cadena seleccionada; 18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED permanecen sin promoción global.

CP-R46: WebSocket polling,views y cierre diferido. Cadena seleccionada; 18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED permanecen sin promoción global.

CP-R47: PARCIAL lifetime KANKYO,global y gates de cleanup. Cadena seleccionada; 18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED permanecen sin promoción global.

CP-R48: Flecha tipo0,At/joint,adhesión y borrado diferido. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R49: PARCIAL retiro room8/20,solicitud y conservación BG. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R50: BTP,binding por slot,texNo y fallo de protocolo condicionado. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R51: UiService BUTTON,guard pane y rebuild/detach. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R52: Flecha enemiga,escudo madera,lista16 y reset. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R53: GameMode,selección PENDING,consumidor y fallback. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R54: KYTAG02,viento global,suavizado y consumidor Kita. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R55: Partícula trace,userWork y retiro por renovación. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R56: Direct-save logo,statusCARD,fallbackRAM y consumo ff. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R57: Gate latched,Mtx** y wrapperMoveBG. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R58: Texturefrontend,prioridad,reregistro y keepalive. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R59: Reactivación,loteLifecycle,operaciónUI y toast. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R60: ObjCarry,boomerang,offset corregido y transferencia Link. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R61: Disposers,destructorvirtual y reset de solid heap. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R62: Precisión de gate RotY y trazabilidad de destroy. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R63: TagWaterFall: región de cámara y maestro persistente — PARCIAL. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R64: Ice_s: apoyo continuo y matriz de plataforma. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R65: LogService: copias, retención y consumidor diagnóstico. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R66: BRK: registros de color TEV y lifetime del recurso. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R67: FileService list: llamadas síncronas y lifetime del sentinel. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R68: KYTAG04: orden de evento, contador y salida SCLS. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R69: BLS/BLK: deformación por clusters y consumidor Demo00. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R70: DigPlace: señal de animación, switch previo y petición de ítem. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R71: KYTAG03: rail de olor y pool ambiental — PARCIAL. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R72: FileService picker: reserva global y completion owned por separado. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R73: Lv4DigSand: handshake de excavación y llegada geométrica. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R74: Gfx: fallos del render worker y consumo diferido. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R75: Onsen: petición de vida y consumidor efectivo en Meter. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R76: NetService TCP: polling, cierre y lifetime de endpoint. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R77: Archive DVD: secuencias, buffers y fallo de enqueue. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R78: Rollgoal: actores distribuidos, resultado y progreso. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R79: Diagnóstico stub: callback, buffer y limpieza por frame. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R80: KYTAG13: nieve compartida, subrangos y limpieza. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R81: Mirilla: evento, modos de escena y snapshot de retorno. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R82: UiService: menú contextual, acción y cierre diferido. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.

CP-R83: InvisibleModel: packets por joint y pase de profundidad. Cadena seleccionada;28 entradas,18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción global.
