# G4 — recursos verificados, ubicación todavía bloqueada

**G4_RESOURCE_VERIFIED_POSITION_BLOCKED. Ubicación: NO_SAFE_POSITION_VERIFIED.** Checkpoint de continuación offline, no G4 superado ni autorización G5. `DISARMED_NO_REGISTRATION` intacto.

| Requisito | Estado actualizado | Evidencia / límite |
|---|---|---|
| Acceso e identidad E_oc/E_ocb | PASS_STATIC | Rama/commit privados correctos, bytes reales, hashes/tamaños/manifiesto coincidentes |
| Yaz0/RARC/J3D e índices | PASS_STATIC | Dos modelos3/4;28 BCK/29 joints, WAIT0x1B; rangos y referencias pertinentes comprobados |
| Geometría/skin/arma | PASS_STATIC | VTX1/JNT1/INF1/EVP1/DRW1/SHP1 y texturas embebidas leídos; no modelo supuesto ni cull usado como envolvente |
| Interpolación de recursos | PASS_STATIC condicionado |18975 segmentos, hulls racionales continuos; todas28 BCK+bind/morphs incluidos; escala variable22 y tangentes FINISH consideradas |
| Cota local cuerpo/arma/colliders | PASS_STATIC matemático, PARTIAL frente al engine |401/494/unión501 bajo condiciones explícitas; no certificado integral de F32/JMath/interpolación gráfica ni recurso efectivo/HIO runtime |
| Suelo local/collisiones próximas | PASS_STATIC limitado | Consulta31 prismas; suelo Acch100/disco501 cubierto; paredes fuera de501 y ARC externos separados en condiciones autoradas |
| Pies, pendientes, agua y navegación | NOT_VERIFIED; PARTIAL | Superficies locales reales y diagnósticos disponibles; no prueba de pies/arma o traversabilidad/agua dinámica |
| Movimiento, actores, eventos/progreso, room limits | BLOCKED / NOT_VERIFIED | Rango2000 blando; región alcanzable y condiciones de progresión/carga no delimitadas; agregados28 G2 no son trayectorias futuras |
| Recursos efectivos de G2 / overrides | NOT_VERIFIED | Manifiesto lo declara; no equiparar copia del disco con fuente efectiva de la sesión |
| G0 | PARTIAL, selección PASS_STATIC conservada | Mismo preset/room/layer; sin posición admitida |
| G1 | PASS_STATIC/PASS_LAB históricos | Sin cambio de observador, SDK/ABI o código nativo; no suites/builds repetidos |
| G2 | PASS_RUNTIME_OBSERVED limitado y conservado | Sesión real28 capturas, censo7, capas diferentes,D3D12; Randomizer/texturas activos; sin relectura del log |
| A1/propiedad por carga natural | PASS_STATIC condicionado, intacto | Contrato anterior reutilizado; ninguna API invocada o adición observada |
| G5 | **NO-GO / NOT_TESTED** | No autorizado; posición/controles pendientes; sin spawner o paquete |
| G6 | NOT_VERIFIED / NOT_TESTED | Ninguna nueva instancia, transición o limpieza ejecutada |
| Descarga DLL de perfiles personalizados | BLOCKED independiente | Sin nueva auditoría, hooks o parche; G2/cotas no resuelven ese bloqueo |
| CP02 | **NO-GO** | No iniciada |

PASS_STATIC prueba exclusivamente el dato/contrato dentro del alcance indicado. PASS_LAB corresponde a pruebas históricas identificadas; las nuevas comprobaciones Python son PASS_OFFLINE de análisis, no pruebas de un enemigo en el juego. NOT_VERIFIED, NOT_TESTED, BLOCKED y NO-GO no se sustituyen por un PASS de compilación o de poses calculadas.

El requisito resuelto es **disponibilidad/estructura de los dos recursos originales aportados**. El que permanece es una **posición y dominio condicionado de movimiento/observación** con suelo, pies/arma, eventos, progresión, recursos efectivos y límites suficientes. Hay avances locales cuantificables, pero no se satisface ese conjunto.

La siguiente entrada mínima ya no son archivos binarios: identificación de overrides efectivos de las dos rutas y contexto/recorrido natural mediante información existente, según [POSITION_REASSESSMENT](POSITION_REASSESSMENT.md). Lo que precise observación nueva dentro del juego queda pendiente de autorización posterior; no se solicita realizarla ahora. Recibir información adicional no autoriza un ensayo.

Detención al terminar G4 offline. No artefactos de ejecución ni avance a G5/G6/CP02.
