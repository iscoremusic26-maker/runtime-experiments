# Light Fades Twice CP06 FIX01 — 0.11.12 PRIVATE TEST

ID `dev.posture.post05_selective_reactions` · **0.11.12** · Windows x64 / DX12 · base compilada 0.11.11 `0ef0ad2824832c9e03d899c298b5f9a8e860d590`.
Datos de artefacto, commits y CI: sección 8 (se completan con la ejecución real del CI).

Estado: los dos defectos tienen **causa identificada en código nativo y en los logs**, corrección implementada en el propio `.dusk` y verificación de laboratorio/CI. **Todo lo jugable y visual sigue HUMAN_RUNTIME_PENDING**: no se ejecutó el juego ni la DLL.

## 1. Diagnóstico de los logs reales (0.11.11, 7-nov, dos sesiones)

Métricas despersonalizadas en `EVIDENCE/HUMAN_LOG_EVIDENCE_0_11_11.json` (sin rutas, cuentas ni líneas crudas).

| Señal | S1 | S2 | Lectura |
|---|---|---|---|
| Golpes Black furia ×2 (Expansion) | 69 | 59 | |
| …terminados sin ningún contacto nativo | 27 | 4 | |
| …de ellos con Link a < 160 u (pies) durante los ticks armados | 16 | 4 | mínimo 47 u |
| …con daño directo del mismo Black ≤ 40 ticks antes (i-frames) | 8 | 2 | exclusión legítima (E) |
| …cercanos (< 160 u) **sin** daño reciente | 13 | 2 | sospechosos P0-A |
| Black normal ×1.15 sin contacto, distancia mínima | ≥ 233 u (14/14) | 61 u (1 de 2) | fallos legítimos por alcance |
| Combos CP05 (1.05–1.35) sin contacto a < 160 u (distancia al final del golpe) | 0/12 | 1/4 (155 u) | sin evidencia clara de fallo |
| Red especial ×2 (RANDOM): golpes / ticks en que el sweep de Expansion escribió | 11 / 2 | 9 / 2 | el sweep casi nunca actúa |
| Red ×2 sin contacto: ticks de sweep por golpe | 1 | 1 | solo el último tick |
| Chips de furia aplicados por Expansion / neutralizados por CP06 | 48 / 49 | 45 / 33 | casi todo el rojo de S1 venía de parries ya compensados |

`CP05_MISS` y `fury_unverified_atp6_refused` no se usan como prueba de fantasma (contadores de condición, no de golpes). Los avisos `CalcDivideInfo xDiv var1=32` son un clamp del host (benigno en Dusklight, sin pérdida de colisión).

## 2. Causa de P0-A (golpes visualmente conectados sin resultado)

Código nativo leído (Dusklight `40457c6`):

* `daE_OC_c::action` apaga las esferas AT; `executeAttack` las arma si el frame **previo** a `play` está en 14..22; `cc_set` las coloca en la pose **posterior** (`d_a_e_oc.cpp:1452, 2415, 2551`). A ×1 se registran las poses 15..23 (una por frame).
* A ritmo r > 1 un tick cubre (p, p+r]: **las poses intermedias nunca se registran**, pero la interpolación de presentación de Dusklight (`frameInterp`) sí las dibuja. A ×2 solo se registran las poses pares; la estocada B además avanza el cuerpo hasta ~48 u por tick (`oc_attackb_trans`).
* El sweep ×2 de Expansion (`red_ai::sweep`, reutilizado por Black) intenta cubrir la pose saltada por **interpolación**, pero se niega con trayectorias curvas (`POSE_JUMP_TOO_LARGE`/`INTERPOLATION_ERROR_BOUND_TOO_LARGE`) y elige candidatas según un modelo de Link (un cilindro R35/H180 en `current.pos`) distinto de los tres cilindros reales de `setCollisionPos`; puede incluso **desplazar** la esfera nativa que sí tocaba. Los logs confirman que en golpes ×2 sin contacto el sweep solo actuó en el último tick.
* Además, a 1.05–1.35 el AT nativo se apaga cuando el frame previo supera 22, así que la cola de la ventana vanilla (≈22,5–23) puede no armarse nunca, y en el primer tick armado las poses 15..pre pueden quedar en un tick sin armar.
* Exclusiones legítimas confirmadas en código: `mDamageTimer` (30 ticks, `mInvincibleTime`) apaga los Tg de Link (`setCollision`), y `OnTgNoConHit` suprime cruces consecutivos del mismo atacante (`dCcS::ChkAtTgHitAfterCross`). No se tocan.

## 3. Corrección P0-A: cobertura con poses nativas exactas

En el POST de `daE_OC_c::execute` con prioridad −300 (después de Expansion y de CP06), por cada tick armado de un espadazo B/C de un Bokoblin rastreado:

1. Se lee la verdad del motor: esferas registradas (las de `cc_set` o las del sweep de Expansion) y los **tres cilindros Tg reales** de la Link viva, con su bit `TgSet` (i-frames). Solo se actúa si `setCollision` de Link ya corrió en este tick (Link registrada para esta pasada).
2. Si alguna esfera registrada ya cruza un cilindro activo con margen 0,5 u (predicado `cM3d_Cross_CylSph` transcrito), no se hace nada: decide el motor.
3. Candidatas, siempre poses **nativas exactas**:
   * la pose actual de `cc_set` (por si un sweep ajeno la desplazó);
   * las poses vanilla que este ritmo se salta, evaluadas con el **propio cálculo del motor** (`mDoExt_McaMorfSO::modelCalc`): `pre+1` en todo tick rápido (a ×2 es exactamente la pose impar), el inicio de ventana 15 en el primer tick armado y el final 23 en el último. Garantía comprobada en float32: **toda pose de la ventana vanilla 15..23 queda a ≤ 0,5 frames de una pose cubierta** (nunca más grueso que vanilla ×1) para todas las tasas 1.05–2.0 y fases.
   * La raíz de cada pose evaluada es la de vanilla: `lunge(m−1)−lunge(pre)` a lo largo de `shape_angle.y` (la misma fórmula de `executeAttack`; 0 para `pre+1`, para 23 y para el clip C).
4. Si una candidata cruza un cilindro **activo** con margen ≥ 0,5 u, se coloca **esa** esfera nativa (radio nativo 45/30) en su ranura solo para esta pasada (`cc_set` la reescribe en el siguiente execute). El motor resuelve guardia, parry, daño, i-frames, no-continuous-hit, chispa y sonido.
5. Sonda de pose: instantánea de todas las matrices de articulación, frame vanilla → `modelCalc`, frame exacto de vuelta → `modelCalc`, y verificación igualdad de **todas** las matrices y del frame; si algo difiere, la cobertura se desactiva para la sesión y se registra `CP06F1_CRITICAL`. El campo de frame se escribe directamente (como el `setFrame` de consola) para no resetear la interpolación de materiales de Dusk. Morph activo ⇒ no se sondea.

No se cambian ritmos, probabilidades, daño, radios, alcance, ventanas de parry, i-frames ni la IA. Nunca se arma un AT que el motor no armó, nunca se escribe vida, `AtShieldHit`, postura ni estado de Link.

## 4. Causa de P0-B (rojo tras parry perfecto en furia)

`cp19f2_chip_post()` de Expansion carga −1 de vida pendiente y llama a `flash_start` sobre **un único flash global** que dibuja en `daAlink_c::modelDraw` PRE/POST (prioridad 0) con `tevStr.TevKColor` = max(nativo, rojo del calendario), y restaura en su POST. CP06 devolvía la unidad, pero el flash ya estaba reiniciado. No se lee ni escribe memoria de Expansion.

## 5. Corrección P0-B: contrafactual causal y exacto

* Espejo del calendario documentado de Expansion (`flash_start` dmg=30/col=18, avance por `mod_update`, colores 15/10/5·|sin|, merge por máximo), verificado **diferencialmente contra su `cp19f2_policy.hpp` real**. Dos sombras: **E** (lo que Expansion muestra: todo chip) y **L** (contrafactual: solo chips legítimos).
* Atribución: POST(+91) y POST(−251) del mismo `execute` comparan la vida pendiente y el contador de neutralizaciones de CP06: −1 sin neutralizar ⇒ chip legítimo (E y L); 0 con una neutralización de CP06 ⇒ reinicio por parry (solo E); cualquier otro cambio ⇒ incierto (no se actúa hasta que expiren ambas).
* Dibujo de Link (cuerpo/cara/sombrero/manos, mismo ámbito que Expansion): PRE(+90) captura el valor previo; PRE(−250), ya tras el PRE de Expansion, **solo si el registro contiene exactamente la escritura esperada de Expansion** lo sustituye por max(previo, L). POST(−250) solo restaura si el valor sigue siendo exactamente el nuestro. Un valor ajeno, un desfase de calendario o un modelo fuera de ámbito nunca se tocan (fallo seguro: se ve el rojo de Expansion como en 0.11.11).
* Resultado: parry perfecto ⇒ ningún rojo atribuible a ese chip; guardia normal ⇒ chip y rojo intactos; daño real ⇒ rojo nativo intacto (nunca se baja un canal); parry tras guardia ⇒ continúa el rojo legítimo restante; no hay ventana de supresión de 30 ticks.

## 6. Telemetría nueva (acotada)

* `CP06F1_SWING` por golpe (anomalías siempre, furia ×2 y Red ×2 siempre, muestra inicial): actor, generación, golpe, tipo (`BLUE/RED/BLACK/BLACK_FURY_X2/RED_SPECIAL_X2`), clip, tasa, ticks, resultado (`VALID_HIT_BODY`, `VALID_SHIELD_BLOCK`, `VALID_PARRY`, `LEGITIMATE_MISS`, `LEGITIMATE_INVULNERABILITY`, `NATIVE_NO_CONTINUOUS_HIT`, `NATIVE_BLOCKED_OTHER`, `CONTACT_LOST_CONFIRMED`, `GEOMETRY_UNDETERMINED`, `CLEANUP_STALE`), ticks esperados/perdidos/backfill, proc y timer de Link. El `tick` coincide con el de POST08/CP05.
* `CP06F1_BACKFILL` por esfera escrita (poses, centros, distancia, origen nativo/ajeno). `CP06F1_FLASH` por reinicio. `CP06F1_SUMMARY` periódico y al cerrar: histogramas por tipo×resultado, motivos, sondas, desajustes, líneas descartadas. Un contador a cero no es prueba visual.

## 7. Verificación

* `cp06f1_lab` (núcleo): predicado frente a la transcripción de `cM3d_Cross_CylSph` (2 M pares), cobertura vanilla por tasa/fase en float32, decisión, clasificación, `sincos16` en los 65 536 ángulos, espejo del flash diferencial contra la cabecera real de Expansion.
* `cp06f1_world_lab`: compila el **adaptador de producción** con stubs y lo ejecuta en un bucle con pipeline nativo transcrito (`executeAttack`/embestida/AT/`play`/`cc_set`, `ChkAtTg` con limpieza de registros, NoConHit de Link, escudo, `setCollision`/i-frames), el **sweep ×2 real** y el **flash real** de Expansion, y un despachador con el orden de prioridades del host. Modelado: cinemática de la espada (4 perfiles), colocación de cilindros de Link, reacción de Link y ángulo frontal del escudo.
  * 78 624 escenarios (B/C, 7 tasas, 4 perfiles, 12 distancias, 21 ángulos, 3 alturas, 3 orientaciones): 14 027 contactos vanilla robustos; **0.11.11: 90 fantasmas (60 a ×2); 0.11.12: 0**. 1 380 contactos nuevos, **todos** dentro del volumen vanilla; cada esfera escrita coincide con la registración vanilla de su pose (1 923 comprobaciones de centro, 283 con desplazamiento de raíz no nulo); paridad exacta con vanilla ×1 en fase par (164/164).
  * Guardia frontal ⇒ bloqueo; espalda ⇒ daño; i-frames ⇒ 0 contactos y 0 escrituras; parry solo con Shield Attack a tiempo (113/113), nunca tardío; nunca daño doble; dos Bokoblins simultáneos sin interferencia; Link no registrada ⇒ 0 escrituras; fallo de restauración inyectado ⇒ cobertura desactivada y línea crítica.
  * Flash: 10 secuencias × 2 órdenes de registro (parry, guardia, parry→guardia, guardia→parry, dos Blacks, ráfagas, daño real, pausa, normales): el color dibujado es exactamente el de Expansion sin los chips neutralizados; 0.11.11 reproduce el rojo indebido; escritor ajeno y tercero en el escudo intactos; POST de Expansion ausente ⇒ restauración propia exacta.
* 41/41 mutantes FIX01 eliminados (0 timeouts), 26 negativas de fuente FIX01, auditoría PE de los tres escritores con negativos de instrucción real; suite heredada completa (ver RESULTS.json).

## 8. Artefacto, commits y CI

* `.dusk`: `LIGHT_FADES_TWICE_CP06_FIX01_0_11_12_PRIVATE_TEST_windows-amd64_2a57ebeeafe6.dusk` · **188 838 bytes** · SHA-256 `82f678a8ffacf197d7828721513597fe1b4d3c6752ca07ce2d6a6c9c2797d2ed`; DLL 1 318 912 bytes, SHA-256 `691497410787b8d90093ac3d47c0adc1e5663c6f50db9202681f276c132ee7c9`; miembros `mod.json` + `lib/windows-amd64/mod.dll`.
* Fuente compilada `2a57ebeeafe6ec48ee5b63b5f614b6a0fff95b5e` (rama `feature/light-fades-twice-cp06-fix01-0-11-12`); CI `e87aa7e3476d484ff94eb350e7f7570e22ee8cf8` (rama `ci/light-fades-twice-cp06-fix01-0-11-12`); este documento va en un commit posterior y separado.
* CI [42482972682](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/42482972682): build SUCCESS, independent-download SUCCESS (`ARTIFACT_DOWNLOADED_VERIFIED`). Artefacto [13618428357](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/42482972682/artifacts/13618428357), caduca 2026-12-08. Descargado otra vez en esta sesión: SHA, ZIP/CRC, DLL x64, `mod.json` y manifiesto coinciden.
* Run previo 42482710995 falló solo en la auditoría de escritores: MSVC añade `__security_check_cookie` (/GS) en `sphere_place`; corregido admitiendo únicamente ese helper local.
* MSVC: 25 labs / 1 396 715 851 comprobaciones (los 23 heredados: 4 899 024, idéntico a 0.11.11), 620/620 mutantes (FIX01 41/41), 0 timeouts; PE_AUDIT_PASS (67 imports, 25 objetivos, HOOK_MEM_EXT 10); alcance de escritores MSVC: kcolor = 3 bytes en +0x550..552, pose_frame = 1 `movss` +0x2c + `modelCalc`, sphere_place = sin almacenes no‑pila, solo `SetC`/`SetR`/cookie; 0 usos de esos imports fuera de su escritor; 4 negativos con instrucciones reales rechazados.
* Rollback: 0.11.11 `7bcebf6f…5be3` · 0.11.10 `9c8f0074…bb4f`.

## 9. Límites honestos

* Las trayectorias reales de los clips B/C no están en el repositorio (activos comerciales): la cinemática del laboratorio es **modelada**. La garantía demostrada es algorítmica (cobertura ≤ 0,5 frames con poses exactas del motor y raíz vanilla); que desaparezcan todos los fantasmas visibles en el juego requiere prueba humana.
* La raíz vanilla incluye la embestida tabulada; las correcciones Co/empujes de ese tick son las del tick real (vanilla tendría las suyas). Un tercero que escribiera en el cuerpo de Link exactamente el valor esperado de Expansion entre nuestros dos PRE sería indistinguible (probabilidad práctica nula; documentado).
* Coste: ~55 ns por ejecución de Bokoblin en reposo, ~20 ns por draw de Link, y ~1,2 `modelCalc` extra por tick armado cerca de Link (solo con Link vulnerable). El FPS real queda HUMAN_RUNTIME_PENDING.
