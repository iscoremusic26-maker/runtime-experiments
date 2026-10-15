# Resultados API y separación de evidencias

| Gate | Resultado |
| --- | --- |
| CP07.1 histórico build/descarga | SUCCESS verificado, no repetido sobre paquete0.7.0 |
| CP07.1 sesiones115005/115119 | HUMAN_RUNTIME_OBSERVED, reporte/sumario usuario, sin rawlogs locales |
| CoreCP06 JSON cuatro modos,109casos | PASS |
| Editor/IO/persistencia/callbacks,55casos | PASS |
| Broker/probe/API C ABI y lifecycle,50casos | PASS |
| C11+C++20 compartidos MSVC | PASS ABI80/24/24, offsets8/16 |
| ProveedorNONE + consumidorFIELD | PASS LAB: llamada real Probe→API→Broker→StageService doble,1recordFIELD |
| Proveedor solo BOTH/FIELD/NORTH/NONE | PASS LAB, sin dependencia de probe |
| JSONFIELD + consumidorFIELD | PASS LAB: MOD_CONFLICT, sin segunda alta |
| JSONNORTH + consumidorFIELD | PASS LAB:2records distintos, coreJSON preservado |
| Ausencia/majorincorrecta/unpublished | PASS LAB modelo + contratos/PE, NO loader real |
| IDs/sitios/ownerduplicados, inputs inválidos, scope cerrado | PASS LAB |
| Detach, remove ajeno, ticketviejo, error/exception/handle0/alias | PASS LAB: limpieza propia/quarantena fail-closed |
| Detach durante petición y petición reentrante | PASS LAB adversarial; no garantía de threads fuera del contrato |
| API externa no aparece en JSON del editor | PASS LAB |
| PE/ABI/deferred/required/imports/exports | PASS |
| Negativos PE/ZIP |13proveedor+9probe=22PASS |
| PackageSDK y DESCARGA REAL de ambos | PASS |
| Aparición/retirada por nuevo par en juego | HUMAN_PENDING |
| Reentrada/FPS/terceros/universalidad | NOT_VERIFIED |
| ActorId↔placement/HP/tinte/IA por instancia | NO IMPLEMENTADOS |
| Bokoblin Expansion/CP07.2/CP08 | NO IMPLEMENTADOS |

Total214casos sobre headers reales usados por las DLL. API tests usan Broker y Probe de producción; dobles sólo de Host/Stage/registro de servicio. Las suites heredadas usan dobles de File/UI sobre archivos Windows reales. No fake de juego, de actor vivo ni GPU.
C ABI de tamaño y offsets compilada en C11 y C++20. Dependencia REQUIRED/deferred comprobada en binarios reales y fuente SDK. El modelo de resolución/fallos del laboratorio no ejecuta ModLoader del juego.
Los registros StageActorHandle pertenecen al proveedor y no son ActorId. Receipt entrega ticket de la API, no handle de host. remove edit no elimina actor vivo.

[Build38787691561](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38787691561) SUCCESS; [descarga38788164065](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38788164065) SUCCESS.214PASS al primer intento, no fallos nuevos en este corte. Nombres, tiempos, metadata, hashes y CRC en evidence/.
Cierre humano previo en ../CP07_1_NATIVE_EDITOR/HUMAN_RUNTIME_RESULTS_2026-10-15.md; no transferir sus PASS al par nuevo. Una QA nueva con NONE y probe, seguida de retirada fría del probe; no repetir pruebas humanasCP06/CP07.1.
