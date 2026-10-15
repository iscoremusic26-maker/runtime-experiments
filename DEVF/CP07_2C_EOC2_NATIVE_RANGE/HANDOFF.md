# Handoff CP07.2C
Fuente compilada 02e9070497bfe0ec2fda83ea63fd2ca237fb6dfd; source base 7c588d2a06d307b0288256fc2383186129430401. Estado al build: proveedor 0.7.4 listo sólo para QA humana; consumidor histórico 0.1.0 obligatorio sin cambios. Ambos servicios @1.0 preservados; capacidad global2 y bootstrap sin cambios.
Un cambio de record: BE24=0132 sólo en EncounterBroker::record. Byte25 06→32. Legacy0106 intacto; finite5000, no persecución infinita ni garantía visual.
Build 38812099184 SUCCESS; verificador final 38812605127 SUCCESS; intento anterior 38812467385 FAIL documentado.
[Paquete](BUILD_AND_PACKAGE.md), [QA](HUMAN_TEST.md), [rollback](RECOVERY.md). No ejecutar de nuevo el build ni reempaquetar el consumidor para recuperar este checkpoint.
Plan histórico antes del feedback: esperar observación humana del rango/retirada; executeWalk/home puede seguir produciendo regreso; no añadir IA, hook, HIO,01FF ni ajustes de terreno. No existe resultado gameplay de Codex.

## Estado vigente — cierre humano
**CP07_2C_FIX_RUNTIME_PASS_USER_OBSERVED_WINDOWS_DX12**. Usuario: «Ya hice la prueba y ahora se comportan como los bokoblin normales». A_ONLY y BOTH con proveedor0.7.4/consumidor0.1.0, legacy0, Zora Swim1.3.0; solicitudes y limpieza result=0 según extractos comunicados. [acta humana del 15-10-2026](HUMAN_RUNTIME_RESULTS_2026-10-15.md) contiene procedencia, hashes, advertencias y límites. Codex no leyó rawlogs ni jugó.
Incidencia resuelta en ese alcance. No reabrir IA ni pedir nuevas pruebas; siguiente funcionalidad sólo cuando se autorice. No se certifican distancias, paridad completa retail, todos los estados home, cooperación o rendimiento universales. Código, paquetes y manifest congelados intactos.
