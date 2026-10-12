# Evidencia nueva — arquitectura oficial desarmada

## Windows/MSVC, sin compilación o ejecución del host

**PASS** del workflow [38277234930](https://github.com/iscoremusic26-maker/Mods-Duskligh/actions/runs/38277234930), job [114905580829](https://github.com/iscoremusic26-maker/Mods-Duskligh/actions/runs/38277234930/job/114905580829), sobre snapshot propio `20efbbf563ad1ec7edb7e22a27128ba07b77c7c7`. `GITHUB_SHA` del evento PR fue el merge ref sintético `a81e0f007bdb310d48cdd6b49c21854957f25df5`; checkout del workflow seleccionó expresamente head.sha. No se hizo merge real.

MSVC **19.51.36260**, toolset **14.51.36231**, Windows SDK **10.0.26100.0**, target **x64**, CMake **4.4.3**, runner Windows-2025Server-10.0.26100. Solo se usó SDK oficial root 40457c6 y aurora 3227d76 para headers; sin vcpkg, import library privado, otros submódulos, SDK Linux ni full-host configure/build.

Comandos efectivos completos, códigos y tiempos en [result.json](evidence/windows-pass/result.json). Comandos reproducibles desde Developer PowerShell x64, con rutas propias:

```powershell
cmake -S DEVF/CP01_OFFICIAL_ARCHITECTURE -B work/official-architecture -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER=cl -DCMAKE_CXX_COMPILER=cl -DDUSK_SOURCE=C:/ruta/official
cmake --build work/official-architecture --target devf_official_disarmed official_placement_lab game_abi_surface --parallel 2
./work/official-architecture/official_placement_lab.exe
```

No usar targets `all`, `*_package` o `install` como parte de esta revisión. El pipeline pidió explícitamente esos tres targets: módulo SDK service-only, laboratorio propio y objeto de comprobaciones de tipos. No se generó `.dusk`. Compilar el módulo service-only no precisa enlaces al ejecutable del juego; dumpbin confirma exportaciones mod_initialize/update/shutdown/mod_ctx y ausencia de import Dusklight. La comprobación de ABI solo compila datos/tipos, sin llamadas ni mutaciones de actores ni linking al host.

Configure **5,422 s**, build **5,500 s**, lab **0,015 s**; siete fases propias, todas exit 0. Inicio 2026-10-12 16:25:45 UTC; fin 16:26:00 UTC. DLL propia desarmada no distribuida: 10752 bytes, SHA256 `b2381b7bd38e9bcbd2773b586a9e6d0811f35182c59aeda06c50e46e1629ffba`. No es un EXE de juego ni un TEST runtime.

## Qué acreditan las pruebas

| Comprobación | Resultado y límite |
|---|---|
| ACTR/TGSC, endianness, nombre/parámetro/setID/ángulos, prefijo común | **PASS**, bytes sintéticos. No lectura/reanálisis ARC. |
| Rechazos de entradas inválidas | **PASS**, stage, room/layer, NaN/Inf, escala y kind. Validación de encoding, no de seguridad de ubicación. |
| ActorSpawnParams de definición con callback NULL | **PASS**, objeto de datos. No solicitud de creación. |
| Stage mock registra cero llamadas en cierre desarmado | **PASS**, laboratorio de nuestro prototipo, no implementación original de StageService. |
| Initialize/update/shutdown propios, host ausente/otra versión/cierre repetido | **PASS**, direct calls del laboratorio con servicios simulados. No descarga DLL real del host ni prueba del loader. |
| Salud/velocidad/escala/model pointer públicos; tamaños C++ 32/36, epoch2 | **PASS compile-only**, headers oficiales exactos. No semántica de setters ni aceptación runtime del objeto. |
| Módulo Windows/MSVC y exports/imports | **PASS compile/link**. Módulo no instalado/ejecutado en el juego. |
| 37 referencias de fuentes / clean tracked trees | **PASS**, preflight y comprobación posterior. Hashes locales y Windows con EOL explicados. |
| CRC/SHA256/allowlist de artefactos de CI | **PASS**, exclusivamente logs/JSON propios. |
| Aparición, readiness, render, colisión, escena, recompensas, limpieza y DX12 | **NOT_VERIFIED**; ejecución de juego **NOT_TESTED**. |
| Descarga segura de perfiles DEVF anteriores | **BLOCKED**, no reauditar ni repetir sus suites. |
| CP02 | **NO-GO**. |

[lab.log](evidence/windows-pass/lab.log) conserva **26 expectativas PASS**, no 26 pruebas del juego. No se repitieron suites de CP00/CP01 ni las 17 expectativas del host experimental.

## Primer intento y corrección de configuración propia

Run [38276827345](https://github.com/iscoremusic26-maker/Mods-Duskligh/actions/runs/38276827345), snapshot `883db67854f2cd8e13a53b666ed5f49c0cb35c54`: configure y módulo/lab compilaron, pero el objeto ABI falló C2440 en `std::exchange` del STL. Sin `/Zc:__cplusplus`, MSVC informa __cplusplus antiguo; Dolphin types.h define el token nullptr como NULL por compatibilidad y afecta headers C++ modernos. Se añadió esa opción **al target propio** del probe ABI, coherente con el CMake previo de CP01. No se alteró ningún archivo oficial, no se corrigió el juego ni se ocultó un fallo del host. Logs y resultado inicial **BLOCKED** quedan en [windows-first-failure](evidence/windows-first-failure).

## Integridad y procedencia de evidencia

Artefacto PASS ID **11759173058**, ZIP 8584 bytes, SHA256 `09dcc93a116682146c3b4dfffea02c6f4d7a8998ce83e9987544988ac590bd83`. Artefacto inicial ID **11758848796**, ZIP 6770 bytes, SHA256 `2fab3e4646518e843c50b532a24437694174faefd8dcb40bfb6a7ece678b0dd1`. Ambos coinciden con digest GitHub, CRC completo válido y allowlist de `.log/.json`, sin DLL/EXE/dusk, ARC, credenciales ni fuentes originales copiadas. Se conservan los textos en Git para no depender de la caducidad de Actions.

Las 37 fuentes del checkout Windows tienen CRLF; el checkout local tiene LF. La primera comparación de hashes raw detectó esa diferencia y **no se declaró igualdad binaria**. [windows-source-comparison.json](evidence/windows-source-comparison.json) acredita que cada fuente local coincide con el Git blob fijado tras normalizar exclusivamente EOL, y que su expansión a CRLF reproduce exactamente tamaño/SHA256 y líneas de referencia de la evidencia Windows. No se reescribió ninguna fuente. [artifact-download-verification.json](evidence/artifact-download-verification.json) registra tamaños, CRC y hash de cada texto recibido. Herramientas propias: `verify_sources.py` y `collect_evidence.py`.

El código C++/CMake/workflow del snapshot exitoso se conserva sin cambios en el checkpoint final. Los cambios posteriores son informes, evidencia y comprobación explícita de procedencia/EOL; no justifican volver a ejecutar compilación/suites ya aprobadas. La publicación documental lleva `[skip ci]`. La regla local `.gitattributes` conserva byte por byte los logs/JSON recibidos, incluidos CRLF y espacios de diagnósticos, para que sus hashes sigan coincidiendo con los miembros de los ZIP.
