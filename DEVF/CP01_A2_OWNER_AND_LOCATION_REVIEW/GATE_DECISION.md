# Decisión de owner y ubicación para la primera prueba

**Resolver: OWNER_STATIC_SUFFICIENT_FOR_TEST_DESIGN. Ubicación: FIRST_TEST_LOCATION_BLOCKED_EXACT_EVIDENCE.** No defecto demostrado ni cambio de código; no build/suite repetidos. Se mantiene DISARMED_NO_REGISTRATION.

| Elemento | Resultado de esta revisión | Alcance |
|---|---|---|
| Controlador desarmado | A2_DISARMED_CONTROLLER_PASS_LAB conservado |70+29checks,6mutantes y compile guards históricos, no reejecutados |
| Enlace MSVC | A2_DISARMED_MSVC_LINK_PASS conservado |Mismo código0fa942f y DLL SHAfd9f04fd…; CI38341931143 |
| Auditoría binaria | A2_DISARMED_BINARY_AUDIT_PASS conservado |No archivo compilable cambió; no binario nuevo |
| Resolver estático | PASS_STATIC / CONDITIONALLY_SUPPORTED |Vínculos/params/init/flags/next/counts respaldados; no lock/OS thread check ni monitor pending |
| Owner: decisión de diseño | OWNER_STATIC_SUFFICIENT_FOR_TEST_DESIGN |Sin campaña adicional obligatoria solo para diseñar; guardas runtime antes de solicitud siguen obligatorias |
| Ownership runtime | A2_RUNTIME_OWNER_NOT_VERIFIED |No nueva captura del resolver ni request/instancia |
| Recursos | PASS_STATIC íntegros / acceso contextual favorable; carga final NOT_VERIFIED |ARC/preset/FILI/presencia nativa/Overlay0 reutilizados, sin revalidación de originales |
| Punto histórico | FIRST_TEST_LOCATION_BLOCKED_EXACT_EVIDENCE |Faltan medio/BG efectivos y ocupación/contexto local presentes, no navegación universal |
| G4 histórico | G4_RESOURCE_VERIFIED_POSITION_BLOCKED / NO_SAFE_POSITION_VERIFIED |No reescribir ni promover resultados anteriores |
| Creación/render | A2_RUNTIME_CREATION_NOT_TESTED / A2_RUNTIME_RENDER_NOT_TESTED |Sin ejecución del juego, solicitudes, actor añadido o TEST |
| G5 | G5_NO_GO |Sin ubicación admitida/adaptador activo/paquete/autorización runtime |
| G6 | G6_NOT_VERIFIED |Ningún teardown/cleanup real |
| CP02 | CP02_NO_GO |No iniciada |
| DLL personalizada | BLOCKED independiente |No reauditar ni aplicar parche |

## Respuestas de decisión

1. **Resolver correcto para preflight:** lookup temprano se combina con init2/!pending; parámetros y backlinks son los del host; room parent debe ser play.layer y target hijo registrado no-root. No prueba runtime ni vida reservada.
2. **Guardas restrictivas pero justificadas:** next puede diferir en una puerta con room todavía viva; parent counts pueden reflejar otros hijos y0x20 limpia sin destruir sala. Mantener esos rechazos para el ensayo sin transiciones. No corrección ni relajación por rutina.
3. **Observación owner adicional para diseñar:** no. **Evidencia local previa a admitir punto:** sí, faltan lecturas de medio/BG/ocupación/contexto. Owner puede viajar en la misma captura desarmada; no nueva campaña completa G2.
4. **Punto admitido:** no. BLOCKED_EXACT_EVIDENCE, no REJECTED: terreno/espacio inicial favorables, agua/ocupación actuales no acreditadas; proximidad pasada de Link no prueba contacto y tampoco aislamiento.
5. **Antes de adapter activo posterior:** cerrar esas carencias del punto, definir preflight/revalidación instantánea y seguimiento request/readiness/continuidad de ID (resolver actual es preflight), revisión dirigida del consumidor exacto. Paquete/runtime necesitarán autorización posterior separada; ninguna bandera arma el módulo actual.
6. **Investigaciones terminadas para este caso:** arquitectura A2, fuentes/SDK/ABI/MSVC, controlador desarmado, ARC/animaciones/envolventes y geometría local, overlays G2 y lectura histórica, colisiones externas estudiadas. No repetirlas salvo contradicción concreta o cambios afectados.
7. **Paso mínimo:** captura local futura desarmada C con suelo/agua/BG, ocupantes próximos/Link, evento/contexto y Owner escalar; después revisión del mismo punto. Sin ejecución/paquete ahora.

El tiempo corto y cierre de proceso no garantizan inmovilidad, ausencia de eventos o reversión de saves. En el futuro ensayo WALK/detección/social normales son observables; anomalía de owner/render, combate o evento/transición inesperado detiene la sesión. No se promete PASS de esos aspectos.

La tarea termina con publicación documental recuperable, PR draft sin merge.
