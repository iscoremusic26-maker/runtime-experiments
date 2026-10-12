# CP01 — integración del host completo

Estado inicial: PATCHED_HOST_BUILD_BLOCKED (resultado CI pendiente), runtime NOT_TESTED; CP02 NO-GO. DEVF DISARMED_NO_REGISTRATION.

Base documental 413377f / DEVF_CP01_OFFICIAL_BASELINE_MSVC. Original 40457c6 y los cuatro gitlinks del baseline preservados. El parche existente de eea4742 se aplica con prepare_experiment.py y se verifican los 12 hashes antes/después. No se reconstruye una etapa baseline: el preflight intacto precede a la aplicación en un runner nuevo.

CI reutiliza acciones, versiones, vcpkg, preset, scripts y procedimientos acreditados. La única opción adicional es CMAKE_EXPORT_COMPILE_COMMANDS=ON, para observar los consumidores compilados, sin cambiar funcionalidades ni dependencias. Todo el build del runner corresponde al árbol modificado.

Los EXE y source extraído permanecen temporales; el artefacto admite solamente logs/JSON propios. No se instala ni ejecuta el juego. No se repiten auditorías de ubicación ni los 25 tests sintéticos por rutina.
