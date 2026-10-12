# G4 — revisión incremental del punto anterior

**NO_SAFE_POSITION_VERIFIED.** Disponibilidad de recursos resuelta y geometría local mejor delimitada; todavía no se admite una posición para G5. No se inventa otro punto ni se descarta definitivamente la referencia WRock.

Único punto contrastado: `F_SP121 / room3 / logical6`, XYZ`(-4806.7346,-6729.480961460304,65135.8281)`, yaw0. Preset normal originalFFFFFFFF/angle.x=-236/argumento-1/setIDFFFF/ACTR1, sin modificar HIO, escala, parámetros o capa. La Y se confirma como **suelo local del origen**, no una garantía de pies/arma o de toda la navegación.

## Consulta nueva justificada por los recursos

Se conserva todo [EOC_POSITION_SAFETY anterior](../CP01_G4_EOC_SAFETY/EOC_POSITION_SAFETY.md), sus28 agregados G2 y resultados WRock/rutas/Digpl/colisiones. No se leyó otra vez el log ni se reejecutaron esos análisis. Se amplía exclusivamente la consulta espacial de **radio501** obtenido de cuerpo/arma/colliders en [MODEL_ANIMATION_ENVELOPE](MODEL_ANIMATION_ENVELOPE.md).

La herramienta [reassess_position.py](analysis/reassess_position.py) recorre19 celdas de octree que intersectan la nueva caja,10 listas de hojas, y decodifica **31 de5326 prismas**, no todo el KCL. Reutiliza los helpers de soporte, half-planes y triángulo/caja de CP01. Resultados en [position-query.json](evidence/position-query.json).

| Consulta local | Resultado y alcance |
|---|---|
| Origen | Prisma2174, Y=-6729.480961460304; normal(-0.015020013,0.998559952,-0.051550031), PLC room3/ground0/special0, sin object/link-through |
| Cuadrado que contiene Acch R100 | Cobertura40000 unidades²; área sin suelo0, prismas2174/2175; alturas[-6741.779357,-6722.814357], pendiente máxima5.521587° |
| Proyección del radio501, polígono circunscrito64 lados | Área~789176.859, descubierta0; prismas2174/2175/2187/2494, alturas[-6777.345370,-6702.528723], pendiente máxima18.605110° |
| Caja XZ±501 más amplia que el disco | Área1004004, descubierta~637.777; incorpora2493. Esa falta en una esquina **no demuestra** un agujero dentro del disco; se distingue del polígono circunscrito cubierto |
| Pared/techo | Prismas4714/4734 intersectan la caja501, pero sus distancias a origen son645.857740/742.278399: fuera de la esfera501 por144.857740/241.278399, en esta geometría estática |

La proyección cubierta es un **PASS_STATIC local de unión de suelo**, dentro de tolerancias numéricas del lector previo; no certifica superficie conectada/caminable, pies, ausencia de agua de BG dinámico o recorrido seguro. La variación de altura~74.82 dentro del polígono501 y pendiente18.6° impiden asumir una plataforma plana. El cuadrado Acch ya varía~18.965 en Y. WAIT/ataques posados aproximados no demuestran soporte de ambos pies en esas superficies ni ausencia de penetración del arma.

No se recalculó el suelo global ni se trasladó el PASS WRock a E_OC. No se inicia una búsqueda masiva de posiciones sin un dominio de movimiento y contexto delimitados.

## Colisiones externas, actores, rutas y Digpl

El origen pertenece a la caja WRock conservada. Por desigualdad triangular, separación de geometría a esa caja menos501 da una cota inferior de separación a la esfera de recursos centrada en el origen. Para colocaciones/estados modelados previamente: mmvbg próximo **≥2842.5612** y ClearB **≥2741.7126**, otras dos mmvbg más alejadas. Se reutilizan sus bounds/transformaciones, sin decodificar esos ARC otra vez. Esto excluye esas colisiones respecto del **volumen local fijo y condiciones autoradas**, no futuras posiciones del enemigo ni cambios de objetos impulsados por eventos.

Los siete originales y sus posiciones móviles se mantienen del JSON G4 anterior:28 capturas, mismo censo/owners; distancia mínima de centro E_OC158~5886.78 al origen de referencia. Se conoce el volumen del **nuevo E_OC normal**, no un confinamiento de todos los originales ni su envolvente futura. No se aprueba una ubicación únicamente con esa distancia ni se pide E_OC2 para ampliar el alcance.

Link pasó a **488.5791 unidades XZ**, dentro de la proyección de la sobreaproximación501 (diferencia-12.4209). **No prueba una colisión real**: la esfera es conservadora y no representa la pose existente. Sí impide afirmar aislamiento respecto del recorrido observado; búsqueda S por defecto1200 y rango2000 se conservan, sin afirmar que el HIO efectivo haya sido medido. No se altera el preset para evitar esa interacción.

Digpl conserva **27 puntos**, separación565.6961 a la caja WRock y centro806.8591 al punto más próximo. Para la esfera local501 la cota geométrica punto-volumen es305.8591; no se transfiere el margen antiguo65.6961 sobre radio500. El consumidor de Digpl se refiere al jugador, **no** a un E_OC barrido; esta comparación no afirma que el enemigo active Digpl. Partículas1000 y flags mantienen las limitaciones previas. Ruta7 a115.6156 de la antigua caja continúa siendo polilínea, no trayectoria de un actor. No se repitió su investigación.

## Movimiento, eventos y límites que impiden admisión

La cota501 se traslada con current.pos. Fuente E_OC `2420–2431` cambia un estado cuando supera rango2000 o2000+300 y lo restablece por debajo de1900; **no fija current.pos a una frontera**. `executeMoveOut:2330–2383` cambia animación/velocidad y decisión frente al jugador; `2529–2531` aplica movimiento, CCMove y Acch después. Los chequeos de suelo/agua y el estado de regreso no acreditan confinamiento absoluto. Se cita únicamente el matiz necesario para la nueva cota, conservando la auditoría de IA previa.

No hay un dominio mundial finito certificado de persecución/retirada/empujes/caídas. Por ello, examinar501 alrededor del origen **no cubre** las superficies que alcanzarían el centro y el arma en el ensayo. No se presenta2000+501 ni2300+501 como radio de seguridad. Tampoco el AABB global de la sala prueba sus límites efectivos, eventos o cargas simultáneas.

Los registros de escenario/eventos/triggers/rutas ya publicados son reutilizables, pero sin una región alcanzable y ramas de progreso delimitadas no acreditan no interferencia durante movimiento. FILI bitSwFF y switchesFF del preset solo desactivan los filtros concretos previamente revisados. Logical6 observado, intervalo estable G2 y entry histórico no demuestran las condiciones de una descarga/reentrada natural ni ausencia de eventos en otra progresión.

El manifiesto tampoco confirma ausencia de override de estos recursos. G2 fue real, con Randomizer/texturas activos; los IDs220/221 siguen de origen NOT_VERIFIED. No se reatribuye ese baseline a una sesión aislada.

## Resultado y siguiente paso mínimo

Se acreditan **recursos, envolvente matemática condicionada y parche estático local**, no un candidato que satisfaga todos los criterios G4. Se mantiene NO_SAFE_POSITION_VERIFIED; no se ofrece un nuevo XYZ ni se confunde el punto de análisis con posición autorizada.

Información mínima adicional: confirmar por escrito la fuente efectiva/override de **estas dos rutas** (sin reenviar los ARC ni ejecutar el juego); y delimitar el contexto de progresión y el recorrido natural accesible/salida-reentrada mediante evidencia **ya existente** y sanitizada, si la hay. Si no existe, se declara pendiente; recopilarla dentro del juego requiere autorización posterior independiente.

Con ese contexto, la siguiente revisión offline puede intentar acotar un dominio **condicionado** a una prueba (no universal), refinar contacto/poses/arithmetic y consultar únicamente sus sectores relevantes. No se amplía ahora a toda la sala en ausencia de ese dominio, ni se pide ROM, SDK, EXE, log o recursos históricos. La presencia de dos ARC ya no es el siguiente input. G5 y pruebas runtime siguen NO-GO.
