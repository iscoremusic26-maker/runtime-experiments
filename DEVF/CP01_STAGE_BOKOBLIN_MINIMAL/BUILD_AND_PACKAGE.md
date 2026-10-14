# Build y paquete verificado

Source `a17109b91ba5fde7a221ac72a4b5640570b8a4d2`; CI `09b6464343a2db0d64a643ab06714ef9f042b061`; run38496922708/job115634702685, [artifact privado](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38496922708/artifacts/11864626006). SDK40457c6adb381928e4b5fef6ed459ed291edd5e2/Aurora3227d76c60e1e782ca576610bce61c9e7744d8be exactos. Importlib9400986bytes/SHA4dc4a511d761e6eb52541733fa31919a2234ed9cd5b2f16f8fea91c468f30ca4/CRC70c35731, extraído del ZIP LFS original sin alterarlo, no distribuido. Windows MSVC19.51.36260/SDK10.0.26100.0. Sin build host, simulación Linux o SDK parcheado.

CMake Ninja Release, DUSK_SOURCE exacto, DUSK_GAME_EXE apuntando a `.lib` verificada, export compile_commands. Targets oficiales: devf_stage_bokoblin_minimal y devf_stage_bokoblin_minimal_package. /Zc:inline- en producción es necesario para conservar los registros oficiales MOD_META_RECORD MSVC, /GL-; Game ABI defs originales. Solo dos unidades: propio mod.cpp y SDK game_feature.cpp. Test y tripwire fuera del grafo DLL.

Se reutiliza el parser estructural G2 y herramientas PE/exports/ZIP G5 sin editarlos. Adaptación propia limita metadata exactamente a Host2.2/Log1.0/Stage1.0/Game2.0, cinco registros incluido header ABI1; ningún servicio opcional/hook/export/service Actor. MáquinaAMD64 y cinco exports mod_ctx/mod_meta/mod_initialize/mod_update/mod_shutdown, no forwarders o ordinal-only. Native imports del juego exigidos **vacíos**. 20 CRT/system por identidad completa en reviewed-exact-imports.json; funciones de bootstrap/formatting/copy propios. Ningún GX call/import residual del header, ActorService, NativeBackend o setters. Stage.add_actor indirecto ES la mutación permitida.

Paquete ID **dev.devf.cp01_stage_bokoblin_minimal v0.1.0**, filename `DEVF_CP01_STAGE_BOKOBLIN_MINIMAL_windows-amd64_a17109b91ba5fde7a221ac72a4b5640570b8a4d2.dusk`:

| Objeto | Bytes | SHA256 |
|---|---:|---|
|.dusk|7364|`4bbf0a8ae5fb436c32a4bb804f52c431bf6e6e1d7b4e95a5534d02505ab9ecf7`|
|DLL suelta e interna|13824|`24b74c4e33bd7745c8937999958ac112a258e136ae78fa49571ae6fa53af1f65`|
|mod.json|364|`68310dba18719f5dacc23e333303df77865e8bcd7f2d28b60f44060ce3c65a82`|
|Actions ZIP delivery|8065|`95a8048b3ac626e4a4d4518c8ad0bec6acfc624ce2c8d2fc340c69b0ad26f804`|
|Actions ZIP texto|17460|`64d5b832bb41cfe373b4b9146f614ebd4fcc2c83af0c3d1b19ba36c51fca9106`|

.dusk solo mod.json + lib/ + lib/windows-amd64/ + mod.dll. Miembros únicos, sin case alias/traversal/symlink/cifrado/extra; tamaños acotados y CRC/SHA de todos los miembros PASS. DLL interna byte-idéntica a suelta auditada del mismo run; empaquetar no la reconstruyó ni normalizó timestamps. Delivery externo solo .dusk + DOWNLOAD_MANIFEST.json; no EXE, ROM, .lib, ARC, logs personales, saves o DLL suelta. Nada de esto se comitea en Git salvo evidencia textual/fuentes propias.

Ambos artefactos descargados realmente: delivery11864626006 y texto11863841559; digest GitHub comprobados y miembros de texto ligados a SHA ledger. ci/verify_download.py repitió CRC/tamaños/hash/PE/services/exports, comparó external manifest byte a byte con el del run y source ledger con fuentes publicadas. evidence/download-verification.json: PASS. Vence delivery2026-11-13 01:40:58UTC /2026-11-12 20:40:58Panamá; texto un segundo antes. Acceso privado/autenticado necesario y no descarga garantizada tras vencimiento.

**Usable para revisión/prueba controlada tras aprobación; no probado dentro del juego.** MOD_OK solo edit registrado. Ver HUMAN_TEST. CP02 NO_GO, sin merge ni instalación.
