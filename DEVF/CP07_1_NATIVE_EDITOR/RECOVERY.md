# Recuperación exacta CP07.1

Base literal **8a6181bd6cbb1efb26efd9adb9f41116cb581ef8**; rama **feature/devf-cp07-1-native-editor**, [PR43 draft](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/43), sin merge.

## Identidades
- Primera fuente819f6a23fde8f125f9dfd2066fead106b18495cc, CI81afcf8e0f45418a392349d97f00baabb51153f5, run38769637138 FAILURE tras compilación/164PASS por auditor CRT; evidencia conservada.
- **Fuente realmente compilada: c084729a36661cc6992843baca99f40b3c8211e2**.
- **Build CI: 420ab15de326153e15e1947742fbe8085b13ea54**, [run38770105933](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38770105933) SUCCESS.
- **Verificador CI: 8ceec3a417649701f2dcd0d23bfb0902fd85b3aa**, [run38770449006](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38770449006) SUCCESS.
- CI rama ci/devf-cp07-1-native-editor, [PR29 draft](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/29), basea9aabade816e8ea366b6f74a2cd731723a762ec1.
- Workflow NUEVO actual download-only; versión build recuperable en420ab15d…. Ningún workflow histórico modificado. Checkout SHA real, no merge-event.
- Checkpoint documental final se publica por SHA completo en PR43/respuesta después de readback. Es posterior al source compilado; no modifica SourceZip/paquete congelado.

## Paquete probado offline
ID dev.devf.cp06_native_config_dual versión0.7.0.
ZIP87947bytes/SHA2569033029e6c4fef90d29ff24d42943910072204b31285946f3e1dfda44f31dc14.
.dusk39591bytes/SHA256c1070b6e4fa53f6cfa5e6f77640c30383351dc3dae10964f06edbb77e962cd46.
DLL77312bytes/SHA2564e17e86d11b77589df93a2b91d2a3e21ed94620d9db39e44ed69e327833ae54f.
Artifact11990562891, DEVF_CP07_1_EDITOR_TEST_38770105933, caduca2026-11-14 11:35:25 Panamá. [Descarga](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38770105933/artifacts/11990562891); si URL profunda falla usar Artifacts del run con acceso privado.
No disponibilidad prometida después de caducar, ni recompilación para sustituir el artifact existente.

## Recuperar código
```powershell
git fetch origin feature/devf-cp07-1-native-editor
if ($LASTEXITCODE -ne 0) { throw 'Fetch falló' }
$checkpoint = Read-Host 'SHA documental final completo publicado en PR43'
if ($checkpoint -cnotmatch '^[0-9a-f]{40}$') { throw 'SHA inválido' }
git merge-base --is-ancestor 8a6181bd6cbb1efb26efd9adb9f41116cb581ef8 $checkpoint
if ($LASTEXITCODE -ne 0) { throw 'Base incorrecta' }
git switch --detach $checkpoint
if ($LASTEXITCODE -ne 0) { throw 'Checkout falló' }
git rev-parse HEAD
```
Para el source del TEST usar c084729a36661cc6992843baca99f40b3c8211e2/SOURCE_COMPILED.zip. Docs finales no se insertan retroactivamente en él.

## Preservación/rollback
1417entradas anteriores del principal y95del CI base conservadas por path/blob/mode/type;12copias exactas de core/tests/ejemplosCP06. Única adición fuera de carpetaCP07: cierre humano documental nuevo en CP06_NATIVE_CONFIG_DUAL/HUMAN_RUNTIME_RESULTS_2026-10-15.md. No modificar blobs previos ni refs/PR históricas.
CP06v0.6.2 inmutable: .dusk28803bytes/SHA2562658f7771344e9334219b1416bdbd9ca97cf817b28300c7d347da8e0454c48bb. SameID implica **una sola versión instalada**, sin hot reload.
Rollback: cerrar, retirar0.7.0, restaurar0.6.2 original si se desea. JSON schema1 compatible. Copiar respaldo verificado placements.cp07-backup-XX.json sobre placements.json con juego cerrado si hace falta recuperar estado anterior; conservar copias fuera.
32slots exclusivos; no eliminación automática. Backup no atómico. Si recuperación falla, no reiniciar hasta reparar; editor bloquea guardados. FileService no tiene delete: un fallo persistente de creación puede dejar archivo incompleto, cuya ausencia/invalidación no se debe confundir con una restauración exitosa.
remove_actor_edit retira edición, no actor vivo. UI callbacks desactivados y slots propios retirados con detach del host; no promesa universal de unload dinámico.

Cloud offline; Git/Actions reales, sin shell local ni gameplay fingido. CP06 cuatro modos humano cerrado sólo en alcance reportado; CP07.1 QA humano aún pendiente. Seguir HUMAN_TEST nuevo sin repetir cuatro ensayos históricos. No CP07.2/CP08 ni personalización.
