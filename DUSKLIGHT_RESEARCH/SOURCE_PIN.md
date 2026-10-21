# Entradas fijadas y alcance de la evidencia

Checkpoint inicial de la campaña encargada el 20 de octubre de 2026. Plataforma solicitada: **Dusklight 2.0.3, Windows x64, DirectX 12, disco GZ2E01 USA**. Esta plataforma es el objetivo de interpretación; esta campaña no ha ejecutado el juego ni certificado el backend del equipo del usuario.

| Entrada | Revisión exacta | Comprobación efectuada |
| --- | --- | --- |
| Upstream `TwilitRealm/dusklight` | `40457c6adb381928e4b5fef6ed459ed291edd5e2` | Commit consultado directamente mediante GitHub; tag `v2.0.3` apunta al mismo commit. |
| Árbol Git del commit | `e4b79b565b2842f711f7c9f2390f56ef11063157` | Consultado mediante Git commit API; distinto del SHA del commit. |
| Fuente ZIP disponible localmente | SHA256 `9dbdc0b068df24c3fbb680c87be25e904978f04b315e2051e3c6203476516008` | SHA256 medido; no se confía solamente en el nombre `dusklight-2.0.3.zip`. |
| Base documental segura | `iscoremusic26-maker/Mods-Duskligh` @ `747ecc410162ed76f9aa68dbe9e9e2ad4e4d8c3f` | Rama predeterminada `checkpoint/devf-cp00-windows-20261011`; árbol `f6373d2254382f924c36bc035ed2b55c4e9a303e`. |
| Rama nueva de esta campaña | `research/dusklight-203-dusk-atlas` | Creada desde el SHA anterior tras inspeccionar las 91 ramas existentes; no había rama research/atlas. |
| Histórico CP20, fuente PR #80 | `d9f83eaabff549440a10a33c002bf8e2e37945a6` | Metadatos y documentación en solo lectura; revisión compilada histórica distinta: `2ce550395ff69d2c9046a2d3e0b635024307ce1e`. |
| Histórico CP21, fuente PR #81 | `fe47c8b828939829914d466a425cb1e2c0223cd9` | Árbol de 3382 entradas incluidas carpetas, sin truncación; revisión compilada histórica `192a7731623d69baacdd37011db60ce894d9de18`. |
| CI auxiliar PR #65 / #66 | `d8b07d029c4f98ca62d4d2eaaf935d87eea290d2` / `341c7a341980c3982d2a1e2671e7852f3ef1d550` | Consultados en solo lectura. No se ejecutó ninguna CI nueva. |

La API confirmó que el repositorio documental es privado. No se cambió su visibilidad. No se incorporó ninguna rama DRAFT a la rama de investigación.

## Cómo se certificó la fuente local

Se reconstruyeron hashes Git de blobs y árboles usando bytes y modos del ZIP, y se contrastaron con las entradas raíz del commit remoto. **28 de 31 entradas raíz coinciden íntegramente**, incluidos `src/`, `include/`, `sdk/`, `docs/`, `libs/`, `assets/`, `cmake/`, `tools/`, `res/` y los CMake raíz. Esto verifica bytes, rutas y modos bajo esos árboles, sin inferir identidad a partir del nombre del ZIP. `mods/`, `platforms/` y `extern/` requirieron comprobación separada:

- `mods/`: los **63 blobs ordinarios** coinciden individualmente. No están los submódulos cosmetics y randomizer.
- `platforms/`: **42 de 43 blobs** coinciden individualmente. `platforms/android/gradlew.bat` tiene bytes diferentes; no se leyó para fundamentar comportamiento ni se presume que la diferencia sea solo de finales de línea. Hashes en [source_tree_pin.json](tools/source_tree_pin.json).
- `extern/`: solo se observaron los gitlinks fijados; los contenidos no están disponibles localmente.

La certificación abarca el árbol principal disponible, con la excepción explícita anterior. **No certifica contenidos de submódulos ausentes, archivos producidos durante la compilación, el EXE de distribución ni símbolos efectivamente resolubles en ese EXE.** El inventario usa hashes de los bytes locales; la excepción Android permanece señalada para evitar citarla accidentalmente.

| Submódulo ausente | SHA fijado | Impacto |
| --- | --- | --- |
| `extern/aurora` | `3227d76c60e1e782ca576610bce61c9e7744d8be` | Interfaces consumidas por el port visibles; interior de GPU/DX12, DVD/CARD y generación de símbolos no auditado. |
| `extern/borealis` | `4ac5e7052a8c49a122f8d57f626b5c75c5ca6968` | Interfaz de UI/IO consumida visible; implementación externa y dependencias transitivas no auditadas. |
| `mods/cosmetics` | `fd93491089fa95441789244f2b2fd22a451ecbcc` | No se inventaría su código interior ni se deducen capacidades de ese mod. |
| `mods/randomizer` | `1f24e81303536db4b77f49d057a8ec1f11162000` | Mismo límite; no se usa su funcionalidad como contrato SDK. |

Las ubicaciones upstream se declaran en [`.gitmodules`, L1-L12](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/.gitmodules#L1-L12); los SHA se observaron en los árboles Git remotos, conservados en `tools/source_tree_pin.json`.

## Acceso y materiales previos

Los tres repositorios indicados fueron accesibles mediante el conector GitHub. Los directorios locales `Mods-Duskligh` y `codex-cp00-inputs` no aportaban un HEAD utilizable del repositorio documental. `git ls-remote` falló por conexión al proxy; `gh auth status` no confirmó credenciales válidas. Se empleó el conector para leer y persistir; no se buscó ningún secreto ni se cambió el proxy. Esto no bloquea la investigación estática.

Se leyó primero `docs/modding.md`, SDK, servicios y ejemplos. Se examinó el [handoff CP00 fijado](https://github.com/iscoremusic26-maker/Mods-Duskligh/blob/747ecc410162ed76f9aa68dbe9e9e2ad4e4d8c3f/DEVF/DEVF_CP00_HANDOFF.md#L1-L15): aquella evidencia separa compilación Windows de juego/DX12 no probado. La instrucción histórica de no iniciar otro proyecto no es un contrato del SDK ni sustituye este encargo general. El material posterior se referencia en PRIOR_RESEARCH.md cuando haya sido contrastado.

## Reproducción y niveles

El [inventario reproducible](tools/inventory.py) lee la fuente y escribe únicamente metadatos fuera de ella. `SOURCE_OBSERVED` describe lógica leída; `STATIC_CROSSCHECKED` exige contrato, implementación y/o consumidor contrastados; `CI_OBSERVED` describe solo la ejecución histórica observada. Ninguno equivale a `WINDOWS_RUNTIME_OBSERVED` o `HUMAN_RUNTIME_OBSERVED`.

Fuentes API consultadas: [tag exacto](https://api.github.com/repos/TwilitRealm/dusklight/git/ref/tags/v2.0.3), [commit Git](https://api.github.com/repos/TwilitRealm/dusklight/git/commits/40457c6adb381928e4b5fef6ed459ed291edd5e2), [árbol raíz](https://api.github.com/repos/TwilitRealm/dusklight/git/trees/e4b79b565b2842f711f7c9f2390f56ef11063157). Estas observaciones de metadatos no tienen un número de línea de código; no se fabrican anclajes para ellas.
