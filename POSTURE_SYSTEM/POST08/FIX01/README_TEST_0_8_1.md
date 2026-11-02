# Enemy Posture System 0.8.1 (POST08 FIX01): prueba humana del parry

**Estado:** `PARTIAL_CANDIDATE / HUMAN_RUNTIME_PENDING`.

## Qué se arregló

En 0.8.0 el mod miraba qué hacía Link **un tick después** del bloqueo. Para entonces el juego ya lo había pasado al retroceso de guardia (`GUARD_SLIP`), así que todos tus Shield Attacks contaban como guardia normal.

0.8.1 guarda el estado de Link **en el instante del choque**. Además la ventana sube a ~1/3 s: el Shield Attack vale si lo empiezas hasta 10 ticks antes de que el arma toque el escudo.

## Instalación (con el juego cerrado)

- **Descarga:** https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41450316723/artifacts/13144835814 (caduca el 2026-12-02, 13:11 UTC).
- **Instala solo** `POSTURE_POST08_1_FIX01_PRIVATE_TEST_windows-amd64_d70f9674e3ba.dusk`:
  - 65 741 bytes;
  - SHA-256 `d3fb369af3d7d37f0d88c3e47c43638441c2577d923ee12af41701788189fb5e`.
- **Mismo ID que 0.8.0/0.7.0:** quita el 0.8.0. **Nunca dos versiones a la vez.**
- **Rollback estable 0.7.0:**
  - `POSTURE_POST07_0_HUD_PRIVATE_TEST_windows-amd64_f0e92c9f1d74.dusk`;
  - SHA-256 `070533d756f1329db3e48a47c00e0245deee08fff7fc0243a647bcd7ead23afd`;
  - run 41392661597, artefacto 13118435513.

## Cómo hacer el parry

1. Espera a que el Bokoblin **empiece** su golpe.
2. Haz el Shield Attack **anticipándote un poco**, para que el arma choque con el escudo durante el primer tercio de segundo del empujón.

| Situación | Resultado |
|---|---|
| Parry | +40 de postura, el Bokoblin sigue combatiendo sin mareo ni pérdida de vida y Link no pierde vida por ese golpe |
| Parry que llega a 100 | Ruptura normal: un pulso, mareo de pie y castigo |
| Black en furia | Sigue sin parry (chip de escudo de Expansion) |

## Fase A: POST08 FIX01 + Zora Swim

1. **Arranque:**
   - `POST08_INIT version=0.8.1 parry=ON weight=40 window=[-1,+9]frames…<=11ticks… link_state=SNAPSHOT_IN_MOD_UPDATE`;
   - `POST08_INIT_DETECT …`;
   - `POST07_INIT … hud=ON`.
2. **Shield Attack sin ataque:** `POST08_SHIELD_ATTACK_START` / `_END … contacts=0`. La postura no sube.
3. **Guardia normal (sin Shield Attack) contra un golpe:** `POST08_EVENT result=NORMAL_GUARD … pass_shield_attack=0`. La postura no sube.
4. **Varios Shield Attacks contra golpes reales, con distintas anticipaciones.** Necesitamos **al menos un** `POST08_EVENT result=CONFIRMED stage=COMMITTED … pass_shield_attack=1 … posture_after=40 … ok=1`.
   - Suele venir con `transitioned=1` y `now_proc=…`: la prueba de que el arreglo usa el estado del choque.
   - Comprueba también `POST08_LINK_LIFE_CHECK delta=0`.
5. **0 → 40 → 80 → 100:** al tercero, `crossed=1` y `POST06_EVENT … why=BREAK_BY_PARRY`, con un pulso y mareo de pie.
6. **Castigo:** espadazo decisivo y Finish. Otra vez sin castigar: vuelve a 50. Tras levantarse: 0.

## Fase B: los 8 mods

- **Bokoblins:** Blue solo y en grupo, Red y Black normal.
- **Black en furia:** `result=FURY_CHIP_POSSIBLE`, nunca `CONFIRMED`.
- **Vida y barras:** EHB y HM (×2) coherentes, sin barras fantasma.
- **Situaciones:** grupos de 6 a 8, pausa, cambio de sala y FPS.

## Cómo leer el log si no sale ningún parry

Mira `POST08_SUMMARY tag=SHUTDOWN`, en sus tres partes:

| Si ves… | Significa |
|---|---|
| `shield_attacks_started=0` | El juego no registró ningún Shield Attack. |
| `sa_with_enemy_contact=0` | Tus Shield Attacks nunca coincidieron con un golpe enemigo. |
| `sa_with_native_block=0` | El golpe llegó, pero el escudo no lo bloqueó (por la espalda o fuera del frente). |
| `blocked_during_shield_attack>0` con `candidates=0` | Mira `missed_early` y `timing_delta_hist_frames={…}`. Deltas por encima de 9 = empezaste el Shield Attack demasiado pronto. |
| `missed_late` | El golpe ya te había alcanzado o lo habías bloqueado con guardia normal antes del Shield Attack. |
| `no_pass_snapshot>0` | Falló la captura del instante del choque. Mándame el log. |

Cada `POST08_EVENT` lleva `pass_proc` / `now_proc`, `sa_age_ticks` y `timing_delta`: con eso se recalibra la ventana.

## STOP inmediato (vuelve a 0.7.0 con el juego cerrado)

- **Estabilidad:** crash o `ok=0`.
- **Parry por debajo de 100:**
  - postura ganada con guardia normal;
  - mareo tras un `CONFIRMED` con `crossed=0`;
  - el Bokoblin pierde vida por un parry;
  - Link herido en un golpe `CONFIRMED`.
- **Postura y ruptura:** +80 en un golpe o dos pulsos.
- **Castigo y rearme:** Helm, Finish o rearme rotos.
- **Combate:** golpes de otro Bokoblin cancelados o Black en furia alterado.
- **Otros:** barras fantasma o caída fuerte de FPS.

**Manda el log completo de cada fase** y, si puedes, un vídeo corto de los intentos.
