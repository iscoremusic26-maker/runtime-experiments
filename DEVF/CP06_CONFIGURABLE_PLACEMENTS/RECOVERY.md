# CP06 — Recuperación exacta / handoff

> **Estado documental posterior a la build (2026-10-15): CP06_PARTIAL_HUMAN_RUNTIME_OBSERVED.** [Cinco pruebas humanas y límites](HUMAN_RUNTIME_RESULTS_2026-10-15.md): presets alternativos en frío, desactivación JSON y rollback CP06 observados; sigue CHECKPOINT_CP06_PARTIAL, sin segundo sitio ni multiinstancia. El texto original que sigue conserva el estado histórico al compilar; no se modificó el .dusk ni se repitieron builds/pruebas. Procedencia de logs: USER_LOG_ANALYZED_IN_CHATGPT; observaciones: USER_HUMAN_REPORTED. Tag humano TAG_PENDING; [recuperación](RECOVERY.md#cierre-humano-documental-2026-10-15).

Base3f6e2fc7a285dbce8cb520e0b4536ff56d542930, rama feature/devf-cp06-configurable-placements-pilot, PR37 draft/sin merge. Checkpoint inicial f634544c62f1f47e86a1a66b4b865bb64a436a8b. Fuente/build/hash finales se publican al completar gates.
CP05 humano TAG_SEALED: objetofc289b8c75b87ebc46ff34003f7545cfa8a60c7a→3f6e2fc7a285dbce8cb520e0b4536ff56d542930, run38688503925/PR36. PR35 y commit inmutables; TAG_PENDING del informe es histórico.
CP05 técnico83b2cea8815a8c01b29ad1f3df2a3731f7b667f4→7a7c8bc34841e6f85020cca93ff591e9cb9e789d; CP04 humano f21d0d95e0fc7d5fcbca15ae17ba6b50cdee564e→f7a6623f6d931bacef6f2c8e54f46f7476780ade; CP03 objeto08ffbae5e5da73658df77b3763de2fe6851f7a45→139d9329f7a2d5d191b6e0ef7149ac9bbf82d29f, sin mover tags.
CP05 .dusk18929/SHA23f81ad131082a03fcd66068ccd926ecf878182a5afce06244898cf663248ddb; CP04 .dusk15287/SHAa1b1e750575253c8ec33193c385240337b8f1d5db6f3e9389fba08683c6d97f9 intactos.
Recuperar en clon nuevo con fetch de rama/tags y switch --detach al SHA literal publicado en PR/chat; no reset/force/amend/merge. Cloud offline; todo código nuevo está en GitHub privado. No volver a pedir ARC ni reanalizar etapas cerradas.
CP06_PARTIAL: 2presets alternativos,1activo,1sitio, iniciofrío. No moverubicaciones ni epoch general ni2instancias; pendientes concretos, noMVP. Siguiente continuación mínima requiere autorización para correlación fiable de placements y nueva evidencia espacial de segundo sitio, sin extender editor/expansión. Tag técnico CP06 no HUMAN_RUNTIME_VERIFIED.

## Checkpoint posterior: CHECKPOINT_CP06_PARTIAL

Fuente realmente compilada `107c79987b0d3d1d28319654739a72bd498271bb`; CI `5ba8018f6af0e3d0b98af745d5cd0433d485955a`; [build38690126831](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38690126831) y [descarga38690375002](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38690375002) SUCCESS. SourceCI distinto del SHA documental/tag final, que se entrega literalmente tras readback en PR37/chat. 28blobsdelbuild y espejo coinciden exactamente;1309entradas delbaseline se conservan.
[Artifact11951843169](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38690126831/artifacts/11951843169),ZIP83222/SHAe79a0e76d3471530927ca169bbe4cbe107689b36200a63119ace012d261a10a1,.dusk41419/SHAb1e8f63797e93c0064e83fc39a984c1c806d046761f675b20ac55063b6a6dfa2,DLL77824/SHA45effe8a0ac9d56c3921c2cd6d0a27e9ea7017821559ef96b94b21ff390214e0,vence2026-11-14 01:04:00 Panamá. NuevoPARTIAL, no reemplazo deCP05.

Recuperar código compilado en clon nuevo:
```powershell
git fetch origin feature/devf-cp06-configurable-placements-pilot --tags
git switch --detach 107c79987b0d3d1d28319654739a72bd498271bb
git rev-parse HEAD
```
Para resultados finales usar SHA dePR37/chat o tagtécnico DEVF_CP06_PARTIAL_SINGLE_SITE_PRIVATE_TEST_READY cuando suref/objeto hayan sido verificados. No usar nombreHUMAN_RUNTIME_VERIFIED. No force/reset/amend/merge.
CIinputs PR24; rama ci/devf-cp06-configurable-placements-pilot enmodo download-only. Baselineinputs6b32ef995814e6a20924d6b6dd3fe5886a5ef3e0 y originales permanecen privados e intactos. No repetirCP01–05/render/ARC/SDKLinux.

**MVPno completo:** A moverXYZ bloqueado por falta de segundo sitio acreditado; B2activos/sceneepoch/correlación general no implementado. C toggle/retirada/2presets alternativos por iniciofrío implementado, runtimeporprobar. D gatesWindows/package/download PASS; E históricos preservados.
Próxima continuación mínima necesita autorización focal para vínculo inequívoco placementId→ActorId/sceneepoch y segundo sitio con evidenciaespacial concreta. No relajar max1/whitelist para simular cumplimiento. No se ha autorizado editor/CP07/08/BokoblinExpansion ni mejoras deAI.

El workflow nuevo .github/workflows/devf-cp06-partial-tag.yml sólo sella un tag técnico PARTIAL desde la rama/PR37 privada y base3f6exacta: verifica ascendencia del cierre, grafo compilado, evidenceJSON/manifestMVPfalse y sólo archivos nuevos CP06; rechaza tag existente, sin force. No build ni cambio de workflows históricos. Objeto/destino se publican literalmente en PR37/chat tras API readback. Si el sello falla, conservar SHA/PR como TAG_PENDING; no usar otro tag ni sobrescribir.

## Cierre humano documental 2026-10-15

[Informe y cinco pruebas](HUMAN_RUNTIME_RESULTS_2026-10-15.md). Estado **CP06_PARTIAL_HUMAN_RUNTIME_OBSERVED**, sigue CHECKPOINT_CP06_PARTIAL. Padre exacto `1a57ce17347d2f9c229af4c424d8b05a5ad59353`; rama hija `feature/devf-cp06-partial-human-runtime-closure`, PR draft separado basado en `feature/devf-cp06-configurable-placements-pilot`. El SHA documental completo se entrega en el PR y respuesta final tras readback (no es el SHA compilado). Sólo cinco Markdown de esta carpeta cambian; los cuerpos históricos de los cuatro documentos anteriores permanecen intactos bajo la nota posterior.

No nuevo build/ZIP/.dusk/DLL/manifest/config/workflow. Código compilado `107c79987b0d3d1d28319654739a72bd498271bb`; .dusk original **41419 bytes**, SHA256 `b1e8f63797e93c0064e83fc39a984c1c806d046761f675b20ac55063b6a6dfa2`. ZIP **83222 bytes**, SHA256 `e79a0e76d3471530927ca169bbe4cbe107689b36200a63119ace012d261a10a1`; DLL **77824 bytes**, SHA256 `45effe8a0ac9d56c3921c2cd6d0a27e9ea7017821559ef96b94b21ff390214e0`. [Artifact histórico](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38690126831/artifacts/11951843169), caduca 2026-11-14 01:04:00 Panamá. Hashes internos conservados del ledger histórico, no recalculados en este cierre.

**TAG_PENDING**, no TAG_SEALED. Ref humana inexistente en preflight. Cloud `environment_startup_failed`/offline; el conector tiene GitHub GET y escritura de branches/commits/PR, pero no creación de objetos tag anotados/refs tags. No se crea ni modifica ningún workflow para suplirlo. Documentación publicada por SHA es recuperable sin sello administrativo.

En un clon nuevo autorizado, con Git y gh autenticados para el repo privado, ejecutar sólo después de copiar el SHA documental literal de la respuesta/PR. Nunca usar el SHA compilado como cierre humano:

```powershell
$ErrorActionPreference = 'Stop'
$repo = 'iscoremusic26-maker/Mods-Duskligh'
$closureBranch = 'feature/devf-cp06-partial-human-runtime-closure'
$closureCommit = Read-Host 'Pegue el SHA documental completo publicado en el PR de cierre'
if ($closureCommit -cnotmatch '^[0-9a-f]{40}$') { throw 'SHA literal inválido' }
$baseCommit = '1a57ce17347d2f9c229af4c424d8b05a5ad59353'
$newTag = 'DEVF_CP06_PARTIAL_SINGLE_SITE_HUMAN_RUNTIME_OBSERVED_2026-10-15'

git fetch origin $closureBranch --tags
if ($LASTEXITCODE -ne 0) { throw 'fetch falló' }
$headCommit = git rev-parse "refs/remotes/origin/$closureBranch"
if ($LASTEXITCODE -ne 0 -or $headCommit -cne $closureCommit) { throw 'HEAD difiere: inspeccionar, no resetear' }
$parentCommit = git rev-parse "$closureCommit^"
if ($LASTEXITCODE -ne 0 -or $parentCommit -cne $baseCommit) { throw 'Padre no corresponde al baseline' }
$changed = @(git diff --name-only $baseCommit $closureCommit)
if ($LASTEXITCODE -ne 0) { throw 'diff falló' }
$expected = @('README.md','HUMAN_TEST.md','TEST_RESULTS.md','RECOVERY.md','HUMAN_RUNTIME_RESULTS_2026-10-15.md') |
  ForEach-Object { "DEVF/CP06_CONFIGURABLE_PLACEMENTS/$_" }
if (@(Compare-Object $expected $changed).Count -ne 0) { throw 'Diff fuera de los cinco Markdown' }

$remoteTag = @(git ls-remote --tags origin "refs/tags/$newTag" "refs/tags/$newTag^{}")
if ($LASTEXITCODE -ne 0) { throw 'No se pudo consultar tag remoto' }
if ($remoteTag.Count -ne 0) { throw 'Tag remoto existente: inspeccionar objeto/destino; nunca sobrescribir' }
git show-ref --verify --quiet "refs/tags/$newTag"
$localStatus = $LASTEXITCODE
if ($localStatus -ne 1) { throw 'Tag local existente o error: detener e inspeccionar' }

git tag -a $newTag $closureCommit -m 'CP06 PARTIAL single-site human observed: five cold-start trials; alternate presets, JSON disable and cold rollback; multi-instance, second site and room reentry unverified. User logs analyzed in ChatGPT; no new build.'
if ($LASTEXITCODE -ne 0) { throw 'Creación local falló' }
git push origin "refs/tags/$newTag"
if ($LASTEXITCODE -ne 0) { throw 'Push falló: conservar checkpoint; no force ni retag' }

$tagRefText = gh api "repos/$repo/git/ref/tags/$newTag"
if ($LASTEXITCODE -ne 0) { throw 'Readback ref falló' }
$tagRef = ($tagRefText -join "`n") | ConvertFrom-Json
if ($tagRef.object.type -ne 'tag') { throw 'Ref no anotada' }
$tagObjectText = gh api "repos/$repo/git/tags/$($tagRef.object.sha)"
if ($LASTEXITCODE -ne 0) { throw 'Readback objeto falló' }
$tagObject = ($tagObjectText -join "`n") | ConvertFrom-Json
if ($tagObject.object.type -ne 'commit' -or $tagObject.object.sha -cne $closureCommit) { throw 'Destino incorrecto; no modificar tag' }
$tagRef.object.sha
$tagObject.object.sha
```

Antes de informar TAG_SEALED, releer además los pares históricos por GET `repos/{repo}/git/ref/tags/{nombre}` y GET `repos/{repo}/git/tags/{objeto}`; deben ser exactamente:

| Tag histórico | Objeto anotado | Commit |
| --- | --- | --- |
| DEVF_CP06_PARTIAL_SINGLE_SITE_PRIVATE_TEST_READY | feabf5382858b0969d7f272bde0c02f91d19ab31 | 1a57ce17347d2f9c229af4c424d8b05a5ad59353 |
| DEVF_CP05_AI_BOUNDED_HUMAN_RUNTIME_OBSERVED_2026-10-15 | fc289b8c75b87ebc46ff34003f7545cfa8a60c7a | 3f6e2fc7a285dbce8cb520e0b4536ff56d542930 |
| DEVF_CP05_AI_BOUNDED_PRIVATE_TEST_READY | 83b2cea8815a8c01b29ad1f3df2a3731f7b667f4 | 7a7c8bc34841e6f85020cca93ff591e9cb9e789d |
| DEVF_CP04_4_EOC2_BLACK_HUMAN_RUNTIME_OBSERVED_2026-10-14 | f21d0d95e0fc7d5fcbca15ae17ba6b50cdee564e | f7a6623f6d931bacef6f2c8e54f46f7476780ade |
| DEVF_CP04_4_EOC2_BLACK_PRIVATE_TEST_READY | 21f9abb6b8dec176cc8b56d2652fb56a797ba45b | 0a2ec044cbae476c6ca8f3e5387737791875f47c |
| DEVF_CP03_HP150_HUMAN_RUNTIME_VERIFIED_2026-10-14 | 08ffbae5e5da73658df77b3763de2fe6851f7a45 | 139d9329f7a2d5d191b6e0ef7149ac9bbf82d29f |

No merge/rebase/amend/reset/force/retag, ni cambios en PR37 o inputs. Para recuperar sólo documentación: tras verificar el SHA, `git switch --detach $closureCommit`; no instalar/recompilar nada. La ausencia del tag no impide recuperar por SHA. Futuro multiinstancia/segundo sitio requiere autorización aparte; no se inicia ahora. No repetir los cinco ensayos ya documentados.
