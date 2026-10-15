# CP04.4 — Build, paquete y descarga reales

Fuente compilada `ee42f62d2bd2bbbfae9e61affb10c066fd0588af`; fuente de cierre documental y tag no deben confundirse con ese SHA.
CI build `565b16f44a9eb338e4d2018c27f2c1bad8caf4f9`, [run38657297492](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38657297492), job116169983378.
CI verificación independiente `1c5365384c561b9bba0e38508a16efc22a4d39ec`, [run38658291368](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38658291368), job116173195779.

MSVC cl19.51.36260 x64, VCTools14.51.36231, Windows SDK10.0.26100.0. Fuente oficial40457c6adb381928e4b5fef6ed459ed291edd5e2; Aurora headers3227d76c60e1e782ca576610bce61c9e7744d8be; importlib original9.400.986 bytes, SHA4dc4a511d761e6eb52541733fa31919a2234ed9cd5b2f16f8fea91c468f30ca4, CRC70c35731. EXE originalSHAffa992038d04290654b8907a7663f4dcf62083beaad2b35014fdfd901d390049 sólo leído, jamás ejecutado/modificado.

Comandos efectivos (versiones y segundos de cada fase en evidence/build-result.json):

```powershell
cmake -S DEVF/CP04_4_EOC2_BLACK_CONTINUATION -B work/build -G Ninja -DCMAKE_BUILD_TYPE=Release -DDUSK_SOURCE=.official -DDUSK_GAME_EXE=work/windows-amd64.lib -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
cmake --build work/build --target devf_cp04_eoc2_black cp044_black_lab --parallel 2
work/build/cp044_black_lab.exe
dumpbin /headers work/build/devf_cp04_eoc2_black.dll
dumpbin /imports work/build/devf_cp04_eoc2_black.dll
dumpbin /exports work/build/devf_cp04_eoc2_black.dll
cmake --build work/build --target devf_cp04_eoc2_black_package
```

El pipeline privado de inputs PR22 sigue el flujo CP03 de checkout/importlib/MSVC/SDK oficial, con IDs/target nuevos y sin repetir sus17 casos o recompilar su binario histórico. El build en sí tomó3.218 s, lab0.016 s, package0.219 s; no son tiempos de gameplay. /Bv y versión CMake están preservadas en evidence/download-verification.json y en artifact TEXT.

## Distribución comprobada

[Artifact TEST privado11936739368](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38657297492/artifacts/11936739368), ZIP45.231 bytes, SHA256 `e7b05803b687324c6f5eace8d3e2954b7e5b26d819f05e7de7d03bf5c2a8ca49`.
Vence 2026-11-13 18:59:41 (Panamá, UTC−05:00); UTC 2026-11-13T23:59:41Z. Está en repo privado; requiere acceso GitHub del usuario. No release público ni cambio de instalación.

| Miembro | Bytes | SHA256 |
| --- | ---: | --- |
| DEVF_CP04_4_EOC2_BLACK_windows-amd64_ee42f62d2bd2bbbfae9e61affb10c066fd0588af.dusk |15287|a1b1e750575253c8ec33193c385240337b8f1d5db6f3e9389fba08683c6d97f9|
| DLL interna lib/windows-amd64/mod.dll |28672|b61e47ed9cc1ee461469fab1f8fa7df38cca9045e17f14e12341657d9cb07f06|
| SOURCE_COMPILED.zip |30916|91d8c8032c8244056959f69dff6926228e5acae225444d691d3c09b8309e0285|

ZIP exterior incluye MANIFEST.json y SHA256SUMS.txt. SourceZip incluye fuentes propias realmente compiladas, ledger y3 headers CP03 reutilizados e inmutables; no ARC/BMD/ISO/JPC/EXE/importlib ni código SDK original redistribuido. Dusk incluye sólo mod.json y su DLL, con directorios oficiales lib/windows-amd64.

Artifact TEXT11936959012:8867 bytes/SHA9b1873b1207e9872aa4d0bdb7ec8031694f054dd7e2f266fc71033905416cb7f. Ambos artifacts se descargaron físicamente en **otro** runner Windows. Se contrastaron digest/tamaños de GitHub, CRC de todas las capas, SourceZip+ledger, manifiesto, checksum, dusk y DLL interna, y se volvió a analizar esa DLL. El token sólo se envía a api.github.com; redirect firmado sin Authorization. No se publican URL firmadas ni credenciales.

CMakePresets del host no se modificaron; no host build nuevo, SDK Linux, Vulkan o simulación como prueba Windows. La plataforma objetivo es el EXE oficial Windows/D3D12; CI no usó GPU ni ejecutó callbacks nativos de la DLL.
