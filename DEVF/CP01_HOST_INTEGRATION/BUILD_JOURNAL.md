# CP01 — diario recuperable de integración

Estado intermedio 2026-10-12 15:03 UTC. No constituye el resultado final.

- Base 413377f / BASELINE_BUILD_PASS preservada. Parche eea4742 aplicado exactamente a los 12 archivos, sin cambios adicionales al host. Root 40457c6 y cuatro gitlinks idénticos al baseline.
- Rama principal experiment/devf-cp01-host-integration, PR draft #3. Snapshot completo 55cbce11239adb3375e6a40002dd67a331b9ac99, run38265011287/job114864857848: preflight/configure PASS; build en marcha, sin resultado disponible.
- Diagnóstico incremental en codex-cp00-inputs, PR draft #4: run38266308440/job114869241679 falló C1083 por PCH inexistente en el driver. Artifact11755157378 recibido y SHA/CRC/allowlist verificados, datos en evidence/directed-attempt1. No se ejecutó el diagnóstico de ese intento.
- Corregida únicamente configuración del driver (mantener /FI, retirar /Yu,/Yc,/Fp), extracción del destructor vacío exacto, path normalizado y tiempos UTC. Retry nativo 250aa82, run38267208054. No se repite el build del host ni la suite25.
- La revisión descubre reentrancia insegura del recorrido/handles y límite del cierre global posterior al loader. Riesgos BLOCKED; ningún resultado de compilación o laboratorio autorizará activación automática.

DEVF DISARMED_NO_REGISTRATION; runtime NOT_TESTED; CP02 NO-GO. Checkpoint intermedio DEVF_CP01_HOST_INTEGRATION_CONFIGURED. Los informes finales posteriores deben leerse antes de reanudar; no reiniciar CI sin comprobar los runs existentes.
