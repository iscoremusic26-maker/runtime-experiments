# Separación en vivo y límites de evidencia

Se reutiliza G4B, incluida su extracción de Link y su censo G2/A2. El filtro histórico conservaba Link, centros dentro de una esfera3D de501 y propietarios BG; no podía demostrar el nuevo guard XZ, particularmente con deltaY grande. La extensión propia añade escalares **al mismo visitor**, antes del filtro histórico. No añade un actor pass: cada captura conserva el match de Link y el censo ya existentes.

`ci/build_overlay.py` aplica sustituciones únicas revisadas a copias temporales de nuestras fuentes. No modifica originales G4B ni SDK/host; no es un hook. El diff y hashes de entradas/salidas se versionan como evidencia del build. Se leen ID, perfil, room, owner registrado, posición y, solo para Link, los campos públicos speed/speedF de `include/f_op/f_op_actor.h` oficial. La lectura sigue después de init2, no IsCreating y actorINIT del visitor previo. No se usan offsets ni se guardan préstamos.

El sidecar propio contiene máximo256 registros POD; detecta IDs duplicados y truncación. Se reinicia antes de cada captura y se copia al Frame junto con la secuencia, el update y la Key del mismo capture. Count debe coincidir con visits y con un scan completo. La extracción inicial de Link debe concordar con la fila Link del censo. No se ensamblan datos de polls distintos ni se asume el local_count histórico.

Fórmulas respecto al C float32 promovido:

- dx=Link.x−C.x; dz=Link.z−C.z; deltaY=Link.y−C.y.
- dXZ=sqrt(dx²+dz²); d3=sqrt(dx²+deltaY²+dz²).
- El guard usa exclusivamente dXZ>=1600; d3 y deltaY son diagnósticos.

Se rechazan NaN/Inf y valores fuera del dominio float32 antes de operar en double. En ese dominio las sumas de cuadrados caben en double. La comparación del umbral es inclusiva y sin epsilon inventado; Y de GroundCross tolera0.01 para la misma observación previamente contrastada. Los fixtures usan1599.999/1600/1600.001, y XZ100 con deltaY9000 para detectar el uso erróneo de d3.

Entre A/B/C se exige secuencia creciente, update idéntico, Key idéntica y filas de actores/Link con identidad/posición coherentes. Un cambio de posición incluso aún lejano deniega. Velocidad cero y tres lecturas en un callback no acreditan reposo fuera de esa ventana ni atomicidad frente a otras DLLs.

Los13 snapshots suministrados permanecen evidencia histórica del observador. Sus distancias d3 de621.886/627.430/825.957 implican XZ no mayor que esos valores y **no pasarían**1600; d3>1600 no demuestra XZ>=1600. No se obtuvo su log privado ni se infirieron posiciones faltantes. No prueban los nuevos registros globales ni velocidades ni cumplimiento de esta política.

No-hit vertical no descarta volumen de agua; cero BG candidatos es la cobertura del filtro existente, no toda intersección. Distancias de centros no acreditan clearance de colliders, navegación ni exclusión de agro. La envolvente501 sigue siendo geométrica condicionada. No se repitió el estudio ARC/KCL/Dawnlight.
