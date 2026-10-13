# Auditoría de binario, paquete y descarga

**Resultado: PASS_STATIC / DIAGNOSTIC_PACKAGE_PASS / DOWNLOAD_VERIFIED. Solo REVIEW_ONLY; ejecución no autorizada.**

Fuente `29efb505a71014f9f8725846576485cdb91f77cd` en PR19; CI `f02cbd99bc280d6bbd54ab0f08b4ba241b7f0fe4` en PR13; [run38466822325](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38466822325), job115535637388. SDK oficial40457c6adb381928e4b5fef6ed459ed291edd5e2 y Aurora3227d76c60e1e782ca576610bce61c9e7744d8be, verificados sin modificación. Importlib privado9400986bytes/SHA4dc4a511d761e6eb52541733fa31919a2234ed9cd5b2f16f8fea91c468f30ca4, CRC70c35731, nunca distribuido.

Grafo: seis unidades nativas (diagnostic_mod/policy/trace/temporal/frame_validation/game_feature) y ocho bridge readonly. Mapa sin NativeBackend, Controller.attempt/poll, LayerScope, setter de layer, request visitor, Actor/Stage/HookService o Fake. El laboratorio con core real/backendFake es target separado excluido del módulo. Request slot32 está AUSENTE intencionalmente, no validado como llamada activa. La producción no registra perfiles ni actores.

AMD64 PE32+, ABI1, metadata exactamente Host2.2/Log1.0/Game2.0. Exports exactos: `mod_ctx`, `mod_meta`, `mod_initialize`, `mod_update`, `mod_shutdown`; cinco nombres/ordinals distintos, sin forward/extra. Completa whitelist propia: 30 imports de juego idénticos a G4B y 24 CRT/system. Única adición memcmp, con buffers/longitud/caller/constante verificados; diff íntegro versionado. No TLS/delay imports. Auditoría histórica intacta.

Target oficial `devf_g5_rejection_diagnostic_package` del SDK. `.dusk` contiene exactamente mod.json, lib/, lib/windows-amd64/ y lib/windows-amd64/mod.dll. CRC de todos los miembros PASS, duplicados/case aliases/rutas inseguras/cifrados/symlinks/especiales/extras rechazados, tamaños acotados y manifiesto byte-idéntico al propio. DLL interna == DLL suelta del mismo run antes/después de empaquetar. No normalización o reescritura del binario.

| Objeto | Bytes | SHA256 |
|---|---:|---|
| .dusk diagnóstico | 31819 | `095f11583e7c4e97f2f0be4455e827fc42f609eac03fd887bc142f707237a436` |
| DLL interna y suelta | 163328 | `d2a5f3bcfeb2870be56968de59321b21ba5388c8d95b5d8e1f4e54d99f14711d` |
| mod.json | 336 | `41985bbc85e02fa4b3ff78ed36ab7d1afbd22c8f5a8a35a235cb9817fd8e803c` |
| ZIP externo Actions delivery | 31866 | `755eca152bffed1bf1e39ef19dd653285e73092ab386524c31d1c07afca84189` |
| ZIP externo Actions texto | 136753 | `3b5fd364f31d9f8c636e2bb439cb1d91a44f18a13628590f74f869627189566d` |

Identidad `dev.devf.cp01_g5_rejection_diagnostic`, v0.0.2, READ_ONLY_DIAGNOSTIC. [Download privado](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38466822325/artifacts/11847829866), artifact11847829866; [texto](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38466822325/artifacts/11848254740), artifact11848254740. Delivery vence2026-11-12 20:57:57UTC/15:57:57Panamá; texto un segundo antes. Git conserva informes y fuentes, no DLL/.dusk ni originales. El ZIP delivery trae solo .dusk + DOWNLOAD_MANIFEST.json externo; no importlib, originales, log personal, saves ni credenciales.

Se descargaron realmente ambos ZIP, contrastando los digest de GitHub. `ci/verify_download.py` inspeccionó outer ZIP, manifiesto externo, nombre ligado al source SHA/run, ledgers SHA del texto, source ledger publicado, `.dusk` interno, CRC/tamaños/SHA, bytes del manifiesto, imports/ABI/servicios/exports. La DLL extraída coincide con el hash de la suelta registrada por el build. `evidence/download-verification.json` guarda el resultado independiente. El manifiesto externo coincide byte a byte con el conservado en el texto del mismo build. Siete negativos incrementales offline rechazaron manifiesto externo/procedencia/digest alterados, ID interno/DLL alterados y dos inconsistencias de directorio/archivo; evidencia download-negative-results.json. No `LoadLibrary`, no ejecución del juego ni DLL en ningún paso.

PASS de compile/link/inspección no prueba render, colisión, aparición, limpieza runtime, reposo físico o seguridad de ubicación/DLL unloading. G6 NOT_VERIFIED, CP02 NO_GO, siguiente G5 no autorizado.
