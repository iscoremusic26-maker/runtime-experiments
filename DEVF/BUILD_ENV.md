# Entorno y build — CP00 Windows
**Build nativa MSVC y verificación estática: PASS. Runtime del juego y DX12: NOT_TESTED.**

Fuente principal: ZIP 2.0.3 con hashes originales conservados. El Cloud local sigue siendo Linux; no se usó su compilador para esta build. La prueba onboarding_sdk_smoke ya realizada permanece intacta y no fue repetida.

## Ejecución verificada
- Runner: windows-latest, Windows Server 2025, imagen windows-2025-vs2026 20260925.250.1.
- Visual Studio 2026 / generador Visual Studio 18 2026 / toolset v145.
- Compilador MSVC 19.51.36260.0, toolchain directory 14.51.36231; Windows SDK 10.0.26100.0.
- RelWithDebInfo, x64, C++20, /MD, /Zc:__cplusplus y flags ABI del SDK oficial.
- Run final: https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38184306482
- CI head: fd97763510b7db06cb0c773581bad108604128c1; mirror de fuente principal 8fdcec0 según DEVF/CP00_SOURCE.json.

Workflow completo revisable: DEVF/ci/cp00-windows.yml en repo principal; activo en .github/workflows/devf-cp00-windows.yml de la rama cp00-ci/windows-msvc-20261011 del repo privado de insumos. PR #1 en borrador, sin merge. Checkout del head exacto, LFS, permisos contents:read y persist-credentials:false. El token del mismo repo pudo leer los originales; no se creó ni publicó ninguna credencial entre repositorios.

## Comandos
Tras checkout LFS, el script comprueba SHA256/CRC y extrae la fuente y únicamente windows-amd64.lib a RUNNER_TEMP. El ZIP Windows original nunca se altera y el juego no se ejecuta.

```powershell
python DEVF/ci/verify_windows.py prepare --root . --work "$env:RUNNER_TEMP/cp00"
# El workflow usa vswhere para escoger la instalación MSVC x64 y generador 17/2022 o 18/2026.
cmake -S DEVF/cp00-probe -B "$env:RUNNER_TEMP/cp00/build" -G 'Visual Studio 18 2026' -A x64 "-DCMAKE_GENERATOR_INSTANCE=C:/Program Files/Microsoft Visual Studio/18/Enterprise" "-DDUSK_DIR=$env:RUNNER_TEMP/cp00/dusklight-2.0.3" "-DDUSK_GAME_EXE=$env:RUNNER_TEMP/cp00/windows-amd64.lib" "-DDUSK_AURORA_DIR=$env:GITHUB_WORKSPACE/.cp00-deps/aurora"
cmake --build "$env:RUNNER_TEMP/cp00/build" --config RelWithDebInfo --target devf_cp00_probe_package --parallel 2 --verbose
python DEVF/ci/verify_windows.py verify --root . --work "$env:RUNNER_TEMP/cp00"
```

Para VS2022 local, usar el generador 17/2022 y rutas reales, manteniendo el mismo SDK/fuente/Aurora. DUSK_GAME_EXE en Windows debe ser la .lib exacta, no el EXE. Target _package genera el .dusk; el comando inicial sin ese sufijo solo pedía DLL. FEATURES game añade epoch GameService 2.0 y flags oficiales; no recompila el juego, Aurora ni Borealis. Sin fmt ni webgpu.

## Dependencia y correcciones
El ZIP omite submódulos. Se cotejó tag v2.0.3/40457c6adb381928e4b5fef6ed459ed291edd5e2: 19366 blobs exactos; gradlew.bat difiere solo CRLF/LF. Aurora se fija en su gitlink 3227d76c60e1e782ca576610bce61c9e7744d8be y se descargan solo encabezados públicos por checkout sparse. DUSK_AURORA_DIR aporta include paths externos, sin parchear el ZIP ni el árbol original.

Run 1 FAIL: VS2022 no existe en imagen actual; corregido seleccionando versión instalada con vswhere. Run 2 FAIL C2440: Aurora usa __cplusplus para compatibilidad nullptr/NULL, mientras MSVC lo deja antiguo por defecto; /Zc:__cplusplus corrige solo el target CP00. Runs 3 y 4 PASS; el cuarto verifica además record kind/flags/major/minor exactos en la DLL y registra hashes. 4 advertencias C4805 de JSUIosBase, 0 errores.

## Alcance de verificación y artefactos
Paquete solo mod.json y lib/windows-amd64/mod.dll; PE32+/AMD64/DLL, exports mod_ctx/mod_meta/lifecycle, seis servicios requeridos con versiones exactas, enlace a dusklight.exe/fopAcM_SearchByID. El probe exporta la dirección del símbolo sin invocarlo; no crea, busca ni muta actores.

Artifacts restringidos a evidence/: logs de build/configuración, JSON, dumpbin de la DLL propia, mod.dll y .dusk recién generado. No ZIP originales, EXE retail, .lib original, fuente extraída, credenciales ni otros mods. En Git se conservan solo informes/extractos de logs y hashes; binarios nuevos permanecen en artifact privado.

Antes de instalación como TEST deben verificarse loader, servicios y guardas en el host real bajo encargo correspondiente. No se ejecutó Dusklight ni DX12. El GO de CP00 permite proponer laboratorio CP01, no certifica runtime ni inicia otra etapa.
