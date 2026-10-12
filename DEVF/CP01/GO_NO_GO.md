# Puerta CP01 — revisión posterior a 092c1e6
**NO-GO para CP02. No está listo para un TEST de actor en Windows/DX12.**

| Bloqueo | Estado | Qué se resolvió | Qué falta |
|---|---|---|---|
| Ubicación real segura | BLOCKED: faltan datos | Inventario exacto confirma ausencia de binarios de escenario/geometría; captura nativa disponible sin mod | Player Info/console y Stg_00.arc, sala Rxx_00.arc, Wrock.arc de la instalación; cotejar suelo, huella, capas, actores y eventos |
| Ciclo de vida / unload | MITIGADO en modo desarmado; NO RESUELTO con actores | Release e identidad de slot verificados, cierre sin reactivación, limpieza parcial conservadora, rechazo de post-callback y cero registros por defecto | Host debe drenar solicitudes por perfil, respetar fallos de destrucción y retener perfil/contexto/DLL si no completa cierre; además cancelación/fin seguro de archivo pendiente |

Build MSVC, 20 casos nuevos distintos (14 de cierre + 6 de propiedad de colisión) y 9 regresiones afectadas: PASS en runs incrementales separados. Los otros 7 casos originales no se repitieron. Los 16 PASS anteriores se conservan como historia, sin usarlos para certificar las nuevas condiciones del host.

El módulo ahora queda DISARMED_NO_REGISTRATION: no registra perfiles ni Stage edits, no solicita actores y no conecta callbacks al engine. Evita una descarga insegura de actores DEVF al no crearlos, pero no convierte al loader en un host con veto. No se activa por cambiar configuración.

Pin de DLL probado solo sobre fixtures propias: mantiene código, no datos/perfiles/contexto del host. No se usa como sustituto de una barrera ni se introducen hooks/parches/EXE nuevo. Instrucciones manuales de no pulsar Reload no bastan para declarar garantía técnica.

No se emite DEVF_CP01_TEST.dusk. Artefacto únicamente BUILD ONLY desarmado. Aparición, dibujo, colisión, sala/capa, limpieza y renderer DX12 dentro del juego siguen NOT_TESTED. Obtener evidencia de ubicación no resuelve el segundo bloqueo. No iniciar CP02.
