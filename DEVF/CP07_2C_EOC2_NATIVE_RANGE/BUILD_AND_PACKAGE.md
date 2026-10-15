# Build y descarga — CP07.2C
Estado **al build**: CP07_2C_NATIVE_RANGE_5000_PRIVATE_TEST_READY / HUMAN_RUNTIME_PENDING. Cierre humano posterior: véase [acta del 15-10-2026](HUMAN_RUNTIME_RESULTS_2026-10-15.md), PASS acotado; no se reconstruye ni reempaqueta nada.

- Fuente realmente compilada: 02e9070497bfe0ec2fda83ea63fd2ca237fb6dfd, padre literal 7c588d2a06d307b0288256fc2383186129430401; [PR47](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/47).
- CI build: 1c1a96cffbdf80199570423addec4c91ded46865, [run 38812099184](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38812099184) SUCCESS.
- CI verificador final: 162e988157af120ee8f87fdc82dba6e90c33bb55, [run 38812605127](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38812605127) SUCCESS; runner Windows distinto, descarga real sin build ni ejecución de DLL/juego.
- MSVC 14.51.36231, Windows SDK 10.0.26100.0, AMD64; SDK Dusklight 40457c6adb381928e4b5fef6ed459ed291edd5e2 y cabeceras Aurora 3227d76c60e1e782ca576610bce61c9e7744d8be intactos.
- Biblioteca oficial original seleccionada por tamaño/SHA del archivo privado aprobado; no generada ni modificada. Host/juego no compilados.
- 354 casos = 109 core +55 editor +50 API +62 encuentros +70 expansión +8 rango; 18 negativos PE/ZIP rechazados. Generador y validación de entrada también ejecutados.
- [PR33 CI](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/33) draft/sin merge; sólo workflow nuevo segregado.

## Descarga privada
[Artifact 12009156482: DEVF_CP072C_PROVIDER_TEST_38812099184](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38812099184/artifacts/12009156482). Si el enlace profundo falla, abrir [el run](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38812099184) con la cuenta autorizada y usar Artifacts.
Caducidad devuelta por API: 2026-11-14T21:45:50Z, **14-11-2026 16:45:50 America/Panama (UTC−05:00)**. No se garantiza disponibilidad después.

| Elemento | Bytes | SHA256 |
|---|---:|---|
| ZIP descargado de Actions | 280547 | 89258783b1d776d762f6b62c71d8bb1cefdd9086f8c3771ddec09ab137278464 |
| DEVF_CP07_2C_PROVIDER_windows-amd64_02e9070497bfe0ec2fda83ea63fd2ca237fb6dfd.dusk | 129925 | 934a0a1a5127fa994b9325a5f94a493d0df53f3b5f9af9acfce3709006379fbb |
| DLL interna | 293888 | 0417629cd97eeaa4259f6f23ed23374602e37fc21e15c26e04da9c94854b0005 |
| SOURCE_COMPILED.zip | 121296 | 958eecba98075ccf6027a6e775ca96941b0d612a795efca5ddd6732c69dff79e |

ZIP incluye un único .dusk nuevo del proveedor, manifest, checksums, ejemplos, README/HUMAN_TEST, validador propio y fuente compilada con ledger de 70 archivos. Documentación completa en esta carpeta del repo y dentro del SourceZip. No contiene nuevo consumidor, host, SDK/binarios oficiales, ROM/ARC ni logs privados.

## Verificador: fallo conservado y corrección
[Intento inicial 38812467385](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38812467385) FAIL: comparó el orden físico de las entradas modmeta del binario previo y nuevo. HostService estaba en otra posición; IAT, exports y contenido de cada entrada coincidían.
Se corrigió únicamente el verificador para comparar todas las entradas canonicalizadas, preservando multiplicidad y todos sus campos; además continúa exigiendo imports/IAT y exports exactos, versiones, flags, tamaños y deferred exports en orden. La fuente oficial registry.cpp L304/L367 consume parsed.exports/parsed.imports por descriptor; el orden físico mixto no identifica ABI distinta.
No se reconstruyó ni reempaquetó el proveedor para esta corrección. El run final SUCCESS conserva toda la trazabilidad.

## Compatibilidad binaria histórica descargada
Consumidor original 0.1.0, artifact 12004087737, .dusk 24439 bytes SHA256 104a6c0908f498b0a833b7ed31d12e75f224bc2f232633bd921446c217d2333f; DLL 45056 bytes SHA256 015fad7772af2208c53892d193d732de819a897b3f654876c1ccbca1a00ec50b.
Se descargaron sus ZIP/DLL/fuentes y el probe original; no se recompilaron, reempaquetaron, publicaron de nuevo ni ejecutaron. Ambas cabeceras ABI y fuentes de cliente se conservaron. El provider anterior también se descargó para comparar imports/IAT, exports y metadata de servicios.
Los manifests/mensajes internos que dicen DOWNLOAD_PENDING o HUMAN_PENDING describen su fase de generación; la descarga posterior se certifica aquí, sin reescribir el paquete.
