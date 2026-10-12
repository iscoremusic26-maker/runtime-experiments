# CP01 — análisis estático F_SP121 / sala 3 / capa 6

Base: checkpoint documental 58c4966fdbadb9a40a184a34c868cca1fe7239b2, descendiente de 1dd539d. La descarga anterior quedó resuelta mediante Git LFS desde el repositorio privado. No se repitieron CP00, compilación ni suites de seguridad CP01.

**Existe un candidato geométrico fundamentado, condicionado. Todavía no hay una ubicación acreditada como segura. NO-GO para TEST activo y CP02; DISARMED_NO_REGISTRATION intacto.**

## Integridad

ZIP completo: 1250550 bytes; SHA256 4914fb424f5c659abb40a4e5d9e12071c2ae521223a4a8d0a6edc9d894cfbfb2. Coincide con CP01_EVIDENCE_SHA256SUMS.txt. Todos los miembros pasan CRC, tamaños y hashes individuales:

| Miembro | Bytes originales / comprimidos ZIP | CRC32 | SHA256 |
|---|---|---|---|
| STG_00.arc | 314496 / 296792 | d1eb1b46 | 3a40151417fb4a6c90588cac24f43de0581a08d83e426b622a43b20c567aa4b8 |
| R03_00.arc | 1031328 / 940189 | aeed9d05 | dc53106667811c4cde18b35edb5279357f00ebecaef2f9de546aea9a5a2b06af |
| WRock.arc | 13749 / 12997 | 2e89248f | 6e1a560e1f6eff833fabe19b8050cacd24c757838658e7b92031bda38ce1cb12 |
| SHA256SUMS.txt | 233 / 160 | 9ee96090 | Hash del propio manifiesto en metadata |

Concordancia acredita integridad de copias, no región/plataforma, procedencia CISO o identidad con recursos montados en Windows. Bytes extraídos, tablas completas y scripts decodificados quedan locales y privados. Ningún recurso original se publica en código o artefactos; únicamente herramientas propias y metadata derivada.

## Formatos y carga

Tres ARC Yaz0 → RARC; tamaños descomprimidos STG=375904, sala=1234976, WRock=16288. Se validan longitudes, offsets y límites antes de interpretar. stage.dzs=27200 bytes; room.dzr=13568. MULT para sala 3: traslación XZ=(0,0), ángulo=0; no hay transformación inventada.

La sala tiene room.kcl (446114 bytes) y room.plc (416), **sin room.dzb**. daBg_c usa dBgWKCol en esa condición, según fuente exacto 2.0.3. KCL: 1535 posiciones y 5326 prismas; PLC: SPLC, stride 0x14, 19 atributos. Triángulos reconstruidos mediante GetTriPnt, no del modelo visual. Árbol: 1214 nodos internos, 4974 listas hoja, referencias válidas a los 5326 prismas.

Comunes + capa 6: sala 37+68=105 registros potenciales; stage 1+25=26. No equivalen a 131 actores vivos: flags, suspensión, loaders y creaciones secundarias cambian el conjunto. El dato previo de 120 actores no los identifica. Sala contiene además capas 0,2,7,e; stage otras capas y EVLY.

**Capa 6 no acumula capa 0 ni equivale a Entry -4.** layerActorLoader selecciona el sufijo efectivo, roomReLoader agrega comunes. getLayerNo usa sala actual y override de entrada. Sin override, F_SP121 selecciona 6 por event bit 0x1E08, 4 por 0x0C01, otras por escort/tmp flags; Twilight puede seleccionar 14. Layer observado 6 no demuestra esos flags ni autoriza otras capas.

## Punto observado y candidato

Usuario observó Dusklight 2.0.3/DX12, F_SP121, room 3, layer 6, entry -4; Link en (-4056.7346,-6717.1538,65135.8281), angle s16 -24697; antes del puente a Kakariko. No hubo nueva ejecución del juego por esta revisión.

Prisma 2494 bajo ese XZ calcula Y=-6717.153941131071: diferencia -0.000141131071 con la observación. Normal=(-0.0210800171,0.9986599684,-0.0472400188), pendiente≈2.9665°. PLC: room=3, exit=63 (sentinela del campo de salida), special=0, ground=0; object/link-through desactivados. No interpretar exit 63 como salida válida. Su hoja KCL incluye el prisma.

El punto observado no se aprueba para spawn: referencia del jugador y ruta cercana. Se compararon puntos vecinos apoyados en KCL. Candidato retenido **solo para análisis**:

| Condición | Valor |
|---|---|
| Stage / Room / Layer | F_SP121 / 3 / **6 solamente** |
| XYZ | **(-4806.7346,-6729.480961460304,65135.8281)** |
| Derivación | X observado -750; Z observado; Y calculado del plano |
| Orientación analizada | yaw s16=0, pitch/roll=0 |
| Escala analizada | (1,1,1) |
| Suelo | Origen en prisma 2174; huella también usa 2175 |

Yaw 0 es elección explícita para medir envolvente, no el ángulo observado de Link. No se escribió posición/orientación en configuración ni se conectó actor al host.

## WRock, suelo y colisión

RARC confirma índices/IDs 4=bmdr/wrock.bmd (13952 bytes), 7=dzb/wrock.dzb (1920), coincidentes con WRock.h y actor exacto. BMD J3D2bmd3: ocho secciones, 67 posiciones XYZ/F32, un joint identidad y TEX1. DZB: 35 vértices, 66 triángulos, tres grupos identidad, un atributo; índices válidos. No se acredita creación J3D/render.

- Colisión local: X[-246.869995,234.380005], Y[0,427.589996], Z[-406.239990,276.130005].
- Modelo local: X[-250.647491,241.038544], Y[0,429.403351], Z[-409.393341,315.409729].

Envolvente conjunta: X[-5057.382091,-4565.696056], Z[64726.434759,65451.237829]. Semiplanos de soporte 2174/2175 con tolerancia 0.0075 de GroundCross cubren la proyección: área descubierta calculada 0. Por envolvente se contrastan 441 puntos con soporte, pertenencia a hoja y reconstrucción baricéntrica independiente (diferencia máxima 1.82e-12). Son cálculos double estáticos, **no ejecución real de GroundCross** ni equivalencia float/MSVC bit a bit.

Pendientes≈3.0752° y 5.5216°. Suelo varía 55.7314 unidades bajo caja de colisión, 58.3206 bajo envolvente conjunta. No es horizontal: apoyar origen central no prueba contacto completo ni ausencia de enterramiento/flotación lateral. CP01 no adapta a pendiente. SAT triángulo/caja encuentra solo estos planos, cero paredes/techos del **KCL estático de esta sala** en caja del modelo. No incluye colisiones móviles u otras salas.

WRock.arc conserva capitalización. El mod solicita Wrock; dRes compara archivos cargados mediante stricmp, y overlays documenta disco sin distinción de mayúsculas. Fundamenta compatibilidad de nombre, sin probar mount, región, RAM/carga real. No se renombró ni reconstruyó recurso.

## Actores, triggers, rutas y eventos

Se usan contratos específicos: scnChg (75/150×escala), noChgRm (100/1000 según parámetro), atkItem (cilindro 50/100), SwAreaS (shape/scale de parámetros), EvtArea tipo 21 (elipse XZ contenida en caja), RMback0 (caja con Y ignorada), hider (AABB suspensión). Volúmenes modelados se separan en XZ aunque estén activos por switches:

| Elemento | Separación según eje/prueba |
|---|---|
| scnChg SCOB[3] próximo al puente | Eje separador 3113.0115 |
| atkItem SCOB[5/6] | Fuera de radio: mínimo 3926.6192 |
| SwAreaS común / capa 6 | Eje separador 6851.1414 /11126.4348 |
| EvtArea SCO6[0] tipo 21 | Fuera de caja conservadora 7026.4348 |
| RMback0 stage SCO6[3] | Eje separador 11180.5677 |
| hider stage SCO6[18..21] | Fuera de AABB |
| KY_chg sala tipo 5 | Fuera del radio 15000: margen 5498.2260 |

No son radios universales de seguridad. KY_chg stage tipo 4 llama lógica ambiental global; no se considera inocuo por distancia.

mmvbg común más cercano: centro a 4062.1080, parámetro 0x1fe0004d. getArcName resuelve **@bg004d**, cuyo spec.dat puede crear actor secundario/modelo/colisión. ARC ausente en el checkpoint anterior; ahora analizado en la sección incremental siguiente. ClearB capa 6: centro a 4078.1925; necesita **Obj_Board.arc**. Parámetro 0xff41 selecciona ClearB02.dzb y escala adicional XZ. El checkpoint anterior no certificaba collider por cull box/distancia al centro. La nueva revisión utiliza ambas DZB reales y transformaciones de carga/ejecución.

Hay enemigos, vegetación, items y otros actores en capa 6: no se aplica patch/delete/replace a ninguno. Home positions no acreditan posiciones actuales o zonas barridas; tampoco incluyen creaciones de scripts/mods.

RPAT/RPPN usa offsets **relativos a RPPN**, conforme a rpatInfoInit. Sala: 33 rutas/170 puntos; stage: 58/700. Ruta sala 7 (27 puntos) incluye (-4000,-6715.284668,65150), a aproximadamente 58.48 del XZ observado. Para candidato queda a **115.6156 de la caja del modelo**, no del centro. Ruta stage 6 queda a 1479.4209. La revisión incremental siguiente identifica un consumidor de puntos discretos: no interpretar esta polilínea como trayectoria barrida de un actor. La distancia geométrica original se conserva; ver sección Digpl.

event_list sala: MapToolCamera4, R03_gate, MapToolCamera25/35/42. Stage: SMELL_1st, iria_nioi, iria_pouch01. Límites de tablas/event/staff/cut/data y referencias tipadas validados. Paquetes R03_gate.stb, iria_nioi.stb, iria_pouch01.stb existen; bloques STB JFVB/cámara/actores/mensajes/control. No se ejecutaron secuencias ni se certificaron todos sus efectos. BGCheck=3 en datos de cámara impide inferir cero efecto de nueva colisión solo porque no se solape un trigger.

R_Gate depende también de M_RGate00.arc y switches/evento de escolta; faltan ARC y estado. Layer 6/eventos no justifican afirmar cero interacción con progreso.

## Estado y evidencias pendientes

**Resuelto:** descarga/integridad, formatos, sala/capa, soporte y WRock estáticos, candidato medido, exclusión acotada de volúmenes.

**Pendiente para seguridad:** región/plataforma, mods/overlays, progreso/Twilight/override; Player Info y Terrain/Trigger View del punto/candidato; lista completa pos/angle/list con perfiles/posiciones; salida/reentrada sin DEVF. Llegar caminando si accesible, sin teleport/spawn/flags ni activar DEVF.

Las copias @bg004d.arc y Obj_Board.arc y sus hashes ya se recibieron y verificaron; no volver a solicitarlas. Ambas colisiones externas quedan resueltas estáticamente en esta revisión. M_RGate00.arc permite completar dependencias puerta/evento si se pretende acreditar su interacción. Si nombres difieren, enviar listado/capitalización real. No ROM completa ni save; no volver a pedir STG/R03/WRock ya verificados.

Ruta 7: consumidor Digpl identificado; falta estado de puntos usados e interacción de excavación/acceso en Windows, y excluir otros consumidores si se pretende garantía global. Además verificar contacto sobre pendiente antes de aprobar escala 1. Capturas sin actor no certifican render/colisión DEVF: requerirán prueba posterior autorizada y barrera host resuelta.

**Unload: bloqueo independiente sin cambios, NO-GO**, ver LIFECYCLE_AUDIT.md. Sin TEST activo, host modificado, instalación, aparición, nueva compilación ni CP02.

Reproducción: analysis/README.md. Metadata derivada: evidence/location-f-sp121-summary.json; fuente exacta por hash/ruta/línea: evidence/location-f-sp121-source-references.json. Recursos y registros completos permanecen fuera del repositorio de código.

## Continuación incremental: consumidor Digpl de ruta 7

Se recuperaron todos los resultados y se publicaron inmediatamente en 9224e1c / DEVF_CP01_LOCATION_F_SP121_REVIEW, comprobados por fetch desde GitHub. No se perdieron KCL/PLC, geometría, hashes o scripts; no hubo reconstrucción/repetición de esos análisis. Estado histórico en 0fe4c16: faltaban @bg004d.arc, Obj_Board.arc y M_RGate00.arc. La subida9f95a34 aporta los dos primeros; no se reabre aquí la dependencia de puerta M_RGate00.

Nuevo hallazgo dirigido: ACTR común [5] es Digpl, parámetro 0xf07ff5ff. create() de daObjDigpl_c extrae tipo inicial5 y route=(param>>20)&0xff=7. Desactiva NOEXEC y obtiene dPath_GetRoomPath(7,room3). No depende de seleccionar ACT0; es registro común, aunque flags/carga real siguen pendientes. Switch=0xff no es un veto de aparición por switch en ese código.

execute() usa la ruta como **27 posiciones discretas de excavación del lobo**, no movimiento interpolado por segmentos. Escoge el punto disponible más próximo en XZ cuando la diferencia Y es menor que200; emite partículas a distancia3D menor que1000; el look target usa distanciaXZ al cuadrado menor que250000 (radio500). Al excavar crea item/tabla, marca el punto usado y, si corresponde, switches. Una ubicación cercana requiere considerar este comportamiento original.

El punto más próximo a la envolvente conjunta del candidato es índice8=(-4000,-6715.284668,65150): centro a806.8591 y caja del modelo a**565.6961 en XZ**. Los27 puntos quedan fuera de la caja y a más de500; margen mínimo sobre ese radio65.6961. Esta exclusión geométrica no acredita su acceso por el jugador, estado mUsedDigFlags, parámetros de atención completos o ausencia de efectos de partículas/cámara. La región de partículas1000 alcanza la zona; no se declara aislada de todo comportamiento.

La medida conservada **115.6156** sigue siendo distancia a segmentos unidos de RPAT, pero **no es una distancia de actor barrido para este consumidor**. Se confirma un consumidor; no se afirma que sea el único posible ni se sustituye por una garantía dinámica global. No se modifica la roca ni se inventa otro lugar. Candidato condicionado y NO-GO permanecen por geometrías externas, contexto/contacto runtime y unload independiente.

Ver evidence/location-f-sp121-digpoints.json y analysis/location_digpoints.py. Esta prueba nueva reutiliza inventory/footprint privados ya calculados y solo analiza el pendiente de puntos de ruta; no ejecuta geometría, host, MSVC o suites de seguridad anteriores. La recuperación final es DEVF_CP01_LOCATION_DIGPOINTS_REVIEW, sin mover el tag del primer checkpoint.

## Revisión incremental de colisiones externas desde 0fe4c16

### Integridad y estructuras — PASS estático

Se recibió main privado en 9f95a34d93810b55250e8b833a2e343757cf8a01 mediante Cloud/Git/LFS. DEVF_CP01_EXTRA_COLLISIONS.zip tiene19489 bytes, firma ZIP real (no puntero LFS), SHA256 **2a4d3e4cbf90d97fd6603f284a826849f37d1c5849ef817e46e9ec1da1011c44**, coincidente con CP01_EXTRA_ZIP_SHA256SUMS.txt. Manifiesto interno y tamaños declarados coinciden; tres miembros pasan CRC32.

| Miembro | Original / comprimido ZIP (bytes) | CRC32 | SHA256 |
|---|---|---|---|
| @bg004d.arc | 19385 /18576 | 23549750 | 5c0dc254e5bb4c19a8a44712a89f910c5c1f6b4129b6e87676be7af6cdd46a6a |
| Obj_Board.arc | 440 /443 | bdc000d2 | dcdbd1e63de5ee0ed485705d00a42119e912bff6e1036341dd65b4fce4b98453 |
| CP01_EXTRA_SHA256SUMS.txt | 160 /122 | 3c40951c | 17235121a0ddb9abd439833d6c69bc83d5fe0a7b239aa536d498e91281b24caa |

Los ARC son Yaz0/RARC válidos: @bg004d descomprime25056 bytes y Obj_Board2176. Se validan límites de tablas/payloads, indices DZB, grupos identidad, secciones BMD, positions packed S16 y límites de spec/texture-sharing. Los modelos nuevos usan GX_S16 con fracciones5/7; no se fuerza el parser F32 del WRock previamente analizado. No hubo fallo de integridad ni dato original modificado.

@bg004d contiene model0.bmd12864, model1.bmd10656, model0.dzb832 y spec.dat148. Model0:77 posiciones, un joint identidad, TEX1 con imagen128×128 embebida; model1:236 posiciones, un joint identidad y TEX1 sin imagen. spec referencia model1→model0; nombres de textura coinciden conforme a setupShareTexture. No es una textura de ARC externo ni de stage. Model0 DZB tiene13 vértices,22 triángulos,3 grupos y1 atributo; límites locales X[-300,300],Y[0,600],Z[-193.190002,146.380005].

Obj_Board contiene cinco DZB clearb00..04,352 bytes cada una; cada una tiene4 vértices/2 triángulos y límites locales X/Z[-50,50],Y=0. Se valida también el recurso seleccionado02. No BMD, scripts ni referencias a otra geometría. ClearB01 tiene grupo de agua; no se confunde con la variante02 usada. CArcName normaliza nombres solicitados a minúsculas: ClearB02 resuelve clearb02.

### mmvbg → BG_OBJ, estados e interacciones

Se reutilizan los registros del análisis anterior: ACTR[16],[19],[20], todos param0x1fe0004d. getArcName usa16 bits bajos→@bg004d; spec type1 hace que el actor intermediario SET_BG_OBJ solicite BG_OBJ. Pasa position/angle/scale del registro; no se crea ningún actor en esta revisión.

BG_OBJ copia home.angle.x/z como argumentos y switches, y pone pitch/roll a0. Las rotaciones de registro (-1,yaw,-227/-136/-134) **no son inclinaciones de geometría**. initBaseMtx usa traslación y yaw; escala de estos ACTR por defecto(1,1,1). Las tres yaw efectivas:2730,15473,-11832. No movimiento espacial interpolado en el Execute de este tipo: retorna mBgMtx. Se modela geometría en su posición de carga; overlays/intervenciones ajenas siguen sin verificar.

Spec type1/flags0x0002 selecciona cilindro objetivo. Antes de destruir: model0 y model0.dzb. Switches primarios de z:29,120,122; secundarios0xff; arg0=0xff; eventId=(param>>21)&0xff=0xff. checkDestroy acepta ataques bomba/bola de hierro según su contrato y permite cambiar estado/switch. En estado roto usa model1 y retira model0.dzb. **model1.dzb no está presente y CreateHeapType1 solo lo carga si existe**: la colisión rota es nula, no una referencia geométrica externa pendiente. No inventar un model1.dzb.

Cilindro de golpe: radio305.246277, altura601.649231, derivados del joint/model0 mediante settingCullSizeBoxForCo y set_cyl_0. Se comprobó también su separación XZ. initAtt crea Tag_Attp: campos por defecto producen arg0=arg1=3, que deshabilitan lock-on en execute de ese helper para ambas ramas de switch. No se ignora esa creación secundaria ni se usa la distancia al actor intermediario como certificado del BG_OBJ vivo.

Spec incluye seis partículas globales0x89c2..89c7 y sonido0x80016 al destruir, con particle model number0; no se toma la ruta Always/BreakWoodBox.bmd. Sus recursos globales y extensión de efectos no vienen en estos ARC; **NOT_VERIFIED** para cero efectos visuales/sonoros o interacción runtime. No constituyen una geometría externa referenciada en spec. EventId0xff evita orderOtherEventId en esa rama; hay cambios de switch originales y no se declaran irrelevantes para progreso.

### ClearB — transformación y carga

Registro SCO6[3],param0xff41: nameArg1 escala X/Z×10; arg0=4 selecciona ClearB02; switch255. Escala de registro(1,1,0.6) queda(10,1,6). setBaseMtx ejecuta T·Ry·Rx·Rz·S con pitch16384=90°, yaw-30037, roll0. El plano local horizontal se vuelve pared vertical, Y[-6700,-6100]. La caja de cull no se usó para inferir estos límites: se transformaron los4 vértices reales.

MoveBGCreate comienza con matriz de yaw y escala de registro antes de Create; esa geometría inicial también se evaluó por separado. Después de Create/MoveBGExecute usa la matriz completa anterior. Arg0=4 registra cuando isSwitch es falso; dSv_info_c::isSwitch(255,room) retorna FALSE. Por tanto, bajo estas APIs/parámetros, la pared queda registrada; no se necesita editar flags ni suponer switch255 activo/inactivo. No hay eventos o geometría secundaria solicitados por esta variante.

### Separación del candidato — PASS estático acotado

Se reutiliza, sin recalcular KCL/WRock/Digpl, la envolvente conjunta ya publicada: X[-5057.382091,-4565.696056],Y[-6729.480961,-6300.077611],Z[64726.434759,65451.237829]. Candidato, yaw0 y escala1 intactos. Transformación usa orden fuente y cuantización JMath de8192 muestras; trigonometría/cálculos locales aproximan la tabla float, sin ejecutar el host. Se conserva margen numérico1 unidad, muy inferior a separaciones.

| Instancia / estado | Separación mínima conservadora entre AABB (unidades) | Triángulos intersectando caja |
|---|---|---|
| mmvbg ACTR[16] intacto | 3343.5612 | 0 |
| mmvbg ACTR[19] intacto | 21191.1170 | 0 |
| mmvbg ACTR[20] intacto | 22147.6549 | 0 |
| ClearB SCO6[3], matriz final | 3242.7126 | 0 |
| ClearB, fase inicial de carga | 3677.0939 | 0 |

La separación AABB es cota inferior a la distancia real, no distancia exacta entre superficies. SAT triángulo/caja corrobora cero intersecciones. Los cilindros objetivo mmvbg tienen márgenes XZ3422.1526,21197.3085,22230.1631. Cajas de ambos modelos intacto/roto también quedan separadas; estado roto no tiene DZB. Ambas geometrías aportadas no alcanzan la caja ni la vertical del candidato en estos estados/transformaciones: no introducen un suelo alternativo bajo él. No hay que descartar o mover el candidato por estas dos colisiones.

### Qué se cierra y qué sigue pendiente

**Cerrado estáticamente:** dependencia de geometría @bg004d/Obj_Board; formatos, selección/transformaciones/estados de las4 ubicaciones y exclusión de sus colisiones/cilindros. No se precisan otros ARC para completar la geometría directa de estas dos familias. La dependencia de puerta M_RGate00, previamente documentada, no se analiza en esta tarea.

**Ubicación segura: NOT_VERIFIED**, no aprobada ni descartada. Persisten contexto región/plataforma, mods/overlays, progreso/Twilight/layer override y evidencia Windows sin DEVF: Player Info/colisión/triggers, lista de actores reales y salida/reentrada. Contacto de roca sobre pendiente, efectos, acceso a puntos Digpl, cámara y progreso no se certifican estáticamente. Digpl conserva27 puntos discretos y separación565.6961: no se repitió su análisis ni se reinterpretó115.6156 como trayectoria barrida.

**Runtime del mod/DX12: NOT_TESTED. Unload: BLOCKED, sin reinvestigar. CP02: NO-GO.** DISARMED_NO_REGISTRATION intacto; sin registros, TEST activo, host modificado, recompilación o suites anteriores. Siguiente paso mínimo para ubicación: capturas/contexto/listado baseline desde Windows con las vistas nativas ya documentadas, sin instalar/activar DEVF. No pedir de nuevo estos dos ARC. Ni esta separación ni las capturas resuelven el bloqueo independiente de DLL.

Reproducción nueva: analysis/location_extra_collisions.py --inputs <repositorio privado> --prior <directorio privado previo>, con DEVF_CP01_LOCATION_WORK fuera del repositorio de código. Reutiliza los JSON anteriores y solo decodifica el nuevo ZIP. Metadata derivada y referencias fuente: evidence/extra-collisions-verification.json y extra-collisions-source-references.json. Recursos permanecen privados; nuevo checkpoint DEVF_CP01_EXTRA_COLLISIONS_REVIEW.
