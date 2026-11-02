# POST08 FIX01 0.8.1: el parry juzgado con el estado de Link en la pasada del bloqueo

## 0. Procedencia

| Campo | Valor |
|---|---|
| Base defectuosa | 0.8.0, código `1eda39a` (rama `feature/posture-post08-parry`, documentos `96c6c42`), CI `e0bd06b`, run 41397088965 |
| Estado de la base | `CI_PASS / HUMAN_PARRY_FAIL` (0/79 contactos) |
| Rama nueva | `feature/posture-post08-fix01-contact-timing`, desde `96c6c42`. Su código es idéntico al compilado `1eda39a` |
| Commits | `0a06af1` (arreglo) y `d70f967` (sin `strcmp` del CRT: conserva el pin PE). **Compilado: `d70f9674e3ba8c17b94d6c69506346be4e1d2195`** |
| CI | `ci/posture-post08-fix01-contact-timing`, desde `e0bd06b` |
| Runs | 41449701818: falló solo en el pin PE (`strcmp`); los 11 labs y 112/112 mutaciones ya pasaban. 41450316723: correcto (compilación e `independent-download`) |

## 1. Causa raíz

| Evidencia | Hecho |
|---|---|
| [R] log humano `20261102-073401` | 79 contactos verificados; 74 `NORMAL_GUARD`, 5 `NOT_BLOCKED`, 0 candidatos. En la misma sesión, 60 Shield Attacks de Link golpearon a Bokoblins **en pleno golpe** (`pre_mode=4 pre_state=1/2`). Ver `EVIDENCE/LOG_0_8_0_EXCERPT.md`. Hubo intentos reales: ninguno llegó a evaluarse por tiempo |
| [S] `d_a_alink_damage.inc:653-684` | Con `TgShieldHit`, si `(mProcID != GUARD_ATTACK \|\| no es E_TK_BALL/KN_BULLET) && !modo 0x4000000` y `ChkTgShield`, sin caballo y con `at_spl != 8 && !checkModeFlg(0x70C52)` → `procGuardSlipInit` |
| [S] `d_a_alink.cpp:1059` | `PROC_GUARD_ATTACK` tiene los flags de modo `0x100`; `0x100 & 0x70C52 == 0` |
| [S] `d_a_e_oc.cpp:83-86` | Esfera At de E_OC: `mGObjAt {se 9, hitmark 0, spl 0, …}`, así que `at_spl = 0` |
| [S] `d_a_alink_guard.inc:239-251` | `procGuardSlipInit` → `commonProcInit(PROC_GUARD_SLIP)`; cada 4.º bloqueo, `procGuardBreakInit` |
| [S] `f_ap_game.cpp:807/828`, `m_Do_main.cpp:285-305` | Por cada tick de simulación: `ModLoader::tick` (`mod_update`) y después `fpcM_Management` (`execute` de todos los actores y luego los `draw`). Los fotogramas de presentación solo redibujan |
| [S] `d_s_play.cpp:557` | La pasada de colisión (`dComIfG_Ccsp()->Move()`) corre en `dScnPly_Draw`, después de todos los `execute` |
| [S] `c_cc_s.cpp:150-153`, `d_a_e_oc.cpp:2582` | La pasada limpia y recalcula las marcas de los colisionadores registrados; E_OC registra sus esferas en cada `execute` |

**Línea temporal real:**

| Momento | Qué ocurre |
|---|---|
| Tick N, `execute` | Link en `GUARD_ATTACK`, con marca de escudo en sus `TgCyls`; el Bokoblin con `AtSet` (frames 14..22) |
| Tick N, pasada de colisión | Bloqueo: `AtShieldHit` en la esfera del Bokoblin, `TgShieldHit` en Link, sin daño |
| Tick N+1, `mod_update` | (0.8.1) Instantánea de Link = **`GUARD_ATTACK`, frame f**, sellada con el tick N+1 |
| Tick N+1, `execute` de Link | Procesa `TgShieldHit` → **`PROC_GUARD_SLIP`** |
| Tick N+1, PRE de `damage_check` del Bokoblin | Lee `AtShieldHit` de la pasada N. **0.8.0 leía `mProcID` ahora = `GUARD_SLIP` → `NORMAL_GUARD`**. 0.8.1 usa la instantánea del tick N+1 = Link durante la pasada N |

- **Por qué los 74 contactos cayeron en `NORMAL_GUARD`:** Link se ejecuta antes que los Bokoblins (ninguno de los 79 contactos vio `guard_attack=1`: 0 confirmados, 0 tempranos, 0 tardíos y 0 duplicados). Esto es una inferencia: la regla nativa de transición sí está probada [S]; el orden de ejecución se infiere del resultado [R].
- **Laboratorio (`ROOT_CAUSE_REPRODUCED`):** `parry_lab` simula la línea temporal por fases. Con la semántica de 0.8.0 da `NORMAL_GUARD` y 0 candidatos cuando Link se ejecuta primero, y solo funcionaba si Link se ejecutaba después. Con FIX01 da un único `CONFIRMED` en ambos órdenes.

**Hipótesis del encargo:**

| Hipótesis | Veredicto |
|---|---|
| A | Probada en la fuente y consistente con el log |
| B | Correcta: la lectura de 0.8.0 mezclaba el instante de la pasada (marcas) con el tick siguiente (`mProcID`) |
| C | Posible para algunos `NOT_BLOCKED`; ahora queda registrado |
| D | No probada por los datos de 0.8.0, que no llegaron a evaluar el tiempo. La ventana se amplía igualmente según el encargo |
| E | Sin instrumentación en 0.8.0; ahora se registra |
| F | Cubierta por el orden de ejecución anterior |

## 2. Arreglo

- **`LinkTrack`** (`parry_core.hpp`, puro): `observe()` una vez por `mod_update`.
  - Lee de la Link viva: `mProcID`, `mUnderFrameCtrl[0].getFrame()`, `field_0x3478`/`0x347c` e id. Solo lectura, desde `post08_observe_link`.
  - El puntero lo pone a `NULL` el destructor de Link (`d_a_alink.cpp:19904`), así que entre ticks nunca está colgante.
  - Abre o cierra un **serial de Shield Attack** con su tick de inicio y su proc de salida.
- **`pass_for(tick, link_ok, id)`:** devuelve la instantánea **solo** si es de este mismo tick y de la misma Link; si no, `NO_PASS_SNAPSHOT`, nunca un sello viejo.
- **El veredicto usa `in.pass`** (Link durante la pasada); `in.now` queda solo como telemetría (`transitioned=1` si ya cambió).
- **Ventana [TIMING_PROVISIONAL_POST08_FIX01]:**
  - el bloqueo debe ocurrir con `frame − inicio ∈ [−1, +9]` frames de `ANM_SHIELD_ATTACK` y con `≤ 11` ticks desde que el rastreador vio empezar el Shield Attack;
  - `ANM_SHIELD_ATTACK` empieza en el frame 1 y avanza 1 frame por tick (velocidad 1,0 [S HIO]), así que son los **10 primeros ticks = 0,333 s**: pulsar el Shield Attack hasta ~1/3 s antes de que el golpe llegue al escudo;
  - en `parry_lab` se barrió la anticipación de −6 a +20 ticks con ritmos del enemigo ×1, ×1,15 y ×2: confirmado exactamente para 0..9;
  - el render no interviene: solo cuentan los ticks de simulación y los frames de animación de Link.
- **Sin cambios:**
  - +40;
  - `apply_parry`/`preview_parry`;
  - el desvío (`restore_reaction` del PRE con estado 3);
  - `BREAK_BY_PARRY`, el HUD y POST04–07;
  - la exclusión del Black en furia.
- **Seguridad del desvío con la nueva captura:** el juicio sigue ocurriendo en el PRE de la misma llamada en que se escribe el desvío, y sigue exigiendo un PRE en golpe activo (ATTACK 1|2), vida intacta y una forma permitida. La captura solo cambia **qué estado de Link** se usa para decidir.

## 3. Telemetría (fin de los «0 candidatos» opacos)

**Escritor propio de POST08**, fuera del presupuesto compartido de la categoría Hit (700 líneas, que en sesiones largas consumen POST03–06):

| Línea | Contenido | Tope |
|---|---|---|
| `POST08_SHIELD_ATTACK_START` / `_END` | serial, tick, frames, duración, proc de salida (`GUARD_SLIP`, etc.), contactos/bloqueos/parries de ese Shield Attack | 160 |
| `POST08_EVENT` (REJECTED / COMMITTED / fallos) | primer contacto de cada ataque y **todo** bloqueo durante un Shield Attack: resultado, esfera, `blocked`, Link en la pasada (proc, serial, edad, frame, delta) y ahora (proc, `transitioned`), enemigo (modo, estado, frame, ritmo, variante), vidas y postura | 250 |
| `POST08_SUMMARY` part=1/3 | Shield Attacks iniciados, terminados, con contacto, con bloqueo nativo y con parry; bloqueos durante un Shield Attack; `transitioned_after_block` | — |
| `POST08_SUMMARY` part=2/3 | un resultado principal por contacto (candidatos, `normal_guard`, `not_blocked`, `missed_early`/`late`, `duplicate`, `latched`, `fury`, `no_pass_snapshot`…) | — |
| `POST08_SUMMARY` part=3/3 | commits, unidades, rupturas, seguridad (vida, escrituras, invariantes), líneas descartadas e **histograma de `timing_delta`** de los bloqueos durante un Shield Attack | — |

`POST08_INIT` se partió en dos líneas (en 0.8.0 se truncaba a 512).

## 4. Binario (DLL descargado, artefacto 13144835814)

- **PE:** `PE_AUDIT_PASS` con el **mismo pin de imports que 0.7.0/0.8.0**; 5 `HOOK_MEM`, sin hooks nuevos.
- **Escrituras al actor y a Link:** **idénticas a 0.8.0** (ni añadidas ni eliminadas). 0.8.0 frente a 0.7.0 solo añadía las 10 del desvío.
- **Lecturas nuevas:** en `do_update` (`post08_observe_link` en línea), `0x4144`/`0x2d4c`/`0x45d8`/`0x45dc` de Link, los mismos offsets del EXE de 0.8.0.
- **Hooks:** ninguno nuevo. El recorrido nativo se observa en `mod_update` + el PRE de `damage_check` existentes.

## 5. Límites

- **Timing en el juego, sensación de la ventana y orden real de ejecución en cada sala:** HUMAN_PENDING. Los logs nuevos lo muestran directamente (`transitioned=1`, `sa_age_ticks`, `timing_delta`).
- **Black en furia:** sigue sin parry (chip de Expansion).
- **Aspecto:** sin rebote hacia atrás del Bokoblin (igual que 0.8.0).
- **Reacción de Link:** su retroceso nativo de guardia tras el bloqueo se mantiene. Cada 4.º bloqueo seguido sin pausa, el juego hace `GUARD_BREAK` (regla nativa).
