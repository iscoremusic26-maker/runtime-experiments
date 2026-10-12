# CP01 — baseline oficial Windows x64 sin parche

Checkpoint de partida: `eea4742` / `DEVF_CP01_HOST_LIFETIME_EXPERIMENT`. Esta etapa tiene alcance propio: recuperar dependencias y compilar el host original. No aplica `host-lifetime.patch`, modifica el código DEVF ni repite auditorías o estudios de ubicación. DISARMED_NO_REGISTRATION y CP02 NO-GO se conservan.

Estado inicial: compilación Windows pendiente. No declarar BASELINE_BUILD_PASS hasta terminar configure + build/install y verificar el PE x64 y source limpio.

## Procedencia comprobada

Checkout independiente oficial `TwilitRealm/dusklight`, tag `v2.0.3`, raíz `40457c6adb381928e4b5fef6ed459ed291edd5e2`. Los cuatro gitlinks coinciden con los facilitados por el usuario y HEAD de cada submódulo descargado. No se reidentificaron desde cero. Ninguno de esos cuatro submódulos registra gitlinks transitivos; las restantes dependencias las obtiene el CMake oficial bajo sus condiciones y pins.

Comparación incremental con el ZIP fuente previamente verificado: **19.366 blobs idénticos**, sin extras, más un único archivo `platforms/android/gradlew.bat` equivalente tras normalizar LF/CRLF. La diferencia está declarada por `.gitattributes` (`*.bat text eol=crlf`). No hay diferencia de contenido fuente ni cambio de código. No se repiten CRC, integridad de ARC, CP00 ni análisis antiguos. Evidencia en `evidence/source-tree-vs-zip.json`.

`SOURCE_LOCK.json` fija raíz, cuatro gitlinks y los 12 hashes **originales** del manifiesto anterior como prueba de que el parche no se aplicó. `evidence/official-dependencies.json` recoge los 38 bloques FetchContent declarados, incluidos algunos condicionales/inactivos: esa lista no significa que se descarguen todos. El resultado de CI inventariará las descargas efectivas.

## Infraestructura y configuración

Preset oficial `x-windows-ci-msvc`: Ninja, MSVC amd64, RelWithDebInfo, CRT DLL, debug Embedded, vcpkg x64-windows, sccache y Sentry habilitado como en CI oficial. Se ejecutan `cmake --preset x-windows-ci-msvc` y `cmake --build --preset x-windows-ci-msvc --parallel 2`; el build preset incluye **install**. Install prepara exclusivamente `official/build/install`, nunca la instalación del usuario. No se ejecuta el juego.

El workflow oficial no fija la revisión de `C:\vcpkg` ni todas las herramientas del runner. Para esta referencia se fija infraestructura, sin alterar pins del source: vcpkg release `2026.07.29`, commit `9e593bb18ea69cc5095e012465dcd675a822ed0d`, tool release `2026-07-27`; sccache `v0.12.0`; acciones fijadas por SHA. Los ports freetype **2.14.3** y zstd **1.5.7** coinciden con las versiones del fallback vendor de Aurora. Se instalan los dos roots del CI oficial y solo sus transitivas; se desactiva la caché binaria implícita para acreditar procedencia. MSVC/SDK/CMake/Ninja efectivos se registrarán en CI, ya que el proyecto no fija sus versiones completas.

Dawn/SDL3/nod se resuelven según las reglas originales del provider `auto` para Windows; no se cambia a versiones aproximadas ni se desactiva funcionalidad. Algunas descargas del proyecto tienen hash, otras solo release/tag: conservar esa limitación y registrar el hash observado. Los parches que el propio CMake aplica a dependencias, como funchook/capstone, forman parte del baseline oficial; no son el parche experimental DEVF.

Los artefactos de Actions se limitan a logs propios y metadatos. No se suben EXE/DLL, archivos .dusk de los demos oficiales, recursos originales ni archivos fuente extraídos. No se pide SENTRY_DSN ni se publica credencial alguna.

## Reproducción

Ver `.github/workflows/devf-cp01-official-baseline.yml` y scripts en `ci/`. Recuperar esta rama/checkpoint en un checkout separado. Checkout del root por SHA y fetch de la etiqueta comprobada; submodule update de los cuatro paths exactos; checkout de vcpkg por SHA; MSVC amd64 + sccache fijado; bootstrap-vcpkg; `vcpkg install freetype:x64-windows zstd:x64-windows`; preflight; configure; build/install; colección de identidad y limpieza.

No aplicar el parche experimental. Esta etapa se detiene al terminar el baseline o identificar un bloqueo preciso. Incluso BASELINE_BUILD_PASS no acreditaría runtime/DX12, seguridad del unload ni GO de CP02.
