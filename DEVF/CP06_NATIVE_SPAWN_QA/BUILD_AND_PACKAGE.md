# Build, paquete y descarga verificados

Fuente compilada: **689f79c1c785bea31715d814f7d03818a7f0dd72**.

- CI de build: **08a5f4d952665bcc223b1b3feda37ac7ff23acdf**, [run 38755215665](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38755215665), job 116491729506: SUCCESS.
- CI de verificación independiente: **35221fa0593522ef3c17d7d89ea31afd4ebe2642**, [run 38755609469](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38755609469), job 116493090464: SUCCESS.
- Se registra el checkout real con `git rev-parse HEAD`; no se usa como fuente el merge temporal del evento.

MSVC AMD64 real: VCTools **14.51.36231**, Windows SDK **10.0.26100.0**. Los logs de CI conservan los comandos y las salidas del compilador; la evidencia JSON registra toolchain y tiempos. CMake/Ninja utiliza el SDK oficial 40457c6… intacto, sin FEATURES game ni compilación de host, Aurora o importlib.

Targets: `devf_native_qa_north`, `devf_native_qa_dual` y `native_registration_lab`. Pasaron 24 casos, comparación independiente de los registros completos con Python BE y seis negativos por DLL, además de PE/ABI/imports/exports y empaquetado oficial.

Ambas DLL miden 15360 bytes. Cada una importa tres servicios y exporta cinco símbolos, sin hooks, imports de funciones del juego, TLS ni delay imports. No se ejecutaron las DLL ni el juego. Los imports CRT son subconjunto estricto del allowlist revisado anteriormente.

| QA | Descarga privada | ZIP bytes | ZIP SHA256 | .dusk bytes | .dusk SHA256 |
| --- | --- | ---: | --- | ---: | --- |
| A | [Artifact 11983910861](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38755215665/artifacts/11983910861) | 35994 | `9f7e003b8963ecd1c60f0215000b5cf72f6c1b30a03fa7cd3b45d42bbd474a25` | 8159 | `d2b84ac8867181aa1c91edd62ea7acfd776d472c8282f39a466d70d00a11e1a3` |
| B | [Artifact 11983696053](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38755215665/artifacts/11983696053) | 36011 | `4a556c25894c090b36e78d70f9a6455d959fd03fc9fc7093979db83eaae8cf96` | 8171 | `b0cabb4a5be4f766f207f58aa2e5db24a9a873a95726d0dc9ba0d7e11d05bed5` |

- A: `DEVF_CP06_QA_A_NORTH_windows-amd64_689f79c1c785bea31715d814f7d03818a7f0dd72.dusk`; ID `dev.devf.cp06_qa_north_native`, versión 0.6.1. DLL SHA256: `2cfcf2d9f2380f95c9579484f1d67bfbdadbddd628abc637d0efd57f565e6d04`.
- B: `DEVF_CP06_QA_B_DUAL_windows-amd64_689f79c1c785bea31715d814f7d03818a7f0dd72.dusk`; ID `dev.devf.cp06_qa_dual_native`, versión 0.6.1. DLL SHA256: `73bba38ddbbf3c8c8e9a3b40a2044d518026a793a7ae346ce2504449eea62ddf`.
- Caducidad leída por API: A **2026-11-14 09:52:52 Panamá (14:52:52Z)**; B **09:52:53 Panamá (14:52:53Z)**. No se promete disponibilidad posterior.
- Artifact de evidencia textual 11983581035: 12240 bytes, SHA256 `446b8e09d9163e0dc827cc54284ea7c346b5e2f9b963626cd229dda3c5a0d3cf`; sólo salidas propias sanitizadas.

Cada ZIP contiene exactamente un .dusk, MANIFEST.json, SHA256SUMS.txt y SOURCE_COMPILED.zip. El .dusk contiene sólo mod.json, lib/windows-amd64/mod.dll y directorios del SDK. SourceZip contiene fuentes propias, lectores reutilizados y ledger; **no se instala**. No incluye SDK, EXE, .lib, ARC/BMD, texturas, ROM, logs del usuario ni credenciales.

Un segundo runner descargó efectivamente los tres artifacts. Envió autorización sólo a api.github.com y siguió la redirección sin token. Verificó tamaños y SHA256 de los ZIP, CRC en todas las capas, SourceZip/ledger/procedencia, .dusk, manifest, DLL interna y PE. No hizo otro build ni ejecutó DLL/juego. Véase [evidencia de descarga](evidence/independent-download.json).

Los manifests congelados conservan DOWNLOAD_PENDING, estado del momento de build. La verificación posterior está documentada por separado; no se reempaquetaron ni cambiaron hashes.

A: **NORTH_NATIVE_QA_BUILD_READY**. B: **DUAL_NATIVE_QA_BUILT / HUMAN_TEST_BLOCKED_UNTIL_NORTH_PASS**. Gameplay, terreno y limpieza runtime de estos QA siguen **NOT_TESTED**.
