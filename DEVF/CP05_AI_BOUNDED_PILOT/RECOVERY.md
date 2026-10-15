# CP05 — Recuperación y handoff

> **Actualización documental posterior (2026-10-15 Panamá).** Nueva rama documental hija feature/devf-cp05-ai-bounded-human-runtime-closure desde7a7c8bc34841e6f85020cca93ff591e9cb9e789d. Paquete/refs históricos intactos. Tag humano nuevo TAG_PENDING por falta de shell/API compatible; comandos exactos al final de este documento. Ver [informe humano y límites](HUMAN_RUNTIME_RESULTS_2026-10-15.md). Las afirmaciones HUMAN_RUNTIME_NOT_TESTED y pasos de prueba siguientes conservan el estado histórico al preparar el TEST; no se reescriben código, logs ni paquete.

Rama feature/devf-cp05-ai-bounded-pilot, PR34 draft/no merge, base humana exacta f7a6623f6d931bacef6f2c8e54f46f7476780ade. Checkpoint temprano c01bb2e9e0da87905f703929b516de05b4c6ae78. Los resultados reales posteriores y sus SHA están registrados abajo.

CP04.4 humano TAG_SEALED: DEVF_CP04_4_EOC2_BLACK_HUMAN_RUNTIME_OBSERVED_2026-10-14, objeto f21d0d95e0fc7d5fcbca15ae17ba6b50cdee564e, destino f7a6623f6d931bacef6f2c8e54f46f7476780ade; API readback, run38671493020 SUCCESS, PR33 tag-only sin merge. El informe histórico f7 conserva honestamente el bloqueo que existía entonces.
PRIVATE_TEST_READY objeto21f9abb6b8dec176cc8b56d2652fb56a797ba45b→0a2ec044cbae476c6ca8f3e5387737791875f47c; CP03 objeto08ffbae5e5da73658df77b3763de2fe6851f7a45→139d9329f7a2d5d191b6e0ef7149ac9bbf82d29f. No mover refs.
CP04 .dusk15287 SHA a1b1e750575253c8ec33193c385240337b8f1d5db6f3e9389fba08683c6d97f9; ZIP45231 SHA e7b05803b687324c6f5eace8d3e2954b7e5b26d819f05e7de7d03bf5c2a8ca49. Artifact11936739368 vence2026-11-13T23:59:41Z. No recompilación ni sustitución de CP04.4.

Clonar nuevo directorio y fetch rama CP05 y tags; switch --detach al SHA concreto publicado en PR/chat, nunca reset/force/amend/merge. No repetir ARC/render/CP01–04. El único scope adicional toca mPlayerRange con restore por actor; fuente propia nueva en esta carpeta. CI/inputs privados separados cuando se ejecute, no recursos propietarios en entrega. Cloud sigue offline; no se simula shell local.

Tag técnico CP05: DEVF_CP05_AI_BOUNDED_PRIVATE_TEST_READY, sin nombre HUMAN_RUNTIME_VERIFIED ni release; su existencia y objeto se confirman por API/PR al finalizar. CP06/expansión no iniciados. Ver TEST_RESULTS para los gates actuales; si queda CI bloqueado preservar este SHA y corregir sólo wrapper/config/AI correspondiente, no fuente oficial.

## Resultado posterior y recuperación exacta

CP05_AI_BOUNDED_PRIVATE_TEST_READY, HUMAN_RUNTIME_NOT_TESTED. Fuente compilada `ec61daa3ed7d539989028cd26b22fa529896de11`, CI `efd8a49ec7b4bcb444bf510c5a9173a92386ce97`; [build38672691356](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38672691356), [descarga38672879974](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38672879974). El commit documental final se entrega literalmente en PR/chat: no confundirlo con la fuente compilada.

[Artifact TEST11945045896](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38672691356/artifacts/11945045896), ZIP52452/SHAc5df6dcbd0f440e096c5c4048f2c3c97476ed6cb1234c9587e2df0a6317914bc; .dusk18929/SHA23f81ad131082a03fcd66068ccd926ecf878182a5afce06244898cf663248ddb; DLL34816/SHA830577e71543301f5ca672094caeb5c54103d61e85a23f01e2ba39074565f509. Caduca2026-11-13 21:46:49 Panamá. Referencias completas en BUILD_AND_PACKAGE y JSON derivados. Tag técnico se publica por workflow aislado al cerrar este checkpoint; leer objeto/destino remoto antes de asumirlo. Commit y PR34/inputsPR23 recuperables, sin merge.

```powershell
git fetch origin feature/devf-cp05-ai-bounded-pilot --tags
git switch --detach ec61daa3ed7d539989028cd26b22fa529896de11
git rev-parse HEAD
```

Esto recupera la fuente realmente compilada. Para los informes finales, usar el SHA documental literal publicado en PR34/chat. No reset sobre otro trabajo. El bundle contiene fuente/ledger del build exacto; no depender sólo de artifacts que caducan.

Para reanudar no repetir gate de tag CP04 (ya TAG_SEALED), ARC/render ni laboratorio sin cambios. Únicamente prueba humana CP05 conforme HUMAN_TEST, salvo fallo concreto nuevo. Conservación baseline verificada por árbol Git completo; no mutaciones en PR31/32, CP03 o CP04. No nuevo juego ejecutado por Codex. Rollback CP05: juego cerrado, retirar sólo nuevo mod y arranque frío; CP04 original puede restaurarse sin recompilar.

El workflow nuevo .github/workflows/devf-cp05-ai-pilot-tag.yml sólo ejecuta el sello técnico de esta rama/PR34 privada, comprueba ascendencia/documentos/grafo compilado y refs históricos y empuja un único tag anotado inexistente, sin force. No build ni scripts host; no workflow histórico editado. Target final y objeto se publican literalmente tras readback en PR34/chat. La clave RELEASED indica retiro del seguimiento AI por ausencia o eliminación nativa encolada (state3), no prueba de liberación de cada allocation del host.

## Cierre humano 2026-10-15 — recuperación documental

Dictamen y procedencia: [HUMAN_RUNTIME_RESULTS_2026-10-15](HUMAN_RUNTIME_RESULTS_2026-10-15.md). HOME_RETURN_WALKING_NOT_VERIFIED;30_UPDATE_GRACE_NOT_DIRECTLY_VERIFIED;CP05_ROLLBACK_PENDING;SAME_MODEL_EOC2_SIMULTANEOUS_PENDING. El cese de persecución no acredita caminar de regreso. No se solicita repetir gameplay.

La rama técnica y tag83b2cea8815a8c01b29ad1f3df2a3731f7b667f4→7a7c8bc34841e6f85020cca93ff591e9cb9e789d permanecen intactos. El nuevo SHA documental se entrega en el PR draft separado y en chat, con lectura remota positiva; la fuente compilada sigue ec61daa3ed7d539989028cd26b22fa529896de11. No recompilar ni reempaquetar.

### Tag humano: TAG_PENDING

Nombre reservado, no creado: DEVF_CP05_AI_BOUNDED_HUMAN_RUNTIME_OBSERVED_2026-10-15. Cloud offline/environment_startup_failed, sin shell; conector sin create_tag/create_ref para tags. El workflow existente sólo sella PRIVATE_TEST_READY desde la rama técnica y no se altera ni ejecuta para este cierre.

En un clon nuevo/autorizado, estos comandos PowerShell recuperan la rama documental, resuelven su SHA y preparan únicamente el tag. Contrastar el SHA obtenido con el literal publicado en PR/chat antes de crear nada:

```powershell
git fetch origin feature/devf-cp05-ai-bounded-human-runtime-closure --tags
if ($LASTEXITCODE -ne 0) { throw 'Fetch falló' }
$closureCommit = git rev-parse refs/remotes/origin/feature/devf-cp05-ai-bounded-human-runtime-closure
if ($LASTEXITCODE -ne 0) { throw 'Commit documental no recuperado' }
Write-Output $closureCommit
# Contrastar exactamente con el SHA documental de PR/chat.
git show --stat --oneline $closureCommit
$parent = git rev-parse "$closureCommit^"
if ($LASTEXITCODE -ne 0 -or $parent -ne '7a7c8bc34841e6f85020cca93ff591e9cb9e789d') { throw 'Base distinta; detener y recuperar el SHA literal del PR' }
$newTag = 'DEVF_CP05_AI_BOUNDED_HUMAN_RUNTIME_OBSERVED_2026-10-15'
$existing = @(git ls-remote --tags origin "refs/tags/$newTag")
if ($LASTEXITCODE -ne 0) { throw 'No se pudo comprobar ref remota' }
if ($existing.Count -ne 0) { throw 'Tag remoto existente: inspeccionar objeto/destino, no sobrescribir' }
git show-ref --verify --quiet "refs/tags/$newTag"
$tagCheck = $LASTEXITCODE
if ($tagCheck -ne 1) { throw 'Tag local existe o comprobación falló; detener' }
git tag -a $newTag $closureCommit -m 'CP05 Windows/DX12 human observed: close detection and pursuit cessation reported; two sequential generations HP150-to-zero; walking home,30-update grace,cold rollback and identical same-frame EOC2 control not verified. Documentary only; original dusk unchanged.'
if ($LASTEXITCODE -ne 0) { throw 'Creación de tag anotado falló' }
git push origin "refs/tags/$newTag"
if ($LASTEXITCODE -ne 0) { throw 'Push sin force falló; no reintentar sobrescribiendo' }
git ls-remote --tags origin "refs/tags/$newTag" "refs/tags/$newTag^{}"
```

Después leer por GitHub API:
`GET /repos/iscoremusic26-maker/Mods-Duskligh/git/ref/tags/DEVF_CP05_AI_BOUNDED_HUMAN_RUNTIME_OBSERVED_2026-10-15`;
la ref debe tener object.type=tag. Leer su object.url; el objeto anotado debe apuntar exactamente a $closureCommit, tipo commit. Revalidar los objetos/destinos históricos CP05 técnico, CP04 humano, CP04 TEST y CP03. Sólo entonces declarar TAG_SEALED. No force, retag, amend, reset ni merge.

Si sólo se necesita recuperar la documentación, usar fetch y `git switch --detach <SHA documental literal del PR/chat>`; no hace falta completar el tag para conservar el trabajo. El artifact original mantiene18929bytes/SHA23f81ad131082a03fcd66068ccd926ecf878182a5afce06244898cf663248ddb; vence2026-11-13 21:46:49 Panamá. No se sustituye tras caducidad sin una tarea nueva autorizada.

**CP06 no iniciado; esperar autorización expresa**. Editor/Bokoblin Expansion y cambios de IA fuera de alcance.
