# Build y descarga verificados del par API

Fuente REALMENTE compilada: **ae4fa410e4543c032fccfe761b2a817ae17479b2**.  
Build CI **d9100a41afe06ed4f23b8d638baba8102e566066**: [run38787691561](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38787691561), job116603837674 SUCCESS.  
Verificación CI **049e028b6f73dae0011966835bd6136322e81d3e**: [run38788164065](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38788164065), job116605471372 SUCCESS.

MSVC AMD64 real; VCTools14.51.36231/WindowsSDK10.0.26100.0. SDK40457c6… intacto, sin host/SDK/Aurora/Borealis/importlib recompilados; add_mod/package oficiales sin FEATURES game. C11 valida header C y C++20 compila ambos consumidores/proveedor. Checkout real registrado; merge-event SHA sólo contexto, no fuente.

Core109+editor55+API50=**214PASS**.13negativos proveedor y9probe=**22PASS**. Los dos PE AMD64 exportan sólo los5símbolos del módulo, sin hooks, imports del juego, TLS o delay imports.
Proveedor: Host2.2/File1.0/Log1.0/Stage1.0 requeridos, Ui2.3 opcional y EXPORT_DEFERRED dev.devf.native_placement1.0.
Probe: Host2.2/Log1.0/dev.devf.native_placement1.0 requeridos; **sin StageService**. Los imports de cadenas CRT permanecen dentro del delta exacto ya revisadoCP07; no se amplió para este par. Primer build PASS; ningún fallo nuevo ocultado.

| Archivo | Bytes | SHA256 |
| --- | ---: | --- |
| provider ZIP | 102621 | `8c1ef26d5bba5da658adc4187c720aa63a11b2c3794ce58e92db6fa09df5aa47` |
| provider .dusk | 42860 | `3014cd62b87e5ccbe7703c7515daf2dda521f8ac999a56275fc2852770adf422` |
| provider DLL | 84480 | `c77671644c367c80d819444a00089194e60837d22157018286360674c185afd7` |
| probe ZIP | 64934 | `b4f92bae7d7129e8110da73d101185eac8d8a6f534f8142c234c814a9d91b599` |
| probe .dusk | 7439 | `6556ffe9253f7c0a0e4c678e8293f85a6c4430295895dabf18e518fcc6e25a15` |
| probe DLL | 14336 | `b407aec64a4d4d79ae4ea54b94a91e0d8b3f904da724e82402b7787812e1c4ec` |

Proveedor **dev.devf.cp06_native_config_dual0.7.1**, archivo `DEVF_NATIVE_API_PROVIDER_windows-amd64_ae4fa410e4543c032fccfe761b2a817ae17479b2.dusk`.
Probe **dev.devf.native_api_probe0.1.0**, archivo `DEVF_NATIVE_API_PROBE_windows-amd64_ae4fa410e4543c032fccfe761b2a817ae17479b2.dusk`. No Bokoblin Expansion.

- [Proveedor DEVF_API_PROVIDER_TEST_38787691561 /11998662928](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38787691561/artifacts/11998662928), caduca **2026-11-14 13:43:54 Panamá (18:43:54Z)**.
- [Probe DEVF_API_PROBE_TEST_38787691561 /11997374800](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38787691561/artifacts/11997374800), caduca **13:43:55 Panamá (18:43:55Z)**.
Caducidad y disponibilidad leídas por API. Si URL profunda da404, usar cuenta autorizada y abrir Artifacts del [run](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38787691561). No promesa tras vencimiento.

Cada ZIP contiene UN .dusk, manifest/SHA, README/HUMAN_TEST y SOURCE_COMPILED.zip. Proveedor incluye ejemplos JSON fuera del .dusk; probe no escribe JSON. SourceZip contiene código propio y lectores reutilizados, no SDK/EXE/importlib/ARC/ROM/assets/rawlogs del usuario/secretos. Se distribuyen dos paquetes separados, nunca una DLL extranjera suelta.

Otro runner descargó realmente los3artifacts (proveedor/probe/evidencia). Autorización sólo api.github.com y redirect sin token. Recalculó SHA/tamaños/CRC en todas las capas; verificó .dusk/DLL/manifest/PE, ejemplos, SourceZip/ledger y correspondencia con checkout. No recompiló ni ejecutó DLL/juego. Resultados completos en evidence/.
Los manifests congelados conservan DOWNLOAD_PENDING de la fase build; la evidencia posterior completa el gate sin reempaquetar.

**DEVF_NATIVE_API_PAIR_QA_READY / HUMAN_PENDING**. No ejecución de loader real/juego en CI; dependencia/load-order son contrato fuente exacta + metadata y modelo de servicios, no gameplay.
