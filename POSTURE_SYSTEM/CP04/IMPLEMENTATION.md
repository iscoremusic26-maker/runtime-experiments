# LIGHT FADES TWICE · CP04 · 0.11.7 PRIVATE TEST

## Procedencia y alcance

Base ejecutable: `8c72aec291a7473f1752c702137229cc2224c998`, no el cierre documental `8c85097e0c805dcf630f6496d0d8b28b99f05550`. El usuario confirmó 0.11.6 con ocho mods. La nueva fuente y su binario se correlacionan en RESULTS.json tras terminar CI. No se ha ejecutado el juego ni la DLL en esta sesión. No hay prueba visual automatizada ni HUMAN_RUNTIME_PASS.

Motor/SDK oficial: `TwilitRealm/dusklight@40457c6adb381928e4b5fef6ed459ed291edd5e2`. EXE oficial leído estáticamente, nunca ejecutado: SHA-256 `ffa992038d04290654b8907a7663f4dcf62083beaad2b35014fdfd901d390049`.

Expansion histórico CP19 FIX02 tiene versión interna0.16.2. La referencia auténtica **0.17.0** es CP21 público, rama `feature/devf-cp21-public-package`, commit `fe47c8b828939829914d466a425cb1e2c0223cd9`, ruta `DEVF/CP21_PUBLIC_RELEASE/runtime/DEVF/CP19_FIX02_UNIVERSAL_AUDIO_BLACK_SHIELD_CHIP/expansion/`. GitHub confirma los blobs:

| Archivo | Git blob |
|---|---|
| mod.cpp0.17.0 | `85642911ab80e8bd6f90e32d818be2fa52595830` |
| blue_ai_policy.hpp | `8117432f2b3badb9670e9cdff515de74601ef651` |
| blue_recruit_policy.hpp | `ba9d38b0e134d8df8c5508af2a0b67500b60260c` |
| red_ai_policy.hpp | `bf6fa2a7d20b604983cb7b592b36e43196dbf189` |
| black_ai_policy.hpp | `8710e2dc9d655600f0c2a40bed5b20bccc66d158` |

Los cuatro encabezados de IA coinciden con el histórico CP19; el mod.cpp público añade la identificación tipada/packaging CP20/CP21. No se modificó ninguno de esos proyectos. Se incorpora **solo al laboratorio** una copia exacta de la política Blue, junto a las referencias CP21 ya existentes; no se enlaza a la DLL.

## Las dos dependencias de mayor riesgo

1. **Velocidad coexistente:** Expansion escribe una sola vez en execute POST, a frame1/rate1, para BCK5/6 Blue, y conserva20/17/15 de lockout. La API oficial `HookOptions` dice “Higher runs first … Applies to pre/post ordering”; hook.cpp ordena ambos tipos de callback en orden descendente. CP04 usa prioridad explícita−100, después del0 de Expansion, en E_OC execute PRE/POST. Ambos órdenes de registro se ensayan ejecutando los callbacks completos y la política auténtica de Expansion. No hay dependencia de qué mod se cargue primero.
2. **Escudo físico:** `procGuardAttackInit` llama a `commonProcInit(PROC_GUARD_ATTACK)`, `setSingleAnimeParam(ANM_SHIELD_ATTACK)`, voz nativa, reset de `mGuardAtCps`, radio/SE y las variables normales. El observador POST exige recurso real, fotograma inicial0..1, rate1, inicio1 y fin ofensivo12; el siguiente snapshot exige avance positivo de ese clip. Una bandera de procedimiento, el buffer o la pulsación por sí solos no conceden parry.

## Planificador Blue y propiedad

`cp04_combo_core.hpp` contiene64 sidecars por identidad/generación/stage/room/layer/epoch, sin punteros. `cp04_adapter.inc` es código de producción incluido una sola vez en mod.cpp y auditado explícitamente; no es un hueco en la barrera de escrituras.

La clasificación reutiliza exactamente LNK07/postbal01: recurso y potencia concordante de las dos esferas e historial de generación, sin heurística de HP. El actor debe estar vivo, admitido y sin postura rota/congelada. Solo un ATTACK/0 nativo que sobrevivió a damage_check/agua/caída y cuyo chaseF llega a cero genera una oportunidad. No se sortea mientras frena, está en WATCH3/SOUND_WATCH, o en callbacks repetidos. Las continuaciones nativas ATTACK/0 también son oportunidades válidas.

Un contador Weyl64 por actor, mezclado biyectivamente y separado por identidad/generación/contexto, usa el bit alto para una partición exactamente1/2 del espacio de estado. No toca `cM_rndF`. Es PRNG determinista, no una garantía de que la mitad de una muestra pequeña salga combo. Se distinguen oportunidades, seleccionados, normales, no iniciados, completados y cancelados. No hay cooldown adicional que sesgue oportunidades futuras.

Fases: Idle → Selected → Swing1 → Gap12 → Swing2 → Gap12 → Swing3 → Gap2 → Swing4 → Recovery → Idle. La selección normal no escribe nada. El original elige B/C, inicia voz y clip, activa sus esferas y mueve su root. Cada swing tiene token nuevo; las dos esferas siguen siendo un episodio. No se inserta daño, contacto, posición, orientación ni hitbox.

La entrega usa **1,00/1,00/1,50/1,50**. La velocidad se adquiere solo en el frame1 fresco, después de Expansion: se acepta el handoff1/1,15/1,30 documentado y se verifica la escritura. Un valor ajeno o pérdida de clip/estado cancela de forma conservadora; no hay escrituras continuas para pelear por la velocidad. Los cambios de grupo no retiman el clip. Al terminar el cuarto, el original y Find recuperan el lockout20/17/15. Si el original ya eligió Find/0, se conserva su `mOldActionMode`; no se repite la transición borrando ese dato.

No se corta ningún clip B/C por temporizador: se espera a `isStop()` y a la salida nativa a idle BCK28. El retroceso por bloqueo/parry sigue siendo **ATTACK/3, rate−1**, y se espera también su final. La pausa mínima empieza después de esa salida; no se promete la misma cadencia de contacto si el jugador fuerza el retroceso. Durante la pausa se utiliza Find y un temporizador propio de12/2 aplicado una vez, con una segunda adquisición delimitada tras la inicialización20 de Find/0. Al vencer la pausa se pide ATTACK/0 por `setActionMode`; si Link se apartó, Find puede haber acelerado/desplazado al Blue y el chaseF nativo requiere frenarlo. El plan espera esa frenada real, con tope32 ejecuciones, sin confundir la petición con un clip iniciado. El intervalo efectivo puede superar12/12/2 y se registra en NEXT_SWING_STARTED. No se escribe speedF para ocultarlo; el original vuelve a ejecutar primero daño, agua y caída. Una prioridad nativa o reclutamiento ya activo cancela.

Las pausas cuentan **ejecuciones efectivas del actor**, no tiempo real ni ticks ausentes por culling. Frames de presentación sin simulación no avanzan el plan. No se acumulan cuatro golpes al volver de culling/pausa. La pausa/evento cancela la secuencia futura.

A100, el aviso del parry cancela sincrónicamente el sidecar y cada entrada comprueba además el latch de postura. Nunca se restaura ATTACK después de una ruptura. Se conserva el handoff POST08→POST06 heredado de una llamada para limpiar correctamente el contacto; la colisión actual sigue siendo autoritativa. Esto no posterga el combo hasta el cuarto. Con ganancias40:40→80→100 impide su cuarto swing.

La liberación de velocidad significa cesar la propiedad/escrituras del plan. Una cancelación nunca rebobina un clip ajeno o una reacción nativa; el original resetea la tasa en su siguiente setBck. La tasa aplicada al espadazo ya iniciado puede persistir hasta su salida nativa; no contamina un ataque normal nuevo.

## Tiempos y assets: límites explícitos

`executeAttack` arma en14≤frame≤22; **22 no es el final del clip**. Producción lee `mFrameCtrl.getEnd()` del B/C realmente cargado, lo registra y espera su parada nativa. No se hardcodean longitudes42/47. No están montados los assets BCK del juego del usuario; **no se afirma haber medido sus longitudes reales**.42/47 en el shim y23..120 en el laboratorio son duraciones sintéticas para comprobar independencia del final; no son pruebas de assets.

x1,50 está acotado por la ruta real `checkFrame→checkPass`: B tiene cues10/12,5/19, C7/11,5; el salto1,50 no puede cruzar dos cues contiguos del mismo else-if. La prueba de callbacks compila el `executeAttack` oficial **sin cambiar su cuerpo**, ejecuta sus cues, root y cuatro ventanas AtSet contra I/O modelada, y compara timestamps de esas ventanas. No es una prueba de audio/partículas/colisión espacial en el juego. No se añade una reparación sonora conjetural. El root permanece nativo.

## Parry rápido general

`shield_chain_core.hpp` no conoce Blue, variantes ni combos. Un observador de setStickData, prioridad−100, lee **la pulsación nativa nueva** R+B en el snapshot propio estampado de LNK_FIX01: aquel callback ya la capturó antes del consumo contextual de B y procesó el rearme de R. Así no se pierde R+B justo en el tick que pasa de RearmRequired a Ready; no se vuelve a interpretar un mItemTrigger que ya fue consumido. La prueba compila también el callback on_stick_post_fx heredado sin cambiarlo, en ambos órdenes de registro. Cada init verificado consume una sola pulsación. Un init observado sin entrada nueva invalida la procedencia de su clip actual; no puede tomar prestada una pulsación anterior. El registro de la pasada anterior permanece separado para juzgar solo su contacto legítimo. Solo un parry POST08 realmente comprometido habilita un permiso de recuperación; un buffer corto de6 ticks puede conservar la pulsación siguiente y caduca. El permiso máximo es30 ticks. Mantener B no produce nuevos inputs.

En checkDamageAction POST, prioridad−100 y después de la decisión nativa de daño y de LNK05, la ruta rápida exige humano vivo, escudo realmente disponible/dibujable, espada equipada, defensa Ready, sin penalización/rearme pendiente, sin damage timer, sin evento/menú y sin modos especiales de agua/montura/etc. Los procedimientos admitidos son recuperación de Shield Attack después de su fin ofensivo12; recuperación de GuardSlip tras completar interpolación corporal y frenar, al menos12 ticks después del parry; o procedimientos terrestres libres3..9/0x1b con ese plazo. No admite crouch, scoop, Helm Splitter, Finish ni otros procedimientos prioritarios. Esto delimita el **nuevo rearme**; la comprobación del movimiento de un Shield Attack normal no depende del equipamiento espada ni del clasificador Blue.

El cambio de GuardSlip no inventa limpieza de colisión: `setCollision` sigue llamando a `mCcStts.Move()`, y `dCcD_GStts::Move` renueva TgApid/AtApid antes del registro. No se escribe ese estado ni el contador nativo de bloqueos. El native init conserva mezcla5 y rate1; no se acelera ni se resetea manualmente la animación del escudo. La nueva acción pasa por todo el init nativo y su readback. No se concede ningún parry durante ese init.

Cada contacto usa el snapshot previo al execute de Link, correspondiente a su pasada real de colisión; un init ocurrido después de esa pasada no puede acreditar el contacto anterior. El registro conserva cuatro episodios por valor y distingue la acción del snapshot de una nueva acción iniciada en el execute actual. Confirmar un episodio anterior **no arma el rearme de otro episodio nuevo todavía sin parry**. Cada Shield Attack solo puede confirmar un parry; una acción nueva obtiene serial nuevo aunque PROC_GUARD_ATTACK no haya cambiado.

Se conservan los límites CP03 **delta[−1,+7], edad≤9**, con un requisito adicional autorizado de procedencia física: no hay crédito en un clip recién inicializado que todavía no avanzó. Puede rechazarse un contacto en ese fotograma inicial; no se amplía la ventana para compensarlo. La pose realmente visible, su mezcla y el resultado defensivo completo requieren aprobación humana: **VISUAL_SHIELD_MOTION_HUMAN_PENDING**.

## Escrituras, ABI y barrera

Dos objetivos nuevos: `daE_OC_c::execute` y `daAlink_c::procGuardAttackInit`; cuatro callbacks adicionales en objetivos ya existentes. Todos continúan el original. Ocho imports nuevos, cada uno justificado en pe_audit.py: execute, setActionMode, checkBck, checkBeforeFloorBg, procGuardAttackInit, checkUnderMove0BckNoArc, checkShieldDraw y getLayerNo (contexto de solo lectura). Total esperado24 objetivos (15 compactos+9 extendidos),63 imports de juego, siete contratos de servicio. El CI41746570392 y la descarga independiente confirmaron estos totales en el binario MSVC; véase PE_IMPORTS.json y NATIVE_WRITER_SCOPES.json.

Cuatro funciones de escritura nueva, sin inline para inspección MSVC: `cp04_native_rate`, `cp04_native_mode`, `cp04_native_gap`, `cp04_native_shield_restart`. Las dos transiciones se enlazan a imports tipados del EXE; las dos escrituras inline son morf+0x28 y timer E_OC+0x8e2. Se comprobaron estáticamente en el EXE los offsets nuevos leídos de Link: mShieldModel0x7c0 (setShieldModel), mNormalSpeed0x44f8 y mProcVar1 0x4166 (procedimientos guard). Hay static_assert MSVC y comprobaciones de firma.

La barrera original107 funciones/15 encabezados y las excepciones CP02/CP03 permanecen. `cp04_policy.json` registra un parche inverso literal mínimo: el auditor heredado compara el programa0.11.6 exacto después de retirar **solo** las inserciones autorizadas. Otro auditor verifica hashes de **todo** el código nuevo, el cuerpo nativo de referencia, el oráculo Expansion y los puntos de integración. No se repinean globalmente HUD/combate para hacer pasar cambios. Se añaden negativos de fuente, mutaciones de comportamiento y negativos de instrucciones extraídas del PE real.

No hay modificaciones de pesos, regen CP02, ventana CP03, bonus/rearme POST06, Fury, HP, lifesteal, IA Red/Black, EVF, HM, EHB, Zora Swim, Luau, Randomizer, SDK/EXE/ROM/saves o geometría/HUD. Los mensajes INIT heredados describen sus componentes históricos; el inventario total del checkpoint está en la auditoría PE y RESULTS.json.

## Telemetría y riesgos pendientes

Presupuesto640 líneas de detalle CP04; resúmenes PERIODIC cada1800ticks de simulación observados y SHUTDOWN independientes del presupuesto. La emisión periódica no cancela ni modifica el combo/escudo y se deduplica por tick. Los contadores siguen completos después de agotarlo. Eventos: BLUE_OPPORTUNITY, COMBO_SELECTED/NORMAL_SELECTED/SELECTED_NOT_STARTED, SWING_START/NEXT_SWING_STARTED, SWING_HITBOX_BEGIN/END, SWING_CONTACT/END, PAUSE_BEGIN, SPEED_APPLIED_READBACK/SKIPPED_FOREIGN/RELEASED, INPUT_NEW/BUFFERED, NATIVE_ANIMATION_STARTED/VISIBLE_CLIP_ACTIVE, PARRY_MATCHED, CHAIN_CANCELLED, COMBO_CANCEL/COMPLETE, SUMMARY. Se correlacionan source, identidad/contexto, tick global/local, oportunidad/combo/swing/token, clip/end, frame de evaluación AT y frame de pose, tasa, procedencia LNK07, serial de animación de Link y serial POST08, postura y motivo. `incoming_group_hint` se infiere del handoff1/1,15/1,30; no pretende leer el contador privado de compañeros de Expansion.

Coste acotado por construcción:64 sidecars y4 recibos de escudo por valor; sin asignación dinámica nueva ni recorrido de la lista global del host. La búsqueda y el mantenimiento recorren solo el ledger propio de64slots. La emisión de detalle está limitada y el agregado periódico se deduplica. Esto no mide el coste real con ocho mods ni garantiza30/60FPS; esa comprobación permanece humana.

Un log de clip activo no certifica visibilidad humana. Las colisiones del laboratorio son inyectadas solo dentro de ventanas AtSet reales de la función oficial, con escudo/targets modelados; no se ejecuta broadphase real ni render DX12. Las pruebas A/B con ocho mods, cámaras, contacto espacial, naturalidad del arco, sonido/FX, FPS y assets reales están **HUMAN_RUNTIME_PENDING**. El orden de hooks es contrato fuente y se prueba en ambos registros; cualquier otro propietario de velocidad desconocido falla de forma conservadora. No se entrega ni requiere un segundo `.dusk` de Expansion.

## Cierre técnico verificado

Fuente compilada `2d103c5562f7199b875d5c4c7de7f00a32922a61`, CI `41746570392`: build e independent-download SUCCESS. Paquete, DLL y91archivos de evidencia descargados con índice de hashes verificado y CRC correcto. Los 20 laboratorios suman 3.188.646 comprobaciones finales; los subtotales de cada log no se suman de nuevo. La adaptación CP04 suma 12.439 y las 468 mutaciones pasan con 0 timeouts. Los informes derivados se publican en un sucesor documental separado, sin reconstruir ese binario. El render real, A/B y defensa física continúan HUMAN_RUNTIME_PENDING.
