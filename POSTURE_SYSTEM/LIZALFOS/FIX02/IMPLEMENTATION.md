# Light Fades Twice: Lizalfos Duelist FIX02 0.12.2

Estado global: **HUMAN_RUNTIME_PENDING**. Nada de este documento se ha observado en Windows/DX12. Se distingue siempre fuente, log, EXE medido, laboratorio, CI y prueba humana.

## Base y procedencia
- Base: 0.12.1, fuente compilada `5c8ac17e75ed2c8d2b9995277edec59e3ea8360d`, documentos `e691a9e08b0c2ca9d3783d9950fafbe24948bd18`.
- Rama `feature/light-fades-twice-lizalfos-duelist-fix02-0-12-2`, worktree `Mods-Duskligh-lftliz2`. CI: rama `ci/light-fades-twice-lizalfos-0-12-2`, worktree `codex-lftliz2`.
- Fuente compilada `c242770e4f155e206590be978a800c461ae4ebc6`, commit CI `f459e1234ad66f89eab963e5bbf4d02999cb354e`, run `42556628271`.
- Log usado con permiso expreso, copia temporal fuera del repo, borrada y no publicada: `dusklight-20261108-190755` (0.12.1, 72 841 líneas, 9 mods).

## Qué mostraba el log de 0.12.1
| Dato agregado | Valor | Lectura |
|---|---|---|
| Combos elegidos P1/P2/P3/P4 | 46/36/34/48 | Sin desviación llamativa del 25 % con esa muestra |
| Ventanas / parries de Link / parries de pareja doble / golpes directos / bloqueos de Link | 968 / 417 / 107 / 96 / 184 | La detección sigue sana |
| Espadazos acreditados / bloqueos del Lizalfos | 363 / 107 | |
| Parries del Lizalfos | 18 | |
| Tiradas por nivel A/B/C, intentos | 76/16/24, 13/4/10 | |
| Entradas en guardia nativas / por intento de parry / en frontera de combo | 106/22/3 | La guardia nativa domina |
| `impacts_missing`, `no_receipt`, `watchdog`, `probe_mismatch` | 0, 0, 0, 0 | FIX01 no regresó |
| Contraataques elegidos, normal/doble | 18/21 | 39 frente a 18 parries del Lizalfos: la mayoría salió de bloqueos, el defecto a corregir |
| Parries por impacto P3 | 0/19/2/2/16/8/6/8/7 | El impacto 1 de P3 tuvo 0 en 14 muestras |

P3 impacto 1: preparación de solo 12 ticks con el clip congelado. En las 14 líneas muestreadas hay 9 de guardia y 5 de cuerpo, sin rechazo técnico, y el laboratorio demuestra que el parry es posible. Es dificultad, no un fallo demostrado; el ritmo está congelado y no se toca. **Queda a tu juicio en juego.**

## Causas raíz
### 1. La guardia nativa se volvía permanente tras el primer golpe
- **Fuente:** `damage_check` hace `learn |= mHitBit`, y `e_dn_fight_run` guarda si `learn & cc_pl_cut_bit_get()`. Una vez golpeado con un corte, ese corte activa la guardia siempre.
- **Corrección:** en POST de `damage_check` se borran solo los bits de espada (`0x0FFF`) de `learn` de este actor. Decide el cerebro: 45 %, 80 %, preparación segura en la tercera herida. Los bits de otros ataques siguen siendo nativos, y así no se suprime toda decisión defensiva nativa.

### 2. Todo contacto con el escudo rebotaba la espada de Link
- **Fuente:** `changeCutReverseProc` → `checkCutReverseAt(&mAtCps[i])` = `ChkAtHit && ChkAtShieldHit`, sin distinguir bloqueo de parry.
- **EXE medido:** 3 llamadas directas a `checkCutReverseAt`, no está inlineada.
- **Corrección:** POST de `checkCutReverseAt`: si el registro At está en el escudo o una esfera de este actor y el escudo tomó de verdad la espada de Link, un bloqueo ordinario devuelve `FALSE` y un parry real conserva el rebote nativo. Los registros At/Tg, la chispa y el sonido no se tocan. Con tres cápsulas de espada, el Tg guarda solo la última: por eso se pregunta por el registro At sobre este actor. Otros escudos, incluido el de un Bokoblin, siguen nativos.

### 3. Cobertura del escudo incorrecta
- **Fuente:** `e_dn_guard` da invulnerabilidad 15 al entrar y refresca 5 en modos 1/6/7, y el Execute aparta `cc_sph` si hay invulnerabilidad: protección total antes de alzar el escudo y por la espalda. En el modo 8 el cuerpo queda vivo con el escudo aún arriba.
- **Corrección:** POST de `e_dn_guard`: escudo arriba y de frente, cuerpo apartado; en otro caso, invulnerabilidad a 0. Nunca se acorta la de una herida real (`kHitLockTicks`). Los modos 0 y 1 (salto) no se tocan.
- **Mismo pase:** si escudo y cuerpo reciben la misma espada de frente, gana el escudo y se limpia el Tg del cuerpo.
- **De espaldas:** el cuerpo recibe daño y un toque de la esfera del escudo no acredita nada.

### 4. `unk_timer_2=10` apartaba el escudo del siguiente corte
- **Fuente:** al aceptar `tate_sph`, `unk_timer_2=10` aparta la esfera 10 ticks. El siguiente corte podía atravesarla.
- **Corrección:** un corte nuevo dirigido a este actor pone ese temporizador a 0. El reembolso de fotogramas no cambia la animación.

### 5. El contraataque lo armaban los bloqueos
- **Causa:** `note_block()` llamaba a `arm_counter(0)` en 0.12.1.
- **Corrección:** dos bloqueos distintos hacen una tirada del 80 % que solo **prepara** una ventana de parry. Solo un parry real arma el contraataque.

## Reglas finales
### Guardia progresiva
| Situación | Resultado |
|---|---|
| 1.ª herida real con pérdida de HP | 45 % de preparar guardia |
| 2.ª | 80 % |
| 3.ª | Preparación segura, no éxito automático: puede perderse y no garantiza parry |
| Memoria de heridas | 150 ticks; se olvida con distancia, parada, muerte, ruptura, sala o reciclaje |
| Entrada | En la siguiente transición segura de `FIGHT_RUN`, nunca antes de 6 ticks, nunca retroactiva; un combo no se cancela |
| Duplicado del mismo corte tras su invulnerabilidad | HP nativo, sin postura, sin tirada |
| Corte sin daño | No cuenta ni tira |

Niveles A 12 %, B 35 % (3 cortes en 75 ticks), C 45 % (4 en 150). Enfriamientos de parry 120/90/60.

**Arbitraje, un resultado por oportunidad:** contraataque → ventana preparada con corte nuevo → guardia por herida → ataque nativo → guardia nativa → tirada de presión. Un corte que hirió o entró en guardia no vuelve a tirar.

### Escudo y parry
| Contacto | HP | Lizalfos | Link | Rebote |
|---|---|---|---|---|
| Bloqueo ordinario de frente | 0 | +5, una vez por corte | Sigue atacando | **No** |
| Parry real: contacto, de frente, en ventana | 0 | +0 | +25 | **Sí, nativo** |
| Por detrás, sin cubrir, o antes de alzar el escudo | Daño | +6 si es corte nuevo | | No aplica |

**Ventana nueva:** el segundo bloqueo prepara (80 %, 45 ticks). El siguiente corte real re-presenta `ANM_GUARD` por el modo 5 nativo, con ventana real. Si ese contacto cae dentro, es parry. Si no, bloqueo. Si no hay corte, no pasa nada y la guardia sale sola en tiempo acotado. Nunca hay parry con un escudo inmóvil.

### Contraataque
Solo tras un parry real. Una tirada 50/50: Normal ×1,25 (1 impacto) o Doble ×1,10 (2 impactos). Salida legal, AT real y defendible, con caducidad. Después, de nuevo los cuatro combos al 25 %.

### ×1,5 del golpe decisivo sobre el Lizalfos
Durante la ruptura de pie: base + `(base+1)/2`, una vez, con espada o Helm Splitter. No se aplica al golpe que cruzó 100 ni al Shield Attack que prepara el Helm. Si el extra es letal, HP 0 y muerte nativa. Se aplica antes de que `big_damage` lea la vida.

### ×1,5 global sobre Link
Solo durante una ruptura de postura real saturada (`lf.def.extended()`, `ModBreak` o `NativeAdopted`, fases `NativeBreak` o `PostVulnerable`). Nunca por el número 100. Sin listas de actores.

El PRE de `setDamagePoint` sube su argumento, y el código nativo sigue igual: magnificación, armadura y temporizador de invulnerabilidad. SDK comprobado: el trampolín pasa al original las copias que `arg_ref` modifica. EXE medido: 8 llamadas directas, función no inlineada. 2→3, 4→6, 6→9, 8→12; impares hacia arriba: 1→2, 3→5.

| Ruta | Tratamiento |
|---|---|
| Contacto Tg con actor del grupo enemigo, conocido o no | **×1,5** |
| Proyectil cuyo padre es enemigo | **×1,5** |
| Bomba propia, actor no hostil | `SKIP_NOT_HOSTILE`, nativo |
| Suelo o polígono, trampa de entorno | Excluido, nativo |
| Registro bloqueado por escudo | `SKIP_BLOCKED`, nativo |
| Sin atacante conocido, fuera de `checkDamageAction`: lanzamiento (`field_0x318c`), aterrizaje, escena, congelación | `SKIP_UNATTRIBUTED`, nativo |
| `daPy_py_c::setPlayerDamage` (p. ej. e_dt, kago) | Fuera de `checkDamageAction`: `SKIP_UNATTRIBUTED`, nativo. **No cubierto** |
| `dComIfGp_setItemLifeCount` directo (e_db, e_yh, e_hb, e_yd, chip de mods) | No pasa por `setDamagePoint`. **No cubierto ni registrado** |
| Armadura Mágica sin pérdida de vida | `SKIP_ARMOR_NO_HP` |

Sin x2,25: un solo commit por llamada y tick. No se confunde con la regeneración ×1,5 de postura de Link.

## Congelado, comprobado contra 0.12.1
Salida `LIZ_RHYTHM` del laboratorio bajo MSVC: **IDÉNTICA** respecto al run 42531603399 (`RHYTHM_MSVC_run_42556628271.txt`). `lab_frozen_rhythm` compara además frames de entrada y preparación de las 20 acciones.

Velocidades N 1,25; D 1,10; cola 1,10 y 1,20. P1 N-D-C (4), P2 N×3-D-N-C (7), P3 D-N-D-N-N-D (9), P4 C-C-N-D-Cfast (6). Sorteo 25 % exacto. D1→D2 0,367 s. HP 370, sin regeneración de HP. Postura 100, regeneración 10/7/4/2/1. Filas de postura de Link y Bokoblins sin cambios.

## Evolución del balance (teórico, sin regeneración)
| Versión | Espada | Parry de Link | Bloqueo | Iron Ball | Parries a ruptura | Espadazos a ruptura |
|---|---|---|---|---|---|---|
| 0.12.0 | +15 | +22 | +5 | +30 | 5 | 7 |
| 0.12.1 | +9 | +15 | +5 | +30 | 7 | 12 |
| **0.12.2** | **+6** | **+12** | **+5** | +30 | **9** | **17** |

Con parries solos: P1 48, P2 84, P3 **108**, P4 72. `lab_nine_parries`: 96 en el 8.º y ruptura exacta en el 9.º, también con el ritmo real de P3 y su regeneración, porque los huecos de P3 nunca alcanzan los 60 ticks de retardo.

## Tabla de cambios
| Ruta bajo `POSTURE_SYSTEM/POST05` | Cambio |
|---|---|
| `src/liz_core.hpp` | Política, ventana preparada, guardia progresiva, regla del cuerpo, veredicto único por corte, ×1,5 decisivo, arbitraje |
| `src/link_break_core.hpp` (nuevo) | Regla pura `lnkdmg::decide` del ×1,5 sobre Link |
| `src/liz_adapter.inc` | 2 escrituras nuevas, 3 hooks nuevos, telemetría, resúmenes |
| `src/mod.cpp` | 3 `DEFINE_HOOK`, `static_assert` de offsets medidos, include |
| `src/lifecycle_core.hpp`, `mod.json` | Versión 0.12.2 |
| `tests/liz_lab.cpp` | Casos previos conservados con pesos nuevos; `lab_deflect`, `lab_counter`, `lab_wound_guard`, `lab_shield`, `lab_nine_parries`, `lab_break_bonus`, `lab_link_rule` |
| `tests/liz_world_lab.cpp` | Adaptador de producción: `w_shield_rebound`, `w_counter`, `w_link_damage`, `w_plugin_order`, `w_delete` |
| `tests/test_liz_mutations.py`, `tests/test_liz_world_mutations.py`, `tests/test_liz_source_negatives.py` | Mutantes y negativos del encargo |
| `tests/test_cp04_pe_names.py`, `tests/compat_lab.cpp`, `tests/test_cp06f1_source_negatives.py`, `tests/bench_liz.py` | Versión, política de importación, banco a 16 actores |
| `ci/pe_audit.py`, `ci/expected_pe.json` | `setDamagePoint` permitido **solo** como objetivo de hook, con prueba binaria de que ningún código lo llama |
| `ci/liz_audit.py`, `ci/liz_policy.json`, `ci/liz_native_audit.py`, `ci/liz_pe_audit.py`, `ci/source_audit.py` | 14 escrituras, tres módulos, 81 líneas del contrato nativo |
| `ci/build_windows.py`, `ci/verify_download.py`, `ci/windows-post05.yml` | Nombre, metadatos y rama 0.12.2 |

Correcciones de limpieza detectadas por mutantes: dos comprobaciones redundantes eliminadas de producción (`L.swing_serial != deflect.serial` en `step_guard`, reinicios duplicados de `decisive_extra` y de la racha de heridas).

## Propiedad de hooks y campos
**Hooks nuevos en 0.12.2:**
| Hook | Tipo | Ámbito | Qué hace |
|---|---|---|---|
| `e_dn_guard` (por nombre, RVA medida `0xb60e00`, flags `0x45`) | POST | Lizalfos admitido | Regla del cuerpo |
| `daAlink_c::checkCutReverseAt` | POST | Un Lizalfos admitido cuyo escudo tomó la espada | `FALSE` solo en bloqueo ordinario |
| `daAlink_c::setDamagePoint` | PRE, prioridad 200 | Global, solo en episodio | Sube su propio argumento |

**Heredados de LIZ:** Execute, Delete, `damage_check`, `small_damage`, `big_damage`, `e_dn_fight_run`, `e_dn_attack_0`, `e_dn_attack`, `e_dn_tail_attack`, `at_hit_check`, `anm_init`, `setCutType`, `setGuardSe`, y los observadores sobre `checkDamageAction`.

**Escrituras (`LIZ_NOINLINE`, auditadas en fuente y PE), solo sobre el `e_dn_class` en curso salvo la última:**
| Función | Campos |
|---|---|
| `liz_native_fields` | `action`, `mode`, `invulnerability_timer`, `timer[2]`, `current.angle.y`, `current.pos` |
| `liz_native_anim` | Frame y velocidad de su morf |
| `liz_native_hp` | `health` y `field_0x560`, una vez, desde el 100/100 nativo |
| `liz_native_hp_bonus` (nueva) | `health`: extra del golpe decisivo |
| `liz_native_learn` (nueva) | Bits de espada de `learn` |
| `liz_native_guard` | Campos de la entrada nativa en guardia |
| `liz_native_break` | `at_info.mHitDirection`, `big_damage` original, invulnerabilidad de su llamador |
| `liz_native_stagger` | `action`, `mode`, ángulo, `field_0x74c`, `field_0x750` |
| `liz_native_hold` | `timer[0]`, HeadLock, `unk_timer_2` |
| `liz_native_tg_clear` | Tg de un `cc_sph` por máscara |
| `liz_native_bash_se` | Solo la llamada SE nativa |
| `liz_native_pose_frame` | Frame temporal del morf con restauración verificada |
| `liz_native_at_place` | Centro y vector de su `at_sph` |
| `liz_native_link_feedback` | `setGuardSe` nativo, shock y `mNormalSpeed` de Link en contacto de escudo real |

`amount` en `setDamagePoint` y el retorno de `checkCutReverseAt` son los únicos valores que pasan por los hooks nuevos hacia Link. No se escribe la vida de Link, EXE, ROM, SDK, partidas ni otros mods.

## Telemetría
`LIZ_GUARD` (BLOCK, WOUND_ROLL, ENTER, INTENT_END), `LIZ_DEFLECT` (PREPARE_ROLL, NEW_WINDOW, ENEMY_PARRY, EXPIRED, SWORD_REBOUND_NATIVE, NO_REBOUND_ORDINARY_BLOCK), `LIZ_COUNTER`, `LIZ_POSTURE`, `LIZ_BREAK_BONUS` (DECISIVE), `LINK_BREAK_DAMAGE` (APPLIED, SKIP_*, EPISODE_BEGIN/END, SUMMARY, INSTALL), `LIZ_IMPACT` (`ENGINE_CALL_VERIFIED` significa que la llamada ocurrió, no que se oyera), `LIZ_SUMMARY part=FIX02`.

## Matriz A/B
| Pasada | Estado |
|---|---|
| A: solo Light Fades Twice | **HUMAN_RUNTIME_PENDING** |
| B: con los otros ocho mods | **HUMAN_RUNTIME_PENDING** |
| Orden alterno de plugins, laboratorio | **LAB_PASS** (`w_plugin_order`, CI): observador ajeno primero y último en los 11 objetivos, resultado idéntico. Si va primero ve el valor nativo (4 y rebote TRUE); si va último, el decidido (6 y FALSE). No sustituye a la pasada real |

Las referencias a `setDamagePoint` en el código de Expansion que revisé son comentarios, sin hook en conflicto. No he ejecutado los otros mods, así que eso no certifica la convivencia.

## Límites honestos
- El laboratorio ejecuta el cerebro y el adaptador de producción sobre tipos stub con rutas del motor transcritas. Prueba lógica y orden de llamadas, no el juego.
- Trayectoria de armas: modelo de arco ajustado, sin BCK real. Longitudes de clip barridas, no leídas.
- Sonido, chispa, animación, colisión real y FPS: **HUMAN_RUNTIME_PENDING**.
- La secuencia de `setDamagePoint` y la lectura de `tate_sph` en la ejecución de Link dependen del orden real de actores: `LIZ_DEFLECT event=SWORD_*` lo confirmará o desmentirá.
- Jefes: la ruta ×1,5 es general, pero no está certificada contra ninguno.
- Lifesteal o cualquier función de otro mod que lea diferencias de vida: interacción con ×1,5 no ejecutada.
- P3 impacto 1: ventana corta por el ritmo congelado.
- Sin p50/p95/p99 en juego. El banco es sintético y no mide FPS.
- No aseguro ausencia de bugs.

## Rollback
Juego cerrado. Sustituye solo el `.dusk` de Light Fades Twice por 0.12.1, SHA-256 `08b18329128041b9b4bec99d10e2736fbd942fe58d4a1b037e7b88aef4480e23`, artefacto https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/42531603399/artifacts/13639325429 . No toques partidas ni los otros ocho mods.
