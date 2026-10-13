# G4 — ubicación, progreso y transición natural

**NO_SAFE_POSITION_VERIFIED.** Se conserva el punto WRock como referencia, no se promueve ni se descarta universalmente:

`F_SP121 / room3 / logical6; (-4806.7346,-6729.480961460304,65135.8281), yaw0`.

Preset E_oc normalFFFFFFFF, angle.x=-236, z0, setIDFFFF, ACTR1, argumento-1: intacto. HIO y partida no se modifican. [position-query.json previo](../CP01_G4_EOC_RESOURCE_CONTINUATION/evidence/position-query.json) y sus31 prismas se reutilizan **sin repetir su consulta**.

## Suelo y pies: alcance real

Prisma2174 confirma Y del origen; Acch100 y proyección local501 cubiertos según el expediente previo. Paredes4714/4734 fuera de501 a645.858/742.278; colisiones externas previamente excluidas en condiciones autoradas. Todos son PASS_STATIC locales, no dominio de navegación.

Las poses guardadas WAIT/ataque son diagnósticos, no se recalculan. WAIT tiene y mínima corporal~-0.124 y extremos de joints de pierna~8.952; un joint no es la planta del pie ni identifica el vértice que toca suelo. El parche Acch100 varía~18.965 en altura y la proyección501~74.82; no se concluye contacto perfecto o penetración real con AABBs.

El fuente añade precisión: `setGroundAngle` muestrea offsets50/80 y alturas relativas<50, pero sus llamadas en E_OC están en BIG_DAMAGE estados4/5 (1671/1696), **no se demuestra por esa función alineación automática de WAIT/WALK o IK de cada pie**. `mtx_set` consume la actitud; Acch corrige origen, y la reacción de arma tiene otras consultas. La cota501 ya incluye rotaciones, pero no convierte cobertura de su proyección en huella de apoyo o clearance a lo largo de movimiento. Agua/superficies especiales/caídas tienen los límites de [EOC_MOVEMENT_DOMAIN](EOC_MOVEMENT_DOMAIN.md).

## Link, actores y sectores alternativos existentes

Se conservan los siete originales, sus agregados móviles28, mínimo de centro5886.78 al punto y Link488.5791XZ. Ni posiciones futuras ni estado AI/LOS/velocidad/sounds se extrapolan. Source busca aliados sin filtro de room; RTBL confirma residencia de otras salas y por ello el censo room3 no cierra la guarda social global. IDs220/221 siguen NOT_VERIFIED en origen.

Se realizó **solo un cribado numérico nuevo de puntos ya calculados**, sin nuevo grid/terreno:16 evaluaciones antiguas y98 refinamientos del vecindario WRock. Se reutilizaron posiciones privadas derivadas de las28 capturas para distancias nuevas; no se releyó el log de capturas ni se repitió el censo G2. Solo agregados del cribado se publican.

Todos esos puntos tienen alguna posición de Link registrada a distancia3D menor que S1200 por defecto. El máximo de esos mínimos es1198.649 para el grupo16 (sector con pendiente WRock~39.975°, separación horizontal mínima~731.713), y539.269 para refinamientos98 (pendiente~18.605°). Es un resultado de cribado, **no detección/ataque garantizados ni validación de un nuevo volumen E_OC**. Las mejores distancias no aportan un sector que pueda admitirse sin más evidencia; no se ofrece una lista o un nuevo XYZ como candidato.

## Rutas, triggers y objetos

Digpl mantiene27 puntos y565.6961 a caja WRock,806.8591 al origen; gap de sobreaproximación501~305.8591, con interpretación del consumidor relativa al jugador conservada. Ruta7/polilínea115.6156 no es actor barrido. Separaciones mmvbg/ClearB y otros eventos originales permanecen sin recalcular. La búsqueda social o física no se cierra con distancias entre centros ni con esas separaciones fijas cuando el origen se desplaza.

Se relacionaron los tres scnChg comunes ya decodificados con SCLS, **sin reconstruir geometría de triggers**:

- SCOB0: exit0, switchFF, arg1FF y labels on/offFFF. Existe ruta declarada F_SP109/room0/point60, layer derivado. Su trigger queda condicionado a presencia del jugador y aceptación de cambio por el motor, no al E_OC.
- SCOB1: exit1, switchE3, arg1FF, on-label232/off-label85. La salida F_SP109/room0/point34 exige condiciones de progreso de esos labels/switch; no se conoce su valor efectivo en G2.
- SCOB3: exit4, switchFF y labelsFFF. Destino D_SB02/room0/point0; no se utiliza para proponer una observación o manipular progreso.

SCLS también contiene otras salidas; un registro de destino no demuestra que su ruta esté habilitada o que se haya cruzado. `daScex_c::checkWork:13–34` controla switches y saveBitLabels de eventos; sus volúmenes reaccionan al jugador. Se mantiene el evento R03_gate del cache previo como dependencia de contexto, sin afirmar activo/inactivo.

## Progresión y layer6

`dComIfG_play_c::getLayerNo_common_common:160–174,642–669`: sin override explícito, fuera de Twilight, F_SP121 usa layer6 al completar el evento0x1E08 (Midna's Desperate Hour). Si se inició0x0C01 sin completarlo usa4; otras ramas escort/tmp dan0/2/3. Twilight tiene rama14 y ajustes específicos; no se fuerza ninguno.

Un override no negativo se devuelve como layer. **Logical6 no prueba por sí solo el flag0x1E08 o ausencia de override**. Además, SCLS del stage contiene una transición declarada F_SP121/room0/point8 con layer explícito6. Entry histórico-4 tampoco es un layer: `dStage_playerInit:1708–1738` usa un dato de restart para resolver point; no identifica por sí solo una ruta de llegada.

R03 conserva17 PLYR: IDs1,99,2,10,20,3,0,21,5,88,15,4,14,6,22,16,17. Dos comparten posición de inicio1/6; no se atribuye automáticamente a una de ellas la llegada de G2. Hay puntos y destinos concretos, pero la accesibilidad de la partida y camino de regreso no se demuestran con esa lista. No se solicitan saves ni flags editados.

## RTBL y consumo A1 natural

Nuevo análisis limitado a RTBL/SCLS de los DZS/DZR **ya extraídos**; hashes individuales coinciden con el inventario previo. `include/d/d_stage.h:98–108` fija SCLS en **13 bytes**. El inventario genérico anterior anotaba record_size12 y no decodificaba registros; se documenta aquí la corrección de formato para nuevas transiciones. No se modifica esa herramienta/historial, ni cambia suelo/ARC/actores previos.

RTBL del stage tiene16 filas. Para room3 carga `[3,2,4]`, todas con BG. Filas2 y4 también incluyen3. **Moverse visualmente3→2 o3→4 no acredita descarga de ROOM_SCENE3**. Filas1/5 excluyen3; secuencias estructurales3→2→1 o3→4→5 podrían causar retirada de3 si las transiciones físicas y condiciones del motor se cumplen, pero RTBL es lista de residencia, no una demostración del camino transitable o habilitado.

`dStage_roomControl_c::loadRoom:315–360` marca0x0C a rooms cargadas que salen de la lista, pospone durante estados pendientes/no-change y crea nodes al faltar residencia. `dScnRoom_Execute/objectSetCheck:243–280` esperan creaciones, solicitan eliminación de objetos/node y después pueden cargar de nuevo. `dScnRoom_Delete:328–365` puede conservar datos de archivo bajo ciertas condiciones de nextStage; **retener bytes ARC no equivale a retener el node ni prueba una nueva carga**. Salida real a otro stage tiene rama de liberación, pero las salidas físicas/progreso y retorno siguen sin ejecución acreditada.

A1 estático previo intacto: una Add activa para stage/room/logical exactos, registrada **antes** de la carga natural correspondiente, se consume en el helper roomReLoader después de preparación de bancos/recursos; hereda la layer hija del node. Nada se llama aquí. Handle no es ActorId y la edición no es one-shot: otras cargas pueden volver a consumirla. G2 current0/room_owner5/child6/logical6 son datos distintos; son IDs de esa sesión, no valores a forzar.

## Requisito pendiente y siguiente comprobación mínima

No existe hoy un candidato con dominio condicionado, contacto/navegación y contexto de llegada/salida acreditados. El bloqueo **no es ya la falta de ARC ni la ausencia de información de OverlayService**. Es vincular condiciones de la partida/carga y sensores/actores al horizonte de observación, y cubrir el desplazamiento pertinente sin fabricar confinamiento.

Primero usar **evidencia existente y privada**, si la hay, con: progreso/Twilight y contexto de entry/override conocidos; llegada/salida/reentrada natural identificada (stage, room, logical, node/child y pendientes); censo global de E_oc de salas residentes, posiciones y estado relevante para búsqueda social; condiciones de Link, sonido/eventos durante el intervalo. El log G2 actual no registra esos flags/estados ni un ciclo de retirada/recreación de node3. Source/RTBL describe reglas, no sus valores reales.

Si esos datos no existen, una nueva observación baseline **requiere autorización runtime independiente**, sin adición, cambios de partida o instrumentalización decidida aquí. No se pide ejecutarla ahora ni aportar ROM/ARC/log completo. La documentación delimita qué faltaría observar para evitar repetir el trabajo; no prepara un paquete. Mientras tanto se conservan NO_SAFE_POSITION_VERIFIED y G5/CP02 NO-GO.
