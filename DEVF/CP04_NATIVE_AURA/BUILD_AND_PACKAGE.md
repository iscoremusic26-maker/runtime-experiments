# Build, PE, package y descarga CP04

BUILD_PASS / PACKAGE_VERIFIED / DOWNLOAD_VERIFIED. [Run 38585920329](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38585920329), job 115927771473, SUCCESS. Fuente `18daf7648a35c5ee3a89b8a21f9f6d8248e25c30`, CI `4bea35d21049ccef0c8ea0f79ff86e066c43a563`. SDK 40457c6, Aurora 3227d76, import library/EXE originales fijados e intactos, sin build del host.

MSVC 19.51.36260 x64, VCTools 14.51.36231, Windows SDK 10.0.26100.0, CMake 4.4.3, Ninja Release. Script el **14 octubre 2026, 10:03:47–10:04:00 Panamá** (15:03:47–15:04:00 UTC), 13,93 segundos sin setup/subida. Comandos, versiones, mapas e imports: [evidencia final](evidence/windows-run-38585920329/result.json).

```text
cmake -S <CP04> -B <WORK>/build -G Ninja -DCMAKE_BUILD_TYPE=Release -DDUSK_SOURCE=<OFFICIAL> -DDUSK_GAME_EXE=<PRIVATE_IMPORTLIB> -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
cmake --build <WORK>/build --target devf_cp04_native_aura --parallel 2
dumpbin /headers <OWN_DLL>
dumpbin /imports <OWN_DLL>
dumpbin /exports <OWN_DLL>
cmake --build <WORK>/build --target devf_cp04_native_aura_package --parallel 2
```

Producción compila mod.cpp y SDK game_feature.cpp, sin laboratorio o tripwire. PE AMD64/ABI1, cinco exports, siete metadata records (header, cinco servicios Host2.2/Log1.0/Game2.0/Stage1.0/Hook1.1 y HookMEM72 del mismo execute), PMF8/import thunk exactos. **38 imports: 15 nativos y 23 CRT/sistema**. Nueve símbolos nuevos, obtenidos del importlib exacto y contrastados con PE: pool create, resource lookup/user-work, entry/get/cut/onActive y lecturas de g_dComIfG_gameInfo/mEmitterMng. Sin imports de GPU/manual patches, TLS/delay, ActorService o Actor create. Los data imports solo se leen; las operaciones mutables se limitan al emisor recién creado y métodos nativos de su registro.

Los cuatro negativos PE (x86, servicio Hook, target y export alterados) fueron rechazados; copias propias no cargadas. Trece casos TEST_FAKE reales MSVC pasaron en 38584533623. El run final reutiliza el grafo de laboratorio idéntico, cinco hashes/CMake/tests/headers y SDK/Aurora/lib/toolchain exactos. Único cambio de producto posterior: setRateStep(0) en el adaptador nativo, compilado de nuevo; el adaptador no se ejecuta en el mock. No se repiten suites históricas.

Paquete oficial, module ID dev.devf.cp04_native_aura, versión 0.4.0:

- `DEVF_CP04_NATIVE_AURA_windows-amd64_18daf7648a35c5ee3a89b8a21f9f6d8248e25c30.dusk`
- **14392 bytes**, SHA256 `221b6ea51b514905a0e8deb69648331ded809d00924482d855e8bc8895ff3fd6`.
- DLL interna/loose: **26624 bytes**, SHA256 `13c991b0c89bd7eb6be107e4a24cb4f3a0cf67d97582da38dfc02107a194d403`; igualdad antes/después de package.
- Solo mod.json, lib/, lib/windows-amd64/, lib/windows-amd64/mod.dll. CRC/rutas/duplicados/manifest/versión y PE PASS.

[TEST](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38585920329/artifacts/11905691294): ZIP15361 bytes, digest b9a626739120d70dbdf60b365ca4eda61c55dc5d7ca4b040f7b0125b067b0914. [TEXT](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38585920329/artifacts/11905676250): ZIP28307 bytes, digest2f35aa288b51142f4a07ee1e396bcce9fdd95d0c1f3f326bc0fb81350c5ea546. Ambos descargados realmente y contrastados: [download-verification.json](evidence/download-verification.json). Se verificaron hashes externos/CRC/ledger/source/CI, manifest externo igual al de CI y DLL/PE interna. No game/DLL o render enCI.

TEST caduca **13 noviembre 2026, 10:04:02 Panamá**, TEXT un segundo antes. Solo artefactos privados propios/texto saneado, sin host/lib/ROM/ARC/common.jpc/SDK binario o logs personales. No promesa de reproducibilidad universal byte a byte si cambia el runner.
