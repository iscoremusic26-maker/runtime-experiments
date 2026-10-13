# Recuperación del checkpoint offline

Base exacta principal `09a682f0338d24928b3ea1abca0df6972004a596`, taghistórico DEVF_CP01_G4B_OBSERVATION_PACKAGE_VERIFIED_FINAL. Rama nueva `experiment/devf-cp01-a2-first-native`; [PR16 draft](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/16),sin merge. Código compilado `1f184e56b66bef014601419a5c9078f16e112944`; el commit final de esta rama añade únicamente informes/evidencia y herramientas de revisión. Tag de esta entrega: **DEVF_CP01_A2_FIRST_NATIVE_REQUEST_OFFLINE_VERIFIED**. Resuelve el commit final mediante el tag; no confundirlo con la fuente compilada.

[PR10CI draft](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/10),base `ci/devf-cp01-g4b-package@1069e2f2897b137c9ec791861eb862c832a3edcb`,head `ci/devf-cp01-first-native-offline@7a33a26b084aed794108d281d5cad84de7d69d37`. [Run38414957463](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38414957463),success,únicamente first-offline. Ambos repos privados,push/pull disponibles. Sin cambios en workflows históricos; trigger-isolation.json fue comprobado antes de crear PR y el listado de runs/jobs lo confirmó después.

Reproducir **offline**, no instalar:

```bash
git fetch origin refs/heads/experiment/devf-cp01-a2-first-native refs/tags/DEVF_CP01_A2_FIRST_NATIVE_REQUEST_OFFLINE_VERIFIED
git switch --detach DEVF_CP01_A2_FIRST_NATIVE_REQUEST_OFFLINE_VERIFIED
```

En checkout privado de inputs usar HEAD7a33a26...con GitLFS,SDK40457c6...y solo Aurora3227d76...; abrir un Developer Shell MSVCx64+SDKWindows. Ejecutar el runner de TEST_RESULTS con lib exacta. CMake no configura ni compila el host oficial. Workflow literal reproducible en ci/windows-offline.yml; solo el workflow raíz del repo privado de inputs lo ejecutó. No abrir otra PR contra main por defecto ni disparar suites históricas.

Evidencia textual completa en evidence/windows-run-38414957463;artifactverification SHA/CRC/manifest,correlaciónslot32,exactdecoratedimports,toolversions,ledgerhistorical y extracción del usuario. No DLL/EXE/lib/.dusk/ARC/ZIPoriginales ni log privado. Los hashes de binarios en texto son identificación del build, no distribución de binarios.

SDK/host/Aurora intactos. Cuatro carpetas históricas protegidas conservadas byte a byte; snapshot y ledger en historical-unchanged.json. Las referencias Git existentes no se sobrescriben; se verifica rama/tag con fetch independiente y fsck después de publicar. `recovery-verification.json` registra el checkpoint publicado previamente verificado y el protocolo de comprobación para el tag final.

Siguiente paso requiere autorización distinta: admitir ubicación/contexto/sesión y preparar piloto único/coldstart/full-exit, sin hotreload ni claims de cleanup. No repetir geometría ni estudios generales. No ejecutar este módulo,no paquete activo,no CP02.
