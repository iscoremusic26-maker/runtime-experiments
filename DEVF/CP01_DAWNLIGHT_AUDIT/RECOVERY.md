# Recuperación del checkpoint documental

Base inalterada: **`545b2d1418bfcae11dd4585c1a9bdcbc526b6a2d`**, tag `DEVF_CP01_OFFICIAL_SDK_ARCHITECTURE`, repo privado `iscoremusic26-maker/Mods-Duskligh`.

Rama nueva: **`audit/devf-dawnlight-v403`**, creada desde esa base. Tag propio: **`DEVF_CP01_DAWNLIGHT_FOCUSED_AUDIT`**. El commit completo de esta entrega es el objeto obtenido por `git rev-parse DEVF_CP01_DAWNLIGHT_FOCUSED_AUDIT^{commit}`; se identifica también en el tag y PR de GitHub. El PR se mantiene draft y no se hace merge. La referencia dinámica por tag evita introducir en un archivo un SHA autorreferente que cambiaría al escribirlo.

Cambios autorizados: **solo seis informes Markdown en `DEVF/CP01_DAWNLIGHT_AUDIT/`**. Ningún código, test, workflow, recurso, ejecutable, original privado o implementación Dawnlight se añade. No se ejecutaron Dawnlight/Dusklight, pruebas in-game, compilaciones o suites de regresión. La publicación usa `[skip ci]`; los paths de los workflows existentes tampoco cubren esta carpeta. No borrar o sobreescribir tags anteriores.

## Recuperar sin alterar una copia existente

```bash
git clone --no-checkout https://github.com/iscoremusic26-maker/Mods-Duskligh.git work/devf-dawnlight-recovered
git -C work/devf-dawnlight-recovered fetch origin refs/tags/DEVF_CP01_DAWNLIGHT_FOCUSED_AUDIT:refs/tags/DEVF_CP01_DAWNLIGHT_FOCUSED_AUDIT
git -C work/devf-dawnlight-recovered switch --detach DEVF_CP01_DAWNLIGHT_FOCUSED_AUDIT
git -C work/devf-dawnlight-recovered rev-parse HEAD
git -C work/devf-dawnlight-recovered status --short
git -C work/devf-dawnlight-recovered merge-base --is-ancestor 545b2d1418bfcae11dd4585c1a9bdcbc526b6a2d HEAD
git -C work/devf-dawnlight-recovered diff --name-only 545b2d1418bfcae11dd4585c1a9bdcbc526b6a2d HEAD
```

El último comando debe mostrar únicamente los seis informes de esta carpeta. No usar reset/force push sobre ramas anteriores. La verificación de recuperación se realiza mediante fetch desde GitHub a un repositorio bare independiente de la copia de trabajo, comprobando tag→commit, head de rama, ancestry, hashes de informes y árboles previos intactos.

Leer COMPARATIVE_AUDIT → SCENE_OWNERSHIP → ENEMY_PARAMETERS → ARCHITECTURE_RECOMMENDATION → NEXT_VALIDATION_GATES. Las conclusiones nuevas se aplican como precisión documental sobre el checkpoint base: propietario de motor distinto de room/layer lógico, cancelación ABI potencial pero sin garantía y rango de layer lógico0–14. No modificar ni armar el prototipo anterior por leer estos informes.

## Fuentes externas fijadas y procedencia

| Referencia | Recuperación / uso |
|---|---|
| Dawnlight | [BeZide93/dawnlight v4.0.3](https://github.com/BeZide93/dawnlight/tree/9bb214d47617c9bc295d22facf36c35d17661e5a), commit **9bb214d47617c9bc295d22facf36c35d17661e5a**. Fuente recuperada por Git en work independiente, sin repetir el HTTP403. No compilar ni incorporar al repo DEVF. |
| Dusklight oficial | [TwilitRealm/dusklight v2.0.3](https://github.com/TwilitRealm/dusklight/tree/40457c6adb381928e4b5fef6ed459ed291edd5e2), commit **40457c6adb381928e4b5fef6ed459ed291edd5e2**. Checkout anterior limpio; lectura focalizada del call path y funciones necesarias. Equivalencia con ZIP y dependencias/build ya acreditadas se reutilizan. |
| Windows oficial | Miembro sdk/windows-amd64.lib ya recuperado por CP00: 9400986 bytes, SHA256 **4dc4a511d761e6eb52541733fa31919a2234ed9cd5b2f16f8fea91c468f30ca4**. Se cotejaron únicamente 18 import objects/export records relevantes; no nueva auditoría de ZIP o binario completo. El binario original permanece privado y no se publica. |
| Evidencia CP00 | `DEVF/SOURCES_AND_VERSIONS.md`, `DEVF/evidence/input_verification.json`: Windows PE32+/AMD64, versión2.0.3.0 y correspondencia de30042 import/export symbols ya verificados. |
| Evidencia CP01 | `CP01_OFFICIAL_ARCHITECTURE/TEST_RESULTS.md` y sus logs: build/lab Windows/MSVC anterior, 26 PASS limitados a su alcance. `CP01/LOCATION_*` y auditorías de seguridad conservados, sin repetirlos. |

La auditoría examinó diez archivos Dawnlight exactos; se comprobó que las copias locales son idénticas a sus Git blobs del commit fijado. new_save_modes se leyó solamente en los hooks de admisión que exige comprender el spawner. Los hashes siguientes son documentación de procedencia, no incorporación de esas fuentes:

| Archivo externo | Bytes | SHA256 |
|---|---:|---|
| `src/enemy_spawner.cpp` | 14414 | `c987c772e48151b94739eb4d0af5cc5fa086ddb17ddd85ddf5d79bd8b5f102eb` |
| `src/enemy_spawner.hpp` | 1198 | `156e17adff0a06e82a49d2bf0cab67ebfc5362431c1ac6649b04ee0985d92266` |
| `src/cave_randomizer.cpp` | 13912 | `1f043f78e8b7d45cd584609906dc8a2fd29dea54dfe7c5b0c79a16b613b847d2` |
| `docs/darknut-arena-spawner.md` | 8726 | `c9f7fe5a9c5872be4d3cd64e7083ed234ef3c9f416f3c5fafcf2b494ffe67fe3` |
| `tests/enemy_spawner_scene_test.py` | 5958 | `e61dd29a17fddca38e4c8cd8a5b6150fe76f5e32ada161b5d345853f1e6f4df3` |
| `src/cave_randomizer_ground.hpp` | 1463 | `19f68eb9c3cf85ee224ce47cdc6e60c915c9f19c6e690a348be7fb4a277f14d6` |
| `tests/cave_randomizer_ground_test.cpp` | 1623 | `bdfe4c925600465de9fd9b711587794fb99e21c7648cdc4a21027eafd1804ff5` |
| `src/new_save_modes.cpp` | 171604 | `ac574286510165e0cbae6d979461f8caa5be9384c34a68dc0a582f71f919d6de` |
| `CMakeLists.txt` | 7312 | `a4913290f2eda6dc4f300a0107e6a512f01a13fe0a9476bc4045d22325a199bc` |
| `cmake/FetchDusklight.cmake` | 3390 | `aed0b2997655385dbb3ece2d29c8ad3d4ea3bf166ac4c05efc39669e2e780288` |

Las referencias a funciones/rangos del host oficial se fijan a40457c6 en COMPARATIVE_AUDIT; los hashes anteriores del SDK siguen disponibles en la carpeta CP01_OFFICIAL_ARCHITECTURE. No trasladar raw offsets o supuestos de plataforma de Dawnlight. CMake default v2.0.0 no es certificación de compatibilidad binaria v2.0.3.

## Parada y próxima autorización

Mantener **DISARMED_NO_REGISTRATION**, **CP02 NO-GO** y bloqueo independiente de perfiles/descarga DLL. No convertir la recuperación en port, hooks, test activo o host recompilado. La fase siguiente propuesta necesita autorización propia y solo los datos nuevos del caso indicado en NEXT_VALIDATION_GATES; no pedir de nuevo ZIP/ARC/coordenadas ya acreditados.

No hay instalación ni runtime que revertir. Para revertir una selección documental, cambiar a la base en una copia nueva o detached; no sobrescribir esta rama/tag ni borrar historia. Esta tarea termina después de publicar/verificar el checkpoint documental.
