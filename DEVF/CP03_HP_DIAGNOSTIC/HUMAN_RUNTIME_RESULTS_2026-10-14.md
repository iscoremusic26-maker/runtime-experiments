# CP03 — cierre de pruebas humanas v0.3.1

**CP03_HUMAN_RUNTIME_PASS**, 14 de octubre de 2026 (America/Panama), para el flujo enumerado de un E_OC2 adicional identificado en Dusklight 2.0.3 Windows x64/DX12, F_SP121, sala 3, capa 6. El usuario autorizó este cierre. No es una declaración de producto estable, compatibilidad universal o motor configurable general.

## Procedencia y gates

Este informe contiene un **extracto comunicado por el usuario / análisis en ChatGPT; raw log no archivado en Git**. El agente no ejecutó el juego ni revisó localmente los logs personales. Los números de línea, conteos y ausencia de errores proceden del resumen suministrado, no de una búsqueda del agente en el archivo completo. No se asigna SHA256 a esos logs, que no se han verificado aquí como archivos.

| Gate | Estado | Procedencia y alcance |
|---|---|---|
| Target, identidad y política del piloto | SOURCE_VERIFIED | REPO_VERIFIED; auditorías anteriores conservadas |
| Compilación Windows | BUILD_PASS | REPO_VERIFIED; MSVC 19.51.36260 x64, SDK 10.0.26100.0, run 38541018826 |
| 17 casos de laboratorio | TEST_FAKE_PASS | REPO_VERIFIED; snapshots/mocks ejecutados en run 38540468476, reutilizados sin cambios; no 17 pruebas del juego |
| Cuatro negativos PE | PASS_OFFLINE | REPO_VERIFIED; copias propias rechazadas, no cargadas |
| Package oficial | PACKAGE_VERIFIED | REPO_VERIFIED; versión 0.3.1 y DLL interna intactas |
| Descarga e integridad | DOWNLOAD_VERIFIED | REPO_VERIFIED; descarga anterior real, hashes medidos nuevamente sin recompilar ni descargar otra distribución |
| Inicialización y health 220→150 | HUMAN_RUNTIME_PASS | USER_SUPPLIED_LOG_SUMMARY_ANALYZED; dos instancias, lectura FIELD_READBACK |
| Decrementos netos hasta cero | HUMAN_RUNTIME_PASS | USER_SUPPLIED_LOG_SUMMARY_ANALYZED; ocho ventanas HP_DELTA |
| Aparición, animaciones, combate y muerte | PASS_REPORTED | USER_REPORTED / HUMAN_REPORTED; observación humana separada del log |
| Salida de zona y reaparición | PASS_REPORTED | HUMAN_REPORTED, correlacionada con ActorId nuevo; no dos simultáneos |
| Retirada tras cierre, quitar .dusk y reiniciar | PASS_REPORTED | HUMAN_REPORTED: «Desaparecio»; no verificación por log |
| Cierre del flujo CP03 probado | CP03_HUMAN_RUNTIME_PASS | Síntesis de las evidencias anteriores, con sus límites |
| Generalización, estabilidad universal, otros mods/configuraciones | NOT_TESTED | Fuera de esta prueba |
| CP04 / CP06 | NOT_STARTED / NOT_AUTHORIZED | Ninguna implementación o investigación nueva |

Fuente compilada: `9dd5b8efd4ad98f1d6260820d782e101366a0f8b`. CI: `7fd3628ee8bfeb30f8070db061220796c1c15b4a`. [Run Windows aprobado](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38541018826). El paquete fue publicado originalmente con HUMAN_RUNTIME_NOT_TESTED; la evidencia posterior cambia el estado documental, no lo que CI ejecutó.

## Log diagnóstico comunicado

`dusklight-20261014-083535.log`: **4496 líneas según la inspección previa comunicada**. Línea 61: módulo `dev.devf.cp03_stage_hook_hp150`, versión 0.3.1, diagnóstico cargado. Línea 64: EDIT_REGISTERED, una edición StageService, actor_id=0; ese registro no es aplicación de HP a un actor.

| Línea | Evento | ActorId | Evidencia comunicada |
|---|---|---|---|
| 1795 | HP_APPLIED | 147 | old_hp=220, new_hp=150, PRE_FIRST_EXECUTE, EXCLUSIVE_FIRST_CREATE, FIELD_READBACK |
| 4175 | HP_APPLIED | 568 | old_hp=220, new_hp=150, PRE_FIRST_EXECUTE, FIELD_READBACK |
| 4176 | HP_SUMMARY | 147 | NEXT_GENERATION, última lectura 0 |
| 4494 | HP_SUMMARY | 568 | SHUTDOWN, última lectura 0 |
| 4495 | SHUTDOWN | — | Cierre normal comunicado |

Las ventanas de decremento se correlacionan por ActorId; los ordinales vuelven a 1 en la nueva instancia:

| ActorId | Línea | Ordinal | hp_before → hp_after | Pérdida efectiva | Cambio neto |
|---|---|---|---|---|---|
| 147 | 1853 | 1 | 150 → 110 | 40 | −40 |
| 147 | 1855 | 2 | 110 → 70 | 40 | −40 |
| 147 | 1856 | 3 | 70 → 30 | 40 | −40 |
| 147 | 1857 | 4 | 30 → 0 | 30 | −30 |
| 568 | 4204 | 1 | 150 → 110 | 40 | −40 |
| 568 | 4205 | 2 | 110 → 70 | 40 | −40 |
| 568 | 4206 | 3 | 70 → 30 | 40 | −40 |
| 568 | 4209 | 4 | 30 → 0 | 30 | −30 |

Ambas transiciones 30→0 tienen `classification=UNKNOWN_OR_SPECIAL`. Los cambios con signo de la tabla son cálculo directo de los valores comunicados; no son una transcripción de campos adicionales no suministrados.

| Evento DEVF_CP03_HP | Conteo comunicado |
|---|---|
| EDIT_REGISTERED | 1 |
| HP_APPLIED | 2 |
| HP_DELTA | 8 |
| HP_SUMMARY | 2 |
| SHUTDOWN | 1 |
| HP_REJECTED | 0 |
| HP_DIAG_REJECTED | 0 |
| HP_INCREASE_OBSERVED | 0 |

Según la inspección comunicada, no aparecieron líneas ERROR/FATAL. No se añade un conteo de supresión, arma o potencia de ataque que no fue proporcionado.

## Observaciones humanas y significado

El usuario confirmó aparición normal, animaciones, combate y muerte; tras salir naturalmente de la zona y regresar apareció una instancia nueva. Esto concuerda con los IDs 147 y 568 y el resumen NEXT_GENERATION. No indica duplicación simultánea.

Para el control negativo se solicitó cerrar el juego, quitar v0.3.1, reiniciar y volver al sitio. La respuesta inequívoca fue **«Desaparecio»**. Se cierra como PASS_REPORTED humano de retirada bajo ese procedimiento. El SHUTDOWN del log acredita cierre comunicado, pero no acredita por sí solo ausencia tras retirar el paquete. No se afirma eliminación en caliente.

Las lecturas comunicadas muestran que health cambió 220→150 y luego descendió hasta cero en las dos instancias elegibles: la personalización afectó el campo de vida usado por la lógica de combate en estas pruebas. Cada HP_DELTA es un cambio neto observado en una ventana del método, no una identificación infalible del arma, un golpe físico individual o mAttackPower bruto. La pérdida final de 30 son los HP restantes hasta cero; no demuestra potencia bruta 30. UNKNOWN_OR_SPECIAL no prueba un movimiento especial concreto.

No hubo incrementos detectados en las ventanas comunicadas ni evidencia comunicada de reset a 150 después de daño. Esto no demuestra que toda curación posible sea imposible. El número visual de espadazos observado antes no medía HP; no se convierte esta serie en una regla universal de cuatro golpes.

## Antecedente, preservación y límites

v0.3.0: `dusklight-20261014-033759.log` comunicó HP_APPLIED 220→150 para 147 (1797), 581 (3959) y 784 (4955), y SHUTDOWN normal (5281), sin medición por impacto. Es antecedente; el cierre principal usa v0.3.1. CP01/CP02 y sus controles negativos humanos permanecen históricos. Los 220 HP de CP02 provienen de fuente, no de una medición experimental individual de CP02.

Se conserva exactamente `DEVF_CP03_HP_DIAGNOSTIC_windows-amd64_9dd5b8efd4ad98f1d6260820d782e101366a0f8b.dusk`: **11975 bytes**, SHA256 `0d9882b072fe5cd6248c16a181171a47364e1acf5870503c1eb2f39c668b4344`, módulo `dev.devf.cp03_stage_hook_hp150`, versión 0.3.1. No se recompiló ni renombró. [Medición de integridad del cierre](evidence/human-runtime-closure-integrity-2026-10-14.json): 17 archivos del ledger iguales byte a byte al commit compilado; paquete y DLL interna medidos contra los hashes anteriores. `field_0x560` no se modificó; el perfil de HP máximo no fue medido.

Host de referencia previo: Dusklight 2.0.3, fuente `40457c6adb381928e4b5fef6ed459ed291edd5e2`, EXE SHA256 `ffa992038d04290654b8907a7663f4dcf62083beaad2b35014fdfd901d390049`. No se midió de nuevo la instalación Windows del usuario desde Codex.

Límites: dos instancias registradas en esta prueba, un escenario y configuración DX12; sin benchmark amplio, prueba de mods conflictivos, otras versiones/mapas/configuraciones, curaciones especiales, daño bruto, hot-unload o generalización a cualquier enemigo. No se ha implementado un motor configurable completo. No se alteraron host, SDK, import library, Aurora, recursos o partidas.

**Dictamen: PASS_RUNTIME del flujo probado CP03 v0.3.1, expresado como CP03_HUMAN_RUNTIME_PASS.** CP04/CP06 no iniciados. Un paso futuro sería acordar alcance y criterios de la siguiente etapa; este cierre no la autoriza ni la ejecuta. [Recuperación exacta](RECOVERY.md).
