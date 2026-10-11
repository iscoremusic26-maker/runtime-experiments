# Entorno y build — CP00
Linux Cloud: g++ disponible. CMake 3.31.6 y Ninja 1.11.1.4 están en /workspace/setup-support/tools/bin, fuera de PATH normal. No cl, clang-cl, lld-link, SDK Windows ni Wine detectados. No instalar toolchains en este checkpoint ni utilizar MinGW como sustitución de ABI MSVC del juego.

La prueba existente /workspace/setup-support/build/mods/onboarding_sdk_smoke.dusk es Linux, proyecto onboarding_sdk_smoke, plantilla com.example.mod, RelWithDebInfo. Fue ejecutada durante configuración según usuario/install.sh; se preserva y no se repite. No prueba DEVF ni DX12.

Se prepara cp00-probe/ para comprobar imports Actor/Stage/Resource/Host/Log y GameService epoch 2, sin registrar, crear o modificar actores. Solo admite Windows x64 MSVC/clang-cl. Estado: NO COMPILADO. La configuración Linux fue rechazada por la guarda de plataforma como se esperaba; eso solo verifica la guarda, no la build Win64. No hay artefacto TEST ni mod final.

En Windows, con Visual Studio 2022 C++ x64 y Windows SDK, CMake >=3.25, extraer ambos ZIP verificados fuera de los originales y usar rutas reales. Ejemplo PowerShell (ajustar únicamente rutas):

```powershell
$devfSource = 'C:/devf/DEVF'
$devfSdk = 'C:/devf/inputs/dusklight-2.0.3'
$devfImplib = 'C:/devf/inputs/windows/sdk/windows-amd64.lib'
cmake -S "$devfSource/cp00-probe" -B "$devfSource/work/build-win64" -G 'Visual Studio 17 2022' -A x64 "-DDUSK_DIR=$devfSdk" "-DDUSK_GAME_EXE=$devfImplib"
cmake --build "$devfSource/work/build-win64" --config RelWithDebInfo --target devf_cp00_probe
```

El SDK oficial add_mod empaqueta build-win64/mods/devf_cp00_probe.dusk, con mod.json y lib/windows-amd64/mod.dll. DUSK_GAME_EXE en Windows debe ser la .lib, no el EXE. FEATURES game usa la biblioteca local exacta; evita descargar stubs de otra revisión y reconstruir todo el juego. No se usa fmt/webgpu para esta comprobación mínima.

Antes de un TEST: compilar y cotejar estructura del paquete, DLL PE AMD64, imports/exports y hashes; verificar el rechazo de host incompatible y resolución runtime de servicios en Windows 2.0.3. Instalación/ejecución en el PC no autorizadas en esta tarea. DX12, IA, colisión y render NOT_TESTED. CP00 sigue NO-GO mientras falte build verificable objetivo; no iniciar CP01.
