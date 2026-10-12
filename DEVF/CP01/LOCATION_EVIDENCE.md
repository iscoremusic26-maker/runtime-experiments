# Ubicación — bloqueo preciso y evidencia mínima Windows

## Inventario histórico de insumos anteriores (checkpoint 1dd539d)
Inventario dirigido, sin repetir CP00: los dos ZIP no contienen .dzs, .dzr, .arc, .dzb ni .bmd de juego. assets/ contiene 14879 archivos: 14876 encabezados .h, 2 PNG y 1 SVG. WRock.h define índices BMD=4 y DZB=7, pero no su geometría. No hay suelo, volúmenes de eventos, actores de sala ni modelo/collider binarios con los que validar el punto. Detalle y referencias en evidence/targeted-source-audit.json.

El demo oficial especifica F_SP108/room 0/layer -1 y posición (-14324, 0, 341). Esto es un candidato de referencia, no una ubicación declarada segura. Su aparición se registra por add_actor, no prueba ausencia de eventos, espacio suficiente ni disponibilidad de Wrock en la instalación.

El código getLayerNo_common_common muestra para F_SP108 decisiones por Twilight y flags 0x2008, 0x1E08, 0x0602 y 0x4510; no hay una única capa universal. getLayerNo(0) usa la sala actual y el override de entrada; el argumento numérico se ignora. layer=-1 de StageService coincide con cualquier capa: no usarlo como acreditación de un estado de progreso seguro. Entry no es Layer.

**Resultado: BLOCKED. No se elige ningún stage/room/layer/XYZ de producción.**

## Captura concreta sin instalar un mod
Estas acciones son manuales y de consulta; no se ejecutó nada en tu PC. Usar una copia de partida para observación y no usar controles que editen progreso. El propio juego advierte que las herramientas avanzadas incluyen opciones de escritura: limitarse a las vistas y comandos siguientes.

1. Iniciar tu EXE exacto Dusklight 2.0.3 con DX12. Capturar versión y backend en Ajustes; anotar región/plataforma del juego y qué otros mods están habilitados. No cambiar EXE/ROM ni instalar esta build.
2. Llegar normalmente a una zona ya accesible, fuera de una cinemática, combate o evento. Elegir un espacio llano y despejado; no un portal, puerta, transición, NPC o mecanismo. No guardar progreso como parte de la captura.
3. En Ajustes activar **Enable Advanced Settings**. Abrir herramientas con **Shift+F1** y escoger **Debug → Player Info**. Esta vista existe en el fuente 2.0.3 y muestra Stage, Layer efectivo, Position, Angle, Room y Entry. Capturarla con Link parado sobre el punto y con el entorno visible. No usar widgets de edición.
4. Como respaldo, abrir la consola con **/** y ejecutar únicamente:

```text
pos
angle
list
```

pos devuelve stage, room, entry y XYZ con cuatro decimales; angle sin argumento consulta el ángulo s16; list enumera actores/posiciones sin crear o borrar. No ejecutar tp, warp, spawn, kill, reset, setters o comandos de flags. Si la vista no existe en tu build, enviar captura del menú y versión en vez de adivinar valores.

5. Opcionalmente, para capturar geometría y volúmenes que el propio host conoce, usar únicamente vistas: **Debug → Collision View → Enable Terrain view**, y **Debug → Trigger View → Load Zones / Event Areas / Event Tags / Switch Areas**. Son flags de visualización transitoria, no setters de progreso. Capturar imágenes y volver a desactivarlos. No usar Save Editor, State Share para restaurar estado, Process Management, Actor Spawner, Development Mode ni edición de flags. Estas vistas ayudan a observar el estado real, pero no sustituyen la auditoría de assets/huella ni prueban ausencia de todos los scripts.
6. Guardar capturas al entrar y tras salir/reentrar normalmente sin DEVF, más un vídeo breve alrededor del punto. Anotar hora/estado Twilight/progreso relevante. Esto acredita datos observados y ayuda a delimitar una prueba; no prueba seguridad de un actor que aún no apareció.

## Archivos mínimos que faltan
Desde la imagen de juego que tu instalación utiliza, usando un explorador de disco/archivos que ya tengas y extracción de solo lectura, copiar a una carpeta de evidencia —nunca reemplazar originales—:

- /res/Stage/<stage observado>/Stg_00.arc
- /res/Stage/<stage observado>/R<room con dos dígitos>_00.arc; por ejemplo room 0 significa R00_00.arc. El número debe venir de Player Info.
- /res/Object/Wrock.arc, con el nombre/capitalización que realmente figure en tu imagen.

Los nombres se fundamentan en setStageRes, getRoomArcName y el actor demo. Exportar el archivo íntegro conserva stage.dzs/room.dzr, capas, registros y recursos de suelo/eventos; si el explorador muestra un nombre distinto, enviar el listado sin renombrar ni crear contenido. No se pide ROM completa, EXE, DLL retail ni saves personales. No modificar .arc, .dzs, .dzr o partida.

Obtener SHA256 de las copias con PowerShell, sustituyendo rutas reales:

```powershell
Get-FileHash -Algorithm SHA256 'C:\ruta\evidencia\Stg_00.arc'
Get-FileHash -Algorithm SHA256 'C:\ruta\evidencia\R00_00.arc'
Get-FileHash -Algorithm SHA256 'C:\ruta\evidencia\Wrock.arc'
```

Adjuntar solo estas copias y la captura; si una supera el límite de adjuntos, ponerla mediante Git LFS en el repositorio privado de insumos, conservando el hash, sin publicar assets de juego en un repositorio público. Si no tienes explorador/extracción disponible, enviar primero Player Info/console/capturas: no instalar herramientas ni usar una extracción destructiva por esta guía.

## Formulario de evidencia
Copiar y completar valores observados, dejando desconocidos como null:

```json
{
  "dusklight_version": "2.0.3",
  "renderer": "DX12",
  "game_region_and_platform": null,
  "stage": null,
  "room": null,
  "effective_layer": null,
  "entry_point": null,
  "position": {"x": null, "y": null, "z": null},
  "angle_y_s16": null,
  "progress_and_twilight_state": null,
  "enabled_mods": [],
  "screenshots_and_actor_list": [],
  "archive_sha256": {}
}
```

Con esa evidencia se podrán cotejar capa, geometría/huella de Wrock, suelo/altura, actores existentes y volúmenes/scripts, y limitar una prueba a ese estado de escena. Las capturas no sustituyen los binarios para una auditoría exhaustiva ni las pruebas de aparición/colisión posteriores. Resolver la ubicación no resuelve por sí solo la barrera de descarga del host.

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
