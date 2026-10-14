# Recuperación CP04.1

Carpeta/rama nuevas sin reescribir CP04/CP03: feature/devf-cp04-1-aura-diagnostic y CIci/devf-cp04-1-aura-diagnostic. Base fuente 080f8e40714f842f170f14ea1a9ff3a5054ac8b2, base CI 4bea35d21049ccef0c8ea0f79ff86e066c43a563. Tag nuevo `DEVF_CP04_1_AURA_GATE_DIAGNOSTIC_OFFLINE_TEST` sobre el checkpoint documental final. No merge/force-push/hostpatch.

La evidencia de esta revisión conserva el fracaso humano como resumen derivado, no log personal. OriginalTESTCP04:14392 bytes / SHA221b6ea51b514905a0e8deb69648331ded809d00924482d855e8bc8895ff3fd6, tag DEVF_CP04_NATIVE_AURA_OFFLINE_TEST080f8e4 íntegro. CP03tag DEVF_CP03_HP150_HUMAN_RUNTIME_VERIFIED_2026-10-14/139d932 y su11975 bytes / SHA0d9882b072fe5cd6248c16a181171a47364e1acf5870503c1eb2f39c668b4344 íntegros. No remitir nuevos logs privados a Git.

Fuente compilada`554c31a3e10906c50dd18a05fe0b55737bf5a3a8`, CI`da07f77fddd13ca1664997e5373f3dfe988cf7e1`, [run 38593704059](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38593704059); [PRfuente27](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/27), [PRCI19](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/19), ambosdraftsinmerge. BUILD/PACKAGE/DOWNLOAD verificados; [HASHES](BUILD_AND_PACKAGE.md), [TEST](HUMAN_TEST.md). Se verifica fetchindependiente del tag/CI y fsck despuésdepush. Los 18 archivosdelledger compilado deben coincidir; documentos/evidencia agregados no cambianproducto.

```bash
git clone --bare https://github.com/iscoremusic26-maker/Mods-Duskligh.git devf-cp04-1-recovery.git
git -C devf-cp04-1-recovery.git rev-parse DEVF_CP04_1_AURA_GATE_DIAGNOSTIC_OFFLINE_TEST^{commit}
git -C devf-cp04-1-recovery.git fsck --full
git -C devf-cp04-1-recovery.git diff --name-only 080f8e40714f842f170f14ea1a9ff3a5054ac8b2 DEVF_CP04_1_AURA_GATE_DIAGNOSTIC_OFFLINE_TEST^{commit}
```

La diferencia fuente exclusivamente DEVF/CP04_1_AURA_DIAGNOSTIC/; CI nueva carpeta+workflowpropio.13 workflowsCI previos intactos;17 archivosCP03 medidos idénticos. Conservar tagscheckpointsviejos080f8e4/139d932 y paquetes privados. Descargar ambosartefactos antesdevencer13-11-2026; no meter .dusk/DLL/assetsoriginales aGit. La apariencia sigueNO-GO y la tarea se detiene al entregar diagnóstico.
