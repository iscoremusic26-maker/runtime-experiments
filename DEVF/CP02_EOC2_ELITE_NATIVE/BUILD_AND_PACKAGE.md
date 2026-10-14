# Paquete CP02 — PASS offline y descarga

Fuente compilada `13959231169aedc111c1c5b5cac747bd62e252fd`; CI `d3a85769f096e2d6eb065ddf2d69847ab0b6b8e1`; [run38501242719](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38501242719), job115648464135. SDK40457c6adb381928e4b5fef6ed459ed291edd5e2/Aurora3227d76c60e1e782ca576610bce61c9e7744d8be exactos; importlib9400986bytes/SHA4dc4a511d761e6eb52541733fa31919a2234ed9cd5b2f16f8fea91c468f30ca4/CRC70c35731, solo leída/extraída de ZIP LFS íntegro. No SDK/Aurora/game source/host patch ni compilación host.

Pipeline mínimo derivado de CP01: CMake Ninja Release, SDKadd_mod(FEATURES game), target devf_cp02_eoc_elite_native/package, DUSK_SOURCE fijado y DUSK_GAME_EXE=.lib verificada. /Zc:inline- retiene metadata MSVC, /GL-; no LTO o limpieza artificial de imports/bytes. Grafo DLL dos unidades: mod.cpp + SDKgame_feature.cpp. Lab separado con abort-only GX, no en DLL.

PE AMD64/ABI1, metadata exactamente Host2.2/Log1/Stage1/Game2, cinco exports mod_ctx/mod_meta/mod_initialize/mod_update/mod_shutdown, sin aliases/forwarders/ordinal-only.20 CRT/system idénticos a CP01 por DLL/símbolo, ningún native game/GX import/TLS/delay/hook/ActorService. La mutación permitida es StageService.add_actor indirecto; no se etiqueta readonly. Auditor estructural/export/ZIP heredado intacto, contrato de identidad CP02 propio.

| Objeto | Bytes | SHA256 |
|---|---:|---|
|`.dusk` CP02|7410|`c3166dcafec29d5963a77bd8bbb1a0cc2197650f4a0c30d310b459be9afa0901`|
|DLL suelta/interna|13824|`c8562d0258bd936d1affd2ec1ea8e7efd89c11302644c66fe65bf2988ad07366`|
|mod.json|397|`ec877d82d2ae38be7b49c34efb79a65f54dae1ad315a14ab0a8c3dca981c1c4d`|
|Actions ZIP delivery|8162|`e96b1a5f26745cfad2b023616e8af7f24afb64434921611f3060631edf34a25a`|
|Actions ZIP texto|21005|`1c711db7c27146af5a8657cdc10801600d8a3cefd2f0f9f1fae952179175fd8d`|

Filename `DEVF_CP02_EOC2_ELITE_NATIVE_windows-amd64_13959231169aedc111c1c5b5cac747bd62e252fd.dusk`; IDdev.devf.cp02_eoc_elite_native/v0.2.0. Es un build nuevo con nuevo payload/identidad: tamaño/hash distintos del CP017364bytes/SHA4bbf0a8a…, no DLL vieja renombrada. Interno exacto mod.json + lib/ + lib/windows-amd64/ + mod.dll; DLL bytes==suelta del mismo run y no reconstruida/normalizada por packaging. Todos los CRC/tamaños/SHA y rutas/case aliases/symlinks/cifrado/extras inspeccionados; sin recursos propios o globales.

[Delivery privado11866086914](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38501242719/artifacts/11866086914), [texto11866420418](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38501242719/artifacts/11866420418). Se descargaron realmente ambos y se contrastaron digest GitHub/miembros/ledger. ci/verify_download.py repitió manifest externo contra evidencia del mismo run, filename/source/CI/run, código por LF hashes, internal DLL contra suelta, PE/imports/metadata/exports, CRC/SHA y contenido. evidence/download-verification.json: DOWNLOAD_VERIFIED. Vence **2026-11-12 21:30:04 Panamá** (2026-11-13 02:30:04UTC), texto un segundo antes; luego no se garantiza descarga.

Artefacto delivery solo .dusk + DOWNLOAD_MANIFEST.json externo, textos separados. Ningún EXE/ROM/.lib/ARC/save/credencial/log personal/standalone DLL subido o comiteado. Paquete únicamente privado. CP02 runtime NOT_TESTED, CP03 no autorizado; usuario debe aprobar antes de instalar y retirar CP01 primero. Sin daño2×, HP runtime o aspecto exclusivo declarados.
