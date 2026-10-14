# Compilación y paquete verificados

**BUILD_PASS · PACKAGE_VERIFIED · DOWNLOAD_VERIFIED. HUMAN_RUNTIME_NOT_TESTED.**

Fuente compilada `b39e010d1a25168dee8de0c2c7740957d76dd853`; CI `4f84a7137011a35f0500dc7ae1104420e58fbb30`. [Run 38513406897](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38513406897), job 115686769327: SUCCESS.

MSVC **19.51.36260 x64**, VCTools 14.51.36231, Windows SDK **10.0.26100.0**, CMake 4.4.3, Ninja/Release. SDK/Aurora fijados en SOURCE_MANIFEST. Import library original: 9400986 bytes, SHA256 `4dc4a511d761e6eb52541733fa31919a2234ed9cd5b2f16f8fea91c468f30ca4`, CRC `70c35731`. No se compiló host ni modificó SDK. Script: **13 octubre 2026, 23:50:28–23:50:43 Panamá**, 14,43 segundos sin setup/subidas; UTC y tiempos por comando en [result.json](evidence/windows-run-38513406897/result.json).

Comandos efectivos, con rutas saneadas:

```text
cl /Bv /c <WORK>/build/version.cpp
cmake -S <PROJECT> -B <WORK>/build -G Ninja -DCMAKE_BUILD_TYPE=Release -DDUSK_SOURCE=<OFFICIAL> -DDUSK_GAME_EXE=<PRIVATE_IMPORTLIB> -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
cmake --build <WORK>/build --target devf_cp03_stage_hook_hp150 --parallel 2
dumpbin /headers <OWN_DLL>
dumpbin /imports <OWN_DLL>
dumpbin /exports <OWN_DLL>
cmake --build <WORK>/build --target devf_cp03_stage_hook_hp150_package --parallel 2
```

Producción compila dos unidades: src/mod.cpp y game_feature.cpp del SDK. /Zc:inline- retiene metadata y /GL- evita LTO. Laboratorio/tripwire no se enlazan en producción. Los 15 casos ejecutados en 38511192326 se reutilizan tras verificar hashes de CPP, headers, tests, CMake, SDK/lib y toolchain; no se repiten suites anteriores.

PE AMD64/ABI1, cinco exports y siete records: header ABI1, Host2.2, Log1.0, Game2.0, Stage1.0, Hook1.1 y Hook MEM72 para daE_OC_c::execute. PMF8 unido al thunk/import exacto `?execute@daE_OC_c@@QEAAHXZ`; binding, nombres y ajustes auditados. **28 imports exactos: 22 CRT/sistema y 6 del juego.** Sin TLS/delay, ActorService, detour manual, patch manual o gráficos. strcmp/strncmp son las comparaciones nuevas; la whitelist CP02 no se reutilizó ciegamente.

Paquete oficial:

- `DEVF_CP03_STAGE_HOOK_HP150_windows-amd64_b39e010d1a25168dee8de0c2c7740957d76dd853.dusk`
- **8953 bytes**, SHA256 `5754a47e84d56563cfb4143139aa0f4660b6852ce409e30b84fd398b0cfe3229`.
- DLL interna/loose: **16896 bytes**, SHA256 `b6eec19c59ad035253fbe2d5bbaf2414a41adfbc4da634cccf3adbcad4a66ef4`; igualdad exacta antes/después de empaquetar.
- Miembros exactos: mod.json, lib/, lib/windows-amd64/, lib/windows-amd64/mod.dll. CRC, rutas, duplicados, manifest e identidad: PASS.

[TEST 11870393231](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38513406897/artifacts/11870393231): ZIP de 9748 bytes, digest `5dbea28d35c7a7f6866d0467bdc9531cbecd243cd23e3e03043ef71ba36c4014`. [TEXT 11870208362](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38513406897/artifacts/11870208362): ZIP de 25345 bytes, digest `01507631908dfecb1ac6e765f0450a70d7806c66485ec43f935968df3f492308`.

Ambos se descargaron realmente. verify_download.py cotejó hashes externos, CRC y ledger, manifest externo igual al de CI, fuente incluyendo .hpp, PE, DLL interna y paquete. Resultado: [download-verification.json](evidence/download-verification.json). TEST caduca **12 noviembre 2026, 23:50:45 Panamá** (13 noviembre 04:50:45 UTC); TEXT dos segundos antes.

Artefactos privados: solo paquete propio/manifest y evidencia textual saneada. Sin EXE, lib, ROM, ARC o log personal. No se promete reproducibilidad universal byte a byte si cambia la imagen del runner. No se ejecutó juego, DLL de producción o backend del hook en CI.
