# G2 real — baseline conservado para G4

**PASS_RUNTIME_OBSERVED para el observador READ_ONLY en la sesión proporcionada.** No acredita una aparición adicional, una ubicación segura ni el framework completo. El observador y sus paquetes históricos no se modificaron.

## Procedencia privada

Evidencia primaria: copia anonimizada `DEVF_G2_log_sin_rutas_personales.txt`, **183907 bytes, 2182 líneas**, SHA256 `d19f2760e695f48f4df59706b791de121ffe77806bdafde8a7539b2cdc2b78b4`, comprobado sobre bytes recibidos. Se conserva íntegra y privada, con las **28 capturas**; no se publica el log ni una reconstrucción de sus capturas.

Original identificado por el usuario: `dusklight-20261012-154319.log`, SHA256 `00a0c35b7f352c43967c4793a1ead07cbd596259b8d84a9a0edf058d94b7e5b5`. Este segundo hash es **USER_REPORTED_ONLY**, no comprobado porque el original sin anonimizar no se recibió. La diferencia corresponde a dos archivos distintos, no a una integridad fallida del adjunto.

Las referencias de línea siguientes corresponden exclusivamente al adjunto anonimizado. [g4-aggregates.json](evidence/g4-aggregates.json) publica conteos y agregados derivados, sin texto del log, rutas personales ni direcciones de memoria.

## Resultado confirmado

| Evidencia | Resultado y límite |
|---|---|
| Host | Log L2: v2.0.3, raíz oficial `40457c6adb381928e4b5fef6ed459ed291edd5e2`; Windows x64 según sesión del usuario y baseline de identidad previamente acreditado |
| Renderer | Marcadores globales D3D12 L14/18/21/23. La consulta local del observador sigue siendo `renderer=NOT_VERIFIED`; se confirma el backend mediante el log del host |
| Observador | L66: v0.0.2, `DISARMED_NO_REGISTRATION`, build `3e441e7c7f09432d9cfb111c22596cb601000000`, Game epoch2. HostService2.2/LogService1.0 conservados del paquete y datos del usuario |
| Capturas | 28 completas, L1846–1897 (lista exacta en JSON), 196 registros E_OC; censo7 y truncado0 en todas |
| Fuera del contexto | Cuatro SKIP conservadores, L82/717/810/2179 |
| Recursos | `E_OC_registered=1`, `E_ocb_registered=1` en 28/28; `loaded=NOT_VERIFIED` en 28/28 |
| Cierre | L2181 cierre normal del observador; L2182 descarga normal de mods. Solo caso del observador, sin perfiles/actores propios |
| Severidad | INFO89, DEBUG1990, WARNING83, ERROR0, FATAL0. Las 83 advertencias son DDS/mipmaps, módulo textura; no se atribuyen a DEVF |
| Apariencia | El usuario confirmó Link y enemigos visibles y comportándose normalmente, sin congelamientos o problemas nuevos. Testimonio real, no una lectura de un flag de render |

Se cuenta el prefijo de severidad del host. Campos DEBUG con `error=4294967295` no son mensajes de nivel ERROR.

## Contexto y actores originales

Invariantes en 28/28: stage `F_SP121`, room3, **logical6, current0, link_owner5, room_node102, room_owner5, room_child_layer6**, room_creates0 y room_deletes0. Son datos diferentes: logical selecciona registros de escenario; current es el contexto del update; owner/child identifican el árbol del motor. La igualdad numérica logical6/child6 en esta sesión no los convierte en un mismo concepto ni hace persistente el ID6.

| ID de esta sesión | Room | Owner | home.angle.x | Interpretación estática |
|---|---|---|---|---|
| 158,159,160,163 | 3 | 6 | 296 | E_OC2, rango4000 |
| 161 | 3 | 6 | -216 | E_OC normal, rango4000 |
| 162 | 3 | 6 | -236 | E_OC normal, rango2000; preset seleccionado |
| 172 | 3 | 6 | 281 | E_OC2, rango2500 |

Los mismos siete IDs aparecen en todas las muestras, con parametersFFFFFFFF. Primera muestra consistente, dentro del redondeo del logger, con los siete registros ACT6 del [checkpoint de selección](../CP01_A1_PREFLIGHT/evidence/selection-static.json). No se tratan sus emplazamientos como huecos libres. Las muestras posteriores registran movimiento; sus agregados espaciales están en [EOC_POSITION_SAFETY](EOC_POSITION_SAFETY.md).

### IDs220/221: incertidumbre conservada

El host registra `fpcBs_Create` para E_OC220/221 en L1513/1517. No están en ninguno de los censos válidos de room3. Es un mensaje del inicio de creación; no prueba phase completada, vida posterior, room, owner ni origen de la solicitud.

Los mensajes ROOM_SCENE incluyen IDs102/103/104 en L982/986/990. Solo102 queda asociado a room3 mediante el observador. Las otras habitaciones no se identifican en esos mensajes. Los datos de room3 común/ACT6 previamente recuperados contienen los siete E_oc seleccionados; no aportan una correspondencia para220/221. Datos de otras salas y el contexto de esas solicitudes no están disponibles. **Origen de220/221 NOT_VERIFIED**: no se atribuyen a DEVF, Randomizer ni a una habitación concreta. G2 no llamó StageService ni un spawner.

## Baseline no aislado y límites

Luau Support oficial y Randomizerv1.0.6 estaban activos (L67/68; inicialización Randomizer L69), además del observador. L46 registra **1867 reemplazos de textura**. La sesión no fue aislada; ni los movimientos ni las advertencias permiten atribuir efectos específicos a Randomizer o DEVF.

PASS_RUNTIME_OBSERVED cubre observación y cierre normal del lector en esta sesión. No cubre nueva creación, propiedad de una adición, índice/modelo/BCK íntegros, envolvente, colisión de una adición, transiciones/limpieza de esta, descarga dinámica de perfiles personalizados ni ejecución de G5. No se ejecutó el juego durante G4.
