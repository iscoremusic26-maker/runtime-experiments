# LNK SESSION01 FIX01 — 0.10.1 PRIVATE TEST

**SOURCE_IMPLEMENTED / HUMAN_RUNTIME_PENDING. La causa exacta del episodio del actor 222 no está demostrada.** La corrección de atribución tiene un defecto original reproducible; la limpieza nativa de contactos interrumpidos, la protección de continuaciones y el monitor corrigen deficiencias demostrables compartidas por las familias admitidas. No presentar esto como una prueba jugable de que todo atasco ha desaparecido.

## Procedencia y alcance

Base compilada exacta: `9453e603c3db5b37c90affec5c619e89ae267cec`, árbol `a48d35f7bd59e4bfb25bfd0ff895c4a7b244f629`. La rama documental `3ec604ed1387c25c3f0f8db1c985fa1aee4c6457` se consultó, pero no sustituye a la base de código. Se reconstituyeron los objetos Git originales y se comprobó el SHA del commit antes de crear el worktree aislado. Los 52 blobs necesarios de la base se verificaron por SHA Git; se conservaron los árboles restantes en checkout disperso.

Ramas nuevas: `feature/posture-lnks1-fix01-direct-hit-ai-liveness` y `ci/posture-lnks1-fix01-direct-hit-ai-liveness`. ID inmutable: `dev.posture.post05_selective_reactions`. Un solo paquete acumulativo, sin LNK05/LNK06, PR, merge, tag o release. Ninguna modificación a otros mods, host, SDK, EXE, ROM, ISO, saves o instalación del usuario.

El paquete real 0.10.0 se descargó por artifact ID `13172155570`: 85987 bytes, SHA-256 `f381cb42a5247bed85326b818955b3b4c1d26b8c0ea079e2c87a78e044516e6c`, mismo ID y versión 0.10.0. Su DLL tiene 187392 bytes, 35 imports del juego y seis objetivos de hook.

`dusklight-20261102-141728.log` no está montado: **LOG_NOT_LOCALLY_AVAILABLE**. Los 33 bloqueos, diez rechazos de atribución, 17 parries, 16 ataques iniciados/7 armados/9 abortados y los datos del actor 222 son evidencia humana aportada en el encargo; no son mediciones nuevas de este agente. No se reutilizó un log antiguo como evidencia de 0.10.0.

## A. Causa de LNK02 y reparación

La puerta original era `Posture::classify`: `NOT_BLOCKED` con `tg_match=0` retorna `REJECTED_DIRECT_NOT_ATTRIBUTED` antes de generar un pendiente. Eso explica exactamente por qué los diez contactos descritos no alcanzaron `confirm_direct`.

La lectura que alimentaba esa puerta se hacía en `lnk_pre`, PRE del Bokoblin. La fuente exacta del host demuestra una ruta incompatible con su supuesto de persistencia:

1. La pasada de colisión registra una esfera At en un cilindro Tg de Link.
2. `daAlink_c::checkDamageAction` toma el **primer** cilindro con hit, con la condición nativa `field_0x2fb8`; antes de usarlo contempla invulnerabilidad y ramas especiales.
3. En daño directo llama a `setDamagePoint`: resta en `ItemLifeCount` y arma `mDamageTimer`. Magic Armor puede gastar rupias sin pérdida de vida.
4. Más tarde en el mismo `execute` de Link, `setCollision` desactiva y limpia los tres registros Tg si `mDamageTimer != 0`.
5. Si el Bokoblin se ejecuta después, su AtHit fresco sigue observándose, pero el Tg que intentaba leer `lnk_pre` ya está vacío. Bloqueos/parries no recorren necesariamente la misma limpieza.

El laboratorio reproduce esta ruta y el rechazo original. Sin el log íntegro no se reconstruyó empíricamente el orden de cada uno de los diez contactos; la fuente demuestra el defecto y su compatibilidad con los datos aportados, sin inventar esa cronología.

La captura nueva es de **solo lectura** en `checkDamageAction` PRE/POST. Conserva valores, no un puntero que se vaya a seguir después: identidad de Link, tick, primer cilindro, clave opaca de collider, escudo, timer, vida y resta pendiente antes/después. El POST de `checkPolyDamage`, únicamente dentro de esa llamada, identifica la rama ambiental real. Se excluyen su resultado no cero y la marca nativa de retorno eléctrico. Esto también elimina el falso positivo de suelo + contacto que el informe de 0.10.0 reconocía como riesgo residual.

`DirectJoin` une esa evidencia con un `NOT_BLOCKED` fresco de POST08, las direcciones de las dos esferas **del actor vivo en su propia llamada**, su generación y su token. Dos recibos, hasta un contacto pendiente por cada uno de los 64 slots. No recorre la cola global de actores. La unión se resuelve en el siguiente `mod_update`, exclusivamente para el mismo tick de resolución nativa, por lo que sirve con ambos órdenes de ejecución. No aumenta `kDirectEdgeTicks` ni `kDirectLifeTicks`.

Solo un recibo con timer PRE cero/POST positivo, pérdida de vida o una resta pendiente nueva, Link humana válida, fuente seleccionada correcta, sin escudo, evento, rama ambiental ni retorno eléctrico autoriza el pendiente. Dos resoluciones nativas ambiguas se rechazan. Identidad, pausa, Link reemplazada, muerte, reciclaje y contactos obsoletos se vuelven a comprobar. El contador heredado vuelve a confirmar timer/vida y aplica una vez el peso, reinicia la recuperación y alimenta el HUD existente. No se escribe vida, timer, estado, guardia o animación de Link.

## B. IA: defecto demostrado y límite causal

La ruta más precisa se identificó al revisar el informe histórico POST08/FIX02 0.8.2: ya describía como hipótesis pendiente una ruptura por espada coincidente con el contacto At del atacante. La implementación 0.10.0 aplaza las rupturas de parry, pero no las rupturas normales por espada. El laboratorio invoca el **Breaker real**: un golpe que cruza 100 durante ATTACK produce `BREAK_SHIELD_STUN` inmediatamente. `action()` apaga At antes de `damage_check`; después del stun ya no pasa por la rama de `executeAttack` que lo rearmaría.

La fuente exacta del motor completa el mecanismo:

1. `cc_set` siempre ofrece las dos esferas a `cCcS::Set`, pero este las incluye en la lista At solo si AtSet está encendido.
2. `ClrAtHitInf` limpia exclusivamente los objetos de esa lista. Una esfera apagada y no registrada conserva el contacto anterior durante el stun.
3. Al volver a ATTACK 1/2, `executeAttack` consulta ese AtHit **sin exigir frame >=14**; si Link mantiene guardia, invierte el ritmo y pasa a recoil3 antes de rearmar.
4. Puede repetirse el retorno a ATTACK y el rebote prematuro, con muchas transiciones y ningún armado reciente. Esto explica por qué maxFrozen1 y siete armados históricos no descartan el problema.

El modelo reproduce seis abortos consecutivos en la ruta antigua y el avance ofensivo corregido en Blue/E_OC, Red, Black, furia y Blue legado, con ritmos 0.75/1/1.15/1.3/2 y grupos 1/2/4/8. Es **SOURCE_AND_LAB_ROOT_CLASS_PROVEN**; no equivale a reproducir dentro del juego el episodio concreto222/gen4 sin su log completo.

La reparación opera en el registro nativo. Tras una intervención realmente aplicada, únicamente si el PRE contiene un contacto At fresco contra un cilindro de Link, se solicita una limpieza de esas esferas por slot/id/generación/tick. PRE de `cc_set` activa temporalmente solo los bits AtSet solicitados que estaban apagados. El `cc_set` original hace su registro habitual. POST restaura esos bits a apagado antes de la pasada global. `ClrAtHitInf` elimina entonces el registro antiguo; `ChkAtTg` omite la esfera porque ya está apagada. **No se genera una colisión adicional, no se borra AtHit manualmente ni se escribe state3.** Los bits que el juego había armado se conservan. Una lectura del siguiente PRE distingue limpieza verificada de fallo/expiración inconclusa. Se mantiene visible el contacto legítimo hasta después del execute del actor, para no ocultarlo a los hooks de Expansion.

La solución no depende de actor 222, Blue ni un ritmo particular; protege las intervenciones de supresión, ruptura y parry de las familias admitidas. No pretende corregir cualquier comportamiento nativo ajeno a una intervención de postura. El límite de capacidad de la lista nativa se conserva; un fallo de registro no se convierte en un PASS y requiere observar `failed`/`expired_inconclusive` en la prueba humana.

Además, `GENERAL` podía restaurar ATTACK 1/2 con un clip en bucle, o con ritmo cero/inverso, sin demostrar que pudiera llegar a la salida nativa `isStop`. En Blue tampoco exigía que la animación permaneciese igual dentro de la llamada; E_OC2 sí tenía esa comprobación parcial. El laboratorio prueba que la política 0.10.0 acepta una continuación ATTACK con atributo de bucle y que la nueva entrada de seguridad la rechaza para Blue, Red, Black, furia y Blue legado admitido.

Esto es un **defecto de contrato de restauración demostrado**, no una demostración de que el actor 222 tuviera ese clip o ritmo. Los datos aportados no contienen la cronología suficiente de atributos, frames, ritmos, distancia y decisiones de todos los pasos. El vínculo exacto del atasco humano con una continuación concreta sigue **AI_CAUSALITY_UNVERIFIED**. Los contactos STALE y los nueve abortos no se presentan como causa por sí solos.

Se revisaron `executeAttack`, `executeFind`, `executeDamage`, `action` y el código exacto de Expansion CP21. Expansion aplica ritmos a golpes recién iniciados y cambia lockouts/grupo/reclutamiento desde sus propios hooks; no se modifica ninguna de esas políticas. No se atribuye a Expansion un fallo sin evidencia. Espera nativa por distancia, suelo, guion o reclutamiento es una alternativa que el log completo debe distinguir del bucle patológico.

## C. Prevención general y monitor

`continuation` se comprueba antes del `post05::process` que realmente escribe. Una entrada insegura se registra como `UNSAFE_NATIVE_CONTINUATION` y conserva la reacción nativa. No reinicia a FIND por tiempo ni manipula posición, ritmo, potencia o vida.

- PRE/POST con animación o velocidad distintas: no restaurar una continuación antigua.
- ATTACK 1/2: clip de una sola ejecución, duración B/C coherente (42/47), frame finito dentro del clip y ritmo positivo finito. Se aceptan los ritmos válidos 1, 1.15, 1.30, 2 y otros positivos coherentes.
- ATTACK 3: solo se continúa un rebote nativo coherente con clip de una ejecución y ritmo negativo. Este FIX no añade un escritor de ATTACK/state3.
- ATTACK 0 conserva su selección nativa de clip; un dato de velocidad no finito se excluye.
- DAMAGE 5 con clip de bucle/ritmo nulo y la cadena física BIG_DAMAGE conservan prioridad nativa.
- La misma prueba protege las restauraciones de POST08; POST06 sigue eligiendo sus entradas nativas, con el protocolo FIX02 de ruptura aplazada intacto.

El monitor nuevo observa hasta 64 identidades, únicamente después de intervenciones. El POST de `executeAttack` lee los AtSet **reales**; alcanzar frame 14 no se usa como sustituto de armado. La recuperación requiere un ciclo armado y salida nativa válida, sin interrupción que invalide la observación. Se detectan rachas recientes de abortos después de armados históricos, reinicios del clip, alternancia ATTACK/FIND y transición ofensiva congelada. No basta un contador aislado de abortos.

Se consideran objetivo, distancia, guardia, hit recibido, evento, knockout, timers, clip, frame, ritmo, recurso, potencia y generación. Las cancelaciones legítimas por daño y la espera fuera de oportunidad ofensiva no se etiquetan automáticamente como atasco. La clasificación sigue siendo diagnóstico, no prueba universal de intención de la IA. Contexto de grupo/reclutamiento se correlaciona con los logs de Expansion; este mod no lee un estado privado no publicado ni pretende conocerlo.

Resultados distintos: `NORMAL_RECOVERY_OBSERVED`, `POSSIBLE_ATTACK_LOOP`, `REPEATED_ABORTS_WITHOUT_PROGRESS`, `POSSIBLE_STATE_TRANSITION_STALL`, `ACTOR_DEAD_BEFORE_RECOVERY_VERIFIED`, `MONITOR_EXPIRED_INCONCLUSIVE`. La muerte conserva las anomalías pendientes. Intervenciones repetidas no renuevan indefinidamente la ventana diagnóstica. El monitor heredado deja de declarar recuperación a partir de un frame armado; sus prefijos y contadores se conservan. Ningún monitor escribe al juego.

## D. ABI y escrituras

Host `40457c6adb381928e4b5fef6ed459ed291edd5e2`. EXE SHA-256 `ffa992038d04290654b8907a7663f4dcf62083beaad2b35014fdfd901d390049`. Las cuatro fuentes nativas consultadas coinciden byte a byte con los blobs de ese commit; hashes en evidencia.

| Evidencia Win64 | Dirección / offset |
|---|---|
| checkDamageAction, `int (daAlink_c::*)()` | thunk `0x14002e8d4`, cuerpo `0x140843e80` |
| checkPolyDamage, `int (daAlink_c::*)()` | thunk `0x14004420b`, cuerpo `0x14084f7b0` |
| llamada real a checkPolyDamage dentro del consumidor | `0x1408442fb` |
| setDamagePoint de la rama de collider | `0x140844991` |
| At mSPrm de las dos esferas E_OC | `+0x1038` / `+0x11f0` |
| primer Tg / stride | Link `+0xb28` / `0x1c0` |
| field_0x2fb8 / timer / reset flags1 | `+0x4114` / `+0x66c` / `+0x684` |

Diez objetivos: seis heredados, tres lectores nuevos y `daE_OC_c::cc_set` con una pareja PRE/POST para la limpieza nativa. `cc_set` tiene firma `void (daE_OC_c::*)()`, import `?cc_set@daE_OC_c@@QEAAXXZ`, thunk `0x14001edc1` y cuerpo `0x140e04b60`. Los dos métodos de Link usan **HOOK_MEM_EXT de 24 bytes**, representación nativa prevista expresamente por el SDK 2.0.3 para una clase cuyo modelo de herencia se fijó estando incompleta (`d_a_alink.h` declara typedefs de puntero a método antes de completar la clase). No se fuerza un modelo compacto ni se altera el SDK o el layout de Link para evitarlo.

El auditor estático solo admite esos dos nombres extendidos y decodifica un subconjunto acotado de instrucciones del materializador generado por MSVC, sin ejecutarlo: escrituras exclusivamente al buffer de salida de 24 bytes del cargador, ajustes nulos y destino unido al import exacto. Cualquier código o destino no admitido falla. Se conservan los ocho registros compactos restantes y se añaden negativos específicos. El pin no admite extensiones arbitrarias.

El único escritor nuevo de memoria del juego es `fix01_at_mask`: cuatro llamadas inline On/OffAtSetBit, exclusivamente al bit0 de los mSPrm At del propio enemigo (+0x1038/+0x11f0, medidos en `action` del EXE y comprobados por layout). Solo lo llaman la pareja PRE/POST de cc_set. El auditor fija su cuerpo exacto y prohíbe esos mutadores fuera de él. Capturas de Link, observación del ataque y monitor siguen siendo de solo lectura; no se añaden escrituras de HP, timer, guardia, velocidad, posición o animación. Las escrituras heredadas de reacción/vida enemiga/Helm/HUD permanecen en sus funciones auditadas. Sin asignaciones por frame, hilos nuevos, escaneo global por contacto o estructuras sin límite. La unión usa O(64) por actualización y las observaciones de IA tienen coste acotado por identidades intervenidas. No se midieron FPS/CPU en juego: **PERFORMANCE_HUMAN_PENDING**.

## E. Sistemas conservados

Una sola postura de Link; pesos Blue 20/30, Red 25/35, Black 30/40, furia 35/45 y Unknown 20/30, ajuste Blue grupo +5 cuando la firma existente lo demuestra. Parry +40 enemigo/+0 Link; furia no parryable; chip no se vuelve a acreditar como directo. Recuperación 10/8/5/2 por vida, guardia x1.5, demora 30 ticks y pausas/menús. HUD inferior, ocultación visual de prompts, controles, barras enemigas, postura enemiga, Helm, castigo único x1.50, Finish, rearme y FIX02 se conservan.

Las pruebas de modelo y la compilación no prueban las ocho integraciones dentro del juego. LNK05/LNK06 y ruptura física de Link siguen fuera de alcance. El campo de guardia nativo no recibe lecturas/escrituras nuevas.

La fuente `c_cc_s.cpp` del host fijado coincide byte a byte con el SDK local: blob Git `73b6993255dedff7e7f7db87b2b2056d5d1f54e4`, SHA-256 `aeda0f16a8f271f10a40ef0f87d82ce85699ed88eb0620879bb26a3bc4c87bab`. El pin final contiene 39 imports del juego, ocho HOOK_MEM y dos HOOK_MEM_EXT.

El manifiesto final de descarga deriva la lista de hooks del DLL auditado. La verificación independiente comprueba esa lista, los tipos de metadatos y el número de imports; un artefacto intermedio con declaración obsoleta de nueve hooks fue rechazado. La descripción del paquete declara también la limpieza At nativa.
