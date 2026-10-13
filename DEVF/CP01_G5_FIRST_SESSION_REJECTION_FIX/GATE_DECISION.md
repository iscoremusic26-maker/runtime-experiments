# Gates separados

**Entrega diagnóstica verificada para revisión. NO-GO a una nueva aparición G5 y a CP02.**

| Gate | Estado | Límite |
|---|---|---|
| Log real G5 | PASS | 2.182 líneas/27 eventos correlacionados; ninguna request DEVF |
| room=-1 KYTAG04 | PASS_STATIC_CONDITIONAL / PASS_LAB | Solo validación de room para perfil686/group0/ownerPLAY coherente, no exclusión de censo/distancia; seguridad física NOT_VERIFIED |
| Speed/Temporal/Trace | PASS_LAB_REUSED_BY_HASH | Nuevas velocidades reales NOT_TESTED |
| Reposo Link | EXACT_ZERO_UNCHANGED; UNVERIFIED | Log histórico carece de speedXYZ/speedF; sin epsilon inventado |
| Build Windows, PE, grafo, imports/export exactos | PASS_STATIC | Run38466822325, 20 negativos PE; no game/loader |
| Paquete oficial | PASS / REVIEW_ONLY | Solo diagnóstico desarmado v0.0.2 |
| Descarga verdadera | PASS | CRC/SHA/PE/manifest/source ledger verificados independientemente |
| Nueva request/render/colisión/limpieza runtime | NOT_TESTED_IN_THIS_TASK | No DLL/game ejecutado |
| Ubicación segura / G6 | NOT_VERIFIED | Distancias y consultas puntuales no acreditan envolvente/colisión/agro/eventos |
| Descarga DLL custom | BLOCKED_INDEPENDENT | Limitación conservada, sin nueva investigación |
| Siguiente sesión G5 | FALSE / NO AUTORIZADA | No se instala/ejecuta diagnóstico ni activo |
| CP02 | NO_GO | No se avanzó |

Resuelto: duplicación propia de headers y rechazo del antiguo import manifest, con revisión del único memcmp adicional y auditor exacto propio. No resuelto: criterio físico de idle, inocuidad/contexto real de KYTAG04, validación runtime/localización y bloqueo independiente de unload.

Siguiente paso mínimo: revisar el diagnóstico/hashes y autorizar por separado una futura captura humana observacional de velocidades/deltas/owner/censo en contexto conocido, con retiro controlado del activo0.0.1 de rutas reales y proceso cerrado. Luego contrastar esos datos con source antes de proponer cambios de política o solicitud activa. Este informe no concede esa autorización. Matriz completa máquina en evidence/gate-decision.json.
