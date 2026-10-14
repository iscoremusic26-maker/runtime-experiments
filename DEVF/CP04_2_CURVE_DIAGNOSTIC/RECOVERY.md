# Recuperación CP04.2 diagnóstico

Base fuente7c31c2e41ff8564ed7f79777c9cb9f309cbcd3c0, CI da07f77fddd13ca1664997e5373f3dfe988cf7e1. Ramas nuevas feature/devf-cp04-2-curve-diagnostic y ci/devf-cp04-2-curve-diagnostic; PRs draft nuevos sin merge. Tag nuevo `DEVF_CP04_2_NATIVE_CURVES_ENDPOINTS_DIAGNOSTIC_OFFLINE_TEST` sobre el cierre documental; no mover tags anteriores.

Conservar CP03tag/139d932, CP04tag/080f8e4 y CP04.1tag/7c31c2e, sus paquetes y PRs. La nueva carpeta es exclusivamente DEVF/CP04_2_CURVE_DIAGNOSTIC; CI solo añade esa carpeta yworkflowpropio. No binarios, recursos originales o logs personales enGit. Checkpoint documental posterior no cambia sourceledgercompilado.

Fuentecompilada`b88ffc89ea45758bfe25beea2e97b59ff1294377`, CI `4cb4c238a1010f5638c5200c6ff5716cc2dba49d`, [run 38603069939](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38603069939). [PR fuente 28](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/28), [PR CI 20](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/20), ambos draft sin merge. BUILD/PACKAGE/DOWNLOAD verificados. El tag/finalHEAD yCI se recuperan con fetch independiente/fsck traspush; sourceledger18 archivos y documental comparados byteexactos.

```bash
git clone --bare https://github.com/iscoremusic26-maker/Mods-Duskligh.git devf-cp04-2-recovery.git
git -C devf-cp04-2-recovery.git rev-parse DEVF_CP04_2_NATIVE_CURVES_ENDPOINTS_DIAGNOSTIC_OFFLINE_TEST^{commit}
git -C devf-cp04-2-recovery.git fsck --full
git -C devf-cp04-2-recovery.git diff --name-only 7c31c2e41ff8564ed7f79777c9cb9f309cbcd3c0 DEVF_CP04_2_NATIVE_CURVES_ENDPOINTS_DIAGNOSTIC_OFFLINE_TEST^{commit}
```

Solo diferencia DEVF/CP04_2_CURVE_DIAGNOSTIC/. CI añade carpeta yworkflowpropio;14 workflowsCI previos intactos.17 archivosmedidosCP03 intactos. Source code LLVM/Linux no recompilado. Obtener[diagnóstico](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38603069939/artifacts/11914346552) y[TEXT](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38603069939/artifacts/11914456505) antes 13-11-2026/12:02 Panamá; hashes exactos yexpiración en BUILD_AND_PACKAGE.md. No empaquetar originalJPC ologs privados en recovery. NO-GO para aura; la siguiente evidencia mínima es una sola línea de los dos keyIDs/envelopes. No retomar CP05/CP06.

El tag inicialDEVF_CP04_2_NATIVE_CURVES_DIAGNOSTIC_OFFLINE_TEST→ed2c8c14ea7f358da386bd2aa2773b3cbaaf8a8e permanece intacto. El nuevo tag de endpoints es independiente, no reemplazo. initial-download-verification.json e initial-actions-artifacts.json y logs del primer run preservan la evidencia anterior.
