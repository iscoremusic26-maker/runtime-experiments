# CP06 — resultado focal de procedencia

**NO_GO_MULTIINSTANCE para el método register_edit opaco, sin modificar host.**

| Gate | Dictamen | Alcance |
| --- | --- | --- |
| P0 SRC_PROVENANCE | PASS | Fuente40457c6… y blobs exactos; trayecto documentado, primer eslabón perdido identificado. |
| P1 ABI_AND_SYMBOL | PASS | Evidencia estática del EXE exacto: símbolo resoluble offline, ABI x64 de entrada opaca y out-handle, flags/intervalo .pdata. No instalación de hook ni callback runtime. |
| P2 OWNER_TO_ACTOR_BRIDGE | NO_GO | El handle no entrega allocation de bytes interna; no se accede a ActorEditRecord/STL privado ni se sustituye por bytes/orden/posición. |
| P3 CORE_ISOLATION | NOT_RUN | P2 no pasó; no core genérico ni fake que aparente probar el puente. |

**SITE2_PENDING**, preservado sin nuevas consultas. No .dusk nuevo, build de mod/host, package/download, dos actores ni pruebas en el PC. Single-site v0.6.0, max1 y whitelist intactos.

Progreso NUEVO: se resolvió que register_edit **sí existe** en el binario aprobado y no presenta flags inline/multiname/dupname en su entrada. Se midió su ABI en358 bytes de una sola función y se ejecutó fixture propio MSVC del formato del manifiesto. No se usa esa medida para copiar offsets de STL en un mod.

[SYMBOL_AND_ABI](SYMBOL_AND_ABI.md), [prueba del bloqueo](OWNER_TO_BUFFER_PROOF.md), [opciones que requieren decisión](ARCHITECTURAL_OPTIONS.md), [resultados](TEST_RESULTS.md), [RECOVERY](RECOVERY.md).
Base d9a776567c9cb999118d6ef29dd34c99f4664085; rama feature/devf-cp06-register-edit-provenance-gate; PR40 draft. NO PROBAR NADA.
