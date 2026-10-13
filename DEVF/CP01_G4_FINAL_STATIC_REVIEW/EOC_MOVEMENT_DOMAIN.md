# G4 — movimiento y dominio condicionado

**PASS_STATIC del flujo y restricciones siguientes; PARTIAL para una cota de avance voluntario; NOT_VERIFIED para un dominio completo de observación seguro.** No se exige demostrar confinamiento universal, pero tampoco se adopta un círculo arbitrario o se trata WAIT como inmovilidad permanente.

Fuente oficial `d_a_e_oc.cpp`, raíz40457c6. Se conserva el preset modo0, rango2000, HIO por defecto1.5/búsqueda S1200 y switchesFF. Las cotas401/494/501 no se recalculan: acotan recursos relativos a current.pos, no el desplazamiento de current.pos.

## Estado inicial y transiciones pertinentes

`fpcBs_Create:155–159` limpia el área del proceso; `s_basic.cpp:11–13` rellena con0. WAIT es enum0 y mOcState inicia0. `create:2828` llama al Execute nativo al completar la creación; por tanto no se promete un frame previo en el que el actor aún no haya actuado. `execute` decrementa timers antes de `action`; daño/agua/caída/búsqueda social pueden alterar el estado antes de ejecutar WAIT.

| Ruta/estado | Disparador relevante | Efecto; límite |
|---|---|---|
| WAIT0,896–978 | Inicial; sin triggers prioritarios | speedF0, WAIT BCK; timers10…30 o50…80 en modo0. Puede entrar en búsqueda de cabeza y después WALK **sin input del jugador** |
| WALK,983–1067 | Expira WAIT | Timer100…200, velocidad objetivo4 y giro aleatorio si distancia home<500; después orienta retorno. No hay clamp de posición |
| FIND,1136–1340 | `searchPlayer2`, cabeza, aliado en batalla | Persigue/reacciona al jugador; velocidad objetivo20+nREG_F(0) o retiro-3, frena/ataca según distancias y evento. No cabe en la cota de WALK |
| ATTACK,1379–1518 | Alineación y distancia200…400, sin evento activo | BCK5/6; añade desplazamiento directo `current.pos += delta(oc_attack*_trans)`, además del movimiento común. Las esferas de arma se activan en frames14…22 |
| SOUND_WATCH,1778–1825 | Corte de Link dentro del rango o sonido detectado a1000 | Puede pasar de mirar a DASH con objetivo20+nREG_F(0); no equivale a estar inmóvil aunque Link permanezca quieto después |
| TALK/WATCH,258–297 y1074…/1707… | Aliados a200…400, daño/muerte de otros | Interrupciones/social/observación; requieren estado dinámico no registrado por el censo G2 |
| MOVE_OUT/FIND_STAY,2244–2394 | Rango/obstáculo/retirada | Cambia velocidad/rumbo y comportamiento frente a Link. Umbrales2000,2300,1900 no reubican el origen a una frontera |
| DAMAGE/BIG_DAMAGE/DEATH | Golpes/health/colliders | Impulsos, caída, muerte y efectos; fuera de observación no interactiva, pero no imposibles por estar lejos de siete centros muestreados |
| FALL/WATER_DEATH | Medio antes de ejecutar estado | No requieren daño del usuario. Detectan consecuencias, no garantizan navegación libre de agua o caídas |

Mode2/puente y creación inicial de DEMO_MASTER/CHILD por mode3/4 no pertenecen al preset0. No se eliminan BCK de la cota anterior ni se excluyen convenientemente estados de daño/agua. Las condiciones del juego o cambios externos no se afirman imposibles.

## Detección: rango no significa ataque demostrado

`searchPlayer:307–331` usa **distancia3D**, S1200 por defecto. Dentro de400: velocidad de Link>12 puede detectar sin la misma prueba angular; en otro caso diferencia de yaw<0x5000 y LOS. Entre400 y1200: yaw<0x4000 (90°) y `otherBgCheck==0`. `searchPlayerShakeHead` usa la orientación de cabeza y límite0x2000. `searchPlayer2` puede reaccionar al aliado mpBattle aunque su detección directa falle.

Link a488.5791 **XZ** del punto antiguo no demuestra contacto, rango3D exacto, LOS, yaw favorable ni ataque ocurrido. Tampoco permite declarar aislamiento. Yaw0 del nuevo preset no evita detección posterior: WALK gira y la búsqueda de cabeza cambia orientación. No se usa orientación fija para eludir el alcance.

**Hallazgo incremental importante:** `s_other_oc:207–244` / `searchOtherOc:256–290` no filtran habitación ni owner al buscar otros E_OC ya creados. La búsqueda fpcM_Search→fpcEx_Search usa el mecanismo global de iteración, no el filtro room3 del observador. Battle participation1200, teammate attention2000 y conversación200…400 son defaults HIO. El censo de siete en room3 no acredita ausencia/estado de otros E_OC en rooms2/4 residentes. IDs220/221 siguen sin atribución; no se presupone que estén cerca o en batalla.

## Qué avance puede acotarse, y qué no

Caso estrictamente condicionado: **primer episodio WALK**, iniciado desde WAIT con speedF0; ninguna detección, sonido, reacción social, daño, evento, caída o agua; trigonometría ideal y sin desplazamientos externos. `cM_rndFX(50)+150` da timer≤200 (`c_math.cpp:203–214`); la velocidad voluntaria se acerca a4 sin sobrepasarla. Contando también el tick que cambia a WAIT pero aún conserva esa velocidad, hay como máximo200 integraciones voluntarias: longitud XZ **≤800** en ese episodio, por desigualdad triangular.

Esta cota tiene condiciones y horizonte derivados del código; **no es un confinamiento** ni una región segura admitida. Bajo las mismas guardas, el prefijo inicial de WAIT antes de expirar su mínimo10 no genera avance speedF; puede cambiar inmediatamente por triggers y no controla gravedad o empujes. No se diseña una prueba de9 ticks ni se convierte ese prefijo en autorización de aparición.

`fopAcM_posMoveF` (`f_op_actor_mng.cpp:808–841`) calcula velocidad y añade CCMove; luego `action:2529–2531` aplica Acch. La cota800 **excluye** esos desplazamientos extra y la reacción a superficies. Nuevos WALK repiten aleatoriedad, SOUND_WATCH/FIND aceleran, ATTACK mueve el origen directamente. El rango500 para orientar un paseo a home y los umbrales de2000 no garantizan terminar antes de una pared o volver a una posición exacta.

No se adopta2000+501,800+501 ni otro radio como región mundial garantizada. Las guardas del episodio no están acreditadas para una creación adicional, y el intervalo/timing relevante tampoco está observado. El lector G2 de cadence120_updates no acreditó estados o forces en los primeros ticks de una adición. No se modifica ese lector ni se implementa contención para fabricar las guardas.

## Suelo, agua, obstáculos y correcciones

- WALK consulta una línea aY+100 y300 hacia delante cada8 ticks (`checkBeforeBg:442–475`). Si la intersección está a menos de100 termina el paseo; si está más lejos gira. No son límites del cuerpo/arma501 ni una garantía de no interferencia entre consultas.
- `checkBeforeFloorBg:508–525` compara GroundCross de grupo especial con suelo normal en un punto adelantado; `dBgS_ObjGndChk_Spl` activa Spl y desactiva normal. No significa simplemente “hay piso caminable”, ni demuestra un corredor completo.
- `checkWaterSurface:2397–2412` consulta desdeY+500, ignora la superficie especial si Acch ya está grounded y pasa a WATER_DEATH cuando superaY-140. Es una transición, no protección de la partida o prueba de ausencia de agua.
- `checkFall:2151–2179` considera falta de suelo/códigos4/10/5 o descensos relativos; puede entrar FALL/FALL_DEAD. No prueba que esos casos no se alcancen al salir del parche local.
- No se infiere una pendiente máxima admitida por la IA a partir de18.605°. Acch/H70/R60/100 corrigen el origen; no acreditan IK/contacto de pies ni clearance del arma.

## Dominio de observación: resultado

Un ensayo futuro no interactivo podría tener guardas explícitas y horizonte limitado, pero **todavía no se ha demostrado un dominio alcanzable suficiente** para él. Faltan las condiciones efectivas de Link/sensores/aliados/colliders, medio y progresión/transición. Un volumen voluntario hipotético no justifica consultar indiscriminadamente toda la sala o declarar un punto seguro.

Requisitos que impedirían ese caso: Link entra en detección, sonido/corte/daño, otro E_OC reactivo cercano (incluidas otras rooms), evento, cambio de layer, corrección/caída/agua o ausencia de carga natural identificable. Su ocurrencia/readiness/limpieza solo puede probarse runtime con autorización posterior. Ningún ensayo se prepara o ejecuta aquí.
