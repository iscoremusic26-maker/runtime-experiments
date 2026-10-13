# G4 — cierre de revisión estática focalizada

**G4_RESOURCE_VERIFIED_POSITION_BLOCKED — NO_SAFE_POSITION_VERIFIED.** Mejoran procedencia y contexto, pero no se admite una ubicación con dominio condicionado suficiente. DISARMED_NO_REGISTRATION, G5/CP02 NO-GO. El tag identifica una revisión recuperable, no un PASS global.

| Requisito/gate | Estado | Evidencia y límite |
|---|---|---|
| Recursos originales E_oc/E_ocb | PASS_STATIC conservado | Hashes, índices, estructuras, modelos/28 BCK del checkpointdc2f65a; sin nueva descarga/decodificación |
| Overlays de mods aplicados en G2 por el servicio | **PASS_RUNTIME_LOG + PASS_STATIC** | Una sincronización0 L70, sin otra en log completo; el servicio cuenta paquetes y runtime slots y reemplaza el conjunto FST |
| Capacidad de overlays dinámicos | PASS_STATIC | Existe, sincroniza cambios; no se convierte la capacidad en un override observado |
| Reemplazos de textura | PASS_RUNTIME_LOG para registros; PASS_STATIC del mecanismo distinto |1867 registros, no cambios ARC demostrados; baseline sigue no aislado |
| Correspondencia byte por byte de recursos cargados | PARTIAL / NOT_VERIFIED | Disco GZ2E01 reportado, ARC comprobados y ausencia de overlays; sin hashes de carga/memoria. Límite runtime, no único bloqueo de ubicación |
| Envolvente401/494/501 | PASS_STATIC matemático condicionado | Resultados anteriores intactos; no certificado de F32/JMath/render/HIO efectivo/origen móvil |
| Suelo/colisiones locales | PASS_STATIC conservado | Acch100/proyección501 y separación a paredes/externos dentro del alcance anterior; no consulta repetida de31 prismas |
| Pies/navegación/agua | PARTIAL / NOT_VERIFIED | Acch y consultas especiales no son IK/garantía de todo el recorrido; pendiente vincular poses/medio al caso efectivo |
| Flujo inicial y detección | PASS_STATIC | WAIT inicial con triggers prioritarios, paseo espontáneo,3D/FOV/LOS, ruido/aliados/daño y cambios de estado identificados |
| Primer WALK voluntario | PARTIAL; cota matemática condicionada≤800 | Horizonte≤200 integraciones avelocidad≤4 bajo guardas; excluye empujes/Acch/estados alternos, no región segura admitida |
| Dominio condicionado de observación | **BLOCKED / NOT_VERIFIED** | Guardas sensores/actores globales/medio/contexto no acreditadas; no confinamiento o inmovilidad inventados |
| Ubicación antigua y alternativas en cache | **BLOCKED / NO_SAFE_POSITION_VERIFIED** | Referencia evaluada, cribado de sectores ya calculados sin nueva geometría; no sector admitido con criterios completos |
| Progreso/layer6 | PASS_STATIC de reglas; RUNTIME_NOT_VERIFIED de sus valores | No Twilight+flag1E08 o override explícito; G2logical6 no discrimina esas condiciones |
| Transición natural | PASS_STATIC de RTBL/SCLS13 y lifecycle; RUNTIME_NOT_VERIFIED de ciclo real | Rooms2/4 retienen3, filas1/5 lo excluyen condicionalmente; salidas declaradas y gates no prueban acceso/retirada/recreación |
| G0 | PARTIAL | Selección/preset/contexto observados intactos; todavía sin colocación admitida |
| G1 | PASS_STATIC/PASS_LAB históricos | Observador/SDK/ABI no cambiados ni recompilados; tests previos no repetidos |
| G2 | PASS_RUNTIME_OBSERVED limitado |28 capturas,7 E_OC de room3,capas diferenciadas,D3D12,visual normal reportado; Randomizer/texturas activos. IDs220/221 sin origen demostrado |
| G4 | **G4_RESOURCE_VERIFIED_POSITION_BLOCKED** | Overlays del servicio ya resueltos; local geometry no prueba dominio/posición/progreso admisible |
| G5 | **NO-GO / NOT_TESTED** | No autorizado, no módulo activo ni aparición; ningún cambio por esta revisión |
| G6 | NOT_VERIFIED / NOT_TESTED | No instancia añadida ni transición/cleanup ensayados |
| CP02 | **NO-GO** | No iniciado |
| Descarga DLL de perfiles personalizados | **BLOCKED independiente** | Estado anterior conservado; sin nueva auditoría o parche |

PASS_STATIC acredita fuente/estructura o cálculo dentro del alcance; PASS_OFFLINE valida herramientas/datos propios; PASS_RUNTIME_LOG acredita lo registrado por el host dentro del mecanismo identificado; PASS_RUNTIME_OBSERVED conserva la sesión real G2. PARTIAL, NOT_VERIFIED, RUNTIME_NOT_VERIFIED, BLOCKED y NO-GO no equivalen a PASS del juego. Ningún resultado nuevo es una compilación o ejecución del mod.

## Incertidumbres cerradas y pendientes

**Cerradas:** servicio de overlays aplicado vacío en G2, distinción respecto de texturas, ruta de actualización dinámica; formato exacto SCLS13 y destinos; RTBL3/2/4 y retención de3; estado inicial/paseo espontáneo y mecanismos que invalidan inmovilidad; alcance social global sin filtro de room; alternativas existentes no acreditan aislamiento.

**Pendientes:** guardas efectivas de un caso de observación (Link/ruido/estado de E_OC en todas las salas residentes, medio y fuerzas), contacto/navegación en su región pertinente, progresión/Twilight/entry/override, camino natural y retirada/recreación del node3. Identidad byte por byte/F32/render/creación/cleanup tienen límites runtime conservados; no se reabren auditorías generales.

**Siguiente comprobación mínima:** aprovechar solo datos existentes privados de ese contexto —progreso y entrada, censo E_oc global de rooms residentes, condiciones de sensores y ciclo natural de room3—. El log actual y los dos ARC no contienen esos estados; RTBL describe qué debería suceder bajo condiciones, no que sucedió. Si no hay evidencia existente, la observación baseline pertinente necesita autorización runtime posterior, sin nueva adición; no se solicita ejecutarla ni se fabrica un paquete. [POSITION_CONTEXT_REVIEW](POSITION_CONTEXT_REVIEW.md) concreta la carencia. No pedir de nuevo overlays, ARC, ROM, SDK, EXE o log completo.

Se detiene esta revisión. No G5, G6 o CP02.
