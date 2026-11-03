# Enemy Posture System 0.11.4 — HUD FIX02 PRIVATE TEST

Esta versión implementa supresión visual condicional de prompts inferiores invasores y una réplica completa del anclaje de Enemy Health Bars CP06. Scoop y la ausencia de flicker fueron confirmados por el usuario en 0.11.3; aquí se preservan mediante regresiones. La validación visual de 0.11.4 en Windows/DX12 sigue en `HUMAN_RUNTIME_PENDING`.

El enlace del paquete, nombre exacto, tamaño, SHA-256, expiración, fuente compilada y ejecución CI están en [RESULTS.json](RESULTS.json). [IMPLEMENTATION.md](IMPLEMENTATION.md) explica las rutas de dibujo, referencia CP06 y límites. Instalar sólo el candidato final cuyo hash coincida con RESULTS; los artefactos de intentos fallidos son únicamente evidencias de texto.

## Paquete verificado

[Descargar artefacto TEST 13248769855](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41673271040/artifacts/13248769855) · [CI 41673271040](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41673271040).

`POSTURE_HUD_FIX02_0_11_4_PRIVATE_TEST_windows-amd64_061e1793d687.dusk`

136658 bytes; SHA-256 `c63d436e8a475ef5b19732ac1006fad14599921232eca5545c33fb477d415fa4`. Expira según GitHub: `2026-12-03T16:33:41Z`.

Fuente compilada `061e1793d687c958d10e9d0c63ae898c369bda24`; CI `f87098b4451e942a183aeb37d9ea39ad57d10861`. Esta documentación es posterior y no recompila el binario.

## Instalar y comprobar

1. Cerrar completamente Dusklight/juego. Conservar una copia del `.dusk` de postura actual **fuera de la carpeta que escanea el cargador**.
2. Descargar el artefacto TEST final de RESULTS y extraer su ZIP de GitHub Actions. Dentro hay un único `.dusk`, `DOWNLOAD_MANIFEST.json` y `SHA256SUMS.txt`. El `.dusk` contiene únicamente `mod.json` y `lib/windows-amd64/mod.dll`.
3. En PowerShell ejecutar `Get-FileHash -Algorithm SHA256 .\POSTURE_HUD_FIX02_0_11_4_PRIVATE_TEST_windows-amd64_061e1793d687.dusk`. Comparar con el hash completo de RESULTS.
4. Sustituir **sólo** el `.dusk` anterior de Enemy Posture System. No dejar dos versiones activas con ID `dev.posture.post05_selective_reactions`. No instalar Lazy Shield Rework adicional: la defensa necesaria ya está integrada.
5. Conservar los otros siete mods y sus versiones/configuraciones: DEVF0.15.0, Bokoblin Expansion0.17.0, EHB CP06 Armos TEST, HM CP11 factor x1, Zora Swim1.3.0, Luau Support1.0.0 y Randomizer1.0.6. No tocar EXE/ROM/SDK ni saves. No cambiar HM a x2 para esta prueba sin autorización separada.
6. Arrancar en frío. No recargar esta mod a mitad de una sesión para evaluar alineación: ambas barras deben empezar sus trackers con la misma historia. INIT debe informar `POST_HUD_FIX02_INIT version=0.11.4 ... reflow=OFF ... human=HUMAN_RUNTIME_PENDING`. `STOP_BLOCKED` significa que un hook o dependencia requerido no se pudo resolver: no dar el bug por corregido.

## Prueba humana A/B

A: en un perfil de prueba separado, ejecutar sólo Enemy Posture System y dependencias imprescindibles del host para comprobar prompts, botella, Link y enemigos nativos. B: repetir en el perfil privado habitual de ocho mods, sin modificar los otros siete. La comparación con EHB y Blue/Red/Black/Fury corresponde a B. Los laboratorios no cuentan como ninguna de estas dos partidas.

| Caso | Resultado esperado en 0.11.4 |
| --- | --- |
| Barra Link invisible | Scoop/Open/Talk/Pick Up/Jump y HUD nativo funcionan como siempre; nada queda oculto por FIX02. |
| Barra visible, prompt inferior cruza su banda | Desaparecen completamente texto, botón y efectos del cluster durante el conflicto. No se trasladan. La acción y la entrada siguen disponibles. |
| Scoop con botella, con/sin barra y durante fade | Recoger sigue funcionando si el juego ofrece la acción. Un prompt invasor puede ocultarse visualmente, pero vuelve al cesar el conflicto. No se inventa una oferta de Scoop. |
| Jump, Shield Attack, Helm Splitter; A/B/R/Z y cambios entre ellos | Ninguna letra, icono, sombra o Pikari invade el marco/pulso. El grupo superior derecho no invasor permanece. Probar también dos prompts simultáneos. |
| Hold/fade y pulso | Mientras exista barra visible, se mantiene su exclusión. Al terminar el fade, los prompts reaparecen sin un frame de residuos. |
| 10–20 golpes consecutivos de espada | Si la barra debe seguir visible, no pierde frames ni se duplica al golpear. Anotar aparte su desaparición legítima al llegar a cero tras hold/fade. |
| Blue/Red/Black/Fury con EHB | Ambas barras mantienen el mismo centro horizontal y separación vertical constante al atacar, caer, levantarse y al mover/rotar/alejar la cámara. Comparar fotogramas consecutivos; objetivo visual de variación relativa <=1 px cuando se pueda medir. |
| Pérdida de target, oclusión y reaparición | La postura reaparece bajo la vida sin conservar una altura antigua. Probar después de ocultarse completamente ambas barras. |
| Presentación 30/60 FPS y ritmo irregular | Sin flash entre ticks ni deriva entre barras. No se ha certificado rendimiento/FPS del juego en cloud. |
| Sala nueva, pausa, menú, evento, transformación a lobo y retorno humano | Ocultación legítima; tras volver no hay prompts perdidos, restos de Pikari, duplicados ni posición acumulada. |
| Combate | L fijar + R mantener defensa; R+B Shield Attack/parry; B sin R espada. Tras ruptura, 75 ticks activos sin defensa/esquiva; al desbloquear, soltar R y volver a pulsar para rearmar. Pausas congelan el contador. |
| Balance | Blue25/40/50, Red17/27/33, Black/Fury13/20/25; cap100; rearme25 de pie y 0 tras levantamiento completo; decisivo x1.5; regeneración sin cambios. |

La supresión visual no elimina una interacción necesaria aunque su etiqueta invasora esté invisible. Si una interacción deja de ejecutarse, un elemento superior desaparece, quedan letras o cambian controles/daño, considerar la prueba fallida y volver al paquete anterior.

Para informar resultados, indicar A o B, escena/acción, barra visible o no, versión, FPS configurados y captura/vídeo breve si es posible. Conservar el log local; no publicarlo crudo con rutas personales. Los contadores útiles son `POST_HUD_FIX02_SUMMARY` y las presentaciones requeridas/dibujadas de `POST_HUD_FIX01_SUMMARY`. `unknown_routes`, `overflows` o `uncovered_observations` impiden interpretar la instrumentación como cobertura completa. Incluso con ceros, los contadores no prueban píxeles de DX12.

## Rollback con el juego cerrado

Retirar sólo el `.dusk` 0.11.4 de la carpeta activa y restaurar una sola versión de postura. Conservar los demás mods.

- **0.11.3**, la base observada por el usuario: [artefacto 13235219659, run41647231559](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41647231559/artifacts/13235219659). SHA-256 `99b1176322e35045f59be01dacefb25de06ba6d262a548af2bd08b5a6a4b5efc`, 122100 bytes. Fuente compilada `0c50f035a55d627379d6f6e2dcd8a04297f905ed`. Expiración conocida del artefacto: 2026-12-03T13:54:18Z. Conserva los fallos de superposición/alineación que motivan FIX02.
- **0.11.2**, alternativa de gameplay congelado: [artefacto13201587185, run41570019310](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41570019310/artifacts/13201587185). SHA-256 `2aa715980bc81af0db13622fc9e210100bcd973cd1255044d570a91f092eba0a`. No se inventa aquí su fecha de expiración; usar la copia local si GitHub ya no lo conserva. Esta versión puede reintroducir los fallos de HUD anteriores.

No hay migración ni edición de saves. El rollback no requiere modificar EHB, Expansion, HM ni el host.
