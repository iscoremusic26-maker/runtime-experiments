# DEVF_CP01 — revisión de bloqueos desde 092c1e6
**Build incremental PASS; NO-GO para TEST de actor y CP02.**

Rama existente checkpoint/devf-cp01-20261011, nuevo tag DEVF_CP01_SAFETY_REVIEW. Tag DEVF_CP01/092c1e6, checkpoints CP00 y PR anteriores conservados. No merge automático, instalación en PC, aparición automática, cambio de EXE ni CP02.

Ubicación: los ZIP solo aportan fuente/binarios host, no datos binarios de salas/geometría del juego. No se inventó un lugar ni se certificó el demo. LOCATION_EVIDENCE.md fundamenta la carencia y permite capturar stage/room/layer efectivo/XYZ/ángulo con Debug → Player Info del juego original. Solicita únicamente Stg_00.arc, sala Rxx_00.arc y Wrock.arc correspondientes, capturas/estado/actor list y hashes; no ROM completa o saves. La ubicación continúa bloqueada hasta analizar esa evidencia.

Cierre: la auditoría corrigió la interpretación de la cola de actores (se añade en primer callback, no al completar recursos) y confirmó la ventana anterior, los callbacks post-create sin token, el forceDelete que enmascara fallos y FreeLibrary pese a shutdown failure. PIN de imagen no conserva contexto/perfiles. dComIfG_resDelete no admite phase.id 1; errores/cancel pueden borrar el estado de fase sin acreditar ausencia de referencia. Referencias y recorrido completo en LIFECYCLE_AUDIT.md.

Correcciones propias: identidad de slot/actor y release de colisión/archivo verificados, ownership retenido ante fallo, closing sin reactivación, limpieza de referencias de heap fallido y cancelación terminal. Rock no declara destroy exitoso cuando release falla; el host aún puede enmascararlo. Runtime rechaza create_function adicional. La política de producción ahora DISARMED_NO_REGISTRATION evita registrar perfiles, Stage edits, actores o callbacks propios; no se abre mediante configuración. No se aplicó pin al mod ni parche/hook al host.

Windows Actions runs 38187694002 y 38189000074 PASS con MSVC 19.51.36260.0/SDK 10.0.26100.0. 14 casos nuevos y 9 regresiones afectadas en el run de recursos/cierre, más seis casos nuevos de identidad de colisión en el run final; las suites anteriores no se repitieron en este último run. Cinco cuerpos upstream exactos se prueban con backends simulados; FreeLibrary/PIN se prueban sobre DLLs propias reales. Ningún PASS de motor o render.

Artefacto únicamente BUILD ONLY desarmado; no DEVF_CP01_TEST.dusk. Falta una garantía real de host para drenar/retener contexto/perfil/DLL ante fallo y para finalizar recursos pendientes, además de ubicación/ejecución. CP01 no listo para prueba de actor en Windows/DX12. Capturar evidencia de lugar sí puede hacerse con vistas nativas sin instalar DEVF.

Leer GO_NO_GO, TEST_RESULTS, LOCATION_EVIDENCE, LIFECYCLE_AUDIT, BUILD_ENV y RESUME_INSTRUCTIONS. Hashes/evidencia nuevos usan prefijos safety-review y collision-review; evidencia original permanece intacta.
