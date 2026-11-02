# Enemy Posture System 0.11.0 (LNK SESSION02): prueba humana

**Estado:** `HUMAN_RUNTIME_PENDING`. La ruptura de guardia de Link a 100 y su recuperación no están probadas aún en el juego.

## A. Instalación (juego CERRADO; partidas intactas)

1. Descarga: https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41534362043/artifacts/13183756914 (caduca el 2026-12-02).
2. Quita el `.dusk` 0.10.1 (`…5454f32e0bb1.dusk`).
3. Pon **solo** `POSTURE_LNK_SESSION02_0_11_0_NATIVE_LINK_GUARD_BREAK_RECOVERY_PRIVATE_TEST_windows-amd64_b68b3ff3c941.dusk`:
   - 101 695 bytes;
   - SHA-256 `6f880aff5d589931e0100879685b6c1efad9b76bb7478a8b1b891b48daecbcc2`.
4. Deja los otros 7 mods como están.

**Rollback:**
- 0.10.1 FIX01: `POSTURE_LNK_SESSION01_FIX01_0_10_1_DIRECT_HITS_AI_STABILITY_PRIVATE_TEST_windows-amd64_5454f32e0bb1.dusk`, SHA-256 `e7b8d5dff337ae1274abc586278999527efe3c1f5c40623b051a8403a29c397d`.
- **No uses** 0.9.0 ni 0.8.1.

**Arranque:** el log debe mostrar `LNK_S2_INIT version=0.11.0 … state=ON trigger=daAlink_c::procGuardBreakInit …`.

## B. LNK05: ruptura real a 100

1. **Bloqueo que llena la barra.** Bloquea golpes de un Blue sin parry hasta que la barra llegue a 100 (5 bloqueos de +20).
   - El último bloqueo debe **romper la guardia de verdad**: la animación de guardia rota del juego, su voz y su vibración.
   - La barra late.
   - Log: `LNK05_EVENT event=REQUESTED kind=BLOCK` → `LNK05_NATIVE_BREAK event=NATIVE_BREAK_ENTERED … proc=31` → `LNK06_EVENT`.
2. **Bloqueo con la barra ya a 100** (por ejemplo, tras una ruptura que caducó): también rompe.
3. **Parry con la barra a 100:** **no** rompe. Link +0, enemigo +40 como siempre.
4. **Golpe directo que llena la barra:**
   - primero ves la reacción normal de daño y pierdes la vida normal;
   - al terminar, la guardia se rompe (hasta ~0,8 s después);
   - si estás rodando o saltando, puede no romper (`event=EXPIRED`).
5. **Con varios enemigos a la vez:** una sola ruptura por saturación, nunca dos seguidas.
6. **Cuarto bloqueo seguido** (ruptura nativa de siempre) con la barra llena: **una** ruptura (`NATIVE_BREAK_ADOPTED`), no dos.
7. **Barra a 100 sin recibir nada:** no rompe sola.

## C. LNK06: vulnerabilidad y recuperación

8. **Durante la ruptura:**
   - Link queda vulnerable el tiempo normal del juego, sin bloqueo eterno;
   - la barra se queda a 100 y no baja.
9. **Al recuperarte** (sin tocar nada o pulsando para cancelar al final): la barra vuelve a **0** una sola vez.
   - Log: `LNK06_RECOVERY event=RECOVERED_NATIVE_END` o `RECOVERED_NATIVE_CANCEL … reset=1`.
10. **Si te golpean durante la vulnerabilidad:**
    - recibes el daño normal;
    - la barra vuelve a 0 (`INTERRUPTED_NATIVE_PRIORITY`).
11. **Pausa durante la ruptura:** al volver, todo continúa normal.
12. **Tras recuperarte, vuelve a llenar la barra:** debe romper de nuevo.

## D. Estados especiales

13. Muere, cambia de sala o transfórmate en lobo durante una ruptura o con la barra a 100. Sin barra fantasma, sin ruptura como lobo y sin bloqueo de controles.
14. **Caballo, nado o evento:** no debe haber ninguna ruptura nueva.

## E. Sin cambios esperados

15. Pesos de bloqueo y directo, parry +40, recuperación por vida y guardia ×1,5, barras enemigas, Finish, iconos inferiores ocultos y posición de la barra.
16. **Estabilidad FIX01:** ningún Bokoblin queda «pensando» tras los golpes.

## Qué mandar

- **El log completo**, sobre todo `LNK_S2_SUMMARY` (al final), las líneas `LNK05_*` y `LNK06_*`, y los `LNK_S1_*` y `POST08_*` de siempre.
- **Tus observaciones:**
  - si la ruptura se ve y se siente como la nativa;
  - cuánto dura la vulnerabilidad;
  - si la barra vuelve a 0 al recuperarte;
  - si el parry a 100 no rompe.

## STOP (cierra el juego y vuelve a 0.10.1)

- **Estabilidad:** crash, cuelgue o controles bloqueados.
- **Link:** queda atascada en la animación de ruptura.
- **Rupturas:**
  - dobles o en bucle;
  - ruptura con un parry;
  - ruptura sin impacto, o como lobo, a caballo o nadando.
- **Daño:** daño o pérdida de vida que no provenga del juego.
- **Enemigos:** atascados.
- **Otros mods:** problemas con Bokoblin Expansion o con los mods de vida.
