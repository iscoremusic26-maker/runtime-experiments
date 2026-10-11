# CP01 — resultados verificables
| Área | Resultado | Alcance |
|---|---|---|
| Build MSVC/Windows SDK y enlace del actor real | PASS | DLL AMD64 con imports del EXE, modelo/colisión del juego |
| Paquete .dusk / exports / versiones de servicios | PASS | manifiesto, DLL y safety-policy exacta; seis required imports con record_size=80 |
| Laboratorio Windows compartido con implementación | PASS | 16 casos; Controller y ResourceLifecycle reales, tablas/actor/operaciones simulados |
| Recursos pendientes/completos y errores parciales | PASS laboratorio | no heap prematuro, terminal error, colisión solo si propia, release ordenado/idempotente |
| Registro, conflicto, Stage add y rollback | PASS laboratorio | handles y orden de llamadas; sin host real |
| Fallos de retirada y reintento | PASS laboratorio | ownership conservado, no nuevo start con cleanup pendiente |
| Orden modDeactivating antes de shutdown | PASS laboratorio + fuente | distingue perfil ya retirado y MOD_UNAVAILABLE; no valida DLL unload real |
| Stage vs runtime y duplicados | PASS laboratorio | exclusión mutua, un request por activación, ID no retenido |
| Callbacks create/execute/draw/delete | PASS simulados | no prueba de callbacks del Rock en el motor |
| Constructor/solid heap/J3D/Bgsp reales | NOT_TESTED | compilados/enlazados, sin ejecución dentro de Dusklight |
| Aparición Stage, sala/capa/escena, suelo, dibujo, colisión | NOT_TESTED | ninguna ubicación real segura acreditada |
| Limpieza de actor activo o pendiente y unload | NOT_TESTED / BLOCKED | loader descarga aun con error; cobertura de pending queue no demostrada |
| Host version gate, carga de servicios/política dentro del juego | NOT_TESTED | guardas implementadas, no host ejecutado |
| Windows DX12 / coexistencia retail | NOT_TESTED | no se ejecutó el juego ni se modificaron actores retail |
| CP02 | NOT_STARTED | fuera de alcance |

Run 1, 38185661092: build y 16 casos PASS; verificación de paquete FAIL por CRLF introducido en safety-policy.txt por checkout Windows. Corrección únicamente en .gitattributes nuevo de CP01 para mantener LF y preservar comparación exacta en runtime.

Run final 38185763365: build, laboratorio y verificación final PASS. MSVC 19.51.36260.0 / Windows SDK 10.0.26100.0 / Visual Studio 2026 / Windows Server 2025 / RelWithDebInfo x64. Actor: 14 advertencias y 0 errores; laboratorio: 0 advertencias y 0 errores. C4805/C4806 y pragmas C4068 de headers SDK; C4291 del placement new fopAcM_ct conservado del patrón oficial (no matching delete si constructor lanza). No se ocultan; no se acredita recuperación de una excepción real del constructor.

16 casos individuales y códigos de salida conservados en evidence/run-2-build-and-lab.log. No se usó assert desactivable por NDEBUG. Hashes en evidence/windows-verification.json y BUILD_ENV.md. Las fixtures LABONLY, callbacks y constantes de fase del laboratorio son simulación explícita, nunca registros de producción ni prueba del juego.

No hay DEVF_CP01_TEST.dusk aprobado. Solo DEVF_CP01_BUILD_ONLY.dusk con NO_AUTOMATIC_SPAWNS; no instalarlo como TEST. NO-GO a CP02 según GO_NO_GO.md.
