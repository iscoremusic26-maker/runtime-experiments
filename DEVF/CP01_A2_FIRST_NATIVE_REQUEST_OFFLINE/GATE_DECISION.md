# Decisión de gates

| Gate | Estado de esta entrega | Fundamento |
|---|---|---|
| A2_NATIVE_ADAPTER_IMPLEMENTED_OFFLINE | PASS_STATIC | Ruta real y única, scope,latch,Admission NONE |
| A2_NATIVE_ADAPTER_PASS_LAB | PASS_LAB |93 checks nuevos +35 equivalencia |
| A2_NATIVE_ADAPTER_MSVC_LINK_PASS | PASS | SDK2.0.3/Actor1/MSVCx64 reales |
| A2_NATIVE_ADAPTER_BINARY_REVIEW_PASS | PASS_STATIC | Metadata,imports,map,disasm,slot32 |
| A2_REQUEST_ID_MONITOR_PASS_LAB | PASS_LAB | Pending/fase/ID/owner/room/timeout/fallos |
| G4B_RUNTIME_CAPTURE_OBSERVED | OBSERVED,13 snapshots | Extracción explícita suministrada;no log recuperado |
| A2_RUNTIME_OWNER_PREFLIGHT_OBSERVED | OBSERVED,13 ReasonNone | ROOMchild identificado en contexto observado |
| A2_RUNTIME_REQUEST_NOT_TESTED | NOT_TESTED | Cero llamadas al juego |
| A2_RUNTIME_CREATION_NOT_TESTED | NOT_TESTED | Cero actores creados |
| A2_RUNTIME_RENDER_NOT_TESTED | NOT_TESTED | Sin ejecución DX12 del adaptador |
| FIRST_TEST_LOCATION_BLOCKED_EXACT_EVIDENCE | BLOCKED | Sin admisión formal de C/sesión |
| G4_RESOURCE_VERIFIED_POSITION_BLOCKED | BLOCKED | Recursos históricos no equivalen a READY/clearance |
| G5_NO_GO | NO-GO | Piloto activo no autorizado |
| G6_NOT_VERIFIED | NOT_VERIFIED | Cleanup/lifetime real pendiente |
| CP02_NO_GO | NO-GO | Gates previos sin cumplir |
| Custom-profile DLL unloading | BLOCKED,independiente | Se conserva;sin nueva investigación |

El éxito offline habilita revisión del código, no una prueba activa ni un paquete instalable. No se concede ni siquiera admisión condicional formal en esta entrega. Siguiente paso mínimo: revisión separada del checkpoint y admisión/autorización explícita de un piloto único en C bajo sesión controlada y criterio full-exit, con los riesgos de FIRST_PILOT_PREFLIGHT. Solo después se puede preparar un release activo separado para nueva auditoría y autorización de ejecución. No se avanza a G5/G6/CP02 aquí.

La restaura del contexto y el monitor no son cancelación ni lease de escena. Si se pierde contexto tras enqueue, una solicitud podría seguir pendiente; STOP no garantiza cleanup. Un mismo-ID reemplazado entre ticks no tiene detector generacional universal. Hot reload no es retry autorizado; la reinicialización de la misma imagen no borra el latch, pero unload/reload destruye globals y no se presenta como persistencia por proceso.
