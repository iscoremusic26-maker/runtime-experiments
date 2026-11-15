# LIGHT FADES TWICE 0.13.13 — DARKNUT MINIBOSS DKN01 FIX04

Estado: **HUMAN_RUNTIME_PENDING**. Pasa laboratorios, mutantes y auditorías; la compilación MSVC real y los tres perfiles CI se registran al final. Nadie lo ha jugado todavía: nada de este documento afirma que algo se vea, se oiga o se sienta bien en el juego.

## Base
- Fuente compilada de 0.13.12 FIX03: `00b3ce6b13877e443ab093bfff8357acbf0ad893` (+ `af4f64d`, registro CI). Entrega FIX03 verificada de nuevo: 376 343 B, SHA-256 `075db091f9bb11c890c0fe8996f513cc35a78a44b0d6f3f78c9b711b53f9eec9`.
- Ramas nuevas: fuente `feature/light-fades-twice-darknut-miniboss-fix04-0-13-13` (worktree `runtime-experiments-dkn-fix04`, desde `af4f64d`), CI `ci/light-fades-twice-darknut-miniboss-fix04-0-13-13` (worktree `windows-build-lab-dkn-fix04`, desde `c5e6e38`). Ninguna rama anterior tocada.
- Log humano analizado: `dusklight-20261114-231220.log` (18 016 líneas, SHA-256 `ce816b1d…08ca5`; copia en `dkn_fix04_evidence/`).
- `mod.cpp` **sin cambios**: 0 objetivos de hook nuevos, 0 imports nuevos, 0 escritores nativos nuevos (siguen los 20 `DKN_NOINLINE`).

## Causas demostradas (log + fuente nativa 40457c6)
1. **Rebote F2 invisible / el contacto del parry hacía daño.** `damage_check` (fase 2) solo bloquea una espada frontal en `mSphA` mientras `field_0xa91` es verdadero; si no, `setDamage`. FIX03 arrancaba el contraataque en el PRE del mismo `action()` cuyo `damage_check` procesaba el contacto del parry, y `dkn_native_attack_flags` ponía `field_0xa91 = false` antes. Log: ticks 7640 (actor 242) y 38910 (actor 279): `ENEMY_PARRY_REAL` → `COUNTER_START` → `HP2_DAMAGE +40` (`act=13`, chispa de daño) **en el mismo tick y sobre el mismo contacto** (cut=33 / cut=4: el corte del propio swing rebotado).
2. **F1 intermitente.** El rebote nativo de Link (`mCut.mRecoilAnm` = {45 frames, rate 1, cancel 15}) solo es cancelable tras el frame 15. Los contras FIX03 golpeaban 6–13 ticks después (golpe de escudo: frame 7 → `DIRECT_OFFERED` 6–7 ticks tras el rebote en los 5 parries F1 del log): la reacción quedaba cortada por un golpe imposible de defender. Con los mazazos (21–25 ticks) sí se veía: de ahí la intermitencia.
3. **Iniciativa prematura.** La guardia nativa (`ACT_GUARDL/GUARDH 1`) se consideraba "neutral" a los 8 ticks (`kGuardLeaveTicks`) y el reloj ofensivo decidía encima de la cadena de Link (actor 279: guardia 37371 → F2-SINGLE-A 37382 con `link_cutting=1`; actor 242: bloqueos 11044/11051 → F2-C2 11059).
4. **"Ralentización irregular".** Dos hechos distintos:
   - Visible (demostrado en el plan): FIX03 reproducía recuperación + preparación a **0,58–0,72** al inicio de F2-C2 y F2-C4 (y 0,87 en F2-C3) junto a tramos a 1,2–1,8 (`evidence/dkn_lab_output.txt` de 0.13.12). Los rangos de corte/inicio de la estocada (corte ≤ 24, inicio ≥ 3) y de la patada (corte ≤ 26) no daban frames de clip suficientes para los huecos grabados. A ×1,40 sin cambios F2-C2 exigiría 0,52 (< 0,55: ritmo roto).
   - Los +2…+5 ticks de `interval_error_ticks` del log **no** son el planificador: `cc_at_check` llama `dScnPly_c::setPauseTimer(2)` (5 al matar) en cada golpe normal de Link que daña → toda la escena se congela 2 ticks (hitstop nativo). Cada intervalo afectado tiene `HP1_DAMAGE`/`HP2_DAMAGE` en medio (p. ej. 38633 y 38646 antes del +4,56 de F2-C3). El +541 es el menú/evento. Ahora el log separa `native_pause_ticks` y `error_ex_pause`.
5. **Doble conteo del empuje (confirmado).** Tras capar en `DARKNUT_DAMAGE_PRE`, la reclamación se re-armaba y el POST de `checkDamageAction` de Link del tick siguiente volvía a capar **el mismo deslizamiento** con `chain+1` (tick 3101 → 3102: 12 → 9,60). En el prefijo completamente registrado: todos los primeros eslabones duplicados y todos los `chain` posteriores pares (2, 4, 6…): cada impacto avanzaba la cadena dos veces.

## P0 — Balance F1 (valores aprobados)
| | F1 | F2 | F3 |
|---|---|---|---|
| Vida / resistencia | **600** (era 420) | 480 | 480 |
| Postura máx. | **200** (era 120) | 160 | 180 |
| Bloqueado por defensa | **+4** (era +2) | +3 | +3 |
| Directo con daño | **+6** (era +4) | +5 | +5 |
| Parry de Link lateral / vertical / escudo | **+12 / +14** / +14 | — | — |
| Bola y cadena | +25 | +25 | +25 |
Tabla B, regeneración por bandas (ahora sobre 600: bordes 450/300/150/60), retraso 60, Link 100 y su ruptura: sin cambios. Sin regeneración de vida, deduplicación por acción de Link igual. Armadura: 12 pasos sobre 600 (uno por 50 HP), 11 como máximo con vida, 12 solo a 0 → `executeZakoChangeDemo` nativa una vez; golpes nativos de 40/60: ≤ 2 pasos por golpe (lab). Entrada a F2: 480/480, 0/160, cadenas/ventanas/contras reiniciados. HUD: porcentaje sobre `max_pts` (200 en F1). Ruptura F1 a 200/200: 90 ticks, sin tope de golpes, recuperación a 0/200 o transformación si HP1 = 0 (sin cambios de lógica).

## P0 — Intercambio defensivo e iniciativa
- **Cadena de Link** = swings consecutivos (≤ 45 ticks) cuyos contactos el Darknut **realmente** defendió. Cada swing nuevo (clave de acción de Link) recibe su **ordinal** = contactos defendidos + 1 al empezar; un whiff, un golpe directo o un Shield Attack no avanzan; dos swings seguidos sin contacto defendido terminan la cadena (sin guard-lock por golpear al aire). El mismo swing visto otra vez conserva su ordinal y no cambia nada.
- **Autoridad del intercambio**: mientras la cadena vive contra una defensa real (F1: el escudo existe; F2/F3: espada) de frente y al alcance, **ninguna decisión ofensiva** (combo, single, especial de pasividad, intento nativo) puede empezar (`NoInit::DEFENDING`, `offense_refused_by_exchange`). Se suelta sola: pausa > 1,5 s, dos swings vacíos, Link lejos/detrás/caído/guard-broken, sin defensa (F1 sin escudo: no hay autoridad, IA normal). Al soltarse, el controlador vuelve con su hueco ordinario (`DEFENSE_RELEASE … gap_after`), nunca con un reloj vencido. Un combo ya en curso nunca se corta por esto.
- **Probabilidad por ordinal**: 0 / 0 / 0 / 25 / 45 / 60 % (una tirada por clave de swing; nunca por frame/hook/colisionador). Lab (40 000 swings por celda): F1 0/0/0/25,18/44,76/60,02 %; F2 0/0/0/24,61/45,03/60,01 %; ordinales 1-3: 0 tiradas. La ventana pertenece a su swing: el siguiente swing la cierra.
- Guardia ordinaria F2/F3 (sin rebote) y variedad: las guardias de contacto son las nativas (`TNB_GUARD_A` 0x1C para cortes verticales/derechos/salto, `TNB_GUARD_B` 0x1D para izquierdos/giros, 50/50 en estocadas; `TNB_DOWN` 0x1A retroceso de guardia en el 4.º+ corte del combo de Link, su ataque automático se suprime); F1: `TNA_GUARD` 0x0C. Ninguna escritura de `ACT_GUARDL 0` (crash 0.13.10): el escritor sigue negándolo.

## P0 — Parry real del Darknut y contraataque
- Rebote solo con ventana armada **y** un procedimiento de Link con ruta `PROC_CUT_REVERSE` (`CUT_NORMAL`, `CUT_FINISH`, `CUT_JUMP_LAND`); si no (giro, corte aéreo) → FALSE, bloqueo ordinario (`ENEMY_PARRY_REFUSED`).
- El contacto del parry **sigue siendo un bloqueo**: `field_0xa91 + mTimer10` también en el tick del rebote y el siguiente (`parry_hold`), y el contraataque nunca arranca en ese tick → nunca `setDamage` del mismo contacto.
- **Crédito +20 (F1) / +25 (F2/F3) una vez** y **un** contraataque solo cuando el PRE lee a Link en `PROC_CUT_REVERSE` después de `procCutReverseInit` (`ENEMY_PARRY_REAL read_after_init=1`). Sin esa lectura en 8 ticks: ni crédito ni contra. Ruptura que coincide: prioridad de la ruptura, el contra se cancela, el crédito del rebote real se conserva una vez.
- **Aterrizaje**: el primer impacto del contra llega ≥ 24 ticks tras el rebote (Link recupera el control tras el frame 15 + 9 ticks para responder); arranca tan pronto como eso permite (sin espera muerta: mientras tanto el Darknut reproduce su reacción nativa de bloqueo). Lab: patada / estocada / doble / golpe de escudo / lateral → 24 ticks; vertical → 26.
- Contras (tercios entre los elegibles): F2/F3 patada / estocada / **doble completo (2 impactos)**; F1 golpe de escudo (solo con escudo) / lateral / vertical; sin escudo 50/50. Lab: 33,5/33,2/33,2 % y 33,3/32,5/34,2 %; sin escudo 49,8/50,2 %. Si el escudo desaparece antes del arranque: alternativa de maza.

## P0 — Tempo
- **F1 congelada**: huellas = 0.13.11/0.13.12 (planes 58041,6504; MoveInfo 21162,0; combos 386376,0). Matriz de parry F1 idéntica.
- **F2/F3 ×1,40 frente a FIX02** (no sobre FIX03): Δt_i/Δt_j exactos del audio; error por par ≤ 0,9 tick, acumulado ≤ 1,0.

| Combo | FIX02 | FIX03 | FIX04 (objetivo 95/130/169/122) |
|---|---|---|---|
| F2-C1 | 8 9 8 9 9 25 (68) | 10 11 10 11 12 31 (85) | 12 12 11 12 13 35 (**95**) |
| F2-C2 | 27 6 34 8 9 9 (93) | 33 8 42 11 11 11 (116) | 37 9 47 12 12 13 (**130**) |
| F2-C3 | 20 6 25 19 7 24 10 10 (121) | 25 8 31 24 8 30 12 13 (151) | 28 9 35 26 9 35 13 14 (**169**) |
| F2-C4 | 27 24 6 30 (87) | 33 30 8 38 (109) | 37 34 8 43 (**122**) |

- **Sin cámara lenta**: rangos naturales del clip (estocada inicio 1..6 y corte 12..35; doble inicio 1..11 y corte 33..54; patada corte 12..28; impactos, ventanas AT, clips, morphs y tablas intactos). Velocidad de reproducción F2: **0,73–1,63** (FIX03 0,58–1,82). Residual: patada→estocada de F2-C4 a 0,73 (FIX03 0,70) porque el clip de la patada tiene 29 frames; ir más allá exigiría una pausa inventada.
- Primer golpe de cada combo: 9–15 ticks de preparación real (FIX03 estocada: 7).
- Golpes sueltos/contras ×1,34 (FIX03 ×1,20) y patada ×1,25 (FIX03 ×1,12): el mismo +12 % que los combos. F1 sin cambios.
- B1 sigue siendo solo el primer corte; el doble, dos cortes. 46/46 posiciones (+ F3 28/28 por separado) con AT ≥ 5 ticks, impacto dentro y ticket propio.

## P0 — Efectos de parry (como Lizalfos FIX05)
Dos tipos nuevos en el libro FX (añadidos al final del enum: los anteriores conservan su número): `LINK_PARRY_DARKNUT` (Shield Attack de Link sobre el arma/escudo/pie de ESTE Darknut con su ventana de impacto abierta y el pase de Link en ventana) y `DARKNUT_PARRY_LINK` (espada de Link sobre `mSphA`/`mSphC` con la ventana armada de ese swing, de frente y con ruta de rebote). Misma chispa naranja (mismo recoloreado de la instancia nativa), mismo sonido nativo con pitch ×1,22, mismo reemplazo localizado del destello; una emisión por contacto (libro por actor/pase), confirmación o reversión por el veredicto real (`pfx_settle`), el ámbito del `damage_check` del Darknut (mapa 42, `setShieldEffect`). Bloqueos ordinarios, golpes directos y whiffs: nada cambia (azul y sonido normales). Integración como capa exacta y contada (`ci/kk_policy.json`, 8 hunks `dkn01_fix04`): `kk_audit`/`liz_audit` reconstruyen FIX05 byte a byte; `liz_world_lab` sin cambios de resultado (329 146 comprobaciones; AtVec 6006/0/4599/0).

## P1 — Empuje
Una sola cuenta de cadena por impacto real (serial de impacto) y re-aplicación idempotente del mismo tope. Para **no aumentar** el empuje que el usuario aprobó, el perfil por impacto real es exactamente el realizado en FIX03: 1.º ×0,80, siguientes ×0,65 (topes nominales 12/12/10 sin cambiar). Lab: deriva por combo bloqueado entero idéntica a la FIX03 realizada (p. ej. F2-C3 192 u), reproducción de la secuencia 3101/3102.

## Protegido sin cambios (solo regresión)
Mortal Draw, Helm Splitter, StaggerA/B (`TNB_DAMAGE_R`), Finish, levantamiento 6 s, DKR01, resurrección única, muerte F3, clip FIX02 (`f96356fb…1524`, idéntico), Shield Attack (autoridad FIX01), Lizalfos, Chilfos, Bokoblins, HUD/Link ajenos. `dkr_lab` 2318 y `dkr_world_lab` 5007 PASS (mismos totales que FIX03). Mortal Draw: **no probado por el usuario**.

## Evidencia automática local
- `dkn_lab`: 639 153 comprobaciones PASS (balance, ordinales, intercambio, crédito/contra/aterrizaje, tempo, parry 46/46 + F3 28/28, empuje).
- Mutantes DKN: **145/145** detectados (108 de FIX03 actualizados + 37 nuevos; en la 1.ª pasada sobrevivían `no_parry_cooldown`, `parried_contact_counted`, `same_swing_new_ordinal`: pruebas reforzadas y el núcleo devuelve el ordinal propio del swing repetido).
- Auditorías: dkn (33 negativos), dkn nativa (95 hechos), dkr, kk, liz, fix03, source, store, anclas de mutantes, negativos de fuente kk/fix03/liz/lft03: PASS. Labs locales g++: liz_world, lft03 (168 422), kk (11 342), liz (3 516 534), dkr, dkr_world: PASS.

## Límites honestos
- Sin prueba en el juego: rebote visible, legibilidad del tempo, color/pitch real, física del retroceso y sensación de iniciativa requieren al usuario.
- [PROVISIONAL] nuevos: `kChainWhiffs` 2, `kCounterLandTicks` 24, `kCounterLateTicks` 10.
- La compilación del DLL se hace en CI (MSVC); no hay una cadena local reproducible guardada para `mod.cpp`.
