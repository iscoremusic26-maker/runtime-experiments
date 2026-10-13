# Decisión de gates

| Gate | Estado | Evidencia |
|---|---|---|
| A2_FIRST_PILOT_POLICY_IMPLEMENTED_OFFLINE | PASS_STATIC | Guard real y vínculo de Key actual |
| A2_FIRST_PILOT_DISTANCE_GUARD_PASS_LAB | PASS_LAB | Checks Link/actores/XZ/A/B/C |
| A2_FIRST_PILOT_TRACE_PASS_LAB | PASS_LAB | Orden/dedup/pools/sink/errors |
| A2_FIRST_PILOT_NATIVE_ABI_MSVC_LINK_PASS | PASS | Compilación/enlace oficial Windowsx64 |
| A2_FIRST_PILOT_BINARY_AUDIT_PASS | PASS_STATIC | PE/meta/imports/map/slot32 |
| A2_FIRST_PILOT_HISTORICAL_INTEGRITY_PASS | PASS_STATIC |277 archivos intactos; #16 preservado |
| POLICIES_CODE_READY / LAB_PASS / MSVC_LINK_PASS / PE_REVIEW_PASS | PASS en su alcance offline | No ejecutan el juego |
| PILOT_CODE_READY_FOR_SEPARATE_PACKAGE_REVIEW | SÍ | Código/auditoría disponibles, no distribución |
| SESSION_AUTHORIZATION_PENDING / REAL_SESSION_NOT_AUTHORIZED | PENDING / NO AUTORIZADA | Provider NONE unchanged |
| ACTIVE_PACKAGE_NOT_GENERATED | CONFIRMADO | Cero .dusk, DLL no distribuida |
| LOCATION_CANDIDATE_CONDITIONAL | Diseño/guard implementado | No safe-location verified |
| LOCATION_SAFE_UNVERIFIED | NOT_VERIFIED | Centros/probes no son clearance |
| G4B_RUNTIME_CAPTURE_OBSERVED |13 históricos observados | Extracción del usuario, no esta DLL |
| G4_RESOURCE_VERIFIED_POSITION_BLOCKED | BLOCKED | Cobertura parcial conservada |
| FIRST_TEST_LOCATION_BLOCKED_EXACT_EVIDENCE | BLOCKED | Sin admisión posterior del piloto |
| A2_RUNTIME_REQUEST_NOT_TESTED | NOT_TESTED | Ninguna solicitud al juego |
| A2_RUNTIME_CREATION_NOT_TESTED | NOT_TESTED | Cero actor nativo creado |
| A2_RUNTIME_RENDER_NOT_TESTED | NOT_TESTED | Sin ejecución DX12 del adaptador |
| G5_NO_GO | NO-GO | Sesión/paquete no autorizados |
| G6_NOT_VERIFIED | NOT_VERIFIED | Cleanup/lifetime runtime pendientes |
| CP02_NO_GO | NO-GO | No se avanza |
| CUSTOM_PROFILE_DLL_UNLOADING_BLOCKED | BLOCKED independiente | Sin reinvestigación |

La política nueva solo puede comprobar cumplimiento de sus reglas. No elimina agua volumétrica/BG exacto/transform/collider/IA ni lifetime, reciclaje invisible de ID o recursosGPU READY. Datos globales de actor y velocidades de Link del piloto real aún no están observados; la política estricta puede denegar una escena con actores globales/room desconocida. No se afloja para forzar un positivo.

Se conservan la admisión nativa NONE y ausencia de registro (históricos DISARMED_NO_REGISTRATION). El módulo experimental contiene creación y no se etiqueta como observador seguro instalable. STOP no cancela ni limpia: una solicitud podría seguir pendiente. Full exit no revierte saves.

Único trabajo siguiente: **revisión y autorización separadas del paquete experimental activo**, que requeriría proveedor explícito revisado, nueva build/auditoría; después, **autorización separada de la sesión cold-start G5** con respaldo/aislamiento/criterios de parada. Esta tarea termina aquí, sin esas acciones.
