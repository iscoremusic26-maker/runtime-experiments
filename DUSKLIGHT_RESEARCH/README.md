# Atlas técnico de Dusklight 2.0.3 para investigación de mods .dusk

**Fuente fijada:** `TwilitRealm/dusklight` @ `40457c6adb381928e4b5fef6ed459ed291edd5e2` (`v2.0.3`). **Objetivo:** Windows x64, DirectX 12, GZ2E01 USA. Investigación general, sin mod objetivo.

**CP-R02: hooks, loader, contratos SDK, escenas, guardado y progresión con evidencia estática.** Checkpoint de auditoría e inventario inicial conservado. El árbol disponible se ha inventariado y clasificado; el análisis transversal de implementaciones se incorpora por bloques. La cobertura real, los límites y los próximos pasos se actualizarán con cada checkpoint. No se afirma investigación profunda de todos los archivos ni ejecución del juego.

- [Entradas, hashes y límites](SOURCE_PIN.md).
- [Inventario y clasificación](INVENTORY.md), [resumen JSON](INVENTORY_SUMMARY.json), [todos los archivos](FILE_INVENTORY.tsv), [todos los directorios](DIRECTORY_INDEX.tsv).
- [Continuidad del checkpoint](CONTINUATION.md) y [cambios documentales](CHANGELOG.md).
- [Instrucciones para consultar y mantener](AGENTS.md); [utilidad de inventario de solo lectura](tools/inventory.py).

Contenido técnico publicado: [servicios SDK](SDK_AND_SERVICES.md), [hooks/ABI](HOOKING_AND_ABI.md), [loader/runtime](systems/runtime_and_lifecycle.md), [evidencia](EVIDENCE_LEDGER.json), [símbolos](SYMBOL_INDEX.json), [sistemas](SYSTEM_INDEX.json) y [cobertura](RESEARCH_COVERAGE.md). Los informes restantes se incorporan por bloques. La existencia de una ruta en el inventario no demuestra que sea exportada, hookeable ni segura en Windows.

**NO MOD IMPLEMENTED / NO GAME RUNTIME CLAIMED / NO PRODUCTION MODIFIED.**

Fichas incorporadas CP-R02: [stages/salas/capas](systems/stages_rooms_layers.md), [save/load](systems/save_load.md), [flags y eventos](systems/flags_events_progression.md), [inventario](systems/inventory_equipment.md), [secuencias y diálogos](systems/cutscenes_dialogue.md).
