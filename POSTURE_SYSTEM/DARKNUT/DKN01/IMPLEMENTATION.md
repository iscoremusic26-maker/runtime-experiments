# LIGHT FADES TWICE 0.13.9 — DARKNUT MINIBOSS (DKN01)

Estado: **HUMAN_RUNTIME_PENDING**. Compila y pasa las auditorías; nadie lo ha jugado todavía. Nada de este documento afirma que funcione en el juego.

## Base y ramas
- Base: **0.13.8 DKR01**, `runtime-experiments` @ `0079b6f8` (rama `feature/light-fades-twice-darknut-resurrection-0-13-8`), entregada en FULL 43488594715 (artefacto 14068922446, `.dusk` `f14d9ce7…1ee0`, verificado por descarga).
- Fuente: rama nueva `feature/light-fades-twice-darknut-miniboss-0-13-9`. CI: rama nueva `ci/light-fades-twice-darknut-miniboss-0-13-9` en `windows-build-lab`.
- Mismo ID de mod (`dev.posture.post05_selective_reactions`), versión **0.13.9** (siguiente de la serie 0.13.x). Un solo `.dusk`.

## Actor exacto
Solo el filtro de DKR01 (`dkr::eligible`): `B_TN` con parámetros **0x000001FF**, `mType 1`, `mType2 0`, `mSwitchNo 0xFF`, sin `mStayNo2Flag`.
El "Darknut (Sword)" 0x010001FF, el del Templo del Tiempo (`mType 0`, ni siquiera llega a la admisión) y los colocados/Hyrule Castle no obtienen ranura: todas las callbacks retornan sin tocarlos. Se registran una vez (`DARKNUT_ELIGIBILITY … result=NATIVE`).

## Puntos de hook comprobados en `dusklight.exe` 2.0.3 (sha `ffa99203…0049`)
Todos exportados; el cuerpo real de cada uno se localizó siguiendo el thunk y se comprobó que el llamador hace un `call` real (no inline):

| Objetivo | Uso | Llamador real (EXE) |
|---|---|---|
| `daB_TN_c::action` PRE/POST | tick de la instancia | `execute` → `call action` (0x140cc8b52) |
| `daB_TN_c::damage_check` PRE/POST | umbral 480, impactos sobre Link, bloqueos | `action` 0x140cc3015 |
| `daB_TN_c::setDamage` PRE/POST | daño real (420 / 480), Tabla A | `damage_check` (3 llamadas reales) |
| `daB_TN_c::executeAttackH/L` PRE/POST | director de combos | `action` 0x140cc30b4 / 0x140cc3106 |
| `daB_TN_c::executeAttackShieldH/L` POST | escudo / patada | `action` 0x140cc30c1 / 0x140cc3110 |
| `daB_TN_c::_delete` PRE (2.ª callback) | retirar ranura | (objetivo DKR01) |
| `daAlink_c::checkDamageAction` POST (callback nueva, prioridad −402) | recibo nativo de impacto directo | (objetivo existente) |

Llamadas nativas nuevas: `setBck`, `setBreakPart`, `setBreakHeadPart` (fuera de línea: `executeDamageH`/`executeZakoChangeDemo` los llaman con `call`). `setActionMode` se replica (3 escrituras, fijado por `dkr_native_audit`).
Offsets x64 medidos en el desensamblado y fijados con `static_assert`: `mNextBreakPart 0xd08`, `mTimer4 0xd0c`, `mTimer5 0xd10`, `mInvincibilityTimer 0xcf8`, `field_0xa91 0xd21`, `mTimer10 0xd37`, `mCutJumpStatus 0xd3b`, `mActionMode2Copy 0xd2b`, `mWalkDir 0xd1c`, `mAtInfo 0x5ba8`, `mSphC 0x4f80`, `mSwordSphs 0x5138` (paso 0x1b8), `mCps 0x5818`, `mStates 0xc8c`.

### Orden real por tick
`execute` → `action()`: **`damage_check()`** (→ `setDamage` → `setActionMode(DAMAGEH/DAMAGEL/ENDING)`) → `field_0x700 = l_HIO.field_0x24 (360)` → `execute<ACT>()` (`executeDamageH/L`, `executeZakoChangeDemo`, `executeYoroke`, `executeAttack*` → `setBck`, `setSwordAtBit`…, `executeZakoEnding`) → `setBodyShield` → `posMove` → `mpModelMorf2->play()`; luego `mtx_set`, `cc_set`. El pase de colisión ocurre entre ticks: el `damage_check` del tick siguiente lee los resultados.

## Diseño por módulo
### 1. Fase 1: 420 HP propios + armadura progresiva
- `setDamage` POST: daño = `100 − health` (tras `cc_at_check`), restado a la reserva de 420 de la instancia. Bloqueos, invulnerabilidad (`mInvincibilityTimer`), bombas, bola de hierro, técnicas de Link: todo lo decide la ruta nativa (`damage_check` solo llama a `setDamage` en golpes que dañan).
- Progreso de armadura = 12 pasos de 35 HP, **tope 11 mientras quede HP** (11 = el escudo cae, "defensa final" nativa); **12 solo con 0 HP**.
- Se llama al `setBreakPart`/`setBreakHeadPart` nativo (sonido y física de piezas) **solo con un argumento mayor que las piezas ya rotas**: con un argumento menor, el bucle nativo nunca llega a 0 y rompería todas las piezas restantes. `mNextBreakPart` queda = piezas realmente rotas (incluido el "salto" del casco, que cuenta 2): el `+1/+2` nativo de `setDamage` se deshace.
- 0 HP → `mNextBreakPart 12` + `ACT_CHANGEDEMO` modo 0 → `executeZakoChangeDemo` nativo (armadura final, salto atrás, lanzamiento de la maza, desenvainado). Nada de `executeChangeDemo` del Templo, cámaras ni escenas.

### 2. Fase 2: 480 por vida
- `damage_check` PRE escribe `field_0x700 = 480` **solo para la instancia elegible en fase 2**. `setDamage` (llamado solo desde `damage_check`) es su único lector; `action()` escribe 360 después, sin efecto. `l_HIO` nunca se toca.
- DKR01 deja `field_0x6fc = 0` al resucitar → otra vez 480 completas. La barra/telemetría muestra `hp1=N/420` y `res2=N/480` por separado.

### 3. Postura, regeneración y ruptura
- 120 (F1) / 130 (F2 y resucitado). Unidades enteras (1 pt = 30000; n pts/s = n·1000 por tick): sin deriva.
- Regeneración tras 60 ticks elegibles sin ganancia; bandas por fracción restante (420 en F1, 480 en F2); **bordes deterministas: el valor exacto 75/50/25/10 % pertenece a la banda inferior**.
- Tabla A y Tabla B exactas (ver `dkn_core.hpp` `kMoves`). Un parry confirmado da +0 a Link.
- Sin tambaleo ordinario: la reacción `DAMAGEH`/`DAMAGEL` del golpe se devuelve al estado previo (se conservan hitmark, SE, invulnerabilidad y armadura). `ACT_YOROKE` nativo (corte fuerte contra la guardia) → bloqueo normal.
- Ruptura solo al máximo: `BREAK_PENDING` → (siguiente `action` PRE) `STAGGER_ACTIVE`: F1 `ACT_DAMAGEH` (`TNA_DAMAGE_L` 0x09), F2 `ACT_YOROKE` (`TNB_DOWN_SIPPU` 0x1B). El clip se reproduce **una sola vez** estirado hasta el final de la ventana (10 fotogramas a ritmo nativo y el resto estirado, sin bucle ni salto a 0); `mTimer5>0`, `mTimer10=0`, `mCutFlag=0`, `mCutJumpStatus=0` impiden la guardia temporizada y la salida temprana nativas.
- Fin: 90 ticks elegibles **o** 3 golpes efectivos únicos (uno por `setDamage`; la invulnerabilidad nativa deduplica fotogramas; los golpes no reinician clip ni ventana) → `RECOVERY_GUARD`: el clip termina a 1.25× con su salida nativa y se activa la guardia nativa forzada (`mTimer10` [PROVISIONAL] 45 ticks): bloquea lo que llega a su frente, sin invulnerabilidad global. Postura → 0.
- Prioridad: 0 HP de F1 → transformación; resistencia agotada → DKR01, aunque esté tambaleado.

### 4. Impactos del Darknut sobre Link (uno por ventana)
- Ventanas de impacto por movimiento (= ventanas AT nativas; **B dividida en dos**: corte 1 [13,21), corte 2 [21,38); B1 [13,20)).
- `damage_check` PRE lee el contacto AT↔cilindro Tg de Link: escudo + ventana de Shield Attack (LinkTrack/CP04 [−1,+7]) = **parry**; escudo sin ventana = **bloqueo**; cuerpo = **directo**, acreditado solo con el recibo nativo de daño de Link (unión FIX01). Tras resolver, el AT de esa ventana se apaga; la siguiente ventana se rearma (re-armado rápido del par para B y las dos estocadas de F2-C2).
- **spl 1** en arma/escudo/patada en lugar de 9/10 (ruptura nativa inmediata de la guardia en `checkDamageAction`): Link solo rompe guardia al llegar a 100 (LNK05).

### 5. Los ocho combos
Los picos son los **medidos de las 8 grabaciones originales** (decodificadas sin modificar; `tests/data/dkn_audio_peaks.txt`); se usan solo las diferencias. Diferencias con el encargo: F1-C2 golpe 1 a 0.53 s (no 0.58 → intervalo 1.60 s), F1-C3 golpe 1 a 0.51 s (no 0.57 → 0.47 s); el resto ±0.03 s.
Fotogramas de impacto medidos por cinemática directa sobre el rig real (`tests/data/dkn_swing_profile.txt`): F1-A 22, F1-B 26 (= `SWD_IMPCT` nativo), escudo 7, F2-A 10, F2-B 15.5 y 29.5, patada 10. **B1 corta en el fotograma 20** (mínimo de velocidad al final del seguimiento del corte 1; el re-armado del corte 2 empieza en 21).
Planificador: línea temporal continua por segmentos (wind-up / entre cortes / seguimiento), cortes y arranques dentro de rangos que conservan wind-up y seguimiento, tasa 0.55–2.40; cada tick la tasa J3D se fija para caer exactamente en el fotograma planificado (sin deriva). Simulación tick a tick del modelo del adaptador (`tests/dkn_lab.cpp`):

| Combo | Par | Audio (s) | Audio (ticks) | Simulado (ticks) | Error | Acumulado |
|---|---|---|---|---|---|---|
| F1-C1 | 1→2 | 0.370 | 11.10 | 12 | +0.90 | +0.90 |
| F1-C1 | 2→3 | 0.860 | 25.80 | 25 | -0.80 | +0.10 |
| F1-C1 | 3→4 | 0.395 | 11.85 | 12 | +0.15 | +0.25 |
| F1-C1 | 4→5 | 0.895 | 26.85 | 27 | +0.15 | +0.40 |
| F1-C2 | 1→2 | 1.600 | 48.00 | 49 | +1.00 | +1.00 |
| F1-C2 | 2→3 | 0.710 | 21.30 | 21 | -0.30 | +0.70 |
| F1-C3 | 1→2 | 0.470 | 14.10 | 15 | +0.90 | +0.90 |
| F1-C3 | 2→3 | 1.120 | 33.60 | 33 | -0.60 | +0.30 |
| F1-C3 | 3→4 | 1.140 | 34.20 | 34 | -0.20 | +0.10 |
| F1-C3 | 4→5 | 0.805 | 24.15 | 25 | +0.85 | +0.95 |
| F1-C4 | 1→2 | 1.515 | 45.45 | 46 | +0.55 | +0.55 |
| F1-C4 | 2→3 | 0.705 | 21.15 | 21 | -0.15 | +0.40 |
| F1-C4 | 3→4 | 0.740 | 22.20 | 22 | -0.20 | +0.20 |
| F1-C4 | 4→5 | 1.155 | 34.65 | 35 | +0.35 | +0.55 |
| F2-C1 | 1→2 | 0.280 | 8.40 | 8 | -0.40 | -0.40 |
| F2-C1 | 2→3 | 0.290 | 8.70 | 9 | +0.30 | -0.10 |
| F2-C1 | 3→4 | 0.265 | 7.95 | 8 | +0.05 | -0.05 |
| F2-C1 | 4→5 | 0.285 | 8.55 | 9 | +0.45 | +0.40 |
| F2-C1 | 5→6 | 0.310 | 9.30 | 9 | -0.30 | +0.10 |
| F2-C1 | 6→7 | 0.830 | 24.90 | 25 | +0.10 | +0.20 |
| F2-C2 | 1→2 | 0.880 | 26.40 | 27 | +0.60 | +0.60 |
| F2-C2 | 2→3 | 0.210 | 6.30 | 6 | -0.30 | +0.30 |
| F2-C2 | 3→4 | 1.120 | 33.60 | 34 | +0.40 | +0.70 |
| F2-C2 | 4→5 | 0.290 | 8.70 | 8 | -0.70 | +0.00 |
| F2-C2 | 5→6 | 0.285 | 8.55 | 9 | +0.45 | +0.45 |
| F2-C2 | 6→7 | 0.300 | 9.00 | 9 | +0.00 | +0.45 |
| F2-C3 | 1→2 | 0.655 | 19.65 | 20 | +0.35 | +0.35 |
| F2-C3 | 2→3 | 0.205 | 6.15 | 6 | -0.15 | +0.20 |
| F2-C3 | 3→4 | 0.840 | 25.20 | 25 | -0.20 | +0.00 |
| F2-C3 | 4→5 | 0.625 | 18.75 | 19 | +0.25 | +0.25 |
| F2-C3 | 5→6 | 0.215 | 6.45 | 7 | +0.55 | +0.80 |
| F2-C3 | 6→7 | 0.820 | 24.60 | 24 | -0.60 | +0.20 |
| F2-C3 | 7→8 | 0.315 | 9.45 | 10 | +0.55 | +0.75 |
| F2-C3 | 8→9 | 0.340 | 10.20 | 10 | -0.20 | +0.55 |
| F2-C4 | 1→2 | 0.880 | 26.40 | 27 | +0.60 | +0.60 |
| F2-C4 | 2→3 | 0.790 | 23.70 | 24 | +0.30 | +0.90 |
| F2-C4 | 3→4 | 0.210 | 6.30 | 6 | -0.30 | +0.60 |
| F2-C4 | 4→5 | 1.015 | 30.45 | 30 | -0.45 | +0.15 |

Peor error por par 1.00 tick, acumulado ≤1.00 tick; ninguna tasa fuera de rango. La más rápida: 2.28× entre los dos cortes de una B separados 0.205 s.
Selección: [PROVISIONAL] 40 % de los inicios de ataque nativos se convierten en combo, 25/25/25/25 entre los cuatro de la fase; [PROVISIONAL] 120 ticks sin combo tras uno. Los parries no cortan combos; ruptura, cambio de fase, derrota, Link lejos (>700 en un límite de movimiento), evento o watchdog sí (AT apagado y tasa 1 al cancelar).

### 6. Pasividad
Guardia **real** (`checkPlayerGuard` virtual de Link) mantenida 38 ticks o sin escudo 75 ticks, contando solo procedimientos pasivos; ataques/parry/esquivas reinician; guard slip, guard break y daño congelan; mientras el Darknut ataca no se cuenta (leer un ataque no es pasividad). En rango (220/230) y de frente: F1 golpe de escudo (solo si el escudo sigue entero), F2 patada; [PROVISIONAL] enfriamiento 240 ticks. Al terminar se corta el encadenamiento nativo (escudo→maza, patada→ataque).

### 7. DKR01 + FIX02
`res/darknut/resurrection_A_agil_natural_FIX02.bck`: 45 024 B, SHA-256 `f96356fb6096f1ced7db8e6e3b4d21b39f9c4ea6b7a30de0cd46b1f2a2321524`, CRC-32 `f92a19f6`, J3D1/bck1/ANK1, bucle 0, 88 fotogramas (2.933 s), 29 articulaciones (= `tn2.bmd`). Única carpeta/archivo final (ver `ARCHIVOS_Y_SHA256_FIX02.txt`). FIX01 ya no se empaqueta. Toda la lógica DKR01 (Finish, temporizador 300, watchdog, una resurrección, segunda muerte nativa, descarga) intacta; durante caída/derribo/Finish/levantamiento DKN01 no hace nada (sin combos, parry, postura, IA ni barra).

## Escritores nativos (13, `DKN_NOINLINE`, auditados)
`dkn_native_threshold`, `_action`, `_armor`, `_clip`, `_wait_clip`, `_rate`, `_at`, `_spl`, `_stagger_hold`, `_guard`, `_attack_flags`, `_motion`, `_timer1`. Nunca: Link, `field_0x6fc`, `l_HIO`, interruptores, banderas de derribo, borrados, `HOOK_SKIP_ORIGINAL`.

## HUD
El tracker de Enemy Health Bars no presenta `B_TN` (perfil 531 = minijefe del catálogo): la barra de postura del Darknut usa 4 ranuras propias (bajo las de Lizalfos y Chilfos) con ancla calculada sobre la cabeza del actor; muestra la fracción de 120/130 en la barra 0..100 existente. Las demás barras no cambian. No hay barra de vida propia: HP/resistencia van a los logs.

## Pruebas automáticas (evidencia local + CI)
- `dkn_lab` (690 comprobaciones): tablas, sumas exactas por combo (51/33/51/51/65/69/91/55 y 118/78/118/118/95/117/163/108; F2-C3 satura a Link en el impacto 7), ritmo, postura, bandas, armadura con el modelo nativo de `setBreakPart`, ruptura, pasividad, selección, ledger.
- `test_dkn_mutations.py`: 45/45 mutantes detectados (local g++).
- `dkn_audit.py` (12/12 negativos), `dkn_native_audit.py` (64 hechos), cadena de auditorías previa intacta; `dkr_lab`/`dkr_world_lab` con los bytes FIX02; 50/50 mutantes DKR01.

## Límites conocidos (honestos)
- Nada probado en juego. La correspondencia A=lateral (0x05) / B=vertical (0x06) es la elegida por el usuario y **está pendiente de su verificación visual**.
- Los fotogramas de impacto son de cinemática + sonidos nativos; el "punto de corte" de B1 (f20) está respaldado por datos, pero su aspecto final requiere la prueba humana.
- No hay laboratorio "world" del adaptador DKN01 contra una transcripción nativa (sí lo hay del núcleo); la lógica del adaptador se valida por auditoría de fuente y por la compilación MSVC.
- Los efectos de parry naranjas de FIX03/FIX05 (pfx) no se extienden al Darknut: se ve la chispa/sonido nativos del escudo.
- Valores [PROVISIONAL]: 40 % combos, 120 ticks entre combos, 240 ticks de enfriamiento de pasividad, 45 ticks de guardia tras la ruptura.
