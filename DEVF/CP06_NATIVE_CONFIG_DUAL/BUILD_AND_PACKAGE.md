# Windows build y paquete privado

**Fuente realmente compilada:** a4b72680d7a6e0e360f52aef1b3a4554150c78a9.  
**Build CI:** af07099fbcffdfca1fae2c8280237c25c079b131. [Run 38761953150](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38761953150), job116515234717 SUCCESS. No usar el merge-event SHA como fuente.

MSVC AMD64, VCTools14.51.36231, Windows SDK10.0.26100.0. SDK oficial Dusklight40457c6… intacto. Targets devf_cp06_native_config_dual/native_config_lab y package oficial. Sin FEATURES game, host/Aurora/importlib build. Comandos, tiempos y resultados en evidence/build-result.json y logs propios sanitizados de CI.

| Elemento | Bytes | SHA256 |
| --- | ---: | --- |
| ZIP TEST descargable | 64772 | `fdc7b9e48f54e734e3272fc41b7eca75ca0227d5792e829357e2e929803ec92d` |
| .dusk | 28803 | `2658f7771344e9334219b1416bdbd9ca97cf817b28300c7d347da8e0454c48bb` |
| DLL interna | 54272 | `e1cb5eb685efd1fc4d1950ea0f7b6aa3d3a1fcb7484ccf9902b373821d3c552d` |


Archivo: `DEVF_CP06_NATIVE_CONFIG_DUAL_windows-amd64_a4b72680d7a6e0e360f52aef1b3a4554150c78a9.dusk`. Mod ID `dev.devf.cp06_native_config_dual`, versión0.6.2.
Artifact **DEVF_JSON_DUAL_NATIVE_TEST_38761953150**, id11986995345: [descarga privada](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38761953150/artifacts/11986995345). Si la URL profunda da Page Not Found, iniciar sesión con acceso y abrir la sección Artifacts del [run](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38761953150).
Caduca **2026-11-14 10:38:36 Panamá (15:38:36Z)**, leído por API; no promesa posterior.

El ZIP incluye exactamente UN .dusk, manifest/SHAs, SOURCE_COMPILED.zip, README/HUMAN_TEST y cinco JSON (cuatro modos + copia placements.json=BOTH) **fuera** del .dusk. No copia configuración automáticamente al PC. Sólo instalar .dusk y el ejemplo seleccionado con nombre placements.json en data_dir.

109 casos PASS sobre core y IO reales, dobles sólo de servicios; ocho negativos PE/ZIP PASS. ABI1, Host2.2/File1.0/Log1.0/Stage1.0, cinco exports, cero hooks/imports del juego/TLS/delay. CRT dentro del allowlist histórico; no ampliación de APIs. No carga ni ejecución de DLL/juego.

Primer run [38761708755](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38761708755) **FAILURE**: compilación y109casos pasaron; nuevo negativo FileService falló por escape NUL incorrecto del auditor Python. Se corrigió ese test en la copia nueva, sin tocar runtime ni auditor histórico. Segundo run PASS. Evidencia y fallo conservados; no se reetiquetan.

Descarga independiente **PASS**, CI **a9aabade816e8ea366b6f74a2cd731723a762ec1**, [run38762282880](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38762282880), job116516404815 SUCCESS. Otro runner descargó realmente los artifacts TEST y evidencia; comprobó SHA256/tamaños/CRC, manifest/.dusk/DLL/PE, los cinco ejemplos y SOURCE_COMPILED/ledger contra checkout. No build ni ejecución de DLL/juego. Resultado íntegro en evidence/independent-download.json. Los manifests congelados del build mantienen DOWNLOAD_PENDING incluso después de una verificación posterior: no reempaquetar para cambiar esa frase. HUMAN_RUNTIME_PENDING.
