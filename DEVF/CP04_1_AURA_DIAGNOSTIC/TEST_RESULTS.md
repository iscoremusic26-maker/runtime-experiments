# CP04.1 — Windows y resultado final

**DIAGNOSTIC_ONLY_HUMAN_TEST_PENDING; NO-GO para apariencia.** No hay causa exacta probada del rechazo humano anterior. CP03_HUMAN_RUNTIME_PASS sigue vigente. No CP05/CP06.

|Comprobación|Estado y evidencia|
|---|---|
|Rechazo v0.4.0|FAIL_RUNTIME_AURA (extracto confirmado/humano); raw log no revisado ni publicado|
|Todos los retornoscreate, orden deguards y carga normal del banco|SOURCE_VERIFIED; DIAGNOSIS/SOURCE_MANIFEST|
|Contenido/propiedades reales0x029D|NOT_VERIFIED — common.jpc ausente|
|Causa concreta original|BLOCKED por motivoRAM discriminante ausente|
|14 escenarios afectados en Windows|OFFLINE_TEST_PASS; fake-*.log, sin motor/render|
|18 fallos precisos +4 éxitos factory/entry|OFFLINE_TEST_PASS, misma plantilla create_checked; fake-native RAM|
|32.768 combinaciones del predicate anterior|OFFLINE_TEST_PASS, aceptaciónidéntica inclNaN/±inf/bounds|
|Un intentoyunREJECTED tras1000 frames por18motivos|OFFLINE_TEST_PASS, fault enclavado sin retry|
|OriginalE_OC2/E_OC40 excluidos; keyreciclada/cleanup/recarga/shutdown|OFFLINE_TEST_PASS, doubles; no píxeles/motor|
|RegistroStage anterior|OFFLINE_TEST_PASS_REUSED38584533623, función/headers/log exactos; no rerun|
|Compilación/enlaceMSVC x64|BUILD_PASS en una ejecución|
|PE AMD64/ABI1/5exports/HostLogGameStageHook/únicoexecute|PASS estático, 38imports exactos iguales aCP04|
|PEnegativos x86/HookServiceID/target/export|PASS:4rechazados, ningunaDLLcargada|
|SDKpackage/DLL internaequaloose/modjsonv0.4.1|PACKAGE_VERIFIED|
|Descarga realTEST/TEXT/CRC/hashes/18 archivosledger/PE|DOWNLOAD_VERIFIED|
|Render/aislamiento de E_OC2original/combate/muerte/reentrada/reversiónCP04.1|NOT_TESTED|
|AparienciaCP04|NO-GO|
|Hostcompilado/juegocorrido/DLLcargada/instalaciónCodex|NO en todos|

[Run 38593704059](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38593704059), job 115954866399, CI`da07f77fddd13ca1664997e5373f3dfe988cf7e1`, fuente compilada`554c31a3e10906c50dd18a05fe0b55737bf5a3a8`. MSVC 19.51.36260, VCTools14.51.36231, Windows SDK 10.0.26100.0, CMake 4.4.3, Ninja Release. Scriptinicio2026-10-14T15:56:48.629636+00:00, fin2026-10-14T15:57:13.260823+00:00:24.631s; excluye setup/upload. No hubo intento fallido o recompilaciones ciegas. Las advertenciasC4805/C4806/C4068 proceden de headers oficiales intactos; C4722deltripwireGXDestroyTexObj es solo TEST_FAKE/abort. No errores. Unidadesproductivas:mod.cpp propio +game_feature.cppSDK; test/tripwire ajenos aDLL.

Logs/cmd/tiempos: [result.json](evidence/windows-run-38593704059/result.json), [build](evidence/windows-run-38593704059/build.log), [lab-build](evidence/windows-run-38593704059/lab-build.log), [18gates](evidence/windows-run-38593704059/fake-typed_native_create_branches.log), [predicate](evidence/windows-run-38593704059/fake-resource_reason_boundaries.log), [binary-audit](evidence/windows-run-38593704059/binary-audit.json), [download](evidence/download-verification.json). LogsWindows propios conservados byteexactos con ledger, no logs personales del juego. Todas las etiquetasTEST_FAKE significan doubles, nunca validación nativa runtime.

Recurso 0x029D, aceptación/refresh/cleanup idénticos: este paquete solo resuelve la falta de observabilidad. Una prueba mínima [HUMAN_TEST](HUMAN_TEST.md) debe entregar el primer gate de esta sesión. APPLIED no acredita píxeles. No descartar/elegir otra técnica antes de esa evidencia.
