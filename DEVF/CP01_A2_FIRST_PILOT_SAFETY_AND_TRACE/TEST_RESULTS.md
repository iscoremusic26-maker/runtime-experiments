# Resultados reales de esta revisión offline

Fuente principal compilada definitiva: **639d4780aeb15c17d9723babb5ff4c8d64c19a9d**. Mirror privado CI: **0b7b517ff2fdce5a0964cbc1dbd91d4a27525b28**. El checkpoint documental posterior conserva esas fuentes sin cambios. [Run final38425038752](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38425038752), job115392086716, success; únicamente pilot-offline.

| Evidencia | Resultado | Alcance |
|---|---|---|
| Nueva política/scope/monitor/traza | PASS_LAB:104 checks,0 failures | Nuevos y regresiones afectadas; no runtime |
| Reproducer focalizado del core anterior | 2/2 defectos esperados observados | Fake reentrada A/B; se cuenta separado |
| ABI oficial x64 | PASS, compilado MSVC | Header real, ninguna llamada al servicio |
| Mutaciones específicas del piloto | 7/7 compilaron y fueron detectadas | Assertion failure exit1, no crashes |
| Compilación/enlace DLL experimental | PASS | SDK2.0.3, MSVC/WindowsSDK reales |
| PE/imports/exports/meta/map/disasm | PASS_STATIC | No ejecución de la DLL |
| Integridad histórica | PASS_STATIC |277 archivos, incluyendo #16, sin modificaciones |
| Ubicación física/sesión/request/render/cleanup real | BLOCKED / NOT_VERIFIED / NOT_TESTED | Gates no elevados |

Los104 comprueban admisión NONE sin lecturas/mutaciones, Key actual con IDs variables y previous distinto de root, XZ1599.999/1600/1600.001, deltaY grande, Link/actores desconocidos o incompletos, velocidad/movimiento entre A/B/C, medio/eventos/recursos, censo/captura stale, único request, restore/throws/reentrada, ID/phase/owner/room/timeout y orden/dedup/budgets/fallo de sink. No se suman93+35 históricos ni los siete mutants anteriores. Los tests son fakes del core real generado, no el juego; los campos de public actor capture se revisan/compilan pero no se observan runtime.

Mutants nuevos: omitir XZ; usar d3; ignorar permiso de sesión; admitir truncación; omitir check C; gastar críticos en budget normal; relajar latch. Todos compilaron y produjeron FAIL específico; ver result.json y mutant-*.log. No se contabilizan fallos de compilación como detección.

## Ejecución fallida y corrección

[Run38424407438](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38424407438) compiló y enlazó, pero tuvo1 fallo entre104: la categoría LOCATION_POLICY_FAIL se repetía al pasar del estado inicial al rechazado. Corrección: dedup de categorías de política independientemente del estado previo, manteniendo eventos de transición/razones/identidades reales. No se relajó el test, el guard ni la sesión. La segunda ejecución pasó. Se conservan los ocho textos del run fallido, CRC y SHA externo verificados; no se otorgaron gates desde ese run.

El reproducer del código original muestra solicitud fake tras reentrada A/B (STOP sobrescrito). La extensión añade checks terminales tras lecturas externas y antes del latch/enqueue. Los fixtures corregidos exigen cero setters/requests. No se cambió el histórico y no se probó el defecto en el juego.

## Build y auditoría

Windows Server2025, image windows-2025-vs2026@20260925.250.1; MSVC19.51.36260.0,toolset14.51.36231,WindowsSDK10.0.26100.0,CMake4.4.3. Configure7.688s,build18.656s,job~141s. Timestamps del runner marcados UTC. Windows-latest es móvil: no se promete reproducir idéntico hash PE con otra imagen. Warnings C4068/C4805/C4806 de headers oficiales quedan registrados sin editar el SDK; avisos de deprecación de Actions no invalidaron el job.

SDK root40457c6adb381928e4b5fef6ed459ed291edd5e2, Aurora3227d76c60e1e782ca576610bce61c9e7744d8be, importlib9400986 bytes/SHA4dc4a511d761e6eb52541733fa31919a2234ed9cd5b2f16f8fea91c468f30ca4/CRC70c35731. Solo se extrae esa entrada privada; se reutiliza integridadCP00. Host no compilado, modificado ni ejecutado.

ABI ActorSpawnParams48,ActorService80,ServiceHeader8,ProfileName2,ActorId4,ModContext*8; create offset32 y room offset64. Metadata ABI1,Host2.2/Log1/Game2/Actor1; exactamente cinco exports mod_ctx/mod_meta/mod_initialize/mod_update/mod_shutdown. Los32 imports del juego son exactamente los revisados anteriormente; no hay nuevas APIs nativas. Se mantienen setter temporal y visitor de requests como mutaciones/lecturas explícitas autorizadas offline. Grafo:7 unidades de módulo +8 bridge separado; ningún fake en la DLL ni guardas READ_ONLY sobre unidades mutadoras.

La correlación del nuevo mapa identifica NativeBackend::request, la carga de svc_actor en r10 y la **única llamada** `[r10+20h]` en0x18000372F dentro de ese método. Son VAs derivados de nuestra DLL, no offsets del host. El anchor conserva el camino pese al proveedor NONE; no se sustituye ActorService por un import ficticio a fopAcM_create.

DLL experimental NO DISTRIBUIDA:121856 bytes,SHA256 `0afa4216e335a7a5bc52ee0fd4f7536ad9434fe1266b259618b8e0e44c196357`. Hash nuevo; no usar el histórico241e20c... como si correspondiera a este build. Hashes de laboratorios en result.json; stack8MiB se fija **solo para fixtures offline** con arrays, sin cambiar el host.

Comandos/fases/compile units en result.json y compile-commands.json. Reproducción offline en Developer Shell MSVCx64:

```powershell
python DEVF/CP01_A2_FIRST_PILOT_SAFETY_AND_TRACE/ci/run_windows.py --source .official --inputs . --work "$env:RUNNER_TEMP/first-pilot-offline"
```

CMake Ninja Release genera el overlay y construye devf_first_pilot_experiment, pilot_safety_trace_lab, pilot_native_abi_lab y pilot_baseline_reentry_reproducer. Solo se ejecutan EXE fake/ABI; no DLL ni host. No add_mod/mod.json/package/install ni .dusk.

Artefacto textual final:164542 bytes,SHA256 `e025aa525e6a9fefd1602ab4f056615977fdfa5b960e9fca608907e938fa7177`;31 archivos .log/.json,CRC y30 hashes internos verificados. [Descarga privada real](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38425038752/artifacts/11828313049), caduca2026-11-12 15:49:38UTC. Todo el texto queda versionado en evidence/windows-run-38425038752;19 entradas de fuentes nuevas,21 fuentes reutilizadas y siete overlays contrastados con la copia local, incluido su hash normalizado entre plataformas. El run fallido ZIP12970 bytes SHA3457d5fdc087c1d48873e27ab6656e6025e7fb748498e163ee357bb985b87728 también queda identificado. No se descargó ningún binario del job.

Sin repetir SDKLinux, suites históricas93/35/92/99, análisis ARC/KCL/Dawnlight ni auditorías generales de lifetime. No se recuperó ni publicó el log privado del usuario.
