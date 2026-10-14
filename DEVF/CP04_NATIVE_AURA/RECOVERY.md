# Recuperación CP04 offline

Rama nueva feature/devf-cp04-native-aura, [PR26](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/26) draft contra CP03 humano139d932. CI ci/devf-cp04-native-aura, [PR18](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/18) draft contra7fd3628. Tag nuevo `DEVF_CP04_NATIVE_AURA_OFFLINE_TEST`, sin merge o force-push. No CP05/CP06.

Fuente exacta compilada `18daf7648a35c5ee3a89b8a21f9f6d8248e25c30`, CI `4bea35d21049ccef0c8ea0f79ff86e066c43a563`, [run 38585920329](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38585920329). El commit documental final añade evidencia e informes sin cambiar el source ledger. CP03 humano/tag08ffbae, sus módulos/ramas/PRs y el paquete11975 bytes/SHA0d9882b072fe5cd6248c16a181171a47364e1acf5870503c1eb2f39c668b4344 se conservan; el nuevo módulo tiene ID/version propios.

```bash
git clone --bare https://github.com/iscoremusic26-maker/Mods-Duskligh.git devf-cp04-recovery.git
git -C devf-cp04-recovery.git rev-parse DEVF_CP04_NATIVE_AURA_OFFLINE_TEST^{commit}
git -C devf-cp04-recovery.git fsck --full
git -C devf-cp04-recovery.git diff --name-only 139d9329f7a2d5d191b6e0ef7149ac9bbf82d29f DEVF_CP04_NATIVE_AURA_OFFLINE_TEST^{commit}
```

Solo debe diferir DEVF/CP04_NATIVE_AURA/. El ledger documental nuevo permite verificar archivos propios, sin incluirse a sí mismo; el source ledger final incluye CPP/headers/tooling y no cambia. Repo CI solo añade carpeta/workflow nuevo; doce workflows anteriores intactos. No reabrir auditorías previas si sus certificados se conservan.

Descargar [TEST](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38585920329/artifacts/11905691294) y [TEXT](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38585920329/artifacts/11905676250) privados antes de vencer (13-11-2026,10:04 Panamá). Archivo `DEVF_CP04_NATIVE_AURA_windows-amd64_18daf7648a35c5ee3a89b8a21f9f6d8248e25c30.dusk`, 14392 bytes/SHA256 `221b6ea51b514905a0e8deb69648331ded809d00924482d855e8bc8895ff3fd6`. Preservar copia privada/manifest, sin añadir binarios a Git. ci/verify_download.py verifica ambos ZIPs con sus digests. No sustituir por DLL antigua renombrada.

[HUMAN_TEST](HUMAN_TEST.md): solo CP04, EXE exacto/DX12, modelo/combate/HP/recarga, control original E_OC2 y retirada tras cierre completo. common.jpc no se recibió para inspección física: su aceptación se determina por guard real, PENDING hasta ejecución. Si REJECTED, cerrar y aportar log, no editar originales o afirmar apariencia. No pide repetir CP03. CP04_APPEARANCE_RUNTIME_PASS aún no otorgado.
