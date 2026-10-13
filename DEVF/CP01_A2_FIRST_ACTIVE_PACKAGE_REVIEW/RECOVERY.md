# Recuperación privada y reproducción

**ACTIVE-CAPABLE / NOT INSTALLED / NOT RUN / SESSION NOT AUTHORIZED.**

Dusklight **2.0.3 Windows x64/DX12**; paquete ID`dev.devf.cp01_eoc_first_active_pilot` versión`0.0.1`; fuente compilada`a67662bec0be8ac7982dd8685f9ac29cc1c0ebea`.

Base0ff1b8bf5e331fc411d6dd9e5fc70c7b3809c75e, tag DEVF_CP01_A2_FIRST_PILOT_SAFETY_TRACE_VERIFIED. Rama nueva `package/devf-cp01-first-active-eoc-review`, [PR18 draft](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/18), base anterior intacta. Nuevo tag anotado **DEVF_CP01_FIRST_EOC_ACTIVE_PACKAGE_REVIEW_VERIFIED** resuelve el checkpoint final; no autoriza una sesión.

Fuente compilada `a67662bec0be8ac7982dd8685f9ac29cc1c0ebea`; producción/laboratorio equivalentes por hash a99b523c790ceecc747e385346e3419af4959e2f7. El runner posterior corrige la comparación de conjuntos de imports y reutiliza evidencias iguales. CI`245c9eec99f7ff0186aac4174f04811cb9918b76`, rama`ci/devf-cp01-first-active-package`, [PR12 draft](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/12), base exacta0b7b517ff2fdce5a0964cbc1dbd91d4a27525b28 intacta. SDK/Aurora/importlib exactos en SOURCE_AUTHORITY y DOWNLOAD_MANIFEST.

```bash
git fetch origin refs/heads/package/devf-cp01-first-active-eoc-review:refs/remotes/origin/package/devf-cp01-first-active-eoc-review
git fetch origin refs/tags/DEVF_CP01_FIRST_EOC_ACTIVE_PACKAGE_REVIEW_VERIFIED:refs/tags/DEVF_CP01_FIRST_EOC_ACTIVE_PACKAGE_REVIEW_VERIFIED
git switch --detach DEVF_CP01_FIRST_EOC_ACTIVE_PACKAGE_REVIEW_VERIFIED
```

Un fetch independiente en bare verifica branch/tag con el mismo peeledSHA, ancestor base y `git fsck --full`. `ci/verify_checkpoint.py` contrasta16 inputs propios de fuente compilada, hashes/bytes textuales de los tres runs,658 archivos históricos(incluido subset277),50 refs y procedencia de la entrega. El record recovery-verification certifica el parent publicado antes de añadir el record; la comprobación del final branch/tag se hace después de publicarlos, sin autorreferencia. PRs#15/#16/#17 y tags anteriores permanecen intactos, sin merge.

Reproducción Windows: workflow `ci/windows-package.yml`, idéntico al real del [run final](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38435464736). Checkout CI exacto y SDK/Aurora fijados; GitLFS para ZIP privado y .lib verificada; MSVC x64/Ninja Release; build solo DLL; verifica hashes para reutilizar labs; auditoría PE/map/disasm; target oficial package; auditoría interna; upload privado. No carga DLL ni ejecuta el juego. La opción Rerun de Actions sobre ese commit repite el pipeline; no se hizo otro rerun tras PASS. La imagen/toolchain móvil puede cambiar timestamps/hashes y exigir nuevo manifiesto/auditoría; no se promete reproducción binaria bit a bit.

Para reproducir el laboratorio offline, configurar este CMakeLists con SDK/.lib exactos y DeveloperShell MSVCx64; construir/ejecutar exclusivamente active_provider_lab. mutations.py conserva los cuatro fixtures de mutación. Reutiliza el Fake histórico sin duplicarlo; el main histórico104 no se ejecuta. Evidencia original en run38434647284.

[Artefacto privado](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38435464736/artifacts/11832392953), expira2026-11-12T17:03:55Z. Textos completos en Git sobreviven a Actions. Git no contiene .dusk/DLL/EXE/LIB/ROM/ARC/saves/logs privados. Si el artefacto expira, cualquier reconstrucción debe volver a auditar su identidad; no sustituir por G4B ni DLL offline. Recuperar este checkpoint no autoriza instalar/cargar. G5/CP02 NO-GO.
