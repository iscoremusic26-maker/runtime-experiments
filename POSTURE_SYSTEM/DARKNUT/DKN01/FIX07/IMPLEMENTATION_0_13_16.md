# LIGHT FADES TWICE 0.13.16 — DARKNUT MINIBOSS DKN01 FIX07

Estado: **AUTOMATED_PASS / HUMAN_RUNTIME_PENDING**. Compila (clang-cl 21 local; MSVC en CI), pasa laboratorios, mutantes y auditorías. Nadie lo ha jugado: nada de este documento afirma que algo se vea, se oiga o se sienta bien en el juego.

## Base
- Fuente compilada FINAL de 0.13.16: `0ef82a51590b6339fc1bd142d42e3ed3d25a3c1d`.
- Fuente compilada de 0.13.15 FIX06: `803a5b1451b8e2b25c0311f766f2fb865279b14e` (rama FIX06 = `9e7a206`, solo documentación encima).
- Ramas nuevas: fuente `feature/light-fades-twice-darknut-miniboss-fix07-0-13-16` (worktree `runtime-experiments-dkn-fix07`); CI `ci/light-fades-twice-darknut-miniboss-fix07-0-13-16` (worktree `windows-build-lab-dkn-fix07`, desde `3dac415`, el FULL de FIX06). Ninguna rama anterior, `main` ni tag tocados; sin release pública.
- Log humano: `dusklight-20261122-090111.log` (0.13.15), leído en `%APPDATA%\TwilitRealm\Dusklight\logs`; no se copió al repositorio.
- Código nativo: `TwilitRealm/dusklight` `v2.0.3` = `40457c6`; EXE 2.0.3 `ffa99203…` (desensamblado local con capstone).

## 1. Espada que no se oscurecía (causa demostrada)
- Log: 4 Finish definitivos con `SWORD_DARKENING_START` y contador de escrituras subiendo, pero la espada no se veía oscura.
- Causa (fuente 2.0.3 + EXE): en `daB_TN_c::draw()` la secuencia de la espada es `setLightTevColorType_MAJI(espada)` → `mpModelMorf1->entryDL()` (EXE `0xcc882d` → `0xcc8839`). MAJI vuelve a escribir el TEV color 0 del material de la espada con `tevStr.TevColor` justo antes de que `mDoExt_modelEntryDL` capture el material (diff `0x11000084`, incluye TevReg). La escritura de FIX06 en el PRE de `draw` quedaba sobrescrita siempre: contador correcto, estado dibujado intacto.
- Corrección: hook PRE/POST de `mDoExt_McaMorfSO::entryDL` (exportado, prólogo `mov rcx,[rcx+8]; test rcx,rcx`, sin nada relativo a IP). El PRE de `draw` solo *arma* el morf de la espada de ESE Darknut (`tint_morf = mpModelMorf1`); el PRE de `entryDL` de ese morf escribe el valor del cuerpo (`mMaterialColor`, progresivo con el cuerpo, sin negro fijo) DESPUÉS de MAJI; su POST restaura; el POST de `draw` restaura cualquier resto. Solo en la muerte definitiva (Finish o HP0 en F3, etapa DEAD); nunca en caídas recuperables, F2, el clip FIX02 ni el getup; otros Darknuts y modelos no se arman.
- `tests/test_dkn_sword_tint_adapter.py`: modelo del orden nativo de draw; reproduce que la ruta FIX06 no llega al diff y que FIX07 sí; 5/5 mutantes detectados. Verificación visual: pendiente humana.

## 2. F1-C3 (solo ese combo)
- Objetivos finales 24 / 56 / 57 / 40 ticks (total 177; FIX06 ≈ 36 / 86 / 88 / 62). Simulador: 24 / 56 / 57 / 40 exactos.
- El par 1→2 es imposible a 24 ticks con el tope de recuperación de FIX01 (1,51: mínimo 35,8). Excepción acotada a ese par: inicio del vertical en el frame 22 y recuperación ×1,75 (`kF1C3Pair1RateMax` 1,76). Ningún otro par ni combo la usa.
- Huellas FNV de los 14 planes restantes = FIX06 bit a bit (F1-C1/C2/C4, F2/F3 ×8, counters, singles; F2-C4 3→4 sigue en 9).

## 3. Ejecuciones F1
- Mortal Draw y Shield Attack → Helm Splitter en F1: **120 HP en total**, saturado `min(hp1, 120)`; armadura 1 pieza por cada 50 HP. F2/F3 sin cambios. `F1_EXECUTION_CONTACT` registra objetivo / efectivo / saturado.

## 4. Salto ofensivo (F2/F3)
- Saltos nativos: `initChaseL` modo 8 (≈245 u) y modo 17 (≈405 u, el largo nativo), aterrizaje modo 9. F1 no tiene salto nativo con maza y armadura (`LEAP_F1_NOT_AVAILABLE`): F1 conserva su aproximación nativa.
- Oportunidad: Link entre 445 y 775 u, de frente, en combate común (sin secuencia, sin ruptura, sin evento). Debounce 5 ticks seguidos → **una sola tirada** (`LEAP_ROLL`): **90 % salto + uno de los cuatro combos de la fase (25 % cada uno) / 10 % aproximación normal**. Sin tirada por tick ni re-tirada en el umbral: tras tirar, el episodio cierra (Link dentro del alcance o 300 ticks) y además 150 ticks de enfriamiento. Lab: 100 000 oportunidades → 89,84 % / 10,15 %; combos 25,08 / 25,05 / 24,76 / 25,12 %.
- Seguridad: 4 muestras `gndCheck` (incluida la del cuerpo tras el aterrizaje), 1 `lineCheck` a la cintura y `waterCheck`; caída > 80, subida > 50, pared o agua → `LEAP_REFUSED_GEOMETRY` (sin salto, sin re-tirada). Desnivel con Link > 120 → no hay oportunidad. Aterrizaje nunca a menos de 200 u de Link (ideal 285).
- Lease `Leap → Combo` desde el despegue hasta la recuperación del combo: las acciones ordinarias de Link no lo cortan; las excepciones legítimas (ruptura, HP0/transformación, derrota, sin objetivo, evento, guardia rota, Link > 700, watchdog 120) sí, una vez. El ataque nativo de aterrizaje se sustituye por el aterrizaje neutro; el combo arranca en suelo.
- Primer impacto tras tocar suelo (lab): F2-C1 21 ticks, C2/C3 15, C4 16 (≥ 0,5 s, golpe justo). Constantes marcadas [PROVISIONAL].

## 5. Reposición tras resucitar / levantarse (revisada)
- Bandas iguales: < 240 salto atrás, 240-370 se queda, > 370 adelante si es seguro. Novedades: el salto atrás también comprueba trayectoria; la decisión espera hasta 20 ticks el giro nativo hacia Link; si el salto corto aterrizaría a < 240 (370-485) se queda (`ForwardTooClose`); si el corto se queda lejos usa el largo (17). Nunca ataca al aterrizar. `REPOSITION_DECISION/WAIT/LANDED`.

## 6. Maza lanzada (F1 → F2, `ACT_CHANGEDEMO`)
- Bloqueo: +50 postura Link. Golpe directo: +60 postura Link (el daño de vida nativo se mantiene). Parry: 0 (FX naranja + ×1,22, sin daño). Esquiva: 0. Postura del Darknut: nunca. Un crédito por lanzamiento (`MaceLedger`). `MACE_THROWN/CONTACT/LANDED/PROJECTILE_END`.

## 7. I-frames de esquiva de Link (LDG01, nuevo módulo)
- Adelante (rodada `PROC_FRONT_ROLL`) 9 ticks; lateral (`PROC_SIDESTEP` izquierda/derecha) 6; atrás (`PROC_BACK_JUMP` / sidestep hacia atrás) 6. Ventana `[inicio, inicio+N)`.
- Solo esquivas humanas en contexto de combate (Z-target a un enemigo o enemigo soportado a ≤ 800 u, [PROVISIONAL]); nunca intención, saltos, recuperación de caída, lobo, caballo, nado. `PROC_SIDE_ROLL` excluido (preparación de Back Slice).
- Mecanismo: POST de `dCcS::ChkAtTgHitAfterCross` (virtual, slot +0x28 de `cCcS`; el propio `SetAtTgCommonHitInf` lo llama): devolver *true* = el cruce no cuenta → sin daño, sin hitmark, sin recibos. Sin invulnerabilidad global, sin daño diferido. Continuidad: el mismo filo que siga atravesando a Link en ticks consecutivos sigue anulado.
- Exclusiones: rodada adelante contra la estocada del Darknut (F2A); barridos especiales: ningún ataque de los enemigos soportados está clasificado como barrido especial genuino, así que no se inventó ninguna clase. Telemetría `LDG01 event=DODGE_START/DODGE_END/CONTACT` y `LDG01_SUMMARY`.

## 8. FX de parry
- Log 0.13.15: 361 transacciones FX Darknut completas (2 emisores + choque). Irregular y demostrado: 60 destellos `ALREADY_WARM` (reinicio en la posición del contacto anterior) y 2 `NATIVE_NO_FLASH` (petición perdida en estado 3).
- Correcciones: `pfx_native_flash` re-arma el estado 3 → 4 (reinicio nativo) y coloca el destello en la posición de ESTE contacto; `pfx_native_unthrottle` limpia el bit `0x40000000` de `actor_status` (throttle nativo de una marca por actor/tick) solo para la marca de un registro naranja sin chispa todavía; el choque se sigue por identidad (id + mapinfo, sin punteros) y se registra si otro SE del mismo id lo corta (`CUT_BY_A_LATER_SAME_ID_SE`) o si dura < 60 ticks.
- Colores: todos los componentes naranja (0x0117 y 0x0118), ×1,22 por parry válido en ambos sentidos, dos señales independientes. Que un parry concreto se vea u oiga no está demostrado: queda la telemetría por contacto.

## PE / contrato
- +2 HOOK_MEM (41): `mDoExt_McaMorfSO::entryDL`, `dCcS::ChkAtTgHitAfterCross` (vcall local, slot 40, sin import). +6 imports de juego (129 con MSVC): `entryDL`, `fopAcM_gc_c::gndCheck/mGroundY`, `fopAcM_lc_c::lineCheck`, `fopAcM_wt_c::waterCheck/mWaterY`.
- Escritores nuevos: `pfx_native_flash` (eflight 0x974/0x978/0x97c..0x987) y `pfx_native_unthrottle` (RMW único sobre `actor_status`+0x583 bit 6 = 0x40000000), auditados en el binario.
- Admisión DKN01 sin cambios (B_TN param 0x000001ff, mType 1, mType2 0, switch 0xff). BCK FIX02 intacto.
