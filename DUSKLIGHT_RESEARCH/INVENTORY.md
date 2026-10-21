# Inventario clasificado del árbol disponible

Fuente: `40457c6adb381928e4b5fef6ed459ed291edd5e2`; certificación y excepciones en [SOURCE_PIN.md](SOURCE_PIN.md). Se recorrió una vez el conjunto de rutas para el inventario canónico. Los hashes se calcularon sobre los bytes locales, sin mutar la fuente.

**19367 archivos; 488 directorios con archivos descendientes; 2097 archivos de implementación; 17067 encabezados/includes.** Los cuatro gitlinks ausentes se registran separadamente, sin contarlos como archivos leídos.

La clasificación automática por ruta es un índice de navegación `STATIC_INFERRED`. No es una auditoría semántica de todos esos archivos. Algunas rutas consumen varios sistemas: el índice asigna uno primario; los informes de sistemas documentan dependencias adicionales.

## Procedencia

| Clase | Archivos |
| --- | ---: |
| `build_or_research_tooling` | 27 |
| `bundled_engine_library` | 619 |
| `bundled_platform_or_third_party` | 1000 |
| `documentation_or_editor` | 19 |
| `dusklight_port` | 329 |
| `dusklight_sdk` | 46 |
| `game_source_with_port_adaptations` | 2301 |
| `platform_packaging` | 43 |
| `port_presentation_resources` | 35 |
| `repository_metadata` | 6 |
| `resource_identifier_headers` | 14879 |
| `upstream_mod_example` | 63 |

`game_source_with_port_adaptations` evita llamar “original GC inalterado” a código que incorpora TARGET_PC. `bundled_engine_library` identifica JSystem; las bibliotecas SDK de consola y compatibilidad no se tratan como código gameplay. Los encabezados regionales `assets/` son índices de recursos presentes en fuente, no archivos del disco redistribuidos. Ejemplo examinado: [assets/GZ2E01/res/FieldMap/D_MN01.h, L1-L18](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/assets/GZ2E01/res/FieldMap/D_MN01.h#L1-L18).

## Cobertura de directorios principales

| Ruta | Archivos descendientes | Clasificación |
| --- | ---: | --- |
| `.github/` | 3 | build_or_research_tooling |
| `.vscode/` | 4 | documentation_or_editor |
| `assets/` | 14879 | resource_identifier_headers |
| `ci/` | 1 | build_or_research_tooling |
| `cmake/` | 12 | build_or_research_tooling |
| `docs/` | 12 | documentation_or_editor |
| `include/` | 1156 | game_source_with_port_adaptations, documentation_or_editor |
| `libs/` | 1620 | bundled_engine_library, bundled_platform_or_third_party, build_or_research_tooling |
| `mods/` | 63 | upstream_mod_example |
| `platforms/` | 43 | platform_packaging |
| `res/` | 35 | port_presentation_resources |
| `sdk/` | 46 | dusklight_sdk |
| `src/` | 1475 | game_source_with_port_adaptations, dusklight_port |
| `tools/` | 2 | build_or_research_tooling |

[DIRECTORY_INDEX.tsv](DIRECTORY_INDEX.tsv) incluye **cada** directorio con archivos, su conteo directo/descendiente y sistemas primarios. [FILE_INVENTORY.tsv](FILE_INVENTORY.tsv) incluye cada archivo: tipo, procedencia, sistema, categoría, bytes y hash Git. Los archivos raíz también se clasifican allí.

## Sistemas primarios por ruta

| Sistema | Archivos |
| --- | ---: |
| `actors_ai_npcs` | 1529 |
| `audio_particles_effects` | 283 |
| `build_tooling` | 33 |
| `cameras_rendering` | 33 |
| `combat_damage` | 12 |
| `cutscenes_dialogue` | 123 |
| `documentation` | 19 |
| `environment_weather_time` | 20 |
| `flags_events_progression` | 14 |
| `game_support` | 83 |
| `hooking_abi` | 8 |
| `hud_ui_text` | 292 |
| `inventory_equipment` | 12 |
| `memory_ownership` | 69 |
| `models_animations_materials` | 95 |
| `movement_physics_collision` | 135 |
| `other_systems` | 12 |
| `platform_backend` | 1251 |
| `player_and_controls` | 47 |
| `port_support` | 58 |
| `resources_archives_overlays` | 14897 |
| `runtime_and_lifecycle` | 226 |
| `save_load` | 22 |
| `sdk_services` | 85 |
| `stages_rooms_layers` | 9 |

## Exclusiones y prioridades

P0: ABI/loader/hooks, registro y contratos SDK, actores/escenas, guardado y propiedad. P1: jugador/input, colisión/combate, recursos y presentación. P2: detalles de minijuegos, cada actor particular y utilidades específicas. La prioridad no implica implementación de un mod.

`assets/` de las diez variantes regionales se cuenta y clasifica, pero la interpretación se centra en GZ2E01. Las otras regiones no certifican compatibilidad con el disco objetivo. Los 1619 archivos de bibliotecas empaquetadas se localizan; solo se estudian mecanismos transversales relevantes (heap, J3D/J2D, audio, partículas), sin pretender auditar cada biblioteca. Los cuatro submódulos ausentes y dependencias descargadas por CMake son huecos explícitos, no fuentes leídas.

CMake declara miniz 3.0.2, PicoSHA2 1.0.1, opusfile opcional por commit y funchook 1.1.3; no se descargaron ni se ejecutó CMake ([CMakeLists.txt L178-L240](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/CMakeLists.txt#L178-L240), SOURCE_OBSERVED). Dependencias transitivas de Aurora/Borealis quedan pendientes.

No se inventarían ROM/CISO, partidas, binarios del juego ni assets de usuario. Los recursos originales no se redistribuyen en este atlas.

## Consulta reproducible

```sh
python DUSKLIGHT_RESEARCH/tools/inventory.py RUTA_FUENTE RUTA_SALIDA_SEPARADA
```

Los conteos son de archivos existentes del árbol principal; no equivalen a archivos compilados para Windows. `files.cmake`, los CMake y las condiciones TARGET_PC deben consultarse para determinar participación en un target. La utilidad rechaza una salida situada dentro de la fuente analizada.
