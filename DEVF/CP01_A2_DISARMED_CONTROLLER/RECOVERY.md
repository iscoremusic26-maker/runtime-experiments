# Recuperación del controlador A2 DESARMADO

Repo privado `iscoremusic26-maker/Mods-Duskligh`. Rama independiente **`implementation/devf-cp01-a2-disarmed`** creada desde **2911af67bde2dc1e6376ed7c989cdc862b79126d**, tag histórico `DEVF_CP01_FIRST_SPAWN_STRATEGY_REVIEW`, PR11 draft. Historial/base/tags anteriores no se sobrescriben.

Commits propios: implementación **e54566ebb9f3eaee50d872e95ae0e20f305221c1**; corrección y código compilado definitivo **0fa942f3758cee7d901cf847651b47477aa032af**; informe/evidencia final se identifica por tag nuevo **`DEVF_CP01_A2_DISARMED_CONTROLLER_VERIFIED`** con `^{commit}`. No escribir SHA autorreferente en el propio archivo. PR principal draft contra rama base, sin merge.

## Compilación reproducible y dependencias

- Host/SDK público limpio: `TwilitRealm/dusklight@40457c6adb381928e4b5fef6ed459ed291edd5e2` / v2.0.3. Aurora gitlink **3227d76c60e1e782ca576610bce61c9e7744d8be**; checkout submódulo solo para headers. No se requieren Borealis/randomizer/cosmetics ni build de host/renderer.
- Import library privada originalCP00:9400986bytes SHA **4dc4a511d761e6eb52541733fa31919a2234ed9cd5b2f16f8fea91c468f30ca4**, obtenida únicamente del miembro sdk/windows-amd64.lib del ZIP Windows. Archivo original permanece en repo privado de inputs/LFS, nunca en código/artifact.
- Workflow revisable [ci/windows.yml](ci/windows.yml), activo `.github/workflows/devf-cp01-a2-disarmed.yml` de repo privadoinputs, rama **ci/devf-cp01-a2-disarmed**, [PR7 draft](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/7). BaseCI2e1cee4 ya usaba acceso same-repo/LFS; no nuevo secreto/permiso cross-repo.
- HeadCI definitivo **6ba5533ec4d32f0c7c3735481d300544a50a92f9**, `CI_SOURCE.json` fija main0fa942f. Mirror de código validado por ledger completo en evidence/result; G2 histórico idéntico a ledger revisado.
- Toolchain Winx64/MSVC19.51.36260.0/SDK10.0.26100.0/Ninja/CMake4.4.3/C++20/Release y ABI oficiales. Comandos y tiempos en [TEST_RESULTS](TEST_RESULTS.md) y [result](evidence/windows-pass/result.json).

Reproducción: obtener rama/tag en copia independiente; para CI recuperar rama privada exacta y abrir/actualizar PR únicamente autorizado; runner usa ZIP LFS y SDK público pinned. No ejecutar lab de ABI DLL en el juego ni construir `_package`. Labs ejecutables no importan Dusklight; sólo simulan. El módulo y probe se enlazan pero no se ejecutan/instalan.

## Evidencia conservada

[Run2 PASS](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38341931143), job115114646018, artifact textual11787297060. DownloadZIP SHA **7f4df21533e3ccc2f4ba24841c596d21a180deb8ee1cc87e635dc5e1280ee624**, CRC probado. Run1 FAIL38341748553 conservado con error de tipos y ledger, no eliminado. No se repiten suites históricas o análisis G4.

`evidence/windows-pass/` preserva logs sanitizados, toolchain/compilación/labs/mutantes/guards/imports/exports/metadata/map/disassembly/compile units/hashes. `evidence/binary-review.json` correlaciona direcciones del código propio y la llamada indirecta Log.write con el SDK. `evidence/SHA256SUMS.txt` identifica los textos sanitizados publicados; pueden diferir en bytes/EOL/path-redaction del ZIP descargado, manteniendo el original digest y procedencia.

Solo originales externos, no objetos de este Git: ZIP/EXE/.lib/ARC/BMD/BCK/ROM/save/log privado G2. La DLL desarmada y los tres binarios de laboratorio se generaron en runner, con hashes documentados, pero no se suben como archivos ni se empaquetan. Evidenceartifact sólo .log/.json. No hay instalación/reversión runtime pendiente.

## Recuperación independiente sin modificar trabajo existente

```bash
git init work/devf-a2-recovered
git -C work/devf-a2-recovered remote add origin https://github.com/iscoremusic26-maker/Mods-Duskligh.git
git -C work/devf-a2-recovered fetch origin refs/heads/implementation/devf-cp01-a2-disarmed:refs/remotes/origin/a2 refs/tags/DEVF_CP01_A2_DISARMED_CONTROLLER_VERIFIED:refs/tags/DEVF_CP01_A2_DISARMED_CONTROLLER_VERIFIED
git -C work/devf-a2-recovered switch --detach DEVF_CP01_A2_DISARMED_CONTROLLER_VERIFIED
git -C work/devf-a2-recovered rev-parse HEAD
git -C work/devf-a2-recovered merge-base --is-ancestor 2911af67bde2dc1e6376ed7c989cdc862b79126d HEAD
git -C work/devf-a2-recovered diff --name-only 2911af67bde2dc1e6376ed7c989cdc862b79126d HEAD
git -C work/devf-a2-recovered status --short
```

Diff sólo esta nueva carpeta; G2 y checkpoints anteriores intactos. Verificación de entrega: fetch a bare nuevo, rama/tag→mismoSHA, ascendencia, blobs publicados iguales y referencias históricas conservadas. Restaurar selección documental/código mediante detached/copia nueva, sin reset/force/merge.

## Reanudación mínima y parada

Leer IMPLEMENTATION_REVIEW → SAFETY_AUDIT → TEST_RESULTS → GATE_DECISION. Tres gates desarmados PASS; runtime owner NOT_VERIFIED, creation/render NOT_TESTED; G4 punto bloqueado, G5/CP02 NO-GO, G6 NOT_VERIFIED. Descarga personalizada BLOCKED independiente.

Antes de admitir un punto: revisión del resolver y necesidad concreta de baseline de nuevos vínculos/retirada/contexto, más hazards locales del punto a evaluar. No rehacer recursos/geometry ni activar observer automáticamente. No hay adapter nativo listo para armar; escribirlo requiere tarea posterior y punto/contexto aceptados. No solicitud de prueba in-game al usuario en esta entrega. Se detiene tras publicación y recuperación.
