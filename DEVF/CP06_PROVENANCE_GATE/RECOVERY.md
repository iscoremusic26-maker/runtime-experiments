# Recuperación exacta y decisión pendiente

Rama nueva `feature/devf-cp06-register-edit-provenance-gate`; [PR40 draft](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/40), base literal `d9a776567c9cb999118d6ef29dd34c99f4664085`.
Cadena verificada d9a7765…→a94eba4…→db254b9…→3ab8ff2…→1a57ce17…; ramas/PR históricos no se modifican.

Checkpoints nuevos:
- Inicial9eee5b975d8d43df79693e98337b826b194a9ee9: fuente del primer probe.
- Fuente/evidencia final **503521e41111c9556daba703d3bb8cc18dc44b3e**: script corregido y resultado real; ninguna fuente de mod compilada.
- SHA documental final completo se publica en PR40/respuesta tras readback; no es hash de un .dusk.
- CI inputs: rama ci/devf-cp06-register-edit-provenance-gate, [PR26 draft](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/26), HEAD9b4930b3bab0a6437b17ce99e3f232f724823a5f desde98bbb027c91e4cabc9629f370971345c887a958c. Run38749877215/job116473164418 SUCCESS, fuente efectiva distinta de GITHUB_SHA merge temporal6f6a462263e5562a13f2bc851cdf3dedb1b108ef.

## Recuperar sin repetir investigación ni gameplay
En clon privado autorizado:
```powershell
git fetch origin feature/devf-cp06-register-edit-provenance-gate --tags
if ($LASTEXITCODE -ne 0) { throw 'Fetch falló' }
$checkpoint = Read-Host 'SHA documental completo publicado en PR40'
if ($checkpoint -cnotmatch '^[0-9a-f]{40}$') { throw 'SHA inválido' }
git merge-base --is-ancestor d9a776567c9cb999118d6ef29dd34c99f4664085 $checkpoint
if ($LASTEXITCODE -ne 0) { throw 'Base incorrecta' }
git switch --detach $checkpoint
if ($LASTEXITCODE -ne 0) { throw 'Checkpoint no recuperable' }
git rev-parse HEAD
```
Para reproducir la medición sólo si se requiere: en inputs autorizado checkout9b4930b3…; ejecutar el workflow propio existente o sus pasos (MSVC x64 dev-cmd, LFS selectivo ZIP Windows, Python ci/inspect_transfer_symbol.py). Requiere red PyPI para zstandard0.25.0 con hash de wheel registrado y raw.githubusercontent.com para api.h exacto con git-blob verificado. No clonar/reconstruir host ni abrir juego. Source y metadata ya preservadas: no hace falta otra ejecución para aceptar este NO-GO.
Cloud siguió environment_startup_failed/offline, pero CI y API permitieron las pruebas; no se atribuye a Cloud un shell usado. No se ejecutaron hooks en el host.

## Estado de cierre
P0 PASS, P1 PASS estático del límite opaco, P2 NO_GO para owner/handle→buffer bajo interfaces y restricciones actuales, P3 NOT_RUN. No leer offsets STL ni convertir rvalue-temporal en allocation. No inventar traza A/B ni ampliar max_active.
Opciones concretas y sus permisos en ARCHITECTURAL_OPTIONS: ninguna alternativa .dusk-only de procedencia completa validada; extensión StageService/SDK sólo propuesta, requiere autorización explícita por implicar host distinto; o conservar single-site intacto. No cambiar EXE automáticamente.
SITE2_PENDING heredado, sin repetir sus consultas. No nuevo mod/TEST; **NO PROBAR NADA**. CP07/08/Posture/Expansion no iniciados.

## Referencias inmutables
Tag humano CP06 parcial DEVF_CP06_PARTIAL_SINGLE_SITE_HUMAN_RUNTIME_OBSERVED_2026-10-15: objeto5b9f28473654e26efe9514d0e2543b561511f3b3→3ab8ff2fdd42128ab75157338699b21ae6d768bd, ya sellado; no tocar.
Tag técnico feabf5382858b0969d7f272bde0c02f91d19ab31→1a57ce17347d2f9c229af4c424d8b05a5ad59353. Seis referencias previas en SOURCE_MANIFEST.
Rollback humano CP06 single-site0.6.0 sigue **41419bytes**, SHA256 b1e8f63797e93c0064e83fc39a984c1c806d046761f675b20ac55063b6a6dfa2; fuente compilada107c79987b0d3d1d28319654739a72bd498271bb.
No recompilación/reempaquetado/descarga binaria del .dusk. El EXE de host sí se leyó offline para ABI, sin modificarlo ni ejecutarlo, exclusivamente desde input aprobado.
