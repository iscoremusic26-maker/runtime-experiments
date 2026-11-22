# LIGHT FADES TWICE 0.13.15 — DARKNUT MINIBOSS DKN01 FIX06

Estado: **HUMAN_RUNTIME_PENDING**. Compila (clang-cl 21 local; MSVC en CI), pasa laboratorios, mutantes y auditorías. Nadie lo ha jugado: nada de este documento afirma que algo se vea, se oiga o se sienta bien en el juego.

## Base
- Fuente compilada de 0.13.14 FIX05: `1c2447ec61fab3cbe8f33a3e7b92ae0d10975bd0` (incluye el cierre de Codex: reanclaje solo de la cápsula de `mCps`, esferas físicas intactas). `origin/feature/...-fix05-0-13-14` = ese SHA; ningún trabajo posterior.
- Ramas nuevas: fuente `feature/light-fades-twice-darknut-miniboss-fix06-0-13-15` (worktree `runtime-experiments-dkn-fix06`, desde `1c2447e`); CI `ci/light-fades-twice-darknut-miniboss-fix06-0-13-15` (worktree `windows-build-lab-dkn-fix06`, desde `83e4c59`, el FULL de FIX05). Ninguna rama anterior tocada.
- Log humano: `dusklight-20261121-234432.log`, 8843 líneas, SHA-256 `b5ef18b09e20f54e4903965fe7d2b2fcbcc6881779ad186a64f9f904020973dd` (copia local en `dkn_fix06_evidence/`, no en el repositorio). Recuentos reproducidos con un parser propio por actor y fase (`dkn_fix06_evidence/analysis/fix05_log.py`): 68 parries enemigos = 68 counters (F1 33, F2 18, F3 17), 26 combos + 2 singles F1, 12 rupturas, 5 contactos Mortal Draw, 1 HELM_PREP, 3 FIX02_RISE_DONE, 22 NATIVE_LEAP_SUPPRESSED, 4738 `offense_refused_by_exchange`.
- Código nativo: `TwilitRealm/dusklight` tag `v2.0.3` = `40457c6adb381928e4b5fef6ed459ed291edd5e2` (comprobado con `gh api`), EXE 2.0.3 `ffa99203…`.

## Causas demostradas
1. **Bucle de iniciativa** (fuente FIX05 + log): `Defense::confirm` programa UN counter; al terminar, `dkn_move_end` → `Initiative::ended` devuelve el turno a la iniciativa común, y mientras Link mantiene su cadena `hold_verdict` / `InitView.defending` rechaza toda ofensiva (4738 rechazos). B → parry → counter → parry de Link → B no tenía salida.
2. **Pausas de F2-C2 / F2-C4**: los intervalos son audio × 1,40 (37/47 y 37/34/43 ticks en el log; el modelo del laboratorio reproduce exactamente 37,9,47,12,12,13 y 37,34,8,43).
3. **Tambaleo congelado**: `helm_rate()` = 1,0 hasta el fotograma 12 y luego `kHoldCreep` 0,02 (log 4358→4423: fotograma 12 → 13,0 en 65 ticks).
4. **F1 sin ejecutor**: `exec_verdict`, `helm_prep` y `sa_verdict` exigían fase 2-3; `STAGGER_A … executor=NONE_IN_F1`. Nativo (2.0.3): `damage_check` fase 1 deja pasar HEAD_JUMP y MORTAL_DRAW_A/B por la esfera del escudo; `setDamage` fase 1 suma piezas y pone ACT_DAMAGEH.
5. **Espada sin oscurecer**: `draw()` escribe `mMaterialColor` en el TEV color 0 de los materiales del CUERPO antes de `mpModelMorf2->entryDL()`; la espada (`mpModelMorf1`, parte 15) se dibuja sin esa escritura. Su material `tn_sword_b` tiene la misma etapa TEV que `tn2_body` (KONST, TEXC, RASC, **C0**, medido en `tn2_sword_b.bmd`), ambos modelos con flags de diff `0x11000084`, y `mDoExt_modelEntryDL` captura el material en la instancia al llamar `entryDL` (cada fotograma de presentación).
6. **FX**: en el log, las 174 transacciones de parry Darknut (106 de Link, 68 del Darknut) tienen 2 emisores nativos y el choque con pitch ×1,22 releído; ninguna `NO_NATIVE_SPARK/CLASH`. Lo único demostrablemente irregular: `flashes=150` para 174 parries. El destello cálido recolorea el destello nativo `g_env_light.eflight`; `pfx_native_flash()` solo lo hace si el nativo acaba de pedirlo (estado 1/4) y aún es del tipo 0. El log no registra por contacto cuál de los casos ocurrió: **no se afirma una raíz**; se añade telemetría por contacto.

## Cambios
### 3.1 Retiming selectivo (`dkn_core.hpp`)
`kIvTargets`: objetivos FINALES en ticks a 30 Hz, después de ×1,40, solo para los cinco pares aprobados; `plan()` los usa solo con el tempo por defecto (`plan(c, i, 1.40f)` reconstruye el plan FIX05 bit a bit; la huella FIX04 de los ocho combos se sigue comprobando por esa vía).

| Combo | par | FIX05 plan (sim / log) | FIX06 objetivo | sim | nota |
|---|---|---|---|---|---|
| F2-C2 | 1→2 | 36,96 (37/37) | **27** | 27 | ritmo nativo 1,0 |
| F2-C2 | 2→3 | 8,82 (9/9) | 8,82 | 9 | protegido |
| F2-C2 | 3→4 | 47,04 (47/47) | **30** | 30 | ritmo nativo 1,0 |
| F2-C2 | 4→5 / 5→6 / 6→7 | 12,18 / 11,97 / 12,60 | iguales | 12 / 12 / 13 | protegidos (dobles) |
| F2-C4 | 1→2 | 36,96 (37/37) | **27** | 27 | = máximo natural del par (corte 28 / inicio 1) |
| F2-C4 | 2→3 | 33,18 (34/34) | **25,5** | 26 | cuantización natural 25/26 |
| F2-C4 | 3→4 | 8,82 (8/8) | 8,82 | 9 | protegido: plan continuo idéntico; 8→9 por la fase de tick |
| F2-C4 | 4→5 | 42,63 (43/43) | **30** | 30 | ritmo nativo 1,0 |

Parámetros protegidos (corte/inicio/ritmos de los pares no modificados, `rate_mid` de los dobles, arranque y recuperación final, morphs) idénticos a FIX05 (lab FIX06-A). Consecuencia inevitable documentada: el kick inicial de F2-C4 ya no se reproduce a cámara lenta (0,73 en FIX05) sino a ritmo nativo; su AT 8..12 dura sus 4 ticks nativos (antes 5).

### 3.2 Secuencia de iniciativa (`Seq`, `seq_gate`, `Defense::confirm` con `routes`)
- Parry auténtico confirmado (rebote persistente, igual que FIX05) → UNA tirada en flujo propio: 60 % uno de los cuatro combos de la fase (25 % cada uno), primer impacto 27 ticks tras el rebote (ventana aprobada 27-36); 40 % el counter FIX05 (tercios, ≥ 24 ticks).
- Counter terminado de forma natural (`NATIVE_END`) → UNA tirada: 80 % uno de los cuatro combos; puente: no antes de 3 ticks tras su recuperación nativa ni con primer impacto < 24 ticks tras el último impacto del counter. Medido por counter/combo (lab): fin de counter→inicio de combo 3 ticks; último impacto del counter→primer impacto del combo 36-52 ticks en F2/F3 y 39-89 en F1 (la recuperación nativa de la maza es larga y no se le suma otra espera). Si Link está en un estado forzado (deslizamiento, daño, derribo) el combo espera a que quede libre + 6 ticks, nunca más de 60 tras el counter.
- La secuencia es propiedad del actor/generación desde la confirmación hasta su última recuperación: en el PRE corre `seq_gate` (función pura cuyas entradas NO incluyen ningún ataque, bloqueo, parry, Shield Attack ni salto de Link) antes de la defensa adaptativa, la retención, los especiales y la iniciativa común; un bloqueo devuelve la acción nativa (como en un movimiento propio). Golpes y bloqueos de Link conservan daño y postura reales (`link_hits_in_seq`, `link_blocks_in_seq`).
- Excepciones (una vez, con lo programado): ruptura, HP1 0 / transformación, derrota, sin objetivo, evento, guardia de Link rota, Link > 700, watchdog, inicio rechazado.

### 3.3 Shield Attack F1 del Darknut
Ya era parable por la ruta común (`dkn_at_authority` → ventana de impacto → `dkn_link_contact`) tanto como counter (`F1-COUNTER-BASH`, movimiento propio) como especial (escudo sostenido 38 / pasividad 75, cooldown 240, solo con escudo físico). Sin cambios de mecánica; el counter parado por Link entra en la regla 80/20.

### 3.4 / 3.5 F1 Mortal Draw / Helm Splitter y tambaleo
- `on_dkn_cut_action_post` pide el Mortal Draw nativo también en la ruptura F1 (mismas condiciones). `sa_verdict` acepta el Shield Attack nuevo en StaggerA de cualquier fase. Contacto real (`exec_verdict_f1`): **100 HP totales** (`f1_exec_hp`, sin underflow), armadura por progreso de HP (cruza 1 o 2 umbrales de 50 sin doble crédito; HEAD_JUMP usa el orden nativo `setBreakHeadPart`), `Break::exec_f1` → recuperación natural del clip → GUARD_RECOVER (0/200). HP 0 → transformación nativa primero. Nunca DKR01.
- Segundo tambaleo: el clip de daño a 1,0 hasta su centro (fotograma 12) y luego un balanceo continuo 12 ± 3,5 con periodo de 24 ticks (dos periodos en la ventana de 60; termina en el centro avanzando, y la recuperación sigue hacia delante a 1,25). Ritmo = deseado − actual cada tick, nunca 0. F2/F3: `TNB_DAMAGE_R` (ACT_YOROKE 10). F1: su clip nativo `TNA_DAMAGE_R` (0x0B, executeDamageH modo 2). Rango 8,5-15,5 = zona medida de cabeza baja / arma baja de ambos clips en el rig `tn2.bmd` (`tests/data/dkn_clip_survey.py`).

### 3.6 Reposicionamiento
Tras `FIX02_RISE_DONE` o `GETUP_DONE` (una decisión): `< 240` salto atrás nativo, `240..370` mantener, `> 370` salto adelante solo si aterriza a ≥ 240 (desplazamiento nativo modelado sobre la física de `executeChaseL`: atrás 450 u, adelante 245 u → umbral efectivo 485; ajuste documentado). Sin salto si hay evento, pared detrás, desnivel > 120 o Link no está delante. `initChaseL(6/8)` replicado; el ataque de aterrizaje nativo se sustituye por su aterrizaje (`initChaseL(9)`) o por la persecución neutra; sin AT; después no hay iniciativa antes de 15 ticks (más la reentrada de 45).

### 3.7 Espada en la muerte definitiva
Nuevo objetivo `daB_TN_c::draw` PRE/POST (exportado; `daB_TN_Draw` salta a su thunk; prólogo `mov r11,rsp; push rdi; sub rsp,0C0h`): solo para el Darknut admitido en fase `DEAD` y con `mMaterialColor ≠ 0`, el PRE escribe ese valor en el TEV color 0 del material de la espada (como el cuerpo) y el POST restaura los valores guardados. Ninguna caída recuperable ni FIX02 (fase ≠ DEAD; DKR01 mantiene `mMaterialColor`), ningún otro Darknut.

### 3.8 FX
Efectos sin cambios. `FX_TXN` añade `flash=WARM_SET|ALREADY_WARM|NATIVE_NO_FLASH|NO_MARK_SEEN(state,type)`, lectura del estado nativo que encontró la primera marca de cada parry.

## Contrato PE
+1 objetivo `HOOK_MEM` (39) y +1 import del juego (`?draw@daB_TN_c@@QEAAHXZ`, 123). Medido en build local clang-cl frente a FIX05: exactamente ese import; confirmado por el enlace MSVC (FAST). Tres escritores nuevos (`dkn_native_jump`, `dkn_native_jump_land`, `dkn_native_sword_color`). mod.cpp: 2 hunks `dkn01_fix06`; parry_fx: 1 + 4 hunks (telemetría).

Toolchain: el runner `windows-latest` pasó de MSVC 19.51.36260 (FAST de FIX05 43866554557) a 19.52.37029 (primer FAST de FIX06 44993300188, bloqueado solo por el pin PE). Con los MISMOS objetos CRT estáticos enlazados en ambos mapas (`gs_report.obj`, `utility_desktop.obj`, `cpu_disp.obj`, `amdsecgs.obj`, `gshandler.obj`), el CRT 14.52 importa `KERNEL32!IsProcessorFeaturePresent`. Se fijó como import de sistema del arranque CRT (commit `223adf9`), sin tocar el conjunto de imports del juego.

## Fuente compilada definitiva
`803a5b1451b8e2b25c0311f766f2fb865279b14e` = `e662c4d` (FIX06) + `223adf9` (pin CRT) + `803a5b1` (prueba ejecutable `tests/test_dkn_sword_tint_adapter.py` del PRE/POST de `draw` de producción contra dobles de material J3D compartidos: solo muerte definitiva, sin acumulación, restauración exacta, otras instancias intactas, un POST perdido nunca escribe después; 1011 comprobaciones, 4/4 mutantes; en el gate FAST).

## Evidencia automática local (antes de CI)
- `dkn_lab` 852 066 comprobaciones PASS (sección FIX06: retiming; 200 000 rutas → 59,98 % combo; 200 000 continuaciones → 80,05 %; 8000 sesiones × 7 perfiles de entrada de Link sin ningún cambio de calendario; 266 220 casos de excepción sin movimiento tardío; F1; salto; tinte). Resto de laboratorios PASS (liz 3 516 534, cp06f1_world 1 375 681 994, lft03 168 442, lgc 565, dkr 2318, dkr_world 5007, …).
- Mutantes DKN+LGC: 241 (191 + 50 nuevos); la primera pasada local detectó 238 y reveló 3 debilidades del laboratorio (constante `kHelmClip` muerta; dos caídas por índice fuera de rango que impedían la línea RESULT); corregidas y re-ejecutadas: detectadas.
- Auditorías: dkn 68/68 negativos, dkr, kk, liz, lft03, fix03, fuente, contrato nativo 157 hechos, anclajes de mutantes 1231.

## Límites honestos
- Sin prueba en el juego: sensación de turnos, legibilidad del primer impacto, naturalidad del balanceo y de los saltos, oscurecimiento visible de la espada y destellos requieren la prueba humana (Windows DX12).
- [PROVISIONAL] nuevos: `kBridgeSettleTicks` 3, `kBridgeFreeTicks` 6, `kBridgeHoldMax` 60, `kSeqWatchdogTicks` 900, `kRepoMaxDy` 120, `kRepoWaitTicks` 15, `kRepoSettleTicks` 15.
- El salto no comprueba suelo/borde a lo largo de la trayectoria (no hay línea de colisión sin nuevos imports); igual que el salto nativo, lo frena el `mAcch` contra paredes.
- No se midieron FPS ni latencia física de entrada.

## Registro CI (fuente compilada `803a5b1451b8e2b25c0311f766f2fb865279b14e`, rama CI `ci/light-fades-twice-darknut-miniboss-fix06-0-13-15`)
| Perfil | Run | Commit CI | Resultado |
|---|---|---|---|
| FAST | 44995124775 | `6ca33aff9957305933d61eb013357736d1e96cd2` | success (FAST_PASS) |
| INTEGRATION | 44995565121 | `22f8fe1bc2da4dd3a28c37b57b01a1048f9baff0` | success |
| FULL | 44996344005 | `3dac41529f1166bc7c21aaa3a049ab479d370f3b` | success: 16/16 jobs, 12 shards, FULL_PASS, mutantes 1633/1633 (dkn 241/241), 0 timeouts, 0 omitidos; independent-download ARTIFACT_DOWNLOADED_VERIFIED |

Ejecuciones previas (no certifican el SHA final): FAST 44993300188 sobre `e662c4d` (falló solo el pin PE por el import CRT del nuevo MSVC), FAST 44993707786 e INTEGRATION 44994113858 sobre `223adf9` (success).

Paquete: `LIGHT_FADES_TWICE_DARKNUT_MINIBOSS_FIX06_0_13_15_PRIVATE_TEST_windows-amd64_803a5b1451b8.dusk`, 389 371 bytes, SHA-256 `49355484f757629e2eefa6d2f0e85f148e0eee5db4c5d6559b3af7ec5dbf8880`; artefacto GitHub `LIZ_TEST_44996344005_1` id 14744347555 (ZIP 414 780 bytes, no es el `.dusk`), expira 2026-12-22T07:18:17Z. DLL MSVC x64 (linker 14.52) 1 750 528 bytes, SHA-256 `9d3ea3839e6530aa12b0625092c0cda2d8d530c9a8efcd0badd4785e102d5d4a`; BCK FIX02 45 024 bytes `f96356fb…1524`. Verificación local repetida contra el artefacto real: ARTIFACT_DOWNLOADED_VERIFIED y 6/6 paquetes manipulados rechazados.
