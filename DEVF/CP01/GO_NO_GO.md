# Puerta CP01 — revisión posterior a 092c1e6
**NO-GO para CP02. No está listo para un TEST de actor en Windows/DX12.**

| Bloqueo | Estado | Qué se resolvió | Qué falta |
|---|---|---|---|
| Ubicación real segura | BLOCKED / NOT_VERIFIED | Nuevo ZIP y punto F_SP121/3/layer 6 comunicados; descarga bloqueada por entorno failed | Leer/verificar adjunto; analizar con fuente exacta 2.0.3; cotejar suelo, huella, actores, capas y eventos; completar observación runtime |
| Ciclo de vida / unload | MITIGADO en modo desarmado; NO RESUELTO con actores | Release e identidad de slot verificados, cierre sin reactivación, limpieza parcial conservadora, rechazo de post-callback y cero registros por defecto | Host debe drenar solicitudes por perfil, respetar fallos de destrucción y retener perfil/contexto/DLL si no completa cierre; además cancelación/fin seguro de archivo pendiente |

Build MSVC, 20 casos nuevos distintos (14 de cierre + 6 de propiedad de colisión) y 9 regresiones afectadas: PASS en runs incrementales separados. Los otros 7 casos originales no se repitieron. Los 16 PASS anteriores se conservan como historia, sin usarlos para certificar las nuevas condiciones del host.

El módulo ahora queda DISARMED_NO_REGISTRATION: no registra perfiles ni Stage edits, no solicita actores y no conecta callbacks al engine. Evita una descarga insegura de actores DEVF al no crearlos, pero no convierte al loader en un host con veto. No se activa por cambiar configuración.

Pin de DLL probado solo sobre fixtures propias: mantiene código, no datos/perfiles/contexto del host. No se usa como sustituto de una barrera ni se introducen hooks/parches/EXE nuevo. Instrucciones manuales de no pulsar Reload no bastan para declarar garantía técnica.

No se emite DEVF_CP01_TEST.dusk. Artefacto únicamente BUILD ONLY desarmado. Aparición, dibujo, colisión, sala/capa, limpieza y renderer DX12 dentro del juego siguen NOT_TESTED. Obtener evidencia de ubicación no resuelve el segundo bloqueo. No iniciar CP02.

## Decisión de esta revisión F_SP121

NO-GO continúa. El adjunto no equivale a verificación: no se leyeron sus bytes y no hay análisis de lugar completado. No se aprobó ninguna coordenada ni condición de aparición. Esta limitación operativa no demuestra que el punto sea inseguro o seguro. El bloqueo de unload sigue independiente e intacto; no se modifica host, código de activación o política. Sin TEST activo, sin CP02, sin merge. Se publica únicamente checkpoint documental separado del anterior.
