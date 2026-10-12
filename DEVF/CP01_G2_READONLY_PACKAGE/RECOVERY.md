# Recuperación del checkpoint G2 READ_ONLY

Rama independiente **package/devf-cp01-g2-readonly**, desde `2124adddae1e4433f7523e777cf0a773b2119bb2` / DEVF_CP01_A1_PREFLIGHT_G0_G4. Tag nuevo **DEVF_CP01_G2_READONLY_PACKAGE**; el commit final se obtiene resolviendo ese tag. Todos los cambios son archivos propios nuevos bajo DEVF/CP01_G2_READONLY_PACKAGE; ningún checkpoint/PR histórico se modifica o reescribe. El PR de esta rama queda draft, sin merge.

La fuente compilada y revisada es **b3ed281cbcb5934b7a8bd7d78b5adcef19b09ad2**. Contiene la copia nueva0.0.2 del observador y el gate de revisión; los commits posteriores añaden únicamente documentación y colección de evidencia. Los hashes de todos los archivos usados en CI coinciden con el checkpoint final (download-verification.json). El observador original0.0.1, resultados36PASS, tag2124add y PR#6 permanecen intactos.

Referencias: Dusklight2.0.3 oficial40457c6adb381928e4b5fef6ed459ed291edd5e2; Aurora3227d76c60e1e782ca576610bce61c9e7744d8be; exact CP00 import lib9,400,986bytes, SHA256 `4dc4a511d761e6eb52541733fa31919a2234ed9cd5b2f16f8fea91c468f30ca4`. Se conservan arquitectura545b2d1 y auditoría60ffb08 en el historial; no se utiliza el parche experimental.

## CI y descarga privada

- Repositorio inputs privado, base main9f95a34d93810b55250e8b833a2e343757cf8a01; branch **ci/devf-cp01-g2-readonly**, head `2e1cee42c7f3799a4671bee457ce442c6cc6026c`; [PR de CI#6 draft](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/6), sin merge.
- [Workflow/run38302076854](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38302076854), job114987154136. Templateexacto `ci/windows-package.yml` → `.github/workflows/devf-cp01-g2-readonly.yml` en inputs.
- [Artefacto privado11771626280](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38302076854/artifacts/11771626280), `DEVF_CP01_G2_READ_ONLY_windows-amd64_b3ed281cbcb5934b7a8bd7d78b5adcef19b09ad2`; descarga comprobada. Caduca26oct2026 20:08:01UTC, salvo borrado administrativo.
- Dentro: `.dusk` del mismo nombre,9,930bytes, SHA256 **a2baea22c9c28aa519d8bf339e9920f8609d14460ac7bc77c3dba9f94b1cf30c**, más DOWNLOAD_MANIFEST.json externo. El ZIP externo de Actions tiene otro digest, registrado en PACKAGE_VERIFICATION.
- Logs/textos id11771686151, también conservados byte por byte en Git bajo evidence/windows-pass y contrastados en download-verification.json. **Ningún `.dusk`, DLL, EXE, LIB, ARC, ROM o save está en el repositorio fuente.**

## Recuperar sin sobrescribir trabajo

```bash
git clone --no-checkout https://github.com/iscoremusic26-maker/Mods-Duskligh.git <directorio-nuevo>
git -C <directorio-nuevo> fetch origin refs/tags/DEVF_CP01_G2_READONLY_PACKAGE
git -C <directorio-nuevo> checkout --detach DEVF_CP01_G2_READONLY_PACKAGE
git -C <directorio-nuevo> rev-parse HEAD
git -C <directorio-nuevo> merge-base --is-ancestor 2124adddae1e4433f7523e777cf0a773b2119bb2 HEAD
git -C <directorio-nuevo> diff --name-only 2124adddae1e4433f7523e777cf0a773b2119bb2 HEAD
```

Verificar status antes de retomar; no reset, force push, checkout forzado o merge sobre trabajo existente. La publicación se verifica mediante fetch independiente de branch/tag desde GitHub, igualdad de IDs, ancestry, alcance de diff y hashes exactos de evidencia.

## Reproducir build y paquete sin ejecutar el juego

Recuperar head CI exacto en checkout privado separado; Git LFS debe materializar el ZIP Windows original ya acreditado. Su GITHUB_TOKEN solo necesita contents:read para **su propio repositorio**; no se creó credencial cross-repo. Nunca copiar esos originales al repo DEVF o artefactos. La CI extrae únicamente import lib a temporal y usa el source público40457c6/Aurora exactos, sin configurar host u otras dependencias.

Con MSVC developer environment x64/Windows SDK, utilizar `ci/run_windows.py --source <40457c6> --inputs <inputs-privados> --work <temporal>`. El CI_SOURCE.json del mirror identifica b3ed281. `verify_review` exige los hashes de la auditoría antes de compilar; construye observer/lab, inspecciona PE y guardas, y solo entonces invoca **devf_a1_observer_package**. No target host/install ni juego. `verify_package.py` compara DLL compilado/empaquetado y permite únicamente los cuatro miembros exactos. La carpeta delivery solo se crea al final satisfactorio; el workflow sube el paquete privado únicamente con success.

Los pasos son reproducibles con dependencias fijadas; `windows-latest`/herramientas futuras y timestamps del ZIP pueden cambiar hashes de una reconstrucción. Registrar las versiones/hashes nuevas, repetir la auditoría del resultado y publicar como artefacto distinto; no fingir que equivale byte por byte a esta descarga ni mover el tag anterior. Para una repetición exacta sin cambios de revisión se puede reejecutar el run/head fijado, sujeto a disponibilidad de GitHub/LFS/runner y expiración de logs/artifacts.

`collect_delivery.py` verifica los ZIP descargados originales por los digests GitHub fijados y compara .dusk/miembros/PE con result.json; guarda solo textos en Git y deja la inspección binaria en scratch privado. Si caduca el artefacto, el checkpoint no contiene el binario: será necesaria una generación/verificación nueva, no presentar un enlace caducado como disponible.

DISARMED_NO_REGISTRATION; paquete únicamente para revisión. G2 runtimeNOT_VERIFIED, G0PARTIAL, G4BLOCKED, G5/CP02NO-GO y bloqueo de perfiles personalizados conservados. No instalación, ejecución, hot reload, A1/A2, G6 o CP02 autorizados por recuperar este checkpoint. Detener tras publicar y verificar.
