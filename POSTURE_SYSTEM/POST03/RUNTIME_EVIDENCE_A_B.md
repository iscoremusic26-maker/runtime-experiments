# POST03 — Evidencia humana de las sesiones A/B (saneada)

**Procedencia: `USER_SUPPLIED_RAW_WINDOWS_LOG_ANALYZED`.** Los dos logs crudos los aportó el usuario y **Claude Code los leyó completos** en local (2026-11-01), comprobó sus SHA-256 y extrajo esta evidencia con un parser reproducible (`POSTURE_SYSTEM/POST03_1/tests/extract_runtime_evidence.py`, con pruebas en `test_extract_runtime_evidence.py`). **Este repositorio no contiene los logs** ni líneas completas de ellos; el usuario conserva los originales. Los resultados procesados están en `POSTURE_SYSTEM/POST03_1/evidence/` (`POST03_AB_EVENTS_SANITIZED.tsv`, `POST03_AB_SUMMARY_SANITIZED.json`). Los eventos son datos de la lista blanca del extractor; no hay rutas, nombres de cuenta ni direcciones de memoria.
Etiquetas: **[R]** observado por el usuario en juego y leído en el log · **[S]** fuente · **[C]** MSVC/CI · **[P]** pendiente.

## 1. Logs
| | Sesión A (sin mods de combate) | Sesión B (coexistencia 8/8) |
|---|---|---|
| Archivo | `dusklight-20261101-081057.log` | `dusklight-20261101-080341.log` |
| SHA-256 (calculado) | `e495427aaf3ba3f5ee4c6b8ab887f24a4df290faa43455903da16f8fcffb1bb5` | `92495e7359458c23c73eb2c5139c5b0f5b6bf46dfd50fb0359db85dfa8747a06` |
| Tamaño · líneas (`splitlines()`) | 325190 bytes · 4250 | 875205 bytes · 5396 |
| Coincide con lo declarado | sí (hash, tamaño y líneas, sin transformación) | sí |
| Host · backend | Dusklight 2.0.3, D3D12 | Dusklight 2.0.3, D3D12 |
| Mods activos | **2/2**: POST03 0.3.0 + Zora Swim 1.3.0 (no es «solo POST03») | **8/8**: POST03 0.3.0, Enemy Health Multiplier `2.0.3-cp11-arrow-route-test`, Enemy Health Bars `2.0.3-cp06-armos-test`, Enemy Variant Framework 0.15.0, Bokoblin Expansion 0.17.0, Zora Swim 1.3.0, Luau Support 1.0.0, Dusklight Randomizer 1.0.6 |
| Hook | `resolve=MOD_OK`, `same_address=1`, `inline_sites_flag=0`, PRE/POST instalados | igual |
| Cierre | `all mods unloaded`; `POST03_SHUTDOWN` | igual |
Código bajo prueba: `dev.posture.post03_hit_classification` v0.3.0, fuente compilada [`f350522fc2097cbbe786c57df2f005ba0b4981b3`](https://github.com/iscoremusic26-maker/Mods-Duskligh/tree/f350522fc2097cbbe786c57df2f005ba0b4981b3/POSTURE_SYSTEM/POST03), run de CI [41280823158](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41280823158), [artefacto original](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41280823158/artifacts/13073232413) `POSTURE_POST03_HIT_CLASSIFICATION_windows-amd64_f350522fc209.dusk` (19688 bytes, SHA-256 `59c8145e…c9f`; los artefactos de Actions caducan el 2026-12-01).

## 2. Contadores `SHUTDOWN` [R]
| | A | B |
|---|---|---|
| `calls` · `adm(cand/e_oc2/other/unsafe)` | 17233 · 8858/8375/0/0 | 47805 · 14624/27774/0/5407 |
| `records_created` · `max_active` · `active` | 19 · 9 · 2 | 21 · 10 · 4 |
| `death_seen` · `absent_verified` · `lookups` (`lookup_unavailable`) | 8 · 17 · 647 (0) | 12 · 17 · 1586 (0) |
| `admission_changes` · `identity_conflicts` · `capacity_drops/evictions` | 0 · 0 · 0/0 | 42 · 0 · 0/0 |
| `unmatched_post` · `discarded` · `frame_overflow` · `post_generation_mismatch` · `pending` | 0 · 0 · 0 · 0 · 0 | 0 · 0 · 0 · 0 · 0 |
| `anomalies` · log `dropped` · `log_errors` | 0 · 0 · 0 | 0 · 0 · 0 |
| `cand_started` = `raw_tg` · `dual_tg` · `pair_distinct` | 6 · 1 · 1 | 18 · 11 · 1 |
| `confirmed` · `processed_mismatch` · `not_processed` | 6 · 0 · 0 | 18 · 0 · 0 |
| `finish_started` = `finish` | 0 | 2 |
| `cooldown_blocked` (`cooldown_with_tg`) · `no_tg` | 54 (0) · 8798 | 168 (0) · 14436 |
| `excluded` · `unknown_unsafe` (llamadas) | 8375 · 0 | 27774 · 5407 |
| `classification_unavailable` = `collider_unmatched` | 6 | 14 |
| `family(sword/…/ambiguous/unavail)` | 0/0/0/0/0/0/0/0/0/0/**6** | **4**/0/0/0/0/0/0/0/0/0/**14** |
| `events_emitted` · `duplicates_suppressed` · `cross_generation_drops` | 6 · 0 · 0 | 20 · 0 · 0 |
| `POST03_CONSERVATION` | `ok=1`, started=6 judged=6 pending=0 | `ok=1`, started=20 judged=20 pending=0 |
Recomputado desde los bytes: coincide con el resumen recibido en todos los campos; no hubo discrepancias.

## 3. Los 26 eventos `POST03_HIT_EVENT` (orden cronológico dentro de cada sesión) [R]
`Link pid` = id de proceso de la última creación de `daAlink_c` (Link) anterior al evento. `colisión`: `IMPLAUSIBLE` = `SELECTED_COLLIDER_IMPLAUSIBLE`. `tg` = esferas con bit TG; `dual/dist` = dos esferas / colliders distintos. `HP`, modo y `cd` son «antes>después». Los campos `hp` son el HP nativo visible en el POST (con HM x2 los valores son los de HM).

| S | # | call | id | gen | Link pid | kind | tg | dual/dist | src | colisión | familia | at | HP | modo | old | cd | elig. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A | 1 | 6625 | 490 | 16 | 434 | CONFIRMED | cc1 | 0/0 | none | IMPLAUSIBLE | UNAVAILABLE | UNAVAILABLE | 40>0 | 7>6 | 7 | 0>10 | CONF |
| A | 2 | 15296 | 491 | 17 | 434 | CONFIRMED | cc0 | 0/0 | none | IMPLAUSIBLE | UNAVAILABLE | UNAVAILABLE | 40>20 | 3>5 | 3 | 0>10 | CONF |
| A | 3 | 15460 | 491 | 17 | 434 | CONFIRMED | cc1 | 0/0 | none | IMPLAUSIBLE | UNAVAILABLE | UNAVAILABLE | 20>0 | 3>6 | 3 | 0>10 | CONF |
| A | 4 | 16637 | 549 | 11 | 434 | CONFIRMED | cc0 | 0/0 | none | IMPLAUSIBLE | UNAVAILABLE | UNAVAILABLE | 40>20 | 3>5 | 3 | 0>10 | CONF |
| A | 5 | 16825 | 549 | 11 | 434 | CONFIRMED | cc1 | 0/0 | none | IMPLAUSIBLE | UNAVAILABLE | UNAVAILABLE | 20>0 | 3>6 | 3 | 0>10 | CONF |
| A | 6 | 16834 | 550 | 12 | 434 | CONFIRMED | cc0+cc1 | 1/1 | none | IMPLAUSIBLE | UNAVAILABLE | UNAVAILABLE | 40>0 | 4>6 | 4 | 0>10 | CONF |
| B | 1 | 8068 | 161 | 8 | 105 | CONFIRMED | cc1 | 0/0 | none | IMPLAUSIBLE | UNAVAILABLE | UNAVAILABLE | 19>9 | 3>5 | 3 | 0>10 | CONF |
| B | 2 | 8293 | 161 | 8 | 105 | CONFIRMED | cc1 | 0/0 | none | IMPLAUSIBLE | UNAVAILABLE | UNAVAILABLE | 11>1 | 5>6 | 5 | 0>10 | CONF |
| B | 3 | 11533 | 161 | 8 | 105 | CONFIRMED | cc0+cc1 | 1/0 | none | IMPLAUSIBLE | UNAVAILABLE | UNAVAILABLE | 25>5 | 3>5 | 3 | 0>10 | CONF |
| B | 4 | 11641 | 161 | 8 | 105 | CONFIRMED | cc0+cc1 | 1/0 | none | IMPLAUSIBLE | UNAVAILABLE | UNAVAILABLE | 6>0 | 5>6 | 5 | 0>10 | CONF |
| B | 5 | 17576 | 221 | 3 | 105 | CONFIRMED | cc1 | 0/0 | none | IMPLAUSIBLE | UNAVAILABLE | UNAVAILABLE | 220>200 | 7>5 | 7 | 0>10 | CONF |
| B | 6 | 17720 | 221 | 3 | 105 | CONFIRMED | cc0+cc1 | 1/0 | none | IMPLAUSIBLE | UNAVAILABLE | UNAVAILABLE | 201>181 | 5>5 | 5 | 0>10 | CONF |
| B | 7 | 17808 | 221 | 3 | 105 | CONFIRMED | cc0+cc1 | 1/0 | none | IMPLAUSIBLE | UNAVAILABLE | UNAVAILABLE | 181>161 | 5>5 | 5 | 0>10 | CONF |
| B | 8 | 17912 | 221 | 3 | 105 | CONFIRMED | cc0+cc1 | 1/0 | none | IMPLAUSIBLE | UNAVAILABLE | UNAVAILABLE | 162>142 | 5>5 | 5 | 0>10 | CONF |
| B | 9 | 18080 | 221 | 3 | 105 | CONFIRMED | cc0+cc1 | 1/0 | none | IMPLAUSIBLE | UNAVAILABLE | UNAVAILABLE | 144>114 | 5>6 | 5 | 0>10 | CONF |
| B | 10 | 19176 | 221 | 3 | 105 | CONFIRMED | cc0+cc1 | 1/0 | none | IMPLAUSIBLE | UNAVAILABLE | UNAVAILABLE | 123>103 | 3>5 | 3 | 0>10 | CONF |
| B | 11 | 19544 | 221 | 3 | 105 | CONFIRMED | cc0 | 0/0 | none | IMPLAUSIBLE | UNAVAILABLE | UNAVAILABLE | 106>76 | 7>6 | 7 | 0>10 | CONF |
| B | 12 | 20607 | 222 | 4 | 105 | CONFIRMED | cc1 | 0/0 | none | IMPLAUSIBLE | UNAVAILABLE | UNAVAILABLE | 147>147 | 4>5 | 4 | 0>10 | CONF |
| B | 13 | 20831 | 222 | 4 | 105 | CONFIRMED | cc0 | 0/0 | none | IMPLAUSIBLE | UNAVAILABLE | UNAVAILABLE | 150>120 | 5>6 | 5 | 0>10 | CONF |
| B | 14 | 21426 | 222 | 4 | 105 | FINISH | none | 0/0 | none | NO_SELECTED | UNAVAILABLE | UNAVAILABLE | 55>0 | 6>9 | 6 | 0>0 | NO |
| B | 15 | 25374 | 162 | 9 | 105 | CONFIRMED | cc0+cc1 | 1/0 | none | IMPLAUSIBLE | UNAVAILABLE | UNAVAILABLE | 220>0 | 4>6 | 4 | 0>10 | CONF |
| B | 16 | 29300 | 562 | 19 | 506 | CONFIRMED | cc1 | 0/0 | cc1 | MATCHES_CC1 | SWORD | 0x04000002 | 220>200 | 3>5 | 3 | 0>10 | CONF |
| B | 17 | 29440 | 562 | 19 | 506 | CONFIRMED | cc0+cc1 | 1/1 | cc1 | MATCHES_CC1 | SWORD | 0x04000002 | 200>180 | 5>5 | 5 | 0>10 | CONF |
| B | 18 | 29550 | 562 | 19 | 506 | CONFIRMED | cc0+cc1 | 1/0 | cc1 | MATCHES_CC1 | SWORD | 0x04000002 | 181>161 | 5>5 | 5 | 0>10 | CONF |
| B | 19 | 29760 | 562 | 19 | 506 | CONFIRMED | cc0+cc1 | 1/0 | cc1 | MATCHES_CC1 | SWORD | 0x04000002 | 163>133 | 5>6 | 5 | 0>10 | CONF |
| B | 20 | 30420 | 562 | 19 | 506 | FINISH | none | 0/0 | none | NO_SELECTED | UNAVAILABLE | UNAVAILABLE | 137>0 | 6>9 | 6 | 0>0 | NO |

## 4. Separaciones que esta evidencia exige
- **`HIT_CONFIRMED` ≠ HP restado.** Significa «cooldown 0→≠0 y reacción nativa comprometida» (P1+P2, `POST03/HIT_PATH_AUDIT.md`). En estos 24 eventos el HP bajó en todos salvo el id 222 (evento B-12: `147>147`, modo `4>5`): un golpe procesado con `hp_delta=0` es compatible con el contrato.
- **Finish ≠ golpe.** Los 2 `FINISH_NATIVE_OBSERVED` (B-14 id 222: HP `55>0`; B-20 id 562: HP `137>0`; ambos `cutdown=1`, modo `6>9`) son rutas nativas observadas, **no inducidas** por POST03, y no entran en el denominador de clasificación (24 golpes).
- **Doble esfera ≠ dos golpes.** 1 evento `cc0+cc1` en A y 11 en B; en cada caso hay un único `HIT_EVENT` (`duplicates_suppressed=0`, conservación exacta). Solo 1 evento de B (B-17) y 1 de A (A-6) tenían colliders distintos (`distinct=1`).
- **Admisión ≠ origen.** B tiene 42 cambios de admisión (`E_OC_CANDIDATE → UNKNOWN_UNSAFE → E_OC_CANDIDATE`) con `identity=KEPT` y sin nueva generación; los Blue de DEVF/Expansion siguen con `origin=UNDETERMINED`.

## 5. El síntoma: `SELECTED_COLLIDER_IMPLAUSIBLE` en 20 de 24 golpes confirmados [R]
| | A | B | Total |
|---|---|---|---|
| golpes `HIT_CONFIRMED` | 6 | 18 | 24 |
| `family=UNAVAILABLE` (`SELECTED_COLLIDER_IMPLAUSIBLE`, `collider_src=none`, `at=UNAVAILABLE`) | 6 | 14 | **20 (83,33 %)** |
| `family=SWORD` (`MATCHES_CC1`, `at=0x04000002`) | 0 | 4 | **4 (16,67 %)** |
- **No requiere HM/Bars/DEVF:** aparece 6/6 en A (solo POST03 + Zora Swim). No hay base para atribuirlo a esos mods.
- **Los 4 `SWORD` son todos del actor id=562 (generación 19)**, un Blue de Expansion en `F_SP121` sala 3 capa 6 (según la propia línea de DEVF); `cc1` seleccionó el collider, 1 de los 4 con `cc1` solo y 3 con `cc0+cc1`.
- **Hallazgo clave (correlación por instancia de Link):** el resultado es **constante por instancia de Link** (`daAlink_c` se recrea en cada carga de stage; `fpcBs_Create … fpcNm_ALINK_e`):
  | sesión | creaciones de Link (pid) | eventos por instancia de Link |
  |---|---|---|
  | A | 17, 105, 265, **434** | pid 434: 6/6 confirmados, 6 `UNAVAILABLE`, 0 `SWORD` |
  | B | 17, 105, 335, **506** (+ las anteriores sin golpes) | pid 105: 14/14 `UNAVAILABLE` · pid 506: 4/4 `SWORD` |
  Ningún evento de una misma instancia de Link difiere de los demás. Esto es **consistente con** que el fallo dependa de una propiedad fija del objeto Link recién asignado (por ejemplo la alineación de su dirección en el heap del anfitrión), y **no** del arma, la esfera, el actor golpeado ni los otros mods; **no lo demuestra** (el log no contiene el residuo del puntero). Es la hipótesis prioritaria de POST03.1 (`POST03_1/COLLIDER_ROOT_CAUSE_AUDIT.md`).
- Limitación de POST03 v0.3.0: el collider seleccionado se rechazaba **antes** de compararlo con los hit obj crudos, y no registraba clases de puntero; por eso este log no dice si coincidían ni qué residuo tenían.

## 6. Incidencias no atribuidas (criterios exactos de conteo)
| Criterio | A | B |
|---|---|---|
| líneas `[WARNING \| dusk] CalcDivideInfo…` | 501 | 355 |
| líneas `[WARNING \| aurora::texture] texture_replacement:…` | 109 | 115 |
| líneas con `event=PERF_WINDOW` (todas con `MEASUREMENT_NOT_AN_ERROR`, nivel de log ERROR) | 0 | 27 |
Son diagnósticos del motor o mediciones de Expansion que ya ocurrían sin POST03 en sesiones anteriores. **No se atribuyen a POST03 ni se descarta definitivamente su efecto.** No hubo crash, `POST03_DISABLED`, `POST03_HOOK_FAILED` ni `was inlined into callers`.

## 7. Contexto de otros mods en B (no correlacionable 1:1 con POST03)
- **HM:** `cc_at_check pre=73 post=73 paired=73`, `events=73 valid=73`, `HP relation: match=73 diff=0`, `identityMismatch=0`, `threadMismatch=0`. HM cubre otros perfiles y rutas (perfiles 510 y 496; su propio resumen separa SWORD, ARROW, STUN, BOMB, HOOKSHOT…), por eso 73 ≠ 18+2.
- **Bars:** `queries=145165 ok=81381 unavailable=2 invalid=0 rejected=0`; `barsDrawn=11968`, `packetDraws=8789`. Los 2 `unavailable` tienen fallback nativo; no prueban un fallo de POST03.
- HM lee `info->mpCollider->GetAtType()` en su hook de `cc_at_check` sin ninguna guarda de alineación a 8 (`hm_203/core8/src/game_read.cpp:153` y `:173`) y clasificó SWORD de forma consistente en esta misma sesión: otro indicio de que los colliders eran objetos válidos.

## 8. Dictamen
- **Observación, identidad, ciclo de vida y deduplicación: `SCOPED_RUNTIME_PASS`** en estas dos configuraciones: 26 eventos, `ok=1` en la conservación, 0 duplicados, 0 desajustes de generación, 0 anomalías, cierres limpios, hook sin inline.
- **Clasificación de familia: parcial.** `CLASSIFICATION_RUNTIME_PARTIAL` (4/24). **No** es `CLASSIFICATION_RUNTIME_PASS` ni POST03 «completo».
- `POST03_1_FIX_PENDING`: la corrección (POST03.1) está pendiente de log real.
- `CLASSIFICATION_COVERAGE` sigue siendo «solo laboratorio» para las familias distintas de SWORD; no hay ningún evento de flecha, bomba, bumerán, tirachinas, escudo ni bola de hierro en estas sesiones.
- G2 y G3: `NOT_STARTED`. No es `UNIVERSAL_COMPATIBILITY_PASS`.

## 9. Riesgos abiertos
Origen de Blue (D1) indeterminable; subtipo de espada, atacante y potencia no disponibles desde un único hook; coste del hook no medido; `CalcDivideInfo`/texturas/`PERF_WINDOW` no atribuidos; el residuo real del puntero rechazado sigue siendo desconocido.

## 10. Qué debe comprobar POST03.1 (hipótesis exactas)
1. Que los `mAtInfo.mpCollider` rechazados sean **iguales** al hit obj crudo de `cc0`/`cc1` y tengan residuo `mod8=4` (4 bytes de alineación del heap del anfitrión, `JKRExpHeap`), no `null`, `too_low` ni `mod4_bad`.
2. Que con la lectura permitida a partir de 4 bytes alineados aparezcan familias `SWORD` repetibles en varias instancias de Link, sin crash y sin eventos duplicados.
3. Que los contadores `reason/sel_class/raw_class` de `POST03_1_COLLIDER_DIAG` expliquen el 100 % de los `HIT_CONFIRMED`.
Si la hipótesis falla, los diagnósticos indicarán cuál es la clase real y la clasificación seguirá `UNAVAILABLE` (fail-closed).
