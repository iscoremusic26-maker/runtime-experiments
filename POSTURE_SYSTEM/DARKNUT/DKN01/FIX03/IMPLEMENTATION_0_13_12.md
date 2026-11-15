# LIGHT FADES TWICE 0.13.12 — DARKNUT MINIBOSS DKN01 FIX03

Estado: **HUMAN_RUNTIME_PENDING**. Compila (clang-cl local; MSVC en CI), pasa laboratorios, mutantes y auditorías; nadie lo ha jugado todavía.

## Base
- Fuente compilada de 0.13.11: `dc5fe6df56a16b44e76d5087baf028f3eee3a0bd` (+ `8a23a87`, registro CI). Rama `feature/light-fades-twice-darknut-miniboss-fix03-0-13-12` (worktree `runtime-experiments-dkn-fix03`); CI `ci/light-fades-twice-darknut-miniboss-fix03-0-13-12` (worktree `windows-build-lab-dkn-fix03`). Los worktrees de FIX01/FIX02 no se tocaron.
- `mod.cpp` sin cambios: **0 objetivos de hook nuevos, 0 imports nuevos** (DLL local: 156 imports idénticos a FIX02).
- Logs analizados: `dusklight-20261114-195050.log` y `dusklight-20261114-200429.log` (fuente `dc5fe6df56a1`).

## P0 — Lizalfos con Z-target: Link se gira y acaba de espaldas
Causa real (no es el lock-on, ni un giro del Lizalfos): la esfera de ataque del Lizalfos (`at_sph`, spl 0xD = ataque GRANDE) lleva un vector At. Link calcula la dirección de su reacción con él (`getDamageVec` → `GetTgRVecP`); en `procCoLargeDamageInit` vuela a lo largo de ese vector y, si para él apunta "hacia delante", se gira de espaldas a la fuente (`shape_angle.y = current.angle.y`). El nativo `MoveCAt` pone ese vector = (centro de este tick − centro anterior). Desde 0.12.x el módulo **recoloca** la esfera sobre Link en el tick de contacto; el tick siguiente el "centro anterior" es nuestro punto sobre Link y el vector nativo apunta **de Link hacia el Lizalfos**: Link salía despedido a través del Lizalfos y aterrizaba de espaldas (y un deslizamiento de guardia lo empujaba contra él).
Arreglo: en cada tick armado el vector se reconstruye desde los **centros nativos** (exactamente la velocidad de barrido vanilla) y se le quita solo la componente que apunta de Link hacia ese Lizalfos. Patrones, velocidades, ventanas, defensa y la opción Z-target personalizada intactos. Lab `liz_world_lab`: 6006 contactos, 0 vectores hacia dentro (sin el arreglo: 120). Mutantes nuevos `atvec_not_rebuilt` / `atvec_inward_kept` detectados. Integración por hunks inversos exactos (`ci/kk_policy.json`, etiqueta `fix03_0_13_12`). Log: `LIZ_SUMMARY part=FIX02_DISTANCE version=0.13.12 ... atvec_rebuilt= atvec_inward_removed=`.

## P0 — Empuje de Link al bloquear
Logs: el nativo daba 18,8 tras el primer frenado; FIX02 lo limitaba a 15/16/13. En F2, **78 de 125** deslizamientos llegaron encadenados (≤ 1,5 s del anterior): la distancia se acumulaba combo a combo.
FIX03 [PROVISIONAL]: maza 12 (~64 u), golpe de escudo/patada 12 (~64 u), espada 10 (~45 u); un deslizamiento encadenado (≤ 45 ticks del anterior del mismo Darknut) conserva ×0,80 y desde el tercero ×0,65 (nunca 0). Combo de 7 impactos bloqueado entero: ~176 u (0.13.11 ~520, nativo ~1190). Misma reacción, sonido, vibración, postura, golpe directo y rotura a 100. Log `LINK_SLIP_CAPPED ... chain=`.

## P0 — Tempo
- **F1 congelada**: huellas del laboratorio iguales a 0.13.11: planes F1 `58041.6504`, MoveInfo de F1 `21162.0`, combos F1 `386376.0` (calculadas con el `dkn_core.hpp` de `dc5fe6d`). El golpe de escudo de F1 no cambia.
- **F2/F3 combos ×1,25** (todos los intervalos de audio × 1,25: Δt_i/Δt_j exactos). Con escala 1,0 los planes reconstruidos dan la huella de 0.13.11 (`129229.2156` sin F2-C4): el único cambio es la escala, más el rango de corte de la patada.
- **Patada**: el corte de la patada pasa de 12..20 a 12..26 porque F2-C4 (patada→estocada, 33 ticks a ×1,25) exigía una recuperación a 0,515 (< 0,55). En el rig, cortar en 22-28 da **menos** salto de pose (42,6-46,0) que el corte 20 de 0.13.11 (52,0) (`tests/data/dkn_kick_cut_survey.txt`).
- **Golpes sueltos/contraataques ×1,20**, **patada ×1,12** (también la patada de pasividad, en su POST).

| Combo | 0.13.11 (ticks) | 0.13.12 (ticks) | × |
|---|---|---|---|
| F2-C1 | 8 9 8 9 9 25 (68) | 10 11 10 11 12 31 (85) | 1,250 |
| F2-C2 | 27 6 34 8 9 9 (93) | 33 8 42 11 11 11 (116) | 1,247 |
| F2-C3 | 20 6 25 19 7 24 10 10 (121) | 25 8 31 24 8 30 12 13 (151) | 1,248 |
| F2-C4 | 27 24 6 30 (87) | 33 30 8 38 (109) | 1,253 |
| Estocada / doble / patada sueltas | 33,0 / 50,0 / 29,0 | 39,6 / 60,0 / 32,5 | 1,20 / 1,20 / 1,12 |

Error por par ≤ 1 tick, acumulado ≤ 2, 0 velocidades fuera de [0,55, 2,40]. **Matriz de parry 46/46** (AT ≥ 5 ticks en cada impacto de combo, impacto dentro, ticket propio); golpe de escudo de F1 nativo (4 ticks).

## P0 — Defensa en F1, F2 y F3
- **Bloqueo normal = sin rebote, en todas las fases.** En F1 el escudo nativo (`mSphC` TgShield) hacía rebotar la espada de Link en CADA bloqueo; ahora `checkCutReverseAt` responde FALSE fuera de una ventana armada también en F1.
- **Parry real** = ventana armada (`mTimer10` + `field_0xa91`, TgShield) + rebote nativo `PROC_CUT_REVERSE` + **una** ganancia de postura de Link (**+20 F1, +25 F2/F3**) + **un** contraataque. Si el rebote se ve dos veces en el mismo tick (otro colisionador de Link) se mantiene pero no se cuenta.
- **Probabilidad por golpe NUEVO de Link** (de frente, a su alcance, Darknut libre), según su racha de golpes seguidos (hueco ≤ 1,5 s): **10 % / 25 % / 45 % / 60 %**. Una sola tirada (sin guardia × parry); medido en el lab: 9,95/25,19/44,78/59,77 % (F1) y 10,14/25,24/45,12/59,99 % (F2). Tras un parry real la racha vuelve a 1 y hay 60 ticks de enfriamiento. En F2/F3, si no hay intento, puede alzar una guardia normal (20 %→75 % con presión, sin rebote).
- **F1**: sin escudo (`mNextBreakPart ≥ 11` o pieza 12 rota) no hay parry. La guardia de F1 entra con su propio escritor `dkn_native_guard_enter_h` (TNA_GUARD, ACT_GUARDH 1); nunca se escribe ACT_GUARDL 0 sin golpe.
- Durante una ventana armada o con un contraataque pendiente no arranca ninguna iniciativa ni patada de pasividad (no se pierde el contraataque).

## P0 — Contraataques (uno por parry, sin cadenas nativas)
- F2/F3: patada / estocada / doble completo, tercios (lab 33,5/33,2/33,2 %).
- F1: golpe de escudo (solo con escudo) / maza lateral / maza vertical, tercios; sin escudo 50/50 lateral/vertical. Tempo de F1 sin cambios.

## P0 — F2-SINGLE-B y autoridad ofensiva
- El golpe suelto ordinario de F2/F3 es siempre la estocada; el doble completo queda en los combos y como contraataque.
- Los 233 `UNAUTHORIZED_NATIVE_ATTACK` de los logs eran **entradas** nativas (ATTACK* 0/10/11/20) escritas durante `action()` y vistas en el mismo POST: intentos que nunca se ejecutaron. Ahora: `NATIVE_ENTRY_SUPPRESSED executed=0` (y ese intento cuenta como punto de decisión propio); `UNAUTHORIZED_NATIVE_ATTACK executed=1` solo si un modo de ataque **en curso** aparece sin arriendo. Cada inicio propio lleva `owner=OWN_CONTROLLER`.

## P0 — Helm Splitter / Mortal Draw
- Log 195050: STAGGER_B fotograma 1 → HELM_START fotograma 15,1 → HELM_CONTACT 36 ticks después sobre esa pose. El segundo tambaleo sostenía **TNB_DOWN** fotograma 15, el clip nativo de *retroceso de guardia* (espada por encima de la cabeza): eso era la "animación de bloqueo".
- FIX03: **TNB_DAMAGE_R** (0x18, la reacción de daño nativa de F2), desde 0 con fundido 5 y sostenido en el fotograma 12: cabeza baja, espada baja (punta 150-192 bajo la cabeza), a 31-35 u de la pose SIPPU (tambaleos distintos).
- Mortal Draw (primer tambaleo, SIPPU agachado): sin cambios de clip; `field_0xa91` falso y sin TgShield durante el tambaleo; la extensión por remate en vuelo sube de 30 a 45 ticks [PROVISIONAL] para que un Helm Splitter / Mortal Draw tardío no caiga en la recuperación.
- Contacto → reacción de daño (no guardia) → caída → Finish. Levantamiento FIX02 y resurrección intactos (DKR01 sin cambios; `dkr_lab` 2318, `dkr_world_lab` 5007 PASS).

## Evidencia automática local
`dkn_lab` 167 157 comprobaciones PASS · mutantes locales: DKN 108/108 (en la 1.ª pasada sobrevivió `streak_kept_after_parry`: prueba reforzada), Lizalfos 239/239, Lizalfos mundo 202/202 (sobrevivía `velocity_kept`: nueva invariante «escudo alzado → vector At nulo», 4599 contactos, 0 no nulos) · `liz_world_lab` PASS (AtVec) · auditorías DKN (26 negativos), DKN nativa (95 hechos), DKR, kk, kk_source, liz, fix03, source, store, anclas de mutantes (1093) PASS · DLL clang-cl: 0 imports nuevos. CI: ver registro.

## Límites honestos
- Sin prueba en el juego. El arreglo del Lizalfos está demostrado sobre la mecánica nativa y el laboratorio de mundo, no con física real.
- Valores [PROVISIONAL]: topes 12/12/10 y ×0,80/×0,65, hueco de racha 45, enfriamiento 60, extensión 45.
- La patada cambia de rango de corte (12..26): es el único cambio de un movimiento.

## CI (windows-build-lab, rama `ci/light-fades-twice-darknut-miniboss-fix03-0-13-12`, fuente compilada `00b3ce6`)
| Perfil | Run | Resultado |
|---|---|---|
| FAST | 43673280999 | PASS (MSVC, PE: 0 imports nuevos) |
| INTEGRATION | 43673553387 | PASS (todos los laboratorios) |
| FULL | 43674303679 | **PASS**: todos los shards (DKN 108/108, DKR 67/67, Lizalfos 239/239, Lizalfos world 202/202, resto), finalize, descarga independiente |

Entregable: `LIGHT_FADES_TWICE_DARKNUT_MINIBOSS_FIX03_0_13_12_PRIVATE_TEST_windows-amd64_00b3ce6b1387.dusk`, 376 343 B, SHA-256 `075db091f9bb11c890c0fe8996f513cc35a78a44b0d6f3f78c9b711b53f9eec9` (artefacto 14145771534, caduca 2026-12-15; recalculado tras descarga). Clip FIX02 sin cambios. Estado: **HUMAN_RUNTIME_PENDING**.
