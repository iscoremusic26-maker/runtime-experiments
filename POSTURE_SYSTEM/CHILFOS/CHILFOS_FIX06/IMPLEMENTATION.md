# LIGHT FADES TWICE 0.13.6 — CHILFOS FIX06

- **Base:** `runtime-experiments` @ `1ec62168e8d16faa04d07a1a484cb0b094a96cfc` (FIX05 0.13.5 público).
- **Rama:** `feature/light-fades-twice-chilfos-fix06-0-13-6`.
- **Mod ID:** `dev.posture.post05_selective_reactions`, versión 0.13.6.
- **Estados:** `HUMAN_RUNTIME_PENDING`, `VISUAL_RUNTIME_PENDING` y `PERF_RUNTIME_PENDING`. Nada de esto se ha probado en Dusklight DX12.

Etiquetas de cada afirmación:
- **[LOG]** visto en `dusklight-20261112-181637` (0.13.5);
- **[SRC]** leído en `TwilitRealm/dusklight@40457c6`;
- **[LAB]** laboratorio o mutante;
- **[PEND]** pendiente de prueba humana.

## Hooks, imports y escritores

Sin cambios: HOOK_MEM 29, HOOK_MEM_EXT 15 y 102 imports del juego en MSVC (98 con clang-cl, idénticos a FIX05). No hay ninguna función escritora nueva. Todo FIX06 va dentro de hooks ya existentes:

| Qué | Dónde |
|---|---|
| HP del Jump Strike | `kk_native_health` (Chilfos), `liz_native_hp_bonus` con delta negativo (Lizalfos), `write_vitality` (Bokoblin) |
| Respuesta de hook | `mCutTypeCheck(2)` y `checkCutReverseAt` |
| Argumento de una sola llamada | `ProcAtTgHitmark` (posición de la chispa) y `drawPikari` (posición del destello) |
| Escritores existentes reutilizados | `kk_native_face` y `kk_native_action` |

Los archivos compartidos (`mod.cpp`, `liz_adapter.inc`, `liz_core.hpp`, `posture_core.hpp`, `balance_core.hpp`) llevan su parche inverso exacto y contado en `ci/kk_policy.json`. Al quitarlo, cada archivo vuelve a ser 0.13.5 byte a byte; lo comprueba `KK_AUDIT_PASS`.

## P0 — Jump Strike potente pero nunca letal

- **Causa [SRC]:** `d_a_alink_cut.inc` asigna `atp 4` al golpe aéreo (`setSwordAtParam`, corte 0x13) y a la onda de aterrizaje (`initCutTurnAt`, corte 0x14). En `d_cc_uty.cpp`, `at_power_get` convierte `atp ≥ 4` en 200, y la Espada Maestra lo duplica: 400. Un tajo normal (`atp 2`) quita 10 × 2 = 20.
- **Hechos [LOG]:**
  - Chilfos 468/36, HP 280 → 0 con el corte 19. `SKILL_INSTANT_SUPPRESSED` cerraba la muerte instantánea, pero el daño ordinario de 400 mataba igual.
  - Lizalfos 463/17, HP 350 → 0 con el corte 20.
- **Arreglo, en los tres adaptadores:** solo para un contacto de espada de Link en fase 18/19/20 sobre un actor admitido.
  - En el PRE de `damage_check` el HP sube 800, más que cualquier potencia nativa. El motor resta su potencia real y nunca entra en su rama letal ni toca el sonido de muerte.
  - En el POST (Lizalfos: en el PRE de `small_damage`/`big_damage`, antes de que el cerebro lo lea) se fija: `HP = max(suelo, HP_antes − 1.75 × daño ordinario efectivo)`.
  - El daño ordinario se deduce de la potencia nativa real y del `atp` del colisionador: 400 → 20 → 35.
  - **Suelos:** el HP mínimo que cada motor todavía trata como vivo. E_KK 2 (con `health <= 1` su `damage_check` vuelve sin procesar nada), E_DN 1 y E_OC 2 (con `<= 1` cae como muerto).
  - **Créditos:** uno de HP y uno de postura por Jump Strike y actor. El episodio lo abre el `setCutType(0x12)` de Link (`JsCredit`). Postura: Chilfos +8, Lizalfos +10, Bokoblin 40/27/21 (Black Fury = Black). En las demás fases, nada.
  - **Chilfos roto:** `mCutTypeCheck(2)` responde `false` y el Jump Strike no se convierte en el decisivo. Pierde el daño acotado y el tambaleo sigue.
  - **Lizalfos roto:** `js_call` impide el decisivo. Los remates auténticos (Helm Splitter, Mortal Draw, tajo decisivo) no cambian.
  - Los golpes normales, bombas, flechas y la historia matan como antes.
- **Laboratorio [LAB]:**
  - `lab_fix06`:
    - 280 → 245 y +8; las fases repetidas del mismo salto no acreditan;
    - 18/19/20 × {340, 300, 36, 30, 3, 2, 1}: nunca por debajo del suelo;
    - en el suelo, un tajo ordinario mata con `HP_ZERO`;
    - roto: no muere y el tambaleo sigue;
    - con bloqueo o parry no pierde HP.
  - `w_fix06`: 350 → 315 y +10; la otra fase no acredita; HP 20 → 1; luego un tajo ordinario mata.
  - `balance_lab`: pesos 40/27/21/21 y 0 para las demás fases.
- **Pendiente [PEND]:** el camino de HP del Bokoblin (`oc_js_pre`/`oc_js_post`) no tiene laboratorio de mundo. Solo está compilado y auditado; su peso de postura sí tiene laboratorio.
- **Limitación conocida:** si otro mod (por ejemplo HM203) lee la salud dentro del mismo `damage_check`, verá el valor elevado durante esa llamada. Un actor sin Posture System no se toca.

## P1 — Defensa real contra el Jump Attack

- **Hechos [LOG]:**
  - Chilfos: ningún veredicto BLOCK/PARRY de salto perdió HP (`jump_verdicts=21/18/39`). Los 39 de daño ocurrieron en acción 8 (su propio ataque), 3 (lanzamiento) o 0 sin guardia.
  - Lizalfos: daño con el escudo puesto en la entrada de guardia (acción 7, modo 6, frame 1). La esfera del escudo estaba colocada (`ut2=10`) y golpeada (`shield_hit=1`) de frente (`covers=1`), pero `presented=0`, así que el cuerpo recibió el daño.
- **Arreglo:**
  - Lizalfos: en la entrada de guardia (modo 6 antes del frame 3), una esfera de escudo colocada que recibe la espada de frente gana el cuerpo (`entry_cover`).
  - Chilfos: regla dura. Si un BLOCK o ENEMY_PARRY confirmado perdiera HP, se devuelve y se cuenta (`def_hp_restored`, que debe quedar en 0).
  - Lizalfos ante el spam: suelo del intento de parry por racha de saltos (45/65/80 %) y de Back Slice (35/55/70 %). Nunca 100 %.
  - El Chilfos conserva su defensa FIX05 (`kJumpWindow 180`, 40/60/75 y 60/80/90).

## P2 — El rebote se ve

- **Causa [SRC]:**
  - En el aire, `procCutJump` → `changeCutReverseProc(ANM_CUT_JUMP)`: `procCutReverseInit` devuelve 1 sin clip ni cambio de proc. Link gira 180°, velocidad 27, vibración POWER5.
  - A los pocos frames aterriza: `procCutJumpLandInit` pone `mNormalSpeed = 0`. El empujón apenas se ve.
  - En tierra, `procCutJumpLand` llama primero, en cada tick, a `changeCutReverseProc(ANM_CUT_RECOIL_B)`. Con TRUE entra en `PROC_CUT_REVERSE` con su clip de retroceso: la reacción visible.
- **Log [LOG]:** `jump_rebound_land=0`. Tras un parry aéreo, el aterrizaje no tenía contacto propio.
- **Arreglo:**
  - El parry aéreo, del Chilfos o del Lizalfos, arma un token para ese mismo salto (`g_jump_id`).
  - En su aterrizaje, el `checkCutReverseAt` del primer colisionador responde TRUE una sola vez. Se ejecuta la ruta nativa completa con su clip, su velocidad y su sonido.
  - El tick siguiente registra el recibo: `LINK_JUMP_RECOIL event=RECEIPT result=PROC_CUT_REVERSE`.
  - El token caduca a los 45 ticks y nunca se arma sin un parry real.
  - En el aire no se fuerza `PROC_CUT_REVERSE`.
- **Laboratorio [LAB]:** en la matriz de 100 saltos, 59 parries aéreos dan exactamente 59 retrocesos de aterrizaje y ningún otro salto recibe uno.
- **Pendiente [PEND]:** vídeo.

## P3 — Contraataque, transición rápida y combo aleatorio

- **Ciclo de la cadena:**
  - Un contraataque que termina de verdad (`End::Completed`, Chilfos y Lizalfos) tira un 65 %.
  - Si sale, uno de los cuatro patrones (¼ cada uno) arranca tras 4 a 9 ticks.
  - **Condición:** solo si hay una apertura real, es decir, ningún tajo nuevo de Link en 24 ticks. Pasa por la misma entrada nativa de ataque que el contraataque.
  - **Límite:** como mucho una cadena por contraataque, y el combo encadenado no encadena otro.
  - **Cancelación limpia** por muerte, ruptura, desarme, herida, otro combo, despacho perdido o caducidad (30 ticks). En el Lizalfos, si no hay cadena vuelve el descanso normal.
- **Laboratorio [LAB]:** 4000 contraataques completados dan 65,7 % de cadenas, patrones 645/658/700/625, ninguna doble y ninguna tras un contraataque cortado.
- **Balance [PEND]:** el 65 % es `[BALANCE_PROVISIONAL]`.

## P4 — Back Slice

- **Causa [SRC]:** el Back Slice es `CUT_TYPE_TWIRL` (0x1E) en `procCutFinishJumpUp` y `procCutFinishJumpUpLand` (procs 35/36 del log). Ninguno llama a `changeCutReverseProc`.
- **Antes [LOG]:**
  - Chilfos: el parry exigía rebote, así que nunca pasaba de bloqueo.
  - Lizalfos: `cut30` = 14 golpes, 0 contactos con el escudo.
- **Arreglo:**
  - **Parry de Back Slice del Chilfos:** se resuelve en el acto con +25 de postura a Link, chispa naranja y contraataque. Link no cambia de proc ni de frame.
  - **Racha:** a partir del segundo Back Slice en 240 ticks, el Chilfos libre gira tras Link con paso acotado (el primero nunca se sigue). Suelos 35/55/70 de parry y 50/70/85 de guardia.
  - **Lizalfos:** el suelo de intento lleva a su guardia, que gira natívamente.
- **Laboratorio [LAB]:** `PARRY_WITHOUT_LINK_RECOIL` con +25, contraataque, cero rebotes y proc 35 intacto.

## P5 — Destello de los botones bajo la barra

- **Código [SRC/LOG]:** `dMeterButton_c::draw` dibuja la pantalla del botón y luego `drawPikari(vtx…, &field_0x2e8[i], …)`. Ya existía la máscara FIX03 del destello propio (`fx_owned=13469` en el log).
- **Arreglo:** si en ese fotograma se dibuja la barra y el destello pertenece a un slot vivo que invade su franja, la posición de esa única llamada sale de la pantalla. El contador, el sonido y la animación siguen siendo nativos; sin barra no se toca nada. Telemetría: `HUD_SPARK_SUMMARY`.
- **[PEND]:** el log no identifica qué destello aislado ve el usuario. Puede no ser este; hace falta vídeo.

## P6 — Chispa de la lanza a quemarropa

- **Causa (inferida y documentada):**
  - `ProcAtTgHitmark` dibuja la chispa en el punto de cruce AT/TG (`i_hitPos`).
  - A quemarropa ese punto queda detrás de la cara del escudo de Link, dentro de su modelo. El sonido se oye y la chispa se tapa.
  - El log solo prueba la ejecución de la ruta (`lines_dropped=2214`), no los píxeles.
- **Arreglo:**
  - Afecta solo a la única chispa que se conserva de un contacto con la guardia de Link.
  - Si su proyección sobre la línea actor→Link cae detrás de la cara (28 unidades), el argumento de esa llamada apunta a una copia del módulo en la cara del escudo, con la altura acotada entre 55 y 135.
  - Un contacto que ya está delante conserva su punto nativo.
  - Un golpe al cuerpo conserva su marca.
  - Telemetría: `PARRY_FX event=SPEAR_SPARK` (con tope).
- **[PEND]:** vídeo.
