# Puerta CP01 — revisión posterior a 092c1e6
**NO-GO para CP02. No está listo para un TEST de actor en Windows/DX12.**

| Bloqueo | Estado | Qué se resolvió | Qué falta |
|---|---|---|---|
| Ubicación real segura | PARTIAL_STATIC_PASS / NOT_APPROVED | ZIP completo verificado; KCL/PLC, WRock, capas, volúmenes y candidato medidos | Colisiones @bg004d/Obj_Board ahora PASS estático; siguen efectos/acceso/contexto Windows, observación runtime y contacto en pendiente |
| Ciclo de vida / unload | MITIGADO en modo desarmado; NO RESUELTO con actores | Release e identidad de slot verificados, cierre sin reactivación, limpieza parcial conservadora, rechazo de post-callback y cero registros por defecto | Host debe drenar solicitudes por perfil, respetar fallos de destrucción y retener perfil/contexto/DLL si no completa cierre; además cancelación/fin seguro de archivo pendiente |

Build MSVC, 20 casos nuevos distintos (14 de cierre + 6 de propiedad de colisión) y 9 regresiones afectadas: PASS en runs incrementales separados. Los otros 7 casos originales no se repitieron. Los 16 PASS anteriores se conservan como historia, sin usarlos para certificar las nuevas condiciones del host.

El módulo ahora queda DISARMED_NO_REGISTRATION: no registra perfiles ni Stage edits, no solicita actores y no conecta callbacks al engine. Evita una descarga insegura de actores DEVF al no crearlos, pero no convierte al loader en un host con veto. No se activa por cambiar configuración.

Pin de DLL probado solo sobre fixtures propias: mantiene código, no datos/perfiles/contexto del host. No se usa como sustituto de una barrera ni se introducen hooks/parches/EXE nuevo. Instrucciones manuales de no pulsar Reload no bastan para declarar garantía técnica.

No se emite DEVF_CP01_TEST.dusk. Artefacto únicamente BUILD ONLY desarmado. Aparición, dibujo, colisión, sala/capa, limpieza y renderer DX12 dentro del juego siguen NOT_TESTED. Obtener evidencia de ubicación no resuelve el segundo bloqueo. No iniciar CP02.

## Decisión tras la evidencia F_SP121 accesible

Se supera el bloqueo operativo de descarga, pero la seguridad del lugar sigue pendiente. Existe candidato geométrico F_SP121/3/layer6, (-4806.7346,-6729.480961460304,65135.8281), yaw0/escala1 únicamente analizados. Cobertura/volúmenes y colisiones externas ahora excluidos estáticamente, sin acreditar efectos o contexto runtime: la medida a polilínea ruta7 queda a115.6156 de caja del modelo (no trayectoria barrida del consumidor Digpl identificado); terreno varía58.3206 unidades bajo ella. LOCATION_ANALYSIS detalla evidencia adicional sin reextraer los tres ARC recibidos.

Unload continúa bloqueado, sin cambio o nueva prueba. No se modifica host, activación, CMake o workflow. No TEST activo, instalación ni CP02. Cambios solo de análisis/documentación en rama documental existente, sin merge.

Consumidor Digpl de ruta7 identificado y sus27 puntos excluidos de caja/radio500: PASS estático incremental. Punto más próximo a565.6961 de caja; quedan efectos/acceso/estado en juego NOT_TESTED. No convierte la ubicación en segura ni resuelve el unload. Recuperación final DEVF_CP01_LOCATION_DIGPOINTS_REVIEW.

## Puerta tras revisión de dos colisiones externas

PASS estático: ambos ARC íntegros, geometría/dependencias/carga y4 ubicaciones mmvbg/ClearB excluidas de caja candidata, incluyendo carga inicial y estados intacto/roto. El acceso a assets ya no es un BLOCKED_INPUT de estas dos colisiones. Model1.dzb opcional ausente no bloquea: el código deja ese collider nulo.

Ubicación segura NOT_VERIFIED: evidencia Windows/contexto, pendiente/contacto, efectos globales/cámara/progreso y acceso Digpl permanecen. Runtime del mod NOT_TESTED. Unload BLOCKED independiente e intacto; no se vuelve a auditar. NO-GO para TEST activo y CP02; mantener DISARMED_NO_REGISTRATION. No se rechaza ni aprueba candidato por suposición. Checkpoint nuevo DEVF_CP01_EXTRA_COLLISIONS_REVIEW, sin merge ni mover tags anteriores.

## Revisión experimental autorizada del host desde 5f3a7ef

Nueva rama independiente `experiment/devf-cp01-host-lifetime`. Ver [HOST_LIFETIME_REVIEW](../CP01_HOST_EXPERIMENT/HOST_LIFETIME_REVIEW.md) y [pruebas incrementales](../CP01_HOST_EXPERIMENT/TEST_RESULTS.md). La auditoría anterior se conserva como base histórica; su declaración de “no modificar host” correspondía al alcance anterior. El usuario autoriza ahora exclusivamente código fuente experimental, sin modificar instalación ni distribuir ejecutable.

Parche experimental con barrera de solicitudes, predrenado separado de retirada de perfiles, veto ante shutdown fallido y ownership retenido. No integrado en un host completo: faltan submódulos exactos del release para compilarlo. No acredita seguridad del runtime. DISARMED_NO_REGISTRATION, ubicación NOT_VERIFIED, ejecución DX12 NOT_TESTED y CP02 NO-GO se conservan. No repetir ubicación/auditoría/suites no afectadas. Recuperar esta rama y comprobar SOURCE_MANIFEST antes de aplicar a una copia del source; nunca a una instalación.

Cierre de esta revisión: **25/25 PASS de laboratorio Windows x64/MSVC 19.51.36260.0 + SDK10.0.26100.0**, run [38204996509](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38204996509). El parche y los scopes efectivos se compilan como funciones extraídas con adaptadores sintéticos; no es compilación del host completo ni ejecución del engine/DX12. Compilación completa BLOCKED por dependencias/gitlinks exactos; integración/fases/escenas NOT_TESTED y compatibilidad/teardown global NOT_VERIFIED.

Checkpoint final: **DEVF_CP01_HOST_LIFETIME_EXPERIMENT**, rama experimental independiente, PR draft #1 sin merge. Ver [recuperación](../CP01_HOST_EXPERIMENT/RECOVERY.md) y [matriz detallada](../CP01_HOST_EXPERIMENT/TEST_RESULTS.md). Bloqueo arquitectónico **no cerrado en producción**, ubicación permanece NOT_VERIFIED. CP01 **no listo para TEST activo Windows/DX12**; DISARMED_NO_REGISTRATION y CP02 NO-GO. Detener aquí: siguiente trabajo mínimo es obtener/integrar las dependencias exactas del host, sin repetir la auditoría ni análisis de ubicación.
