# Enemy Posture System 0.11.3 — HUD FIX01 PRIVATE TEST

**Prueba parcial, HUMAN_RUNTIME_PENDING.** El combate de 0.11.2 se conserva. No se ha probado esta versión en una partida Windows/DX12. **La alineación exacta con Enemy Health Bars CP06 (bug C) NO está corregida.** La exclusión visual B cubre los contextos J2D admitidos; no constituye una garantía universal de ausencia de superposiciones.

Fuente compilada: `0c50f035a55d627379d6f6e2dcd8a04297f905ed`. Consulta [RESULTS.json](RESULTS.json) para el run, archivo, tamaño, SHA-256 y descarga finales. El commit documental posterior no es el commit compilado. ID invariable: `dev.posture.post05_selective_reactions`, versión `0.11.3`.

## Instalar solo el candidato de esta entrega

1. Cierra Dusklight. Conserva una copia del `.dusk` 0.11.2 fuera de la carpeta activa de mods.
2. Descarga el artefacto **TEST** enlazado en RESULTS.json y extrae su ZIP. Compara el SHA-256 del archivo `.dusk` con el valor de RESULTS.json; no confundas ese hash con el del ZIP del artefacto ni con el de la DLL.
3. Sustituye únicamente el `.dusk` del Enemy Posture System. Debe quedar **una sola versión** del ID anterior en la carpeta activa. No cargues juntos 0.11.2, el primer candidato 0.11.3 de `24a4e188...` y este candidato actualizado.
4. Conserva los otros siete mods: DEVF 0.15.0, Bokoblin Expansion 0.17.0, EHB CP06, HM CP11, Zora Swim, Luau Support y Randomizer. No añadas Lazy Shield Rework; su continuidad de defensa ya está integrada. Mantén DX12 y las configuraciones actuales.
5. Comprueba en el inicio del log el ID/versión y `POST_HUD_FIX01_INIT`. Ruta normal: `SCREEN_GEOMETRIC_REFLOW+GFX_FRAME_PAIR`. Si aparece `FALLBACK_ORIGINAL_BAR_NO_PROMPT_HIDING`, la ruta nueva no está activa: ese ensayo no valida la corrección.

Esta entrega no instaló nada ni modificó EXE, SDK, ISO/ROM, partidas, configuraciones o los demás mods.

## Recorrido de prueba humana

Realiza el recorrido a 1920×1080, primero a 30 FPS y después a 60 FPS donde el equipo lo permita. Prueba también caídas irregulares y un cambio de viewport/aspecto si ya es una opción normal del host. No se exige cambiar de backend.

1. **Scoop y contexto.** Con botella adecuada y contenido realmente recogible, alterna botella, entra/sal del alcance y recoge el contenido. Repite sin enemigos, tras combate, con la barra visible, durante su hold/fade a cero y con ella ausente. Repite tras una sala nueva, después de mostrar otros prompts y con las botellas disponibles. Scoop debe conservar el texto y botón nativos y permitir la acción. Comprueba también Open, Talk, Pick Up y Use cuando el juego los ofrezca. No se crean etiquetas para acciones que el juego no ofrece.
2. **Exclusión espacial.** Con la barra activa, provoca Jump, Shield Attack, Helm Splitter y acciones A/B/R simultáneas o alternadas. Mira texto, iconos, halo, destellos Pikari y mensajes auxiliares. Deben quedar fuera de todo el marco/pulso de postura. Una pista trasladada tampoco debe tapar otra pista, corazones o mensajes. Cuando la barra termina su fade, las posiciones nativas deben recuperarse sin saltos acumulados ni residuos.
3. **EHB, pendiente.** Observa Blue, Red, Black y Black Fury con ambas barras, caminando, girando, golpeando, recibiendo daño, stagger, caída, down/getup, pendiente y cambios de cámara/zoom. La referencia deseada es una separación constante en ambos ejes; un cambio mayor de un píxel relativo es evidencia útil. **Este candidato conserva el anclaje anterior; no se espera que cierre C.** No interpretes una imagen de laboratorio como una captura del juego.
4. **Parpadeo.** Mantén postura propia para que la barra de Link deba estar visible. Da 10–20 espadazos seguidos, incluyendo impactos no mortales, muerte, cruce de 100, Helm Splitter y Finish cuando correspondan. Observa si falta algún fotograma, cambia alfa o se duplica la barra. Distingue el fade normal cuando se agota la postura y las ocultaciones nativas de menú/evento.
5. **Ciclo de vida.** Pausa y vuelve, abre/cierra menús, cambia de sala, entra/sale de eventos y alterna humano/lobo cuando sea posible. Prueba el primer y último fotograma de la barra y HUD recreado. No deben quedar posiciones modificadas ni barras fantasma.
6. **Uno contra uno y grupo.** Repite con un Bokoblin y con varios de las tres variantes. El laboratorio conserva el límite de 16 barras y el tratamiento de 65+ actores; hace falta observación visual real para comprobarlos en una partida.
7. **Regresión de combate.** L fija, R mantenido con fijación protege, R+B activa Shield Attack/parry; B sin R sigue siendo espada. Provoca ruptura de Link: 75 ticks activos (~2,5 s a 30 Hz), movimiento/espada permitidos, escudo y esquivas voluntarias bloqueados durante la ventana; pausa congela el cómputo. Tras desbloqueo, suelta R y vuelve a pulsarlo. Comprueba rearme enemigo 25 de pie / 0 tras levantamiento completo y restricciones de furia.
8. **Coexistencia.** Escenario B: los ocho mods anteriores, HM ×1; HM ×2 solo si forma parte de un entorno de prueba permitido. El escenario A (postura solo) debe hacerse en un entorno de prueba permitido, sin alterar la instalación principal para obtener evidencia. No se declara A/B ejecutado con 0.11.3.
9. **Informe.** Conserva el log completo generado por esa ejecución. Anota versión/SHA, acción, sala, cámara, estado de la barra, FPS/resolución y si se desplazó otra pista. Una captura o vídeo corto ayuda a relacionar geometría y fotograma; los contadores por sí solos no prueban visibilidad.

## Diagnósticos y STOP

`POST_HUD_FIX01_TRANSITION` relaciona serial de presentación, tick, alfa, admisión del HUD nativo, viewport/banda y Scoop ofrecido por `mBottleStatus`. Ese campo no demuestra que el texto se haya rasterizado. `POST_HUD_FIX01_SUMMARY` cuenta frames requeridos/dibujados, traslados, restauraciones, contextos rechazados, límites, pares incompletos, intersecciones de bounds restantes y contactos ponderados de espada cerca de una ocultación. Las trazas de transición tienen tope; no se escribe una línea por fotograma. Los logs LNK01 antiguos describen un componente retirado: la autoridad de la ruta nueva es `POST_HUD_FIX01_*`.

**Detén la prueba y vuelve a 0.11.2** ante crash, corrupción de HUD, acción vital ofrecida cuyo prompt no se ve, entrada bloqueada, caída importante de FPS, barras fantasma, duplicación/parpadeo persistente o regresión de postura/defensa. Contextos J2D recortados, otra proyección, árbol excesivo, matriz singular o falta de espacio se dejan intactos y se cuentan: puede persistir una superposición en esos casos. Tampoco está certificada la colisión entre pantallas distintas o con dibujado que no pasa por J2DScreen.

## Rollback

Con juego cerrado, retira solo el `.dusk` 0.11.3 y restaura el único 0.11.2:

`POSTURE_BALANCE_SESSION01_0_11_2_BLUE_RED_BLACK_STANDING_REARM25_PRIVATE_TEST_windows-amd64_a0a4d43718bc.dusk`

SHA-256: `2aa715980bc81af0db13622fc9e210100bcd973cd1255044d570a91f092eba0a`.

[Artefacto 0.11.2 — run 41570019310](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41570019310/artifacts/13201587185). Conserva los otros siete mods. No hace falta editar partidas ni configuraciones.
