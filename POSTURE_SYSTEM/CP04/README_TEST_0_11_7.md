# LIGHT FADES TWICE · CP04 0.11.7 · PRIVATE TEST

<!-- VERIFIED_DELIVERY -->

**HUMAN_RUNTIME_PENDING · VISUAL_SHIELD_MOTION_HUMAN_PENDING.** La fuente implementa el Blue2+2 y el rearme animado reutilizable. Compilar y pasar laboratorios no certifica la animación visible ni el resultado defensivo en Windows/DX12.

## Instalación y retorno

Con el juego cerrado, guarda fuera de la carpeta de mods el `.dusk`0.11.6. Coloca **solo un** `.dusk`0.11.7 de este ID en su lugar: `dev.posture.post05_selective_reactions`. Conserva intactos los otros siete mods y sus configuraciones. No dupliques0.11.6/0.11.7 en carpetas que cargue el modloader. No cambies EXE, ROM, SDK ni saves.

Rollback humano aprobado: [CI41703645193](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41703645193), [artifact13264179241](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41703645193/artifacts/13264179241).

`POSTURE_CP02_CP03_0_11_6_PRIVATE_TEST_windows-amd64_8c72aec291a7.dusk`

SHA-256: `0aa8e8d2941d644a33765fe288bc3f9867cc1e188506fed691caf069c63fb019`.

Si hay regresión, cierra el juego, retira0.11.7 y devuelve **solo** ese0.11.6. No cargues ambos. El artifact de respaldo expiraba según GitHub el3 de diciembre2026 a14:44:30, Panamá(UTC−5); conserva tu copia.

## A/B y escenarios auténticos

A: prueba el mod solo con un **E_OC nativo ya existente** que el log identifique como Blue. No se asegura aquí un spawn/horario/sala nativa que no se haya observado. No edites el save ni inventes colocaciones para esta prueba.

B: verifica en el log ocho mods realmente cargados: EVF0.15.0, Bokoblin Expansion0.17.0, Enemy Health BarsCP06, Enemy Health MultiplierCP11, Zora Swim, Luau, Randomizer y este mod. Una copia shadowed de Zora no cuenta otra vez. Para B existen en `CP21_PUBLIC_RELEASE/inputs/encounters.json` las colocaciones Blue `bokoblin-001` y `bokoblin-002`, stageF_SP121, room10, layer6. Son referencias **de configuración**, no prueba de aparición en tu partida: confirma su admisión/contexto antes de usarlas. Utiliza los encuentros existentes para separar uno o atraer compañeros y comprobar los tres niveles; respeta el grito/reclutamiento y los leashes.

| Caso | Qué comprobar en juego |
|---|---|
| Blue solo, pareja, grupo≥3 | Tanto ataques normales como combos. Normales1/1,15/1,30 según compañeros; combo1/1/1,5/1,5 en todos. El cambio de compañeros no retima un swing. |
| Frecuencia | Cuenta BLUE_OPPORTUNITY, SELECTED y NORMAL durante muchas oportunidades. Cada decisión es1/2; una muestra corta no tiene por qué dar50%. No contar ticks ni seleccionados abortados como nuevas tiradas. |
| Combo sin parry | Cuatro espadazos visibles reales: normal–pausa–normal–pausa–rápido–pausa corta–rápido. Esquivar no debe cancelar por sí solo ni crear seguimiento/teletransporte. |
| Escudo ordinario | R manual, L+R, B normal, nuevoR+B. Sin escudo o sin rearme válido: no parry. El primer Shield Attack debe mover el escudo. |
| Parry3 y4 | Evita parar1/2. Usa dos pulsaciones nuevasR+B: **dos arcos de escudo visibles**, dos contactos y feedback separados, dos seriales. B mantenido no debe repetir. |
| Parry1/2/3 desde0 |40→80→100 y ruptura sin cuarto swing. No se reduce el peso40 para facilitar la prueba. |
| Bloqueo/parry<100 | El Blue hace el retroceso nativo y continúa después. Esa reacción puede cambiar el intervalo entre contactos; no debe quedar pensando ni inventar un golpe. |
| Link dañado/guard-break | Sin rearme rápido durante daño,75 ticks de penalización o sin soltarR/rearmar. Conserva las prohibiciones de esquiva. |
| Prioridades | Daño/muerte del Blue, caída/agua, evento, cambio de sala/lobo/pausa cancelan con seguridad; no se restaura un ataque tras una ruptura. Helm Splitter/Finish y Scoop conservan prioridad. |
| HUD | Corazones, rupias, mapa y botones; Scoop/Open/Talk; Jump/Shield Attack/Helm Splitter; barra de Link mientras golpea10–20 veces; barras enemigas con EHB moviéndose y cayendo. |
| Regresión | Regen CP02 por bandas10/7/4/2/1 tras60 ticks elegibles; CP03[−1,+7]/9; rearme25/0; bonusx1,5 una vez; Red/Black/Fury, chip y lifesteal normales. |

Si puedes grabar a60fps, revisa el inicio del segundo arco **antes** del segundo contacto. Eso sigue pendiente hasta tu prueba; los logs NATIVE_ANIMATION_STARTED/VISIBLE_CLIP_ACTIVE no lo sustituyen. Tras una sesión cierra normalmente para guardar CP04_SUMMARY, incluidos los contadores después del límite de líneas. No publiques un log crudo con rutas personales.

La pareja rápida usa clips completos acelerados, no contactos separados artificialmente8ticks. El buffer dura6 ticks y solo tras parry confirmado; una nueva pulsación demasiado temprana puede caducar. Se mantiene la ventana CP03, y además se exige avance del clip real: un contacto justo en su fotograma inicial puede quedar como bloqueo sin parry. Valora ritmo, mezcla, arco, SFX, colisión y defensa real. Si cualquier segunda defensa se acredita con el escudo inmóvil o después del contacto, considéralo **FAIL** y usa el rollback.

Consulta [IMPLEMENTATION.md](IMPLEMENTATION.md) para propiedad, ABI y límites de los laboratorios; [RESULTS.json](RESULTS.json) contiene la correlación fuente/CI/paquete y los conteos verificados.
