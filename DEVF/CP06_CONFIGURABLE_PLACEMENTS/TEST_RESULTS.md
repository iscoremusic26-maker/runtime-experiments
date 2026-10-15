# CP06 — Resultados reales y límites

> **Estado documental posterior a la build (2026-10-15): CP06_PARTIAL_HUMAN_RUNTIME_OBSERVED.** [Cinco pruebas humanas y límites](HUMAN_RUNTIME_RESULTS_2026-10-15.md): presets alternativos en frío, desactivación JSON y rollback CP06 observados; sigue CHECKPOINT_CP06_PARTIAL, sin segundo sitio ni multiinstancia. El texto original que sigue conserva el estado histórico al compilar; no se modificó el .dusk ni se repitieron builds/pruebas. Procedencia de logs: USER_LOG_ANALYZED_IN_CHATGPT; observaciones: USER_HUMAN_REPORTED. Tag humano TAG_PENDING; [recuperación](RECOVERY.md#cierre-humano-documental-2026-10-15).

**CHECKPOINT_CP06_PARTIAL**, no MVP completo. Fuente compilada107c79987b0d3d1d28319654739a72bd498271bb; [build](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38690126831), [descarga real](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38690375002).

| Gate | Resultado | Evidencia / límite |
| --- | --- | --- |
| Catálogo/schema/parser | PASS OFFLINE30 | Core real config_core.hpp usado por DLL y laboratorio; schema1,IDs únicos,presets distintos,tipo/clave/versión/rangos/size/profundidad/encoding/duplicados/referencias. |
| IO externo y persistencia entre lecturas | PASS OFFLINE / SOURCE_VERIFIED | Mismo config_io.hpp; Windows files reales vía FileService fake, editarpreset/yaw/retirar/releer;data_dir persistente/join fundamentados en host/Borealis exactos. Backend del juego NOT_TESTED. |
| Fallos IO/parse/close/partialconfig | PASS OFFLINE | Missing/nullAPI/oversize/readcorto/error/cierre/archivo vacío; Config sólo se publica tras validar todo; ninguna alternativa de spawn. |
| Identidad/policy | PASS OFFLINE + fuente | Record completo,retail excluido,admisiónúnica/reentrada/IDreciclado/concurrenciarechazada. Un solo activo; no garantía multiinstancia/sceneepoch general. |
| Rutas de2presets | PASS CORE / NATIVE_RUNTIME_NOT_TESTED | flags reales hp150/black/guard vs220/no flags; DLL condicionalmente no escribeHP ni instala render ni admite AI en presetnative. No prueba de píxeles/combate nuevos. |
| MSVC AMD64 | BUILD_PASS | run38690126831,job116273859695; cl19.51.36260,VCTools14.51.36231,SDK10.0.26100.0,CMake/Ninja. |
| PE/ABI/imports/exports | PASS |9metadata records/6servicios,2PMFs8bytes unidos a IATexacto,5exports; sinTLS/delayimports; gameimports iguales aCP05. FileService1.0 y CRT revisados estrictamente. |
| Negativos binario/paquete | PASS7 | x86,target,HookService,FileService,export,ARCextra,traversalZIP rechazados; ninguna DLL mutada ejecutada. |
| PaqueteSDK | PACKAGE_VERIFIED |.dusk41419; manifest/DLL idénticos,miembros/CRC/hash comprobados. |
| Descarga nueva independiente | DOWNLOAD_VERIFIED | run38690375002,job116274633220;ZIP exterior/SourceZip/dusk/manifest/DLL/PE/SHA/CRC/ledger reales, sin rebuild/game. |
| Fuente principal↔CI | REPO_VERIFIED |28blobs del commit compilado idénticos al espejo por objeto Git;1309entradas baseline conservadas. |
| GateA moverubicaciones sin compilar | NOT_IMPLEMENTED / BLOCKED_BY_SITE_EVIDENCE | Sólo sitio1; nuevasXYZ rechazadas, no se finge configurabilidad espacial. Cambiar yaw/preset/enable/remove sí implementado. |
| GateB2activos/2sitios/sceneepoch | NOT_IMPLEMENTED / BLOCKED | Correlación general sinAPIStageActorHandle→ActorId y segundaubicación no acreditada.2IDsconfig no bastan. |
| GateC retirada/configreinicio | IMPLEMENTED / HUMAN_NOT_TESTED | Lectura al iniciofrío y0registros si entrada retirada; no borraactor vivo al editar archivo. |
| RuntimeCP06,aparición/HP/render/AI/cleanup/reentrada/rollback | HUMAN_RUNTIME_NOT_TESTED | Sólo usuario Windows/DX12 podrá observar. No heredarCP05 ni GAMEPLAY_PASS. |
| Same-modelEOC2/terceros/performance | PENDING/NOT_TESTED | No aislamiento universal ni rendimiento certificado. |

Incidencias: run38689650849 compiló30casos peroTLSpor staticlocal dinámico, corregido a recordporvalor (StageServicecopia síncrona). Run38689862134 pasóTLS y bloqueó importsCRT delparser/std::string/vector; revisión específica en CRT_IMPORT_REVIEW,allowlist exacto. Run38690126831 pasó30/PE/7negativos/paquete. Run38690375002 descargó/verificó realmente; no se repitió build.
No se recompilaron CP03–05 ni se repitieron sus suites/render/ARC/32fuentes. Helpers aprobados tienen hash inmutable. ArchivoSourceZip conserva documentación previa a gates; este cierre añade resultados posteriores sin reempaquetar.

CP05 conservado: HOME_RETURN_WALKING_NOT_VERIFIED,30_UPDATE_GRACE_NOT_DIRECTLY_VERIFIED,CP05_ROLLBACK_PENDING,SAME_MODEL_EOC2_SIMULTANEOUS_PENDING. No se afirman más pruebas humanas.
