# Recuperación CP04.2 diagnóstico

Base fuente7c31c2e41ff8564ed7f79777c9cb9f309cbcd3c0, CI da07f77fddd13ca1664997e5373f3dfe988cf7e1. Ramas nuevas feature/devf-cp04-2-curve-diagnostic y ci/devf-cp04-2-curve-diagnostic; PRs draft nuevos sin merge. Tag nuevo `DEVF_CP04_2_NATIVE_CURVES_DIAGNOSTIC_OFFLINE_TEST` sobre el cierre documental; no mover tags anteriores.

Conservar CP03tag/139d932, CP04tag/080f8e4 y CP04.1tag/7c31c2e, sus paquetes y PRs. La nueva carpeta es exclusivamente DEVF/CP04_2_CURVE_DIAGNOSTIC; CI solo añade esa carpeta yworkflowpropio. No binarios, recursos originales o logs personales enGit. Checkpoint documental posterior no cambia sourceledgercompilado.

Fuentecompilada`63450cdc25e1714cdff9ef9e987dec0d2091bde2`, CI `3ef9e525c9dd1e04f8661ef624b267d86fe6b0db`, [run 38601042519](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38601042519). [PR fuente 28](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/28), [PR CI 20](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/20), ambos draft sin merge. BUILD/PACKAGE/DOWNLOAD verificados. El tag/finalHEAD yCI se recuperan con fetch independiente/fsck traspush; sourceledger18 archivos y documental comparados byteexactos.

```bash
git clone --bare https://github.com/iscoremusic26-maker/Mods-Duskligh.git devf-cp04-2-recovery.git
git -C devf-cp04-2-recovery.git rev-parse DEVF_CP04_2_NATIVE_CURVES_DIAGNOSTIC_OFFLINE_TEST^{commit}
git -C devf-cp04-2-recovery.git fsck --full
git -C devf-cp04-2-recovery.git diff --name-only 7c31c2e41ff8564ed7f79777c9cb9f309cbcd3c0 DEVF_CP04_2_NATIVE_CURVES_DIAGNOSTIC_OFFLINE_TEST^{commit}
```

Solo diferencia DEVF/CP04_2_CURVE_DIAGNOSTIC/. CI añade carpeta yworkflowpropio;14 workflowsCI previos intactos.17 archivosmedidosCP03 intactos. Source code LLVM/Linux no recompilado. Obtener[diagnóstico](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38601042519/artifacts/11912504137) y[TEXT](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38601042519/artifacts/11913134088) antes 13-11-2026/11:48 Panamá; hashes exactos yexpiración en BUILD_AND_PACKAGE.md. No empaquetar originalJPC ologs privados en recovery. NO-GO para aura; la siguiente evidencia mínima es una sola línea de los dos keyIDs/envelopes. No retomar CP05/CP06.
