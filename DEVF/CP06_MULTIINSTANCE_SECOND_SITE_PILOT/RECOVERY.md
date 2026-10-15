# Recuperación del checkpoint acotado

Base exacta `3ab8ff2fdd42128ab75157338699b21ae6d768bd`, rama `feature/devf-cp06-multiinstance-second-site-pilot`, [PR39 draft](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/39), sin merge.
Inicial db254b9fa7d2714e4bb647b1880cac11b18fa5ba: alcance y sello. Herramientas/datos `a94eba477869a6a203949366945414a309e3902b`: progreso recuperable. SHA documental final literal en PR39/respuesta tras readback, no fuente compilada.

## Tag humano resuelto
[DEVF_CP06_PARTIAL_SINGLE_SITE_HUMAN_RUNTIME_OBSERVED_2026-10-15](https://github.com/iscoremusic26-maker/Mods-Duskligh/tree/DEVF_CP06_PARTIAL_SINGLE_SITE_HUMAN_RUNTIME_OBSERVED_2026-10-15): objeto anotado **5b9f28473654e26efe9514d0e2543b561511f3b3** → **3ab8ff2fdd42128ab75157338699b21ae6d768bd**, API ref tipo tag y objeto tipo commit comprobados.
[Run38744256177](https://github.com/iscoremusic26-maker/Mods-Duskligh/actions/runs/38744256177), job116453620391 SUCCESS. Las notas TAG_PENDING en el cierre anterior quedan históricas, no reescritas. Seis refs históricos en SOURCE_MANIFEST.json; no retag/force/amend/reset/rebase/merge.

## Recuperar sin instalar ni compilar
En clon privado autorizado:
```powershell
git fetch origin feature/devf-cp06-multiinstance-second-site-pilot --tags
if ($LASTEXITCODE -ne 0) { throw 'Fetch falló' }
$checkpoint = Read-Host 'SHA documental completo publicado en PR39'
if ($checkpoint -cnotmatch '^[0-9a-f]{40}$') { throw 'SHA inválido' }
git merge-base --is-ancestor 3ab8ff2fdd42128ab75157338699b21ae6d768bd $checkpoint
if ($LASTEXITCODE -ne 0) { throw 'Base incorrecta' }
git switch --detach $checkpoint
if ($LASTEXITCODE -ne 0) { throw 'Recuperación falló' }
git rev-parse HEAD
```
CI privado: rama ci/devf-cp06-second-site-source-review, commit98bbb027c91e4cabc9629f370971345c887a958c, [PR25 draft](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/25), base0dcb9fade4cf48a136f210efc1c4a42cd3e5a4ba. ZIP y baseline originales intactos. Cache privada temporal, sin artifacts de recursos ni rawlogs de usuario.

## Continuar sin repetir
TAG_SEALED: no sellar otra vez. NO_GO_MULTIINSTANCE: probar primero único límite de transferencia owner+handle→buffer propio→solicitud, con ABI/lifecycle y rechazo de ambigüedad; no setID/posición/orden como token. Ver PROVENANCE_AND_LIFECYCLE.
Norte: soporte fundamentado y bounds externos autorados separados; sur dos cotas inconclusas. Conservar consultas y JSON, no repetirlas salvo corrección/pérdida. SITE2_PENDING por rutas/interacciones/contexto/envolvente efectiva; no otro ARC general.
Sólo tras resolver esos gates: adaptar owners y rollback atómico, pruebas core/negativos, MSVC/PE/package/descarga independiente de versión nueva y ensayo humano condicionado. No se emitió TEST multiinstancia. El .dusk parcial original sigue rollback exacto, sin cambios. CP07/08/Posture/Expansion no iniciados.
