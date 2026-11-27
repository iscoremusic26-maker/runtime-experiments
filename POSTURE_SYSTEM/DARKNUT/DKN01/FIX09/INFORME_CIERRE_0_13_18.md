# Informe de cierre — LIGHT FADES TWICE 0.13.18 — DKN01 FIX09

**Estado: AUTOMATED_PASS / HUMAN_RUNTIME_PENDING.** FAST, INTEGRATION y FULL pasaron sobre el mismo SHA y el artefacto se verificó por descarga independiente. El juego no se abrió ni se jugó; no se midieron FPS. Nada aquí afirma que algo se vea, se oiga o se sienta bien, ni que no queden exploits.

## 1. Entrega
- `LIGHT_FADES_TWICE_DARKNUT_MINIBOSS_FIX09_0_13_18_PRIVATE_TEST_windows-amd64_3221981c18f3.dusk` — 419 376 bytes — SHA-256 `b3d54656df1910c67ead20cd5e593d6be01057302840e008ba8620dc0bf97ff7`.
- WSL `/home/fran2607/dusklight_work/lft_0_13_18_dkn01_fix09_delivery/` · Windows `\\wsl$\Ubuntu\home\fran2607\dusklight_work\lft_0_13_18_dkn01_fix09_delivery\`.
- Artefacto: run 46024705027, artefacto 15213961576 (ZIP 448 574 bytes, distinto del .dusk), caduca 2026-12-27T15:59:03Z: https://github.com/iscoremusic26-maker/windows-build-lab/actions/runs/46024705027/artifacts/15213961576
- DLL MSVC 1 825 792 bytes `10651faa882ee068347ab3ccd6de39a45f62f82e2b2c62240f374d324b18b8e4`; BCK FIX02 45 024 bytes `f96356fb…2321524` (idéntico); mod.json 0.13.18, id sin cambios.

## 2. Fuente, CI y verificación
- Fuente compilada `3221981c18f3bcf00d18d78d34e94b1f3ecc8a33` (rama `feature/light-fades-twice-darknut-miniboss-fix09-0-13-18`, base FIX08 `460429f6`; los commits FIX08 posteriores eran solo docs). Commits posteriores a `3221981c`: solo documentación.
- FAST 46022040170, INTEGRATION 46022901980, FULL 46024705027: PASS, mismo SHA, ledger de 285 archivos. FULL: 16 jobs (12 shards), finalize y descarga independiente PASS.
- **Intentos fallidos (registrados, no ocultos)**: FAST 46015452979 (fuente `2ae1c27d`): el pin PE detectó un import CRT nuevo (`strcmp`, de un `std::strcmp` de un log); los 129 imports del juego eran idénticos; corregido sin cambiar el pin y con regla de auditoría + negativo. FULL 46019495657 (fuente `7b396251`): shard `dkn` falló por `PermissionError WinError 32` al limpiar un temporal (bloqueo de Windows sobre `dkn_lab.exe` recién terminado, sin timeout); se endureció la limpieza (`ignore_cleanup_errors=True`, la detección no cambia) y se repitió la cadena completa sobre el SHA final.
- **Mutantes FULL 1803/1803** (DKN 408/408 = 360 FIX08 + 48 FIX09; rework 393/393; Liz 239/239; Chilfos 210/210; Liz-world 202/202; DKR 67/67; LFT03 57/57; resto en `ci/CI_INVENTORY.json`); 0 supervivientes, 0 timeouts. Local además: suite DKN completa 408/408, laboratorio DKN 31 059 154 comprobaciones, prueba de adaptador FIX09 26/26 mutantes, FIX08 12/12, FIX07 8/8, LDG 7/7, espada 6/6, transformación 4/4, auditoría DKN 132/132 negativos, DKR 13/13, contrato nativo 222 hechos, anclas de mutantes 1234.
- PE (MSVC): 129 imports del juego y HOOK_MEM 41, **idénticos a FIX08**; 0 destinos de hook nuevos, 0 imports nuevos. Escritores DKN 25 → 28. Ningún archivo compartido modificado.
- Descarga independiente: `ARTIFACT_DOWNLOADED_VERIFIED` en CI y en local; 6/6 paquetes manipulados rechazados (versión, BCK, traversal, import desconocido, miembro extra, hooks declarados). La copia local coincide byte a byte con la descarga.
- Rollbacks 0.13.17 / .16 / .15 / .14 / .13 verificados intactos (MANIFEST). Ninguna rama ajena, `main`, tag ni release tocados.

## 3. Los nueve bloques
| # | Observación | Causa | Cambio | Pruebas | Pendiente humano |
|---|---|---|---|---|---|
| 1 Salto que no daña | "golpea sin quitar vida" | **Demostrada en código nativo**: entradas evasivas nativas 11/14 dejan `mTimer7=10` (10 pasos sin esferas corporales) que FIX08 no revertía (20 casos; 7 con tajo de Link dentro, 0 daño). **Segunda**: en F2/F3 el bloqueo nativo de cortes fuertes (el salto es spl 1) no comprueba el frente | Entrada devuelta en el POST del mismo `action()` antes de `cc_set` con `mTimer7` previo restaurado; guardia F2/F3 solo de frente (±0x3000) | lab, adaptador (restauración, salto propio intacto, 10/13 nativos), auditoría, contrato nativo | Verlo en juego; no se identificó en el log cada salto fallido concreto |
| 2-3 Choque en esquiva, i-frames | tick 13064 | **Demostrada**: `field_0xa91` sigue activo en los saltos (14 bloqueos con lease EVADE) | Sin guardia en toda la evasión/salto aéreo/reposición; i-frames 6/6/6 desde el despegue nativo, ticks ejecutados, sin re-armado, en `ChkAtTgHitAfterCross` solo para Link→este Darknut | bordes −1/0/5/6, pausa, cancelación, mismo tajo, nuevo tajo, spam 10 min | Sensación, bordes de mapa |
| 4-5 Fin tras daño | 14 golpes confirmados seguidos del resto del combo | Diseño FIX08 (protección total del combo) | Recibo de vida (DirectJoin) + instantánea de la oferta; barrera de ventana; doble: 2.º corte nunca; follow-through natural; motivo `LINK_HP_HIT`; sin 80/20; una decisión hold/atrás | rutas de los 14 planes (46 impactos), ambos órdenes de recibo, rechazo, ruptura, counter | Naturalidad visual de cada salida |
| 6 Cautela | — | — | R=min(H,Q) exacto, Tablas A/B aprobadas, preferencia atrás 170/195/220/245 [PROVISIONAL], enfriamiento común 90 | distribuciones 100 000 tiradas por celda, monotonía exhaustiva, sin RNG cuando no elegible | Frecuencia percibida |
| 7 Compatibilidad | — | **Defecto adicional**: flujo RNG de evasión FIX08 sin sembrar | Semillas por actor/generación (evasión, retirada); maniobras no encadenadas a reposición; espera de salto ofensivo tras retirada | spam, alternancia de bandas, retirada+evasión | — |
| 8 FX | azul + sin agudo en dobles | Texturas del usuario **descartadas** (hash verificado); render PC **descartado** (orden create→executeAfter→capture). **Demostrada**: clank `def_se_set(42)` sin agudizar del Shield Attack rechazado sobre el cuerpo en 68/342 parries. 37 dobles parry→bloqueo sin segundo Shield Attack = azul **correcto** | El Shield Attack rechazado no cruza en F2/F3 (Helm nativo); la evasión no produce choque; telemetría `DOUBLE_CUT2_BLOCKED_AFTER_PARRY` | lab, adaptador, auditoría | **Percepción sin demostrar**: ver y oír cada parry; anotar el corte |
| 9 Auditoría | ver §4 | | | | |

## 4. Auditoría adicional
- Corregidos: residuo `mTimer7`; bloqueo sin frente; guardia en el aire; clank del Shield Attack rechazado; RNG de evasión sin semilla; elección de movimiento al recibir tarde (instantánea en la oferta).
- Investigado y mantenido: 2 `LNK05 EXPIRED` (ticks 2982 y 21318): `kind=DIRECT` con Link en `PROC_LARGE_DAMAGE_UP`, puerta de seguridad diseñada. Etiquetas `guard_mul=3/2` y `decisive_bonus=x1.50` son la regeneración en guardia y la ejecución (se conservan); el castigo de Link instala y aplica ×2. 12 ofertas directas sin recibo de vida (sin fin de ofensiva, correcto). `mInvincibilityTimer` nativo (10 ticks tras un golpe) puede dejar sin daño un tajo nuevo muy rápido con marca de golpe: comportamiento nativo de todos los enemigos, no tocado. Esquivas nativas 10/13 (proyectiles) con `mTimer7` nativo: no tocadas. Si LDG01 no se instala, su desinstalación quita también el callback DKN (los i-frames del Darknut dejarían de aplicarse; sin otro efecto).
- No probado: imagen y sonido finales; geometría compleja real; varios Darknuts simultáneos en juego (probado solo con dobles); rendimiento (coste añadido: comparaciones de punteros por cruce, O(1) por tick, sin asignaciones).
- Otros enemigos: sin cambios.

## 5. Antiexploits cubiertos (pruebas reproducibles)
Spam de saltos/tajos (≤1 maniobra cada 90 ticks, exactamente 6 i-frames por maniobra, ≤12 en cualquier ventana de 90); una tirada por tajo aunque cambie la banda; sin RNG si no elegible; i-frames sin re-armado ni por reloj de pared; tajo persistente sin daño tardío y tajo nuevo con daño; absorber un golpe sin pérdida de vida no termina el combo; bloqueo/parry/esquiva no terminan el combo; retirada y evasión comparten enfriamiento; ruptura prevalece; decisión acotada (60 ticks) y bloqueo de iniciativa acotado (90). Pendiente humano: abuso en geometría real y con varios enemigos.

## 6. Prueba humana
`README_TEST_0_13_18.md` (sesión A aislada, sesión B con mods habituales). Mantén 0.13.17 como rollback y no cargues dos LFT a la vez.
