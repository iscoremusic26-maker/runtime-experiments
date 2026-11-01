# POST04 — Evidencia humana A1/B1 (saneada)

Fecha de análisis: 2026-11-01. Etiquetas: **[R]** juego real (logs del usuario leídos completos por Claude Code) · **[S]** fuente · **[C]** CI · **[L]** laboratorio · **[P]** pendiente.
Binario probado: `POSTURE_POST04_NUMERIC_OBSERVER_windows-amd64_ccf0f2d2b7b1.dusk` (SHA-256 `d43e46b37760f93090f162e3807f6b70640695dccda61870836000d1bf42f8f7`), compilado desde `ccf0f2d2b7b12092cf3407ae49bc8ba42a8ebd64`. **Este cierre no cambia ningún archivo compilado.**
Los logs crudos no están en el repositorio. Solo hay derivados de `evidence_tools/extract_posture_runtime.py` (lista blanca **por campo**; sin rutas, nombres de cuenta, direcciones ni ids de build) en `evidence/POST04_A1_B1_*`.

## 1. Logs
| | A1 | B1 |
|---|---|---|
| Archivo | `dusklight-20261101-102951.log` | `dusklight-20261101-102439.log` |
| Bytes / líneas (`splitlines`) | 160072 / 1960 | 982863 / 5847 |
| SHA-256 | `12fa22d0871b9f56661becd307db2e583408fa69a3e649662e8c4357f9c7ef17` | `d3595694ffe1856124074b66482815a8d5b52778bd8944d6a93c7e4464adb70c` |
| Mods | 2/2: POST04 0.4.0 + Zora Swim 1.3.0 (no es «vanilla estricto») | 8/8: POST04 + Zora Swim + HM CP11 + Bars CP06 + EVF 0.15.0 + Expansion 0.17.0 + Luau + Randomizer |
| Gancho | `resolve=MOD_OK`, `inline_sites_flag=0`, PRE `HOOK_CONTINUE` | igual |
| `POST04_INIT` | `passive=1 writes_to_game=0 game_actions=NONE`, `source_commit=ccf0f2d…` | igual |
| Cierre | `POST03_SHUTDOWN` + «all mods unloaded» | igual |

## 2. Reconstrucción independiente (0 violaciones)
El extractor une cada `POST03_HIT_EVENT` con su `POST04_POSTURE_HIT` por `(event, id, generation, family, at)` y recalcula la contabilidad. **Falla** ante cualquiera de estos casos:
- serial duplicado o no contiguo;
- golpe sin decisión de postura, o consumido dos veces;
- aritmética incorrecta, o razón de omisión incoherente con la política;
- más de un `BREAK_READY` por generación;
- contadores que bajan entre un resumen periódico y el de cierre;
- E1–E5 que no se cumplen con los números del propio resumen (aunque diga `ok=1`);
- invariantes distintos de 0, `inline_sites_flag≠0`, `delete_claim` indebido o cierre anómalo.

Resultado sobre A1+B1: **0 violaciones**, y dos ejecuciones dan salidas idénticas byte a byte. El extractor tiene 10 pruebas y detecta 14 de 14 mutaciones propias. Mi primera versión daba un falso positivo (trataba `units_live`, un valor instantáneo, como contador acumulado); lo corregí antes de cerrar.

| Magnitud | A1 | B1 | Total |
|---|---|---|---|
| Informes (eventos) | 1 | 26 | **27** |
| `HIT_CONFIRMED` / Finish nativos | 1 / 0 | 23 / 3 | **24 / 3** |
| Familias de los confirmados | SWORD 1 | SWORD 19, SHIELD_ATTACK 3, OTHER_VERIFIED 1 | |
| Ponderados (APPLY) | 0 | 12 (todos SWORD) | **12** |
| Omitidos | 1 `LETHAL` | 6 `BREAK_READY_LATCHED`, 4 `ZERO_WEIGHT_POLICY`, 1 `LETHAL` | |
| Cruces de umbral / líneas `BREAK_READY` | 0 / 0 | 2 / 2 (162/9 y 565/13) | **2** |
| Unidades añadidas / recuperadas / cerradas / vivas | 0 / 0 / 0 / 0 | 300 / 7 / 293 / 0 (`300 = 7 + 293 + 0`) | |
| Carreras de recuperación | 0 | 1 (505/18: 25→18, cortada por un golpe) | |
| Sidecars ligados / retirados | 4 / 1 | 9 / 9 | |
| `POST03_CONSERVATION` | `started=1 judged=1 pending=0 ok=1` | `started=26 judged=26 pending=0 ok=1` | |
| `POST04_CONSERVATION` | `ok=1`, E1–E5 = 1 | `ok=1`, E1–E5 = 1 | |
| Invariantes (`underflow`, `overflow`, `generation_leak`, `multi_consume`, `ring_dropped`) | 0 | 0 | |
| Resúmenes periódicos (acumulativos; no se suman) | 1 | 3 | |

## 3. Los 27 informes
`antes→después` es la postura de **esa** generación; `marca` señala el golpe que cruzó a 100. Modos: 3 FIND, 4 ATTACK, 5 DAMAGE, 6 BIG_DAMAGE, 7 WATCH, 9 DEATH (enum de `d_a_e_oc.cpp:20-37`).

| Ses. | ev | id/gen | Tipo | Familia | tg | hp | modo | estado | POST04 | antes→después | marca |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A1 | 1 | 161/7 | HIT | SWORD | cc0 | 40>0 | 8>6 | 1>0 | SKIP LETHAL | 0→0 |  |
| B1 | 1 | 162/9 | HIT | SWORD | cc0 | 220>200 | 7>5 | 4>0 | APPLY | 0→25 |  |
| B1 | 2 | 162/9 | HIT | SWORD | cc0 | 202>182 | 3>5 | 4>0 | APPLY | 25→50 |  |
| B1 | 3 | 162/9 | HIT | SWORD | cc0+cc1 | 186>166 | 4>5 | 0>0 | APPLY | 50→75 |  |
| B1 | 4 | 162/9 | HIT | SWORD | cc1 | 170>150 | 3>5 | 4>0 | APPLY | 75→100 | BREAK_READY |
| B1 | 5 | 162/9 | HIT | SWORD | cc0+cc1 | 154>134 | 4>5 | 0>0 | SKIP BREAK_READY_LATCHED | 100→100 |  |
| B1 | 6 | 162/9 | HIT | SWORD | cc1 | 137>117 | 3>5 | 4>0 | SKIP BREAK_READY_LATCHED | 100→100 |  |
| B1 | 7 | 162/9 | HIT | SWORD | cc0+cc1 | 147>127 | 4>5 | 0>0 | SKIP BREAK_READY_LATCHED | 100→100 |  |
| B1 | 8 | 162/9 | HIT | SWORD | cc0+cc1 | 127>107 | 5>5 | 5>1 | SKIP BREAK_READY_LATCHED | 100→100 |  |
| B1 | 9 | 162/9 | HIT | SWORD | cc0+cc1 | 108>88 | 5>5 | 5>0 | SKIP BREAK_READY_LATCHED | 100→100 |  |
| B1 | 10 | 162/9 | HIT | SHIELD_ATTACK | cc0+cc1 | 89>89 | 5>5 | 5>3 | SKIP ZERO_WEIGHT_POLICY | 100→100 |  |
| B1 | 11 | 162/9 | HIT | SWORD | cc0+cc1 | 91>0 | 5>6 | 5>1 | SKIP LETHAL | 100→100 |  |
| B1 | 12 | 505/18 | HIT | SHIELD_ATTACK | cc1 | 220>220 | 7>5 | 4>3 | SKIP ZERO_WEIGHT_POLICY | 0→0 |  |
| B1 | 13 | 505/18 | HIT | SWORD | cc0 | 220>190 | 5>6 | 5>1 | APPLY | 0→25 |  |
| B1 | 14 | 505/18 | HIT | SWORD | cc0+cc1 | 130>100 | 7>6 | 4>0 | APPLY | 18→43 |  |
| B1 | 15 | 505/18 | FINISH | — | none | 105>0 | 6>9 | 5>1 | — | — |  |
| B1 | 16 | 565/13 | HIT | SWORD | cc0+cc1 | 220>200 | 7>5 | 4>0 | APPLY | 0→25 |  |
| B1 | 17 | 565/13 | HIT | SWORD | cc1 | 203>183 | 3>5 | 4>0 | APPLY | 25→50 |  |
| B1 | 18 | 565/13 | HIT | SWORD | cc0+cc1 | 184>164 | 5>5 | 5>1 | APPLY | 50→75 |  |
| B1 | 19 | 565/13 | HIT | SWORD | cc0+cc1 | 165>145 | 5>5 | 5>0 | APPLY | 75→100 | BREAK_READY |
| B1 | 20 | 565/13 | HIT | SHIELD_ATTACK | cc0 | 119>119 | 7>5 | 4>3 | SKIP ZERO_WEIGHT_POLICY | 100→100 |  |
| B1 | 21 | 565/13 | HIT | SWORD | cc0 | 121>91 | 5>6 | 5>1 | SKIP BREAK_READY_LATCHED | 100→100 |  |
| B1 | 22 | 565/13 | FINISH | — | none | 26>0 | 6>9 | 5>1 | — | — |  |
| B1 | 23 | 506/19 | HIT | OTHER_VERIFIED | cc0 | 220>200 | 7>5 | 4>2 | SKIP ZERO_WEIGHT_POLICY | 0→0 |  |
| B1 | 24 | 506/19 | HIT | SWORD | cc0+cc1 | 202>182 | 5>5 | 5>0 | APPLY | 0→25 |  |
| B1 | 25 | 506/19 | HIT | SWORD | cc0+cc1 | 185>155 | 3>6 | 4>0 | APPLY | 25→50 |  |
| B1 | 26 | 506/19 | FINISH | — | none | 159>0 | 6>9 | 5>1 | — | — |  |

## 4. Lo que demuestran estos dos logs
- **Acumulación [R]:** 12 golpes de espada no letales, cada uno con +25 aplicado una sola vez. Los dos actores llevados al umbral recorren exactamente `0→25→50→75→100`: 162/9 en los ticks 3283, 3325, 3386 y 3444, y 565/13 en 6654, 6712, 6727 y 6741. Con `tg=cc0+cc1` sigue habiendo un solo consumo.
- **Marca de ruptura [R]:** una línea `POST04_BREAK_READY … game_action=NONE` por actor. Los golpes posteriores al mismo actor se omiten como `BREAK_READY_LATCHED` y no reemiten la marca.
- **Recuperación [R]:** 505/18 recibe +25 en el tick 5314 y el siguiente golpe en el 5476 (162 ticks después). La línea registra `from=25 to=18`: 7 unidades, que es exactamente `(162 − 120) / 6` con retardo 120 y cadencia 1/6. El golpe parte de 18 (18→43).
- **Peso cero [R]:** se omiten con `ZERO_WEIGHT_POLICY` tres SHIELD_ATTACK (los tres sin pérdida de HP) y un OTHER_VERIFIED (`at=0x00080000`, HP 220→200). No se infiere qué arma es `0x00080000`.
- **Letal y Finish [R]:** el único golpe de A1 mata (40>0) y se omite como `LETHAL`. **Que A1 no pondere nada es correcto, no un fallo.** Los 3 Finish de B1 no tienen decisión de postura.
- **Identidad [R]:** los sidecars se retiran con `LOOKUP_ABSENT_VERIFIED` cuando corresponde. Los actores con marca se retiran con `final=100 latched=1`, sin traslado a otra generación.

## 5. Otros mods (solo B1, solo lo que aparece)
- **HM:** `events=77 valid=77`, `HP relation match=77 diff=0`. Su denominador son las llamadas a `cc_at_check`, no el de POST04.
- **Bars:** `barsDrawn=12612`.
- **Expansion:** 27 `PERF_WINDOW` (telemetría).

Nada de esto autoriza a afirmar compatibilidad universal.

## 6. Incidencias (criterio exacto, sin causalidad)
| | A1 | B1 |
|---|---|---|
| `CalcDivideInfo` | 24 | 670 |
| texturas | 90 | 114 |
| `PERF_WINDOW` (telemetría, no avisos) | 0 | 27 |

## 7. Veredicto
| Etiqueta | Estado |
|---|---|
| `POST04_A1_SCOPED_RUNTIME_PASS` | **sí**: arranque, identidad, golpe letal omitido y cierre. **No** valida acumulación ni recuperación |
| `POST04_B1_FULL_STACK_SCOPED_RUNTIME_PASS` | **sí** |
| `POST04_ACCUMULATION_SCOPED_RUNTIME_PASS` | **sí** (B1, SWORD) |
| `POST04_REGEN_SCOPED_RUNTIME_PASS` | **sí, acotado**: una carrera de 7 unidades, nunca hasta 0 |
| `POST04_BREAK_MARKER_SCOPED_RUNTIME_PASS` | **sí**: 2 marcas, 0 duplicadas |
| `POST04_RUNTIME_PASS_SCOPED` | **sí** |
| `UNIVERSAL_COMPATIBILITY_PASS`, `BALANCE_APPROVED`, `PERFORMANCE_PASS`, `POST05_RUNTIME_PASS` | **no** |

`BREAK_READY` sigue siendo solo una marca: POST04 no causó ningún derribo.

## 8. No cubierto
- IRON_BALL +50 (no apareció).
- Recuperación completa hasta 0.
- Recuperación durante menús o pausa (`TIMEBASE_PAUSE_UNVERIFIED`).
- ARROW, BOMB, BOOMERANG, SLINGSHOT y AT_TYPE_40.
- Rendimiento aislado.
- Políticas específicas de Blue (D1).
- Compatibilidad universal.
