# DEVF CP04.4 — Bokoblin negro individual

**Dictamen: CP04_4_BLOCKED_WITH_EVIDENCE.** No hay implementación de recoloreado admitida, DLL ni paquete TEST. Esta revisión identifica condiciones concretas pendientes; no demuestra que todo recoloreado por instancia sea imposible.

Base inmutable: CP03 humano `139d9329f7a2d5d191b6e0ef7149ac9bbf82d29f`. Rama privada nueva: `feature/devf-cp04-4-black-bokoblin`. [PR draft #30](https://github.com/iscoremusic26-maker/Mods-Duskligh/pull/30), sin merge. El checkpoint temprano `a3c6b934e27c40c2044dfc6c83eb835c0b0a1c95` ya conserva el alcance y las referencias.

Objetivo conservado: un E_OC2 adicional de 150 HP, F_SP121/3/6, home (-1250,-6304.00830078125,60750), modelo negro carbón con detalle y un E_OC2 original del mismo modelo intacto. CP03 mantiene su selección individual, StageService y write único PRE_FIRST_EXECUTE 220→150. No se ha cambiado ese código ni `field_0x560`. Su paquete histórico de 11975 bytes / SHA256 `0d9882b072fe5cd6248c16a181171a47364e1acf5870503c1eb2f39c668b4344` no se recompiló ni sobrescribió; ese hash es la referencia previa, no una nueva descarga.

Resultados:
- Cosmetics recolorea copias de texels pero registra reemplazos por contenido/formato/tamaño, sin ActorId: no proporciona aislamiento individual.
- J3DModel, matrices y packets son de instancia; J3DModelData, materiales, shapes y texturas conservan referencias compartidas.
- Hay un display list diferido **privado por shape** y un puntero de color de vértices **por modelo**. No se niegan estas posibilidades reales. Falta demostrar que los canales del E_OC2 producen el negro deseado, que la ruta persiste durante regeneración/interpolación y que la memoria se retira sin lectores pendientes.
- Un loader nativo existe, pero carga un grafo que presta datos del buffer y convierte arrays en el buffer. Una copia superficial o volver a cargar el buffer del recurso original no es una copia privada segura.

La decisión, matriz de propiedad y dos rutas se encuentran en [ROOT_CAUSE_AND_CHOSEN_ROUTE.md](ROOT_CAUSE_AND_CHOSEN_ROUTE.md). [HUMAN_TEST.md](HUMAN_TEST.md) describe el mínimo dato que falta y un protocolo futuro condicionado; hoy no autoriza instalación ni ejecución. [TEST_RESULTS.md](TEST_RESULTS.md) separa revisión estática, evidencia reproducible y runtime.

Cloud seleccionado está failed (error al consultar capacidades del executor). No se ha leído ni escrito un workspace local de esa máquina. GitHub permite recuperar y publicar el checkpoint. El workflow nuevo verifica exclusivamente procedencia fuente, preservación y tag; no compila juego/mod ni sustituye MSVC por Linux.

CP04.3: el NO-GO runtime `RESOURCE_84ED_MISSING_NO_FALLBACK` (actor 147, banco 1) se conserva como evidencia aportada por el usuario. No se retomaron partículas 0x84ED/0x029D, ni auditorías CP01–03, ubicación, salud o SDK. CP05/CP06 no iniciados.

Verificación Windows de procedencia ejecutada: [run 38649308109](https://github.com/iscoremusic26-maker/Mods-Duskligh/actions/runs/38649308109), SUCCESS. 32 fuentes contrastadas y todas las rutas/refs anteriores preservadas. No MSVC/build/render PASS. Resultado completo en TEST_RESULTS y evidence/static-audit-result.json.
