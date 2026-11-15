# LIGHT FADES TWICE 0.13.11 — DARKNUT MINIBOSS DKN01 FIX02

Estado: **HUMAN_RUNTIME_PENDING**. Compila, pasa laboratorios, mutantes y auditorías; nadie lo ha jugado todavía.

## Base
- Fuente compilada de 0.13.10: `c1020a7f48eed36aa768a54137c637d6986ab0fa` (verificado: el nombre del `.dusk` 0.13.10 lleva `c1020a7f48ee`; la rama tenía después solo `8c0b8ad`, documentación CI de 11 líneas, incluida).
- Rama nueva `feature/light-fades-twice-darknut-miniboss-fix02-0-13-11` desde `8c0b8ad` (worktree `runtime-experiments-dkn-fix02`). CI: `ci/light-fades-twice-darknut-miniboss-fix02-0-13-11` desde `c1e42c1` (worktree `windows-build-lab-dkn-fix02`). Los worktrees de FIX01 no se tocaron.
- `mod.cpp` sin cambios; **0 objetivos de hook nuevos, 0 imports nuevos del juego** (DLL local frente a `ci/expected_pe.json`).

## P0 — Los tres crashes: causa raíz demostrada
Logs del usuario `dusklight-20261114-181434.log` (SHA-256 `a63849b0…c33c11`), `-181752.log` (`9e5b4d2b…6d1f`), `-182038.log` (`a1a9ae7d…a6dd`), todos con fuente `c1020a7f48ee`. Firma idéntica: `EXCEPTION_ACCESS_VIOLATION`, `Fault addr 0x20`, PC `dusklight.exe+0xcd1f86`, traza `0xcd1f86 ← 0xccee03 ← 0xcc311f ← mod.dll+0x7566f ← 0xcc8b57`.

Desensamblado del EXE exacto (2.0.3, SHA-256 `ffa99203…0049`, build 40457c6, base 0x140000000):
| Marco | Dirección | Función | Instrucción |
|---|---|---|---|
| #00 | `0x140cd1f86` | `daB_TN_c::getCutType` (`0x140cd1f70`) | `mov rax,[rcx+0x5ba8]` (`mAtInfo.mpCollider`); `test byte [rax+0x20],2` = `ChkAtType(AT_TYPE_NORMAL_SWORD)` **sin comprobar NULL** |
| #01 | `0x140ccee03` | `executeGuardL` (`0x140cced40`), rama modo 0 | `test ecx,ecx; jne` → `mov byte [rbx+0xd21],1` (field_0xa91) → `call getCutType` |
| #02 | `0x140cc311f` | `action()`, caso `ACT_GUARDL` | `call 0x1400819fd` (thunk de executeGuardL) |
| #03 | `mod.dll+0x7566f` | trampolín de nuestro hook de `action` | — |
| #04 | `0x140cc8b57` | `execute` → `action` | — |

`damage_check` escribe `mAtInfo.mpCollider = NULL` (`0x140cc7913`, `0x140cc7ad3/7d39`) cuando ninguna esfera recibió golpe. El nativo solo entra en `ACT_GUARDL 0` desde `damage_check` **con** colisionador (todos los `setActionMode(ACT_GUARDL,0)` del EXE están en `damage_check`, comprobado). La guardia adaptativa de FIX01 escribía `ACT_GUARDL 0` en el PRE de `action` **sin golpe** → mismo tick: colisionador NULL → lectura en 0x20.
Corroboración: en las tres sesiones hay **0** líneas `DARKNUT_ADAPTIVE_GUARD`, pese a una probabilidad ≥ 20 % por tajo nuevo de Link de frente: cada guardia adaptativa derribaba el juego en el mismo tick, antes de vaciarse el búfer del log (el último log acaba truncado a mitad de línea). Los contextos (fin de F2-C1/C2, Shield Attack, reentrada) son el estado libre en el que la guardia podía activarse. No hay relación con RAM, DirectX ni otros mods.

Corrección (causa raíz, no ocultación):
- `dkn_native_guard_enter`: entra en la guardia en **modo 1** con su propio clip `TNB_GUARD_A/B` (elegido como lo haría `getCutType`, pero leyendo el tipo de corte de **Link**), AT apagado, `field_0xa91`, giro acotado 0x2000 — exactamente lo que hace el modo 0 nativo, sin leer el colisionador. También se usa para el antiguo YOROKE→guardia.
- Invariante en el propio escritor `dkn_native_action`: nunca escribe un `(acción, modo)` que necesite el colisionador de la pasada (`native::needs_hit_context`; hoy `ACT_GUARDL 0`); se convierte en persecución neutral y se cuenta.
- Toda restauración de instantáneas pasa por `dkn_restore` (misma invariante, `INVARIANT_HIT_CONTEXT_ENTRY_REFUSED`).
- `dkn_native_neutral` además apaga el AT de espada y de patada.
- Auditoría: prohíbe el literal `kActGuardL, 0`, exige la invariante en el escritor y el modo 1 en la entrada; negativos que reintroducen el fallo son rechazados. Evidencia: `crash_disassembly.txt` (carpeta de entrega).

## P1 — Empuje de Link al bloquear
`procGuardSlipInit` (d_a_alink_guard.inc) da `mNormalSpeed = mGuardSpeedLarge = 20` con spl 1 (el del Darknut desde 0.13.9) y `procGuardSlip` frena 1,25/tick: ~160 unidades por cada impacto bloqueado. FIX02 no cambia el spl ni la física general de Link: cuando un contacto de **este** Darknut en el escudo de Link provoca el deslizamiento, su velocidad se **limita** (nunca se sube) en el POST de `checkDamageAction` de Link (o en el PRE de `damage_check` del Darknut si Link ya se deslizaba): maza 15 (~90 u), escudo/patada 16 (~102 u), espada 13 (~68 u) [PROVISIONAL]. Se conservan animación, sonido, vibración, postura, el golpe directo grande y la rotura de guardia a 100. Log `LINK_SLIP_CAPPED` (velocidad nativa/limitada, deslizamiento, separación XZ; con tope).

## P1 — Lizalfos
- El paso de aproximación del wind-up avanzaba 12/tick a lo largo de su **rumbo** (`current.angle.y`, aún girando): ahora va hacia Link (`search_angle_y`).
- Gobernador de distancia: este tick nunca acerca al Lizalfos a Link por debajo de **110 XZ** [PROVISIONAL] (esferas 45-70 + cilindro de Link): primero se recorta el paso propio y la compensación de embestida; si la embestida nativa sola (D2 25/tick por `current.angle.y`, cola 30/tick hacia Link, ventanas 25-30 / 33-41) cruzaría ese límite, se frena como máximo hasta anularla (nunca tira hacia atrás). Tasas, fotogramas, ventanas y patrones intactos. Log `LIZ_SUMMARY part=FIX02_DISTANCE`.
- Integración por hunks inversos exactos contados (`ci/kk_policy.json`, etiqueta `fix02_0_13_11`).

## P1 — 46 impactos parryables (y golpes sueltos/contraataques)
`tests/dkn_lab.cpp` simula el modelo de reproducción del adaptador tick a tick y, por impacto, cuenta los ticks con el AT encendido (el AT se decide en el POST de `action`, tras `play()`), comprueba que el fotograma de impacto cae dentro de la ventana abierta y que cada impacto tiene su **propio ticket** (la ventana se cierra antes del siguiente del mismo movimiento): **46/46** en los combos (F1: 5/3/5/5, F2-F3: 7/7/9/5), mínimo **5 ticks** por impacto (también los golpes sueltos y contraataques: estocada 7, doble 8+17, mazazos 8-11). Patada y golpe de escudo: ventanas nativas de 4 ticks a velocidad 1. Los ritmos no cambian: huella numérica de todos los planes = **145463.5789**, idéntica a la calculada con el `dkn_core.hpp` de c1020a7.

## P1 — Ofensiva solo del controlador
- Además de las entradas de ataque nativas (0.13.10), el **salto de aproximación** nativo (`ChaseL` 8/17, termina en ataque) se convierte en el paso nativo (`TNB_WALK`, modo 3): `NATIVE_LEAP_SUPPRESSED`. Los saltos evasivos (6, 10/11/13/14) siguen siendo nativos.
- Auditoría en cada `action` POST: una acción de ataque sin arriendo (combo/single/counter/special) es un fallo de integración: `UNAUTHORIZED_NATIVE_ATTACK` (contado, neutralizado). Los logs 0.13.10 no muestran ninguna; los arranques `NATIVE_ATTEMPT_TAKEN` eran planes propios.

## P1 — Levantamiento con FIX02
El levantamiento tras 6 s sin Finish **reproduce el BCK FIX02** (mismos bytes `f96356fb…1524`, 88 f, 29 articulaciones; mismo escritor y mismo enlace que la resurrección: fotograma 0 = última pose de TN2B_DIE, fotograma 88 = TNB_WAIT 0). Animación compartida, lógica separada: misma resistencia, resurrección **no** consumida, misma fase; luego `ACT_CHASEL 2` con TNB_WAIT (fundido 3). Eliminada la reproducción invertida de TN2B_DIE (`dkr_native_getup_rate`). Descarga del mod durante el levantamiento: el clip sale del modelo antes de liberar su búfer (probado).
Ramas: (A) 6 s sin Finish con vida → FIX02 como levantamiento; (B) Finish F2 → FIX02 como resurrección (consume la única, F3 480/480, 0/180); (C) Finish F3 → muerte definitiva; F3 HP0 → muerte nativa; (D) resistencia 0 al vencer la espera → nunca levantamiento (F2 → resurrección, F3 → muerte).

## Evidencia automática local
`dkn_lab` 13 016 PASS · `dkr_world_lab` 5 007 PASS (incl. FIX02 como levantamiento, 88-90 ticks, 0 resurrecciones, clip enlazado una vez; descarga durante el levantamiento) · `liz_lab` 3 516 529+ PASS (gobernador) · `liz_world_lab` PASS · auditorías DKN (19 negativos)/DKR/kk/liz/fix03/lft03/source/store/mutant-anchors/native PASS. Mutantes y CI: ver registro CI.

## Límites honestos
- Sin prueba en el juego. La causa raíz del crash está demostrada por desensamblado + logs; que no queden **otros** crashes solo lo dirá tu prueba.
- No hay laboratorio "world" del adaptador DKN; el tope de deslizamiento de Link y el gobernador del Lizalfos se prueban en núcleo/lab, no con física real (paredes, escaleras, alturas): pendiente humano.
- Valores [PROVISIONAL]: topes 15/16/13, separación mínima 110 del Lizalfos.
