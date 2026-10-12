# Checkpoint CP01 A1 G0–G4

Rama principal independiente **preflight/devf-cp01-a1-g0-g4**, desde `60ffb08ea1337592d3e05216f3f3d97f37426e18`. [PR#6 draft](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/6) contra audit/devf-dawnlight-v403 para mostrar exclusivamente el incremento; sin merge. Tag nuevo **DEVF_CP01_A1_PREFLIGHT_G0_G4** identifica el commit final de este directorio. Resolver el commit por Git/tag, no por un hash autorreferencial dentro del archivo.

Fuentes propias de observador/lab compiladas: `57a167a6c650ab9473db31c4eac531dba8e6a127`. Los commits posteriores solo conservan informes y extracción de evidencia; mismos src/tests/ci de build, verificados por windows-verification.json. Recuperar tag recupera también todos los checkpoints anteriores en su ancestry. No se mueve ningún tag ni se edita un PR histórico.

Referencias preservadas:

- DEVF_CP01_DAWNLIGHT_FOCUSED_AUDIT /60ffb08.
- DEVF_CP01_OFFICIAL_SDK_ARCHITECTURE /545b2d1418bfcae11dd4585c1a9bdcbc526b6a2d.
- Dusklight2.0.3 oficial /40457c6adb381928e4b5fef6ed459ed291edd5e2; Aurora3227d76c60e1e782ca576610bce61c9e7744d8be.
- Dawnlight4.0.3 /9bb214d47617c9bc295d22facf36c35d17661e5a, solo referencia histórica.
- inputs privados main9f95a34d93810b55250e8b833a2e343757cf8a01; originales LFS sin modificar.
- CI independiente [inputs PR#5 draft](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/5), rama ci/devf-cp01-a1-g0-g4, head988bafed31e93674082cc926086e56d92728c175; [run38297058072](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38297058072). Solo fuentes propias y workflow nuevos; ningún original añadido.

## Recuperación sin alterar un checkout existente

```bash
git clone --no-checkout https://github.com/iscoremusic26-maker/Mods-Duskligh.git <nuevo-directorio>
git -C <nuevo-directorio> fetch origin refs/tags/DEVF_CP01_A1_PREFLIGHT_G0_G4
git -C <nuevo-directorio> checkout --detach DEVF_CP01_A1_PREFLIGHT_G0_G4
git -C <nuevo-directorio> rev-parse HEAD
git -C <nuevo-directorio> merge-base --is-ancestor 60ffb08ea1337592d3e05216f3f3d97f37426e18 HEAD
git -C <nuevo-directorio> diff --name-only 60ffb08ea1337592d3e05216f3f3d97f37426e18 HEAD
```

El diff debe contener únicamente DEVF/CP01_A1_PREFLIGHT. Comprobar primero status antes de retomar trabajo; nunca checkout/reset forzado sobre cambios propios. La verificación de publicación utiliza fetch independiente por rama y tag y compara ambos IDs, ancestry y diff; no hace merge.

## Reproducción limitada

Workflow exacto en ci/windows-observer.yml, ejecutado como .github/workflows/devf-cp01-a1-observer.yml del repo privado inputs. Se ejecuta allí porque GITHUB_TOKEN tiene acceso a **sus propios** LFS; no se crea ni publica una credencial cross-repo. Public source40457c6 y Aurora exacta solamente; no configure host/vcpkg/otros submódulos. MSVC developer prompt x64 y Windows SDK requeridos.

`ci/run_windows.py --source <checkout-oficial> --inputs <inputs-privados> --work <temporal>` extrae solo import lib a temporal, compila targets observer/lab, prueba guardas, inspecciona PE/metadata y produce exclusivamente evidencia textual. No ejecutar target package/install. Artefacto original de CI y sus12logs/result.json están preservados y verificados en evidence/. No DLL/lib/EXE/.dusk ni bytes de ARC en este directorio.

`ci/collect_static.py --cache <cp01-location-conservado> --source <40457c6> --output <json>` reconstruye únicamente selection-static usando el inventario y room.dzr ya decodificados. Si se pierde el caché, conservar este JSON verificable; no reanalizar KCL/WRock/Digpl. Reconstruir solo la extracción DZR necesaria desde la evidencia privada ya acreditada si se requiere cambiar/comprobar esos campos. No solicitar los ZIP completos otra vez.

Al retomar: G0PARTIAL, G1build/labPASS, G2NOT_VERIFIED, G4BLOCKED, G5/CP02NO_GO. Mantener DISARMED_NO_REGISTRATION y el bloqueo independiente de descarga DLL; no aplicar parches experimentales ni alterar implementación previa. Siguiente paso mínimo: nueva autorización para observación G2 sin spawn, con E_OC/E_ocb privados si se desea avanzar el expediente geométrico. Detener esta tarea tras verificar la publicación.
