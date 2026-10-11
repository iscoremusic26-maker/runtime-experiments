# CP01 — build Windows reproducible
Reutiliza el entorno validado CP00: fuente ZIP exacta 2.0.3, import library exacta y Aurora headers 3227d76c60e1e782ca576610bce61c9e7744d8be. No se repitió la build SDK Linux ni el probe CP00. Los ZIP se verifican en el nuevo runner por integridad, sin cambios a originales.

MSVC 19.51.36260.0, Windows SDK 10.0.26100.0, Visual Studio 2026/generador 18, Windows Server 2025. Configuración RelWithDebInfo x64, C++20, /MD, /Zc:__cplusplus y flags game ABI oficiales. Actor lab sin FEATURES game para ejecutar pruebas aisladas de Controller/ResourceLifecycle; DLL real con FEATURES game y enlace al EXE. Sin dependencias adicionales ni rebuild de motor/Aurora/Borealis.

Workflow: ci/cp01-windows.yml aquí; activo en .github/workflows/devf-cp01-windows.yml del repo privado codex-cp00-inputs, rama cp01-ci/windows-msvc-20261011, PR #2 en borrador contra rama CI de CP00. El PR #1 se conserva. Checkout head SHA exacto y LFS, contents:read, persist-credentials:false. No credencial entre repos privados: CI está junto a sus insumos. CI original y main no cambiaron.

```powershell
python DEVF/ci/verify_windows.py prepare --root . --work "$env:RUNNER_TEMP/cp01"
# vswhere selecciona instalación MSVC x64 y generador VS17/2022 o VS18/2026 disponible.
cmake -S DEVF/CP01 -B "$env:RUNNER_TEMP/cp01/build" -G 'Visual Studio 18 2026' -A x64 "-DCMAKE_GENERATOR_INSTANCE=C:/Program Files/Microsoft Visual Studio/18/Enterprise" "-DDUSK_DIR=$env:RUNNER_TEMP/cp01/dusklight-2.0.3" "-DDUSK_GAME_EXE=$env:RUNNER_TEMP/cp01/windows-amd64.lib" "-DDUSK_AURORA_DIR=$env:GITHUB_WORKSPACE/.cp00-deps/aurora"
cmake --build "$env:RUNNER_TEMP/cp01/build" --config RelWithDebInfo --target devf_cp01_package devf_cp01_lifecycle_lab --parallel 2 --verbose
ctest --test-dir "$env:RUNNER_TEMP/cp01/build" -C RelWithDebInfo --output-on-failure --verbose
python DEVF/CP01/ci/verify_cp01.py --root . --work "$env:RUNNER_TEMP/cp01"
```

CI final head: 8d1cb5889e59d6f2e89d3ee4e104d1caefb4936c; código principal compilado: 9aeca7c (provenance y hashes en DEVF/CP01_SOURCE.json del repo CI). Los informes añadidos después no cambian ese código compilado.

Run final: https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38185763365
Artefacto: https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38185763365/artifacts/11719761096
Retención: 14 días, vence 2026-10-25. Contenido permitido: logs, verificaciones, dumpbin de DLL propia, mod.dll y DEVF_CP01_BUILD_ONLY.dusk. No binarios originales, ZIP, EXE retail, .lib original, fuentes extraídas ni credenciales. En Git solo evidencia textual, fuente y hashes. No se afirma determinismo binario.

SHA256 DLL: 68d76960e3b8d2d3491814fe3dcf934dfa53c90f0fbb4dd02ed7c488996a655a
SHA256 BUILD_ONLY.dusk: be4d7be38e003b955a4301cc2294917ea2870277e8fcf83f9babef99e9b88dc1
SHA256 EXE de laboratorio ejecutado: 6cf87290501e0e938a92410300a5208ea100d9901f9140c0e66b3322c66282dc

Runtime del juego y DX12 NOT_TESTED. No paquete TEST aprobado por los bloqueos de ubicación/unload; ver GO_NO_GO y RUNTIME_TEST_PLAN.
