# LIGHT FADES TWICE 0.13.8 — DARKNUT RESURRECTION (DKR01)

## Base elegida
- Base: **0.13.7 CHILFOS FIX07**, `runtime-experiments` @ `501a26d` (rama `feature/light-fades-twice-chilfos-fix07-0-13-7`).
- Es la última versión de Light Fades Twice que existe. Está entregada (FULL 43384533943, `.dusk 482bed51…5cd7`) con prueba humana pendiente.
- No hay ninguna rama, tag ni artefacto posterior.
- Rama nueva: `feature/light-fades-twice-darknut-resurrection-0-13-8`. Mismo ID de mod: `dev.posture.post05_selective_reactions`.

## Actor exacto
- `daB_TN_c` (`B_TN`) con parámetros **exactamente `0x000001FF`**: es el "Darknut" de Enemy Spawner.
  - Valores: `mSwitchNo 0xFF`, `mType 1` (archivo `B_tnp2`), `mBrkAnmFrame 0`, `mType2 0` (cuerpo con maza).
  - Además se exige `!mStayNo2Flag`.
- Quedan intactos todos los demás:
  - el Darknut del Templo del Tiempo (`mType 0`, que nunca llama a `executeZakoEnding`);
  - el "Darknut (Sword)" `0x010001FF`;
  - los Darknuts colocados con interruptor;
  - el Darknut de Hyrule Castle con `stay-no-2`.

## Hechos nativos en los que se apoya
La fuente es `ci/dkr_native_audit.py`, que los fija como texto exacto en dusklight `40457c6`.
- **Acumulador de daño:** `setDamage` pone `health = 100`, suma el golpe a `field_0x6fc` y, al llegar a `field_0x700` (360, que `action()` reescribe en cada tick), llama a `setActionMode(ACT_ENDING, 0)`. Es la única entrada a `ACT_ENDING`.
- **`damage_check`** retorna en seco en `ACT_ENDING`: ni golpes, ni reinicio, ni duplicado.
- **`executeZakoEnding`** (modos 0..3, sin `default`):
  - **Modo 0:** atención a 0, `BCK_TN2B_DIE` (índice 4), voz `DEAD2`.
  - **Modo 1:**
    - fotograma 3: `mStates[15]=2` (la espada cae y desaparece);
    - fotogramas 33 y 68: SE y vibraciones;
    - `mMaterialColor` se lleva hacia −50 (oscurecimiento);
    - cuando el clip se detiene: modo 2 y `mTimer1 10`.
  - **Modo 2:** efecto de desaparición, interruptor y `fopAcM_delete`.
- **Ending Blow de Link:**
  - **Disponibilidad:** `checkDownAttackState` exige que el objetivo fijado sea un enemigo con `checkDownFlg()` y una `getDownPos()` a menos de 800.
  - **Al pulsar:** `checkDoCutAction` vuelve a comprobarlo.
  - **Al aterrizar:** `procCutDownLandInit` da `onCutDownHitFlg()` al actor de `field_0x280c` solo si sigue con la bandera de derribo, la punta de la espada cae a menos de 100 de la posición y la altura difiere menos de 100. Ese es el **recibo nativo**.
  - **Al terminar:** el éxito acaba con `procBackJumpInit(1)`.

## Puntos de intercepción
Solo PRE/POST.
- **Objetivos de hook (+2 `HOOK_MEM`):**
  - `daB_TN_c::executeZakoEnding` (PRE y POST);
  - `daB_TN_c::_delete` (PRE).
- **Llamadas y servicio nuevos:**
  - +4 llamadas nativas: `setSwordAtBit`, `mDoExt_McaMorfSO::setAnm`, `J3DAnmLoaderDataBase::setResource` y `J3DFrameCtrl::setFrame` (fuera de línea en PC; solo en la descarga). Total de imports del juego: 108;
  - +1 servicio opcional: `ResourceService 1.1`.
- **Comprobaciones en el EXE 2.0.3:**
  - `action()` llama de verdad a `executeZakoEnding` (thunk `0x4c11d`) y a `damage_check`;
  - `damage_check` llama 3 veces a `setDamage`;
  - los prólogos no tienen saltos relativos en los primeros 5 bytes;
  - offsets medidos y fijados con `static_assert`: `0x980`, `0x984`, `0x98c`, `0x990`, `0x9b8`, `0xcaa`, `0xcfc`, `0xd23`, `0xd34`, `0xd35`, `0xd3d`, `0x760`, `0x650`, `0x620`.

## Máquina de estados por instancia (`dkr_core.hpp`)
Clave: el ID de proceso, nunca una dirección.

`ARMED → FALLING → DOWN ⇄ FINISH_COMMITTED → FINISH_HIT → RISING → CONSUMED`

- **Primera transición letal (PRE del modo 0):**
  - Se guardan `mStates[15]`, `mMaterialColor`, la atención y `mUpdateNeckAngle`.
  - La llamada nativa corre entera.
- **`FALLING`:** el POST de cada tick deshace solo tres cosas:
  - el oscurecimiento;
  - la caída de la espada en el fotograma 3;
  - el reinicio de la atención (para conservar el fijado).

  También apaga el AT de la espada con el `setSwordAtBit(0)` nativo, y el del escudo (`mSphC`).
- **Cuando el clip se detiene (modo nativo 2):**
  - El modo pasa a `0x5D`, que ningún `case` nativo trata.
  - Se activan la bandera de derribo nativa y la posición de derribo (articulación 2, +45 de altura y 30 hacia Link, la receta del Lizalfos).
  - Arranca el temporizador de **300 ticks** del propio actor (10 s; no corre durante pausas).
- **`DOWN`:**
  - Cualquier Ending Blow en curso (`PROC_CUT_DOWN` / `PROC_CUT_DOWN_LAND`) congela el temporizador.
  - Si va dirigido a este actor, pasa a `FINISH_COMMITTED`.
  - Un fallo o interrupción vuelve a `DOWN` y reanuda el tiempo donde se quedó.
  - El recibo nativo lleva a `FINISH_HIT`: se apaga la bandera de derribo (no hay segundo Finish).
  - **Ruta A:** levantarse solo cuando Link sale de `CUT_DOWN`, `CUT_DOWN_LAND`, `BACK_JUMP` y `BACK_JUMP_LAND`.
  - **Ruta B:** levantarse cuando el temporizador llega a 0 sin ningún Finish en vuelo.
  - **Watchdogs de 20 s:** ante un Link que no termina, el actor nunca se queda tumbado para siempre.
- **`RISING`:**
  - `McaMorfSO::setAnm(clip, 0 /*una vez*/, morph 0, ritmo 1)` sobre el modelo del cuerpo.
  - El clip empieza en la pose final del DIE.
  - Se reproducen los 88 fotogramas una vez.
- **Fin del clip:**
  - `field_0x6fc = 0` (el umbral vuelve a contar desde cero) y `health = 100`;
  - atención y cuello como antes de la caída;
  - `ACT_CHASEL` modo 0 y `field_0xa91 = true`, igual que la salida nativa de `executeDamageL`;
  - se marca `CONSUMED`. La armadura no se reconstruye.
- **Segunda transición letal:** el PRE ve `CONSUMED` y no hace nada.
  - El `executeZakoEnding` original corre entero: oscurecimiento, caída y desaparición de la espada, efecto de desaparición y `fopAcM_delete`.
  - No hay bypass permanente.
- **`_delete` PRE:** retira el slot. Sirve para cambio de sala, reinicio y muerte nativa; si se reutiliza una dirección, el ID nuevo empieza en `ARMED`.

## El clip
- **Fichero:** `res/darknut/resurrection_A_pulida_FIX01.bck`, una copia byte a byte del archivo aprobado.
  - 44 512 B;
  - SHA-256 `7476e89e72b2e97a392b3f9e61875397eb91a4e95c88d45516130084fb2129a8`;
  - CRC-32 `853870d1`.

  Va empaquetado en el `.dusk` con `RES_DIR`.
- **Carga:**
  - `ResourceService` lo lee una vez a un búfer que el mod posee hasta su descarga.
  - Se comprueba tamaño, CRC, `J3D1/bck1/ANK1`, bucle 0, 88 fotogramas, 29 articulaciones y que cada tabla de claves esté dentro de su pool.
- **Enlace:** se hace una sola vez en la primera transición letal.
  - Copia byte a byte de un `mDoExt_transAnmBas` nativo de `B_tn` (mismo tipo dinámico y vtable del host), con los campos solo-de-constructor a 0 y `mBas = NULL`.
  - Después, el cargador nativo `J3DAnmLoaderDataBase::setResource` (el mismo de `d_resorce.cpp`) intercambia los bytes in situ una sola vez.
  - No usa ningún heap del juego ni sustituye recursos globales: un objeto de clip compartido y un control de fotogramas por actor.
- **Descarga del mod:** cada cuerpo retenido o que se levanta recibe el clip DIE nativo y el modo nativo de desvanecimiento (muerte nativa controlada) **antes** de liberar el búfer.

## Límites y reservas
- La muerte nativa de un tipo 1 deja caer la espada, y la primera caída la conserva en la mano. Es el único cambio visible respecto a la caída nativa. Lo pide el encargo.
- Con el oscurecimiento deshecho, el cuerpo se ve normal durante los 10 s.
- Si el jugador no ha aprendido el Ending Blow (`F_0339`) o es lobo, no hay Finish. Solo funciona la ruta B.
- El HUD de Light Fades Twice solo oculta slots de aviso que invadan la barra de postura, y esa barra no se muestra para el Darknut. Si a la vez está visible la barra de otro enemigo, se aplica la regla existente.
- Laboratorios: la duración de los clips nativos y de los procedimientos de Link es un **modelo**. No equivalen a una partida.
