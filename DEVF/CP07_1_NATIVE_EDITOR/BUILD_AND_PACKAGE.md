# CP07.1 — Build Windows, paquete y descarga real

Fuente realmente compilada: **c084729a36661cc6992843baca99f40b3c8211e2**.  
Build CI: **420ab15de326153e15e1947742fbe8085b13ea54**, [run38770105933](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38770105933), job116543365142 SUCCESS.  
Verificador CI: **8ceec3a417649701f2dcd0d23bfb0902fd85b3aa**, [run38770449006](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38770449006), job116544560702 SUCCESS.

MSVC AMD64 real, VCTools14.51.36231/WindowsSDK10.0.26100.0. CMake/Ninja, SDK oficial40457c6… intacto; sin FEATURES game, host/Aurora/Borealis/importlib build. Los comandos y tiempos están en logs CI sanitizados y evidence/build-result.json. Checkout real registrado, distinto del SHA de merge del evento.

Targets: devf_cp07_1_editor, native_config_lab, editor_lab, package oficial devf_cp07_1_editor_package.109casos de regresión del core real copiado y55casos editor/IO/UI PASS;11negativos PE/ZIP PASS.
ABI1;4servicios requeridos Host2.2/File1.0/Log1.0/Stage1.0;Ui2.3 **opcional**;5exports;0hooks/imports del juego/TLS/delay. Se revisó exclusivamente delta CRT strcmp/strlen/strncmp; no nuevos Kernel32 en resultado final. Allowlist histórico intacto.

Primer [run38769637138](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38769637138) FAILURE conservado: compiló y pasó164casos, auditor PE rechazó imports aún no revisados. Se retiró una inicialización estática local que incorporaba4funciones de sincronización innecesarias y se revisaron sólo3funciones de cadenas CRT. Segundo run PASS. No se oculta ni reetiqueta el fallo; no paquete entregado de esa ejecución.

| Elemento | Bytes | SHA256 |
| --- | ---: | --- |
| ZIP TEST | 87947 | `9033029e6c4fef90d29ff24d42943910072204b31285946f3e1dfda44f31dc14` |
| .dusk | 39591 | `c1070b6e4fa53f6cfa5e6f77640c30383351dc3dae10964f06edbb77e962cd46` |
| DLL interna | 77312 | `4e17e86d11b77589df93a2b91d2a3e21ed94620d9db39e44ed69e327833ae54f` |

ID **dev.devf.cp06_native_config_dual**, versión **0.7.0**. Archivo:
`DEVF_CP07_1_NATIVE_EDITOR_windows-amd64_c084729a36661cc6992843baca99f40b3c8211e2.dusk`.

Artifact **DEVF_CP07_1_EDITOR_TEST_38770105933**, id11990562891: [descarga privada](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38770105933/artifacts/11990562891). Si da Page Not Found, usar cuenta con acceso y abrir Artifacts del [run](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38770105933).
Caducidad leída por API: **2026-11-14 11:35:25 Panamá (16:35:25Z)**; no promesa después.

ZIP: exactamente un .dusk, MANIFEST.json, SHA256SUMS.txt, README/HUMAN_TEST,5JSON de referencia fuera del mod y SOURCE_COMPILED.zip. No se sobrescribe el JSON del usuario: conservar el suyo. No instalar DLL suelta ni SourceZip. Fuentes propias/lectores reutilizados/ledger, sin SDK, EXE, importlib, ARC/BMD/ROM/texturas/assets originales, logs de usuario ni secretos.

Otro runner descargó realmente TEST+evidencia por API, autorización sólo api.github.com y redirección sin token. Recalculó bytes/SHA256/CRC, .dusk/DLL/manifest/PE, ejemplos y SOURCE_COMPILED/ledger contra checkout. Sin rebuild ni ejecución de DLL/juego. Evidencia íntegra en evidence/independent-download.json.
El manifest congelado conserva DOWNLOAD_PENDING del momento de build; el resultado posterior lo completa documentalmente sin reempaquetar. JSON_read=COLD_START_ONLY describe la aplicación del core a actores; el editor sí realiza IO en inicialización y Guardar explícito para backup/verificación, nunca por frame.

**CP07_1_EDITOR_QA_BUILD_READY**, sólo QA humano controlado. Nuevo menú/guardado en juego/persistencia por reinicio real todavía HUMAN_RUNTIME_PENDING.
