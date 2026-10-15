# CP05 — Cierre humano observado, 2026-10-15 (America/Panama)

**CP05_AI_BOUNDED_HUMAN_RUNTIME_OBSERVED**, limitado a detección cercana y cese de persecución reportados, reaparición normal reportada y combate/HP hasta cero según el log analizado en ChatGPT. No acredita regreso caminando a home, pathfinding ni todo CP05.

## Procedencia y alcance

| Etiqueta | Significado en este cierre |
| --- | --- |
| REPO_VERIFIED | Referencias, documentos y árboles Git leídos por Codex mediante integración GitHub. Base técnica exacta7a7c8bc34841e6f85020cca93ff591e9cb9e789d; no modificación funcional. |
| CI_VERIFIED (histórico) | [Build38672691356](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38672691356) y [descarga38672879974](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38672879974) releídos por API como SUCCESS.29 casos y6 negativos son evidencia técnica histórica, no ejecución CI del juego. |
| USER_LOG_ANALYZED_IN_CHATGPT | Hechos, líneas y eventos siguientes proceden del resumen del log adjunto al usuario en ChatGPT y aportado explícitamente en el encargo. Codex no recibió ni leyó aquí los bytes originales. |
| CHATGPT_VERIFIED_FROM_USER_ATTACHMENT | Tamaño/hash/recuento de líneas calculados previamente en ChatGPT según el usuario. Procedencia atribuida, no comprobación local nueva de Codex. |
| USER_HUMAN_REPORTED | Declaraciones expresas del usuario sobre detección cercana, desistimiento y reaparición. Se conserva su alcance literal. |
| RUNTIME_NOT_TESTED / NOT_VERIFIED / PENDING | Comprobaciones específicas sin evidencia suficiente; no equivalen a FAIL. No se heredan pruebas humanas CP04.4. |

Codex no ejecutó el juego, no inspeccionó píxeles ni capturas nuevas y no recalculó el hash del log. No se archivan raw logs/capturas/rutas personales en Git.

## Identidad del log privado

- Nombre original: `dusklight-20261015-002029.log`.
- Tamaño suministrado: **349987 bytes**.
- SHA256 suministrado: `4be5680cb8a119e7264339b6a134496b95fcd7cb8b509e02f65e321c1980385c`.
- Recuento físico suministrado (`wc -l`): **4518**. Un visor puede mostrar una línea terminal adicional; los índices citados abajo se conservan, sin fingir recalcularlos.

L2: Dusklight2.0.3, fuente/build40457c6adb381928e4b5fef6ed459ed291edd5e2. L14–23: D3D12 / Intel UHD Graphics. L61–66: dev.devf.cp05_ai_guard v0.5.0, **1/1 mods activos**. Escenario F_SP121 / room3 / layer6. El EXE SHA de referencia permanece en BUILD_AND_PACKAGE; este cierre no acredita una lectura nueva del EXE instalado.

## Dos generaciones secuenciales, nunca concurrentes

Todas las entradas de la tabla pertenecen a USER_LOG_ANALYZED_IN_CHATGPT.

| Hecho | Actor147 / generation1 / epoch1 | Actor566 / generation2 / epoch2 |
| --- | --- | --- |
| HP_APPLIED220→150 | L1794; PRE_FIRST_EXECUTE; result0 | L4186 |
| CP05_AI READY | L1796; entry1200/exit1400/grace30 | L4188; mismos valores |
| CP04_BLACK_APPLIED | L1848; rgb_word08080AFF | L4217; rgb_word08080AFF |
| STATE_ENTER | L1861; NATIVE_FIND_OBSERVED; distancia²94224.2; outside_updates0 | L4222; NATIVE_FIND_OBSERVED; distancia²1318119.8 (raíz aprox1148.1<1200); outside_updates0 |
| STATE_EXIT tras entrada | L1862; ACTION_NATIVE_PRIORITY | L4223; ACTION_NATIVE_PRIORITY |
| Otras salidas lógicas | L1815/L1853/L1867/L1868 incluyen EVENT_NATIVE_PRIORITY y HOME_GUARD_REARM | L4208/L4215: EVENT_NATIVE_PRIORITY/HOME_GUARD_REARM |
| Secuencia HP neta | L1863/L1865/L1869/L1871:150→110→70→10→0 | L4228:150→0, una diferencia neta |
| CP04_BLACK_RELEASED | L1873 | L4231 |
| CP05_AI RELEASED | L1874; salida externa finalL1875 | L4232 |

Totales de los eventos identificados: **2 HP_APPLIED,2 READY,2 STATE_ENTER,2 BLACK_APPLIED,2 BLACK_RELEASED y2 AI RELEASED; ambas generaciones llegan a0 HP**. Son generaciones secuenciales; la salida/reentrada se atribuye al usuario y es compatible con actor566/gen2/epoch2.

L4516–4517 registran HP_SUMMARY y SHUTDOWN. Esto acredita el cierre registrado del mod, **no su desinstalación**. HP_DELTA representa diferencias netas, no potencia bruta, causa/arma ni cantidad exacta de golpes. RELEASED registra retiro lógico del seguimiento; no certifica toda allocation del host.

## Declaraciones humanas y matriz posterior al TEST

> «Se notó que solo reaccionaba cuando estaba muy cerca de él».

> «Y también cuando me alejé perdió el interés rápido».

> «Ya hice la prueba de la reaparición también. Todo fue normal».

Ante la pregunta específica «Cuando te alejaste y el Bokoblin perdió el interés, ¿regresó caminando a la zona donde estaba originalmente o simplemente dejó de perseguirte?», el usuario respondió:

> «Dejó de perseguir».

| Comprobación | Dictamen limitado | Evidencia / límite |
| --- | --- | --- |
| Detección cercana | PASS HUMAN_OBSERVED / USER_HUMAN_REPORTED | Sin medición manual del umbral exacto1200 ni control de todos los disparadores nativos |
| Cese de persecución al alejarse | PASS HUMAN_OBSERVED / USER_HUMAN_REPORTED | No demuestra regreso caminando, causalidad exclusiva del piloto ni contador30 |
| Reaparición normal | PASS HUMAN_REPORTED | Declaración explícita y nueva identidad566/gen2/epoch2 |
| HP150 y combate/muerte hasta HP0 | LOG_OBSERVED / USER_LOG_ANALYZED_IN_CHATGPT | Ambas generaciones; no certificación universal de combate/animación |
| Recoloreado CP05 | COMMAND_WORD_READBACK | BLACK_APPLIED08080AFF en ambas; sin nueva prueba de píxeles independiente |
| Regreso caminando al origen | **HOME_RETURN_WALKING_NOT_VERIFIED** | La respuesta fue sólo «Dejó de perseguir» |
| Navegación, camino de regreso, obstáculos | NOT_VERIFIED | No inferir de STATE_EXIT, HOME_GUARD_REARM ni cese de persecución |
| Periodo de30 updates fuera de rango | **30_UPDATE_GRACE_NOT_DIRECTLY_VERIFIED** | No evento explícito outside_updates30/ReturnNative en este log; no convertir updates a segundos |
| Desinstalación / cold rollback CP05 | **CP05_ROLLBACK_PENDING** / NOT_REPORTED | SHUTDOWN no lo demuestra; rollback CP04.4 no se transfiere a CP05 |
| Original E_OC2 idéntico, simultáneo/mismo frame | **SAME_MODEL_EOC2_SIMULTANEOUS_PENDING** | Ningún control equivalente nuevo suministrado |
| Otros enemigos/aislamiento visual universal CP05 | NOT_VERIFIED | No trasladar observaciones CP04.4 a este TEST |
| FPS/frametime, terceros, otras GPU/escenarios | RUNTIME_NOT_TESTED | **NO_UNIVERSAL_ISOLATION/PERFORMANCE_CERT** |

Según el análisis suministrado, no aparece la línea literal `[ERROR]`. No se transforma esa ausencia en ausencia de cualquier advertencia/error posible ni en certificación de estabilidad. STATE_ENTER/FIND es transición lógica: la observación visual de la persecución se atribuye a las declaraciones del usuario.

Los mensajes embebidos `visual=HUMAN_RUNTIME_NOT_TESTED` y `evidence=AI_EVENT_OBSERVED` permanecen literalmente intactos. Eran clasificación de la build y no se editan retroactivamente: este documento registra evidencia humana posterior.

## Procedencia técnica y paquete inalterable

- Fuente realmente compilada: `ec61daa3ed7d539989028cd26b22fa529896de11`.
- CI compilación: `efd8a49ec7b4bcb444bf510c5a9173a92386ce97`; CI descarga: `41396f1fe17120b0f95e2ae0da4abc9c2866821e`.
- Checkpoint técnico sellado: `7a7c8bc34841e6f85020cca93ff591e9cb9e789d`.
- Mod `dev.devf.cp05_ai_guard`, versión0.5.0: sin cambios.

| Elemento histórico | Bytes | SHA256 histórico, no recalculado sobre binarios en este cierre |
| --- | ---: | --- |
| DEVF_CP05_AI_GUARD_windows-amd64_ec61daa3ed7d539989028cd26b22fa529896de11.dusk | 18929 | 23f81ad131082a03fcd66068ccd926ecf878182a5afce06244898cf663248ddb |
| ZIP TEST | 52452 | c5df6dcbd0f440e096c5c4048f2c3c97476ed6cb1234c9587e2df0a6317914bc |
| DLL interna | 34816 | 830577e71543301f5ca672094caeb5c54103d61e85a23f01e2ba39074565f509 |

[Artifact privado11945045896](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38672691356/artifacts/11945045896). La metadata API releída coincide en bytes/digest del ZIP y expired=false. Vence **2026-11-13 21:46:49 America/Panama**, UTC2026-11-14T02:46:49Z; sin promesa posterior. No descarga binaria, nuevo build, laboratorio, PE, repack ni TEST en esta tarea. Los registros técnicos históricos y las capas internas siguen en [BUILD_AND_PACKAGE](BUILD_AND_PACKAGE.md).

## Recuperación y estado del sello documental

Rama hija `feature/devf-cp05-ai-bounded-human-runtime-closure`, base exacta7a7c8bc34841e6f85020cca93ff591e9cb9e789d. El commit documental y PR draft nuevos se publican y se releen por GitHub; sus SHA literales quedan en PR/chat. Sólo cinco Markdown de esta carpeta son elegibles para el cierre: este informe y notas en README/HUMAN_TEST/TEST_RESULTS/RECOVERY. La auditoría por árboles completos verifica cada blob/mode; no se cambian fuentes, core, CMake, manifest, CI, workflow, assets, evidencia JSON ni binarios. PR34/rama técnica no reciben escrituras.

Refs históricos comprobados:

- CP05 PRIVATE_TEST_READY objeto83b2cea8815a8c01b29ad1f3df2a3731f7b667f4 →7a7c8bc34841e6f85020cca93ff591e9cb9e789d.
- CP04.4 HUMAN_RUNTIME_OBSERVED objetof21d0d95e0fc7d5fcbca15ae17ba6b50cdee564e →f7a6623f6d931bacef6f2c8e54f46f7476780ade.
- CP04.4 PRIVATE_TEST_READY objeto21f9abb6b8dec176cc8b56d2652fb56a797ba45b →0a2ec044cbae476c6ca8f3e5387737791875f47c.
- CP03 humano objeto08ffbae5e5da73658df77b3763de2fe6851f7a45 →139d9329f7a2d5d191b6e0ef7149ac9bbf82d29f.

Tag propuesto `DEVF_CP05_AI_BOUNDED_HUMAN_RUNTIME_OBSERVED_2026-10-15`: **TAG_PENDING, no publicado**. Cloud sigue environment_startup_failed/offline y no hay shell ni herramienta de creación de tags anotados/refs de tags. El workflow CP05 existente fija el nombre PRIVATE_TEST_READY, la rama técnica y la base CP04; no es compatible con el sello humano. No se modifica ni ejecuta. No se crea un workflow nuevo o mecanismo genérico. Los comandos mínimos para completar sólo el tag desde un clon autorizado están en [RECOVERY](RECOVERY.md). Esta limitación administrativa no invalida el commit recuperable ni las observaciones humanas.

No se solicita repetir la prueba para cerrar este encargo. Los pendientes permanecen documentados; no se declara FAIL por falta de evidencia. **CP06 no iniciado; esperar autorización expresa**. Bokoblin Expansion, editor y nuevas conductas fuera de alcance.
