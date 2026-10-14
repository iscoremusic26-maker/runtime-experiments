# Recuperación del piloto offline

Fuente: `feature/devf-cp03-stage-hook-hp150`, [PR24](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/24) draft contra CP02. CI: `ci/devf-cp03-stage-hook-hp150`, [PR16](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/16) draft contra CI CP02. Sin merge ni force-push. Tag nuevo **DEVF_CP03_STAGE_HOOK_HP150_OFFLINE_TEST**, sin declarar PASS runtime.

Fuente compilada `b39e010d1a25168dee8de0c2c7740957d76dd853`; CI `4f84a7137011a35f0500dc7ae1104420e58fbb30`; run 38513406897. HEAD documental/tag final añade informes y evidencia sin cambiar CPP/headers/tooling del source ledger. CI_SOURCE.json identifica el origen compilado.

```bash
git clone --bare https://github.com/iscoremusic26-maker/Mods-Duskligh.git devf-cp03-recovery.git
git -C devf-cp03-recovery.git rev-parse DEVF_CP03_STAGE_HOOK_HP150_OFFLINE_TEST^{commit} refs/heads/feature/devf-cp03-stage-hook-hp150
git -C devf-cp03-recovery.git fsck --full
git -C devf-cp03-recovery.git diff --name-only 0d2430262181bb2844f13bb8da0a628f71740998 DEVF_CP03_STAGE_HOOK_HP150_OFFLINE_TEST^{commit}
```

Solo difiere DEVF/CP03_STAGE_HOOK_HP150/. CP01, CP02, tags y PR20/21/14/15 permanecen intactos; PR22/23 y checkpoints 08433c6/85ad920 se conservan en sus ramas. Los diez workflows históricos de CI no se editan. Los filtros y guardas nuevos restringen rama/base/repositorio privado; los artefactos son privados.

Para reproducción: checkout CI al SHA exacto; SDK/Aurora fijados y ZIP LFS original privado ya autorizado. El nuevo workflow ejecuta MSVC/Windows SDK en Windows x64; run_windows.py registra comandos/condiciones. No construye host ni instala en PC. No repetir análisis previos si se conservan certificados/hashes.

Descargar ambos artefactos antes del vencimiento indicado en BUILD_AND_PACKAGE.md. `ci/verify_download.py --help` documenta entradas. [document-ledger.json](evidence/document-ledger.json) fija integridad del checkpoint, excluyéndose a sí mismo; no contiene binarios ni recursos originales. El TEST solo contiene .dusk/manifest.

[HUMAN_TEST](HUMAN_TEST.md) define el siguiente paso tras aprobación del usuario: prueba controlada, sin hot reload y con cierre completo para reversión. Quitar una edición no elimina un actor materializado. No CP04.
