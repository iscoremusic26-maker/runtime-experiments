# Enemy Posture System 0.10.0 (LNK SESSION01): prueba humana

**Estado:** `HUMAN_RUNTIME_PENDING`. Ninguna mecánica nueva está probada aún en el juego.

## A. Instalación (juego CERRADO; partidas intactas)

1. Descarga: https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41506630106/artifacts/13172155570 (caduca el 2026-12-02).
2. Quita el `.dusk` 0.9.0 (`…10dff331f201.dusk`).
3. Pon **solo** `POSTURE_LNK_SESSION01_0_10_0_DIRECT_HITS_REGEN_VARIANTS_PRIVATE_TEST_windows-amd64_9453e603c3db.dusk`:
   - 85 987 bytes;
   - SHA-256 `f381cb42a5247bed85326b818955b3b4c1d26b8c0ea079e2c87a78e044516e6c`.
4. Deja los otros 7 mods como están.

**Rollback:**
- **Principal:** 0.9.0, `POSTURE_LNK01_0_9_0_LINK_BAR_HIDE_ACTION_PROMPTS_PRIVATE_TEST_windows-amd64_10dff331f201.dusk` (`8f1562aa…672c`).
- **Histórico:** 0.8.2 (`…62533c27730d.dusk`).
- **Nunca** 0.8.1.

**Arranque:** el log debe mostrar `LNK_S1_INIT version=0.10.0 … hooks_new=0 hooks_total=6 … link_writes=0`.

## B. Golpes directos

1. **Golpes de un Blue sin guardia:**
   - pierdes vida como siempre (nativo);
   - la barra sube **+30** una vez por golpe.
   - Log: `LNK_S1_DIRECT event=CONFIRMED_DIRECT_HIT … variant=BLUE weight=30`.
2. **Repite con Red y con Black.**
   - Valores esperados: Red **+35**, Black **+40** y Black en furia **+45**.
3. **Dos golpes muy seguidos:** el segundo, durante el parpadeo de invulnerabilidad, no quita vida ni suma (`REJECTED_NO_NATIVE_DAMAGE`).
4. **Golpe que falla o daño de lava o caída:** no suma nada.

## C. Parries

5. **Varios parries a un Blue y a un Red:**
   - el enemigo gana postura como siempre;
   - **la barra de Link no se mueve**.
   - Log: `LNK_S1_PARRY … link_credit=+0`.
6. **Después de los parries:**
   - siguen atacando con normalidad (`POST08_AI_TRACE … NORMAL_NEXT_ATTACK_OBSERVED`);
   - una ruptura por parry funciona.
7. **Black en furia:** no intentes parries nuevos; su chip de escudo sigue igual.

## D. Recuperación y guardia

8. **Con vida completa:** sube la barra a ~40 y no hagas nada. Tras ~1 s baja unos 10 por segundo.
9. **Con unos 2/3 de vida, y luego con 1/3 y con muy poca:**
   - baja cada vez más lento: 8, 5 y 2 por segundo;
   - log: `LNK_S1_REGEN … band=…`.
10. **Con guardia mantenida y sin recibir golpes:**
    - baja más rápido (×1,5);
    - log: `LNK_S1_REGEN event=GUARD_CHANGE guard=SAFE_GUARD_X1.5`.
11. **Guardia mientras te bloquean golpes seguidos:** la barra no baja.
12. **Abre la pausa:** la barra no baja mientras está abierta.

## E. Variantes y grupos

13. **Bloquea un golpe de cada variante:**

    | Variante | Puntos por bloqueo |
    |---|---|
    | Blue | +20 |
    | Blue en grupo | +25 |
    | Red | +25 |
    | Black | +30 |
    | Black en furia | +35 |

    Log: `LNK_S1_BALANCE`.
14. **Grupos mixtos** (Blue bloqueado + Red por detrás, parry a uno y bloqueo a otro):
    - cada golpe suma una sola vez y al atacante correcto;
    - ningún Bokoblin queda «pensando».
15. **Barras:** Enemy Health Bars, las barras de postura enemigas y la vida ×2 del Health Multiplier siguen igual.

## F. HUD y estados especiales

16. **HUD:** la barra está en el mismo sitio, los iconos de acción inferiores siguen ocultos y los botones funcionan.
17. **Estados:** cambia de sala, abre el inventario, transfórmate en lobo y muere y reintenta. Sin barra fantasma ni valores heredados.
18. **A 100:** la barra solo late. **No** hay ruptura nueva; la ruptura de guardia nativa del juego sigue como antes.

## Qué mandar

- **El log completo**, sobre todo:
  - `LNK_S1_SUMMARY tag=SHUTDOWN part=1/2` y `part=2/2`;
  - `LNK01_SUMMARY`;
  - `POST08_SUMMARY part=1..4`.
- **Tus observaciones**, en especial:
  - si los golpes directos suben la barra una vez;
  - si los parries no la suben;
  - si se nota la recuperación más lenta con poca vida;
  - si se nota la recuperación más rápida en guardia.

## STOP (cierra el juego y vuelve a 0.9.0)

- **Estabilidad:** crash, corrupción o FPS claramente peores.
- **Controles y HUD:** controles rotos o HUD necesario desaparecido.
- **Parries:** parries falsos o que dejan de funcionar.
- **IA:** enemigos atascados.
- **Vida:** daño artificial o pérdida de vida que no provenga del juego.
- **Ruptura:** ruptura nueva al llegar a 100.
- **Postura:**
  - golpes que suman dos veces o se atribuyen al enemigo equivocado;
  - recuperación descontrolada.
- **Otros mods:** problemas con Bokoblin Expansion o con los mods de vida.
