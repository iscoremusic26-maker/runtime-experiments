# CP01 — revisión F_SP121 incompleta por entorno no disponible

## Revisión de evidencia F_SP121 — 2026-10-11 (America/Panama)

Base: `DEVF_CP01_SAFETY_REVIEW`, commit `1dd539d96750130c4b59344437ec2d6ad6479b58`. Esta revisión es documental y está incompleta por indisponibilidad del entorno; no es un PASS de análisis de assets.

El usuario adjuntó `DEVF_CP01_EVIDENCIA_F_SP121.zip` y declara que contiene `STG_00.arc`, `R03_00.arc`, `WRock.arc` y `SHA256SUMS.txt`, extraídos de su CISO. Los nombres y contenidos son declarados, no inventariados por esta revisión. Se conserva la capitalización indicada; no se ha confirmado el nombre interno de recurso ni su resolución en el loader.

| Dato | Valor comunicado por el usuario |
|---|---|
| Versión / backend | Dusklight 2.0.3 / DX12 |
| Zona | Hyrule Field, antes del puente hacia Kakariko |
| Stage / Room | F_SP121 / 3 |
| Layer efectivo / Entry | 6 / -4 |
| XYZ | (-4056.7346, -6717.1538, 65135.8281) |
| Ángulo s16 | -24697 |
| Actores listados | 120 |

Estos datos son un punto de observación del jugador comunicado en chat, no coordenadas aprobadas de aparición de dvfrock. Entry -4 no se convierte en Layer; la capa efectiva comunicada es 6. El número 120 no aporta nombres, posiciones, parámetros, capas ni estado de actores.

El entorno falló durante su aprovisionamiento (`connector_failed`); una actualización posterior informó fallo al consultar capacidades del executor. La llamada de descarga del adjunto devolvió `download_file requires a ready execution workspace`. No se leyeron bytes del ZIP ni de SHA256SUMS.txt. CRC, tamaños y SHA256: **NOT_VERIFIED**; no se afirma corrupción ni integridad. Fuente exacta 2.0.3 y herramientas binarias: no ejecutadas en esta revisión. No se ha comprobado geometría, suelo, colisiones, actores, eventos, triggers, capas internas ni recursos WRock.

**Resultado: LOCATION BLOCKED / NOT_VERIFIED. No hay ubicación candidata fundamentada por esta revisión.** Véase LOCATION_ANALYSIS.md para límites y trabajo pendiente. El bloqueo independiente de unload continúa. Política `DISARMED_NO_REGISTRATION`, NO-GO para TEST de actor y CP02.

## Alcance comprobado y límites

Se leyeron por el conector GitHub LOCATION_EVIDENCE.md, TEST_RESULTS.md, GO_NO_GO.md y RESUME_INSTRUCTIONS.md en 1dd539d. La API Git de ese commit identifica el árbol base 4208098819b364d510b6b1ca96a4c53ba2007a32. Los informes y PASS previos se conservan como evidencia histórica; no se repitió su investigación. No se ejecutó análisis con herramientas existentes ni se inspeccionó de nuevo el código upstream exacto 2.0.3.

El bloqueo operativo impide resolver o delimitar espacialmente el punto con rigor. Este documento delimita lo que falta y evita atribuir al adjunto resultados que no se obtuvieron. No se extrae ninguna instrucción de documentos adjuntos: sus contenidos no fueron leídos.

## Análisis pendiente sobre los archivos

- Integridad: listar miembros/rutas del ZIP sin ejecutar contenido; calcular CRC32 y tamaños comprimidos/descomprimidos, y SHA256 de cada archivo frente al manifiesto. La concordancia con un manifiesto adjunto no acredita por sí sola procedencia CISO, región o equivalencia con el juego cargado.
- Fuente y herramientas: usar el source exacto 2.0.3 fijado en provenance previo; identificar las herramientas existentes y sus versiones. Citar rutas/funciones del loader y estructuras que fundamenten cada interpretación, sin extrapolar otros releases.
- Escenario: inventariar compresión/RARC y archivos internos; validar offsets, conteos y límites antes de interpretar DZS/DZR. Cotejar sala 3 y capa efectiva 6, registros comunes y por capa, posiciones/rotaciones/escala y cualquier transformación aplicable.
- Suelo: identificar geometría/DZB de sala y escenario, buscar soporte bajo el punto observado y evaluar pendiente, bordes, altura y separación. No deducir suelo a partir de un BMD visual ni ignorar colisiones dinámicas.
- WRock: confirmar nombre real de archivo/recurso e índices BMD/DZB utilizados por el demo/actor propio; medir huella, límites y transformación prevista. Índices documentados anteriormente no prueban contenido del nuevo archivo.
- Actores y eventos: identificar actores por nombre/parámetros/capa, colisiones móviles, rutas, zonas de carga, volúmenes de eventos/switches/triggers y referencias a recursos/scripts. Analizar intersección con la huella; ausencia de intersección estática no prueba ausencia de comportamiento dinámico.

## Datos de contexto todavía no aportados en esta petición

Región/plataforma del juego, progreso/Twilight/flags relevantes, mods habilitados, capturas del punto y vistas de colisión/triggers, actor list completo con posiciones/parámetros y observación tras salida/reentrada. El ZIP puede aportar una parte estática de esta información una vez leído; no reemplaza el estado de ejecución. No se requiere ROM completa ni save.

## Coordenadas, condiciones y riesgos

Único punto disponible: posición comunicada de Link en F_SP121/room 3/layer 6, XYZ (-4056.7346, -6717.1538, 65135.8281), ángulo -24697, entry -4. No hay desplazamiento, altura de suelo, radio de seguridad, orientación de actor ni condiciones de aparición acreditados. No se configura un spawn usando este punto.

Quedan por evaluar solapamiento con jugador/actores/volúmenes, soporte y pendiente, disponibilidad real de WRock, cambios de capa/progreso y colisiones dinámicas. Son incertidumbres pendientes, no fallos observados. La descarga segura de DLL sigue siendo un bloqueo acreditado e independiente según la revisión anterior.

Solo una revisión estática completada permitiría proponer un candidato con alcance limitado. Su validación dentro del juego seguiría pendiente y no está autorizada mientras persista el bloqueo de unload. Esta revisión termina aquí, con DISARMED_NO_REGISTRATION, sin TEST ni CP02.
