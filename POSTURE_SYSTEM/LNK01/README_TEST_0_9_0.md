# Enemy Posture System 0.9.0 (LNK01): prueba humana

**Estado:** `HUMAN_RUNTIME_PENDING` y `HUMAN_VISUAL_PENDING`. Nada de esta guía está probado aún en el juego.

## Qué trae

- **Todo 0.8.2:** postura de los Bokoblins, sin tambaleo por debajo de 100, ruptura, castigo y Finish, barras de postura enemigas y parry con Shield Attack (+40).
- **Barra propia de Link**, grande y centrada abajo:
  - sube **+20** con cada **bloqueo real** con el escudo de un golpe de Bokoblin (valor de prueba);
  - un **parry da +0** a Link;
  - tras **1 s** sin bloquear, baja 10 puntos/s;
  - a 0 sigue visible ~0,7 s y se desvanece.
- **Sin los iconos y textos de acción del centro inferior** (los prompts de botón con énfasis: icono A/B/X/Y/Z… + «Hablar», «Abrir»…, con sus destellos). **Los botones siguen funcionando.**
  - Los **mensajes flotantes** (texto de aviso del juego en esa zona) se conservan.
  - El clúster de botones de **arriba a la derecha** no se toca.
- **Limitación:** llegar a 100 es **solo visual** en esta versión.
  - No hay ruptura de guardia nueva, ni daño, ni penalización.
  - La ruptura de guardia **nativa** del juego (la 4.ª defensa seguida) sigue igual y no está ligada a la barra; se integrará en LNK05.

## Instalación (con el juego CERRADO; partidas intactas; DX12)

- **Descarga:** https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41495366683/artifacts/13166950661 (caduca el 2026-12-02).
- **Instala solo** `POSTURE_LNK01_0_9_0_LINK_BAR_HIDE_ACTION_PROMPTS_PRIVATE_TEST_windows-amd64_10dff331f201.dusk`:
  - 80 077 bytes;
  - SHA-256 `8f1562aac831257b89aafa069d182d98e2f5ac0bff876d7e1eab638b72f4672c`.
- **Quita** el `.dusk` 0.8.2 (`…62533c27730d.dusk`). **Nunca dos versiones de Posture a la vez** (mismo ID).
- **Rollback validado:** 0.8.2 FIX02
  - `POSTURE_POST08_2_FIX02_PRIVATE_TEST_windows-amd64_62533c27730d.dusk`;
  - SHA-256 `b0e245e687b313ce07b1efaf8ba3bc3e2cfe65205ed4dba5d909dc716c7166ba`.
- **No uses 0.8.1** como rollback.

## Fase A: visual (puedes empezar con Posture + Zora Swim para aislar; luego los 8 mods)

1. **Al entrar al juego, antes de bloquear:**
   - abajo en el centro **no** aparece ningún icono ni texto de acción;
   - la barra de Link no está (o está vacía);
   - A, B, Z, objetos y menú funcionan.
   - Log: `LNK01_INIT … button_hud=HIDDEN_CANDIDATE sparkle_mask=ON prompt_draw_hook(post/pre)=MOD_OK/MOD_OK`.
2. **Habla, abre, recoge y ataca** donde normalmente salía un aviso abajo en el centro:
   - la acción ocurre;
   - abajo no aparece nada (ni icono, ni texto, ni destello).
   - Log: `LNK01_ACTION_UI event=PANE_RESOLVED|VISUAL_HIDDEN`.
3. **Bloquea un golpe normal de un Blue:**
   - aparece la barra abajo en el centro con 1/5 lleno, del centro hacia los lados;
   - sin perder corazones por el bloqueo.
   - Log: `LNK01_BLOCK event=CONFIRMED_NATIVE_BLOCK post08=NORMAL_GUARD … before=0.000 after=20.000`.
4. **Deja de recibir golpes:**
   - ~1 s después la barra baja;
   - al vaciarse desaparece en ~1 s;
   - **los iconos siguen sin volver**.
   - Log: `LNK01_REGEN event=START` y luego `ZERO`.
5. **Si puedes, cambia a 720p/1080p y abre pausa e inventario:**
   - la barra no tapa menús;
   - al volver, los iconos inferiores siguen ocultos.
   - Log: `LNK01_HUD_LAYOUT`.

## Fase B: combate y regresión (los 8 mods)

6. **Bloqueos normales frente a Blue, Red y Black:**
   - +20 una vez por golpe;
   - **nada** por guardar al aire;
   - la ruptura nativa de guardia sigue como siempre (`LNK01_GUARD event=NATIVE_GUARD_BREAK`).
7. **3–5 parries:**
   - el enemigo gana +40 como en 0.8.2;
   - **la barra de Link no sube** (`LNK01_BLOCK event=REJECTED_PARRY`);
   - sin daño a Link ni atascos (`POST08_AI_TRACE … NORMAL_NEXT_ATTACK_OBSERVED`).
8. **Grupos de 2–4, golpeando A/B y con parries:**
   - ningún Bokoblin queda «pensando»;
   - las barras enemigas y la de Link no se confunden.
9. **Black en furia:**
   - su chip de escudo sigue igual;
   - un bloqueo real suma +20;
   - un golpe no bloqueado no suma nada.
10. **Cambia de sala, muere y reintenta, transfórmate en lobo y nada:**
    - sin barra de Link fantasma (en lobo se oculta);
    - sin iconos de acción reapareciendo.

## Qué mandar

- **El log completo**, y sobre todo:
  - `LNK01_INIT`, `LNK01_HUD_LAYOUT` y `LNK01_ACTION_UI`;
  - `LNK01_SUMMARY tag=SHUTDOWN part=1/2` (`blocks`, `rejected(...)`, `native_guard_break`, `invariants=1`) y `part=2/2` (`hidden_frames`, `missing_tags_or_layout_refused=0`, `hide_verify_failed=0`, `unpaired=0`);
  - `POST08_SUMMARY part=1..4` (parries, `ai_stall_suspected`).
- **Tus observaciones:**
  - ¿La barra está donde la querías?
  - ¿Ya no hay iconos de acción abajo?
  - ¿Funcionan los controles?
  - ¿Responde a los bloqueos?

## STOP (cierra el juego y vuelve a 0.8.2)

- **Estabilidad:** crash o corrupción visual grave.
- **Iconos:** iconos de acción que vuelven en combate o al cambiar de acción.
- **Controles:** controles o conversaciones que dejan de responder.
- **HUD:** desaparecen por error los corazones, el inventario, el mapa, el texto de diálogo, Enemy Health Bars, las barras POST07 o el minimapa.
- **Link:** recibe daño artificial o la guardia se rompe **por** llegar a 100.
- **Parry:** deja de funcionar, da postura falsa a Link, atasca la IA o cambia el daño.
- **Rendimiento:** caída clara de FPS con varios enemigos, o una barra duplicada.
