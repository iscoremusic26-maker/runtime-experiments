# Un único punto de ensayo E_OC: decisión incremental

**FIRST_TEST_LOCATION_BLOCKED_EXACT_EVIDENCE**. La geometría estática inicial es favorable; no hay un motivo demostrado para REJECTED. Faltan condiciones locales concretas, no una certificación universal de navegación. No se admite todavía el punto ni se incorpora al controlador.

Punto histórico único: **F_SP121 / room3 / logical6**, XYZ **(-4806.7346,-6729.480961460304,65135.8281)**, yaw0. Procedencia: candidato anterior, Y del soporte2174, conservado en [position-query.json](../CP01_G4_EOC_RESOURCE_CONTINUATION/evidence/position-query.json). No nuevo desplazamiento/coordenada ni uso de una posición original ocupada.

Preset intacto: E_oc / perfil0x1FE CURRENT, parametersFFFFFFFF, argumento−1, X−236/FF14, yaw/z0, escala1, setIDFFFF, callbackNULL. Ruta A2 sobre hijo de ROOM_SCENE; sin A1/edición/recarga manual. Controlador permanece XYZ=NO_ASIGNADO.

## Evidencia reutilizada y decisión sobre cada límite

| Aspecto | Evidencia existente | Evaluación para primera prueba |
|---|---|---|
| Apoyo del origen |2174, Y exacta, normal(-0.015020013,0.998559952,-0.051550031), PLC room3/ground0/special0, sin through | PASS_STATIC condicionado. No vacío demostrado en origen. |
| Huella Acch100 |2174/2175, área descubierta0; alturas[-6741.779357,-6722.814357], pendiente máx5.521587° | Soporte local favorable; contacto perfecto de pies no es gate previo universal. |
| Cuerpo/arma y proyección501 | Cotas401/494/501 conservadas; cobertura polígono64 sin hueco, pendiente máx18.605110°, altura[-6777.345370,-6702.528723] | No hay demostración de intersección inicial grave; pendiente/penetración leve/contacto real serán observables. No interpretar esfera como volumen ocupado exacto ni región navegable. |
| Pared/techo estático |4714/4734 a645.857740/742.278399, fuera de501 | Excluidos respecto de la sobreaproximación inicial y condiciones del cálculo; no durante WALK/persecución. |
| Colisiones externas resueltas | mmvbg≥2842.5612; ClearB≥2741.7126 de esfera501 bajo transformaciones estudiadas | No repetir ARC ni bounds. Estados/objetos efectivos actuales siguen distintos de datos autorados. |
| Siete E_OC originales | Mínimo centro muestreado5886.78, movimiento documentado | Ningún solapamiento inicial conocido con esos centros. No censo de todos los procesos actuales/rooms residentes. |
| Link | Mínimo histórico488.5791XZ, dentro de proyección501 y búsquedaS1200 | **No aislar ni reproducir ese recorrido como ensayo.** No prueba contacto/ataque. Posición/volumen efectivo antes de crear debe estar separado; reacción normal posterior es riesgo experimental, no fallo de ownership. |
| Triggers estudiados | scnChg próximo gap3113.0115 a caja antigua; atkItem3926.6192, EvtArea7026.4348 y otros separados | Separaciones reutilizadas solo para sus volúmenes anteriores. No trasladar sin más cajaWRock a esfera501; no se recalculan. No se ha mostrado trigger local causado directamente por E_OC. |
| Digpl/ruta7 |27 puntos, gap565.6961 a caja y806.8591 al centro; gap de501305.8591. Polilínea115.6156 no barrido de actor | No incompatibilidad inicial demostrada. No tratar la ruta como enemigo ni Digpl como trigger de E_OC. |
| Agua/BG efectivo | PLC del soporte y ground codes0; expediente explícitamente **no prueba ausencia de agua/dynamic BG** | **Dato pendiente esencial local.** Un piso sólido no excluye agua por encima ni una colisión dinámica superpuesta. No aprobar origen por duración corta. |
| Eventos/admisión/recursos | FILIFF; modo0 y switchesFF; ARC íntegros, E_OC naturales, registered G2, OverlayService0 histórico | Favorable. No exigir historia completa/probar cada flag. Sesión actual debe ser compatible, sin evento/cambio de progreso activo y con recursos nativos accesibles. |

No se recalculó KCL, animaciones, cotas o censo. No se ejecutó consulta geométrica nueva: una nueva consulta al mismo piso estático no resuelve la composición BG/ocupación **actual** de la sesión y no cambiaría esa carencia.

## Evento local: qué importa y qué puede dejar de bloquear

La presencia de `R03_gate` en event_list no demuestra que esté activo. **No confundirlo con `RIDER_GATE_OPEN00`, nombre que selecciona el Create nativo de R_Gate; además usa un MapToolID. No se acredita aquí una correspondencia entre ambos eventos ni sus cuts.** Consulta focalizada nueva, motivada por decidir si añadir E_OC afecta directamente la puerta: [d_a_obj_rgate.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/d/actor/d_a_obj_rgate.cpp):37–49 busca COACH;317–470 verifica coach/caballo/Link;474–495 apertura por llave/posición/dirección del jugador;537–555 estado por label68/switch;730–751 comando de puerta/evento y escritura de llave/switch nativos. **Esas condiciones de admisión/apertura no usan el nuevo E_OC ni un conteo global de Bokoblins.** No es una auditoría de todos los eventos o cuts.

Por tanto, no exigir M_RGate00.arc ni label68/llave/switchE3 individualmente como inputs obligatorios por la sola aparición del nombre del evento. La geometría de esa puerta y sus posibles efectos siguen no certificados; una puerta/evento actualmente activo o BG local inesperado invalida el ensayo. La condición específica útil es **ausencia de evento/acción de puerta/coach/escolta que interfiera en la escena de prueba**, no demostrar toda la progresión del juego. ScnChg ya responde al jugador; no se atribuye su activación directamente al enemigo. Sin posición presente de Link/BG ni estado de evento no se proclama la condición satisfecha.

## Qué queda indispensable y qué se puede observar después

Antes de admitir/armar: medio y BG efectivos en el origen/volumen inicial; ocupación cercana relevante (incluido Link); sesión sin evento/interferencia de progreso; owner válido y recursos admitidos. Las dos primeras carencias no están cubiertas por el log G2 ni por modelos ARC estáticos. Son las razones exactas de BLOCKED, sin alegar que el Bokoblin deba permanecer inmóvil.

Tolerables como resultados del experimento: WAIT→WALK, orientación/detección/social nativas, contacto de pies/animación/render y navegación observada del intervalo. No requerir censo global exhaustivo ni demostrar nunca perseguir/abandonar región. Se deberá cerrar la sesión si deriva a combate, abandona área observada, se inicia evento/transición o aparece anomalía de carga/owner/render. El timeout no confina físicamente al actor ni deshace un save.

## Condiciones futuras, sin autorización de ejecución

Una instancia y una sesión, sin combate deliberado, room/stage changes, guardado deliberado o HIO/mods que cambien actores/escenas. Baseline aislado verificado (G2 tenía otros mods), backup/config y prevención de autosave mediante opciones oficiales reversibles si disponibles. Intervalo finito y salida completa declarados antes de autorizar ensayo; nada de hot reload ni instalación aquí.

Guardas actuales de contexto y comprobación de separación deben repetirse **antes** de una solicitud futura; un baseline pasado no acredita el instante de activación. No inventar posición de Link ni distancia segura300. Radio501 no es contención y no sustituye volumen del propio Link; excluir overlap inicial con información de colliders/BG pertinente, no con centros solos.

**No se examina candidato alternativo.** No se rechazó geométricamente el punto; la incertidumbre de medio/ocupación actuales no se resolvería escogiendo un antiguo refinamiento sin esa evidencia. No reabrir16+98 puntos ni crear coordenadas nuevas.

G4 histórico sigue G4_RESOURCE_VERIFIED_POSITION_BLOCKED/NO_SAFE_POSITION_VERIFIED. Este resultado específico no autoriza G5 ni CP02.
