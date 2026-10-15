# CP07.2A — resultados y limites
**CP07_2A_ENCOUNTER_EDITOR_QA_READY / HUMAN_RUNTIME_PENDING.**
Fuente compilada e066a5e7505a266658783259b70cb320321747f2; CI build 2f02e07e7916ef0c947042dbbc9e4d79b12153f3; verificador c7f9dfbd1ffedc15db06b4dfd084c0f9c476b1e1.

| Funcion/gate | Resultado |
| --- | --- |
| API0.7.1 anterior, par+NONE y luego proveedor solo+NONE | HUMAN_RUNTIME_OBSERVED_PASS limitado a confirmacion+extractos comunicados; acta nueva, sin releer rawlogs |
| CP06 core cuatro modos |109PASS Windows, core real reutilizado |
| CP07.1 editor/persistencia |55PASS Windows, fuentes/tests historicos copiados sin cambios |
| API broker/probe y lifecycle |50PASS Windows, core real/dobles publicos |
| Encuentros/parser/serializer/modelo/UI/IO |62PASS Windows |
| Total |276PASS |
| C11/C++20 shared API80/24/24 |PASS |
| Enlace de lector real +GameService2.0 |PASS,12simbolos exactos de bibliotecaSDK original |
| Scene changing/transicion/evento/ticks/NaN/invalid snapshot |PASS core con entradas normalizadas; NO memoria de juego ejecutada |
| Captura real de Link, UX en menu pausado, segunda sala/stage |HUMAN_PENDING |
| Coleccion UTF8/escapes/IDs/nombres/multi-stage/roundtrip/limites |PASS LAB |
| Backup exclusivo/fallos escritura/flush/close/relectura/conflicto/rollback |PASS LAB con FileService doble sobre archivos Windows reales |
| No IO update sin peticion, cancelar captura al cerrar/nuevo borrador/editar |PASS LAB |
| Guardado/reinicio simulado/exportacion/seleccion/borrador/eliminacion confirmada |PASS LAB |
| Validador CLI compartido con DLL |PASS MSVC y ejemplo export vacio; parser negativo en62casos |
| PE/ABI/metadata/imports/exports/paquete oficial |PASS |
| Negativos PE/ZIP |14PASS:incluye wrong_game_major,wrong_api_major,deferred flags,extraasset,traversal |
| Descarga REAL de QA y evidencia por otro runner |PASS SHA256/bytes/CRC/ledger/DLL/CLI/manifests |
| Probe0.1.0 binario historico, sin recompilar |PASS descarga/CRC/SHA/PE,header y cliente iguales; NO ejecucion loader real |
| Capturar/guardar/exportar hace spawns |NO IMPLEMENTADO deliberadamente; solo diseno |
| Grupos/navegacion/suelo/respawn ejecutable fuera de whitelist |NO IMPLEMENTADO |
| FPS/terceros/universalidad/powerloss/concurrent writer atomico |NOT_VERIFIED |

[Build38794698410](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38794698410) SUCCESS; [descarga38795046018](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38795046018) SUCCESS. Primer build38794202966 tambien SUCCESS(271casos); se ajustaron cancelacion de borrador, staging de memoria antes de IO y se añadieron5casos; segundo build276PASS verifica ESOS cambios. No fallos ocultados ni recompilacion rutinaria del0.7.1.

Los62casos ejecutan Session/Model/Ui/Store/parser/serializer reales de DLL. File/UI/Host son dobles publicos, archivos reales Windows; read_native del laboratorio suministra datos normalizados y NO emula Link/GPU. Native_capture.cpp real solo se compilo/enlazo/audito; no fue invocado contra un juego ni ejecutada DLL por CI. Archivo JSON de ejemplo vacio no es una captura humana. La suite50API no ejecuta ModLoader real; contrato fuente+metadata+modelo, no gameplay.

Sin StageService/ActorService/HookService en las cuatro unidades encounter_core/encounter_store/native_capture/encounter_ui; StageService permanece solo en autoridades historicas core/broker. No personalizacion HP/color/IA. Scene epoch/ActorId general no se implementan para exportar datos. No Bokoblin Expansion ni CP08.
