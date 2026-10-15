# Segundo sitio — consulta incremental nueva, sin autorización de spawn

**SITE2_PENDING.** No se incorporó ningún XYZ a la whitelist. Sitio1 humano permanece (-1250,-6304.00830078125,60750), F_SP121/3/6, parámetrosFFFF0100 y contrato pitch/setID intactos. El punto antiguo (-4806…) mantiene NO_SAFE_POSITION_VERIFIED; no se consultó de nuevo.

## Evidencia ejecutada

[Windows Actions38744954662](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38744954662), job116456060543, SUCCESS; fuente/CI `98bbb027c91e4cabc9629f370971345c887a958c`, [PR25 draft](https://github.com/iscoremusic26-maker/codex-cp00-inputs/pull/25). Es Python de análisis estático en windows-latest, **no build MSVC, no DLL ejecutada ni gameplay**. Logs del job leídos por el conector; se extrajo el objeto CP06_SITE_REVIEW y se preservó metadata en [site-query-summary.json](evidence/site-query-summary.json). Sin artifacts ni originales subidos.

Se leyó únicamente R03_00.arc del ZIP LFS privado: SHA256 `dc53106667811c4cde18b35edb5279357f00ebecaef2f9de546aea9a5a2b06af` y CRC del miembro al leerlo. No se rehízo auditoría de tres ARC. Reutilizados sin cambios los decodificadores/query octree/half-planes anteriores; dos consultas NUEVAS elegidas a Z±1200 respecto del sitio1 observado para estudiar coexistencia en la misma sala/capa, sin asumir suelo. Las Y siguientes se **calcularon del KCL**, no son coordenadas de spawn admitidas.

| Consulta F_SP121/3/6 | Norte (preferida sólo para estudio) | Sur |
| --- | --- | --- |
| X/Z | -1250 / 61950 | -1250 / 59550 |
| Y suelo calculada | -6327.600450915229 | -6351.869361310774 |
| Prisma de soporte | 2281 | 2455 |
| Celdas / hojas / prismas decodificados | 38 /20 /57 | 17 /8 /48 |
| Huella±100: área sin suelo | 0 de40000 | 0 de40000 |
| Huella±501: área sin suelo | 0 de1004004 | 0 de1004004 |
| Alturas de huella501 | [-6374.855453,-6261.322710] | [-6452.265291,-6275.132032] |
| Pared más cercana ENTRE PRISMAS CONSULTADOS | 802.709079 | 1742.535856 |
| EvtArea: margen círculo conservador menos501 | +2152.530820 | -222.999576 |
| KY_chg acotado: margen análogo | +717.091504 | -366.322368 |
| ClearB / otro KY_chg en tabla heredada | BOUND_NOT_AVAILABLE | BOUND_NOT_AVAILABLE |

Soporte y prismas contribuyentes reportan PLC room3/ground0/special0/exit63, sin object/link-through ni normal_group. **PASS_STATIC de cobertura local** con tolerancias del lector, no certificación de todo terreno/caminabilidad. Distancia de pared es resultado local de celdas consultadas, no mínimo global de la sala. Radio501 es la pantalla conservadora histórica, no una demostración nueva de envolvente dinámica E_OC2; no se reabrieron BMD/animaciones.

Cotas por círculos reutilizan volúmenes autorados del JSON anterior (sin recalcular scripts/triggers). Un margen negativo del sur **no demuestra intersección real ni invalida definitivamente el punto**; impide demostrar separación mediante esa cota. Norte ofrece mejores cotas para esos volúmenes modelados. Sus records cercanos incluyen flwr7 a940.691/950.329 y Digpl-home a1025.914XZ: son centros de registros, **no los27 puntos Digpl ni una prueba de radio efectivo**. No se transfirió la distancia565.7 del candidato antiguo ni115.6 de su ruta al punto nuevo.

## Qué falta para acreditar norte

- **Consulta adicional ya resuelta por reutilización:** se calcularon en functions.exec/JavaScript distancias XZ del nuevo centro a AABB mundiales previamente publicados de los cuatro placements mmvbg/ClearB, incluidos initial-load y estados de render autorados. Fórmula y resultados en [external-bounds-reuse.json](evidence/external-bounds-reuse.json). Margen mínimo menos501: norte **7707.998506**, sur **9202.203462**, positivos para esos bounds/estados. No se decodificaron ARC ni se recalcularon transformaciones. Así se completa esa pantalla estática pese al BOUND_NOT_AVAILABLE de la tabla de volúmenes general; siguen pendientes movimiento futuro/efectos globales/ocupación y envolvente efectiva E_OC2. No se atribuye este cálculo al job Windows anterior.
- Consulta incremental de rutas, puntos discretos/zonas de interacción y entrada/salida para este nuevo dominio; los resultados previos de otro origen no prueban éstos. No se repite aquí la investigación de semántica Digpl.
- Contrastar huella/altura y dominio de movimiento efectivo E_OC2 con evidencia ya existente, progresión/eventos y carga efectiva de recursos en esa zona; KCL local y mismo room/layer no bastan. No se garantiza que dos enemigos permanezcan separados durante combate.
- Resolver identidad antes de dos activos; después validación humana de terreno/visibilidad/recursos/simultaneidad con paquete seguro. Ausencia de GPU por sí sola no es el bloqueo técnico actual.

No se pide al usuario otro ARC, repetir los cinco ensayos ni ejecutar un diagnóstico activo. Información geométrica mínima adicional es el contexto local de estos bounds/rutas y recursos efectivos, primero consultable offline en la evidencia privada existente; no otra extracción general. El soporte norte queda preservado para esa continuación focal, sin reclamar SITE2_ACREDITADO.
