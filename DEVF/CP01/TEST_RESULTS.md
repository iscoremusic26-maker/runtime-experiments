# CP01 — matriz incremental de seguridad
Resultados originales 16 PASS/build Windows conservados en tag DEVF_CP01 (092c1e6) y evidence/windows-verification.json. Esta revisión no ejecuta la suite completa original.

| Área | Estado actual | Evidencia/límite |
|---|---|---|
| Binarios de escenario/suelo/modelo | NOT_VERIFIED en revisión F_SP121 | Inventario histórico: ausentes en ZIP del host; nuevo adjunto declarado por usuario, bytes inaccesibles |
| Stage/room/layer/XYZ seguros | NOT_APPROVED | Candidato geométrico fundamentado; faltan colisiones externas, ruta/contexto y contacto en pendiente |
| Funciones de cierre exactas del host | PASS auditoría/reproducción acotada | Cinco cuerpos sin modificar compilados con colas/slots/backends simulados; hashes en exact-host-functions.json |
| Guardas de activación antes de registro | PASS laboratorio | Falta de cada requisito/default no produce llamadas de registro; cierre repetido sin ownership |
| Propiedad de slot de colisión tras scene teardown/reutilización | PASS lógica propia, seis casos | No retira slot ajeno; referencia propia única exige índice/actor correctos; tabla sin referencia propia solo retira ID local; adaptador nativo compilado/enlazado, no ejecutado en motor |
| Retirada de colisión fallida | PASS lógica propia | No libera archivo ni referencias; ready=false y estado closing; retry ordenado/idempotente |
| Liberación de archivo fallida/pendiente | PASS lógica propia | No borra referencias ni reinicia load; solo release nativo phase.id==2; pending real no ejecutado |
| Cancelación y callbacks de actor en cierre | PASS lógica propia | UNK3 terminal; no execute/draw hasta ready; no reactivación tras intento de destroy |
| Callback opcional en request runtime | PASS laboratorio | Rechazado antes de create_actor; no puntero extra sin lifetime token |
| Request antes del primer callback en unregister | PASS reproducción de limitación | Cuerpo exacto devuelve OK sin drenar una cola pendiente no inspeccionada; no prueba de crash real |
| Force-delete ignora fallo de callback | PASS reproducción de limitación | actor_delete exacto devuelve 1 con forceDelete aunque deleteFunction retorna 0 |
| Retirada con actor restante | PASS reproducción | MOD_UNAVAILABLE conserva slot; no barrera del loader por ese retorno |
| FreeLibrary tras shutdown fallido | PASS Windows real, DLL fixture propia | La fixture se descarga; nunca se invoca un puntero después del unload |
| PIN de imagen DLL | PASS Windows real, DLL fixture propia | Conserva imagen propia hasta salir; no preserva slot/contexto del host; no aplicado en producción |
| MSVC, SDK, PE, imports/exports, paquete/servicios | PASS | Run final 38189000074, metadata y hashes nuevos |
| Aparición, recursos/mount, J3D, colisión, room/layer y cleanup real | NOT_TESTED | No se ejecutó Dusklight ni se conectó perfil/actor |
| DX12 y progreso/save | NOT_TESTED | Ninguna prueba de juego ni modificación de partida |
| TEST de actor | NOT_APPROVED | Bloqueos de ubicación y host persisten |
| CP02 | NOT_STARTED | Fuera de alcance |

Run 38187449685: PASS de la primera revisión incremental (11 casos nuevos + 9 regresiones). La auditoría posterior descubrió el contrato específico de dComIfG_resDelete en fase pendiente; se corrigió y añadieron tres casos de archivo/cierre.

Run de recursos/cierre 38187694002: 14 casos nuevos + 9 regresiones afectadas PASS. Regresiones seleccionadas: seis casos de recursos y tres de runtime que usan el lifecycle modificado. No se ejecutaron los siete casos originales de Stage/registro/rollback/orden de pre-hook no afectados. La ejecución del grupo de seguridad final verifica el programa incrementado y sus fixtures de cierre; no se declara ejecución del motor.

Compilador MSVC 19.51.36260.0 / Windows SDK 10.0.26100.0, x64 RelWithDebInfo. Warnings originales de headers/placement new se conservan en logs, no se ocultan ni se convierten en prueba de recuperación de excepción de constructor. Ver safety-review-build-and-tests.log; los hashes binarios finales están en collision-review-verification.json.

Run final 38189000074: seis casos nuevos de propiedad de colisión PASS, sin repetir las suites 14/9/16. Ver collision-review-build-and-tests.log y collision-review-verification.json. El laboratorio usa una tabla simulada para demostrar la política; no certifica la ejecución del adaptador cBgS en una sala real. Total de esta revisión: 20 casos nuevos distintos y nueve regresiones afectadas.

## Revisión F_SP121 desde 58c4966: comprobaciones nuevas

| Comprobación | Resultado | Alcance / límite |
|---|---|---|
| Git LFS, SHA256 ZIP y tres hashes individuales | PASS | Copias íntegras, no acredita procedencia/región/runtime |
| CRC de cuatro miembros y tamaños | PASS | Sin corrupción detectada; manifiesto interno leído |
| Yaz0/RARC y límites DZS/DZR | PASS | Tablas acotadas antes de interpretar |
| Sala3, MULT identidad, comunes/capa6 | PASS estático | No es lista de actores vivos; layer efectivo comunicado |
| KCL/PLC y árbol completo | PASS estático | 5326 prismas referenciados; ningún query del motor ejecutado |
| Suelo observado y WRock BMD/DZB/joint | PASS estático | Y difiere0.000141; índices/tamaños correctos |
| Cobertura envolventes del candidato | PASS numérico | Resta semiplanos: área sin soporte0;441 puntos por caja y octree/baricéntrico |
| KCL paredes/techos en caja del candidato | PASS separación estática | Solo intersecta dos planos de suelo; no colliders externos |
| Triggers/volúmenes con contrato identificado | PASS separación acotada | No equivale a ausencia de eventos globales |
| Rutas/event_list/STB inventario estructural | PASS análisis | Polilínea7 a115.6156; consumidor Digpl usa puntos discretos; efectos de secuencias no certificados |
| Geometría @bg004d / Obj_Board | PASS estático | Nuevos ARC íntegros;4 ubicaciones y fases evaluadas; runtime NOT_TESTED |
| Actores vivos, anchura de ruta, scripts y progreso | NOT_VERIFIED | Contexto y evidencia Windows pendientes |
| Ubicación candidata geométrica | PASS existencia condicionada | Ninguna coordenada aprobada de aparición |
| DEVF runtime: aparición/render/colisión/cleanup, DX12 | NOT_TESTED | No se ejecutó juego ni activó mod |
| Barrera unload / TEST activo / CP02 | NO-GO / NOT_APPROVED / NOT_STARTED | Sin cambios respecto de auditoría de seguridad |

Python estándar, análisis local reproducible (analysis/README). Metadata y referencias exactas en evidence/location-f-sp121-*.json. Sin nuevas suites Windows ni SDK Linux: módulo y política no cambiaron. PASS previos conservados. Los antiguos BLOCKED_ENVIRONMENT de 58c4966 quedan históricos en ese commit.

Comprobación nueva incremental: consumidor ACTR[5]/Digpl y ruta7 PASS por parámetros/fuente; exclusión de sus27 puntos de la caja y radio500 PASS numérico. Mínima distancia caja-punto565.6961. La prueba reutiliza resultados privados sin repetir KCL/WRock/seguridad. Acceso, partículas, puntos usados y otros consumidores NOT_VERIFIED; juego/DX12 NOT_TESTED. Evidencia: location-f-sp121-digpoints.json.

## Incremento extra-collisions desde 0fe4c16

| Comprobación nueva | Estado | Alcance/límite |
|---|---|---|
| ZIP real frente a LFS, SHA256 externo | PASS | 19489 bytes, coincide manifiesto privado |
| Manifiesto interno, tamaños y CRC3 miembros | PASS | @bg004d19385, Obj_Board440; no corrupción detectada |
| Yaz0/RARC, DZB/BMD/spec y límites | PASS estático | 6 DZB y2 BMD nuevos; modelos S16 y spec interpretados según2.0.3 |
| Texture-sharing model1→model0 | PASS estático | Mismo nombre TEX1; imagen embebida fuente, sin dependencia geométrica externa |
| model1.dzb ausente | PASS interpretación de contrato | Opcional, collider roto nulo; no asumir recurso externo |
| mmvbg3 ubicaciones: colisión/cilindro/modelos | PASS separación estática | Switches29/120/122, intacto/roto; no engine ejecución |
| ClearB02, escala(10,1,6), pitch90 | PASS separación estática | Matriz final y carga inicial; switch255 devuelveFALSE |
| Efectos globales partículas/sonido y progreso | NOT_VERIFIED | IDs identificados, sin datos/ejecución que certifiquen alcance o cero interferencia |
| Digpl/KCL/WRock anteriores | CONSERVED | No reejecutados;27 puntos y565.6961 intactos |
| Ubicación segura completa | NOT_VERIFIED | Contexto Windows, contacto/pendiente y efectos/acceso pendientes |
| Mod runtime/render/colisión/cleanup/DX12 | NOT_TESTED | Ningún TEST activado |
| Unload / CP02 | BLOCKED / NO-GO | Auditoría previa conservada, sin nueva investigación |

Ver metadata extra-collisions-verification.json, hashes/líneas en extra-collisions-source-references.json y herramienta location_extra_collisions.py. Solo cálculos estructurales/geométricos nuevos con Python estándar; ninguna compilación o suite anterior repetida. Los recursos originales nunca entran en Git/artefactos del repositorio principal.

## Revisión experimental autorizada del host desde 5f3a7ef

Nueva rama independiente `experiment/devf-cp01-host-lifetime`. Ver [HOST_LIFETIME_REVIEW](../CP01_HOST_EXPERIMENT/HOST_LIFETIME_REVIEW.md) y [pruebas incrementales](../CP01_HOST_EXPERIMENT/TEST_RESULTS.md). La auditoría anterior se conserva como base histórica; su declaración de “no modificar host” correspondía al alcance anterior. El usuario autoriza ahora exclusivamente código fuente experimental, sin modificar instalación ni distribuir ejecutable.

Parche experimental con barrera de solicitudes, predrenado separado de retirada de perfiles, veto ante shutdown fallido y ownership retenido. No integrado en un host completo: faltan submódulos exactos del release para compilarlo. No acredita seguridad del runtime. DISARMED_NO_REGISTRATION, ubicación NOT_VERIFIED, ejecución DX12 NOT_TESTED y CP02 NO-GO se conservan. No repetir ubicación/auditoría/suites no afectadas. Recuperar esta rama y comprobar SOURCE_MANIFEST antes de aplicar a una copia del source; nunca a una instalación.

Cierre de esta revisión: **25/25 PASS de laboratorio Windows x64/MSVC 19.51.36260.0 + SDK10.0.26100.0**, run [38204996509](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38204996509). El parche y los scopes efectivos se compilan como funciones extraídas con adaptadores sintéticos; no es compilación del host completo ni ejecución del engine/DX12. Compilación completa BLOCKED por dependencias/gitlinks exactos; integración/fases/escenas NOT_TESTED y compatibilidad/teardown global NOT_VERIFIED.

Checkpoint final: **DEVF_CP01_HOST_LIFETIME_EXPERIMENT**, rama experimental independiente, PR draft #1 sin merge. Ver [recuperación](../CP01_HOST_EXPERIMENT/RECOVERY.md) y [matriz detallada](../CP01_HOST_EXPERIMENT/TEST_RESULTS.md). Bloqueo arquitectónico **no cerrado en producción**, ubicación permanece NOT_VERIFIED. CP01 **no listo para TEST activo Windows/DX12**; DISARMED_NO_REGISTRATION y CP02 NO-GO. Detener aquí: siguiente trabajo mínimo es obtener/integrar las dependencias exactas del host, sin repetir la auditoría ni análisis de ubicación.
