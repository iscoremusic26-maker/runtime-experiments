# Enemy Posture System 0.11.1 (LNK SESSION02 FIX01): prueba humana

**Estado:** `HUMAN_RUNTIME_PENDING`. La defensa manual, la penalización extendida y el veto de esquivas no se han probado aún en el juego. El mod no «ve» la animación: lo que se ve en pantalla solo lo puedes confirmar tú.

## A. Instalación (juego CERRADO; partidas intactas)

1. Descarga: https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41554571299/artifacts/13194926059 (caduca el 2026-12-03).
2. Quita **solo** el `.dusk` 0.11.0 (`…b68b3ff3c941.dusk`).
3. Pon **solo** `POSTURE_LNK_SESSION02_FIX01_0_11_1_MANUAL_SHIELD_EXTENDED_VULNERABILITY_PRIVATE_TEST_windows-amd64_8879ea08649e.dusk`:
   - 109 650 bytes;
   - SHA-256 `8325dcf92d1ad7f39b330cef55713930d4dfce39c7baba27f64c8ec7d23e93ac`.
4. Deja los otros 7 mods como están. **No** instales Lazy Shield Rework a la vez: engancha las mismas funciones.

**Rollback:**
- **Principal:** 0.11.0, `POSTURE_LNK_SESSION02_0_11_0_NATIVE_LINK_GUARD_BREAK_RECOVERY_PRIVATE_TEST_windows-amd64_b68b3ff3c941.dusk` (`6f880aff5d589931e0100879685b6c1efad9b76bb7478a8b1b891b48daecbcc2`).
- **Segundo nivel:** 0.10.1 (`e7b8d5df…397d`).
- **Nunca** 0.9.0 ni 0.8.1.

**Arranque:** el log debe mostrar:
- `LNK_S2_INIT version=0.11.0 … state=ON` (componente LNK05/06 heredado);
- `LNK_FIX01_INIT version=0.11.1 … state=ON … hooks(results)=0/0/0/0/0/0 … hooks_total=16`;
- 8/8 mods.

Si `LNK_FIX01_INIT` dice `state=OFF_HOOK_FAILED_0_11_0_BEHAVIOUR`, el mod se comporta como 0.11.0: avísame.

## B. Escudo manual (con un Blue delante)

1. **Fija con L sin pulsar R:** **no** sube el escudo. **B:** espada normal.
2. **L + R mantenido:** el escudo sube y bloquea. **Suelta R:** el escudo baja.
   - Log: `LNK_FIX01_SHIELD event=GUARD_ENABLED` y `event=DENIED_NO_R`.
3. **R + B en pleno golpe enemigo:** Shield Attack y parry de siempre (+40 al enemigo, +0 a Link). No sale un espadazo extra.
   - Log: `LNK_FIX01_SHIELD_ATTACK event=R_B_ACCEPTED`, `LNK_S1_PARRY`.
4. **R sin fijar:** no hay escudo ni defensa agachada; **B** sigue siendo la espada.

## C. Ruptura y castigo

5. **Bloquea con L+R hasta llenar la barra:** la ruptura de guardia es la **original** y a velocidad normal, sin cámara lenta.
6. **Mantén R durante toda la ruptura y unos 2,5 s después:** el escudo **no** vuelve. **Suelta R y vuelve a pulsarlo:** el escudo vuelve.
   - Log: `LNK_FIX01_PENALTY event=ENTER_NATIVE` → `POST_VULNERABLE` → `COMPLETE` → `SHIELD_REARMED`.
7. **Pulsa R a mitad del castigo y mantenlo hasta después:** el escudo **no** vuelve hasta que lo sueltes y lo pulses otra vez.
8. **Durante el castigo:**
   - backflip, salto lateral y rodadas: **no** salen (`LNK_FIX01_DODGE event=…_DENIED`);
   - andar, correr, girar, fijar y atacar con la espada: **sí** funcionan;
   - R+B: **no** hay Shield Attack.
9. **Deja que el enemigo ataque durante el castigo:** si te golpea, el daño y la reacción son los del juego, sin daño extra.
10. **Pasados ~2,5 s:** vuelven las esquivas, y el escudo necesita una pulsación nueva de R. La barra ya había vuelto a 0 al terminar la animación (`LNK06_RECOVERY`).

## D. Casos especiales

11. Comprueba estos casos:
    - parry con la barra a 100 (no rompe);
    - 4.º bloqueo seguido a 100 (una sola ruptura);
    - golpe directo que llena la barra;
    - dos rupturas seguidas;
    - 2-3 enemigos;
    - muerte;
    - cambio de sala;
    - lobo;
    - pausa durante el castigo (el tiempo se congela);
    - menús.
12. **Regeneración:**
    - más rápida solo mientras de verdad cubres con L+R;
    - con L sola, normal;
    - durante el castigo, nunca rápida (`LNK_FIX01_REGEN`).
13. **Comprobaciones generales:**
    - ningún Bokoblin se queda «pensando»;
    - el HUD, la vida y los otros 7 mods siguen normales.

## Qué mandar

- **El log completo**, sobre todo:
  - `LNK_FIX01_SUMMARY`;
  - `LNK_S2_SUMMARY`;
  - `LNK05_NATIVE_BREAK`;
  - `LNK06_RECOVERY`;
  - `POST08_*`;
  - `LNK_S1_FIX01_AI_*`.
- **Tus observaciones:**
  - si R se reconoce con tu mando;
  - si la ventana de castigo se nota y es justa;
  - si un enemigo solo llega a castigarte.

## STOP (cierra el juego y vuelve a 0.11.0)

- **Estabilidad:** crash.
- **Controles:**
  - controles atascados;
  - Link sin poder esquivar después de la ventana;
  - latencia o fallo grave en los botones.
- **Escudo:**
  - deshabilitado para siempre;
  - sube solo con L, sin R;
  - aparece durante el castigo.
- **Shield Attack:** R+B no hace parry.
- **Ruptura:** doble o en bucle.
- **Vida:** cambio artificial.
- **Rendimiento:** caída apreciable.
- **Enemigos:** Bokoblins congelados.
