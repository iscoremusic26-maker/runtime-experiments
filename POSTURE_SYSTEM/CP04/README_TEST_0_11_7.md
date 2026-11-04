# LIGHT FADES TWICE · CP04 0.11.7 · PRIVATE TEST

**Candidato verificado:** [descargar artifact privado 13283289812](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41746570392/artifacts/13283289812) · [CI 41746570392](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41746570392). Los jobs build e independent-download terminaron SUCCESS.

`LIGHT_FADES_TWICE_CP04_0_11_7_PRIVATE_TEST_windows-amd64_2d103c5562f7.dusk` — **147197 bytes**.

SHA-256: `e446ed3ee1111837a9feed628adf939942a006e60913fe66b00d48986b71826e`.

Fuente compilada: `2d103c5562f7199b875d5c4c7de7f00a32922a61`. Este informe se publica en un commit documental posterior; ese sucesor no se atribuye al binario. ID `dev.posture.post05_selective_reactions`, versión 0.11.7, Windows x64/DX12.

Expiración GitHub: **2026-12-04T00:40:20Z**, equivalente a 2026-12-03 19:40:20 Panamá(UTC−5). Guarda el `.dusk` antes de esa fecha.

Verificación:20 laboratorios MSVC / 3,188,646 comprobaciones; callbacks CP04 / 12.439; 468/468 mutaciones, 34 nuevas, 0 timeouts; 20 negativos PE y 4 negativos de instrucciones reales; 63 imports de juego y 24 objetivos de hook auditados. Alcance y evidencia en [VALIDATION.json](VALIDATION.json), [DOWNLOAD_VERIFIED.json](DOWNLOAD_VERIFIED.json) y [PRESERVATION.json](PRESERVATION.json).


**HUMAN_RUNTIME_PENDING · VISUAL_SHIELD_MOTION_HUMAN_PENDING.** La fuente implementa el Blue 2+2 y el rearme animado reutilizable. Compilar y pasar laboratorios no certifica la animación visible ni el resultado defensivo en Windows/DX12.

## Instalación y retorno

Descarga el ZIP del artifact y extrae el `.dusk`. Con el juego cerrado, guarda fuera de la carpeta de mods el `.dusk` 0.11.6. Coloca **solo un** `.dusk` 0.11.7 de este ID en su lugar: `dev.posture.post05_selective_reactions`. Conserva intactos los otros siete mods y sus configuraciones. No dupliques 0.11.6/0.11.7 en carpetas que cargue el modloader. No cambies EXE, ROM, SDK ni saves.

Rollback humano aprobado: [CI41703645193](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41703645193), [artifact13264179241](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41703645193/artifacts/13264179241).

`POSTURE_CP02_CP03_0_11_6_PRIVATE_TEST_windows-amd64_8c72aec291a7.dusk`

SHA-256: `0aa8e8d2941d644a33765fe288bc3f9867cc1e188506fed691caf069c63fb019`.

Si hay regresión, cierra el juego, retira 0.11.7 y devuelve **solo** ese 0.11.6. No cargues ambos. La expiración del artifact de respaldo indicada por GitHub es el 3 de diciembre de 2026 a las 14:44:30, Panamá (UTC−5); conserva tu copia.

## A/B y escenarios auténticos

A: prueba el mod solo con un **E_OC nativo ya existente** que el log identifique como Blue. No se asegura aquí un spawn/horario/sala nativa que no se haya observado. No edites el save ni inventes colocaciones para esta prueba.

B: verifica en el log ocho mods realmente cargados: EVF 0.15.0, Bokoblin Expansion 0.17.0, Enemy Health Bars CP06, Enemy Health Multiplier CP11, Zora Swim, Luau, Randomizer y este mod. Una copia shadowed de Zora no cuenta otra vez. Para B existen en `CP21_PUBLIC_RELEASE/inputs/encounters.json` las colocaciones Blue `bokoblin-001` y `bokoblin-002`, stage F_SP121, room 10, layer 6. Son referencias **de configuración**, no prueba de aparición en tu partida: confirma su admisión/contexto antes de usarlas. Utiliza los encuentros existentes para separar uno o atraer compañeros y comprobar los tres niveles; respeta el grito/reclutamiento y los leashes.

| Caso | Qué comprobar en juego |
|---|---|
| Blue solo, pareja, grupo≥3 | Tanto ataques normales como combos. Normales1/1,15/1,30 según compañeros; combo1/1/1,5/1,5 en todos. El cambio de compañeros no retima un swing. |
| Frecuencia | Cuenta BLUE_OPPORTUNITY, SELECTED y NORMAL durante muchas oportunidades. Cada decisión es1/2; una muestra corta no tiene por qué dar50%. No contar ticks ni seleccionados abortados como nuevas tiradas. |
| Combo sin parry | Cuatro espadazos visibles reales: normal–pausa–normal–pausa–rápido–pausa corta–rápido. Esquivar no debe cancelar por sí solo ni crear seguimiento/teletransporte. |
| Escudo ordinario | R manual, L+R, B normal, nuevoR+B. Sin escudo o sin rearme válido: no parry. El primer Shield Attack debe mover el escudo. |
| Parry individual y parejas | Prueba cada índice1/2/3/4 por separado, luego1→2 y2→3; repite con postura inicial0/25/60/80/99 cuando sea viable sin editar el save. |
| Parry 3 y 4 | Evita parar 1/2. Usa dos pulsaciones nuevas R+B: **dos arcos de escudo visibles**, dos contactos y feedback separados, dos seriales. B mantenido no debe repetir. |
| Parry 1/2/3 desde 0 |40→80→100 y ruptura sin cuarto swing. No se reduce el peso40 para facilitar la prueba. |
| Bloqueo/parry<100 | El Blue hace el retroceso nativo y continúa después. Esa reacción puede cambiar el intervalo entre contactos; no debe quedar pensando ni inventar un golpe. |
| Link dañado/guard-break | Sin rearme rápido durante daño, 75 ticks de penalización o sin soltar R/rearmar. Conserva las prohibiciones de esquiva. |
| Prioridades | Daño/muerte del Blue, caída/agua, evento, cambio de sala/lobo/pausa cancelan con seguridad; no se restaura un ataque tras una ruptura. Helm Splitter/Finish y Scoop conservan prioridad. |
| HUD | Corazones, rupias, mapa y botones; Scoop/Open/Talk; Jump/Shield Attack/Helm Splitter; barra de Link mientras golpea 10–20 veces; barras enemigas con EHB moviéndose y cayendo. |
| 30/60FPS y carga | Repite a 30/60FPS y con grupos densos. Los tiempos son ticks de simulación; comprueba presentación, catchup y ausencia de tirones. No se ha medido aquí el rendimiento de juego. |
| Regresión | Regen CP02 por bandas 10/7/4/2/1 tras 60 ticks elegibles; CP03 [−1,+7]/9; rearme 25/0; bonus x1,5 una vez; Red/Black/Fury, chip y lifesteal normales. |

Si puedes grabar a 60fps, revisa el inicio del segundo arco **antes** del segundo contacto. Eso sigue pendiente hasta tu prueba; los logs NATIVE_ANIMATION_STARTED/VISIBLE_CLIP_ACTIVE no lo sustituyen. CP04_SUMMARY se emite cada 1800 ticks observados sin interrumpir combate y al cerrar normalmente; conserva también ese último resumen, incluidos los contadores después del límite de líneas. No publiques un log crudo con rutas personales.

Una animación nativa de Shield Attack acredita como máximo **un parry global**. Si coinciden varios atacantes, los demás contactos conservan su bloqueo nativo y no suman otro parry con la misma entrada. Comprueba este caso especialmente en grupos.

La pareja rápida usa clips completos acelerados, no contactos separados artificialmente 8 ticks. El buffer dura 6 ticks y solo tras parry confirmado; una nueva pulsación demasiado temprana puede caducar. Se mantiene la ventana CP03, y además se exige avance del clip real: un contacto justo en su fotograma inicial puede quedar como bloqueo sin parry. Valora ritmo, mezcla, arco, SFX, colisión y defensa real. Si cualquier segunda defensa se acredita con el escudo inmóvil o después del contacto, considéralo **FAIL** y usa el rollback.

Consulta [IMPLEMENTATION.md](IMPLEMENTATION.md) para propiedad, ABI y límites de los laboratorios; [RESULTS.json](RESULTS.json) contiene la correlación fuente/CI/paquete y los conteos verificados.
