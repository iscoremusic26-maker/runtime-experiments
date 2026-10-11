# DEVF_CP01 — checkpoint de laboratorio
Fecha: 2026-10-11. **Build Windows y 16 casos de laboratorio PASS; NO-GO para CP02/TEST de juego.**

Autorización: petición CP01 adjunta, conservada en REQUEST_CP01.txt. Solo CP01. CP00 747ecc4/DEVF_CP00_WINDOWS y 8a14628/DEVF_CP00 permanecen intactos. Rama de trabajo checkpoint/devf-cp01-20261011; tag DEVF_CP01 identifica este checkpoint, sin merge automático.

Se implementó Rock adaptado del wrock oficial 2.0.3, perfil exclusivo dvfrock; creación por fases, modelo/colisión por instancia con BMD/DZB nativos compartidos mediante el gestor de recursos, solid heap, colisión, tick, dibujo y destrucción según APIs del demo. Se añadió estado compartido de recursos y controlador modular Actor/Stage con registros separados, exclusión de spawns, validación, cleanup idempotente, rollback y retención de handles ante errores. No guarda IDs/punteros efímeros ni reemplaza perfiles retail, EXE, escena, ROM o save. Ningún hook ni funcionalidad CP02.

Se detectó y trató el orden real: ActorService limpia en modDeactivating antes de mod_shutdown; StageService limpia en detach. La devolución de error de shutdown no impide unload_native, y no está probado el cierre de solicitudes de creación pendientes. El laboratorio prueba la lógica y los fallos usando servicios simulados; no ejecuta el motor.

Actions run 38185763365 PASS: MSVC 19.51.36260.0 / Windows SDK 10.0.26100.0, DLL AMD64/enlace al EXE, paquete/exports y required service records verificados. 16 casos Windows específicos PASS. Run anterior falló solamente la validación de safety-policy debido a CRLF, corregido con atributos Git de CP01. Evidencia/hashes durables en evidence/ y BUILD_ENV.md. No se repitió CP00 ni smoke Linux.

No existe ubicación segura real acreditada. Por instrucción explícita no se inventaron coordenadas: Stage y runtime no se activan en el módulo. Política empaquetada NO_AUTOMATIC_SPAWNS y guardas 2.0.3; se registra únicamente perfil sin instancia. El artefacto es DEVF_CP01_BUILD_ONLY.dusk, no TEST aprobado. Aparición visible, colisión, dibujo, sala/capa/escena, recursos/destroy/unload reales y DX12 NOT_TESTED. NO-GO permanece hasta cerrar estos bloqueos en CP01.

Código/proyecto completo, IMPLEMENTATION.md, TEST_RESULTS.md, GO_NO_GO.md, BUILD_ENV.md, RUNTIME_TEST_PLAN.md, CHANGES.md y RESUME_INSTRUCTIONS.md incluidos. PR CI #2 en borrador, PR CP00 #1 conservado, sin merge. No instalar artefacto ni iniciar CP02.
