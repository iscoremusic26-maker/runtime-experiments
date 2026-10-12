# Reproducir únicamente el baseline oficial

Recuperar el checkpoint de esta etapa en un checkout independiente. La implementación DEVF y host-lifetime.patch no se aplican ni se modifican. No instalar el resultado en la PC del usuario, ejecutar Dusklight, activar mods o cambiar saves.

El snapshot CI probado durante esta etapa es 65c9b8b47f38ea966f5cb69fbc2e5b2623a785ba. Los informes posteriores se publican con [skip ci] para evitar reconstrucciones rutinarias sin cambios de código. Comprobar SOURCE_LOCK.json, la identidad del workflow/scripts y el resultado final de Actions antes de volver a compilar.

En un entorno Windows x64 independiente con MSVC, Windows SDK, CMake, Ninja, Python y sccache v0.12.0 disponibles, desde un Developer Prompt amd64:

```powershell
git -c core.autocrlf=false -c core.eol=lf -c core.longpaths=true clone --depth 1 --branch v2.0.3 --no-recurse-submodules https://github.com/TwilitRealm/dusklight.git official
git -C official rev-parse HEAD
# Debe ser 40457c6adb381928e4b5fef6ed459ed291edd5e2.
git -C official -c core.longpaths=true -c core.eol=lf -c core.autocrlf=false submodule update --init --depth 1 extern/aurora extern/borealis mods/randomizer mods/cosmetics
git -C official ls-tree HEAD extern/aurora extern/borealis mods/randomizer mods/cosmetics
git -C official submodule status
git clone --depth 1 --branch 2026.07.29 https://github.com/microsoft/vcpkg.git baseline-vcpkg
git -C baseline-vcpkg rev-parse HEAD
# Debe ser 9e593bb18ea69cc5095e012465dcd675a822ed0d.
$env:VCPKG_ROOT = "$PWD/baseline-vcpkg"
$env:VCPKG_BINARY_SOURCES = 'clear'
& "$env:VCPKG_ROOT/bootstrap-vcpkg.bat" -disableMetrics
& "$env:VCPKG_ROOT/vcpkg.exe" install freetype:x64-windows zstd:x64-windows
$evidence = "$PWD/baseline-evidence"
python DEVF/CP01_BASELINE/ci/baseline_evidence.py preflight --source official --vcpkg baseline-vcpkg --evidence $evidence --lock DEVF/CP01_BASELINE/SOURCE_LOCK.json
python DEVF/CP01_BASELINE/ci/run_phase.py --phase configure --source official --evidence $evidence -- cmake --preset x-windows-ci-msvc
python DEVF/CP01_BASELINE/ci/run_phase.py --phase build --source official --evidence $evidence -- cmake --build --preset x-windows-ci-msvc --parallel 2
python DEVF/CP01_BASELINE/ci/baseline_evidence.py collect --source official --vcpkg baseline-vcpkg --evidence $evidence --lock DEVF/CP01_BASELINE/SOURCE_LOCK.json
```

Detenerse si cualquier comando falla. Mantener la revisión exacta y versiones registradas; no usar HEAD ni cambiar hashes para pasar. En CI se fijan core.eol/core.autocrlf por entorno antes de todos los checkouts, incluso submódulos; localmente hacerlo también para cada checkout. *.bat sigue CRLF según atributos oficiales. Si un clon local trae CRLF inesperado, corregir la configuración en una nueva copia antes de verificar hashes, no relajar el preflight.

El workflow conserva el preset oficial y descarga únicamente las transitivas seleccionadas por CMake/vcpkg. Install prepara official/build/install. Nada de ese staging se incluye en el checkpoint ni los artefactos: conservar solo JSON/logs propios.

GitHub puede requerir que workflow_dispatch exista en la rama por defecto. No hacer merge para habilitarlo. La ejecución acreditada es la del PR draft de esta etapa; para otra ejecución autorizada usar un PR nuevo con el snapshot CI o los comandos Windows anteriores. No relanzar el build activo antes de inspeccionar su resultado.

Reversión: retirar solamente el checkout/staging independiente creado para la prueba. No hacer reset/clean sobre trabajo existente, ni tocar instalaciones, ejecutables o partidas. Esta etapa finalizó con BASELINE_BUILD_PASS. La integración del parche queda para una tarea posterior; no hacerlo aquí.

Checkpoint final: DEVF_CP01_OFFICIAL_BASELINE_MSVC. Recuperarlo con git fetch origin tag DEVF_CP01_OFFICIAL_BASELINE_MSVC, resolver el tag a commit y verificar que eea4742 es ancestro. El tag intermedio DEVF_CP01_BASELINE_CONFIGURED y los anteriores permanecen intactos. Los metadatos y logs recibidos están versionados en evidence/final; el ejecutable no se conserva como entregable.
