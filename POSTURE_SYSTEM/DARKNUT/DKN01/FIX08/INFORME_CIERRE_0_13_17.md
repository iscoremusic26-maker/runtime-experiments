# Informe de cierre — LIGHT FADES TWICE 0.13.17 — DKN01 FIX08

**Estado: AUTOMATED_PASS / HUMAN_RUNTIME_PENDING.** El juego no se abrió ni se jugó. No se midieron FPS ni latencia física de entrada. Nada de este informe afirma que algo se vea, se oiga o se sienta bien.

## 1. Entrega
- `LIGHT_FADES_TWICE_DARKNUT_MINIBOSS_FIX08_0_13_17_PRIVATE_TEST_windows-amd64_460429f68207.dusk` — 411 709 bytes — SHA-256 `c7f210cdaedb684adfb406a7356e79e8af88d1fa32cb509ed0178e2e8fdd7b4b`.
- WSL `/home/fran2607/dusklight_work/lft_0_13_17_dkn01_fix08_delivery/` · Windows `\\wsl$\Ubuntu\home\fran2607\dusklight_work\lft_0_13_17_dkn01_fix08_delivery\`.
- Artefacto: run 45960411116, artefacto 15182385339 (ZIP de 439 452 bytes, distinto del .dusk), caduca 2026-12-27T08:06:16Z: https://github.com/iscoremusic26-maker/windows-build-lab/actions/runs/45960411116/artifacts/15182385339
- DLL MSVC 1 804 288 bytes, `ffcfe95fb457edc0c4138ad6ffb8a2dd1554325a605d6b50cc552eb84946f749`. BCK FIX02 45 024 bytes, `f96356fb…2321524` (idéntico). mod.json 0.13.17, id sin cambios.

## 2. Fuente, CI y verificación
- Fuente compilada: `460429f68207b6588f2568eae2626131543c9f27` (rama `feature/light-fades-twice-darknut-miniboss-fix08-0-13-17`); commits posteriores solo documentales.
- FAST 45958431582 (CI `d0caa93`), INTEGRATION 45959054928 (CI `5b52fbc`), FULL 45960411116 (CI `cfc9aa3`): los tres PASS sobre el mismo SHA, ledger de 283 archivos. Ningún run fallido en FIX08.
- FULL: 16 jobs, 12 shards; **1755/1755 mutantes detectados** (DKN 360/360, de ellos 45 nuevos FIX08; Liz 239/239; Liz-world 202/202; Chilfos 210/210; DKR 67/67; LFT03 57/57; resto en `ci/CI_INVENTORY.json`). Labs completos PASS (dkn_lab 31 054 992 comprobaciones).
- Local además: 38 labs (g++), suites DKN/Liz/Liz-world/LFT03 de mutantes, auditorías dkn (113/113 negativos), dkr (13/13), kk, liz, source, tests de adaptador de producción (FIX08 nuevo: 12/12 mutantes; tinte de espada 6/6; FIX07 8/8).
- Contrato PE (MSVC): 129 imports del juego y HOOK_MEM 41, **idénticos a FIX07**; 0 destinos de hook nuevos, 0 imports nuevos (también tabla de imports idéntica en el build clang-cl local). Escritores DKN 23 → 25 (`dkn_native_neck`, `dkn_native_recover_clip`), `dkn_native_jump` acepta los saltos laterales nativos 11/14.
- Descarga independiente: `ARTIFACT_DOWNLOADED_VERIFIED` en CI y en local (`ci/download-verification.json`); 6/6 paquetes manipulados rechazados (versión, BCK, traversal, import desconocido, …: `ci/download_negatives.json`).
- Rollbacks 0.13.16 / 0.13.15 / 0.13.14 / 0.13.13 verificados intactos (ver MANIFEST). Ninguna rama ajena, `main`, tag ni release tocados.
- Disco: solo una carpeta de entrega (~640 KB); temporales de la sesión limpiados.

## 3. Los diez puntos
| # | Síntoma / evidencia | Causa | Cambio | Pruebas | Pendiente |
|---|---|---|---|---|---|
| 1 Helm F1 | Darknut «mirando a la nada» tras Helm (5 casos en el log, recuperación 30-33 t) | **Demostrada en el rig**: TNA_DAMAGE_R gira la cabeza -120° (frames 6-18); el contacto cae en 8,6-12; el cuello nativo no se activa en mType 1 y el cuerpo no gira hasta ChaseH | Cuello nativo tras 6 t, giro del cuerpo a velocidad nativa ChaseH desde el frame 24, cola 20 t, flag OFF al final; solo Helm F1 no letal | lab (giro sin snap, ±180°, máquina de estados), adaptador (fin limpio), auditoría | Verlo |
| 2 Postura F1 | aprobado | — | 24/36, 31/43, 50/60; nada más | lab (6 valores, resto igual, saturación), mutantes | Sensación |
| 3 x2 | 8 golpes potenciados en el log (2→3 ×5, 1→2 ×3) | — | `extra = D` (2D); mismo alcance y gates, 75 t | liz/liz-world labs (1→2…8→16), mutantes | Verlo |
| 4 Evasión | — | FIX07 dejaba correr las evasiones nativas sin control (10 releases con el Darknut en salto nativo) | 0/10/15/20 % tras la tirada de parry, 90 t, saltos nativos 11/14/6 con trayectoria leída; nativas 6/11/14 devueltas | lab (100 000 tiradas: 0/10,02/15,01/20,14 %), geometría con terreno doble, mutantes | Frecuencia, bordes |
| 5 Espada | 4 muertes, tinte escrito pero no visible | **Demostrada**: material más claro saturado en el clamp TEV; mismo C0 oscurece 2,6× menos; F3 Finish llega solo a -13,5 | C0 perceptual (`kSwordTint`), al compás del cuerpo; **solo Darknut** | test de adaptador con el orden nativo de draw (6/6 mutantes), lab (monótono, tope -100) | Verlo (Finish F3 y HP 0) |
| 6 FX parry | 421/421 transacciones completas; usuario ve fallos | Defecto de ruta demostrado: un 2.º `startCollisionSE` del mismo id+map en el mismo tick silenciaba el choque agudo sin rastro | Re-pitch único si es el mismo propietario; edades de corte completas; ledger por ruta | test de fuente LFT03 + negativos, liz-world mutantes | **Percepción sin demostrar**: imagen y sonido son prueba humana |
| 7 Iniciativa | tick 14602: combo sobre un FINISH_STAB vivo tras salto nativo | Evasión nativa + iniciativa sobre tajo activo; 34/34 counters sí tenían token | Sin evasiones nativas; `swing_threat`; recibo DEFENSA→NEUTRAL→INICIATIVA; intento nativo sin bypass | lab (caso 14602, gate), adaptador, auditoría, mutantes | Sensación |
| 8 F1-C3 | primer vertical «aparece en el suelo» | Mezcla de 10 frames con solo 4 de preparación (FIX07) | 36/56/57/40; par 1: corte 61, inicio 16, morph 8, ×1,50; sin excepción 1,76 | lab (36 exactos, total 189), simulación FK del morph | Verlo |
| 9 B1 | 18 B1_RECOVERY | **Medida**: morph 10 a TNB_WAIT = barrido a 120-156 u/t (velocidad de corte) y 30 t quieto | Morph nativo suavizado -20 a TNB_WAIT_B_2, espera 18 | lab, contrato de adaptador, mutantes | Verlo |
| 10 Auditoría | ver §4 | | | | |

Valores efectivos: postura F1 sobre Link 24/36, 31/43, 50/60; maza lanzada 50/60/0/0; daño en penalización 2D (75 t); evasión 0/10/15/20 % condicionada a que el parry no se armara, denominador = tajos elegibles por ordinal, enfriamiento 90 t entre inicios; F1-C3 36/56/57/40 (6,30 s, simulado exacto); B1: recuperación suavizada de 16 t + 2 t de guardia (antes 10 t de barrido + 30 t quieto). **Ninguna desviación de los valores aprobados.**

## 4. Auditoría adicional
- Corregidos: evasiones nativas sin control (fuente del «contraataque» sin parry); iniciativa sobre tajo vivo; intento nativo que saltaba el estado neutral; corte mismo-tick del choque agudo; presupuesto de log DKN casi lleno (6000 → 9000, líneas nuevas muestreadas).
- Investigado y mantenido: LNK05 `EXPIRED` (tick 72307): la saturación llegó con Link en Shield Attack (origen no permitido por diseño en la ventana de 3 t); la postura quedó a 100 y regeneró sin ruptura. Es la puerta de seguridad; cambiarla es decisión de diseño (futuro). 12 ejecuciones F1 / 11 recuperaciones: la 12.ª es letal (transformación), correcto. 3 cancelaciones de salto ofensivo: las tres Link > 700, legítimas.
- No probado / riesgos residuales: percepción de FX y sonido; evasión cerca de geometría compleja real (la lectura de trayectoria usa las consultas nativas, validadas solo con dobles); el seguimiento de cuello en F1 Helm Splitter con Link detrás (se limita a ±67° nativos); Mortal Draw F1 usa TNA_DAMAGE_L, cuya cabeza también gira (+110°): no tocado para preservar Mortal Draw (anotado como posible mejora futura).
- Rendimiento: sin benchmark de juego. Costes nuevos acotados: geometría de evasión solo en una tirada ganada (≤ 1 cada 90 t; 3 arcos × 7 consultas), comprobaciones por tick O(1), seguimiento de audio 4 pistas por choque. Ninguna asignación ni escaneo global nuevo.
- Otros enemigos: sin cambios de comportamiento salvo el x2 general de la penalización de Link (aprobado) y el re-pitch del choque de parry en un caso de reinicio en el mismo tick. **Ningún oscurecimiento de armas fuera del Darknut.**

## 5. Prueba humana
`README_TEST_0_13_17.md` (sesión A aislada, sesión B con mods habituales). Mantén 0.13.16 como rollback y no cargues dos LFT a la vez.
