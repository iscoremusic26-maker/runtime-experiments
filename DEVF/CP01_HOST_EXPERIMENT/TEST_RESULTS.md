# Validación incremental del experimento CP01

**25/25 PASS de laboratorio Windows. NO-GO de integración/producción.** Ningún resultado acredita ejecución del host completo o del juego.

Código probado del proyecto: `f627b88` (hash completo en `evidence/windows-validation.json`). Snapshot CI privado: `b9f03cbe10144c8ea240758dfae0f74917951891`. Las seis entradas de código/manifest de la evidencia son idénticas byte a byte entre ambos repositorios. Los cambios posteriores del checkpoint final son informes/evidencia, sin modificar ese código.

- [Run final 38204996509](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38204996509).
- [Job y logs 114666409226](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38204996509/job/114666409226).
- [PR CI draft #3](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/3); [PR experimental draft #1](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/1). Sin merge.

Windows x64, `windows-latest`, MSVC **19.51.36260.0**, Windows SDK **10.0.26100.0**, Visual Studio 18 2026, configuración `RelWithDebInfo`. Se compilan 22 cuerpos efectivos del parche y las declaraciones/definiciones efectivas de los scopes de ownership. No se compilan los archivos completos del motor. Colas, layouts, servicios, NativeModule y backend de eliminación son adaptadores sintéticos. LoadLibrary/FreeLibrary sobre la fixture CP01 propia sí son operaciones del Windows real.

Comandos efectivos (rutas temporales normalizadas; el workflow selecciona la instalación VS con vswhere):

```powershell
git lfs pull --include="dusklight-2.0.3.zip"
python DEVF/CP01_HOST_EXPERIMENT/ci/prepare_ci.py --root . --work "$env:RUNNER_TEMP/host-experiment"
cmake -S DEVF/CP01_HOST_EXPERIMENT -B "$work/build" -G "Visual Studio 18 2026" -A x64 "-DCMAKE_GENERATOR_INSTANCE=$vsPath" "-DDUSK_DIR=$work/dusklight-2.0.3" "-DEXTRACTED_DIR=$work/functions"
cmake --build "$work/build" --config RelWithDebInfo --parallel 2 --verbose
ctest --test-dir "$work/build" -C RelWithDebInfo --output-on-failure --verbose
```

El workflow exacto se conserva en `ci/windows-workflow.yml` y en el commit CI indicado. La preparación reutiliza el SHA conocido del ZIP fuente y hashes de los 12 archivos afectados como precondición; no repite los análisis de recursos, CP00 ni suites anteriores. No descarga el ZIP binario del juego. El parche normalizado LF se verifica por SHA antes de aplicarlo.

| Comprobación | Estado | Alcance / límite |
|---|---|---|
| Identidad de los 12 originales y correspondencia patch/manifest | PASS estático | Hashes antes y después, tanto local como runner |
| Compilación/enlace laboratorio Windows x64/MSVC | PASS | Funciones extraídas y fixture propia; no host completo |
| Pre-primer-callback, dueño del requester/perfil y cierre cruzado | PASS laboratorio | Adaptadores sintéticos |
| Solicitud opaca y marcada cancelada | PASS laboratorio | Bloquea hasta retirada de cola; no ejecuta `fpcCtRq_Cancel` real |
| Actor activo, destructor fallido y cola de borrado sin retirada | PASS laboratorio | No enmascara el fallo; mantiene registros |
| Reintentos, reentrancia, scopes anidados/excepciones | PASS laboratorio | Scopes efectivos del parche; backend sintético |
| ProfileName monótono, agotamiento sin wrap | PASS laboratorio | Nunca reutiliza un número en el proceso |
| Perfiles originales abiertos y callbacks personalizados en cierre | PASS laboratorio | No demuestra compatibilidad general del motor |
| Dependiente retenido, init fallida, errores de prehook/detach | PASS laboratorio | Campos/servicios del loader sintéticos |
| Shutdown incompleto conserva perfil/contexto/DLL | PASS laboratorio + Windows OS fixture | Callback devuelve fallo; DLL propia permanece cargada; retiro y FreeLibrary después de éxito |
| Shutdown exitoso, repetido, terminal bloqueado | PASS laboratorio | Cuarentena completa e idempotencia; no teardown global real del juego |
| Compilación/enlace host completo | BLOCKED | Faltan submódulos/gitlinks exactos del release y transitivas |
| Cola real, mount pending/error/cancel, escena y Stage ya aplicado | NOT_TESTED | Requiere integración del host |
| Ausencia universal de callbacks, ownership terminal real, compatibilidad otros mods | NOT_VERIFIED | No certificada por mocks ni por fixture OS |
| Registro/actores DEVF, render, colisión, DX12 | NOT_TESTED | DISARMED_NO_REGISTRATION |
| CP02 / TEST activo | NO-GO | Host y ubicación aún pendientes |

Los 25 nombres y resultados aparecen en `evidence/windows-lab.log`, extracto obtenido del job real. `patched-functions.json` se reconstruyó localmente desde el mismo patch/hashes probados; no se presenta como descarga del artefacto. El artefacto GitHub contiene únicamente logs propios y hashes, expira el 26 de octubre; los resultados persistentes quedan en Git. Su digest publicado y el historial de ejecuciones están en `windows-validation.json`.

El primer run falló en preparación por finales de línea Windows; no llegó al compilador. El segundo pasó 20 casos, antes de añadir scopes/wrappers efectivos y corregir la puerta cruzada. El run final pasó los 25. No se suman esos runs como casos distintos ni como pruebas de producción.

Las pruebas anteriores mantienen sus resultados históricos y no se vuelven a ejecutar. No se emiten binarios del juego ni TEST activo. Faltan dependencias exactas, integración real, pruebas de fases/escenas/teardown y la acreditación de ubicación ya documentada.
