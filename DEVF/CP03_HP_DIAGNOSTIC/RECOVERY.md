# Recuperación del diagnóstico v0.3.1

## Cierre humano actual

Estado: **CP03_HUMAN_RUNTIME_PASS** para el flujo documentado en [HUMAN_RUNTIME_RESULTS_2026-10-14.md](HUMAN_RUNTIME_RESULTS_2026-10-14.md). El cierre utiliza el tag nuevo `DEVF_CP03_HP150_HUMAN_RUNTIME_VERIFIED_2026-10-14`, dirigido al commit documental de la rama `feature/devf-cp03-hp-diagnostic`. Su SHA completo se obtiene con los comandos siguientes y se informa en PR25 y en la entrega final, evitando escribir un SHA circular dentro de su propio commit. El objeto del tag y su commit se comprobarán mediante fetch independiente; no se mueve ningún tag anterior.

```bash
git clone --bare https://github.com/iscoremusic26-maker/Mods-Duskligh.git devf-human-recovery.git
git -C devf-human-recovery.git rev-parse DEVF_CP03_HP150_HUMAN_RUNTIME_VERIFIED_2026-10-14
git -C devf-human-recovery.git rev-parse DEVF_CP03_HP150_HUMAN_RUNTIME_VERIFIED_2026-10-14^{commit}
git -C devf-human-recovery.git fsck --full
git -C devf-human-recovery.git diff --name-only 9e0a804e73d474df9345680ad77e677656bd0d32 DEVF_CP03_HP150_HUMAN_RUNTIME_VERIFIED_2026-10-14^{commit}
git -C devf-human-recovery.git diff --exit-code 9dd5b8efd4ad98f1d6260820d782e101366a0f8b DEVF_CP03_HP150_HUMAN_RUNTIME_VERIFIED_2026-10-14^{commit} -- DEVF/CP03_HP_DIAGNOSTIC/src DEVF/CP03_HP_DIAGNOSTIC/tests DEVF/CP03_HP_DIAGNOSTIC/ci DEVF/CP03_HP_DIAGNOSTIC/CMakeLists.txt DEVF/CP03_HP_DIAGNOSTIC/mod.json DEVF/CP03_HP_DIAGNOSTIC/SOURCE_MANIFEST.json
```

El diff del cierre solo debe incluir Markdown autorizado y nueva evidencia documental/ledger dentro de DEVF/CP03_HP_DIAGNOSTIC/. Los 17 archivos de fuente del ledger se midieron contra el commit compilado y permanecen byte a byte iguales. [Medición de cierre](evidence/human-runtime-closure-integrity-2026-10-14.json), [ledger documental nuevo](evidence/human-runtime-closure-ledger-2026-10-14.json). `evidence/document-ledger.json` sigue siendo el ledger histórico del checkpoint **9e0a804**; validarlo sobre ese commit, no sobre los Markdown actualizados. No se altera ese ledger, CI_SOURCE.json ni los manifests de build.

Recuperar el paquete exacto del [TEST privado existente](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38541018826/artifacts/11881653953), no reconstruirlo: `DEVF_CP03_HP_DIAGNOSTIC_windows-amd64_9dd5b8efd4ad98f1d6260820d782e101366a0f8b.dusk`, **11975 bytes**, SHA256 `0d9882b072fe5cd6248c16a181171a47364e1acf5870503c1eb2f39c668b4344`. Fuente compilada `9dd5b8efd4ad98f1d6260820d782e101366a0f8b`, CI `7fd3628ee8bfeb30f8070db061220796c1c15b4a`, [run 38541018826](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38541018826), TEXT11881743937. Module ID/versión0.3.1 no cambian.

TEST caduca el **13-11-2026, 04:16:37 Panamá**; TEXT un segundo antes. Disponibilidad confirmada en este cierre mediante metadata de GitHub. Se volvió a medir el ZIP de la descarga anterior disponible localmente; no se descargó de nuevo ni se creó otra distribución. Preserva offline el paquete original y su manifest de procedencia verificada antes de expirar, en almacenamiento privado propio; verifica con `Get-FileHash -Algorithm SHA256`. No subas el paquete ni logs personales a Git. Si el artifact expira, usar la copia privada previamente verificada; no presentar un rebuild como el mismo binario.

No se requiere repetir pruebas ya completadas. El protocolo anterior permanece como referencia histórica. PR25/PR17 siguen draft sin merge; repo CI intacto, sin nuevas ejecuciones Windows. CP01/CP02, v0.3.0 y tags históricos preservados. CP04/CP06 no iniciados.

## Recuperación del checkpoint offline histórico

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
