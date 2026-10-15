# Compilacion y paquete privado CP07.2A
- Fuente REAL: **e066a5e7505a266658783259b70cb320321747f2**.
- Build CI **2f02e07e7916ef0c947042dbbc9e4d79b12153f3**, [run38794698410](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38794698410), job116627894322 SUCCESS.
- Verificador CI **c7f9dfbd1ffedc15db06b4dfd084c0f9c476b1e1**, [run38795046018](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38795046018), job116629108114 SUCCESS. Otro Windows runner, DESCARGA REAL sin compilar ni ejecutar DLL/juego.
- MSVC AMD64 VCTools14.51.36231, WindowsSDK10.0.26100.0;276casos+14negativos PASS. Cinco exports mod_* solamente;12imports game leidas, GameService2.0 requerido, API1.0 deferred intacta, Ui2.3 opcional. Sin hooks/TLS/delay imports ni CRT nuevo. No loader/juego ejecutado.

SDK40457c6 yAurora3227d76c(headers) checkout exactos. Biblioteca oficial SDK extraida sin modificar desde ZIP privado aprobado CP00;9400986bytes SHA2564dc4a511d761e6eb52541733fa31919a2234ed9cd5b2f16f8fea91c468f30ca4. No version-independent HEAD stub, no EXE/host/renderer reconstruido. Solo target .dusk/CLI/tests y glue oficial game_feature.cpp dentro del modulo. Git status oficial limpio. Biblioteca/ZIP/SDK/assets originales excluidos de artifacts.

| Archivo | Bytes | SHA256 |
| --- | ---: | --- |
| ZIP QA |244329|`eb7696af4353ab9d2ad1cbc3f548ff482e67564eab7da47c90497892662bc93f`|
| .dusk |127380|`9e63d0e66f6e0cc6f4695ec665eca7bbddfca3d428ee44294c2fa246cc4c60ce`|
| DLL interna |288768|`00ff69ceefea75fea33f9c9bc840c27703a50851d0a435a6d63ffb632773d808`|
| CLI propio Windows |67584|`86c41d26eceae523fb74d593f8956e26625f6dd4d300bb6c4b3078db3e63b2c1`|
| SOURCE_COMPILED.zip |82183|`71bcbef65f403f005a32ff51604d8e7b682b411419555eec43cf935af00e1a2f`|

**dev.devf.cp06_native_config_dual v0.7.2**, archivo `DEVF_CP07_2A_ENCOUNTER_EDITOR_windows-amd64_e066a5e7505a266658783259b70cb320321747f2.dusk`.
[Artifact privado DEVF_CP072A_EDITOR_TEST_38794698410 /12000983275](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38794698410/artifacts/12000983275).
Caduca **2026-11-14 14:33:40 Panama (19:33:40Z)**, metadata leida por API. Si enlace profundo404, usar cuenta autorizada y Artifacts del run38794698410. No disponibilidad prometida tras caducar.

ZIP contiene un .dusk, README/HUMAN_TEST, manifest/SHA, ejemplosCP06 fuera del mod, ejemplo export VACIO, CLI propio y fuentes exactas. El .dusk contiene solo mod.json y DLL propia AMD64. CLI es herramienta propia que solo lee/valida JSON, NO Dusklight.exe; no instalarlo como mod ni instalar DLL suelta. Hashes de todos miembros y CRC en evidence/independent-download.json.
El manifest y README congelados conservan BUILD/DOWNLOAD_PENDING del instante de empaquetar; este cierre posterior completa el gate sin reempaquetar.
El probe0.1.0 anterior se DESCARGO y audito, no se recompilo/republico; header C ABI y probe.hpp coinciden con fuente previa. No incluir probe para QA de captura. API gameplay anterior solo consta como HUMAN_REPORTED del usuario, no nuevo gameplay CI.

Reproduccion: checkout SDK yAurora en hashes indicados, proporcionar biblioteca original verificada mediante DUSK_GAME_EXE; ejecutar ci/run_windows.py bajo MSVCx64 con SOURCE_CI.json de fuente exacta. Workflow NUEVO devf-cp07-2a-encounter-editor.yml: fase build en 2f02e07e7916ef0c947042dbbc9e4d79b12153f3, HEAD verificador download-only en c7f9dfbd1ffedc15db06b4dfd084c0f9c476b1e1. Sin modificar workflows anteriores. Evidencia fuente/CI separa checkout real de merge-event SHA.
