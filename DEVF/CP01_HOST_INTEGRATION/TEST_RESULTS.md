# CP01 — matriz de integración del host

**PATCHED_HOST_BUILD_PASS; INTEGRATION_TEST_PASS dirigido (17 expectativas); seguridad activa BLOCKED.** DISARMED_NO_REGISTRATION; CP02 NO-GO.

| Comprobación | Estado acreditado | Alcance |
|---|---|---|
| Baseline intacto 413377f | BASELINE_BUILD_PASS reutilizado | Run 38256856294; no recompilado como otra prueba |
| Raíz 40457c6, cuatro gitlinks, 12  hashes antes/después | PASS estático | Checkout independiente; parche eea4742 exacto |
| Configure del host completo modificado | PASS | Run 38265011287, MSVC/preset del baseline |
| Build/enlace/PE AMD64 modificado | PATCHED_HOST_BUILD_PASS | Run 38265011287; build exit0 y PE inspeccionado, 40m13,797 s |
| Nuevos diagnósticos nativos de colas/layouts | INTEGRATION_TEST_PASS, 17/17 | Run 38270210787; compila/enlaza/ejecuta driver en6,328 s; intentos1–4 de configuración conservados |
| Laboratorio previo 25/25 | PASS previo conservado | Adaptadores sintéticos + DLL propia Windows; sin repetición rutinaria |
| ABI pública SDK Actor/Stage sin cambios de source | PASS estático | Solo 12 paths internos modificados; no equivale a compatibilidad runtime universal |
| Request factory, fases reales, mount/error/cancel | NOT_TESTED | Driver no ejecuta la factoría, Handler o recurso real |
| Retención DLL/contexto dentro del juego | NOT_TESTED | Laboratorio anterior e integración compilada no son ejecución del host |
| Seguridad ante reentrancia de destrucción | FAIL en diagnóstico controlado / BLOCKED | Recorrido exacto revisita tag retirado; handles invalidados por revisión estática, runtime NOT_TESTED |
| Teardown global después del loader | BLOCKED | main continúa con ui::shutdown; orden estático global no demostrado |
| Transición real de escena, recursos/componentes, otros mods/servicios | NOT_VERIFIED / NOT_TESTED | Sin contratos nuevos de drenado para servicios legacy |
| Ubicación previa y condiciones de ejecución Windows/DX12 | NOT_VERIFIED / NOT_TESTED, conservados | Sin nuevo análisis ni ejecución |
| Activación DEVF y GO CP02 | NO-GO | No instalación, TEST activo ni merge |

INTEGRATION_TEST_PASS se limita a las expectativas del diagnóstico con headers/layouts reales, siete TUs originales y funciones extraídas exactas. El driver utiliza adapters de owner/fase/capa/heap/proceso; el destructor controlado del diagnóstico no libera los procesos. No se permite afirmar PASS de runtime, render, DX12, colisión, aparición o descarga global segura.

El run completo figura en rojo únicamente por el driver antiguo C1083; configure/build/collect pasaron y el artefacto acredita PE y hashes. El diagnóstico corregido se ejecutó en otro run para evitar repetir el host. Los 31 warnings del host coinciden en código/mensaje y ocurrencias con el baseline; no hay nuevos tipos ni errores. D9025 pertenece solo al driver /Od. Dependencias: 43 archivos observados (23 descargas +20 fixtures) y15 repositorios Git/recursivos idénticos, ports vcpkg iguales.
