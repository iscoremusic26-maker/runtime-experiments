# Investigación histórica reutilizable

Estado de esta ficha: lectura documental y contraste estático; **ninguna ejecución del juego en esta campaña**. CP20/CP21 se usan como evidencia de método y límites técnicos. Su funcionalidad concreta no define el alcance del atlas. Los PR fuente #80/#81 y CI #65/#66 se consultaron en solo lectura.

## Entradas y procedencia

| Material consultado | Commit exacto | Alcance de lo observado |
| --- | --- | --- |
| PR fuente #80 / CP20 | `d9f83eaabff549440a10a33c002bf8e2e37945a6` | Metadata del PR; fuente declarada compilada `2ce550395ff69d2c9046a2d3e0b635024307ce1e`. No se reinterpretó el cierre documental como una compilación nueva. |
| PR fuente #81 / CP21 | `fe47c8b828939829914d466a425cb1e2c0223cd9` | Árbol recursivo de 3.382 entradas, sin truncamiento; documentos de CP19, FIX01/FIX02, CP20 y CP21. Fuente declarada compilada `192a7731623d69baacdd37011db60ce894d9de18`. |
| CI #65 / run `39325015857` | `d8b07d029c4f98ca62d4d2eaaf935d87eea290d2` | Metadata de run y jobs/steps consultados directamente a GitHub. |
| CI #66 / run `39359746319` | `341c7a341980c3982d2a1e2671e7852f3ef1d550` | Metadata de run y jobs/steps consultados directamente a GitHub. |
| Fuente upstream para contraste | `40457c6adb381928e4b5fef6ed459ed291edd5e2` | SDK de ABI/StageService, empaquetado y arranque del audio. |

Los SHA compilados/de cierre y el pin upstream están declarados en [CP21 DELIVERY, líneas 18–26](https://github.com/iscoremusic26-maker/Mods-Duskligh/blob/fe47c8b828939829914d466a425cb1e2c0223cd9/DEVF/CP21_PUBLIC_RELEASE/DELIVERY.md#L18-L26). La distinción entre el snapshot histórico de regresiones y el árbol posterior ya era explícita en [CP20 SOURCE_AUDIT, líneas 3–11](https://github.com/iscoremusic26-maker/Mods-Duskligh/blob/fe47c8b828939829914d466a425cb1e2c0223cd9/DEVF/CP20_EXPLICIT_BLUE_RED_BLACK/SOURCE_AUDIT.md#L3-L11). **DOC_CONTRACT histórico, HIST-001**.

## CI observada y límite de la evidencia

| Run consultado | SHA CI observado | Jobs observados | Resultado consultado |
| --- | --- | --- | --- |
| [CP20 `39325015857`](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/39325015857) | `d8b07d029c4f98ca62d4d2eaaf935d87eea290d2` | `build` (`118308460609`), `independent-download` (`118310610334`) | Ambos `completed` / `success`; run intento 1, evento `pull_request`. |
| [CP21 `39359746319`](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/39359746319) | `341c7a341980c3982d2a1e2671e7852f3ef1d550` | `build` (`118422869348`), `independent-download` (`118424910938`) | Ambos `completed` / `success`; run intento 1, evento `pull_request`. |

La consulta de jobs muestra pasos satisfactorios de regresión Windows, corpus/ABI/PE y auditoría de paquetes, y de descarga independiente de bytes, SHA256, CRC, ABI, imports, hooks y ledger. Los workflows fijan Windows y los checkouts upstream/Aurora: [CP20, líneas 11–49](https://github.com/iscoremusic26-maker/codex-cp00-inputs/blob/d8b07d029c4f98ca62d4d2eaaf935d87eea290d2/.github/workflows/devf-cp20-explicit-blue-red-black.yml#L11-L49), [CP21, líneas 11–49](https://github.com/iscoremusic26-maker/codex-cp00-inputs/blob/341c7a341980c3982d2a1e2671e7852f3ef1d550/.github/workflows/devf-cp21-public-package.yml#L11-L49). Los trabajos de descarga son dependientes de `build`: [CP20, líneas 91–116](https://github.com/iscoremusic26-maker/codex-cp00-inputs/blob/d8b07d029c4f98ca62d4d2eaaf935d87eea290d2/.github/workflows/devf-cp20-explicit-blue-red-black.yml#L91-L116), [CP21, líneas 97–122](https://github.com/iscoremusic26-maker/codex-cp00-inputs/blob/341c7a341980c3982d2a1e2671e7852f3ef1d550/.github/workflows/devf-cp21-public-package.yml#L97-L122). **CI_OBSERVED, HIST-002/HIST-003**.

Esto acredita los estados y pasos que GitHub conserva para esos commits. En esta campaña no se descargaron artefactos, no se reejecutaron jobs y no se reprodujeron las auditorías. Las cifras de casos y bytes de los informes son **reportadas**, no medidas de nuevo. No se deduce de `success` que una llamada sea segura durante un cambio de sala, que un sonido se oiga o que un hook conviva con cualquier otro mod. CP21 separa expresamente laboratorio, compilación y lo que requiere juego vivo en [DELIVERY, líneas 38–47](https://github.com/iscoremusic26-maker/Mods-Duskligh/blob/fe47c8b828939829914d466a425cb1e2c0223cd9/DEVF/CP21_PUBLIC_RELEASE/DELIVERY.md#L38-L47). **DOC_CONTRACT histórico, HIST-004**.

## Lecciones generales contrastadas

### 1. Un singleton existente puede preceder a sus recursos

FIX01 documenta un crash al consultar ondas desde `mod_update` y distingue la dirección global del gestor de la creación efectiva de la tabla de bancos: [IMPLEMENTATION, líneas 15–28](https://github.com/iscoremusic26-maker/Mods-Duskligh/blob/fe47c8b828939829914d466a425cb1e2c0223cd9/DEVF/CP19_FIX01_STARTUP_AUDIO_READINESS/IMPLEMENTATION.md#L15-L28). La explicación se contrasta en el upstream fijado:

- El constructor de `Z2AudioMgr` asigna `mAudioMgrPtr = this`: [Z2AudioMgr.cpp, líneas 22–29](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/Z2AudioLib/Z2AudioMgr.cpp#L22-L29).
- `Z2AudioMgr::init` crea `JAUSectionHeap` después: [líneas 107–118](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/Z2AudioLib/Z2AudioMgr.cpp#L107-L118).
- El objeto de audio es global estático; la ruta PC de sonido de menú comprueba `isInitFlag()`: [m_Do_audio.cpp, líneas 27–51](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/m_Do/m_Do_audio.cpp#L27-L51).
- La carga espera los comandos, llama a `init` solo con heap disponible y activa `onInitFlag()` fuera de esa condición; `mDoAud_Execute` no crea audio durante shutdown/retorno a menú: [líneas 118–182](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/m_Do/m_Do_audio.cpp#L118-L182).
- `Z2SceneMgr::getWaveLoadStatus` obtiene el section heap y lo desreferencia para consultar el banco: [Z2SceneMgr.cpp, líneas 1990–2001](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/Z2AudioLib/Z2SceneMgr.cpp#L1990-L2001).

Conclusión estática reutilizable: el contrato de disponibilidad debe seguir recursos, inicialización y reset, además del puntero global. Un número fijo de frames de espera no demuestra esas condiciones. La causa exacta del crash histórico sigue siendo la interpretación del informe; no se ha leído un dump ni reproducido aquí. **STATIC_CROSSCHECKED, HIST-005**. Véase [audio, partículas y efectos](systems/audio_particles_effects.md).

### 2. La ABI de punteros a miembro requiere representación nativa

FIX02 reportó para `daAlink_c` un puntero a miembro de 24 bytes en MSVC y la necesidad del registro extendido: [IMPLEMENTATION, líneas 60–68](https://github.com/iscoremusic26-maker/Mods-Duskligh/blob/fe47c8b828939829914d466a425cb1e2c0223cd9/DEVF/CP19_FIX02_UNIVERSAL_AUDIO_BLACK_SHIELD_CHIP/IMPLEMENTATION.md#L60-L68). Esto no se usa como medida universal de clases C++.

El SDK upstream reserva una forma extendida diferenciada con capacidad 24 y función materializadora: [api.h, líneas 235–254](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/sdk/include/mods/api.h#L235-L254). La implementación de plantillas elige el registro extendido cuando `sizeof` supera la capacidad original y copia la representación nativa mediante un helper: [meta.hpp, líneas 306–331](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/sdk/include/mods/meta.hpp#L306-L331). **STATIC_CROSSCHECKED, HIST-006**. No trasladar offsets GC/Wii ni un tamaño de miembro de otra jerarquía a Windows x64. El detalle de resolución y trampolines se mantiene en [HOOKING_AND_ABI.md](HOOKING_AND_ABI.md).

### 3. Un canary fallido sigue siendo un bloqueo, aunque compile

El cierre CP21 conserva `LINK_LAYOUT_CANARY_FAILED_LIFESTEAL_DISABLED` como riesgo pendiente y su prueba humana exige no declararlo corregido sin observación y traza: [DELIVERY, líneas 45–47](https://github.com/iscoremusic26-maker/Mods-Duskligh/blob/fe47c8b828939829914d466a425cb1e2c0223cd9/DEVF/CP21_PUBLIC_RELEASE/DELIVERY.md#L45-L47), [HUMAN_TEST, líneas 9–12](https://github.com/iscoremusic26-maker/Mods-Duskligh/blob/fe47c8b828939829914d466a425cb1e2c0223cd9/DEVF/CP21_PUBLIC_RELEASE/HUMAN_TEST.md#L9-L12). **DOC_CONTRACT histórico, HIST-007**.

Se reutiliza la regla de evidencia: una sonda de layout, import library o prueba COFF no demuestra que se esté leyendo el objeto correcto en su estado vivo. Esta campaña no examinó el log crudo del canary, no diagnostica su causa y no certifica ninguna corrección de layout. Estado del caso: **NOT_VERIFIED** para su causa y resolución.

### 4. Registro de edición de stage y actor vivo son entidades distintas

CP20 explica que sus receipts de edición carecen de ActorID y no justifican atribuir una instancia a otro contexto: [IMPLEMENTATION, líneas 7–11](https://github.com/iscoremusic26-maker/Mods-Duskligh/blob/fe47c8b828939829914d466a425cb1e2c0223cd9/DEVF/CP20_EXPLICIT_BLUE_RED_BLACK/IMPLEMENTATION.md#L7-L11). El contrato SDK devuelve un `StageActorHandle` de 64 bits y habla de registros retirados al detach: [stage.h, líneas 13–39](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/sdk/include/mods/svc/stage.h#L13-L39).

La implementación asigna handle/mod/secuencia al insertar una edición y devuelve `MOD_OK`; la creación posterior recorre las adiciones activas que coinciden en sala/capa y llama al callback de creación: [stage.cpp, líneas 139–165](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/mods/svc/stage.cpp#L139-L165). Eliminar un handle o un mod borra sus registros, sin una llamada de destrucción de actor en esas funciones: [líneas 200–219](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/mods/svc/stage.cpp#L200-L219). **STATIC_CROSSCHECKED, HIST-008**.

Por eso `MOD_OK` no prueba aparición, terreno correcto ni vida de una instancia. El rollback histórico exige recarga de escena/reinicio antes de juzgar la retirada de actores ya cargados: [CP21 RECOVERY, líneas 3–7](https://github.com/iscoremusic26-maker/Mods-Duskligh/blob/fe47c8b828939829914d466a425cb1e2c0223cd9/DEVF/CP21_PUBLIC_RELEASE/RECOVERY.md#L3-L7). Véase [stages, rooms y layers](systems/stages_rooms_layers.md).

### 5. Mantener contratos versionados y comprobar capacidades

La implementación CP20 separa V1 y V1.1; documenta tamaños/versiones/capacidades explícitos y evita sobrecargar campos antiguos: [IMPLEMENTATION, líneas 5–7](https://github.com/iscoremusic26-maker/Mods-Duskligh/blob/fe47c8b828939829914d466a425cb1e2c0223cd9/DEVF/CP20_EXPLICIT_BLUE_RED_BLACK/IMPLEMENTATION.md#L5-L7). Es un ejemplo histórico de diseño de servicio privado, **no un servicio adicional del SDK oficial**.

El SDK oficial define majors incompatibles, minors aditivos, campos nuevos con `SERVICE_HAS` y puntero no nulo, y diferencia imports declarados de lookup dinámico sin garantía de orden: [api.h, líneas 76–118](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/sdk/include/mods/api.h#L76-L118). El registro usa ID+major y rechaza minor insuficiente al resolver: [registry.cpp, líneas 145–160](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/mods/svc/registry.cpp#L145-L160). **STATIC_CROSSCHECKED, HIST-009**. No trasladar los tamaños privados de CP20 a ninguna interfaz oficial.

### 6. La presencia de archivos en el checkout no garantiza que lleguen al bundle

CP21 registra `RES_DIR res` en sus CMake: [DELIVERY, línea 24](https://github.com/iscoremusic26-maker/Mods-Duskligh/blob/fe47c8b828939829914d466a425cb1e2c0223cd9/DEVF/CP21_PUBLIC_RELEASE/DELIVERY.md#L24). La función oficial añade `res` al paquete y copia sus archivos solo bajo `if (ARG_RES_DIR)`: [ModSDK.cmake, líneas 350–358](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/cmake/ModSDK.cmake#L350-L358). **STATIC_CROSSCHECKED, HIST-010**. Comprobar el bundle final es distinto de comprobar la fuente; el informe histórico de auditoría de descarga lo reconoce en [DELIVERY, líneas 36–43](https://github.com/iscoremusic26-maker/Mods-Duskligh/blob/fe47c8b828939829914d466a425cb1e2c0223cd9/DEVF/CP21_PUBLIC_RELEASE/DELIVERY.md#L36-L43).

### 7. Identidad del recurso, disponibilidad y contenido son preguntas separadas

El informe FIX02 distingue la inferencia de grupo de audio desde la fuente, la existencia/exportación de APIs, los límites de memoria y lo que solo se confirma al oír el resultado: [SOURCE_AUDIT, líneas 15–33](https://github.com/iscoremusic26-maker/Mods-Duskligh/blob/fe47c8b828939829914d466a425cb1e2c0223cd9/DEVF/CP19_FIX02_UNIVERSAL_AUDIO_BLACK_SHIELD_CHIP/SOURCE_AUDIT.md#L15-L33), [IMPLEMENTATION, líneas 70–76](https://github.com/iscoremusic26-maker/Mods-Duskligh/blob/fe47c8b828939829914d466a425cb1e2c0223cd9/DEVF/CP19_FIX02_UNIVERSAL_AUDIO_BLACK_SHIELD_CHIP/IMPLEMENTATION.md#L70-L76). **DOC_CONTRACT histórico, HIST-011**.

No se adoptan aquí sus offsets binarios, presupuestos ni estrategia residente como solución general. No se examinó contenido de ROM/ARC/AW/BAA ni se reprodujo el desensamblado histórico. Antes de cualquier integración futura debe separarse la prueba de que un registro existe, la disponibilidad de su dependiente y la prueba de que el contenido corresponde a lo esperado.

## Cobertura y continuidad

Se examinaron diez documentos históricos de implementación/auditoría/recuperación/prueba humana, metadata de cuatro PR, dos workflows exactos y metadata/jobs de dos runs. La profundidad es selectiva: fueron contrastados los mecanismos generales de audio readiness, ABI de miembros, stage-edit ownership, versiones de servicios y `RES_DIR`. No se revisaron íntegros los 3.382 registros del árbol histórico, los cientos de blobs del ledger ni los binarios de las entregas.

Para continuar, consultar primero esta ficha y su evidencia `HIST-*`; usar el SHA compilado para preguntas de CI y el cierre documental para sus informes. Profundizar solo si una pregunta nueva requiere otra evidencia histórica. El canary pendiente necesita evidencia adicional; no corresponde repetir pruebas sintéticas para declararlo resuelto. Los informes de runtime humano aquí citados no fueron abiertos en bruto y conservan el nivel de **reporte histórico**, no `HUMAN_RUNTIME_OBSERVED` de esta campaña.

Cobertura: READ/CROSSCHECKED selectiva según SYSTEM_INDEX y los niveles de cada evidencia; ninguna ruta constituye prueba runtime Windows/DX12.
