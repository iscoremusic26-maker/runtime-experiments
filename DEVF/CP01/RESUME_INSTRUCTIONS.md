# Reanudar CP01 bloqueado
1. Recuperar tag DEVF_CP01 o rama checkpoint/devf-cp01-20261011 de Mods-Duskligh; leer handoff, GO_NO_GO y TEST_RESULTS. CP00 sigue conservado en tags anteriores. No iniciar CP02.
2. Build/laboratorio Windows PASS; no repetirlos salvo cambios o fallo nuevo. CI usa código principal 9aeca7c, head 8d1cb588... y PR #2 contra rama CI CP00; PR #1 intacto. Hashes y logs en evidence/. Artifact 11719761096 vence 2026-10-25.
3. Resolver dentro de CP01: evidencia de ubicación real segura y registro Stage tipado correcto, y lifecycle/unload de actores activos y pendientes. F_SP108 del demo es referencia, no certificación. No inventar coordenadas ni poner location_verified=true sin evidencia.
4. Mantener NO_AUTOMATIC_SPAWNS y clasificación BUILD ONLY hasta resolver. El loader no respeta shutdown failure como bloqueo de unload; no hot reload con actores. Ningún parche al motor autorizado por este checkpoint.
5. Tras revisión y nueva build/laboratorio, aplicar RUNTIME_TEST_PLAN en proceso limpio bajo encargo de prueba correspondiente. Solo entonces evaluar DEVF_CP01_TEST.dusk/GO. Cualquier evidencia real debe marcarse PASS/FAIL; lo demás NOT_TESTED. Detenerse en CP01.
