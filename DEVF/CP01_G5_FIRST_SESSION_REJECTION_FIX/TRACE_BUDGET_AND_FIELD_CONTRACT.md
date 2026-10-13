# Contrato de trazas acotadas

Dusklight2.0.3 Windows x64/DX12. **DISARMED_NO_REGISTRATION / READ_ONLY_DIAGNOSTIC / NEXT G5 NOT AUTHORIZED.**

24 normales +32 críticos +8 terminales=64, sin ampliar cuotas. Cache de24 signatures representativas incluye causa, contexto completo, actor/profile/owner y clase por eje; no todos los valores continuos de cada tick. La primera causa/identidad nueva se conserva, recurrencias repetidas incrementan dedup_skipped en lugar de vaciar la cuota. Oscilación entre causas ya conocidas queda contada y resumida, no como historial frame a frame ilimitado.

PREFLIGHT_REJECT que duplica LOCATION_POLICY_FAIL del mismo update/capture/causa se coalesce; otros rechazos y cambios genuinos de identidad/contexto no se confunden. Los críticos y terminales mantienen algoritmo y pools separados. LOG_BUDGET_EXHAUSTED y shutdown incluyen suppressed por clase/coalesced/dedup; contadores saturan sin wrap. Límites aún pueden truncar una sesión con más signatures de las soportadas; no se garantiza un registro completo.

Se añaden raw speedXYZ/speedF, speed_observed, exact_zero_mask, axis_class; delta_state/valid/previous_update/gap/XYZ; known_global_count y actor_global_scope_allowed condicionado a metadata/censo/distancia; unknown_actor_rejected para room no clasificable. Ninguno es aprobación física o admisión del mod. DIAGNOSTIC_OBSERVATION_NO_ADMISSION jamás muestra POLICY_PASS ni arma el provider.

LogService.write es void, sin ACK ficticio. drain después de regresar del controlador/capture, nunca en scope crítico. Errores de formato/sink se contabilizan y señalan falta de evidencia; no afectan control/latch ni reintentan infinitamente. No ficheros runtime/PII/pointers/threads. Evidencia real histórica27eventos está separada de SYNTHETIC_LAB. Futuro operador preservará solo líneasDEVF_PILOT sanitizadas, sujeto a permiso posterior.
