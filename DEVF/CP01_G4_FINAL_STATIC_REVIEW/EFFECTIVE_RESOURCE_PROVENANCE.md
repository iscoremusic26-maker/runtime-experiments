# G4 — procedencia efectiva y overlays de G2

**La incertidumbre de overlays aplicados por el servicio de mods queda cerrada para el intervalo documentado de G2: PASS_RUNTIME_LOG, conjunto vacío.** No se transforma este resultado en identidad byte por byte de recursos cargados, ni en prueba de una futura sesión aislada.

Base `dc2f65ab5d1423ce74d78661dbbea5e14a692409`. Se reutilizan [RESOURCE_INTEGRITY](../CP01_G4_EOC_RESOURCE_CONTINUATION/RESOURCE_INTEGRITY.md) y [G2_RUNTIME_BASELINE](../CP01_G4_EOC_SAFETY/G2_RUNTIME_BASELINE.md), sin modificar su estado histórico. El nuevo alcance resuelve el NOT_VERIFIED previo **del servicio de overlays**, no altera retroactivamente el manifiesto privado.

## Evidencia primaria dirigida

El log anonimizado completo sigue privado e intacto:2182 líneas, hash `d19f2760e695f48f4df59706b791de121ffe77806bdafde8a7539b2cdc2b78b4`. Se buscó únicamente el módulo de overlays y nombres de carga E_oc/E_ocb; no se reanalizaron las28 capturas.

Existe **una sola** línea de `dusk::mods::overlay`: sincronización de **0 archivos en L70**. No hay otro mensaje del módulo ni otra sincronización en el archivo completo, incluido el intervalo de capturas L1846–1897 y el cierre. Luau/Randomizer se habían activado en L67/68; no es un conteo anterior a activar esos mods. No hay nombres de carga de los dos ARC ni hashes de bytes cargados en ese log; su ausencia no significa que no se cargaran.

El texto completo del log, direcciones y rutas privadas no se publica. [focused-review.json](evidence/focused-review.json) conserva solamente conteo, línea y estados derivados. El hash distinto del original sin anonimizar mantiene la distinción documentada previamente.

## Contrato exacto, PASS_STATIC

Raíz oficial `40457c6adb381928e4b5fef6ed459ed291edd5e2`:

- `src/dusk/mods/svc/overlay.cpp:71–117,185–212`: `find_overlay_files` añade miembros `overlay/` de mods activos; `append_runtime_overlays` incluye registros dinámicos por archivo de paquete o buffer. Se cuenta **la unión de ambos**, no solo overlays declarados al inicio. Rutas case-insensitive, orden posterior prevalece.
- El sync vacía el mapa publicado, construye esa lista y registra su tamaño antes de pasarla a Aurora. `extern/aurora/lib/dolphin/dvd/fst.cpp:319–348` vacía la lista anterior y reconstruye el FST: registrar0 no conserva overrides anteriores en ese mecanismo.
- `overlay_add_file/add_buffer/remove/remove_mod:214–255` cambia slots y marca dirty. `frameEnd:340–344` sincroniza cuando hay cambios; lifecycleApplied también sincroniza. `registry.cpp:226–247` despacha ambas rutas; `loader.cpp:1238–1265` llama frameEnd tras actualizaciones nativas o Luau.
- Luau expone el mismo OverlayService (`mods/luau_runtime/src/services/bindings.cpp:171–195`), no una vía silenciosa diferente para esas funciones. Un registro dinámico **aplicado** durante ticks normales produciría otra sincronización registrada.
- `JKRArchivePri.cpp:306–440` invalida generaciones y puede sustituir miembros de un ARC mediante rutas virtuales abiertas por DVD/FST. Esos archivos, si los publica el servicio, también entrarían en el conteo; no son una excepción al cero observado.

Se concluye, para el flujo original normal y el log completo proporcionado: **no se aplicaron overrides de mods mediante este servicio para E_OC/E_ocb ni para sus miembros durante las capturas**. Slots solicitados pero todavía no sincronizados no se pueden censar con esta línea; por definición no habrían cambiado aún el FST efectivo. No se afirma que el servicio carezca de capacidad dinámica ni que otra sesión tenga el mismo conjunto.

## Clasificación y límites

| Categoría | Estado | Conclusión |
|---|---|---|
| Overlays de paquetes/slots aplicados en G2 por OverlayService | **PASS_RUNTIME_LOG + PASS_STATIC** | Lista completa publicada0 antes del intervalo, sin cambios posteriores registrados; ausencia acreditada dentro de este mecanismo |
| Capacidad de overlays dinámicos | PASS_STATIC | Existe; cambios aplicados pasan por sync/frameEnd/lifecycle y deberían reflejarse en el log normal |
| Slots dinámicos no aplicados o cambios después de terminar el log | NOT_VERIFIED | No se miden; no constituyen overrides efectivos observados durante G2 |
| Reemplazos de textura | PASS_RUNTIME_LOG para1867 registros; PASS_STATIC de sistema distinto | Aurora carga registros de imágenes/texture keys; `src/dusk/texture_replacements.cpp:14–26` no publica archivos ARC por OverlayService |
| E_oc/E_ocb aportados desde GZ2E01 | PASS_STATIC de bytes/estructuras; procedencia reportada | Hashes/tamaños/manifiesto y análisis anteriores intactos; extracción individual del disco declarada por el usuario |
| Bytes efectivamente usados en memoria/modelos G2 | **PARTIAL / NOT_VERIFIED byte a byte** | Registro de recursos y visualización normal, fuente y ausencia de overlays respaldan la procedencia; no hay hash de carga nativa ni identidad de toda la imagen |

Los reemplazos de textura no demuestran modificaciones del ARC, sus vértices, joints o BCK; tampoco garantizan render idéntico al disco.1867 es cantidad de **registros**, no1867 texturas necesariamente dibujadas. Las advertencias DDS no se atribuyen a DEVF.

La búsqueda focalizada del fuente oficial Randomizer no encontró llamadas OverlayService o referencias a los dos recursos buscados. El cero runtime del servicio es la evidencia principal; no se deduce que Randomizer no altere progresión/escenario u otros datos mediante sus capacidades. Su actividad y Luau se conservan como baseline **no aislado**, sin nueva auditoría ni atribución de efectos no observados.

El mensaje no valida la imagen base, recursos inyectados con APIs de memoria como `dRes_control_c::setObjectRes` (d_resorce.cpp:1024…), modificaciones directas a modelos/datos o archivos virtuales ajenos a la lista del servicio. Tampoco identifica bytes de un handle ya abierto o un recurso decodificado que siga en memoria: el conteo es del conjunto publicado en FST. Se identifican límites de cobertura del mensaje, **sin afirmar que estas sustituciones ocurrieran en G2**. El ARC/hash aportado sigue siendo la referencia geométrica de la revisión estática.

**No se pide ahora una declaración de ausencia de overlays ni reenviar ARC/ROM/log:** esa pregunta del checkpoint anterior ya tiene respuesta para OverlayService en G2. La identidad byte a byte se conserva como límite de procedencia/runtime, no se utiliza como único motivo para mantener bloqueada la ubicación ni se solicita nueva instrumentación.
