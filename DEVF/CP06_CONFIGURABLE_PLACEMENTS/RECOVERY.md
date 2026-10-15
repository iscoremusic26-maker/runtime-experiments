# CP06 — Recuperación exacta / handoff

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
