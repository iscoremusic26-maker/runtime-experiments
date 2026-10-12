# G4 — ubicación de un E_OC normal adicional

**NO_SAFE_POSITION_VERIFIED.** No se propone un spawn. El punto WRock continúa como referencia de cálculo, no aprobado ni descartado definitivamente para E_OC:

`F_SP121 / room3 / logical6; XYZ=(-4806.7346,-6729.480961460304,65135.8281), yaw0`.

Falta la envolvente real de modelo/arma/animaciones. El rango nativo2000 no es confinamiento. No se inventan otras coordenadas ni se promueve una posición meramente plausible.

## Suelo y sectores ya estudiados — reutilizados

Fuentes: [LOCATION_ANALYSIS](../CP01/LOCATION_ANALYSIS.md), [resumen geométrico](../CP01/evidence/location-f-sp121-summary.json), [Digpl](../CP01/evidence/location-f-sp121-digpoints.json) y [colisiones externas](../CP01/evidence/extra-collisions-verification.json). Sus hashes actuales se conservan en el JSON G4. No se ejecutaron otra vez análisis KCL/PLC/WRock, rutas o Digpl.

El corpus ya cubre la superficie del punto de observación original y el sector de la caja WRock desplazada750 en X, además de16 evaluaciones de suelo/huella en el vecindario X[-5556.7346,-4056.7346], Z[63635.8281,66135.8281] del cache anterior. Esas evaluaciones son puntos/huellas concretos, **no certificación continua de todo ese rectángulo**. No acreditan un área de deambulación del enemigo.

En la referencia WRock, la unión modelo/colisión ocupa X[-5057.3821,-4565.6961], Z[64726.4348,65451.2378]. La revisión anterior acreditó cobertura de suelo por prismas2174/2175, área descubierta0,441 muestras, alturas[-6767.8931,-6709.5725]. Son datos de la **huella WRock**, no de E_OC. La diferencia de alturas~58.32 obliga a comprobar soporte/pies/movimiento para una nueva envolvente; no se copia automáticamente la Y calculada para otro modelo.

El punto observado original tenía soporte2494, pendiente~2.9665°, PLC room3 y sin object/link-through, según evidencia existente. El AABB global del KCL no identifica límites caminables ni prueba ausencia de agua/caídas. E_OC usa Acch, suelo y comprobación de agua (con ruta WATER_DEATH); todavía no se cubren estos requisitos para su volumen y trayectoria. No se concede PASS de suelo de una nueva instancia.

## Nueva comparación con las 28 muestras reales

Se usaron **las 28 capturas**, no solo posiciones iniciales. Distancias XZ desde los centros registrados hasta la referencia anterior; no son clearance entre volúmenes. Redondeo del logger: enemigos0.1 unidades, Link0.001; error de coordenada horizontal por punto hasta~0.071/~0.00071 respectivamente, aparte de los movimientos entre capturas. No se interpola una trayectoria ni se deduce una velocidad máxima.

| Actor original | Menor distancia XZ registrada | Muestra / línea | Mayor desplazamiento 3D muestreado respecto a primera posición |
|---|---:|---|---:|
| 158 | 5886.78 | 22 /1888 | 973.97 |
| 159 | 11555.46 | 3 /1858 | 985.96 |
| 160 | 9372.99 | 7 /1865 | 825.97 |
| 161 | 8602.79 | 3 /1858 | 799.55 |
| 162 | 17464.36 | 14 /1876 | 749.08 |
| 163 | 7791.91 | 15 /1877 | 830.80 |
| 172 | 10677.97 | 10 /1870 | 1023.85 |

Sus cajas de centros **muestreados** XYZ están en [g4-aggregates.json](evidence/g4-aggregates.json). Esas cajas no contienen necesariamente todos los estados futuros, sus armas ni trayectorias intermedias. La distancia grande de los originales no prueba ausencia de futuras persecuciones o interacción entre aliados.

**Link llegó a488.5791 unidades XZ de la referencia**, muestra22/L1888. El punto no está aislado del recorrido observado de Link. El preset conserva búsqueda S, por defecto HIO1200; puede admitir atención/agresión según orientación, línea de visión y estado. No se afirma un ataque futuro observado ni que1200 fuera el valor HIO efectivo medido. Este nuevo dato exige evaluar acceso/observación y reacción; no autoriza reducir HIO o rango para eludirlo.

## Envolventes: lo conocido y lo pendiente

| Dominio | Evidencia disponible | Lo que impide aprobación |
|---|---|---|
| Cuerpo estático | Escala HIO por defecto1.5, joints esperados, radios50/45 | BMD/joints/escala real no recibidos; origen/pies y dimensiones desconocidos |
| Animación y arma | Modelo arma4, junta mano0xC, offsets70/20, radios45/30; BCK esperados | Geometría del arma, curvas, interpolación y callbacks no acotados; radios no delimitan centros animados |
| Movimiento | Preset normal modo0, rango2000; source de estados ya auditado | Regreso/persecución/obstáculos/ataque/huida pueden salir de un disco ideal de2000 |
| Agresión/social | Búsqueda S1200 por defecto; Link cercano y originales móviles observados | Efectos futuros, línea de visión, rango efectivo y aliados no verificados |

Cull box±200, círculo Acch60/100 y heap no sustituyen una envolvente. Sin un límite geométrico fundamentado no puede calcularse un margen corporal/arma suficiente ni elegir la superficie que habría que examinar incrementalmente.

## Obstáculos, rutas, eventos y progreso

Los PASS estáticos anteriores de @bg004d/mmvbg y Obj_Board/ClearB excluyen sus colisiones respecto a **la caja WRock** (separaciones conservadas~3343.56/~3242.71), no respecto a una futura trayectoria E_OC. La dependencia preexistente M_RGate00 y las limitaciones de eventos de CP01 permanecen; no se reabre su análisis en ausencia del volumen que habría que contrastar.

La distancia115.6156 a la polilínea de ruta7 se conserva sin interpretarla como un actor barrido. **Digpl usa27 puntos discretos**: el más cercano está a565.6961 de la caja WRock y806.8591 de su centro en XZ; la antigua separación superior al radio de atención500 no excluye un enemigo móvil. El alcance de partículas1000 y los flags runtime tienen los límites ya documentados. No se recalcularon ni cambiaron esas conclusiones.

Las rutas/volúmenes/actores nativos en los JSON previos siguen disponibles para comparar una envolvente respaldada. Sus distancias a un punto o a una caja de roca no son pruebas de no interferencia con cuerpo, arma, persecución, triggers o cambios de habitación del enemigo nuevo.

FILI bitSwFF y EnemyAppear1Flag=false conservan el PASS_STATIC del filtro genérico concreto; switches del presetFF tampoco acreditan ausencia de todos los eventos. El logical6 observado pertenece a la progresión real del usuario, no un valor a forzar. Las28 muestras sin creates/deletes establecen un intervalo estable, **no** una prueba de salida/reentrada natural ni todas las ramas de progreso.

## Decisión y condiciones de no admisión

No hay una ubicación estática suficiente para etiquetar CANDIDATE_STATIC_ONLY. No se asumen márgenes, piso plano, confinamiento2000 ni limpieza runtime. Antes de elegir una única posición: recibir/verificar los dos ARC, acotar cuerpo/arma/poses y movimiento con supuestos explícitos, reutilizar cobertura previa solo donde corresponda y estudiar exclusivamente el suelo/obstáculos adicionales que esa envolvente alcance. Después resolver restricciones de acceso, eventos, progreso y carga pendientes.

El siguiente input mínimo está en [EOC_RESOURCE_VERIFICATION](EOC_RESOURCE_VERIFICATION.md). Puede ser necesario otro dato puntual después de medir los recursos; no se solicita ahora una nueva sesión, recursos históricos o una colección de salas.
