# POST00 — Decisión de arquitectura (Enemy Posture System, E_OC normal)

**Dictamen: GO_CONDITIONAL.** Existe una ruta concreta dentro de un `.dusk` autónomo y está verificada en la fuente y en el binario. Le faltan tres comprobaciones de runtime, que se ordenan como gates (§6). No equivale a un PASS funcional.

Las referencias `archivo:línea` se detallan en `DAMAGE_AND_FINISH_TRACE.md` (T§n).

## 1. Hechos que deciden

1. `daE_OC_c::damage_check` es un objetivo hookable. `action()` lo llama de verdad (thunk `0x14006c4ae` → RVA `0xe06390`). El manifiesto no tiene el flag INLINE y ya lo había verificado HM CP01. [B]
2. Dentro de `damage_check`, `setActionMode`, `offTgSph` y `cc_at_check` son llamadas reales a través de thunks. Después del último `setActionMode(DAMAGE)` solo queda el epílogo. [B] (T§2)
3. `setActionMode` solo escribe 8 cosas conocidas: `mOldActionMode`, `mActionMode`, `mOcState`, `field_0x6c0`, `field_0x6c2`, los bits CoSet/TgSet de `cc[0/1]` y el bit HeadLock. [S] `d_a_e_oc.cpp:584-594`
4. El daño, el SE de golpe, el hit-stop, la dirección del golpe y las señales de muerte ocurren dentro de `cc_at_check`, **antes** de elegir la reacción. La animación y la voz de la reacción ocurren después, en `executeDamage`/`executeBigDamage`, dentro del mismo `action()`. [S] (T§3)
5. El down flag que exige el Finish solo lo pone `executeBigDamage` estado 4, si `health ≥ 1`. Link lo vuelve a comprobar al aterrizar. [S] (T§4)
6. HM 2.0.3 engancha `cc_at_check` (PRE con prioridad −1e9 y POST con +1e9) y otros objetivos ajenos a E_OC. DEVF CP21 engancha `daE_OC_c::execute` (PRE+POST) y `daAlink_c::modelDraw`. Bars engancha `dMeter2_c::_execute/_draw/_delete`. **Ninguno engancha `daE_OC_c::damage_check`.** [S] `hm_203/core8/src/mod.cpp:60-73,1014-1029`; CP21 `expansion/mod.cpp:133-135,2020-2022`; `bars_203_hm/mod/src/mod.cpp:27-29`

## 2. Estrategias evaluadas

| | A. PRE de `setActionMode` con SKIP filtrado | **B. PRE/POST de `damage_check` con instantánea y restauración** (principal) | C. Variar las entradas en PRE (enmascarar `mCutType`, como DEVF CP19) o bifurcar |
|---|---|---|---|
| Objetivos | `setActionMode` y además `damage_check` para saber el contexto | Solo `damage_check` (exportado, `?damage_check@daE_OC_c@@QEAAXXZ`) | `damage_check` o `execute` |
| Firma | `void (daE_OC_c::*)(int,int)`, `QEAAXHH@Z` | `void (daE_OC_c::*)()`, `QEAAXXZ`, por `DEFINE_HOOK(&daE_OC_c::damage_check, …)` | — |
| Daño, muerte y efectos | Intactos (`cc_at_check` ya se ejecutó) | Intactos: no se salta nada y el original corre completo | El enmascarado solo cambia `my_val` 0–7. No puede evitar DAMAGE. Una bifurcación duplicaría `damage_check` |
| Supresión de DAMAGE | SKIP de un setter de 8 escrituras | El POST restaura las 8 escrituras con los valores de la instantánea PRE | No es posible |
| Supresión de BIG_DAMAGE no letal | Insuficiente: `offTgSph()` corre igualmente y deja TG apagado (actor invulnerable) | Posible: se restauran también los bits TgSet. `ClrTgHit` es inocuo | — |
| Conflictos | El SKIP cancela los PRE de menor prioridad de otros mods. Intercepta también las llamadas que hace DEVF a `setActionMode` (necesita filtro) | Un objetivo que ningún otro mod usa hoy. Los PRE/POST se anidan dentro del hook `execute` de DEVF y fuera del de `cc_at_check` de HM | — |
| Coste | Hook en un setter muy llamado | Dos callbacks por ejecución de cada E_OC (unos 10 Bokoblins → ~20 llamadas por tick) | — |
| Descarga en caliente | Si se descarga a mitad, el estado es nativo | Igual: las restauraciones solo dejan valores nativos previos | — |
| Veredicto | **Respaldo**, solo para DAMAGE, si B mostrara un problema en runtime | **Elegida** | Descartada |

No se usa `HOOK_SKIP_ORIGINAL` ni `replace` en ningún objetivo. Tampoco se copia `damage_check`.

## 3. Contrato de la estrategia B (diseño, sin implementar)

**PRE (`damage_check`)**, solo para actores admitidos (T§1):
- Guarda una instantánea con: `health`, `mActionMode`, `mOldActionMode`, `mOcState`, `field_0x6c0/6c2`, `field_0x6cc`, `mFlags` (HeadLock y CutDownHit), los bits CoSet/TgSet de `cc[0/1]` y el TG de cada esfera.
- Calcula `hit_expected = !CutDownHit && field_0x6cc==0 && (TG0||TG1)`.
- No escribe nada.

**POST (`damage_check`)** se ejecuta cuando ya han terminado `cc_at_check` y el POST de HM:
1. *Golpe aceptado* = `hit_expected` y `field_0x6cc` pasó de 0 a ≠0, o hubo transición de modo. Una sola contabilidad por impacto.
2. **Vetos absolutos.** No se interviene, solo se observa, si se cumple cualquiera:
   - `health_post ≤ 1`;
   - CutDownHit en PRE;
   - la ruta cancel-turn (`field_0x6cc == 3` tras la llamada);
   - un modo previo en DEATH, WATER_DEATH, FALL_DEAD, FALL, DEMO_MASTER, DEMO_CHILD, BIG_DAMAGE o TALK;
   - el resultado no es DAMAGE ni BIG_DAMAGE;
   - el mod está deshabilitado o el actor no está admitido.
3. **Sin ruptura** y la reacción está en la política de supresión (D2/D3): se restauran las 8 escrituras de `setActionMode`. Si la reacción era BIG_DAMAGE, se restauran además los bits TgSet de `cc[0/1]`. El modo de ataque sigue con su `mOcState` y sus temporizadores.
4. **Ruptura** en este golpe no letal: si el nativo ya eligió BIG_DAMAGE, se deja tal cual. Si eligió DAMAGE, se llama a `daE_OC_c::setActionMode(6, k)` y luego a `daE_OC_c::offTgSph()` (imports existentes en `windows-amd64.lib`), con `k ∈ {0,1,2}` según el `my_val` nativo (0 por defecto). No se toca `mFlags`: el down flag lo pondrá el juego. Después se marca `broken` y se reinicia P según la política de POST03.
5. Lo que corre después en `action()` (agua, caída, `executeXXX`) sigue siendo nativo y prevalece.

**Reloj:** la recuperación avanza en el PRE de cada ejecución del actor, con un contador de ticks de simulación propio. No usa reloj de pared, y la pausa la congela de forma natural. La ralentización según el HP efectivo usa `health/field_0x560`. Si existe el servicio opcional de vitales de HM (`com.dusklight.enemy_health_multiplier_203.vitals` v1.0, que Bars ya importa de forma opcional), se usa su vista efectiva. Sin HM, la vista nativa.

## 4. Módulos (POST01–POST07)

`admission` (clasificador), `ledger` (tabla fija de 32 entradas con clave (id, puntero, tick de primera vista), revalidada con `fopAcM_SearchByID` y desalojada por discrepancia o por barrido acotado), `posture_core` (P, Pmax, recuperación, ruptura; puro y testeable sin el juego), `reaction_gate` (B §3), `hud` (POST05), `log` (contadores acotados).

| CP | Contenido | Comportamiento |
|---|---|---|
| POST01 | Observador pasivo de `damage_check`: impactos, modos y HP (ver handoff) | Ninguno |
| POST02 | Gate de supresión: restaurar DAMAGE solo en ATTACK, interruptor de configuración, sin postura | Mínimo y reversible |
| POST03 | Postura P/Pmax, ruptura → BIG_DAMAGE nativo, Finish nativo | Núcleo |
| POST04 | Valores por tipo de ataque, recuperación dependiente del HP efectivo, vista HM opcional | Balance |
| POST05 | HUD J2D propio en `dMeter2_c::_draw` (POST), con el mismo patrón que Bars | Visual |
| POST06 | Matriz de coexistencia DEVF/HM/Bars, descarga y recarga, cambio de sala | Compatibilidad |
| POST07 | Paquete candidato privado | — |

**HUD (contrato, POST05):** hook POST en `dMeter2_c::_draw` con una puerta de tick de simulación, y en `_execute` para avanzar el tick. Exclusión: pausa, evento, ventana y `mStatus & (0x4000|0x40|0x100)`. Proyección con `mDoLib_project`. Todo igual que en Bars (`bars_203_hm/mod/src/game_bars.cpp:98-130`). Solo dibuja las entradas del ledger, sin barrido global de la cola de actores. Para quedar «debajo» de Bars se replica su ancla (`normal_height`, `reused/normal_model.h:21-24`) con un desplazamiento propio, sin importar ni parchear Bars. Ese acoplamiento es solo visual: si Bars no está, la barra se dibuja en la misma posición. Se oculta cuando `attention_info.flags==0` (muerte), igual que Bars.

## 5. Matriz de riesgos

| R | Requisito | Clasificación | Gravedad | Evidencia | Consecuencia si falla | Mitigación | Se prueba en |
|---|---|---|---|---|---|---|---|
| R01 | Fuente y SDK exactos | VERIFIED_SOURCE + VERIFIED_ABI_OR_TOOL | — | SOURCE_INVENTORY §1 | — | — | Cerrado |
| R02 | Clasificador E_OC normal por instancia | VERIFIED_SOURCE para E_OC frente a E_OC2. **INFERRED_NEEDS_RUNTIME** para nativo frente a DEVF Blue | Alta | T§1 | La postura se aplicaría a Blue, que DEVF ya modifica | D1. Log de admisión en POST01 con DEVF activo | POST01 / POST06 |
| R03 | Observar golpes y HP sin alterar nada | VERIFIED_SOURCE + VERIFIED_ABI_OR_TOOL (llamada real, sin inline) | Media | §1.1, T§2 | Sin observador no hay sistema | Fallo de instalación → mod inerte | POST01 [R] |
| R04 | Inhibir la reacción ordinaria conservando HP, muerte y efectos | VERIFIED_SOURCE + VERIFIED_ABI_OR_TOOL (tail sin efectos). Continuidad visual del ataque: **INFERRED_NEEDS_RUNTIME** | **Crítica** | §1.2–1.4 | Animación o IA incoherente al restaurar | Vetos §3; solo ATTACK en POST02; respaldo A | POST02 [R] |
| R05 | Derribo nativo en la ruptura | VERIFIED_SOURCE (ruta 780-781 replicada con funciones nativas). Comportamiento: INFERRED_NEEDS_RUNTIME | Alta | T§4 | Derribo anómalo | Llamar solo con HP>1 y un modo vivo | POST03 [R] |
| R06 | Finish solo con el down flag nativo | VERIFIED_SOURCE | Media | T§4 | — | No se escribe `mFlags` ni se toca a Link | POST03 [R] |
| R07 | Coexistencia con DEVF y HM | VERIFIED_SOURCE (sin objetivos compartidos). El orden real es INFERRED_NEEDS_RUNTIME. Fuente HM/Bars sin comprobación byte a byte: INCOMPLETE_DEPENDENCY_AUDIT | Alta | §1.6 | DEVF ajusta HP y modo en el POST de `execute`, después del POST de Posture. HM reconcilia HP antes | Vetos. Leer el HP en el POST de `damage_check`. Log de orden | POST01 / POST06 |
| R08 | Estado por instancia, limpieza y reentrada | VERIFIED_SOURCE (ID monótono, SearchByID) | Media | T§1, T§5 | Contaminación entre actores | Clave (id, ptr, primera vista), revalidación y capacidad fija | POST01 / POST06 |
| R09 | HUD autónomo con coste acotado | VERIFIED_SOURCE (patrón de Bars). En runtime: INFERRED_NEEDS_RUNTIME | Baja | §4 | Barra mal situada | Ancla replicada; sin barrido global | POST05 [R] |
| R10 | Reversión, fallos de instalación y descarga | VERIFIED_SOURCE (`hook.h` minor 1 `uninstall`, `hook.cpp:518-574`; el SKIP corta los PRE siguientes, `hook.cpp:605-609`; prioridad mayor primero y empate por orden de registro, `hook.cpp:140-143`) | Media | `hook.h:39-71`, `hook.cpp:431-437` | Hook a medias | Registrar el POST antes que el PRE (patrón DEVF). Si falla, desinstalar y quedar inerte | POST01 [R] |

## 6. Condiciones del GO (gates)

1. **G1 (POST01):** el detour se instala sin aviso de inline. Cada impacto aceptado se registra una sola vez, con el HP y el modo correctos, con y sin DEVF/HM/Bars. Se cumple el orden de anidamiento DEVF `execute` ⊃ Posture `damage_check` ⊃ HM `cc_at_check`.
2. **G2 (POST02):** restaurar DAMAGE en ATTACK mantiene el ataque visualmente coherente, sin congelaciones, sin invulnerabilidad y sin alterar muertes ni excepciones.
3. **G3 (POST03):** el BIG_DAMAGE forzado produce derribo, botón Finish, Finish y levantamiento nativos.

Si G2 falla con B, se prueba el respaldo A limitado a DAMAGE. Si falla también, el resultado es NO_GO solo para la «supresión en ataque», y la alternativa mínima es suprimir únicamente fuera de ATTACK. No se parchea el host.

## 7. Decisiones pendientes del usuario (no asumidas)

- **D1:** ¿DEVF Blue (recurso E_OC) entra en el alcance v1? Sin un servicio de identidad de DEVF no se distingue de forma fiable. *Recomendación:* v1 solo para actores no clasificados por DEVF. Mientras no haya señal, desactivar Posture si el servicio `dev.devf.encounter_placement.v11` está presente.
- **D2:** ¿En qué modos se suprime la reacción ordinaria? *Recomendación:* ATTACK en POST02. FIND como opción en POST03. WAIT/WALK/WATCH siguen nativos, porque la reacción provoca el aggro.
- **D3:** sin ruptura, ¿se convierten en «sin reacción» los BIG_DAMAGE nativos no letales (giro, salto, cuarto golpe del combo, especial, bola de hierro)? *Recomendación:* sí, de forma coherente con el objetivo de reservar el derribo para la ruptura, sumando mucha postura. Se prueba en POST03, no en POST02.
- **D4:** las reacciones utilitarias, como el gale del bumerán (DAMAGE 4) y el empujón del escudo (DAMAGE 3), ¿se conservan? *Recomendación:* conservarlas en v1.
- **D5:** ubicación exacta de la barra respecto a Bars (desplazamiento y escala).
