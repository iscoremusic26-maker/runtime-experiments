# Prueba humana — Enemy Posture System 0.11.2 PRIVATE TEST

**HUMAN_RUNTIME_PENDING** para nuevos pesos y rearme25. La defensa manual y la ventana heredada0.11.1 fueron validadas por el usuario en la sesión anterior; no se extrapola esa observación al balance nuevo.

Con el juego CERRADO, retirar SOLO el .dusk de Enemy Posture System0.11.1 y poner SOLO el 0.11.2 indicado en RESULTS.json. Mantener los otros siete mods y configuraciones; no instalar Lazy Shield Rework aparte ni cargar dos versiones de este ID. No modificar HP con debugger ni instalar herramientas adicionales.

1. Blue aislado, ensayos separados desde postura cero:3 parries /4 golpes de espada /2 impactos de Iron Ball.
2. Red aislado:4 parries /6 golpes de espada /4 impactos de Iron Ball. **Tres IronBall suman99; el cuarto rompe.** Registrar también curación/lifesteal; recuperar HP no debe cambiar la etiqueta de variante ni el peso del siguiente contacto.
3. Black aislado:5 parries cuando sean admitidos /8 golpes de espada /4 impactos de Iron Ball.
4. Black Fury: Sword 13 / Iron 25; conservar negativa original de parry/chip. No forzar un parry que el juego rechace.
5. Registrar HP real de cada enemigo en su primera ruptura; no asumir que HM x2 duplica su HP o divide todos los ataques.
6. Dejar terminar una ruptura DE PIE: medidor vuelve a 25. Repetir fin de stun y timeout seguro. Desde25, Sword Blue 3 / Red 5 / Black 6; parry 2/3/4; Iron 2/3/3.
7. Provocar la caída y levantamiento nativos completos: medidor vuelve a CERO, no 25. Comprobar también Helm, golpe decisivo único x1.50 y Finish.
8. Probar grupos mixtos y cambiar sala/volver: distinguir actor/id/generación/epoch; no debe heredarse un perfil o postura de otro actor.
9. Comprobar HP regen Blue/Red/Black, robo de vida Red y ventana de aliados, barras de vida y HM x2.
10. Revisar L solo sin guardia; L+R mantenido para escudo; soltar R lo baja; R sin fijar sin agacharse; R+B parry cuando se ofrece; B sin R espada. Tras ruptura de Link:75 ticks activos, pausa no cuenta, cuatro esquivas vetadas durante penalización y posibilidad de actuar al terminar; soltar R después del desbloqueo y volver a pulsar. Mantener animación/cancel/end, postura propia, HUD e iconos como 0.11.1.

Los conteos exactos presuponen postura inicial conocida, ausencia de regeneración entre contactos, actor vivo y ninguna otra familia. No prometer esos tiempos como duración real de una pelea. El test puede hacerse con encuentros normales y logs; no se exige manipular HP o desactivar otros mods.

## Qué revisar en el log

- POST_BAL01_INIT:0.11.2, tabla correcta, standing25/getup 0, cap=100, regen120y5/4/3/2/1 sin cambio,16 hooks / 48 imports.
- POST_BAL01_HIT:misma identidad/generación/epoch, variante/origen verificados, familia, peso nominal, antes/después/cruce y HP observado. El crédito contable tras saturación es after-before.
- POST_BAL01_PARRY:token único, peso 40/27/20, misma prueba preview/commit; rechazos con motivo. Un falso contacto no recibe este evento de parry confirmado.
- POST_BAL01_REARM:old100→new25 para fin de stun/timeout/fallback seguro;→0 para levantamiento completo. No confundir con rearme manual del escudo de Link.
- POST_BAL01_REGEN:solo cambia banda/tasa con HP real; máximoOBSERVED_MAX_THIS_GENERATION, no un máximo inventado por color.
- POST_BAL01_SUMMARY:unidades/ciclos por variante, `rearms_standing25`/`rearms_getup0`, preview_mismatch=0, auditorías=1 y contadores de mensajes descartados.
- Conservar POST03/04/05/06/08, LNK_FIX01 y logs de Expansion. Una sospecha inconclusa de IA no equivale a congelamiento confirmado.

Guardar el log COMPLETO y anotar enemigo, arma, sala, secuencia y momento de cualquier fallo. No publicar logs personales en GitHub.

## STOP / rollback

Parar ante crash/freeze/FPS grave, clasificación cruzada, suma doble, ruptura repetida, parry/escudo roto, HP artificial o curación/lifesteal dañados, HUD corrupto, IA congelada, rearme25 tras getup completo, Link bloqueado después de su castigo o errores de identidad/epoch.

Con el juego cerrado, volver exclusivamente a **0.11.1** del mismo ID:

[Artifact 0.11.1 verificado](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41554571299/artifacts/13194926059)

SHA-256: `8325dcf92d1ad7f39b330cef55713930d4dfce39c7baba27f64c8ec7d23e93ac` (109650 bytes).

Segundo nivel 0.11.0:`6f880aff5d589931e0100879685b6c1efad9b76bb7478a8b1b891b48daecbcc2`. **No usar 0.9.0 ni 0.8.1** para este checkpoint. No hubo cambios a otros mods, DEVF CP10, EXE/SDK/ROM/save ni instalación automática.
