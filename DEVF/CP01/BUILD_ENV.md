# CP01 — build incremental de revisión de bloqueos
Se reutiliza el pipeline Windows validado; sin build SDK Linux, sin probe CP00, sin recompilar motor ni cambiar ZIP/EXE. Los insumos exactos y Aurora gitlink permanecen fijados. MSVC 19.51.36260.0 / Windows SDK 10.0.26100.0, Visual Studio 2026, Windows Server 2025, RelWithDebInfo x64.

Código principal ejecutado en CI: 745b06dc264032e6b669dd1cad376238b5135d47, mirror CI 63f211d24c9d20c7af2b4b33c66740a1b5dea9ad. Provenance por hash en DEVF/CP01_SOURCE.json. Rama principal existente checkpoint/devf-cp01-20261011 y CI cp01-ci/windows-msvc-20261011; PR #2 existente sin merge. CP00 y CP01 original/tags/PR #1 preservados.

```powershell
# Tras el mismo checkout LFS e integridad/preparación exacta del nuevo runner:
cmake -S DEVF/CP01 -B "$env:RUNNER_TEMP/cp01/build" -G 'Visual Studio 18 2026' -A x64 "-DCMAKE_GENERATOR_INSTANCE=C:/Program Files/Microsoft Visual Studio/18/Enterprise" "-DDUSK_DIR=$env:RUNNER_TEMP/cp01/dusklight-2.0.3" "-DDUSK_GAME_EXE=$env:RUNNER_TEMP/cp01/windows-amd64.lib" "-DDUSK_AURORA_DIR=$env:GITHUB_WORKSPACE/.cp00-deps/aurora"
cmake --build "$env:RUNNER_TEMP/cp01/build" --config RelWithDebInfo --target devf_cp01_package devf_cp01_safety_lab --parallel 2 --verbose
ctest --test-dir "$env:RUNNER_TEMP/cp01/build" -C RelWithDebInfo --output-on-failure --verbose
python DEVF/CP01/ci/verify_cp01.py --root . --work "$env:RUNNER_TEMP/cp01"
```

CMake genera un include temporal con cinco funciones de cleanup exactas del source verificado. El lab usa sustitutos explícitos de colas/slot, no un ABI de producción. Dos DLLs propias mínimas prueban FreeLibrary/PIN real en Windows sin cargar el EXE del juego. Esas fixtures no se instalan ni se usan como hooks o como PIN del mod.

El run anterior 38187694002 ejecutó CP01_affected_regression (--affected, nueve casos) y CP01_new_safety (14 casos). El run final 38189000074 ejecuta únicamente CP01_collision_ownership (--collision-only, seis casos) con DEVF_CP01_TEST_SCOPE=collision por defecto; no repite las suites anteriores. Para cambios futuros que sí las afecten existe la selección incremental explícita. El exe original mantiene opción sin selección para compatibilidad histórica, pero el pipeline de esta revisión no ejecuta sus 16 casos completos.

Verificación de paquete: mod.json, DLL AMD64 y DISARMED_NO_REGISTRATION exacto. Servicios/versiones y imports de modelo/colisión del EXE verificados estáticamente, sin invocar el juego. Artefactos: logs, metadata/funciones-hash/dumpbin propio, mod.dll y DEVF_CP01_BUILD_ONLY.dusk. No include con cuerpo de fuente original ni binarios originales en artifact, ni credenciales. Los hashes/metadata y extractos de logs se conservan en Git.

Run final: https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38189000074
Artifact: https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38189000074/artifacts/11720474171
Retención 14 días (26 de octubre UTC; 25 de octubre local, America/Panama). Hash DLL: 6d688d58782b2792a4a16fa58688fb98a4d465f5bbe8bcf96fb85c982e975415
Hash .dusk BUILD ONLY: 4c1978292620fa4ea8f4eb1e3758e29ae1d4477c222fd0bac31dbc08abcbcfde
Hash EXE de seguridad: 1530815210aa924c0fad7be0c354c85d32c98e5cdbc330f86d427e7359554605

Build y lógica seleccionada PASS; ubicación NOT_VERIFIED, juego/DX12 NOT_TESTED, TEST de actor no aprobado. Los informes históricos del checkpoint 092c1e6 siguen disponibles por tag.
