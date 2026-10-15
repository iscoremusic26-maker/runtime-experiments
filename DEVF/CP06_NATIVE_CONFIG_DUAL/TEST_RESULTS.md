# Resultados del nuevo mod JSON nativo

| Gate | Resultado |
| --- | --- |
| BOTH -> dos registros BE idénticos a QA B | PASS OFFLINE |
| FIELD ONLY / NORTH ONLY -> uno correcto | PASS OFFLINE |
| Ambos false / placements=[] -> cero | PASS OFFLINE |
| Orden JSON invertido -> registro determinista field,north | PASS OFFLINE |
| Float32 equivalente permitido; suelo KCL rechazado | PASS OFFLINE |
| JSON ausente/vacío/BOM/oversize/sintaxis/duplicados/desconocidos/tipos | PASS OFFLINE; cero altas |
| Catálogo sólo nativo, IDs/referencias, sitio/escena/yaw/params | PASS OFFLINE; valida disabled |
| IO parcial/growth/error/throw/close; servicios/versiones nulos o incompatibles | PASS OFFLINE; cero altas |
| Fallos de Add/handles/rollback inverso propio/removal retry | PASS OFFLINE |
| No reinyección init/update; cleanup idempotente; config entre reinicios | PASS OFFLINE |
| Total core+adaptadores reales | **109 PASS** |
| Windows MSVC AMD64 / PE/ABI / package SDK | PASS |
| Ocho negativos PE/ZIP, incluido FileService | PASS |
| Descarga independiente del ZIP y todas sus capas | DOWNLOAD_VERIFIED |
| Nuevo gameplay JSON0/1/2, reentrada/rollback | HUMAN_RUNTIME_PENDING |
| Correlación ActorId por placement / personalización | NO IMPLEMENTADA, fuera de alcance |
| FPS/terceros/aislamiento universal | NOT_VERIFIED |

La DLL y el laboratorio usan los mismos headers config_core/config_io/runtime/registration/native_records. Los dobles de servicio se limitan a Host/File/Stage; FileService de laboratorio utiliza archivos Windows reales para editar/releer al simular reinicio. No fake de motor ni demostración de nacimiento por MOD_OK.

Los24casos de registro previo se ejercitaron porque se adaptó ese core a máscara de activación, no por repetir investigación histórica. Los85casos adicionales cubren integración JSON/IO/runtime. Nombres completos en evidence/build-result.json.

[Primer CI38761708755](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38761708755): FAILURE después de compilación/109PASS por error del auditor negativo nuevo (escape NUL). [Segundo CI38761953150](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38761953150): SUCCESS tras corrección del auditor. No fallo del host ni cambio de lógica para ocultarlo. No paquete listo de la ejecución fallida.

Observaciones previas: el usuario reportó QA A correcto y dos Bokoblins adicionales simultáneos en QA B. Son USER_HUMAN_REPORTED; el resumen del log QA B fue USER_LOG_ANALYZED_IN_CHATGPT. No lectura de bytes o píxeles por Codex, no mapa PID147/148→placement, no herencia de reentrada/FPS a la versión JSON.

[Descarga independiente 38762282880](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38762282880): SUCCESS, job116516404815, CIa9aabade816e8ea366b6f74a2cd731723a762ec1. SHA/bytes/CRC, ejemplos y ledger comprobados sobre descarga real. **JSON_DUAL_NATIVE_QA_BUILD_READY**, sin gameplay. Los textos PENDING internos del manifest congelado describen la fase de build; el informe posterior actualiza el gate sin reempaquetar.
