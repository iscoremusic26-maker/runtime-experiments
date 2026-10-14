# Compilación, auditoría, paquete y descarga

**BUILD_PASS / PACKAGE_VERIFIED / DOWNLOAD_VERIFIED; HUMAN_RUNTIME_NOT_TESTED.** [Run 38541018826](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38541018826), job 115775493318, SUCCESS. Fuente `9dd5b8efd4ad98f1d6260820d782e101366a0f8b`, CI `7fd3628ee8bfeb30f8070db061220796c1c15b4a`.

MSVC 19.51.36260 x64, VCTools 14.51.36231, Windows SDK 10.0.26100.0, CMake 4.4.3, Ninja/Release. SDK 40457c6, Aurora 3227d76 y import library originales intactos. Windows-latest privado, sin build del host ni juego. Script el **14 octubre 2026, 04:16:21–04:16:36 Panamá** (09:16 UTC), 14,55 segundos sin setup/subidas. Comandos y tiempos exactos: [result.json](evidence/windows-run-38541018826/result.json).

```text
cl /Bv /c <WORK>/build/version.cpp
cmake -S <PROJECT> -B <WORK>/build -G Ninja -DCMAKE_BUILD_TYPE=Release -DDUSK_SOURCE=<OFFICIAL> -DDUSK_GAME_EXE=<PRIVATE_IMPORTLIB> -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
cmake --build <WORK>/build --target devf_cp03_hp_diagnostic --parallel 2
dumpbin /headers <OWN_DLL>
dumpbin /imports <OWN_DLL>
dumpbin /exports <OWN_DLL>
cmake --build <WORK>/build --target devf_cp03_hp_diagnostic_package --parallel 2
```

Laboratorio real MSVC del primer run: `cmake --build <WORK>/build --target cp03_diagnostic_lab --parallel 2`, después `cp03_diagnostic_lab.exe <caso>` para 17 casos separados. El último run reutiliza sus resultados con seis hashes CPP/headers/tests/CMake, SDK/Aurora/lib/toolchain exactos. No rerun de suites históricas ni de casos nuevos sin cambios.

Producción compila src/mod.cpp y game_feature.cpp del SDK, sin tests/tripwire. PE AMD64/ABI1, cinco exports, siete records (header, Host2.2/Log1.0/Game2.0/Stage1.0/Hook1.1 y HookMEM72), PMF8 unido al execute nativo exacto. **29 imports: 6 nativos sin cambios y 23 CRT/sistema**; nuevo __std_terminate revisado. Sin TLS/delay, ActorService, parches manuales o gráficos. Cuatro negativos rechazados: x86, serviciohook, target y export alterados, usando copias propias nunca cargadas.

Paquete genuino del SDK:

- `DEVF_CP03_HP_DIAGNOSTIC_windows-amd64_9dd5b8efd4ad98f1d6260820d782e101366a0f8b.dusk`
- **11975 bytes**, SHA256 `0d9882b072fe5cd6248c16a181171a47364e1acf5870503c1eb2f39c668b4344`.
- DLL interna/loose: **22016 bytes**, SHA256 `6951304f4cadfadc845e1760f31ba7582508a157738aceaac404c6d53b1b3eeb`; igualdad exacta antes/después del package.
- Solo mod.json, lib/, lib/windows-amd64/, lib/windows-amd64/mod.dll. Identidad de módulo y versión 0.3.1, CRC, rutas, duplicados y hashes PASS.

[TEST](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38541018826/artifacts/11881653953): ZIP12815 bytes, digest bb4d467aef263e35d6c4bdf90a3d2ebaee6f086dac5e9531c9fd3be4de0bdaa2. [TEXT](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38541018826/artifacts/11881743937): ZIP27144 bytes, digest620febc03004295f4714471893763d417dfc9e4ee517adfffde026228570c4e4. Ambos descargados realmente, verificados con ci/verify_download.py: CRC, ledgers, manifest externo igual al de CI, fuente/CI, DLL interna y PE. [Resultado posterior a descarga](evidence/download-verification.json).

TEST caduca **13 noviembre 2026, 04:16:37 Panamá** (09:16:37 UTC); TEXT un segundo antes. Descargar con acceso al repo privado. Artefactos propios únicamente; nunca EXE, ROM, .lib, saves, ARC o logs personales. No reproducibilidad universal byte a byte ante otra imagen de runner. DLL/backend de producción y juego no ejecutados.

## Estado posterior al build

El HUMAN_RUNTIME_NOT_TESTED y la ausencia de ejecución del juego anteriores describen el build/CI y la actividad de Codex. El usuario completó después la prueba v0.3.1: [CP03_HUMAN_RUNTIME_PASS, con procedencia y límites](HUMAN_RUNTIME_RESULTS_2026-10-14.md). No se recompiló, modificó o redistribuyó el paquete. El cierre midió nuevamente el mismo .dusk previamente descargado y los 17 archivos del ledger; [integridad medida](evidence/human-runtime-closure-integrity-2026-10-14.json). La disponibilidad remota del TEST se confirmó mediante metadata de GitHub, sin afirmar una descarga nueva.
