# Implementación CP05 FIX02 — 0.11.10

[Descargar artifact privado 13338164623](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41856406121/artifacts/13338164623) · [CI 41856406121](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/41856406121)

`LIGHT_FADES_TWICE_CP05_FIX02_0_11_10_PRIVATE_TEST_windows-amd64_d6e4c2179c2c.dusk`

**169147 bytes** · ID `dev.posture.post05_selective_reactions` · **0.11.10** · Windows x64 / DX12 / PRIVATE TEST.

SHA-256 del `.dusk`: `9c8f0074962386d7f46984cab43c0cff8fb429911d731e846aa52bef44e4bb4f`.

SHA-256 DLL interna: `5d9fef1e46e9e18fb5c4a49acc4c26758078909bdb7343e1005a5b19cfc45049`.

Caducidad informada por GitHub: **2026-12-04 10:38:41 Panamá (UTC−5)** (`2026-12-04T15:38:41Z`). Guardar el `.dusk` antes de caducar.

Fuente compilada `d6e4c2179c2c42a7aa807ce862290de728abb396`, árbol `47562231f0dc9c05075ef784cb064a7dd233c6f9`; commit CI `6f7ef784cde3cd1ee17511af863eaf5614aca9b0`. Este informe pertenece a un commit documental posterior y separado: su SHA se consulta en el historial de la rama; no se atribuye al binario. Base compilada FIX01 `785f7044a09588ea9f570f09b4b74580e4f7ee93`, no su commit documental `cf1cf30eacf2bee7db37bd03bd49f82c6d6d57b7`.

Jobs **build SUCCESS** e **independent-download SUCCESS**, mismo run. Paquete descargado de nuevo en esta sesión: CRC, SHA, DLL, manifiesto, fuente y PE coinciden. No se ejecutó el juego ni se cargó la DLL.


## P0-A: por qué cinco golpes escapaban al anti-tambaleo

En0.11.9 `lnks1fix::continuation` rechaza rate0 en Attack1/2/3. Ese rechazo incluye finales legítimos: `isStop` nativo es estado detenido o rate0; Attack puede terminar B/C o recoil con rate0 y elegir su salida normal. La nueva prueba no cambia ese gate compartido: concede una continuación de sidecar solo alrededor de la transacción POST05 existente, restablece el gate original antes de POST08 y deja sus compare-before-write/readbacks intactos.

Exige actor/slot/generación vivos y ABI válido, origen Link/espada ordinaria confirmada/no letal, snapshot PRE/POST del mismo callback sin cambio de animación, lectura actual idéntica, BCK5 o6 exclusivo, atributo0, isStop yrate0, end42/47 y extremo correspondiente. Tolerancia0.01frame: J3D clampa el final aend−0.001 en la revisión auténtica. No acepta rate0 a mitad, recoil positivo detenido, otro BCK, recepción vieja, pausa/evento, otra generación o escritor. No cambia HP, skips globales ni relojes ajenos.

Cinco decisiones reales de `dusklight-20261104-081302.log`:

| actor/gen/event | variante | PRE → POST nativo | frame/rate | HP | postura | ruta |
|---|---|---|---|---|---|---|
| 812/27/29 | RED | 4/3 → 5/0 | 0.00/0.00 | 330>290 | 54>71 | Recoil terminado |
| 813/28/37 | RED | 4/1 → 5/0 | 42.00/0.00 | 330>290 | 0>17 | Final B |
| 826/23/59 | RED | 4/3 → 5/0 | 0.00/0.00 | 330>290 | 27>44 | Recoil terminado |
| 1168/40/181 | BLACK_FURY | 4/2 → 5/0 | 47.00/0.00 | 335>295 | 0>13 | Final C |
| 2411/84/282 | RED | 4/3 → 5/0 | 0.00/0.00 | 295>255 | 44>61 | Recoil terminado |

Las cinco son SKIP_UNSAFE del log0.11.9, no cinco capturas visuales aisladas. El evento1168 es **Black furia ATP6**, no Red. En el laboratorio de fuente real se reproduce la exclusión vieja y FIX02 conserva HP/postura y permite la salida nativa segura sin Damage prematuro en las cinco familias de extremo. Para813 el logCP05PRE7538 da BCK5/end42/frame41.999; para1168 BCK6/end47 se infiere de estado2/gate, no lectura directa; en los tres recoil no quedaron BCK/end originales en log. Se ensayan B/C autenticados, sin certificar que se reconstruyó cada pose histórica. Producción siempre lee BCK/end/isStop reales y falla cerrada si no coinciden. Los POST03 históricos registran origin=UNDETERMINED; el laboratorio modela el origen Link de la observación humana y no lo presenta como un recibo de origen capturado en esos logs.

## P0-B: transición y control causal

Attack arma AT en frames14..22. Un contacto de la pasada de colisión a22 puede leerse en el siguiente Execute a23 (Blue23.5 con rate1.5). Al seguir Link guardando, Attack lo consume y pasa a recoil Attack3/−1, cuando AT ya se desactivó. `cc_set` registra sus objetos, pero `cCcS::Set` solo incorpora a la lista AT los que tienen AtSet. `ClrAtHitInf` limpia solo esa lista. El contacto de Link queda almacenado; tras recoil/Find, el siguiente ataque lo vuelve a leer alrededor deframe1, antes de alcanzar14 y limpiarlo. Repetir R sostenido produce rebotes prematuros y ninguna ventana AT nueva. Soltar R deja avanzar hasta14 y limpiar.

La limpieza emparejada de FIX01 ya cubría supresión/parry/ruptura, pero no todos los contactos frescos, incluido guard normal. FIX02 solicita ese mismo lease tras un contacto fresco y verificado, únicamente para el actor/token propios. Durante su `cc_set` se añade temporalmente AtSet a las esferas pendientes de limpieza y se restaura exactamente antes de la pasada global. El motor ejecuta su limpieza; `ChkAtTg` comprueba el bit ya apagado antes de colisionar. No escribimos flags de hit, no abrimos un golpe inactivo y no fabricamos contacto/parry. La validación ABI existente se inicializa también en el primer guard normal, sin depender de haber recibido antes una espada; mismatch cierra la ruta.

El log07:46 registra Red248/gen8 NormalGuard a23 (8206), luego repetidos4/3/frame1 conR=1 (8261..8475), REPEATED_ABORTS8422 y recuperación posterior guard0(8597/8614). Blue242/gen2 muestra contacto23.5(7326); el log08:13 Blue816/gen31 contacto23(8588). Son correlaciones compatibles. No identifican inequívocamente al Blue de la anécdota ni prueban que todo sospechoso sea por R; hay Fury guard0. El aislamiento causal procede de los controles de laboratorio con los mismos cuerpos nativos, distancia225, semilla/estado iguales y R cambiado a300: native+Expansion, CP04+Expansion y FIX01+Expansion reproducen el residual; FIX02 elimina ese bucle conservando pausas y ataques nativos. Resultados fila por fila en VALIDATION, no una certificación de la partida.

## Telemetría y coste

`ANTI_STAGGER` distingue prueba terminal demostrada/rechazada, gate concreto, motivo legado, aplicación real, HP/postura e identidad. `native_stop_proved` indica lo demostrado; no inventa isStop al rechazar. La línea antigua LNK_AI puede seguir mostrando la razón de su gate conservado: usar la nueva prueba explícita y el resultado POST05 conjuntamente.

`GUARD_AI` observa PRE/POST de cada Execute elegible y no solo impactos: identidad/generación/stage/room/layer/epoch, inputR fresco, estado/timers/frame/rate/BCK, target/rango disponibles, yaw relativo nativo, última tentativa/AT/contacto/parry y progreso. Son campos observables, no una API completa del target/pathfinder.64slots; límite240 detalles+reserva32 críticos,8por actor ordinarios,96 recibos de contacto y96 reacciones, contadores dropped. Los contadores identity_attempts/identity_AT_samples, transiciones y progreso son acumulados por identidad, no deltas de un único episodio de R. Resúmenes periódicos cada1800ticks y SHUTDOWN fuera del presupuesto; expiración por culling se marca inconclusa y no como recuperación. Duplicados no adelantan tiempo propio. No hay watchdog que fuerce ataques.

## Fuente auténtica, congelación y cobertura

SDK `40457c6adb381928e4b5fef6ed459ed291edd5e2`, Expansion `fe47c8b828939829914d466a425cb1e2c0223cd9`. Referencias de cuerpo nativo Set/ClrAtHitInf verificadas contra SDK; también Damage/Attack/Find/offTg/SetAction/cc_set de suites heredadas. Se ejecutan terminal_proof y contact_cleanup de producción, POST05 real, Parry/ArmTrack y lease; no se reescriben como una máquina ideal. I/O, J3D/poses, hojas de colisión, contactos de broadphase, Link y render se modelan. No se ejecutaron DLL, juego o pila real de ocho mods.

Cambios de producción: `src/mod.cpp` integraciones delimitadas; nuevos `cp05_fix02_core.hpp`, `cp05_fix02_monitor.hpp`, `cp05_fix02_adapter.inc`; lifecycle versión; `cp05_adapter.inc` solo7 etiquetas de versión. El resto son manifest/CMake/CI/pruebas. Todos los archivos cambiados y SHA-256 completos en EVIDENCE/COMPILED_FILES.json; ledger178, políticas34fuentes,107funciones/15headers y hashes en EVIDENCE/PRESERVATION.json. Inversión exacta de inserciones autorizadas, sin repinear cuerpos protegidos ni ampliar imports PE. Dos callbacks sobre target ya existente; cero targets y escritores nativos nuevos.

Se conservan Red50/50, rates[1,1.15,1.15,1], AT[68,46,72]; Black normal1/3 cada opción, Black8 rates[1,1,1.15,1.15,1.15,1.15,1.15,1],AT[65,67,46,46,46,46,70], Black7 rates[1.15,1.15,1,1,1,1,1],AT[46,68,70,56,56,56], RNG byte idéntico. Blue50/50 y2+2[1,1,1.5,1.5], shieldchain6ticks/buffer30, nuevo R+B por parry, POST08[-1,+7]/edad9; pesos Blue25/40/50,Red17/27/33,Black/Fury13/20/25, ruptura100, rearmes25/0, decisivo1.5, penalizaciónLink75, CP02regen, ManualShielding y HUD FIX03 intactos. No se arregla ni habilita parry de especialRedx2/12% o Blackfuria; sus multiplicadores/chip/prioridades no se alteran.

22 laboratorios/4,486,668 checks; 525mutaciones heredadas+25nuevas=550,0TIMEOUT; nuevos18negativos,20PE+6instrucciones. Detalle MSVC, controles y límites en VALIDATION.json. No suma doble de controles ni de114negativos ya contenidos en la suite heredada; los contadores de adaptadores se publican aparte.

Los dos logs se leyeron completos y se verificaron sus hashes. Las decisiones detalladas288/260 son subconjuntos limitados; no hay POST05_SHUTDOWN final. No se extrapola errors=0 ni se suman acumulados periódicos. EVIDENCE/HUMAN_LOG_EVIDENCE.json conserva números de línea y hechos derivados, sin logs crudos ni rutas del usuario.

Ambos P0 alcanzan las mismas etiquetas técnicas de RESULTS y quedan HUMAN_RUNTIME_PENDING. La matriz humana de README incluye ocho mods, R mantenido/soltado, multi-actor, espada/parry,100/Finish, sala/pausa y Link/HUD. No se afirma A/B real, FPS, sonido, chispa o movimiento físico de escudo desde fixtures. No PR/merge/tag/release.
