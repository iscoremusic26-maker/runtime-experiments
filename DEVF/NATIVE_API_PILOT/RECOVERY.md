# Recuperación exacta del par API

Base literal **f11006f73e84f3aed0427773c5e185aa5345fe42**. Rama **feature/devf-native-api-provider-probe**, [PR44 draft](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/44), sin merge.
Cierre humano previo: **0fe70711d04b1fb8eeb25daf2d481f9e84b28e25**, sólo constancia CP07.1. PR43 mantieneHEADf11006… y descripción corregida, no paquete0.7.0 recompilado/reempaquetado.

## Identidades
- **Fuente realmente compilada: ae4fa410e4543c032fccfe761b2a817ae17479b2**.
- **Build CI: d9100a41afe06ed4f23b8d638baba8102e566066**, [run38787691561](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38787691561) SUCCESS.
- **Verificador CI: 049e028b6f73dae0011966835bd6136322e81d3e**, [run38788164065](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38788164065) SUCCESS.
- CI rama ci/devf-native-api-provider-probe, [PR30 draft](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/30), base8ceec3a417649701f2dcd0d23bfb0902fd85b3aa.
- Workflow nuevo actual download-only; su versión build está en d9100a41…. Ningún workflow histórico cambiado. Checkout real explícito; no usar merge-event SHA como source.
- Checkpoint documental final publicado en PR44/respuesta después de readback, posterior al fuente compilado; no sustituye SOURCE_COMPILED.zip.

## Recuperar sin pisar ramas
```powershell
git fetch origin feature/devf-native-api-provider-probe
if ($LASTEXITCODE -ne 0) { throw 'Fetch fallo' }
$checkpoint = Read-Host 'SHA documental final completo de PR44'
if ($checkpoint -cnotmatch '^[0-9a-f]{40}$') { throw 'SHA invalido' }
git merge-base --is-ancestor f11006f73e84f3aed0427773c5e185aa5345fe42 $checkpoint
if ($LASTEXITCODE -ne 0) { throw 'Base incorrecta' }
git switch --detach $checkpoint
if ($LASTEXITCODE -ne 0) { throw 'Checkout fallo' }
git rev-parse HEAD
```
Para reproducir código del paquete usar ae4fa410e4543c032fccfe761b2a817ae17479b2 o SourceZip verificado. No recompilar para reemplazar artifact histórico. Hashes/tamaños/miembros/CRC exactos en BUILD_AND_PACKAGE.md y evidence/.

## Distribución y preservación
Proveedor0.7.1 mismo ID/editor + probe0.1.0 distinto ID; dos ZIP con un .dusk cada uno. IDs distintos no autorizan mezclar0.7.0/0.7.1. Caducidad API2026-11-14 13:43:54/55 Panamá; no disponibilidad prometida después.
1450entradas históricas principal y123del CI base preservadas por path/blob/mode/type;10copias de core/UI/testsCP07 iguales. Única adición fuera del piloto: constancia humana nueva bajo CP07.1. No tags/commits/binarios/PR históricos movidos; sólo descripciónPR43 actualizada según autorización.
Paquete0.7.0 rollback: .dusk39591bytes/SHA256c1070b6e4fa53f6cfa5e6f77640c30383351dc3dae10964f06edbb77e962cd46 intacto. Mismo data_dir; respaldar su JSON antes de probar NONE. Retirar par con juego cerrado y restaurar sólo0.7.0 y JSON respaldado para rollback.
Retirar probe en frío con NONE deja proveedor independiente y0adicionales, pendiente de QA humana nueva. No borrar actor vivo mediante remove; sin hot reload. Watch/drop owner y cuarentena son política del broker, no una API de ActorId.

Cloud offline: Git/Actions reales, sin shell local ni gameplay fingido.214PASS y22negativos, package/download PASS; HUMAN_PENDING para nuevo par. CP07.1 previo HUMAN_RUNTIME_OBSERVED sólo según reporte/sumario, sin rawlogs/píxeles ni hashes inventados. Sin Expansion/CP07.2/CP08/personalización.
