# POST08 FIX02 (0.8.2): causa raíz de la IA «pensando» y de los parries con frame 1

**Etiquetas de evidencia:**
- [R] log humano 0.8.1 `dusklight-20261102-081838` (extracto en `EVIDENCE/LOG_0_8_1_EXCERPT.md`);
- [S] fuente del host 40457c6;
- [B] DLL o EXE;
- [L] laboratorio (`LAB_MODEL_ONLY`);
- [H] hipótesis;
- [U] observado por el usuario.

## 1. El mecanismo nativo que 0.8.1 no tenía en cuenta [S]

| Hecho | Fuente |
|---|---|
| `cCcS::Set` solo mete un colisionador en la lista At si `ChkAtSet()` | `c_cc_s.cpp:56-66` |
| `cCcS::ChkAtTg` → `ClrAtHitInf` limpia el registro (`AtHit`, objeto golpeado y `AtShieldHit`) **solo** de esa lista | `c_cc_s.cpp:124-133, 150-153` |
| `OffAtSetBit` es `ClrSet`: apaga el armado pero no borra el registro | `c_cc_d.h:364`, `c_cc_d.cpp:705` |
| E_OC arma sus dos esferas At solo en `executeAttack`, estado 1\|2, con el clip en [14, 22]; después lee `ChkAtHit` y, si Link está en guardia (`checkPlayerGuard()`), **rebota**: `setPlaySpeed(-1)`, estado 3 | `d_a_e_oc.cpp:1453-1483` |
| `checkPlayerGuard()` es verdadero en guardia normal y en `GUARD_SLIP` (llama a `setUpperGuardAnime`), y falso en `GUARD_ATTACK` | `d_a_alink_guard.inc:155-171, 239-276` |
| `action()` = `OffAtSetBit` → `damage_check` (POST03-08 PRE/POST) → `execute*` → `cc_set` | `d_a_e_oc.cpp:2415-2420, 2551-2584` |

**Consecuencia:** el registro At de una esfera E_OC **sobrevive** desde la última pasada en que estuvo armada hasta su siguiente armado (frame 14 de un golpe futuro).

- **En el juego original** el rebote ocurre **dentro** de `executeAttack`, **después** de armar la esfera. Esa pasada la registra una vez más y refresca el registro.
- **En 0.8.1** (y 0.8.0), cualquier escritura de POST08/POST06 en el **POST de `damage_check`** que saque al Bokoblin del golpe (ATTACK/3 del desvío, `DAMAGE 3` de la ruptura) impide ese armado y deja vivo el registro del contacto.

## 2. Incidente A: Bokoblins que se quedan «pensando» tras un parry [U]

**Cadena causal** [S], con encaje en [R] y reproducida en [L]:
1. Parry real en la pasada N (contacto bloqueado; registro At con golpe y escudo).
2. Tick N+1: 0.8.1 escribe ATTACK/3 en el POST, antes de `executeAttack`. La esfera no se arma y el registro queda vivo.
3. Golpes siguientes, frames 0..13: `executeAttack` lee `ChkAtHit` (viejo) y `checkPlayerGuard()` (Link en `GUARD_SLIP` o en guardia tras el parry) → **rebote en el frame ~1**. El golpe nunca llega al 14, el registro nunca se renueva y el ciclo se repite mientras Link guarde.
4. Si Link hace otro Shield Attack (sin rebote nativo), POST08 juzgaba el registro viejo con un **episodio nuevo** → **parry falso** a frame 1 → otro ATTACK/3 → el ciclo continúa y además regala +40.

**Evidencia:**

| Evidencia | Qué muestra |
|---|---|
| [R] `contacts_verified=5646`, `not_attacking=4922` | Registros leídos fuera de golpe. En 0.8.0, sin desvío y con 74 bloqueos nativos, hubo 79 |
| [R] histograma de `timing_delta` plano (0..13, unos 40 cada uno) y `contacts=14/28 blocks=14/28` por Shield Attack | El mismo registro releído en cada tick |
| [R] los 6 `CONFIRMED` con `enemy_frame=1.00` (L3064, L8311, L8439, L8606, L8613, L8689) | Todos con `transitioned=0` (Link siguió en `GUARD_ATTACK`: **no hubo bloqueo real** en esa pasada) y todos tras un parry o ruptura real **del mismo actor** (221: L3040; 836: L7712; 838: L7927) |
| [R] actor 836 tras L8311 | Expansion registra en bucle `ATTACK_RATE_APPLIED native 4/1-2` → `ATTACK_LOCKOUT_SCALED native 3/4`: golpes que empiezan y vuelven a FIND sin completarse |
| [L] `run_sim2` con 0.8.1 | 1 golpe armado y 51 abortados tras el parry (monitor: `AI_STALL_SUSPECTED`) |
| [L] `run_sim2` con FIX02 | 15 armados y 0 abortados |
| [L] Shield Attack repetido | 0.8.1: 7 parries falsos; FIX02: 0 |

- **Por qué un espadazo a veces lo «desatasca» y otras no** [H, coherente con [S]]: el daño no limpia el registro. Solo un golpe que llegue al frame 14 sin que Link esté en guardia lo renueva. Si el espadazo coincide con un momento sin guardia, se libera; si no, sigue el bucle.
- **Los seis parries con frame 1:** **eran falsos**. No hubo bloqueo en su pasada; el `AtShieldHit` era el residuo del parry o ruptura anterior. No se puede filtrar «frame ≥ 14» a ciegas: la causa es la frescura del registro, y FIX02 la exige.

## 3. Incidente B: «pensando» en grupo al alternar objetivos sin parry [U]

**Estado: `HYPOTHESIS` fuerte, misma raíz que A con efecto diferido.** No se ha podido demostrar con el log, que no traza a cada actor de forma continua.

- **Lo que sí está probado:**
  - [S] el registro viejo persiste **indefinidamente** hasta un golpe que alcance el frame 14 sin guardia.
  - [R] 838 tuvo un parry real (L7927) y ~690 líneas después un parry falso por residuo (L8613): el registro siguió vivo todo ese tiempo, mientras el jugador peleaba con otros actores.
- **Mecanismo propuesto:** un Bokoblin con un registro viejo (de un parry o ruptura anterior) se queda en el bucle de rebote cada vez que Link guarda frente a **otro** Bokoblin. El usuario lo ve «pensando» sin parry en ese momento.
- [L] `run_sim2` con dos Bokoblins: en 0.8.1 los dos se atascan tras el bloqueo compartido; con FIX02 los dos siguen atacando.
- **POST05 descartado como causa** [S]: su restauración reescribe exactamente los 10 campos de `setActionMode` (modo, estado, previo, dos timers, `HeadLock` y 4 bits Tg/Co) a su PRE. El clip no se toca porque la `setActionMode(DAMAGE)` nativa tampoco lo toca. FIND/4 y ATTACK/3 se restauran coherentes con su clip y sus timers.
- **Sin probar en el juego:** queda HUMAN_PENDING con el monitor nuevo `POST08_AI_TRACE`, que ahora vigila también las supresiones de POST05 (`cause=SUPPRESSION`).

## 4. Tabla de estados y contratos

| Instante | 0.8.1 (desvío) | FIX02 |
|---|---|---|
| Pasada N | Contacto bloqueado: `AtHit` + `AtShieldHit` | igual |
| Tick N+1, `mod_update` | Instantánea de Link (GA) | igual |
| Tick N+1, `execute` de Link (normalmente primero) | → `GUARD_SLIP` | igual |
| Tick N+1, PRE de `damage_check` | Juzga el registro de N (fresco por casualidad) | Juzga el registro de N **solo si** el POST de N dejó la esfera armada (`ArmTrack`) |
| Tick N+1, POST | **Escribe ATTACK/3** (ritmo +, sin armar) | **No escribe** si Link está en GA o `SLIP`. Si el Shield Attack mareó al Bokoblin (`DAMAGE 3`) y POST05 no lo deshizo → **restaura el PRE exacto** |
| Tick N+1, `executeAttack` | Estado 3: no arma; el registro queda vivo | Estado 1\|2, frame 15–22: **arma** → la pasada N+1 refresca el registro. Con Link en `GUARD_SLIP`: **rebote nativo** (−1, estado 3), el mismo que reconoce Expansion (`rate<0`) |
| Golpes siguientes | Rebote en el frame 1 si Link guarda; parry falso si hace Shield Attack | Normales |
| Ruptura por parry | `DAMAGE 3` en el POST del contacto → registro vivo (221: L3040 → L3064) | Postura a 100 y pulso al instante; el mareo de pie se entrega en la **siguiente** llamada (`executeAttack` refresca antes) |

**Ritmos** (pregunta D):
- Expansion es dueño del ritmo de Red/Black (×1,15/×2) y reconoce el rebote nativo por `rate<0` [S `red_ai_policy.hpp:246,360`, `black_ai_policy.hpp:223`].
- FIX02 ya no deja ATTACK/3 con ritmo positivo (forma que Expansion no reconocía) salvo en el caso de respaldo `ForceRecoil` (Link sin protección, p. ej. `GUARD_BREAK`).
- Ninguna escritura de animación o ritmo nueva.

## 5. Otros hallazgos

| Hallazgo | Estado | Acción |
|---|---|---|
| Parry falso por registro viejo (el actor no atacaba en esa pasada) | `SOURCE_PROVEN` + `LAB_REPRODUCED` + log | Corregido: puerta de frescura (`STALE_CONTACT`) |
| Ruptura por parry deja el registro vivo | `SOURCE_PROVEN` + log (221) + lab | Corregido: ruptura aplazada una llamada |
| Telemetría de contactos inflada por residuos (5 188 líneas de contacto descartadas por tope en 0.8.1) | log | Corregido: los residuos ya no son contactos |
| POST06 `BREAK_SHIELD_STUN` por espada en el mismo tick de un contacto At | `HYPOTHESIS` de baja frecuencia (igual que el mareo nativo del juego) | Sin cambio; lo vigila el monitor (`cause=BREAK`) |
| `GUARD_BREAK` de Link (cada 4.º bloqueo seguido) | `SOURCE_PROVEN` (`procGuardSlipInit`) | Desvío de respaldo `ForceRecoil` para no dejar a Link expuesta |

## 6. Antes / después

- **Laboratorio:** `parry_lab`, familias FIX02 1–8: 0.8.1 reproduce el bucle, los falsos y el atasco tras la ruptura; FIX02 los corrige.
- **Mutaciones:** 18 de FIX02 (14 de lógica y 4 negativas de la auditoría de fuente). Revertir la puerta de frescura, forzar ATTACK/3, armar desde el frame 0, aceptar ticks posteriores, ignorar la identidad, quitar la espera de la ruptura, cegar o contaminar el monitor… cada una hace fallar el laboratorio o la auditoría.
- **Binario:** escrituras al actor idénticas a 0.8.1. Desaparece el uso **habitual** del ATTACK/3, que queda solo como respaldo.
