# Recuperación exacta y rollback

Base inmutable: **89dad44ca07ddd414e946e6d910371b9b7a1e7a3**. Rama nueva **feature/devf-cp06-json-dual-native-qa**, [PR42 draft](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/42), sin merge. Carpeta nueva DEVF/CP06_NATIVE_CONFIG_DUAL/. El checkpoint documental final se publica por SHA completo en PR42/respuesta después de readback; no es la fuente compilada.

## Identidades separadas

- Primera fuente0182b51eb7029d52468993a493b6d0664e6e764b, CI4ed8e08913a5cde42418050c62cd5fed3d008011: run38761708755 FAILURE por escape NUL en negativo Python; compilación/109casos sí pasaron, no paquete entregado de esa ejecución.
- **Fuente realmente compilada del TEST: a4b72680d7a6e0e360f52aef1b3a4554150c78a9**.
- **Build CI: af07099fbcffdfca1fae2c8280237c25c079b131**, [run38761953150](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38761953150) SUCCESS.
- **Verificador CI: a9aabade816e8ea366b6f74a2cd731723a762ec1**, [run38762282880](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38762282880) SUCCESS, descarga real independiente.
- CI rama **ci/devf-cp06-json-dual-native-qa**, [PR28 draft](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/28), base35221fa0593522ef3c17d7d89ea31afd4ebe2642. Workflow nuevo actual download-only; su versión de build se recupera en el commit af07099f…. No workflows históricos modificados.
- Se registra checkout real; merge-event SHA sólo es metadato. SDK40457c6… oficial intacto; no host/Aurora/importlib build.
- Mod **dev.devf.cp06_native_config_dual**, versión **0.6.2**: .dusk28803bytes/SHA2562658f7771344e9334219b1416bdbd9ca97cf817b28300c7d347da8e0454c48bb. ZIP64772bytes/SHA256fdc7b9e48f54e734e3272fc41b7eca75ca0227d5792e829357e2e929803ec92d. DLL54272bytes/SHA256e1cb5eb685efd1fc4d1950ea0f7b6aa3d3a1fcb7484ccf9902b373821d3c552d.
- Artifact11986995345, nombre DEVF_JSON_DUAL_NATIVE_TEST_38761953150. [Descarga](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38761953150/artifacts/11986995345); caduca2026-11-14 10:38:36 Panamá. Si la URL profunda falla, abrir Artifacts del run con acceso privado. No promesa tras vencimiento.

## Recuperación Git sin sobrescrituras

```powershell
git fetch origin feature/devf-cp06-json-dual-native-qa
if ($LASTEXITCODE -ne 0) { throw 'Fetch falló' }
$checkpoint = Read-Host 'SHA documental final completo publicado en PR42'
if ($checkpoint -cnotmatch '^[0-9a-f]{40}$') { throw 'SHA inválido' }
git merge-base --is-ancestor 89dad44ca07ddd414e946e6d910371b9b7a1e7a3 $checkpoint
if ($LASTEXITCODE -ne 0) { throw 'Base incorrecta' }
git switch --detach $checkpoint
if ($LASTEXITCODE -ne 0) { throw 'Checkout falló' }
git rev-parse HEAD
```

El código empaquetado se recupera específicamente desde a4b72680d7a6e0e360f52aef1b3a4554150c78a9/SOURCE_COMPILED.zip. Las docs de cierre no se insertan retroactivamente en el paquete. No recompilar para sustituirlo. Ledger/CRC/hashes/miembros y errores conservados en evidence/. No tags nuevos ni retag, force, amend, rebase, reset o merge.

## Preservación y siguiente paso

Native records idénticos a QA B. Parser/IO adaptados sólo en copia nueva; registro usa máscara validada field/north. Runtime real se comparte con laboratorio. No punteros/IDs de actores, hooks o callbacks retenidos.
Los 1389 archivos anteriores del principal y 71 del CI base siguen iguales por blob/mode/type; la comprobación final y refs se registran en PR42. CP06v0.6.0 permanece41419bytes/SHA256b1e8f63797e93c0064e83fc39a984c1c806d046761f675b20ac55063b6a6dfa2; QA A/B, tags y PR37–41 intactos. No host, SDK, Aurora, EXE, ROM, saves o assets alterados/distribuidos.

Cloud offline: operaciones Git por conector y ejecución por Actions, sin shell local fingido. Nada se instaló en el PC del usuario.
Próximo paso: probar la versión nueva con BOTH y luego, si se desea completar los cuatro modos, FIELD/NORTH/NONE cerrando entre ejecuciones. Sin JSON no aparecen adicionales. No repetir terreno A/B ni cinco ensayos históricos. Manual HUMAN_TEST.md.
Rollback frío retirando únicamente el nuevo .dusk; puede restaurarse después el CP06 histórico y su JSON. remove_actor_edit retira ediciones, no actores vivos. CP06 general/personalización pendientes; CP07/08/Posture/Expansion fuera de alcance.
