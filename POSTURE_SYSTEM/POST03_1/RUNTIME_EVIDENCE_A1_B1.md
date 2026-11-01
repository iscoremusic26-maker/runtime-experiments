# POST03.1 — Evidencia humana A1/B1 (saneada)

Fecha de análisis: 2026-11-01. Etiquetas: **[R]** juego real (logs del usuario, leídos completos por Claude Code) · **[S]** fuente · **[C]** MSVC/CI · **[L]** laboratorio · **[P]** pendiente.
Los logs crudos **no están** en el repositorio, ni en PR, CI o artefactos. Aquí solo hay la salida de `tests/extract_runtime_evidence_a1_b1.py` (lista blanca de campos, sin rutas, nombres de cuenta, direcciones ni ids de build). Datos: `evidence/POST031_A1_B1_*` (TSV de eventos, JSON de resumen, manifiesto de origen y esquema).

## 1. Logs y verificación
| | A1 | B1 |
|---|---|---|
| Archivo | `dusklight-20261101-090925.log` | `dusklight-20261101-090302.log` |
| Bytes (exactos) | 332709 | 890364 |
| Líneas (`splitlines`) | 4200 | 7007 |
| SHA-256 | `b8424dbda469c18c88358047ec92369ad6faaf845d2acbee66a31ac61d031b55` | `427ef9f66da5ba054a652413382b8b8cc0c2cc46e8fb6fb3b00541878118372f` |
| Hash/tamaño/líneas vs. lo declarado | coinciden | coinciden |
| Mods | 2/2: POST03.1 0.3.1 + Zora Swim 1.3.0 | 8/8: POST03.1 0.3.1 + HM CP11 + Enemy Health Bars CP06 + Enemy Variant Framework 0.15.0 + Bokoblin Expansion 0.17.0 + Zora Swim 1.3.0 + Luau 1.0.0 + Randomizer 1.0.6 |
| Host / backend | 2.0.3.0 / D3D12 | 2.0.3.0 / D3D12 |
| Gancho | `resolve=MOD_OK`, `same_address=1`, `inline_sites_flag=0`, `pre=MOD_OK post=MOD_OK pre_returns=HOOK_CONTINUE_ALWAYS` | igual |
| Compilación declarada en `POST03_1_INIT` | `cab67784e418fbcca0dd99d145eaf7168c50ea4a`, `deref_gate=eq_raw_hit_obj+align4`, `sizeof_cCcD_Obj=136` | igual |
| Cierre | `POST03_SHUTDOWN` antes de «all mods unloaded»; `hook_removal=HOST_DETACH instances_dereferenced=0` | igual |

A1 se nombra «POST03.1 sin otros mods de combate» (lleva Zora Swim); **no** es «POST03.1 solo».

## 2. Resultado reconstruido desde los bytes
Los contadores se **recomputaron** desde las 36 líneas de evento y las líneas de ciclo de vida y se contrastaron con los contadores `SHUTDOWN` del propio mod (`derived.discrepancies`): **0 discrepancias en ambos logs** (comprobaciones de `cross_check()` del extractor: familias, clases, esferas, ciclo de vida, conservación). No se sumó ningún checkpoint anterior a estos 36.

| Contador | A1 | B1 | Total |
|---|---|---|---|
| Eventos emitidos | 12 | 24 | **36** |
| `HIT_CONFIRMED` | 12 | 21 | **33** |
| `FINISH_NATIVE_OBSERVED` (no son golpes; fuera del denominador 33) | 0 | 3 | **3** |
| Lecturas válidas del tipo nativo (de `HIT_CONFIRMED`) | 12/12 | 21/21 | **33/33** |
| `family=SWORD` | 6 | 17 | **23** |
| `family=IRON_BALL` | 2 | 2 | **4** |
| `family=BOOMERANG` | 0 | 1 | **1** |
| `family=OTHER_VERIFIED` (`at=0x00080000`; arma NO identificada) | 4 | 1 | **5** |
| `UNAVAILABLE` / `AMBIGUOUS` / ARROW / BOMB / SHIELD / SLINGSHOT / AT_TYPE_40 | 0 | 0 | **0** (no aparecen) |
| `SELECTED_FRESH_MATCH_CC0` / `CC1` | 4 / 8 | 1 / 20 | 5 / 28 |
| `sel_class` `mod8_0` / `mod8_4` | 11 / 1 | 1 / 20 | 12 / **21** |
| `tg=cc0+cc1` (un evento cada uno) | 2 (`pair_distinct=1`) | 13 (`pair_distinct=0`) | 15 |
| Letales (`lethal=1`) | 8 | 4 (1 `HIT_CONFIRMED` + 3 Finish) | 12 |
| `HIT_CONFIRMED` sin cambio de HP | 0 | 1 | 1 |
| Anomalías / `processed_mismatch` / `not_processed` / `finish_unexpected` | 0 | 0 | 0 |
| `duplicates_suppressed` / `cross_generation_drops` / `post_generation_mismatch` / `stale_frames` | 0 | 0 | 0 |
| `POST03_CONSERVATION` | `started=12 judged=12 pending=0 ok=1` | `started=24 judged=24 pending=0 ok=1` | |
| Instancias (`records_created`) / `death_seen` / `absent_verified` | 20 / 14 / 20 (`active=0`) | 21 / 11 / 18 (`active=3`) | |
| `ADMISSION_CHANGED` (siempre `identity=KEPT`) | 0 | 26 | |
| Llamadas al gancho (`calls`) | 23950 | 44334 | |
| Líneas del mod escritas (vida/golpe/otras/resumen) | 54/12/3/4 | 76/24/3/8 | sin descartes (`dropped=0`, `log_errors=0`) |

**Aviso de lectura.** «33/33 clasificados» significa **lectura válida del tipo nativo**. 28 de ellos tienen una familia identificada (SWORD, IRON_BALL, BOOMERANG) y 5 son `OTHER_VERIFIED`: el tipo se leyó y no pertenece a la cadena nativa conocida; no se afirma qué arma es. Nada de HM se usó para clasificar.

## 3. Los 36 eventos
`#` es el orden dentro de la sesión; `Link` es el pid de `daAlink_c` vigente (cambia al cargar un stage). `hp` = nativo visible en el POST (con HM es el HP tras su reconciliación). `modo` = `mActionMode` antes>después.

| Ses. | # | id/gen | Link | Evento | Familia (at) | tg | clase sel / raw | hp | letal | modo |
|---|---|---|---|---|---|---|---|---|---|---|
| A1 | 1 | 161/7 | 105 | HIT | SWORD (0x04000002) | cc1 | mod8_0 / null/mod8_0 | 40>0 | 1 | 7>6 |
| A1 | 2 | 162/8 | 105 | HIT | OTHER_VERIFIED (0x00080000) | cc0 | mod8_0 / mod8_0/null | 40>20 | 0 | 3>5 |
| A1 | 3 | 162/8 | 105 | HIT | SWORD (0x04000002) | cc0+cc1 | mod8_0 / mod8_0/mod8_0 | 20>0 | 1 | 3>6 |
| A1 | 4 | 221/3 | 105 | HIT | OTHER_VERIFIED (0x00080000) | cc1 | mod8_4 / null/mod8_4 | 40>20 | 0 | 3>5 |
| A1 | 5 | 221/3 | 105 | HIT | IRON_BALL (0x00400000) | cc1 | mod8_0 / null/mod8_0 | 20>0 | 1 | 4>6 |
| A1 | 6 | 220/2 | 105 | HIT | IRON_BALL (0x00400000) | cc0 | mod8_0 / mod8_0/null | 40>0 | 1 | 4>6 |
| A1 | 7 | 539/17 | 483 | HIT | OTHER_VERIFIED (0x00080000) | cc0 | mod8_0 / mod8_0/null | 40>20 | 0 | 3>5 |
| A1 | 8 | 539/17 | 483 | HIT | SWORD (0x04000002) | cc0+cc1 | mod8_0 / mod8_0/mod8_0 | 20>0 | 1 | 5>6 |
| A1 | 9 | 598/12 | 483 | HIT | SWORD (0x04000002) | cc1 | mod8_0 / null/mod8_0 | 40>0 | 1 | 4>6 |
| A1 | 10 | 599/13 | 483 | HIT | SWORD (0x04000002) | cc1 | mod8_0 / null/mod8_0 | 40>0 | 1 | 4>6 |
| A1 | 11 | 540/18 | 483 | HIT | OTHER_VERIFIED (0x00080000) | cc0 | mod8_0 / mod8_0/null | 40>20 | 0 | 3>5 |
| A1 | 12 | 540/18 | 483 | HIT | SWORD (0x04000002) | cc1 | mod8_0 / null/mod8_0 | 20>0 | 1 | 3>6 |
| B1 | 1 | 161/8 | 105 | HIT | SWORD (0x04000002) | cc1 | mod8_4 / null/mod8_4 | 220>200 | 0 | 3>5 |
| B1 | 2 | 161/8 | 105 | HIT | SWORD (0x04000002) | cc0+cc1 | mod8_4 / mod8_4/mod8_4 | 201>181 | 0 | 5>5 |
| B1 | 3 | 161/8 | 105 | HIT | SWORD (0x04000002) | cc0+cc1 | mod8_4 / mod8_4/mod8_4 | 182>162 | 0 | 5>5 |
| B1 | 4 | 161/8 | 105 | HIT | SWORD (0x04000002) | cc0+cc1 | mod8_4 / mod8_4/mod8_4 | 163>143 | 0 | 5>5 |
| B1 | 5 | 161/8 | 105 | HIT | SWORD (0x04000002) | cc0+cc1 | mod8_4 / mod8_4/mod8_4 | 144>124 | 0 | 5>5 |
| B1 | 6 | 161/8 | 105 | HIT | SWORD (0x04000002) | cc0+cc1 | mod8_4 / mod8_4/mod8_4 | 126>96 | 0 | 5>6 |
| B1 | 7 | 161/8 | 105 | FINISH | — | none | null / null/null | 101>0 | 1 | 6>9 |
| B1 | 8 | 162/9 | 105 | HIT | OTHER_VERIFIED (0x00080000) | cc0 | mod8_4 / mod8_4/null | 220>200 | 0 | 7>5 |
| B1 | 9 | 162/9 | 105 | HIT | SWORD (0x04000002) | cc0+cc1 | mod8_4 / mod8_4/mod8_4 | 202>182 | 0 | 5>5 |
| B1 | 10 | 162/9 | 105 | HIT | IRON_BALL (0x00400000) | cc1 | mod8_4 / null/mod8_4 | 185>65 | 0 | 3>6 |
| B1 | 11 | 162/9 | 105 | HIT | SWORD (0x04000002) | cc1 | mod8_4 / null/mod8_4 | 74>54 | 0 | 3>5 |
| B1 | 12 | 162/9 | 105 | HIT | SWORD (0x04000002) | cc0+cc1 | mod8_4 / mod8_4/mod8_4 | 55>35 | 0 | 5>5 |
| B1 | 13 | 162/9 | 105 | HIT | SWORD (0x04000002) | cc0+cc1 | mod8_4 / mod8_4/mod8_4 | 36>16 | 0 | 5>5 |
| B1 | 14 | 162/9 | 105 | HIT | SWORD (0x04000002) | cc0+cc1 | mod8_4 / mod8_4/mod8_4 | 19>0 | 1 | 3>6 |
| B1 | 15 | 868/18 | 812 | HIT | SWORD (0x04000002) | cc1 | mod8_4 / null/mod8_4 | 220>200 | 0 | 7>5 |
| B1 | 16 | 868/18 | 812 | HIT | SWORD (0x04000002) | cc1 | mod8_4 / null/mod8_4 | 201>181 | 0 | 5>5 |
| B1 | 17 | 868/18 | 812 | HIT | SWORD (0x04000002) | cc0+cc1 | mod8_4 / mod8_4/mod8_4 | 183>163 | 0 | 3>5 |
| B1 | 18 | 868/18 | 812 | HIT | IRON_BALL (0x00400000) | cc1 | mod8_4 / null/mod8_4 | 166>46 | 0 | 3>6 |
| B1 | 19 | 868/18 | 812 | HIT | BOOMERANG (0x00010000) | cc1 | mod8_0 / null/mod8_0 | 55>55 | 0 | 3>5 |
| B1 | 20 | 868/18 | 812 | HIT | SWORD (0x04000002) | cc0+cc1 | mod8_4 / mod8_4/mod8_4 | 57>37 | 0 | 5>5 |
| B1 | 21 | 868/18 | 812 | HIT | SWORD (0x04000002) | cc0+cc1 | mod8_4 / mod8_4/mod8_4 | 39>9 | 0 | 5>6 |
| B1 | 22 | 868/18 | 812 | FINISH | — | none | null / null/null | 14>0 | 1 | 6>9 |
| B1 | 23 | 929/14 | 812 | HIT | SWORD (0x04000002) | cc0+cc1 | mod8_4 / mod8_4/mod8_4 | 187>157 | 0 | 7>6 |
| B1 | 24 | 929/14 | 812 | FINISH | — | none | null / null/null | 162>0 | 1 | 6>9 |

Reconstrucción por instancia `(id, generation)` (completa en `evidence/POST031_A1_B1_SUMMARY_SANITIZED.json`, `actors`): los 33 golpes confirmados recaen en 12 pares id/generation (A1: 8, B1: 4). Los tres Finish de B1 (161/8, 868/18, 929/14) recaen en actores que ya habían recibido `HIT_CONFIRMED` (6, 7 y 1 respectivamente); los tres traen `life=DEATH_SEEN` y `mode 6>9`; ninguno se cuenta como golpe.

## 4. Hipótesis de alineación, contrastada
- **POST03 (0.3.0, sesiones A/B del 2026-11-01 anterior):** 20/24 `HIT_CONFIRMED` quedaron `UNAVAILABLE` por `SELECTED_COLLIDER_IMPLAUSIBLE`; 4/24 SWORD. [R]
- **POST03.1 (0.3.1), A1 + B1:** 33/33 lecturas válidas, 0 `UNAVAILABLE`. De ellas **21 con `sel_class=mod8_4`** (puntero múltiplo de 4 y no de 8), justo la clase que la guarda de 8 bytes de POST03 rechazaba. [R]
- Todas las lecturas con `mod8_4` salieron con `SELECTED_FRESH_MATCH_*` (el valor es el hit obj crudo de la misma llamada) y dieron un tipo coherente: SWORD (17), IRON_BALL (2) y OTHER_VERIFIED (2); 0 fallos de lectura.
- **Conclusión justificada:** los datos son **coherentes con** que el rechazo de POST03 era espurio por exigir alineación de 8 y **respaldan** la corrección. `COLLIDER_ALIGNMENT_RUNTIME_OBSERVED`. No es una demostración contrafactual: no hay una misma instancia de Link ejecutada con POST03 y POST03.1, y los logs de POST03 no contienen el residuo del puntero. [R]+[S]
- **Corrección de una frase anterior:** en la evidencia A/B se observó «resultado constante por instancia de Link». A1/B1 matiza: la clase depende del **objeto collider concreto**, no de la instancia de Link entera. En A1 (Link pid 105) hay un collider `mod8_0` (5 eventos) y otro `mod8_4` (1 evento, `OTHER_VERIFIED`); en B1 (Link pid 812) el bumerán es `mod8_0` y la espada/bola de hierro `mod8_4`. Sigue siendo compatible con colliders miembros de `daAlink_c` colocados con alineación de 4 por el heap, y con colliders de otro objeto (bumerán) a 8, pero la afirmación se limita a lo observado.
- Los punteros `mod8_0` también leen bien (12): la corrección no degrada el caso ya soportado.

## 5. Casos relevantes
- **Bumerán sin pérdida de HP (B1 #19, id 868 gen 18):** `HIT_CONFIRMED`, `family=BOOMERANG`, `at=0x00010000`, `hp=55>55`, `lethal=0`, `mode 3>5` con cooldown puesto (reacción comprometida). Demuestra que `HIT_CONFIRMED` **no** implica pérdida de HP. Es el único caso del tipo en 33.
- **`OTHER_VERIFIED` (5):** todos `at=0x00080000`, ninguno letal, todos restan 20 HP (A1 ×4 con HP 40>20; B1 ×1). No se infiere arma ni se llama «bomba»: no hay evidencia. Son, además, los **únicos** impactos confirmados no letales de A1.
- **Escala de HP con HM:** en B1 (con HM) los HP iniciales observados son 187 y 220 y los golpes de espada restan 20 o 30 (la bola de hierro 120); en A1 (sin HM) el HP inicial es 40 y las muertes son de uno o dos golpes (los letales aparecen recortados al HP restante). El peso de cualquier política futura no puede derivarse de la cantidad de daño.
- **Un golpe letal con `HIT_CONFIRMED`** (B1 #14, SWORD, `hp 19>0`, `mode 3>6`) y Finish nativos separados (B1 #7, #22, #24; HP 101, 14 y 162 antes). Ejemplo de los dos caminos de muerte observados.
- **Cambio de admisión:** en B1, 26 transiciones `E_OC_CANDIDATE ↔ UNKNOWN_UNSAFE` en cuatro actores (ids 221/222 y 928/929), todas `identity=KEPT`; el actor 929 las sufrió y después recibió golpe y Finish. No se atribuye la causa (la sospecha, `AtAtp` de Blue/DEVF, sigue sin demostrar: `origin=UNDETERMINED`).
- **Cambios de sala / Link:** A1 creó 4 instancias de Link (pids 17, 105, 314, 483) y B1 6 (17, 105, 298, 505, 574, 812); los golpes ocurrieron bajo los pids 105 y 483 (A1) y 105 y 812 (B1). `epoch` del observador: 3→5 (A1), 3→7 (B1).

## 6. Otros mods: solo lo que aparece
- **HM (B1)** [R]: `cc_at_check pre=65 post=65 paired=65`, `unmatchedPost=0 orphanPre=0`; `events=65 valid=65`, `HP relation: match=65 diff=0 statusDiff=0`; `masterX2=52`. Combos de daño: SWORD 52, STUN 5, ARROW 5, HEAVY 2, OTHER 1. **El denominador de HM (65 `cc_at_check`) no es el de POST03.1 (21 `HIT_CONFIRMED` + 3 Finish):** no se igualan ni se usan para clasificar. En particular, las flechas de HM no se atribuyen a ningún evento de POST03.1.
- **Bars (B1)** [R]: puente HM `queries=124236 ok=70412 unavailable=0 invalid=0 rejected=0`; `barsDrawn=12257 refused=0`.
- **DEVF / Expansion (B1)** [R]: 32 `REQUEST_ACCEPTED` y 32 `REMOVE_RESULT`; 27 líneas `PERF_WINDOW` (todas con `MEASUREMENT_NOT_AN_ERROR`, aunque la etiqueta de nivel del log sea ERROR). Sin evidencia de interacción con POST03.1.
- **Zora Swim, Luau, Randomizer:** presentes y cargados; sin hallazgos.

## 7. Incidencias (conteo por criterio exacto; sin causalidad)
| Criterio | A1 | B1 |
|---|---|---|
| Líneas `[WARNING \| dusk] CalcDivideInfo` | 250 | 18 |
| Líneas `[WARNING \| aurora::texture] texture_replacement:` | 111 | 153 |
| Líneas `event=PERF_WINDOW` | 0 | 27 |
No hay un A/B que permita atribuir ninguna de ellas a POST03.1 (A1 tiene más `CalcDivideInfo` que B1 con menos mods). No son un perfil de rendimiento de POST04.

## 8. Veredicto de la evidencia
| Etiqueta | Estado | Alcance |
|---|---|---|
| `POST031_A1_SCOPED_RUNTIME_PASS` | **sí** | 12 impactos, 0 anomalías, conservación `ok=1 pending=0`, cierre normal, gancho `MOD_OK`/`inline_sites_flag=0`; sin crash visible en el log |
| `POST031_B1_SCOPED_RUNTIME_PASS` | **sí** | 8/8 mods; 21 impactos + 3 Finish; HM 65/65 `diff=0`; Bars sin rechazos; cierre normal |
| `COLLIDER_ALIGNMENT_RUNTIME_OBSERVED` | **sí** | 21 lecturas `mod8_4` válidas con igualdad frente al hit obj crudo; coherente con la hipótesis, no contrafactual |
| `CLASSIFICATION_SCOPED_RUNTIME_PASS` | **sí, acotado** | lectura de tipo 33/33; familias identificadas: SWORD, IRON_BALL, BOOMERANG; 5 `OTHER_VERIFIED` sin arma |
| `UNIVERSAL_COMPATIBILITY_PASS` | **false** | |
| `POST04_HUMAN_RUNTIME_PENDING` | **true** | POST04 aún no existe en juego |
Esto es evidencia de **juego real de estos dos logs únicamente**. Una observación humana de que «se veía normal» no figura en los logs y no se afirma.

## 9. Límites
- Sin evidencia de ARROW, BOMB, SHIELD_ATTACK, SLINGSHOT y AT_TYPE_40 en POST03.1, ni de casos adversariales (puntero no coincidente en juego). Sus rutas siguen cubiertas solo por laboratorio.
- No se conoce subtipo de espada, atacante, potencia ni la ejecución de `cc_at_check`.
- No hay medición de rendimiento. Los avisos del §7 no se atribuyen.
- D1–D5 siguen abiertas. G2 y G3: `NOT_STARTED`.
- Dos Link pids de B1 (105 y 812) y dos de A1 (105 y 483) es una muestra pequeña de configuraciones del heap.
