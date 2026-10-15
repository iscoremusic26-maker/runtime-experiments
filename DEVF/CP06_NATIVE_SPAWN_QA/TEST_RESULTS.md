# Resultados A/B

| Gate | A: norte | B: sitio 1 + norte |
| --- | --- | --- |
| Core real de registro y cleanup | PASS OFFLINE: 24 casos | PASS OFFLINE: rama dual ejercitada |
| Registro completo BE, 0x20 bytes | PASS: comparación Python struct.pack | PASS: dos registros, posiciones distintas |
| Errores/API/handle cero/duplicado/excepciones | PASS OFFLINE | PASS: fallo del segundo revierte handles propios |
| Cleanup inverso, idempotencia y reintento | PASS OFFLINE | PASS; no implica destruir actores vivos |
| Sin reinyección | PASS CORE; update vacío | PASS CORE; update vacío |
| Windows MSVC AMD64 | BUILD_PASS | BUILD_PASS |
| PE/ABI, tres servicios y cinco exports | PASS; cero hooks/imports del juego/TLS | PASS; misma superficie |
| Negativos PE/ZIP | PASS: seis | PASS: seis |
| SDK package | PACKAGE_VERIFIED | PACKAGE_VERIFIED |
| Descarga real independiente | DOWNLOAD_VERIFIED | DOWNLOAD_VERIFIED |
| Estado técnico | NORTH_NATIVE_QA_BUILD_READY | DUAL_NATIVE_QA_BUILT |
| Gameplay nuevo | HUMAN_RUNTIME_NOT_TESTED | HUMAN_TEST_BLOCKED_UNTIL_NORTH_PASS |

Los 24 casos cubren A con una entrada norte, B con dos entradas distintas, bytes del registro, no reinyección A/B, fallo y excepción en primera/segunda alta, handles cero, handles duplicados, error con handle, excepción después de devolver handle, fallo de remoción y reintento propio, excepción al remover, cleanup idempotente/sin init, contexto/servicio nulos, servicio pequeño/major incorrecto y funciones add/remove nulas.

El laboratorio utiliza **registration.hpp real**, compartido por ambas DLL; sólo la API StageService es un doble de prueba que copia records y devuelve handles. No simula ActorId, GPU ni motor. Los seis negativos por DLL son x86, StageService ajeno, export faltante, major de StageService incorrecto, ARC extra y traversal ZIP. No se ejecutaron binarios mutados.

[Build 38755215665](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38755215665), job 116491729506: SUCCESS. Fuente **689f79c1c785bea31715d814f7d03818a7f0dd72**; CI **08a5f4d952665bcc223b1b3feda37ac7ff23acdf**.

[Verificación 38755609469](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38755609469), job 116493090464: SUCCESS. CI **35221fa0593522ef3c17d7d89ea31afd4ebe2642**. Descargó los tres ZIP y verificó bytes/SHA/CRC, SourceZip, ledger, manifest, .dusk, DLL y PE, sin recompilar ni ejecutar DLL/juego. Los logs de CI se leyeron mediante el conector; sólo evidencia derivada está publicada. No hubo fallos de build en esta iteración.

El control incremental del norte revisó rutas, 27 puntos discretos, registros de actores y entradas; reutilizó KCL/PLC y bounds previos. No encontró un impedimento estático concreto para QA A. **No equivale a SITE2_ACREDITADO.**

Aparición, asentamiento, visibilidad, colliders, eventos, recursos efectivos, simultaneidad, combate/muerte/reentrada/rollback de los nuevos QA, FPS y terceros: **NOT_TESTED en juego**. Estos resultados no heredan ni invalidan los cinco PASS humanos del CP06 anterior.

B tiene dos altas probadas offline, no dos enemigos observados. La personalización sigue PENDIENTE y CP06 general sigue parcial. Fuente/binarios/refs históricos permanecen intactos; la comparación por árboles queda registrada en PR41.
