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

mmvbg común más cercano: centro a 4062.1080, parámetro 0x1fe0004d. getArcName resuelve **@bg004d**, cuyo spec.dat puede crear actor secundario/modelo/colisión. ARC ausente. ClearB capa 6: centro a 4078.1925; necesita **Obj_Board.arc**. Parámetro 0xff41 selecciona ClearB02.dzb y escala adicional XZ. Cull box no certifica collider ausente; distancias al centro no prueban exclusión de ambas geometrías.

Hay enemigos, vegetación, items y otros actores en capa 6: no se aplica patch/delete/replace a ninguno. Home positions no acreditan posiciones actuales o zonas barridas; tampoco incluyen creaciones de scripts/mods.

RPAT/RPPN usa offsets **relativos a RPPN**, conforme a rpatInfoInit. Sala: 33 rutas/170 puntos; stage: 58/700. Ruta sala 7 (27 puntos) incluye (-4000,-6715.284668,65150), a aproximadamente 58.48 del XZ observado. Para candidato queda a **115.6156 de la caja del modelo**, no del centro. Ruta stage 6 queda a 1479.4209. Falta acreditar consumidor, ancho barrido e inactividad/compatibilidad de ruta 7; separación positiva pequeña no aprueba seguridad.

event_list sala: MapToolCamera4, R03_gate, MapToolCamera25/35/42. Stage: SMELL_1st, iria_nioi, iria_pouch01. Límites de tablas/event/staff/cut/data y referencias tipadas validados. Paquetes R03_gate.stb, iria_nioi.stb, iria_pouch01.stb existen; bloques STB JFVB/cámara/actores/mensajes/control. No se ejecutaron secuencias ni se certificaron todos sus efectos. BGCheck=3 en datos de cámara impide inferir cero efecto de nueva colisión solo porque no se solape un trigger.

R_Gate depende también de M_RGate00.arc y switches/evento de escolta; faltan ARC y estado. Layer 6/eventos no justifican afirmar cero interacción con progreso.

## Estado y evidencias pendientes

**Resuelto:** descarga/integridad, formatos, sala/capa, soporte y WRock estáticos, candidato medido, exclusión acotada de volúmenes.

**Pendiente para seguridad:** región/plataforma, mods/overlays, progreso/Twilight/override; Player Info y Terrain/Trigger View del punto/candidato; lista completa pos/angle/list con perfiles/posiciones; salida/reentrada sin DEVF. Llegar caminando si accesible, sin teleport/spawn/flags ni activar DEVF.

Completar colisiones próximas con copias de solo lectura de /res/Object/@bg004d.arc y /res/Object/Obj_Board.arc y SHA256 en repositorio privado. M_RGate00.arc permite completar dependencias puerta/evento si se pretende acreditar su interacción. Si nombres difieren, enviar listado/capitalización real. No ROM completa ni save; no volver a pedir STG/R03/WRock ya verificados.

Ruta 7: identificar consumidor/estado y amplitud barrida; listado de perfiles/IDs y observación de zona. Además verificar contacto sobre pendiente antes de aprobar escala 1. Capturas sin actor no certifican render/colisión DEVF: requerirán prueba posterior autorizada y barrera host resuelta.

**Unload: bloqueo independiente sin cambios, NO-GO**, ver LIFECYCLE_AUDIT.md. Sin TEST activo, host modificado, instalación, aparición, nueva compilación ni CP02.

Reproducción: analysis/README.md. Metadata derivada: evidence/location-f-sp121-summary.json; fuente exacta por hash/ruta/línea: evidence/location-f-sp121-source-references.json. Recursos y registros completos permanecen fuera del repositorio de código.
