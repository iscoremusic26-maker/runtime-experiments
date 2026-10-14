# Recuperación del diagnóstico v0.3.1

Tag nuevo `DEVF_CP03_HP_DIAGNOSTIC_OFFLINE_TEST`, rama `feature/devf-cp03-hp-diagnostic`, [PR25](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/25) draft contra el baseline v0.3.0. CI `ci/devf-cp03-hp-diagnostic`, [PR17](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/17) draft contra CI v0.3.0. Sin merge ni force-push; baseline76c53b6 y CI4f84a71 intactos.

Fuente compilada `9dd5b8efd4ad98f1d6260820d782e101366a0f8b`; CI `7fd3628ee8bfeb30f8070db061220796c1c15b4a`; run 38541018826. El checkpoint documental final añade informes/evidencia sin cambiar archivos del source ledger. CI_SOURCE.json conserva ese origen. Baseline antiguo .dusk8953 bytes/SHA5754a47e84d56563cfb4143139aa0f4660b6852ce409e30b84fd398b0cfe3229 no se reemplaza.

```bash
git clone --bare https://github.com/iscoremusic26-maker/Mods-Duskligh.git devf-diagnostic-recovery.git
git -C devf-diagnostic-recovery.git rev-parse DEVF_CP03_HP_DIAGNOSTIC_OFFLINE_TEST^{commit} refs/heads/feature/devf-cp03-hp-diagnostic
git -C devf-diagnostic-recovery.git fsck --full
git -C devf-diagnostic-recovery.git diff --name-only 76c53b6bcc61228df3b5a19f35b28fc777d4bde9 DEVF_CP03_HP_DIAGNOSTIC_OFFLINE_TEST^{commit}
```

El diff debe contener solo DEVF/CP03_HP_DIAGNOSTIC/. Los once workflows CI anteriores quedan byte a byte iguales; solo se añade el workflow exclusivo nuevo. CI_SOURCE y SOURCE_MANIFEST fijan origen/hashes; recuperar CI al SHA indicado con SDK/Aurora/lib privados exactos. Pipeline de Windows nunca compila host o ejecuta juego. No repetir el target/ABI/terreno si se conserva evidencia previa.

Descargar TEST/TEXT antes de vencer, verificar SHA externo y ejecutar ci/verify_download.py con ambos ZIPs y sus digests. evidence/document-ledger.json conserva integridad de archivos propios del checkpoint, excluyéndose a sí mismo; no binarios originales o propios en Git.

[HUMAN_TEST](HUMAN_TEST.md) es la siguiente tarea del usuario, tras aprobación: solo v0.3.1, DX12 y EXE exacto, sin hot reload; cierre completo para reversión. No se pide de nuevo la evidencia humana ya proporcionada del baseline. CP03_DIAGNOSTIC_PASS_RUNTIME pendiente; no CP04/CP06.
