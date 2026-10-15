# Recuperación y rollback

Base: **9c3ce7cc4fefec1855b1e014630326005c6f4556**. Rama **feature/devf-cp06-native-north-dual-qa**, [PR41 draft](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/41), sin merge.

Checkpoint inicial: **03ed8d1a4dcc28dd0b58ec2a4b60a3ec86be2035**.  
Fuente realmente compilada: **689f79c1c785bea31715d814f7d03818a7f0dd72**.

El SHA documental final, publicado tras readback en PR41 y en la respuesta, es distinto del compilado. Las docs posteriores no se insertaron retroactivamente en SOURCE_COMPILED.zip ni en los paquetes.

CI/inputs: rama **ci/devf-cp06-native-north-dual-qa**, [PR27 draft](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/27), base **9b4930b3bab0a6437b17ce99e3f232f724823a5f**.

- Build CI **08a5f4d952665bcc223b1b3feda37ac7ff23acdf**, [run 38755215665](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38755215665).
- Verificación CI **35221fa0593522ef3c17d7d89ea31afd4ebe2642**, [run 38755609469](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38755609469).
- El workflow nuevo actual sólo verifica descarga; su versión de build es recuperable en el commit 08a5f4d… No se modificaron workflows históricos.
- El checkout real se registra explícitamente. SDK oficial 40457c6… intacto; no se compiló ni empaquetó host, Aurora o importlib.

En un clon privado autorizado:

```powershell
git fetch origin feature/devf-cp06-native-north-dual-qa --tags
if ($LASTEXITCODE -ne 0) { throw 'Fetch falló' }
$checkpoint = Read-Host 'SHA documental completo publicado en PR41'
if ($checkpoint -cnotmatch '^[0-9a-f]{40}$') { throw 'SHA inválido' }
git merge-base --is-ancestor 9c3ce7cc4fefec1855b1e014630326005c6f4556 $checkpoint
if ($LASTEXITCODE -ne 0) { throw 'Base incorrecta' }
git switch --detach $checkpoint
if ($LASTEXITCODE -ne 0) { throw 'Recuperación falló' }
git rev-parse HEAD
```

Para la fuente del artifact usar **689f79c1c785bea31715d814f7d03818a7f0dd72**. No recompilar para sustituir el TEST ya verificado. [BUILD_AND_PACKAGE](BUILD_AND_PACKAGE.md) y evidence/ conservan ledger, hashes y miembros. Los artifacts caducan el 2026-11-14 según API; no se promete disponibilidad posterior. Cualquier redistribución futura necesitará verificar sus propios bytes.

Cloud no estuvo operativo; las operaciones reales se realizaron mediante GitHub y Actions, sin atribuir ejecución a un shell local inexistente.

## Uso y reversión

Seguir [HUMAN_TEST](HUMAN_TEST.md): A primero; B sólo tras A satisfactorio. Sin JSON, un solo .dusk DEVF. Cierre completo al cambiar o retirar QA: remove_actor_edit no destruye actores vivos.

Rollback histórico CP06 v0.6.0: **41419 bytes**, SHA256 **b1e8f63797e93c0064e83fc39a984c1c806d046761f675b20ac55063b6a6dfa2**, intacto, con su JSON original conservado.

Tag humano histórico: objeto **5b9f28473654e26efe9514d0e2543b561511f3b3** → **3ab8ff2fdd42128ab75157338699b21ae6d768bd**. No retag, merge, rebase, reset, amend, force ni cambios a PR37–40.

## Próximo paso

Recibir observación visual y log privado de A: aparición, asentamiento, terreno y anomalías. Si falla, detener B y corregir sólo el problema concreto. Si pasa, B permite comprobar dos adicionales nativos y su ciclo de vida. No repetir los cinco ensayos anteriores.

Personalización por instancia **PENDIENTE**, independiente de estas altas nativas. No se implementó una nueva estrategia de identidad ni se cambió el host/SDK. CP06 general continúa parcial. CP07/08, postura y Bokoblin Expansion no iniciados.
