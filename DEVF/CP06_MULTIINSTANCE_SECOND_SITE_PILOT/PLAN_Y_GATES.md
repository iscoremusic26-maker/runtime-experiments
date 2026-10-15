# CP06 — gates de correlación y segundo sitio

**CHECKPOINT_CP06_PARTIAL / NO_GO_MULTIINSTANCE / SITE2_PENDING.**

Base principal `3ab8ff2fdd42128ab75157338699b21ae6d768bd`, rama `feature/devf-cp06-multiinstance-second-site-pilot`, [PR39 draft](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/39), sin merge. El TEST parcial v0.6.0 y sus cinco ensayos permanecen históricos e intactos.

| Gate | Resultado de esta tarea |
| --- | --- |
| Base/cadena/PR38 | REPO_VERIFIED: 3ab8ff2… hijo directo de1a57ce17…, draft/open/unmerged. |
| Sello humano parcial anterior | TAG_SEALED, objeto `5b9f28473654e26efe9514d0e2543b561511f3b3` → `3ab8ff2fdd42128ab75157338699b21ae6d768bd`; API ref y objeto leídos. |
| Procedencia multiinstancia | NO_GO: falta demostrar vínculo propietario/handle/registro copiado → solicitud/ActorId; no se sustituye por coordenadas/orden. |
| Segundo sitio | STATIC_QUERY_PASS limitado para soporte del candidato norte; SITE2_PENDING para acreditación completa. |
| Dos activos | NOT_IMPLEMENTED; max_active=1 y whitelist previos sin cambios. |
| Mod nuevo/build/lab/PE/package/download | NOT_PERFORMED, gate de identidad no superado. |
| Runtime nuevo | NOT_TESTED; Codex no ejecutó juego ni pidió repetir cinco ensayos. |

Se hizo únicamente auditoría focal del traspaso de creación, consultas geométricas nuevas con lectores existentes y un workflow de sello segregado. No nueva ingeniería de render, ARC de modelos, ActorService, CP01–05, partículas, IA, CP07/08, Enemy Posture System ni Expansion. No se reconstruyó host/SDK/Aurora ni se instaló nada.

El checkpoint es un **NO-GO de implementación segura con la evidencia reunida**, no una afirmación de imposibilidad matemática de toda instrumentación interna. HookService sí permite símbolos locales; la asociación por ownership y su ABI/lifecycle aún deben demostrarse. Detalle en [PROVENANCE_AND_LIFECYCLE](PROVENANCE_AND_LIFECYCLE.md); nuevo resultado espacial en [SECOND_SITE_EVIDENCE](SECOND_SITE_EVIDENCE.md).
