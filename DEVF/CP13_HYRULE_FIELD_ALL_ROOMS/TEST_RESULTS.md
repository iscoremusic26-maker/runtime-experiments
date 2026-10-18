# Resultados CP13

CP13_WINDOWS_CI_PASS_HUMAN_PENDING. Dictamen de cobertura: **CP13_PARTIAL_WITH_EXPLICIT_GEOMETRY_BLOCKERS**. El editor ya no limita el catálogo a1..5, pero no se certifica suelo ni runtime de recursos no disponibles aquí.

- Fuente realmente compilada: c3257bdd360c717fb906aa9e2c942ad9e98a1bd6.
- CI: d126316a01d3243a805f899a1ffe9ec77ce90723.
- [Run final 39153841948](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/39153841948): build SUCCESS + independent-download SUCCESS.
- [TEST privado DEVF_CP13_HYRULE_FIELD_TEST_39153841948](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/39153841948/artifacts/12146112007); artifact12146112007. Caduca2026-11-17 13:25:23 America/Panama (18:25:23UTC), comprobado por API.
- Fuente PR69 y CI PR54 permanecen draft/open/unmerged. El checkpoint documental posterior NO es la fuente compilada. MANIFEST/SOURCE_COMPILED del paquete conservan el pin anterior al cierre documental.

|Suite realmente ejecutada Windows|Casos|Resultado|
|---|---:|---|
|CP08 app/legacy geometry|42|PASS|
|CP09 importer incl.CISO+576/4096B|71|PASS|
|Multi-editor/schema/backup/legacy/UI|110|PASS|
|Alias de nombres (también incluidos en suite multi)|25|PASS|
|CP13 editor/catálogo/32/blocked/DZR|39|PASS|
|CP13 core real/provider/client32|26|PASS|
|Runtime anterior|66|PASS|
|Black/texture/identity|26/20/30|PASS|
|Damage/dynamic/visual/eyes|22/28/22/9|PASS|
|Strokes/perf/CP12|36/4/7|PASS|
|Negativos PE/ABI/ZIP provider + expansion|19+7|PASS|

Los conteos por suite no deben sumarse como casos únicos (hay pruebas de nombres reutilizadas). Paridad C#→C++ schema1/schema2/Black y export CP13 de32 registros PASS. MSVC14.51.36231, SDK Windows10.0.26100.0\, AMD64; .NET8 self-contained; SDK host40457c6 intacto y empaquetador oficial. Auditoría PE/imports/exports/hooks/manifests PASS. El cuerpo del hook CP12 se comparó con el baseline: idéntico excepto versión. Políticas de combate y efectos sin cambios; máximo8 auras.

Corpus: un ARC auténtico R03 hash dc53106667811c4cde18b35edb5279357f00ebecaef2f9de546aea9a5a2b06af,5326 triángulos; alturas contrastadas con PythonCP01. Salas adicionales y catálogo de ausencia R08/STG son fixtures legales sintéticos: CI_SYNTHETIC_PASS, NO REAL_GEOMETRY_VERIFIED de R00/R07/etc. Los tres vectores humanos legacy y sus IDs/enabled/XYZ/layer/yaw se preservan. Schema1 original no se reescribe. Nuevas colocaciones nunca heredan CP08_OBSERVED.

Descarga real: otro runner descargó el artifact publicado y el ZIP interior, recalculó bytes/SHA256/CRC, extrajo ambas DLL, comprobó PE/ABI/manifests, EXE y SOURCE_COMPILED/ledger/pines. No solo metadatos de Actions. No contiene geometría, disco, recursos originales o DLL suelta.

|Archivo|Bytes|SHA256|
|---|---:|---|
|ZIP interior|66608917|2f118703d7c23d55f3bf9eb18bdbf9b4ab731f1f7ee5011b255226b75f1e33e0|
|DEVF Map Editor CP13.exe|161967639|1b6c72ae8b81d2b23409e311f60ca8f942b01ba2e70e0b484c6a7f547f3a45de|
|DEVF_Provider_0.13.0_CP13_TEST.dusk|130335|3a3c874e71cf8b63c43fb54340e11778011c486026897d6c29d3d6ad2e67634e|
|DLL provider interna|296960|2932b3e2c1b188ae89f22545e94431a81e71d79c96c076038ae286af9a328c83|
|BokoblinExpansion_0.10.0_CP13_TEST.dusk|80597|e216c9989114e42744ca0a88402c416736c0a3ad8e743e81ce3630fd6197a218|
|DLL expansion interna|178688|7fdb6681904c675220f09fbde19d1811c8a2b7c0988a5177c28ef6996a3a692b|

Primer run39153420732: build SUCCESS, independent-download FAIL por KeyError cp13_lab_cases (el resultado histórico correcto es cp12_lab_cases). Se corrigió la clave y se repitió la CI completa sobre nuevo pin; no se presenta aquel paquete como entrega final.

Laboratorio Linux adicional:26 casos del core real con ASan/UBSan PASS (detect_leaks=0). LeakSanitizer no ejecutable bajo ptrace del entorno, NOT_RUN; no es un PASS de fugas. sizeof observados Linux:broker3264/config2664/tabla exacta3600 bytes;100 parseos acotados, no medición FPS/GPU ni runtime humano.

Integridad contra CP12:1940 blobs previos con igual SHA/mode/type, sin borrados/cambios; todas las adiciones están bajo CP13. Workflows históricos y ramas CP12 intactos.

Pendiente: diagnóstico local auténtico de todas las entradas F_SP121, especialmente R06 KCL_DEGENERATE y STG sin KCL reutilizable; no hay transformación/asociación compartida demostrada. [Matriz completa con procedencia](COVERAGE.md). Nuevas capas/spawns, rendimiento y apariencia en Windows/DX12: HUMAN_RUNTIME_PENDING. No se ejecutó Dusklight.
