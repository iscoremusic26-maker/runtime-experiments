# Puerta documental V1 — investigación estática

Dictamen CP-R98: **V1_READY_STATIC_ONLY**. La puerta se satisface como referencia general selectiva del motor y SDK del pin,no como investigación exhaustiva ni certificación de compatibilidad. Base de sesión CP-R93 `240a8b7f498618d4c919db0199159ff2eb3af359`;padre remoto CP-R97 `967925cf72933b36cecff5181d543cff9a068969`. Consultar el ref/commit actual y [CONTINUATION](CONTINUATION.md) para la publicación propia;no se inventa SHA autorreferente. No tag/release/PR/merge ni integración con otro asistente.

El objetivo conceptual es Windows x64/DX12/GZ2E01 USA;la fuente única es TwilitRealm/dusklight@40457c6adb381928e4b5fef6ed459ed291edd5e2,tree e4b79b565b2842f711f7c9f2390f56ef11063157. V1 permite localizar contratos,mecanismos representativos,ownership,error y pendientes. No significa28 sistemas completos,452 hooks,209 slots auditados o ABI Windows medido.

## Criterios I–VIII y sustento del dictamen

| Criterio | Resultado documental | Sustento / límite |
| --- | --- | --- |
| I. Pin,plataforma,excepciones | Satisfecho | [SOURCE_PIN](SOURCE_PIN.md) y blobs protegidos coincidentes con CP-R93. Cuatro gitlinks ausentes y Android excluido explícitos. CP-R94/C03 contrastan13 blobs puntuales al pin;no nueva auditoría R00. |
| II. Arquitectura y mecanismos localizables | Satisfecho | [README](README.md),[índice](SYSTEM_INDEX.json),[guía](ATLAS_GUIDE.md),[SDK](SDK_AND_SERVICES.md),[matriz](DUSK_INTEGRATION_MATRIX.md) y [dependencias](SYSTEM_DEPENDENCIES.md) conectan loader/SDK/memoria/actor-stage/recursos/eventos/save/UI/audio/render/mundo. Servicio oficial se prefiere solo donde cubre el contrato. |
| III. 28 registros/24 fichas,scope honesto | Satisfecho al alcance definido | Todos con scope/pending/paths/reports;24 fichas indexadas y enlazadas.54 archivos navegables desde README por enlaces/índice.18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED sin promoción. No se afirma lectura profunda de cada path. |
| IV. Brechas críticas y externas | Satisfecho documentalmente | C01 clasificación/auditoría,C02 guía y C03 consistencia resueltos. Matriz de seis READ abajo mantiene mejoras diferibles. Backends/ABI y assets necesarios para garantías externas siguen bloqueados o pendientes;V1 estática no depende de inventarlos. |
| V. Auditoría semántica enfocada | Satisfecho,selectivo | [AUDIT_FINDINGS](AUDIT_FINDINGS.md):dos etiquetas oficiales corregidas con traza WORLD-021/033;cinco TYPED_HOOK conservados por procedencia;versiones UI/Game/Save/Luau y tamaño/ownership delimitados. No reaudita452 cadenas o209 slots. |
| VI. Coherencia,validación y persistencia | Satisfecho por el procedimiento comprobado de CP | [Reporte](VALIDATION_REPORT.json),[métricas](RESEARCH_METRICS.json),[changelog](CHANGELOG.md),[handoff](CONTINUATION.md). Validador protegido exit0;checks complementarios de navegación/URLs/clasificación,lease,parent/tree/diff/readback remoto. El commit actual debe superar esa misma verificación antes de reportarse publicado. Ningún PASS runtime. |
| VII. Limitaciones y ausencia de certificación | Satisfecho | Cuatro gitlinks;Android;209 slots localizados,no auditados todos;357 POTENTIAL al inicio,360 ahora;0 pruebas runtime/ABI/exports Windows. Datos GC/Wii/STATIC_ASSERT no miden layoutPC. Ver límites abajo. |
| VIII. Guía y mantenimiento reanudable | Satisfecho | [Guía](ATLAS_GUIDE.md) y [CONTINUATION](CONTINUATION.md) permiten consulta por capacidad y pregunta pequeña. No hay CP técnico obligatorio pendiente para declarar esta versión documental. Investigación posterior motivada por una necesidad concreta,sin barrido masivo ni integración Claude. |

V1-C01/02/03 son tareas de cierre documental,no niveles de evidencia. CP-R95/96/97 registraron V1_NOT_READY mientras faltaban;CP-R98 conserva esa historia y cambia el dictamen al satisfacer la puerta. Ninguna pregunta técnica se cierra por esta decisión.

## Seis áreas READ: utilidad existente y brechas por impacto

Las cuatro clases siguientes priorizan trabajo,**no son nuevos niveles de evidencia o cobertura**. Se consultaron scopes/pending del índice y claims/limitaciones de las fichas, evidencias y preguntas enlazadas;no se reauditaron todos los rangos históricos.

| Área READ / ruta | Cadena útil ya respaldada | Brecha e impacto .dusk | Clase y efecto sobre V1 |
| --- | --- | --- | --- |
| [HUD/UI/texto](systems/hud_ui_text.md) | BFN compartido→pane→liberación (PRES-036..039);loader TextBoxEx→material/buffer→draw/cleanup (PRES-056..059);BMG→Explain (PRES-068..073);UiService en CALLBACK-032..034/047..049 | Charsets/refresh, assets TBX2 y medidores dinámicos no completos. No presentar UIhost Rml como API de panes J2D. Paso mínimo según necesidad:seguir estado de un medidor a draw, antes de recomendar intervención. | **MEJORA DIFERIBLE** técnica;**V1-C02 realizado** para la distinción de mecanismos en guía. Las muestras de texto ya permiten orientarse. |
| [Modelos/materiales](systems/models_animations_materials.md) | AutoMata BCK/BTK, PRES-044..047;skin, PRES-102..105;BTP/BRK/BPK, BLS/BLK, packets y filmPRES-160/161 | LOD/BVA sin consumidor cerrado, assets/sharing/alloc/GPUdrain pendientes. Paso mínimo:tabla de propiedad ModelData/modelo/animador/ARC y selección de rutas;no otra variante por volumen. | **MEJORA DIFERIBLE** de cobertura;la guía de propiedad de **V1-C02 está publicada**. No afirmar soporte universal de formatos. |
| [Otros sistemas](systems/other_systems.md) | Swpush, MYNA2, B_DS, Sekizoa, Bombf, DigPlace, Rollgoal y pesca LURE con resultados/cleanup delimitados | Secuencias de assets/compañeros, recompensas y durabilidad dependen del caso. Sekizoa es guardianes/saltos de Link;sin Cetro del Dominio en la cadena. Paso mínimo:consultar muestra comparable y su límite;leer nueva familia solo ante pregunta concreta. | **MEJORA DIFERIBLE**. Catalogar todos los NPC, puzzles o minijuegos **NO REQUERIDO PARA V1**. |
| [Entorno](systems/environment_weather_time.md) | Reloj, tags de color/viento/niebla, nieve, olor y agua con consumidores/cleanup selectivos | Arbitraje global y room unload/PRES-089 no resueltos;assets/orden necesarios para afirmar alcanzabilidad. KYTAG09 se excluye del clima en CP-R94. Paso mínimo si se requiere:colocación y escritor concreto, gates de retiro y consumidor vivo. | **MEJORA DIFERIBLE** y validación posterior condicionada a assets;no usar pendiente como prueba de UAF. No bloquea atlas estático con riesgo explícito. |
| `platform_backend`: [pin](SOURCE_PIN.md),[ABI](HOOKING_AND_ABI.md),[memoria](systems/memory_ownership.md) | Fronteras host/SDK, heaps y contratos;GameService es época ABI, no tabla arbitraria de engine | Aurora/Borealis/cosmetics/randomizer ausentes al SHA gitlink. No se conocen DX12, IO, drain/atomicidad ni DLL de distribución concreta. Paso mínimo futuro:fuente exacta necesaria o evidencia de imagen/biblioteca/manifiesto, con autorización distinta para pruebas. | **BLOQUEO EXTERNO / BLOCKED_BY_EXTERNAL_SOURCE** de esas garantías. No impide V1 estática si no se inventan;build/runtime **NO REQUERIDOS PARA V1** y prohibidos en esta campaña. |
| `port_support`: [mapa en README](README.md),[dependencias](SYSTEM_DEPENDENCIES.md) | Logros, LiveSplit, presencia, comandos, diagnóstico de disco, ring/stublog y ControllerConfig | Host interno no equivale a servicio SDK;ACK, backend y configuración durable no certificados. Paso mínimo:mapa APIoficial/interno/fronteraexterna;sin cuentas, logs, archivos o dispositivos personales. | **MEJORA DIFERIBLE** de cobertura;**V1-C02** publica mapa de mecanismos. Backend es **BLOQUEO EXTERNO**, no invitación a probar red. |


## Resultado de la auditoría y cifras

[Auditoría enfocada y C03](AUDIT_FINDINGS.md) documenta qué se corrigió y qué solo se comprobó estructuralmente. 2916 URLs de índices coinciden con sus campos;128 url opcionales ausentes no rompen trazabilidad. No se afirma auditoría semántica exhaustiva por validar JSON. CI histórica conserva repo/SHA/jobs propios y no se promueve a juego ejecutado.

| Unidad | CP-R93 inicial | CP-R98 | Delta |
| --- | ---: | ---: | ---: |
| Evidencias | 521 | 523 | +2 (PRES-160/161) |
| Símbolos | 451 | 452 | +1 (daKytag09_Draw) |
| Ocurrencias de rangos citados | 5703 | 5740 | +37 |
| Rangos únicos | 2689 | 2702 | +13 |
| Archivos upstream citados | 442 | 444 | +2 |
| Fichas de sistemas | 24 | 24 | 0 |
| Archivos del atlas | 51 | 54 | +3 documentos complementarios |
| MD/JSON comprobados | 47 | 50 | +3 |

Evidencia final:428 STATIC_CROSSCHECKED,50 SOURCE_OBSERVED,5 DOC_CONTRACT,38 STATIC_INFERRED,2 CI_OBSERVED. Símbolos:87 OFFICIAL_SERVICE,360 POTENTIAL_REQUIRES_VERIFICATION,5 TYPED_HOOK. Dos oficiales pasaron a potencial en CP-R96;el potencial adicional viene de CP-R94. CP-R95..98 son mejoras editoriales,sin nuevos IDs o símbolos. Citas nuevas no se cuentan como nuevas cadenas.

## Limitaciones permanentes y mantenimiento

- Cuatro fuentes gitlinked ausentes:Aurora,Borealis,cosmetics,randomizer. Internals DX12/IO/drain/atomicidad no certificados. BLOCKED_BY_EXTERNAL_SOURCE aplica a esas garantías,no al atlas entero.
- Excepción Android documentada y excluida. Pin e inventario R00/siete erratas se conservan íntegros. No se homologan versiones,regiones ni distribuciones binarias por analogía.
- Contratos oficiales no acreditan backend ni éxito posterior. Solicitud/aceptación/creación/ejecución/cleanup/durabilidad son hitos distintos;unregister no prueba callback drenado,Delete no GPU idle,overlay retirado no consumidor restaurado.
- 25 contratos C,26 módulos candidatos,209 slots localizados;profundidad desigual. No se auditaron452 callchains ni todos los actores,materiales,charsets,LOD o arbitrajes ambientales. Se mantienen seis áreas READ y cuatro INVENTARIED.
- ABI,export/manifiesto,target,layoutWindows,convivencia y unload requieren evidencia concreta que esta campaña no ejecutó.0 builds,juego,integrationruntime y pruebas humanas nuevas. Ninguna inferencia condicionada es crash/UAF/fallo visual reproducido.
- Conservar PRES-089/111/118/122/126/134/139/146/150,PLAYER-095/106,CALLBACK-045,ARCH-020/028,WORLD-046/050 y demás pendientes de [riesgos](RISK_REGISTER.md)/[preguntas](OPEN_QUESTIONS.md). No borrar incertidumbres para embellecer el dictamen.

La siguiente investigación empieza por una pregunta real y su contrato/consumidor;si falta evidencia,actualizar límite. El candidato diferible HUD dinámico se deja acotado en handoff,no como condición retrospectiva de V1. No hacer tag/release/merge/PR ni preparar integración con Claude. No hay trabajo en segundo plano.

NO MOD IMPLEMENTED / NO BUILD PERFORMED / NO GAME RUNTIME CLAIMED / NO PRODUCTION MODIFIED / NO CLAUDE INTEGRATION.
