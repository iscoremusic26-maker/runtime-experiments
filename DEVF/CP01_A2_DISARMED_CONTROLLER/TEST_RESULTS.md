# Resultados de laboratorio y Windows/MSVC

**A2_DISARMED_CONTROLLER_PASS_LAB · A2_DISARMED_MSVC_LINK_PASS · A2_DISARMED_BINARY_AUDIT_PASS**. Alcance: código propio desarmado, dos laboratorios offline y link/auditoría estática. No host/game/DX12 ejecutado, no `.dusk` generado.

## Ejecuciones y procedencia

| Ejecución | Fuente propia / head privado CI | Resultado |
|---|---|---|
| [Windows run1](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38341748553) | e54566ebb9f3eaee50d872e95ae0e20f305221c1 / 3fdb50233e7de29a3d903550633cde682638925e | FAIL compilación de adaptación: C2664, const layer* pasado a getter público no-const. Configure/dependencias correctos. |
| [Windows run2](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38341931143) | **0fa942f3758cee7d901cf847651b47477aa032af** / **6ba5533ec4d32f0c7c3735481d300544a50a92f9** | PASS todos los targets/checks. Ledger compilado coincide con código final; documentos/evidencia posteriores no alteran código compilado. |

Cambio puntual: usar punteros devueltos mutables según firma pública, sin writes a host ni const_cast/SDK patch. Revisión detectó además desarme que podía borrar STOP previo a consumir latch; corregido preservando terminal y cubierto por `resolver_uncertainty_disarm_no_reset`. Añadida validación current==previous antes de seleccionar. Ningún fallo se sustituyó por Linux.

Runner Windows Server2025, imagen windows-2025-vs2026/20260925.250.1 (runner2.337.0). MSVC **19.51.36260.0**, toolchain14.51.36231, Visual Studio18; SDK Windows **10.0.26100.0**, x64; CMake4.4.3/Ninja/Release/C++20, /MD, /EHsc, /Zc:__cplusplus, /utf-8. SDK añade /FIglobal.h, /bigobj y TARGET_PC/WIDESCREEN_SUPPORT/AVOID_UB/VERSION0/MTX_USE_PS/PARTIAL_DEBUG. Fuente oficial40457c6, Aurora3227d76 y `.lib`9400986 bytes SHA256 `4dc4a511d761e6eb52541733fa31919a2234ed9cd5b2f16f8fea91c468f30ca4`. Se reutiliza integridad CP00; solo extraído/comprobado miembro .lib y CRC del ZIP privado completo. No build de Aurora/renderer/host.

Advertencias18 en headers públicos JUTTexture/JSUIosBase y pragmas antiguos, cero errores en run2. No se parchearon ni silenciaron para fabricar PASS.

## Pruebas nuevas ejecutadas con MSVC

| Grupo | Resultado | Garantía y límite |
|---|---|---|
| Controller lab | **70 PASS, 0 FAIL** | Guards node/child/scene/context, previous/root, revalidación, latch, reentry, C++throw antes/después, nesting/restauración, ID propio/readiness/pending/fallos/timeout/terminal/reuse informado. Source tests etiquetan cada caso. Engine simulado. |
| Adaptador lifecycle real + fake resolver/services | **29 PASS, 0 FAIL** | Host/epoch/función/header, initialize/update/shutdown/reentrada,16 diagnósticos acotados, reactivación desarmada. Incluye16 comprobaciones de log; no son29 pruebas del motor ni de resolver nativo. |
| Mutaciones temporales | **6/6 detectadas**, compiladas y ejecutadas | Doble intento, restore omitido, root permitido, ID ajeno, continuación tras error y transición ignorada. Cada exe retorna1 con fallos dirigidos esperados, no crash/compilefail. Definitivo sin mutaciones. |
| Guardas compile | **1 positiva y6 negativas PASS** | Config válido compila; missing/0/spawn/armed/mutation y fake sinLAB_ONLY rechazados C++. No runtime flag para habilitar creación. |
| ABI probe offline DLL | **LINK PASS**, no ejecutado | Current/SetCurrent/Root/IsDeleting/Search/IsCreating importados exactos; tipo create callback cotejado contra ActorSpawnParams. No request/create invocado. |
| Módulo desarmado | **LINK y auditoría PASS** | PE32+AMD64,16 imports de juego de lectura, servicios exactos y grafo sin request/scope fake/setter; fuente/map/disassembly correlacionados. |

Total laboratorios nuevos finales: **99 comprobaciones PASS, 0 FAIL**, más6 mutantes y7 expectativas de compilación. No se repitieron suites históricas. Preflight local C++ algorítmico69PASS y6 mutantes detectados antes del último cambio; es evidencia auxiliar, no resultado MSVC/SDK ni validación Linux del juego. El caso final adicional se ejecutó en MSVC.

## Comandos reproducibles del pipeline

```powershell
python DEVF/CP01_A2_DISARMED_CONTROLLER/ci/run_windows.py --source .official --inputs . --work "$env:RUNNER_TEMP/a2-disarmed"
# Dentro del script, después de validar fuente/.lib:
cmake -S DEVF/CP01_A2_DISARMED_CONTROLLER -B <WORK>/build -G Ninja -DCMAKE_BUILD_TYPE=Release -DCMAKE_C_COMPILER=cl -DCMAKE_CXX_COMPILER=cl -DDUSK_SOURCE=<OFFICIAL> -DDUSK_GAME_EXE=<WORK>/windows-amd64.lib -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
cmake --build <WORK>/build --target devf_a2_disarmed a2_controller_lab a2_adapter_lab a2_abi_link_probe --parallel 2
<WORK>/build/a2_controller_lab.exe
<WORK>/build/a2_adapter_lab.exe
dumpbin /headers <WORK>/build/devf_a2_disarmed.dll
dumpbin /imports <WORK>/build/devf_a2_disarmed.dll
dumpbin /exports <WORK>/build/devf_a2_disarmed.dll
dumpbin /disasm <WORK>/build/devf_a2_disarmed.dll
```

Ledger de comandos/tiempos completos en [result.json](evidence/windows-pass/result.json); macros, includes y flags efectivos en [compile-commands.json](evidence/windows-pass/compile-commands.json). Configure5.656s/build9.656s aproximadamente según ledger; mutaciones y guards separados. CI pull_request windows-latest privado, pinned actions, contents:read y persist-credentials:false. El token del mismo repo de inputs accede LFS; no credencial cross-repo ni resource original en logs.

windows-latest es una imagen móvil: se fijan SDK/dependencias/actions y se registra el toolchain efectivo, no se promete identidad byte por byte de futuros builds.

## Hashes de los binarios propios generados, sin distribuir

| Artefacto | Bytes | SHA256 |
|---|---:|---|
| devf_a2_disarmed.dll | 18944 | fd9f04fdd52c87ac29ed491f6cdcb8f1b39187ac6086179a8b033412ce5b5ad1 |
| a2_abi_link_probe.dll | 10240 | 06f144690ad1f1ab87dad530cd1ed0756835b1d7a66d41d6b5cdf642371f4e82 |
| a2_controller_lab.exe | 64000 | b80d45910aa1fbad11961988b44ee58571e164b5fa95907efe14f52a7a77bc5c |
| a2_adapter_lab.exe | 19456 | 239fca6e311773828581e33bee9848e46649c56becf35582e38ef434ab103965 |

Artefacto CI **solo texto**11787297060, ZIP SHA256 `7f4df21533e3ccc2f4ba24841c596d21a180deb8ee1cc87e635dc5e1280ee624`; descarga comprobada SHA/CRC y contenido .log/.json exclusivamente. Logs sanitizados preservados en Git para no depender de expiración30d. DLL/probe/EXE/.lib/ARC/log G2 no se publican ni instalan.

## Auditoría binaria concreta

[Binary review](evidence/binary-review.json) correlaciona mapa con instrucciones: update0x180001180 llama capture_owner0x1800014c0, disarm0x180001350 y validate_owner0x180001370; después snprintf y `call [rax+8]`0x1800012c9 desde svc_log0x1800060c8, exactamente LogService.write del SDK. Initialize solo valida headers/version; shutdown estado escalar. Enlace optimizado elimina begin_simulation/requested/observe y todos los helpers de laboratorio del módulo. La seguridad estructural no depende únicamente de esa optimización: no hay backend nativo en sus unidades.

Metadata ABI1, Host2.2/Log1.0/Game2 y solo cinco exports lifecycle/mod_ctx/mod_meta. IAT de dusklight.exe:16 getters/iterador/datos públicos; no setter/request ni servicio Actor/Stage/Hook. Imports CRT/KERNEL32 (incluido GetCurrentThreadId de startup) no son implementación propia de worker o comprobación OS de hilo. Ningún callback Create/post-create de DEVF.

Owner real y fases/recursos/readiness del nuevo actor, render/contacto/colisión, transiciones y cleanup: **NOT_VERIFIED/NOT_TESTED**. No derivar esos PASS del laboratorio ni enlace.
