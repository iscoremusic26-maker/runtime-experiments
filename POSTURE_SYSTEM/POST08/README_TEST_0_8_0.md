# Enemy Posture System 0.8.0 (POST08): prueba humana del parry

**Estado:** `PARTIAL_CANDIDATE / HUMAN_RUNTIME_PENDING`. Compila con MSVC y supera los laboratorios, las mutaciones y las auditorías, pero nadie lo ha cargado en el juego. El timing es provisional.

## Instalación (con el juego cerrado)

- **Descarga:** https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41397088965/artifacts/13118929802
- **Instala solo** `POSTURE_POST08_0_PARRY_PRIVATE_TEST_windows-amd64_1eda39a7f603.dusk`:
  - 63252 bytes;
  - SHA-256 `ef3a7ef4b281aa9541e329d53d8851910ae91133b18a2738cb5f7c973f79719a`;
  - el artefacto caduca el 2026-12-02 (06:02 UTC).
- **Mismo ID que 0.7.0:** retira el 0.7.0. **Nunca los dos a la vez.**
- **Rollback a 0.7.0:** cierra el juego, borra el 0.8.0 y copia `POSTURE_POST07_0_HUD_PRIVATE_TEST_windows-amd64_f0e92c9f1d74.dusk`:
  - SHA-256 `070533d756f1329db3e48a47c00e0245deee08fff7fc0243a647bcd7ead23afd`;
  - run 41392661597, artefacto 13118435513.

## Cómo se hace el parry

1. El Bokoblin empieza su golpe.
2. Pulsa **Shield Attack justo antes de que el arma llegue al escudo**.

El golpe tiene que chocar contra el escudo durante los **primeros ~5 fotogramas** del Shield Attack, unos 0,17–0,20 s.

| Situación | Qué pasa |
|---|---|
| **Parry correcto** | El Bokoblin gana **+40 de postura** (la barra crece desde el centro con un destello). No pierde vida ni se marea: su golpe termina en el aire y sigue combatiendo. Link no pierde vida por ese golpe. |
| **Parry que llega a 100** | Ruptura normal: un pulso, mareo de pie y ventana de castigo (espadazo decisivo o Escudo → Helm). |
| **Shield Attack demasiado pronto o tarde** | No hay parry. Todo sigue como en 0.7.0. |
| **Black en furia de Expansion** | **No se le puede hacer parry** en esta versión. Expansion le quitaría vida a Link por el chip de escudo. |
| **Shield Attack normal, sin golpe del enemigo** | Igual que en 0.7.0: por debajo de 100 no aturde (es así desde 0.5.4). |

## Fase A: POST08 + Zora Swim (5 min)

1. **Log de arranque:**
   - `POST08_INIT version=0.8.0 parry=ON weight=40 window_frames=[-1,+5]…`;
   - `POST07_INIT … hud=ON`;
   - `POST06_INIT version=0.8.0`.
2. **Blue:** Shield Attack sin que ataque. Sin parry y sin `POST08_EVENT result=CONFIRMED`.
3. **Shield Attack muy pronto** (antes de que levante el arma). En el log: `POST08_EVENT result=MISSED_EARLY timing_delta=…`. Apunta el `timing_delta` para calibrar.
4. **Parry preciso.**
   - Log: `POST08_EVENT result=CONFIRMED … posture_before=0 posture_after=40 crossed=0 link_attack_deflected=1 ok=1` y `POST08_LINK_LIFE_CHECK … delta=0`.
   - Debe verse +40 sin mareo y sin que Link pierda vida. **Captura o vídeo.**
5. **Dos parries más:** 40 → 80 → 100. En el tercero: `crossed=1`, `POST06_EVENT … why=BREAK_BY_PARRY`, pulso y mareo de pie.
6. **Castigo:** espadazo decisivo (caída, Finish o levantamiento). En otro intento, Escudo y luego Helm.
7. **Deja pasar la ruptura sin atacar:** vuelve a 50 de pie.

## Fase B: los 8 mods (8 min)

- **Bokoblins:** Blue solo y en grupo, Red y Black normal. Parry en cada uno.
- **Black en furia:** intenta el parry. Esperado: `result=FURY_CHIP_POSSIBLE` y comportamiento de 0.7.0. Si ves `SHIELD_CHIP_APPLIED` junto a un `CONFIRMED`, es un STOP.
- **HM ×2:** la vida del Bokoblin no cambia con el parry.
- **Barras y grupos:** las dos barras correctas; grupos de 6 a 8 y FPS.
- **Al cerrar:** `POST08_SUMMARY … unexpected_hp_delta=0 write_failed=0 invariant_ok=1` y `POST04_CONSERVATION … ok=1`.

## STOP inmediato

Cierra el juego, vuelve a 0.7.0 y mándame el log y el vídeo si ves:

- **Estabilidad:** crash, `ok=0` o `VERIFY_FAILED`.
- **Parry por debajo de 100:**
  - el Bokoblin se marea tras un `CONFIRMED` con `crossed=0`;
  - el Bokoblin pierde vida con un parry;
  - Link pierde vida en un golpe marcado `CONFIRMED`.
- **Defensa:** golpes de otros Bokoblins bloqueados sin escudo.
- **Postura:**
  - +80 en un solo golpe;
  - ruptura sin mareo o con dos pulsos.
- **Castigo y rearme:** Shield → Helm roto, ×1,50 incorrecto o rearme incorrecto.
- **Otros:** HUD fantasma, Black en furia alterado o caída grande de FPS.

## Qué mandar

- El log **completo** de cada fase.
- Si puedes, un vídeo de los parries. Sin vídeo no puedo verificar fotograma a fotograma.
