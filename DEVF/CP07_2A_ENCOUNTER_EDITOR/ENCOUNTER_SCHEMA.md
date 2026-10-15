# Contrato de coleccion/exportacion schema1
Dos archivos FIJOS en HostService.data_dir del mismo mod_id:
- encounters.work.json: document_type=devf_encounter_collection.
- encounters.export.json: document_type=devf_encounter_export.
Nunca placements.json ni CP06 schema1. API nativa1.0 no ejecuta estas ubicaciones arbitrarias.

Raiz EXACTA: document_type, schema_version(1), producer(dev.devf.cp06_native_config_dual@0.7.2), runtime_applied(false), encounters(array0..16).
Cada encounter exige:

| Campos | Contrato |
| --- | --- |
| encounter_id/name | ID ASCII a-z0-9_- de1..32;nombre UTF8 imprimible1..96bytes; ambos unicos |
| enemy/variant_id/native_profile | E_OC2/native_elite/510, solo catalogo soportado |
| stage/room/layer | stage ASCII alfanumerico+_1..7;room0..63,layer0..15 |
| x/y/z | valores copiados float32 del juego, serializados double17digitos sin perder valor;finitos±1e6 |
| yaw_s16 | orientacion inicial elegida,-32768..32767 |
| capture_yaw_s16 | orientacion nativa de la captura;se conserva al editar yaw inicial |
| quantity/spacing_units |1..4 y0..1000entero;SOLO METADATO,no calculo de posiciones de grupo |
| respawn_policy |on_zone_reentry o no_respawn_during_session;respawn_applied=false |
| capture_origin/capture_tick |link_readonly_v203 y contador local de update1..2^53-1;no reloj civil |
| capture_validity/terrain_verified |READ_ONLY_SNAPSHOT_NOT_TERRAIN_VERIFIED yfalse |

Claves desconocidas/duplicadas, referencias de variantes futuras, claim de respawn/terreno, NaN/Inf,strings invalidos y archivo>16384bytes se rechazan. UTF8 validado;escapesJSON y pares surrogate validos se decodifican/roundtrip. No token en params/setID ni lectura de ActorId. Los datos son diseño, no firma de autenticidad ni permiso de spawn.

Ejemplo reproducible sin inventar captura: examples/encounters.export.empty.json. Para obtener dos capturas REALES usar HUMAN_TEST; laboratorio cubre dos stages sinteticos y no los presenta como datos humanos. Validador comparte encounter_core.hpp con DLL:
```powershell
.\tools\encounter_validate.exe .\encounters.export.json
# exit0: ENCOUNTER_EXPORT_VALID count=N runtime_applied=false
# exit1: JSON/esquema invalido; exit2: uso/archivo inaccesible
```
CLI no escribe archivos, solo valida export, no terreno, API runtime, gameplay ni procedencia criptografica.

Flujo: Nuevo→Capturar→editar metadata→Anadir/actualizar→Guardar coleccion. Seleccionar elemento permite editar metadatos conservandoID; eliminar requiere confirmacion. Descartar borrador restaura seleccion; deshacer coleccion restaura ultima guardada. Exportar escribe instantanea de coleccion provisional valida (puede incluir cambios aun no guardados al work); estado/botones distinguen ambos archivos. Guardar trabajo no exporta ni viceversa. Ninguna accion produce altas/bajas en StageService.
Backup exclusivo independiente32slots por archivo, relectura/parse/bytes antes y despues, deteccion de conflicto previo. Sin garantia atomica/lock frente a powerloss o otro escritor; no editar externamente durante Guardar. Error de recuperacion deja backup util y estado read-only, sin activar fallback.
