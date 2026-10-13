# Resultados verificables — 13 de octubre de2026, UTC−5

**PASS offline**, sin prueba del juego. Fuente principal compilada: `1f184e56b66bef014601419a5c9078f16e112944`; mirror CI `7a33a26b084aed794108d281d5cad84de7d69d37`. El checkpoint final añade documentación/evidencia sin cambiar esas fuentes. [CI real](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38414957463), job115356817967, un único run, success; ninguna corrección de build ni rerun necesarios.

| Comprobación | Resultado | Evidencia |
|---|---|---|
| Nuevo request/scope/monitor core fake | PASS_LAB:93 checks,0 failures | first_request_lab.log |
| Equivalencia del predicado Owner contra A2 real | PASS_LAB:35 fixtures,0 failures | first_equivalence_lab.log |
| ABI oficial Winx64 | PASS_STATIC/compilado MSVC | first_abi_lab.log |
| Mutaciones semánticas | PASS_LAB:7/7 compilaron y fueron detectadas por assertions; exit1 esperado | mutant-*.log/result.json |
| MSVC Release + import library exacta | PASS:compilación/enlace | build.log/configure.log |
| PE/metadata/exports/imports/map/disasm | PASS_STATIC del módulo experimental | module-*.log, correlación slot32 |
| Admission nativa | NONE_ALWAYS; sin interfaz de armado | source audit/admission.cpp |
| Histórico/SDK/Aurora | PASS_STATIC:sin cambios | ledger de CI + historical-unchanged.json |
| Request/creación/render/colisión/limpieza real | NOT_TESTED | No host iniciado ni DLL cargada |
| READY de recursos/GPU | NOT_VERIFIED | REGISTERED no READY |
| Ubicación formal/lifetime/unloading | BLOCKED/NO-GO | GATE_DECISION.md |

Los siete mutants: omitir restauración; doble enqueue; seleccionar ownerLink; READY desde MOD_OK; ignorar IDincorrecto; rearmar tras timeout; ignorar transición. Ninguno se contabiliza como detectado por error de compilación o crash. Los tests prueban la respuesta del core a evidencia sintetizada, no la fidelidad completa del motor ni detección generacional universal.

ABI real: ActorSpawnParams48,ActorService80,ServiceHeader8,ProfileName2,ActorId4,ModContext*8 bytes. Create offset32,room offset64; no sizeof del opaco ModContext. Firma y tipo de punteros del header oficial; callbackNULL. Módulo:cinco unidades de integración+nuevo puente readonly de siete, sin fakes y sin guardas históricas sobre los mutadores. Se retienen anchor, setter y visitor; la correlación map/disasm identifica exactamente svc_actor y la única llamada slot32 dentro de NativeBackend::request, no una llamada virtual cualquiera.

Windows Server2025, image windows-2025-vs2026@20260925.250.1, MSVC19.51.36260.0,toolset14.51.36231,WindowsSDK10.0.26100.0,CMake4.4.3. Configuración5.969s,build15.734s,pipeline40.304s,job~95s. Las versiones reales se registran; windows-latest es una imagen móvil y no promete el mismo hash PE en una reconstrucción futura. Warnings oficiales C4068/C4805/C4806 se conservan sin modificar headers; avisos de deprecación Node en Actions no invalidaron el job. Sin errores de build.

Comandos completos/versiones/fases en `evidence/windows-run-38414957463/result.json` y compile-commands.json. Target intencional EXCLUDE_FROM_ALL, sin add_mod/mod.json/package.

```powershell
python DEVF/CP01_A2_FIRST_NATIVE_REQUEST_OFFLINE/ci/run_windows.py --source .official --inputs . --work "$env:RUNNER_TEMP/first-native-offline"
# Internamente: CMake Ninja Release con cl, SDK exacto e importlib verificada.
# build --target devf_first_native_experiment first_request_lab first_equivalence_lab first_abi_lab --parallel 2
# Solo se ejecutan los tres laboratorios nuevos; la DLL nunca se carga.
```

DLL experimental NO DISTRIBUIDA:57344 bytes,SHA256 `241e20c95267d3aa4e204420a8a600013aeeb6976f9efa3863728d123ecf4306`. Los hashes de EXE de laboratorio constan en result.json. Ningún binario se descargó de CI ni se añadió al código.

ZIP de evidencia textual:109198 bytes,SHA256 `39ed3ea1f41b9cf6ca0155a71504ed5e6e37d35e8834e771f95ed18bf257fa1f`;29 entradas .log/.json,CRC completos y28 hashes internos verificados. [Artefacto privado real](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38414957463/artifacts/11824545435), caduca12nov2026 14:39:06UTC; todo el texto descargado queda también en Git. Importlib9400986 bytes,SHA4dc4a511d761e6eb52541733fa31919a2234ed9cd5b2f16f8fea91c468f30ca4,CRC70c35731;se reutiliza integridadCP00,solo se lee esa entrada.

No se repitieron suites históricas92/99, auditorías de ubicación/ARC ni SDKLinux. Las13 capturas runtime se preservan como extracción explícita del usuario; no se recuperó ni publicó su log privado. No acreditan este request experimental.
