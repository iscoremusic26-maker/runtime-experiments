# Checkpoint y reproducción

Tag anotado **DEVF_CP01_STAGE_BOKOBLIN_MINIMAL_PACKAGE_VERIFIED**, rama feature/devf-cp01-stage-bokoblin-minimal, [PR20](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/20) draft sin merge. Fuente compilada `a17109b91ba5fde7a221ac72a4b5640570b8a4d2` distinta del checkpoint documental final. Base2e1b86edc1d189f0954714e0a168ae3f0bef6cea y tag DEVF_CP01_G5_DISARMED_DIAGNOSTIC_VERIFIED intactos; PR19/13 y piloto ActorService conservados.

CI rama ci/devf-cp01-stage-bokoblin-minimal/[PR14](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/14), HEAD `09b6464343a2db0d64a643ab06714ef9f042b061`, basef02cbd99bc280d6bbd54ab0f08b4ba241b7f0fe4. Ocho workflows históricos sin cambios y filtros disjuntos; nuevo workflow requiere repo privado/PR same-repo/baseSHA/head/base exactos.

Recuperación independiente, con autorización al repo privado:

```bash
git clone --bare https://github.com/iscoremusic26-maker/Mods-Duskligh.git devf-stage-recovery.git
git -C devf-stage-recovery.git rev-parse DEVF_CP01_STAGE_BOKOBLIN_MINIMAL_PACKAGE_VERIFIED^{commit} refs/heads/feature/devf-cp01-stage-bokoblin-minimal
git -C devf-stage-recovery.git cat-file -t DEVF_CP01_STAGE_BOKOBLIN_MINIMAL_PACKAGE_VERIFIED
git -C devf-stage-recovery.git fsck --full
```

HEAD y tag deben resolver al mismo SHA y tipo=tag. Base debe seguir siendo ancestor. SOURCE_MANIFEST fija SDK/fuentes/tooling; evidence/checkpoint-file-sha256.json fija informes/herramientas. Solo nuevo directorio cambia respecto2e1b86e; no originales ni binarios comiteados.

Workflow ci/windows-stage.yml reutiliza checkout/actions/MSVC privados. Tras checkout del commit CI exacto y SDK/Aurora indicados, LFS debe suministrar ZIP Windows íntegro. RunWindows valida SHA/size/CRC de.lib y source pins, configura CMake y compila; runner exige evento PR exclusivo y registra comandos/tiempos reales en result.json. Reproducir mediante nuevo run autorizado del mismo workflow, no cargar DLL ni compilar host. Windows-latest puede cambiar toolchain: versiones efectivas registradas, no promesa de reproducibilidad byte-a-byte futura.

ci/verify_download.py --help reproduce solo inspección de ambos ZIP descargados, scratch y hashes GitHub; nunca ejecuta DLL. Evidencia de once fakes de38496356945 se reutiliza por hashes exactos y misma toolchain; no repetir suites históricas. Los tres fallos y el éxito final permanecen versionados.

Punto/params: LOCATION/SOURCE_REVIEW; operación humana: HUMAN_TEST. No instalación automática. Tras eventual aprobación, procesos cerrados y backups/rutas reales; no hot reload/teleport/flags. No afirmar spawn desde edit_handle. Aparición/render/combate/limpieza/DX12 NOT_TESTED, CP02 NO_GO, unloading custom anterior preservado independientemente. Detener esta etapa tras entregar.
