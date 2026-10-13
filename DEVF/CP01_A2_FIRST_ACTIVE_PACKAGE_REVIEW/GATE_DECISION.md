# Gates del paquete de revisión

**ACTIVE-CAPABLE / NOT INSTALLED / NOT RUN / SESSION NOT AUTHORIZED.**

Dusklight **2.0.3 Windows x64/DX12**; paquete ID`dev.devf.cp01_eoc_first_active_pilot` versión`0.0.1`; fuente compilada`a67662bec0be8ac7982dd8685f9ac29cc1c0ebea`.

| Gate | Estado | Evidencia |
|---|---|---|
| Fixed provider C/E_OC, live Key, A/B/C | PASS_STATIC / PASS_LAB | Provider real, hashes/ledger,46 checks |
| Compilación/enlace Windows/ABI | PASS | MSVC real SDK oficial; ABI headers recompilados en laboratorio run2 |
| PE/imports/exports/slot32/provider | PASS_STATIC | DLL suelta/interna/descargada + mapa/disasm |
| Oficial .dusk/integridad/security | PASS_STATIC | Target SDK, estructura4 entries, CRC/SHA, igualdad bytes |
| Private download | DOWNLOAD_VERIFIED | Archivo real reabierto en Codex |
| Main/CI recovery + historical integrity | PASS_STATIC | Fetch independiente,fsck,658 archivos y277 ledger,50refs |
| ACTIVE_PACKAGE_READY_FOR_PRIVATE_USER_REVIEW | SÍ | Entrega para revisión, no runtime |
| PROVIDER_ARMED_IN_BINARY | TRUE | Permiso técnico true/true, no NONE |
| USER_AUTHORIZED_TO_EXECUTE / INSTALL | FALSE | Veto operativo; ningún ensayo autorizado |
| LOCATION_SAFE_VERIFIED | NOT_VERIFIED / BLOCKED | Solo política por centros/probes |
| A2_RUNTIME_REQUEST/CREATION/RENDER/COLLISION | NOT_TESTED | No ejecución de juego/DLL |
| G5 | NO-GO | Hasta autorización humana posterior del paquete y sesión |
| G6 | NOT_VERIFIED | Cleanup/lifetime runtime pendientes |
| CP02 | NO-GO | Sin avance |
| CUSTOM_PROFILE_DLL_UNLOADING | BLOCKED independiente | Preservado, no reevaluado |

PACKAGE_BUILD_PASS ≠ PACKAGE_RUNTIME_PASS. PROVIDER_ARMED_IN_BINARY ≠ USER_AUTHORIZED_TO_EXECUTE. LOCATION_POLICY_PASS_LAB ≠ LOCATION_SAFE_VERIFIED. REQUEST_QUEUED ≠ ACTOR_READY; READY ≠ render/collider. PROCESS_EXIT ≠ rollback de autosave.

Link y otros centros XZ>=1600 no certifican collider, agro/persecución ni navegación; snapshots G4B no validan el nuevo censo global/velocidades. Water volume, BG exacto/transform y overlap siguen sin verificar. Recursos REGISTERED no prueban READY GPU ni render. IDs carecen de generación/lease universal; la petición es asíncrona y E_OC puede ejecutar antes de READY. Lifetime de room/layer incierto; globales desconocidos pueden bloquear todo intento. Randomizer/otros mods pueden interferir. STOP no cancela, elimina ni hace rollback; FULL EXIT no revierte autosaves. Hot reload/re-enable en vivo prohibidos, sin mecanismo para impedir una nueva imagen DLL del host. Unloading custom BLOCKED independiente, sin reinvestigación.
