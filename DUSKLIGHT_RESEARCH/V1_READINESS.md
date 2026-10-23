# Puerta documental V1 — investigación estática

Estado en CP-R95: **V1_NOT_READY**. Base de la auditoría: CP-R93 `240a8b7f498618d4c919db0199159ff2eb3af359`, ampliada por CP-R94 `e4d713d7c2d85d74a9fcf02dfc026ac6fe5677da`. Falta terminar la revisión semántica enfocada y la guía de consulta;no se pide investigar exhaustivamente el motor para satisfacer esta puerta.

V1 significa referencia general de mecanismos representativos del pin `40457c6adb381928e4b5fef6ed459ed291edd5e2`, objetivo Windows x64/DX12/GZ2E01 USA. No significa 28 sistemas completos,451 hooks operativos,209 slots auditados o compatibilidad runtime. No release/tag/merge/PR ni integración con otro asistente.

## Criterios de aceptación y trabajo restante

| Criterio | Estado CP-R95 | Sustento / cierre mínimo |
| --- | --- | --- |
| I. Pin, plataforma y excepciones | Documentado | [SOURCE_PIN](SOURCE_PIN.md):árbol fijo, certificación histórica, cuatro gitlinks y Android excluido. Blobs protegidos conservados;no rehacer R00. |
| II. Arquitectura y rutas generales localizables | Base comprobada;guía pendiente | [README](README.md),[sistemas](SYSTEM_INDEX.json),[SDK](SDK_AND_SERVICES.md),[matriz](DUSK_INTEGRATION_MATRIX.md). Explicar cómo elegir servicio/recurso/helper sin asumir API de gameplay. |
| III. 28 entradas /24 fichas, scope y pendientes | Comprobación estructural realizada | Todos los registros tienen scope, pending, reports y paths no vacíos;24 fichas están indexadas y enlazadas desde README. READ permanece READ. La revisión no significa leer todo archivo listado. |
| IV. Brechas críticas delimitadas | Matriz inicial abajo | Los bloqueos externos no impiden un atlas estático si se preservan como límites. No exigir toda pesca/LOD/JUTCacheFont para declarar utilidad documental. |
| V. Auditoría semántica de riesgos | PENDIENTE, crítico V1-C01 | Revisar cinco TYPED_HOOK, clasificaciones oficiales de mayor riesgo y afirmaciones de tamaño/ownership/plataforma. Contrastar solo rangos necesarios y registrar correcciones o conservación. |
| VI. Consistencia y publicación | Por checkpoint;final pendiente V1-C03 | Validador existente+diff/lease+readback. Verificar al final métricas, navegación y nueve blobs protegidos;ningún PASS runtime. |
| VII. Limitaciones explícitas | Documentadas aquí y en pin | Cuatro gitlinks, Android,209 slots localizados,357 POTENTIAL al inicio,0 runtime/ABI/export medido. Los conteos actuales pueden cambiar sin transformar localizadores en hooks. |
| VIII. Guía y handoff mantenibles | PENDIENTE, crítico V1-C02 | Guía corta por capacidad y mantenimiento;primera acción exacta en [CONTINUATION](CONTINUATION.md). No volver a recorrer actores arbitrarios. |

V1-C01/02/03 son tareas documentales de cierre, no tres checkpoints prometidos ni bloqueos técnicos nuevos. La falta de una auditoría terminada justifica V1_NOT_READY hoy;los pendientes diferibles no deben prolongarla artificialmente.

## Seis áreas READ: utilidad existente y brechas por impacto

Las cuatro clases siguientes priorizan trabajo,**no son nuevos niveles de evidencia o cobertura**. Se consultaron scopes/pending del índice y claims/limitaciones de las fichas, evidencias y preguntas enlazadas;no se reauditaron todos los rangos históricos.

| Área READ / ruta | Cadena útil ya respaldada | Brecha e impacto .dusk | Clase y efecto sobre V1 |
| --- | --- | --- | --- |
| [HUD/UI/texto](systems/hud_ui_text.md) | BFN compartido→pane→liberación (PRES-036..039);loader TextBoxEx→material/buffer→draw/cleanup (PRES-056..059);BMG→Explain (PRES-068..073);UiService en CALLBACK-032..034/047..049 | Charsets/refresh, assets TBX2 y medidores dinámicos no completos. No presentar UIhost Rml como API de panes J2D. Paso mínimo según necesidad:seguir estado de un medidor a draw, antes de recomendar intervención. | **MEJORA DIFERIBLE** técnica;**CRÍTICA PARA V1-C02** la distinción de mecanismos en guía. Las muestras de texto ya permiten orientarse. |
| [Modelos/materiales](systems/models_animations_materials.md) | AutoMata BCK/BTK, PRES-044..047;skin, PRES-102..105;BTP/BRK/BPK, BLS/BLK, packets y filmPRES-160/161 | LOD/BVA sin consumidor cerrado, assets/sharing/alloc/GPUdrain pendientes. Paso mínimo:tabla de propiedad ModelData/modelo/animador/ARC y selección de rutas;no otra variante por volumen. | **MEJORA DIFERIBLE** de cobertura;la guía de propiedad es parte de **V1-C02**. No afirmar soporte universal de formatos. |
| [Otros sistemas](systems/other_systems.md) | Swpush, MYNA2, B_DS, Sekizoa, Bombf, DigPlace, Rollgoal y pesca LURE con resultados/cleanup delimitados | Secuencias de assets/compañeros, recompensas y durabilidad dependen del caso. Sekizoa es guardianes/saltos de Link;sin Cetro del Dominio en la cadena. Paso mínimo:consultar muestra comparable y su límite;leer nueva familia solo ante pregunta concreta. | **MEJORA DIFERIBLE**. Catalogar todos los NPC, puzzles o minijuegos **NO REQUERIDO PARA V1**. |
| [Entorno](systems/environment_weather_time.md) | Reloj, tags de color/viento/niebla, nieve, olor y agua con consumidores/cleanup selectivos | Arbitraje global y room unload/PRES-089 no resueltos;assets/orden necesarios para afirmar alcanzabilidad. KYTAG09 se excluye del clima en CP-R94. Paso mínimo si se requiere:colocación y escritor concreto, gates de retiro y consumidor vivo. | **MEJORA DIFERIBLE** y validación posterior condicionada a assets;no usar pendiente como prueba de UAF. No bloquea atlas estático con riesgo explícito. |
| `platform_backend`: [pin](SOURCE_PIN.md),[ABI](HOOKING_AND_ABI.md),[memoria](systems/memory_ownership.md) | Fronteras host/SDK, heaps y contratos;GameService es época ABI, no tabla arbitraria de engine | Aurora/Borealis/cosmetics/randomizer ausentes al SHA gitlink. No se conocen DX12, IO, drain/atomicidad ni DLL de distribución concreta. Paso mínimo futuro:fuente exacta necesaria o evidencia de imagen/biblioteca/manifiesto, con autorización distinta para pruebas. | **BLOQUEO EXTERNO / BLOCKED_BY_EXTERNAL_SOURCE** de esas garantías. No impide V1 estática si no se inventan;build/runtime **NO REQUERIDOS PARA V1** y prohibidos en esta campaña. |
| `port_support`: [mapa en README](README.md),[dependencias](SYSTEM_DEPENDENCIES.md) | Logros, LiveSplit, presencia, comandos, diagnóstico de disco, ring/stublog y ControllerConfig | Host interno no equivale a servicio SDK;ACK, backend y configuración durable no certificados. Paso mínimo:mapa APIoficial/interno/fronteraexterna;sin cuentas, logs, archivos o dispositivos personales. | **MEJORA DIFERIBLE** de cobertura;**V1-C02** exige mapa de mecanismos. Backend es **BLOQUEO EXTERNO**, no invitación a probar red. |

## Comprobaciones realizadas y límites

CP-R95 comprobó en el índice actual:28 IDs, scope/pending/reports/paths presentes;reports apuntan a archivos existentes;las24 fichas de systems están en el índice y en enlaces directos de README. Esta comprobación complementaria leyó JSON y rutas locales con blobs documentales coincidentes con GitHub;no se atribuye al validador protegido, que no comprueba esos campos semánticamente.

Se corrigieron pendientes que podían sugerir ausencia total de TextBoxEx/BMG o skin pese a sus muestras contrastadas;se precisó READ global de other_systems y las rutas de platform_backend. No cambió ningún nivel canónico. Preservar preguntas Q-01..14 y riesgos históricos:retirada no drena callbacks, request no crea escena, estado RAM no es disco, overlay no recarga consumidor y localizador no es export Windows.

El validador verifica referencias/estructura, no veracidad exhaustiva. Históricos CI conservan su repo/SHA/jobs;no se convierten en pruebas Windows de esta campaña. Los riesgos STATIC_INFERRED necesitan sus supuestos;no son defect reports reproducidos.

## Limitaciones permanentes y mantenimiento

Fuente completa de backends ausente, excepción Android excluida, ABI/exports/hook instalable no certificados,209 slots no auditados uno por uno y cobertura selectiva. No ejecutar juego, build, red o acceder a datos personales para cerrar esta puerta. Nuevos proyectos deberán comprobar su imagen, contrato, fase, ownership y rollback;no heredan compatibilidad del atlas.

Actualizar este dictamen solo tras V1-C01/02/03 con enlaces a sus resultados y commit remoto verificado. V1_READY_STATIC_ONLY sería un dictamen documental, no release, autorización de mod o integración con Claude. No ejecución en segundo plano.
