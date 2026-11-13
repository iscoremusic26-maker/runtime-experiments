# LIGHT FADES TWICE 0.13.7 — CHILFOS FIX07

- **Base:** `runtime-experiments` @ `18d5fcc7d91bd5fe094950eba268381915b020b9` (FIX06 0.13.6 público).
- **Rama:** `feature/light-fades-twice-chilfos-fix07-0-13-7`.
- **Mod ID:** `dev.posture.post05_selective_reactions`, versión 0.13.7.
- **Estados:** `HUMAN_RUNTIME_PENDING`, `VISUAL_RUNTIME_PENDING` y `PERF_RUNTIME_PENDING`. Nada de esto se ha probado en Dusklight DX12.

Etiquetas de cada afirmación:
- **[LOG]** visto en `dusklight-20261112-230201` (0.13.6, conjunto habitual de mods);
- **[SRC]** leído en `TwilitRealm/dusklight@40457c6`, el mismo host que compila el CI (y fijado en `ci/kk_native_audit.py`);
- **[LAB]** laboratorio o mutante;
- **[PEND]** pendiente de prueba humana.

## Hooks, imports y escritores

Sin cambios: HOOK_MEM 29, HOOK_MEM_EXT 15 y 102 imports del juego en MSVC (98 con clang-cl en local, idénticos a FIX06). Sin directorio TLS. No hay ninguna función escritora nueva:

| Qué | Escritor existente |
|---|---|
| HP de un especial (subida temporal y liquidación) | `kk_native_health` (Chilfos), `liz_native_hp_bonus` con delta negativo (Lizalfos), `write_vitality` (Bokoblin) |
| Muerte por HP real con un especial acotado | Chilfos: `kk_native_health(a, 0)` + `kk_native_action(10,0)`, los dos campos que deja la rama `health <= 1` de su `damage_check`. Lizalfos: `liz_native_break` (su `big_damage` nativo) |
| Guardia sostenida durante una racha | `kk_native_action(6,0)` (Chilfos), `liz_native_guard` y `liz_native_fields` (Lizalfos) |
| Giro tras el rodar lateral de Link | `kk_native_face` |

Los archivos compartidos (`mod.cpp`, `liz_adapter.inc`, `liz_core.hpp`, `posture_core.hpp`) llevan su parche inverso exacto y contado en `ci/kk_policy.json` (bloques `fix07`). Se aplica primero: el archivo vuelve a 0.13.6 byte a byte, y luego la cadena anterior lo devuelve a FIX05. Lo comprueba `KK_AUDIT_PASS`.

## Causas

| # | Causa | Tipo | Dónde |
|---|---|---|---|
| 1 | El giro fuerte (23/24) y el Mortal Draw (26/31) tienen potencia 4: `at_power_get` → 200, ×2 Espada Maestra = 400 HP. FIX03 solo suprimía la muerte instantánea de `mCutTypeCheck(2)`; la potencia nativa seguía en `cc_at_check` | [SRC] demostrado | `d_a_alink_cut.inc` `procCutTurnInit` (`atp = 4`), `procCutFinishInit` (`var_r30 ? 4 : 3`); `d_cc_uty.cpp` |
| 2 | Chilfos 340 → 0 con postura 0 y sin romper: cortes 24 (actores 265, 309) y 31 (398, 402), `cause=HP_ZERO` tras `SKILL_INSTANT_SUPPRESSED` | [LOG] demostrado | `CHILFOS_BREAK event=NATIVE_DEATH` |
| 3 | Lizalfos 370 → 0 con postura 0: cortes 24 (×3) y 31 | [LOG] demostrado (corte por el serial de `COMBO_LINK`) | `LIZ_TRACE` |
| 4 | La cláusula de entrada de guardia de FIX06 exigía `unk_timer_2 > 0`, pero E_DN solo lo escribe (10) en el bloque de `tate_sph`, **después** de `action()`/`damage_check`. Nunca se cumplió | [SRC] + [LOG] (`entry_cover=0`) | `daE_DN_Execute` |
| 5 | `on_guard_post` anulaba la invulnerabilidad 5 que el propio `e_dn_guard` escribe en el modo 6 antes del fotograma 3: las esferas del cuerpo quedaban colocadas junto al escudo. En el log, el modo 6 fotograma 1 con escudo tocado dio `BODY_DAMAGE` | [SRC] + [LOG] | `liz_core.hpp` `on_guard_post` |
| 6 | El giro usa la esfera `mAtSph` de Link (`initCutTurnAt`), y la lectura del escudo del Lizalfos solo reconocía `mAtCps` y `mAtCyl`. Ningún giro contaba como espada de Link en el escudo | [SRC] demostrado | `liz_contact_reads` |
| 7 | El Back Slice toca el cuerpo 2 ticks después de su `setCutType` (serial 242: inicio en el tick 17219, contacto en el 17221). Ninguna guardia reactiva llega a tiempo; entre Back Slices la guardia se bajaba | [LOG] demostrado | `LIZ_TRACE` + `COMBO_LINK` |
| 8 | El Chilfos recibía el Back Slice sobre todo mientras atacaba: en 9 de los 13 veredictos registrados estaba en la acción 8. En el resumen de FIX06, `twirl=47/156/1/5/23` | [LOG] demostrado | `CHILFOS_DEFENSE event=VERDICT` |
| 9 | Giro normal (8/22) letal con poca HP: el log no da una reproducción letal. Se reproduce en el laboratorio: potencia 3, 60 HP | [LAB] | `lab_fix07`, `w_fix07` |

## P0 — Back Slice: defensa real

- **Racha de especiales (Chilfos y Lizalfos):** cada Back Slice, giro, giro fuerte o Mortal Draw que Link dirige a un enemigo entra en su racha (`kk::f7::Streak`, ventana de 240 ticks).
- **Guardia sostenida mientras dura la racha:** hasta `kHold` = 75 ticks después del último especial. En el spam del log hay un Back Slice cada ~60 ticks.
  - **Chilfos:** si está listo (lanza en mano, sin episodio propio, sin romper ni morir) y Link está a ≤ 450, levanta su guardia nativa (6,0). Mientras tanto, la entrada de ataque nativa se convierte en el descanso, así que no se mete en el spam con un combo comprometido. El contraataque tras un parry y su combo encadenado (65 %) siguen pasando: no se ha tocado la política de FIX06.
  - **Lizalfos:** desde `FIGHT_RUN` y mirando a Link, entra en guardia con un 75/90/100 % según la racha (una tirada por especial). Cada especial nuevo renueva el *watchdog* de 180 ticks; la guardia sigue acotada a `kHold` tras el último.
- **Guardia que sube:** en el modo 6 antes del fotograma 3, el Lizalfos conserva la invulnerabilidad del propio `e_dn_guard` si Link está en su arco (las esferas del cuerpo se apartan). Si el escudo colocado recibe el golpe, gana al cuerpo. Nunca es parry: el escudo aún no está presentado (regla de FIX05).
- **Solo el frente:** el Chilfos defiende en su arco de 67,5°; el Lizalfos, en el arco del escudo (112,5° a su izquierda, 67,5° a su derecha). La espalda, los flancos y los ataques comprometidos reciben el golpe.
- **Sin dos créditos:** un contacto defendido da un único bloqueo o parry por serial de golpe. La otra fase del mismo Back Slice no suma de nuevo (`block_dupes`, `contact_swing`).
- **Animación de Link intacta:** el parry de Back Slice del Chilfos se queda como en FIX06, sin rebote, con +25 a Link y contraataque. El Lizalfos acepta ahora su parry especial sin ruta de rebote para el Back Slice y los giros (`parry_no_route`).

## P1 — Giros y Mortal Draw: defensa y anti-muerte instantánea

- **Enemigo no roto que no se defiende:**
  - Antes de `damage_check`, la HP sube 800 por encima de cualquier potencia nativa.
  - En el mismo paso de `damage_check` se aplica **una** pérdida acotada por ejecución (serial de `setCutType`) y **un** crédito de postura.
  - Las demás fases y esferas del mismo giro no cuentan (`DUPLICATE_NO_EFFECT`).
- **HP baja:** si esa pérdida acotada se lleva la última HP, muere por la ruta nativa:
  - **Chilfos:** acción 10 con HP 0.
  - **Lizalfos:** `big_damage`; si el motor había elegido `small_damage`, se redirige a `big_damage`, porque E_DN no muere en `S_DAMAGE`.
  - **Bokoblin:** suelo 2, es decir, el siguiente golpe lo mata. Es una limitación documentada abajo.
- **Bloqueo:** 0 HP y la postura de bloqueo aumentada, una vez. Chilfos: la guardia nativa (6,0) no resta HP. Lizalfos: el escudo gana al cuerpo.
- **Parry:**
  - **Giro y giro fuerte:** no tienen ruta de rebote (`procCutTurn`). El parry se liquida al momento, Link sigue girando, gana +25 y llega el contraataque.
  - **Mortal Draw:** sí tiene ruta de rebote (`procCutFinish`), así que su parry usa el rebote nativo.
- **Suelos de anticipación:** en la racha, el bloqueo tiene un suelo de 75/90/100 % para un enemigo listo que mira a Link. El parry tiene 20/30/40 %, menos que el bloqueo, como pide el encargo («si no sale, la guardia alzada bloquea»).
  - Los suelos de parry del Back Slice de FIX06 (35/55/70 %) se mantienen sin cambios.
- **Remate de Mortal Draw:** solo la petición B del propio Posture System sobre un Chilfos roto emite un **recibo** (`MdReceipt`: ranura, generación, token y ventana de 120 ticks). La muerte sigue siendo la rama letal nativa de siempre.
  - Línea `SPECIAL_SKILL event=NATIVE_DEATH ... authorized_finisher=1 source_of_finisher_token=POSTURE_B_REQUEST`.
  - Otro actor no hereda el recibo. Un segundo Chilfos no roto, alcanzado por el mismo Mortal Draw, recibe el daño acotado [LAB].
  - Un Mortal Draw común sobre un Chilfos roto sigue siendo la estocada decisiva de la ruptura (regla aprobada, sin cambios), pero sin recibo: `source_of_finisher_token=BROKEN_DECISIVE_SWORD`.
- **Lizalfos roto (vulnerabilidad de pie):** no usa la ruta acotada; conserva sus reglas decisivas (caída nativa, ruta del Ending Blow).

## P2 — Balance [BALANCE_PROVISIONAL]

Base: el tajo ordinario efectivo de ese mismo Link, medido en el propio golpe (`daño nativo × 10 / at_power(atp)`); con la Espada Maestra son 20. Redondeo determinista, mitad hacia arriba.

| Técnica | HP si impacta | Chilfos postura impacto / bloqueo | Lizalfos impacto / bloqueo | Bokoblin Blue / Red / Black (Fury = Black) |
|---|---|---|---|---|
| Base | 20 | +5 / +3 | +6 / +5 | 25 / 17 / 13 |
| Giro normal | ×1,5 = **30** | ×1,6 = **8** / ×1,8 = **5** | **10** / **9** | **40** / **27** / **21** |
| Giro fuerte | ×2,25 = **45** | ×2,0 = **10** / ×2,5 = **8** | **12** / **13** | **50** / **34** / **26** |
| Mortal Draw común | ×2,5 = **50** | ×2,25 = **11** / ×2,75 = **8** | **14** / **14** | **56** / **38** / **29** |
| Back Slice | nativo 60 (sin número acordado: sin cambios) | +5 / +3 | +6 / +5 | nativo |

- **Base del multiplicador de bloqueo:** se aplica a la ganancia de bloqueo de cada familia (Chilfos +3, Lizalfos +5), no a la de espada. Es la lectura literal de las referencias «bloqueo +3/+5» del encargo; si se prefiere la otra lectura, es una constante.
- **Bokoblin:** no tiene guardia, así que no se inventa ninguna.
- **Ruptura de Blue:** ningún especial rompe a un Blue por sí solo (máximo 56). Dos especiales sí (56 + 50).
- **Madera:** con espada de madera el tajo vale 10, así que la tabla queda en 15/23/25 HP.
- **Parry:** 0 HP; Link gana su postura de siempre y no se duplica el crédito del bloqueo.

## Telemetría nueva

`CHILFOS_DEFENSE_FIX07 event=CONTACT|GUARD_HOLD|PARRY_WITHOUT_LINK_RECOIL`, `LIZ_DEFENSE_FIX07 event=CONTACT`, `SPECIAL_SKILL event=HP_COMMITTED|NATIVE_DEATH`, `CHILFOS_FIX07_SUMMARY`, `LIZ_FIX07_SUMMARY` y `SPECIAL_SKILL_SUMMARY` (una por familia, con la fuga de HP en contactos defendidos, que debe ser 0).

- **Línea de contacto:** actor, generación, técnica, corte, proc, swing, acción y modo nativos, `guard_effective`, `frontal_arc`, veredicto, HP y postura antes y después, `credit_once`, racha y razón (`DEFENDED`, `COMMITTED_ATTACK`, `FLANK`, `NO_GUARD`, `BROKEN`; `GUARD_BEATEN` sería un defecto).
- **Tope:** familia de log propia (`kKkFix07`, 320 líneas) más los descartes en los resúmenes.

## Limitaciones honestas

- **Bokoblin:** un especial acotado no mata en el mismo contacto (suelo 2); el siguiente golpe sí. E_OC decide su muerte dentro de `damage_check` y este adaptador no la sintetiza.
  - La ruta del Bokoblin no tiene laboratorio de mundo: solo los pesos (`balance_lab`) y la compilación.
- **Chilfos y spam de Back Slice:** el spam sigue entrando cuando el Chilfos está comprometido en su contraataque o en el combo encadenado del 65 %, incluida la cola del C3 (retroceso y lanzamiento).
  - El laboratorio no simula que esos ataques golpeen a Link; en el juego interrumpirían el spam. Es la política aprobada de FIX06 y no se ha tocado.
  - Si en la prueba humana sigue siendo eficaz, las palancas son `kTwirlParryPct` (FIX06) y la cadena del 65 %.
- **Contacto solo de cuerpo con guardia efectiva:** con la guardia efectiva del Lizalfos, las esferas del cuerpo se apartan (nativo). Un golpe que esquiva la esfera del escudo pasa sin contacto: 0 HP y sin crédito de bloqueo.
- **Mortal Draw de remate:** las líneas fijadas en `kk_native_audit.py` cubren la ruta; la animación, el sonido y la altura del remate no se han tocado, pero su verificación visual sigue `[PEND]`.
