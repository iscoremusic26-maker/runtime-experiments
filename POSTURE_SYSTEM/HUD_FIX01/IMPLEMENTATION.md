# HUD FIX01 0.11.3 — implementación y límites

## Dictamen

PRIVATE TEST acumulativo sobre el **commit compilado** 0.11.2 `a0a4d43718bca99e7e9cbfd2d1860cac6da1718d`. Fuente candidata: `0c50f035a55d627379d6f6e2dcd8a04297f905ed`, rama `feature/posture-hud-fix01-0-11-3`. El estado binario final y las etiquetas individuales están en [RESULTS.json](RESULTS.json). No hay HUMAN_RUNTIME_PASS.

| Incidencia | Cambio real | Límite de la conclusión |
|---|---|---|
| A, Scoop/contexto | Se desactiva el ocultamiento persistente de la raíz y la máscara de slots de brillo. Se traslada presentación J2D que compite con la barra; no se modifican acciones ni textos. | Falta comprobar disponibilidad y presentación real de Scoop/Open/Talk en Windows. El log anterior no contiene eventos explícitos de Scoop. |
| B, invasión de barra | Exclusión geométrica de máximo marco/halo/pulso; reflow PRE/POST en pantallas J2D admitidas. La continuación evita colocar grupos sobre otros elementos de la misma pantalla y preserva elementos no competidores. | PARTIAL: no se garantiza la cobertura universal de otras rutas, pantallas independientes, clipping, texto que desborde sus bounds ni situaciones sin espacio. |
| C, alineación EHB | Ningún cambio al anclaje/interpolación enemigo. | BLOCKED: referencia exacta CP06/API de anclaje no disponible; no hay delta relativo real por frame. |
| D, parpadeo Link | Snapshot de presentación y pintado independiente AFTER_HUD, una vez por presentación admitida, conservando hold/fade. | El fallo visual original no tiene correlación causal suficiente en el log. Es una corrección de dependencia de dibujo, todavía pendiente de prueba real de espadazos. |

## Evidencia humana anterior y causalidad

Se leyó entero `dusklight-20261102-223104.log`: 6.395.642 bytes, 29.945 líneas, SHA-256 `483b285fa9b2d86027323318558f1f389fceb5a64558ea5cae65f3cf3bb86a0a`. No se modificó ni se subió el log crudo. El resumen saneado está en EVIDENCE/RUNTIME_0_11_2_AUDIT.json.

Al cierre de LNK01: 144 escrituras de ocultamiento de raíz, 15.008 comprobaciones con raíz oculta, 4.999 máscaras/restauraciones de brillo y 15.402 dibujos de un objeto distinto de `mpEmpButton`. No se deduce que esos objetos fueran todos cinematográficos. Los cinco meters y 144 resoluciones de prompt indican ciclos de creación/reutilización; no son 144 interacciones de Scoop. Los contadores antiguos de ocultación correcta no prueban ausencia de superposición de otras superficies.

La última muestra POST07 disponible, **no el total de sesión**, llega a 17.124 executes / 50.731 draws; `refused=0`, `hud_not_queued=0`, `skipped=0`, 20.608 hits / 241 misses de interpolación. No hay `POST07_HUD_DISABLED`. Estos hechos **no prueban** que cada espadazo perdiera una cola o que cada miss causara parpadeo. El log no trae alfa/serial de dibujo por contacto ni coordenadas de EHB. Sus resúmenes del HUD terminan antes que los resúmenes dedicados de Link por los límites de logging; no se extrapolan al cierre.

Hay ocho mods encontrados con las versiones declaradas. Las 155 líneas ERROR son ventanas `PERF_WINDOW` de Expansion etiquetadas `MEASUREMENT_NOT_AN_ERROR`: p50 entre ticks de simulación = 33.500 µs en sus ventanas; mediana de p95=34.000 µs y de p99=34.481 µs. No son FPS de presentación, coste GPU ni coste de este HUD. Se registran además 187 advertencias `aurora::texture` y 27 `CalcDivideInfo` del host; su relación causal con este HUD no está demostrada y no se modifican texturas ni otros mods. La advertencia de `setRStatus` inlined se conserva como limitación de la defensa heredada; no se usa ese hook para ocultar prompts y no se alteró defensa para arreglar texto.

## A/B: ruta nativa verificada y leases

Autoridad: Dusklight 2.0.3 `40457c6adb381928e4b5fef6ed459ed291edd5e2`, EXE oficial SHA-256 `ffa992038d04290654b8907a7663f4dcf62083beaad2b35014fdfd901d390049`.

`daAlink_c::execute` puede ofrecer `BUTTON_STATUS_SCOOP` por `dComIfGp_setBottleStatus` cuando existe objetivo de recogida y el estado de botella/Link lo permite. `dMeter2_c` captura y limpia estados, `drawButtonBin` determina énfasis tras contar botellas, y `check2DContents` reparte hasta dos slots de énfasis con prioridades. `getActionString` selecciona el texto nativo; la acción de botella procede por la lógica nativa de `d_a_alink_bottle.inc`. No se reduce Scoop a un icono `BUTTON_BIN_e` ni se cambia esa admisión/selección.

`dMeterButton_c::draw` dibuja por rutas diferentes `mpButtonScreen`, `field_0x00c`, `mpScreen`, `mpTextScreen`; además obtiene posiciones globales para out-font y Pikari. El viejo ocultamiento solo cubría una raíz de un prompt vivo. En 0.11.3 esa política queda permanentemente desactivada. Los helpers/modelos heredados se conservan auditados pero no se activan; no hay show/hide global ni escritura en alfa, inventario o estados de acción.

El único nuevo objetivo nativo es `J2DScreen::draw`, PRE/POST síncronos. El PRE se admite únicamente dentro de la presentación activa de Link y con contexto ortográfico actual no recortado. Recorre <=512 panes y profundidad <48, usa visibilidad/alfa heredadas, matrices y bounds vivos. Replica la transformación PC del canvas 608 y `n_43`; la predicción de raíz llama al `makeMatrix` virtual del pane vivo y restaura inmediatamente sus campos/matriz. ABI estático más EXE: matriz +0x50, escala X +0xcc, traducciones +0xd4/+0xd8, scissor de J2DScreen +0x128; firma y metadata Windows auditadas. No se adivina memoria de otros mods.

El rectángulo de exclusión en `hudfix_core.hpp` incluye la máxima expansión del pulso, remates y margen de ocho píxeles de referencia. Es constante para un viewport durante el fade/pulso, evitando jitter por el tamaño instantáneo del brillo. La traslación se convierte mediante la inversa XY del padre; un padre singular rechaza el plan completo antes de escribir. Los grupos conservan su relación interna cuando pueden moverse juntos. Las traducciones/matriz local de descendientes se guardan y restauran exactamente en POST; los argumentos de raíz son valores de la llamada de dibujo. Los caches globales producidos por el draw reflejan su posición dibujada para que out-font/Pikari posteriores la sigan. No se retienen direcciones después del par PRE/POST; no hay acumulación sobre los campos de diseño ni promesa de que todos los caches derivados sean bit-idénticos al draw sin mod.

### Corrección acotada de la continuación

El candidato anterior `24a4e188...`, run **41580806911**, sí pasó build, independent-download y 391 mutaciones. Su `.dusk` verificado fue 120.575 bytes, SHA-256 `6a3399338771d9b2c9aef1c819ea6e01796c59a2cdaa7e071988e43bda233968`. No se interpreta la interrupción por uso como fallo de ese CI.

La auditoría adicional reprodujo un contraejemplo **en los callbacks reales con árbol J2D simulado**: una pista existente ocupaba y=330..360 y un prompt, tras despejar Link, acababa en y=348,4..373,4; `introduced_overlap=1`, `bar_clear=1`. No es una observación nativa ni una captura de Scoop. Justifica cambiar únicamente el núcleo nuevo de geometría y sus pruebas, y por ello generar otro artefacto.

Ahora se comprueban obstáculos de la **misma pantalla**, incluidas las posiciones de grupos ya trasladados. Se exploran cuatro franjas con empuje monótono y un máximo de 32.768 comprobaciones de colisión por plan; una comprobación incompleta nunca se toma como espacio libre. Solo puede moverse un grupo cuyos renderables compiten con la banda: un padre que incluye corazones/pistas ajenas no se desplaza entero aunque su bbox quepa en otro lugar. El algoritmo busca una posición válida entre esas franjas; no promete un óptimo global en toda la interfaz. Sin espacio o presupuesto suficiente conserva la presentación nativa y cuenta intersecciones restantes. Puede quedar superposición, y B se mantiene PARTIAL.

No existe aún un atlas de ocupación compartido de todas las pantallas y rutas directas. Un nuevo prompt en otra pantalla, un dibujo fuera de J2DScreen, sombras/glyphs fuera del bbox con margen, clipping, proyección distinta o un árbol excesivo siguen requiriendo prueba/diagnóstico. No se oculta la acción para disimular esas limitaciones. El fondo y los elementos decorativos de pantalla completa tampoco se certifican por el modelo de hojas renderables.

## D: presentación independiente

El nuevo servicio **opcional** GfxService 1.4 ofrece callbacks oficiales BEFORE_HUD/AFTER_HUD en el hilo de juego para cada presentación. `FEATURES webgpu` habilita sus cabeceras SDK; no crea recursos WebGPU, no construye el host y no cambia DX12 a Vulkan. Los hooks se emparejan y se retiran al descargar el mod.

BEFORE_HUD fija una sola copia de alfa/geometría/visibilidad, con admisión nativa, presencia del meter nativo en su lista y viewport válido. Ese mismo snapshot decide la reubicación y el pintado de Link. AFTER_HUD pinta una vez a partir de la copia. El paquete POST07 sigue pintando enemigos; su rama Link se evita mientras la ruta nueva está activa. La animación de PlayerHud avanza una vez por tick, sin avanzar en frames de presentación extra: no se elimina hold/fade ni se convierte en barra siempre visible.

El pintado de Link ya no depende de `hg.frame.n`, `hg.visible`, una nueva muestra enemiga, la disponibilidad de su paquete XLU o el observador enemigo deshabilitado. Sigue respetando ocultaciones nativas, pausa/menú/eventos y la alfa propia. Si falta GfxService/hook, se conserva la barra antigua como fallback con prompts visibles y sin ocultamiento persistente. Esto no demuestra la causa exacta del parpadeo original. Los contactos ponderados de espada se leen de contadores, sin tocar actores/combate.

## C: referencia EHB y bloqueo

POST00 documenta EHB CP06 en un repositorio **local sin remoto**, commit `e9b42a4dab2e7a4e0e69b2d634dedacaa7ce2102`; `game_bars.cpp` tenía SHA-256 `8a726dbe5db9e36ba95775b50e1071604856655857db2333821f8ce39624f3e1`. Esas rutas no existen aquí. Se revisaron nombres de fuentes/worktrees accesibles y los índices de 25 ZIP disponibles: no apareció la referencia CP06 ni una API de anclaje con ABI/versionado verificables. No encontrar una API no demuestra que nunca exista.

POST07 resume reglas equivalentes (head estable, +8, proyección y franja de vida ±14/±2), pero eso no basta para replicar el historial de seguimiento, identidad, comienzo del muestreo ni fase/clave de interpolación de EHB. La asimetría de `stable_head_height` que solo sube y los historiales independientes son riesgos reales de diseño; el log no proporciona su delta contra EHB en el mismo frame. Cambiar solo esa asimetría sin fuente auténtica podría empeorar la paridad.

Por ello `hud_core.hpp`, `Anchors`, los helpers de interpolación y el anclaje/proyección enemigo permanecen intactos frente a 0.11.2. No hay offset arbitrario, dependencia obligatoria, lectura de memoria de EHB o hook a su DLL. **No se declara C resuelto, LAYOUT/POSITION_PASS ni error <=1 px medido.**

## Regresión, costes y entrega

La barrera compara 107 cuerpos fijados (incluye tres nuevos escritores visuales) y los 15 encabezados heredados con la base compilada. Solo normaliza el cambio de versión de lifecycle 0.11.2 a 0.11.3. Los pesos, POST06, HP/regen, atribución, IA y Manual Shielding no cambian. Hay 17 objetivos de hook y 49 imports del juego en 0.11.3 frente a 16/48 en 0.11.2; la diferencia es exclusivamente el draw de J2DScreen. No cambian CRT/imports de combate. La continuidad añade GfxService opcional, no EHB.

La suite final debe confirmar MSVC x64, PE/imports, 20 negativos PE, dos negativos de instrucciones reales de escudo/B, cinco positivos/diez negativos PMF estáticos, 18 labs y el adaptador de producción sobre J2D simulado. Las 380 mutaciones heredadas y 13 HUD tienen límites de compilación/ejecución; TIMEOUT/ERROR nunca equivalen a KILLED. g++ ASAN/UBSAN conserva las regresiones heredadas y vuelve a ejecutar lo afectado; CI vuelve a comprobar todo el candidato. Los números y hashes finales proceden de los artefactos de ese run y están en RESULTS/EVIDENCE.

No se ejecutó juego Windows, prueba A/B con ocho mods, HM ×2 ni una medición de coste/FPS de este HUD. Los renders de referencia son LAB, no capturas del juego. El coste está acotado y no usa memoria dinámica en el camino del mod, pero su efecto real sobre Intel UHD queda pendiente de la prueba humana.

La descarga se comprueba por un job separado y de nuevo localmente desde el ZIP publicado: nombre, tamaño, SHA-256, mod.json, DLL, imports y hooks. El commit documental posterior solo añade HUD_FIX01 y evidencias saneadas; no se le atribuye el binario. No se hace PR, merge, tag, release ni instalación. Ver [README_TEST_0_11_3.md](README_TEST_0_11_3.md) para prueba y rollback.
