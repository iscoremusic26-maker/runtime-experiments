# Enemy Posture System 0.6.0 (POST06) — prueba humana

**Estado:** `HUMAN_RUNTIME_PENDING`. Compila y supera las auditorías del CI, pero nadie la ha cargado en el juego.

## Instalación (con el juego cerrado)
- **Instala solo el `.dusk` 0.6.0.** El enlace y el SHA-256 están en `IMPLEMENTATION.md`, sección «CI y binario».
- **Mismo ID que POST05:** retira el 0.5.4. **Nunca los dos a la vez.**
- **Rollback a 0.5.4:** cierra el juego, borra el 0.6.0 y copia `POSTURE_POST05_4_GENERAL_PRIVATE_TEST_windows-amd64_3053a7511302.dusk` (SHA-256 `d3b7ddb63dc300bf55d42fca184bea9c12c72b3797c105b5e43337b2126d2a91`). No hay que tocar partidas.

## Qué debería pasar
1. **Antes de 100:** como en 0.5.4. Ningún tambaleo por golpes no letales.
2. **Ruptura:** el espadazo que llega a 100 hace la reacción normal del juego. Empieza el **castigo**: ahora sí se tambalea con tus golpes y cada espadazo quita un **20 % más** (siempre el mismo 20 %).
3. **Si dejas de golpear 1 segundo:** cae al suelo con la caída del juego (salto hacia atrás y golpe contra el suelo).
4. **Si sigues golpeando:** cae como máximo **3 segundos** después de la ruptura.
5. **Un giro, salto o 4.º corte durante el castigo:** lo tumba de inmediato con la caída original.
6. **En el suelo:** puedes hacer el **Finish** del juego. Si no, se levanta solo.
7. **Después de levantarse:** postura 0. Vuelve a resistir los golpes sin tambalearse. Con poca vida, la postura baja más despacio.
8. **Sin barra de postura ni efecto o sonido nuevo** (eso llega con el HUD).

## Fase A — POST06 + Zora Swim (5 min)
1. **Log de arranque:**
   - `POST05_INIT version=0.6.0 …`;
   - `POST06_INIT version=0.6.0 punish_bonus=x1.20_fixed …`;
   - `POST03_TARGET … inline_sites_flag=0`.
2. **Red o Blue nativo:** 4 espadazos normales.
   - Del 1.º al 3.º no se tambalea.
   - El 4.º rompe la postura: `POST06_EVENT … phase=TRACKING>BROKEN_PUNISH why=BREAK_STANDING_PUNISH`.
3. **No lo golpees 1 s:** debe caer (`why=DROP_INACTIVITY_1S act=NATIVE_KNOCKDOWN_START`).
4. **En el suelo:** haz el Finish. Debe morir (`phase=DOWN_FINISH>DEAD`).
5. **Otro Bokoblin, sin Finish:** espera a que se levante. `phase=GETTING_UP>TRACKING why=REARM_AFTER_NATIVE_GET_UP act=REARM_POSTURE_0`. Golpéalo: vuelve a no tambalearse.
6. **Castigo con espadazos seguidos:** `act=BONUS_X1_20 … base=N bonus=M`, con M ≈ 20 % de N. Debe caer como mucho a los 3 s (`why=DROP_MAX_3S`).

## Fase B — los 8 mods (7 min)
- **Blue:** solo y en grupo.
- **Red:** nativo y de Expansion (el robo de vida no debe duplicarse).
- **Black:** normal y en furia (velocidad x2, cadena, como mucho 1 chip de escudo).
- **Barras (HM y Bars):** deben bajar acorde al daño, incluido el +20 % del castigo.
- **Segunda ruptura** del mismo Bokoblin, con poca vida.
- **Varios Bokoblins a la vez:** el castigo de uno no afecta a los otros.

## STOP inmediato
Cierra el juego, vuelve a 0.5.4 y mándame el log por el chat si ves:
- **Estabilidad:** crash, `VERIFY_FAILED`, `RECHECK_FAILED`, `ok=0` o `write_failed` creciendo en `POST06_SUMMARY`.
- **Vida y daño:** doble daño, vida o barras incoherentes, o un bonus que crece golpe a golpe.
- **Caída y Finish:**
  - un Bokoblin que cae dos veces seguidas o que no cae nunca tras el castigo;
  - Finish imposible estando en el suelo;
  - no se levanta, o queda congelado o sin colisión.
- **Postura:** vuelve a 0 antes de levantarse (`REARM` mientras está en el suelo).
- **Expansion:** velocidad x2 o IA de Expansion rotas.
- **Rendimiento y audio:** audio en bucle o caída fuerte de FPS.

## Qué mandar
El log de cada fase y, para cada caso raro, qué variante, en qué fase estaba y qué pasó.
