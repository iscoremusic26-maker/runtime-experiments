# Recuperación y reproducción

Checkpoint final: tag ANOTADO `DEVF_CP01_G5_DISARMED_DIAGNOSTIC_VERIFIED` de la misma rama `fix/devf-cp01-g5-real-log-false-rejects`, PR19 draft, sin merge. Su SHA se verifica mediante `git rev-parse DEVF_CP01_G5_DISARMED_DIAGNOSTIC_VERIFIED^{commit}` y debe ser el HEAD final publicado. El commit fuente compilado es `29efb505a71014f9f8725846576485cdb91f77cd`, distinto del checkpoint final de informes. CI `f02cbd99bc280d6bbd54ab0f08b4ba241b7f0fe4`, rama `ci/devf-cp01-g5-rejections`, PR13 draft; base245c9eec99f7ff0186aac4174f04811cb9918b76 inmutable.

```bash
git clone --bare https://github.com/iscoremusic26-maker/Mods-Duskligh.git devf-recovery.git
git -C devf-recovery.git fetch origin refs/heads/fix/devf-cp01-g5-real-log-false-rejects:refs/heads/g5-recovered refs/tags/DEVF_CP01_G5_DISARMED_DIAGNOSTIC_VERIFIED:refs/tags/DEVF_CP01_G5_DISARMED_DIAGNOSTIC_VERIFIED
git -C devf-recovery.git cat-file -t DEVF_CP01_G5_DISARMED_DIAGNOSTIC_VERIFIED
git -C devf-recovery.git rev-parse DEVF_CP01_G5_DISARMED_DIAGNOSTIC_VERIFIED^{commit} refs/heads/g5-recovered
git -C devf-recovery.git merge-base --is-ancestor 843b2436d9a28305248316b9f54906447e5ec566 refs/heads/g5-recovered
git -C devf-recovery.git fsck --full
```

Verificar que ambos SHA HEAD/tag coinciden y que cat-file informa `tag`, no tag ligero. Recuperar CI de su rama exacta y comparar con `f02cbd99bc280d6bbd54ab0f08b4ba241b7f0fe4`. Bases/historia/762 archivos originales conservados; ledgers `evidence/historical-worktree-sha256.json`, `historical-git-sha256.json` y `historical-refs.json`. Resultados fallidos y finales permanecen en evidence/windows-run-*; no repetir laboratorios cuyos hashes se conservan en REUSE_WINDOWS_LAB.json. Evidencias viejas104+7/46+4 son solo históricas.

Para reproducción Windows, checkout de la rama CI en commit exacto indicado, repositorio privado con LFS disponible. El workflow versionado fija el SDK40457c6adb381928e4b5fef6ed459ed291edd5e2/Aurora3227d76c60e1e782ca576610bce61c9e7744d8be, valida .lib privado y fuentes. Con MSVC x64/WinSDK disponibles, ejecutar el runner:

```powershell
python DEVF/CP01_G5_FIRST_SESSION_REJECTION_FIX/ci/run_windows.py --source .official --inputs . --work "$env:RUNNER_TEMP/g5-rejections"
```

Requiere el evento PR exclusivo y env DEVF_CI_HEAD/GITHUB_HEAD_REF/GITHUB_BASE_REF, no simularlos para adjudicar evidencia Actions. Internamente: CMake Ninja Release con DUSK_SOURCE, DUSK_GAME_EXE=.lib y COMPILE_COMMANDS; target devf_g5_rejection_diagnostic; dumpbin /headers /imports /exports /disasm; auditor exacto/negativos; target SDK devf_g5_rejection_diagnostic_package. No compilar host ni cargar DLL. Comandos/versiones/timing exactos en result.json.

La descarga verificada usa ambos ZIP reales de [este run](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38466822325); las URLs requieren autorización al repositorio privado y los artefactos vencen2026-11-12. `ci/verify_download.py --help` y `ci/download_negatives.py --help` describen inputs/digest GitHub/scratch/output; reproduce solo inspección estática. Los digest/build/source ledgers y miembros se conservan en Git aunque los artefactos expiren. No se puede prometer re-descarga tras su vencimiento.

Retiro/reversión futura solo tras autorización humana: cerrar totalmente el proceso, identificar rutas reales/backups/mods/data/saves/autosaves, retirar de forma controlada el activo0.0.1; nunca sobrescribirlo ni cargarlo junto al diagnóstico. Eventualmente retirar solo el nuevo archivo con proceso cerrado. No hot reload y no promesa de rollback de progreso/autosaves. Nada instalado/modificado en la PC en esta tarea.

NEXT_G5_SESSION_AUTHORIZED=FALSE, CP02=NO_GO, ubicación/G6 NOT_VERIFIED, unloading custom BLOCKED_INDEPENDENT. Detenerse aquí.
