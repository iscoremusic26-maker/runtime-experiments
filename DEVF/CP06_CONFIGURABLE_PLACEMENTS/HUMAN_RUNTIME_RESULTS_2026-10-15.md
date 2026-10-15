# CP06 parcial — cierre humano de cinco pruebas, 2026-10-15

**CP06_PARTIAL_HUMAN_RUNTIME_OBSERVED. Se mantiene CHECKPOINT_CP06_PARTIAL; no CP06_MVP_COMPLETE ni release estable.**

Alcance: TEST privado single-site `dev.devf.cp06_single_site` v0.6.0, Dusklight 2.0.3 Windows x64/D3D12; máximo un placement activo en F_SP121 / room 3 / layer 6, (-1250, -6304.00830078125, 60750). Dos presets alternativos, nunca dos actores DEVF simultáneos. Configuración leída al arranque en frío; sin hot reload.

## Procedencia y autoridad

- **USER_HUMAN_REPORTED / HUMAN_OBSERVED:** declaraciones del usuario tras ejecutar en su PC. Codex no ejecutó el juego ni inspeccionó capturas o píxeles en este cierre.
- **USER_LOG_ANALYZED_IN_CHATGPT / LOG_OBSERVED:** resumen, líneas, tamaños, recuentos y hashes suministrados en la instrucción, procedentes del análisis de cinco adjuntos en ChatGPT. Los bytes originales no están disponibles para Codex en esta tarea; no se han releído ni recalculado sus hashes aquí. No se almacenan raw logs ni capturas en Git.
- **REPO_VERIFIED:** API GitHub: rama técnica y PR #37 draft/open/unmerged con cabeza exacta `1a57ce17347d2f9c229af4c424d8b05a5ad59353`; base del PR `feature/devf-cp05-ai-bounded-human-runtime-closure`. Tag técnico anotado `DEVF_CP06_PARTIAL_SINGLE_SITE_PRIVATE_TEST_READY`, objeto `feabf5382858b0969d7f272bde0c02f91d19ab31` → ese commit. Documentos de alcance single-site revisados.
- **CI_HISTORICAL:** estados SUCCESS, SHA de CI y metadatos del artifact comprobados por API; resultados técnicos originales conservan su procedencia histórica. No se ejecutó build, laboratorio, análisis PE, descarga binaria ni gameplay nuevos.
- **NOT_VERIFIED / NOT_IMPLEMENTED:** límites explícitos al final. La ausencia de evidencia no se clasifica como FAIL.

## Índice de evidencia privada suministrada

Recuentos físicos de líneas y SHA256 atribuidos al análisis en ChatGPT, no a una lectura local de Codex.

| Prueba | Log | Bytes | Líneas físicas | SHA256 |
| --- | --- | ---: | ---: | --- |
| 1 | dusklight-20261015-013415.log | 175522 | 2288 | `9948617afeee05043d0f016eed2d205ec4c3c0aff4fe1e4f455bdf76a9b2d38a` |
| 2 | dusklight-20261015-013757.log | 145897 | 1890 | `260d5218599572cb92dc09a955793b4c238c3c223b6aaa30803fa0addffd4a79` |
| 3 | dusklight-20261015-080517.log | 140943 | 1853 | `f17fcbda6b3e433f8605ddfe59dcac0c119f298abb0da47a4b4eedc423527625` |
| 4 | dusklight-20261015-080746.log | 147251 | 1882 | `e8dd912f35ee65ca35c86b08fec37e068711614f3b9f600b23249099f0d68325` |
| 5 | dusklight-20261015-080841.log | 139532 | 1843 | `1f8593f0b73ba50c9f49a46b21e9797ad9f7450d6acc398805cd5b4bb9566c51` |

## Cinco ensayos y sus límites

### 1. Black_guard activo y enemigo negro visible

**Usuario:** «Ya apareció el negro».

L61 carga v0.6.0. L64 `CONFIG_ACCEPTED schema=1 placement_id=field_black variant_id=black_guard active=1 max_active=1 status=CP06_PARTIAL`. L65 `EDIT_REGISTERED` acredita registro de edición, no nacimiento por sí mismo. L1796 `ADMITTED actor_id=147 generation=1 admission_epoch=1 scene_epoch=NOT_GENERALIZED`. L1797 `HP_APPLIED 220→150 PRE_FIRST_EXECUTE` (lectura del campo). L1799 AI READY 1200/1400/30: evento lógico, no una nueva observación humana de guardia CP06. L1848 `CP04_BLACK_APPLIED rgb_word=08080AFF`; el color visible lo confirma el usuario.

L1864/1866/1867/1868: HP neta **150→110→70→30→0**. L1902/L1903 BLACK_RELEASED/AI RELEASED. L2287/L2288 SHUTDOWN/all mods unloaded.

**PASS HUMAN_OBSERVED** aparición/apariencia negra; **LOG_OBSERVED** configuración, HP150 y vida hasta cero. No prueba reentrada, FPS, otras salas ni seguridad universal.

### 2. Cambio en frío a native_elite sin recompilar

**Usuario:** «Ya apareció. No pasó nada extraño».

L64 `CONFIG_ACCEPTED placement_id=field_native variant_id=native_elite active=1`. L1795 admite actor147/gen1: es otra ejecución, no el actor concurrente ni el mismo ciclo vital del ensayo 1. L1796 `HP_NATIVE_PRESERVED old_hp=220 new_hp=220 NO_HP_WRITE`. L1871 HP neta **220→0**. L1889/L1890 SHUTDOWN/all mods unloaded.

**PASS HUMAN_REPORTED** aparición normal y ausencia de anomalías observadas. **LOG_OBSERVED** 220 HP preservado sin escritura. El cambio de JSON con cierre/reinicio, sin recompilar ni reinstalar el mismo .dusk, se atribuye al procedimiento reportado por el usuario; no se ha medido aquí un hash del archivo instalado en su PC. No se infiere un golpe único, arma, daño especial ni validación completa de IA nativa.

### 3. placements=[] con CP06 aún instalado

**Usuario:** «Ya lo probé. El enemigo desapareció».

L61–63 mantienen CP06 instalado/activo. L64 `CONFIG_ACCEPTED schema=1 placement_id=NONE variant_id=NONE active=0 max_active=1`. Configuración del ensayo: `placements=[]`; ninguna entrada activa. L1852 SHUTDOWN `edit_handle=0`; L1853 all mods unloaded.

**PASS HUMAN_OBSERVED** ausencia del añadido con JSON desactivado en un arranque frío; **LOG_OBSERVED** active=0. No es desinstalación, eliminación en vivo ni hot reload.

### 4. Restauración en frío de black_guard

L61 carga CP06 v0.6.0. L64 acepta field_black/black_guard active=1. L1800 admite actor147/gen1 en esta ejecución independiente (no se atribuye un admission_epoch que el resumen no aporta). L1801 HP220→150. L1852 BLACK_APPLIED `08080AFF`. L1869/1871/1872/1873 HP neta **150→110→70→30→0**. L1876/L1877 BLACK_RELEASED/AI RELEASED. L1881/L1882 SHUTDOWN/all mods unloaded.

Respalda restauración del preset negro en un nuevo arranque. No se presenta como salida/reentrada de sala en una misma sesión.

### 5. Retirada del .dusk y arranque posterior

Tras el protocolo de restaurar black_guard, cerrar y retirar CP06, el usuario confirmó: **«Ya lo hice. El enemigo desapareció»**. Ensayos 4 y 5 son dos ejecuciones distintas.

L61 `[INFO | dusk::mods::loader] no mods found`: no se carga ningún .dusk DEVF. L1843 all mods unloaded. El reporte humano acredita que visitó la zona y no estaba el enemigo adicional; `no mods found` sólo corrobora la retirada efectiva. Otros E_OC nativos no se confunden con residuos DEVF.

**CP06_ROLLBACK PASS HUMAN_OBSERVED**, limitado a este experimento: añadido con CP06/preset activo y ausencia tras retirada en frío. El shutdown de un mod activo, por sí solo, no habría acreditado desinstalación.

## Matriz de cierre posterior a la build

| Resultado | Estado | Límite |
| --- | --- | --- |
| Black_guard negro / HP150 / combate hasta HP0, sitio único | PASS HUMAN_OBSERVED (aparición/color) + LOG_OBSERVED (HP) | Ensayos 1 y 4; APPLIED no prueba píxeles por sí solo. |
| Native_elite nativo / 220 HP | PASS HUMAN_REPORTED + LOG_OBSERVED NO_HP_WRITE | Ensayo 2; no certificación de toda su IA. |
| Alternar presets por placements.json sin recompilar/reinstalar .dusk, con cierre/reinicio | PASS HUMAN_OBSERVED + CONFIG_ACCEPTED | Presets alternativos en el mismo sitio, no simultáneos; procedimiento aportado por usuario. |
| placements=[] con mod instalado y sin añadido | PASS HUMAN_OBSERVED + CONFIG_ACCEPTED active=0 | Ensayo 3; no hot reload ni uninstall. |
| Restaurar black_guard y retirar .dusk con juego cerrado | CP06_ROLLBACK PASS HUMAN_OBSERVED + LOG no mods found | Ensayos 4/5; ausencia en la zona atribuida al humano. |

**Recuento:** cinco logs de cinco ejecuciones; tres ciclos admitidos (1, 2, 4), cada uno actor147/gen1 en su proceso. No son generaciones globales 1/2/3 ni actores concurrentes. Dos HP_APPLIED220→150, un HP_NATIVE_PRESERVED220→220, tres secuencias netas hasta cero; dos BLACK_APPLIED y dos BLACK_RELEASED/AI RELEASED según los extractos suministrados. No convertir reducciones netas de HP en número de golpes, potencia bruta o identificación del arma.

Los mensajes compilados `visual=HUMAN_RUNTIME_NOT_TESTED` / `evidence=AI_EVENT_OBSERVED` siguen literalmente intactos. Este informe añade evidencia humana posterior; no reescribe el binario, los logs ni los estados históricos al compilar. No se extiende la prueba de CP05/CP04 a CP06.

## Procedencia del paquete preservado

| Identidad | Valor histórico |
| --- | --- |
| Commit técnico/documental base | `1a57ce17347d2f9c229af4c424d8b05a5ad59353` |
| Fuente efectivamente compilada | `107c79987b0d3d1d28319654739a72bd498271bb` |
| .dusk | `DEVF_CP06_PARTIAL_SINGLE_SITE_windows-amd64_107c79987b0d3d1d28319654739a72bd498271bb.dusk` — 41419 bytes |
| SHA256 .dusk | `b1e8f63797e93c0064e83fc39a984c1c806d046761f675b20ac55063b6a6dfa2` |
| ZIP TEST / SHA256 | 83222 bytes / `e79a0e76d3471530927ca169bbe4cbe107689b36200a63119ace012d261a10a1` |
| DLL / SHA256 | 77824 bytes / `45effe8a0ac9d56c3921c2cd6d0a27e9ea7017821559ef96b94b21ff390214e0` |

[Build histórico Windows/MSVC, 30 casos, PE/ABI y 7 negativos](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38690126831), CI `5ba8018f6af0e3d0b98af745d5cd0433d485955a`; [descarga independiente histórica](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38690375002), CI `0dcb9fade4cf48a136f210efc1c4a42cd3e5a4ba`: ambos SUCCESS por API. No son ejecuciones CI del juego ni pruebas nuevas del commit documental.

[Artifact privado histórico 11951843169](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38690126831/artifacts/11951843169): metadatos API confirman 83222 bytes, digest ZIP anterior y expiración **2026-11-14 01:04:00 Panamá / 06:04:00Z**. No se promete disponibilidad posterior ni se crea otro TEST. La identidad .dusk/DLL se conserva del ledger histórico, sin recálculo binario en esta tarea.

## Preservación, sello y recuperación

Rama documental hija `feature/devf-cp06-partial-human-runtime-closure`, padre exacto 1a57ce17…; cambios limitados a este informe y notas en README/HUMAN_TEST/TEST_RESULTS/RECOVERY. El árbol completo se compara por path/blob/mode/type con el padre: ningún archivo funcional, JSON, evidencia de build, paquete ni workflow autorizado a cambiar. Readback íntegro de los cinco Markdown y referencias finales se registra en el PR documental.

Tags históricos CP06 técnico, CP05 humano/técnico, CP04.4 humano/TEST y CP03 humano verificados por API (objeto anotado y destino). No se mueven ramas/tags históricos ni se modifica/mezcla PR37. Binarios/recursos/host/SDK/ROM/saves no se tocan.

**TAG_PENDING** para `DEVF_CP06_PARTIAL_SINGLE_SITE_HUMAN_RUNTIME_OBSERVED_2026-10-15`: ref inexistente en preflight; Cloud offline con `environment_startup_failed`, sin shell ni API de creación de tags anotados expuesta por el conector (fetch es GET; update_ref sólo branches). No se añade workflow ni se intenta retag. El commit y PR documental son el checkpoint recuperable. [RECOVERY](RECOVERY.md#cierre-humano-documental-2026-10-15) contiene comandos PowerShell y readback API requeridos; no declarar TAG_SEALED hasta obtenerlos.

## Pendientes conservados y handoff, sin implementación

- **NOT_IMPLEMENTED:** segundo sitio acreditado / XYZ libres; dos placements activos o dos actores DEVF simultáneos; correlación multiinstancia StageActorHandle→ActorId; scene epoch general e identificación robusta ante cambios de sala/reciclado.
- **NOT_VERIFIED / NOT_TESTED en juego:** reentrada específica CP06; yaw observado; JSON inválido runtime; casos adversariales/concurrentes. El laboratorio histórico de parser/límites sigue siendo evidencia offline separada.
- **PENDING:** home return walking, grace30 medido, guardia visual CP06, postura/remates, comparador E_OC2 retail idéntico mismo frame, contaminación de materiales con ese mismo modelo, terceros, FPS/frametime, otros GPUs y aislamiento universal. No son FAIL por falta de prueba. No se transfiere rollback CP06 a CP05.
- CP06 continúa **PARCIAL** pese a los cinco PASS. No se solicita repetir estos ensayos.

**Siguiente etapa propuesta, NO iniciada:** autorización independiente para correlación multiinstancia inequívoca (placement_id/handle/ActorId/generación/epoch) y acreditación de un segundo sitio. Gates: contrato fuente verificable sin heurística de proximidad; ownership/limpieza/anti-duplicados y fallos parciales; evidencia geométrica concreta del sitio; tests del core compartido/retail/IDs reciclados; build Windows y paquete/descarga independientes de una nueva versión; después ensayo humano controlado de dos ubicaciones/instancias. Riesgos: admisión ambigua, lectores diferidos, duplicados, transición de sala y sobrecarga; mantener max1 y whitelist actuales hasta resolverlos. No hay código nuevo, CP07/08, Enemy Posture System ni Bokoblin Expansion iniciados en este cierre.
