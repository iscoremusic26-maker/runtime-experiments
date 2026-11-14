# LIGHT FADES TWICE 0.13.10 — DARKNUT MINIBOSS DKN01 FIX01

Estado: **HUMAN_RUNTIME_PENDING**. Compila (MSVC en CI, clang-cl local), pasa laboratorios, mutantes y auditorías; **nadie lo ha jugado todavía**. Nada de este documento afirma que funcione en el juego.

## Base, ramas y derivación
- Base funcional: **0.13.9 DKN01**, `runtime-experiments` commit compilado **2bbc7c8** (FULL 43627586151, `.dusk` `bc9b0b07…c601`). La rama nueva parte de **3aa505d** = 2bbc7c8 + solo documentación (`IMPLEMENTATION.md`, registro CI de 0.13.9; 11 líneas), así que esa documentación posterior queda incluida sin cambios.
- Fuente: rama nueva `feature/light-fades-twice-darknut-miniboss-fix01-0-13-10`, worktree `runtime-experiments-dkn-fix01`.
- CI: rama nueva `ci/light-fades-twice-darknut-miniboss-fix01-0-13-10` en `windows-build-lab` (desde ab4dd84), worktree `windows-build-lab-dkn-fix01`.
- Mismo ID de mod, versión **0.13.10**. Un solo `.dusk`: `mod.json`, `lib/windows-amd64/mod.dll`, `res/darknut/resurrection_A_agil_natural_FIX02.bck` (FIX02 sin cambios: 45 024 B, `f96356fb…1524`).
- `mod.cpp` **no cambia** (sin hooks nuevos: las dos callbacks nuevas van sobre objetivos ya existentes). **0 imports nuevos del juego** (comprobado con el DLL local frente a `ci/expected_pe.json`).

## Diagnóstico del log humano `dusklight-20261114-140344.log` (0.13.9)
- 574 ganancias de postura `LINK_BLOCKED` frente a 11 golpes efectivos y 36 parries: la fase 2 se pasó casi entera en `ACT_GUARDL` (modos 0 y 11).
- Entre los ticks 14 147 y 23 438 no hubo **ninguna** decisión de ataque: `checkNormalAttackAble()` nativo rechaza todo inicio mientras `getCutCount() != 0` (Link presionando), y la selección de 0.13.9 dependía de ese inicio nativo (40 %).
- Shield Attack: `damage_check` fase 2 → `setActionMode(ACT_GUARDL, 0)` siempre, sin comprobar el frente; 0.13.9 además contaba ese cambio como "bloqueo" (+3), de ahí el bucle espadazo → Shield Attack → espadazo.
- Patada tras `RECOVERED` (tick 27 891, 71 ticks después): la detección de pasividad seguía contando durante la guardia forzada; además `executeGuardL` modo 3 y `checkNextMove` (<200) arrancan la patada por su cuenta.
- El error de cierre final del log se ignora (memoria del PC del usuario, sin evidencia contra el mod).

## Arquitectura: un único dueño por instancia
Prioridades (aplicadas en este orden en `action` PRE / `setDamage` POST):
1. Borrado / descarga / mundo no seguro (`dknb_world_safe`), sin objetivo.
2. Transformación nativa F1 (HP1 = 0) y derrota real F2/F3 (acumulador ≥ 480).
3. Recibos de ejecución / Finish (DKR01 los posee desde la caída).
4. Ruptura de postura (cancela toda ofensiva y la defensa).
5. Caída por ejecución, suelo, levantamiento (DKR01).
6. Defensa adaptativa y contraataque tras parry real (F2/F3).
7. Ofensiva propia (combo / golpe aislado / especial de pasividad).
8. Reposicionamiento nativo (perseguir, rodear, saltos de esquiva) — se conserva.

Estados: `F1_ARMOR / F1_TRANSFORM / F2_SWORD / DKR01_OWNED / F3_SWORD_REVIVED / DEAD` × ruptura `COMBAT / BREAK_PENDING / STAGGER_A / STAGGER_B_HELM_READY / RECOVERY / EXECUTION` × arriendo `NONE / COMBO / SINGLE / COUNTER / SPECIAL`; DKR01: `ARMED / FALLING / DOWN / FINISH_COMMITTED / FINISH_HIT / RISING / GETTING_UP / FINAL_DEATH / CONSUMED`. Ranura por id de proceso + generación; vigilantes: combo 600, recuperación 60, levantamiento 120, Finish 600.

## 1. Autoridad ofensiva propia (las 3 fases)
- Todo `setActionMode(ATTACK*, modo de entrada)` que escribe la IA nativa (checkNextMove, checkStartAttackH, aterrizajes de salto, GuardL 3, fin de patada/escudo) se **devuelve a la persecución neutral antes de ejecutarse** (`dkn_native_neutral`: `ACT_CHASEL 1` / `ACT_CHASEH 0`) en el PRE de `action`: `NATIVE_CHAIN_SUPPRESSED`. La cadena B→A nativa es imposible en movimientos propios (`mActionMode2Copy = 1`, también en la cola).
- El controlador decide en cada tick neutral (y en cada intento nativo suprimido): rechazo por `BUSY / UNSAFE / NO_LINK / NOT_NEUTRAL / REENTRY / FAR / NOT_FRONT / GAP` (contados), o elección: **golpe aislado 25 %** [PROVISIONAL] (F1 A/B por distancia como el nativo; F2/F3 estocada/doble 50/50) o **combo 25/25/25/25** (equidad condicional). Ya no existe el 40 % ni el enfriamiento de 120 ticks.
- Cadencia [PROVISIONAL]: tras cada ofensiva, espera aleatoria 36–66 ticks (F1) / 22–46 (F2/F3); 45 ticks de re-entrada tras recuperación, levantamiento, resurrección o transformación (sin ataque ni patada).
- La guardia nativa puede dejarse para atacar tras 8 ticks (no durante una ventana de parry armada): el Darknut recupera la iniciativa aunque Link presione.
- Laboratorio: con la espera cumplida decide el 100 % de los puntos libres; máximo 106 ticks entre ofensivas en la simulación (movimiento 60 + espera).

## 2. Los ocho combos
- F2/F3: sin cambios de 0.13.9 (ritmos rápidos, B dividida en dos ventanas, B1 corta en el fotograma 20). Error simulado ≤ 0,90 ticks por par.
- **F1 pesada** (instrucción del usuario: más lento respetando la separación entre ataques). Medido sobre el rig real (`tests/data/dkn_f1_transition.py`): los cortes de 0.13.9 (fotogramas 28–40) dejaban **126–141 unidades** de salto medio de pose fundidas en 4 fotogramas = la maza se "teletransportaba". FIX01:
  - una **escala temporal uniforme S por combo**: cada separación = separación del audio × S (las proporciones del ritmo son exactamente las de la grabación);
  - impulso, recorrido y contacto de cada mazazo a **velocidad nativa 1.0**; solo la recuperación del golpe anterior se acompasa (0,70–1,50);
  - corte/inicio elegidos con salto de pose ≤ 90 (la mayoría ≤ 30), fundido de 10 fotogramas (salto > 60) o 6.
  - Resultado (`tests/data/dkn_f1_heavy.json`):

| Combo | S | Duración audio → nueva | Separación mínima |
|---|---|---|---|
| F1-C1 B A B A B | 2,59 | 2,52 s → 6,53 s | 0,37 s → 0,96 s |
| F1-C2 B B B | 1,44 | 2,31 s → 3,33 s | 0,71 s → 1,02 s |
| F1-C3 A B B B A | 2,56 | 3,54 s → 9,05 s | 0,47 s → 1,20 s |
| F1-C4 A B B A B | 1,45 | 4,12 s → 5,97 s | 0,71 s → 1,02 s |

  Plan original vs nuevo por impacto: `tests/dkn_lab.cpp` imprime la matriz (corte, inicio, tasas) y comprueba que ningún par F1 baja de 27 ticks y que cada par = audio × S (error simulado ≤ 0,90 ticks). **Naturalidad visual: pendiente de juicio humano.**

## 3. Shield Attack (bug del bucle)
- `damage_check` PRE identifica por **identidad de puntero** qué colisionador de Link tocó cada esfera de daño (`mSphA[3]`, `mSphB[3]`, `mSphC`): `mGuardAtCps` = Shield Attack, `mAtCps[0..2]` = espada.
- POST: fuera de la única ruta legítima, la guardia que fuerza (`ACT_GUARDL/GUARDH`) **se deshace** al estado previo: combo, golpe, guardia, recuperación o tambaleo siguen igual (`SHIELD_ATTACK_REJECTED`, con veredicto y arriendo). El sonido/chispa nativos se conservan. **0 postura** por Shield Attack; el +3/+2 de bloqueo solo cuenta espadas (una vez por acción de Link).
- El HeadLock nativo de F1 (GUARDH tras Shield Attack → Helm Splitter nativo) se apaga en cada `action` POST: no hay ejecutor en F1.
- Ruta legítima: Shield Attack **nuevo** (Link entró en `PROC_GUARD_ATTACK` después del inicio de la ruptura, serial no usado) durante el **primer** tambaleo de F2/F3 → `HELM_PREP`.

## 4. Defensa adaptativa F2/F3
- Presión = contactos de espada de Link (bloqueados o con daño) en los últimos 90 ticks.
- Cuando Link inicia un tajo nuevo de frente y a < 300, con el Darknut libre: guardia nativa `ACT_GUARDL 0` (TNB_GUARD_A/B por tipo de corte) con 20 % + 15 %/contacto (máx. 75 %) [PROVISIONAL]; de esas guardias, 15 % + 10 %/contacto (máx. 50 %) arman una **ventana de parry** de 20 ticks tras 3 de preparación, con enfriamiento 150 [PROVISIONAL].
- Ventana armada = `mTimer10` mantenido mientras Link está de frente → `setBodyShield` pone TgShield en `mSphA` → la espada de Link **rebota por su ruta nativa** (`checkCutReverseAt` TRUE → `procCutReverseInit`). Callback POST de `checkCutReverseAt` (después de Lizalfos y Chilfos): en las esferas de este Darknut, TRUE se conserva **solo** con ventana armada (`ENEMY_PARRY_REAL` + `SWORD_REBOUND`); cualquier otro TRUE → FALSE (bloqueo ordinario sin rebote).
- Contraataque: **uno**, solo si Link está realmente en `PROC_CUT_REVERSE` dentro de 8 ticks; estocada o doble 50/50 (aprobado); ambos con ventanas de parry para Link. Luego vuelve el controlador.
- Suspendida durante ruptura, tambaleos, ejecución, caída, Finish, levantamiento, transformación y resurrección.

## 5. Pasividad
Igual que 0.13.9 (38 ticks escudo real / 75 sin escudo, 220/230, enfriamiento 240 [PROVISIONAL]), pero solo desde estado neutral, nunca durante la re-entrada, y los contadores se congelan fuera de neutral. La patada/escudo nativos automáticos (<200, rodar, GuardL 3, fin de clip) quedan suprimidos.

## 6. Ruptura
- **Sin límite de golpes en ninguna fase.** Golpes durante la ruptura = daño nativo normal (invulnerabilidad nativa), sin postura.
- F1: 120/120 → TNA_DAMAGE_L sostenido 90 ticks → recuperación → 0/120 (sin guardia forzada). HP1 = 0 → transformación nativa (prioridad).
- F2/F3: 160/180 → **STAGGER_A** (TNB_DOWN_SIPPU sostenido 90 ticks), **sin caída**.
  - **Ruta A Mortal Draw**: B cerca (≤ 350, Link mirando al Darknut, ±0x2800) durante STAGGER_A → callback POST de `checkCutAction` (después de Chilfos) convierte el tajo en el **Mortal Draw nativo** (`kk_native_mortal_draw` = `procCutFinishInit(MORTAL_DRAW_B)`, el escritor ya auditado de Chilfos) y emite un recibo de esta instancia/generación (75 ticks). Solo el **contacto real** (`setDamage` con corte Mortal Draw, colisionador = espada de Link, recibo válido) ejecuta.
  - **Ruta B Shield Attack + Helm Splitter**: Shield Attack nuevo → **STAGGER_B**: clip **TNB_DOWN** (distinto: ninguna de sus poses de sujeción está a menos de 43 unidades de cualquier pose de TNB_DOWN_SIPPU), desde el fotograma 1 con fundido de 5, sostenido en el 15; HeadLock encendido (Link: `checkCutHeadState`); ventana propia 60 ticks [PROVISIONAL]. Solo el contacto real del Helm Splitter (`CUT_TYPE_HEAD_JUMP`) ejecuta.
  - Extensión: si el remate ya vuela al cerrarse la ventana, como máximo 30 ticks [PROVISIONAL], una vez, mientras siga volando.
  - Sin contacto: recuperación limpia y postura 0.

## 7. Caída, suelo, Finish, levantamiento (DKR01 extendido)
- Contacto de ejecución con resistencia restante: `dkr_exec_request()` (identidad, ranura, clip listo, cuerpo no poseído) → `ACT_ENDING 0` (`dkn_native_exec_fall`) → la caída nativa **TN2B_DIE** igual que la primera derrota (cuerpo, espada, color, atención, DownFlg/DownPos, Finish nativo).
- **180 ticks contados desde el final del clip de caída**, congelados mientras vuele cualquier Ending Blow.
- Sin Finish y resistencia > 0: **levantamiento** = TN2B_DIE **hacia atrás** con su propio control de fotogramas (79→72 ×2, 72→60 ×0,8, 60→34 ×1,6, 34→16 ×1,1; ~1,7 s), y desde el fotograma 16 (la pose de DIE más cercana a TNB_WAIT: 31 unidades) TNB_WAIT con fundido de 10 → `ACT_CHASEL 2` (espera en guardia) → controlador con postura **0/160 (F2) o 0/180 (F3)**, **misma resistencia**, resurrección **no** consumida, FIX02 **no** reproducido.
- Finish real en F2 → exactamente la primera derrota: FIX02 una vez → F3 con 480/480 y 0/180.
- Finish real en F3 → al terminar todo el Ending Blow de Link: modo nativo 2 de desaparición (oscurecimiento 45 ticks, efecto, borrado) del cuerpo ya caído; sin segunda caída ni segunda resurrección.
- HP 0 en el mismo impacto que la ejecución: gana la derrota real (F2 → ruta DKR01 de 300 ticks/Finish/FIX02; F3 → muerte nativa). Nunca levantamiento con 0.
- Descarga del mod durante una caída por ejecución: el Darknut se pone en pie (nunca muere por descargar).
- La derrota real por daño ordinario no cambia (F2: caída/Finish/300 ticks/FIX02; F3: muerte nativa).

## 8. HUD y logs
Barra: 120/160/180, oculta en transformación, caída, suelo, Finish, levantamiento y resurrección; tambaleos marcados. Trazas: `COMBO_SELECT/START/END/CANCEL`, `NATIVE_CHAIN_SUPPRESSED`, `SHIELD_ATTACK_REJECTED`, `STAGGER_A`, `STAGGER_B`, `HELM_PREP/START/CONTACT`, `MORTAL_START/CONTACT/END`, `ADAPTIVE_GUARD`, `ENEMY_PARRY_REAL`, `SWORD_REBOUND`, `ORDINARY_BLOCK_NO_REBOUND`, `COUNTER_START`, `POSTURE_BREAK`, `BREAK_TIMEOUT/EXTENDED`, `EXECUTION_FALL`, `EXECUTION_LETHAL_PRIORITY`, DKR01 `EXECUTION_FALL`, `DOWN_START`, `GETUP_TIMER_180`, `FINISH_COMMIT`, `FINISH_RECEIPT`, `GETUP_START/DONE`, `DKR01_REAL_LETHAL`, `FIX02_RISE`, `FINAL_NATIVE_DEATH`, resúmenes por fase (`DARKNUT_STAGE_SUMMARY`, `DARKNUT_INITIATIVE_REJECTS`, `DKN01_SUMMARY`, `DKR01_SUMMARY`). Tope 6000 líneas; supresiones y rechazos con límite.

## Escritores
DKN (16, `DKN_NOINLINE`): los 13 de 0.13.9 + `dkn_native_headlock`, `dkn_native_exec_fall`, `dkn_native_neutral`. Link solo a través de `kk_native_mortal_draw` (uno, auditado). DKR (10 + binder): + `dkr_native_getup_rate`, `dkr_native_getup_combat` (el único `setBck`, TNB_WAIT 0x2A; no toca resistencia/vida/resurrecciones), `dkr_native_final`.
Offsets nuevos leídos, medidos en el EXE 2.0.3 y fijados con `static_assert` (`dkn_bridge.inc`): `mSphA 0x4530`, `mSphB 0x4a58` (bucles de `damage_check`), `mSphC 0x4f80`, paso 0x1b8 (TgShield de `setBodyShield` en 0x4618/0x47d0/0x4988).

## Evidencia automática
- `dkn_lab`: 12 609 comprobaciones PASS (tablas, 46 impactos, ritmo F1 escalado/F2, postura 120/160/180, bandas, armadura, ruptura sin tope y rutas, iniciativa 25/25/25/25 y sin dependencia nativa, regresión Shield Attack, defensa/parry/contraataque, veredictos de ejecución y prioridades).
- `dkr_world_lab` (adaptador DKR01 literal contra la transcripción nativa): 4 814 comprobaciones PASS, incluidos caída por ejecución, 180 exactos desde el fin de la caída, levantamiento monótono hacia atrás, misma resistencia, Finish F2→FIX02, F3 sin Finish→de pie, F3 Finish→desaparición tras el Ending Blow, Finish en el tick 179 (sin levantarse a mitad; fallo reanuda), rechazos, descarga.
- Mutantes: DKN **78/78**, DKR **65/65** detectados (g++ local; CI con MSVC).
- Auditorías: `dkn_audit` (16 negativos), `dkr_audit` (13), `dkn_native_audit` (87 hechos de la fuente oficial, incluidos `checkNormalAttackAble`, `checkNextMove`, Shield Attack→GUARDL, `setBodyShield`, `checkCutReverseAt`, `checkCutHeadState`, `procCutHeadInit`, `J3DFrameCtrl::update`), `source/store/mutant-anchors`, `kk/liz/fix03/lft03` negativos.

## Límites honestos
- **No hay laboratorio "world" del adaptador DKN** (como en 0.13.9): su lógica se valida por el núcleo, la compilación MSVC/clang-cl, auditorías de fuente y hechos nativos. Las rutas de Link (Mortal Draw, Helm Splitter, rebote, Ending Blow) solo se prueban de verdad en el juego.
- Valores [PROVISIONAL] listados en `dkn_core.hpp`.
- Naturalidad de F1, del segundo tambaleo y del levantamiento hacia atrás: medidas por pose, **pendientes de juicio humano**. Si el levantamiento resultara poco natural, la alternativa documentada es un clip propio (no FIX02, reservado a la resurrección).
- El Helm Splitter requiere fijar al Darknut (Z) y tener la técnica aprendida. El Mortal Draw no requiere envainar: un tajo con B cerca del Darknut roto se convierte en el Mortal Draw nativo, como en Chilfos.

## CI (windows-build-lab, rama `ci/light-fades-twice-darknut-miniboss-fix01-0-13-10`)
| Perfil | Run | Fuente | Resultado |
|---|---|---|---|
| FAST | 43647437923 | 41e6a2f | PASS (MSVC, PE: sin imports nuevos del juego) |
| INTEGRATION | 43647898447 | c1020a7 | PASS (todos los laboratorios) |
| FULL | 43648730941 | c1020a7 | **PASS**: todos los shards de mutantes (DKN 79/79, DKR 65/65), finalize, descarga independiente verificada |

Entre 41e6a2f y c1020a7: un clip de tambaleo sostenido ya no se reproduce a velocidad 0 (el `isStop()` nativo terminaría el segundo tambaleo y la extensión del remate).

Entregable: `LIGHT_FADES_TWICE_DARKNUT_MINIBOSS_FIX01_0_13_10_PRIVATE_TEST_windows-amd64_c1020a7f48ee.dusk`, 372 216 B, SHA-256 `2baaab066f185ea27cad6e2d9a2692cc09cf18dc2378e70731828a4ed3552148` (artefacto 14135033845, caduca 2026-12-14; recalculado tras descargarlo). DLL `c5299fb5…cacca`; FIX02 sin cambios (`f96356fb…1524`). Estado: **HUMAN_RUNTIME_PENDING**.
