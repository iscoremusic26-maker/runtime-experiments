# G2_PACKAGE_READY_FOR_USER_REVIEW

Paquete generado con el SDK oficial y **descargado de GitHub para verificarlo**. Esta decisión habilita únicamente revisión del artefacto; no acredita ejecución, G2 superado ni riesgo cero. No fue instalado o cargado, ni se ejecutó Dusklight.

## Descarga privada e identidad

[Run38302076854](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38302076854), [artefacto11771626280](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38302076854/artifacts/11771626280), repositorio privado del usuario. Nombre del artefacto:
`DEVF_CP01_G2_READ_ONLY_windows-amd64_b3ed281cbcb5934b7a8bd7d78b5adcef19b09ad2`.

Archivo `.dusk` dentro del ZIP de descarga:
`DEVF_CP01_G2_READ_ONLY_windows-amd64_b3ed281cbcb5934b7a8bd7d78b5adcef19b09ad2.dusk`.

**9,930bytes; SHA256**:
```text
a2baea22c9c28aa519d8bf339e9920f8609d14460ac7bc77c3dba9f94b1cf30c
```

Module ID `dev.devf.a1_readonly_preflight`, versión propia0.0.2. Fuente compilada `b3ed281cbcb5934b7a8bd7d78b5adcef19b09ad2` del repositorio DEVF. CI mirror `2e1cee42c7f3799a4671bee457ce442c6cc6026c`, [PR de CI#6 draft](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/6). El checkout usa ese head, no el merge sintético GITHUB_SHA `9d04b777b0541eb626707c2b1d63a957c47bfd8a`. Generado12oct2026 **20:07:59.283461 UTC**. Artefacto disponible hasta **26oct2026 20:08:01 UTC**, salvo borrado administrativo; fuentes/logs preservados en el checkpoint.

## Estructura SDK y loader

El target **devf_a1_observer_package** de `cmake/ModSDK.cmake` copió manifest y DLL al staging y utilizó `cmake -E tar --format=zip`. No se construyó manualmente un paquete supuesto. El loader original escanea `.dusk`, exige formato Mod y busca `lib/windows-amd64/mod.dll` (packages.cpp, bundle_zip.cpp, natives.cpp).

| Miembro real | Bytes | CRC32 | SHA256 |
|---|---:|---|---|
| mod.json |318|0f9d57c1|f8e6a556bd86187d7994690fad9881cfb61f1deeaae3b95b1b1fbe148cc914fd|
| lib/ |0|00000000|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855|
| lib/windows-amd64/ |0|00000000|e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855|
| lib/windows-amd64/mod.dll |18432|1834c627|1f7821cf05cacf7b0621fcdd782ef55f05e300b5a3be20e90394e7414c30ead9|

Exactamente dos archivos y dos entradas de directorio. Sin duplicados, symlinks, cifrado, traversal, rutas inesperadas u otras plataformas. Sin EXE/LIB del host, ARC/ROM/saves, otros mods, instaladores o DLL de terceros. El ZIP externo de Actions contiene únicamente el `.dusk` y DOWNLOAD_MANIFEST.json; ese manifest externo no forma parte del mod.

DLL compilado y DLL empaquetado: **idénticos byte por byte**, AMD64 PE32+, hash de la tabla. Metadata: headerABI1 y solo tres imports requeridos **Host2.2, Log1.0, Game2.0**; no hooks/exports de servicios. Exports exactos: mod_ctx, mod_meta, mod_initialize, mod_update, mod_shutdown.

Imports del ejecutable: mismos12 acreditados, diez funciones de consulta y mStayNo/mStatus públicos. Nombres completos en evidence/windows-pass/result.json y module-imports.log. Runtime exclusivo: dusklight.exe, VCRUNTIME140.dll, UCRTstdio/runtime y KERNEL32.dll. Las llamadas de inicialización CRT a IDs/tiempo/DisableThreadLibraryCalls no crean threads ni instalan hooks. Ningún import de spawn/delete/layer setter ni API de parches/escritura de archivos.

## Compilación y comprobaciones efectivas

MSVC19.51.36260.0, toolset14.51.36231, Windows SDK10.0.26100.0, CMake4.4.3, Ninja, Release AMD64. Official root40457c6, Aurora3227d76 solo headers, FEATURES game/epoch2 y lib exacta CP00 SHA256 `4dc4a511d761e6eb52541733fa31919a2234ed9cd5b2f16f8fea91c468f30ca4` (9,400,986bytes). No SDK alternativo/link stub, host build o descarga de recursos de enemigo.

| Comprobación | Resultado | Límite |
|---|---|---|
| Revisión previa y coincidencia de código/fuentes por hash | PASS_STATIC | Contratos y flujo original revisados; no prueba runtime |
| Compilación/link MSVC y12 imports reales | PASS_LAB | Compila lector real, no lo ejecuta en host |
| Laboratorio mod/core afectado | **47 PASS_LAB** |36 controles anteriores del observador más11 validaciones nuevas; backend nativo sustituido por fixture explícito |
| Guardas | PASS_LAB | READ_ONLY1 compila; READ_ONLY0/ENABLE_SPAWN/ENABLE_MUTATION fallan como esperado |
| Propietarios distintos/truncación/error/cleanup propio | PASS_LAB | Sin exigir igualdad; rechaza datos incompletos; lifecycle/logs acotados; sin callbacks/resources propios |
| Metadata/exports/imports del PE original y empaquetado | PASS_STATIC | Igualdad exacta de superficie; no PASS de lectura real |
| SDK package/CRC/SHA/layout | PASS_STATIC | Todos los miembros e identidad manifest/DLL verificados |
| Descarga efectiva privada | PASS_STATIC | Dos artefactos descargados; digests GitHub, CRC externos/interno, hashes de miembros y PE contrastados de nuevo |
| Juego/DX12/escenas/render/préstamos reales | NOT_VERIFIED / NOT_TESTED | Ningún arranque, instalación, hot reload o actor añadido |

Run exitoso al primer intento; intervalo propio18.384s, suma de comandos17.391s. Logs incluyen advertencias de headers originales ya conocidos, sin modificar el host. Comandos y tiempos exactos en result.json; el pipeline invoca build observer/lab, audit/guardas y luego **solo** package. No se repitieron las26 comprobaciones CP01 ni suites anteriores del host.

Digest del ZIP externo del paquete: `a0c1533e1a2b1808df3af5b93729fd1fb733f09250e74d34d4147700758b2182` (10,628bytes). Evidencia textual id11771686151: `e2c15672b693000bf29899b41268245ebc4de4868ae7850acb45956ff9eee317` (10,196bytes). No confundir estos hashes con el **hash del .dusk** anterior. [download-verification.json](evidence/download-verification.json) acredita la descarga,14archivos textuales, hashes LF propios y miembros. Solo textos están en Git; binarios únicamente en el artefacto privado y scratch de inspección.
