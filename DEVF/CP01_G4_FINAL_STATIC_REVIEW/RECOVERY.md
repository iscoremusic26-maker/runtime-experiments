# Recuperación — G4 final static review

Estado: **G4_RESOURCE_VERIFIED_POSITION_BLOCKED / NO_SAFE_POSITION_VERIFIED**. Exclusivamente lectura/análisis offline; sin host/mod/observador modificados, compilación, ejecución de juego, spawn, registro, StageService, A2, hooks, cambios de partida o recursos. DISARMED_NO_REGISTRATION. G5/CP02 NO-GO y descarga DLL independiente intactos.

## Identidad

Repositorio privado `iscoremusic26-maker/Mods-Duskligh`; base exacta **dc2f65ab5d1423ce74d78661dbbea5e14a692409**, tag base `DEVF_CP01_G4_EOC_RESOURCE_CONTINUATION`, PR9 draft sin merge. Rama independiente **`review/devf-cp01-g4-final-static-review`**, tag nuevo **`DEVF_CP01_G4_FINAL_STATIC_REVIEW`**. El commit exacto del nuevo checkpoint se resuelve con `git rev-parse DEVF_CP01_G4_FINAL_STATIC_REVIEW^{commit}`; su hash/enlace y PR independiente se entregan tras publicación/verificación. PR contra rama anterior para mostrar solo el delta. Sin merge, force push o movimiento de tags/ramas históricos.

Fuente consultada limpia: `TwilitRealm/dusklight@40457c6adb381928e4b5fef6ed459ed291edd5e2`, checkout baseline original. Se limitaron lecturas a OverlayService/ciclo de sync/FST/archive members/texturas; decisiones E_OC de movimiento/detección/medio/social; reglas layer, RTBL/SCLS/scnChg y lifetime natural de ROOM_SCENE. Hashes de funciones/archivos relevantes en [focused-review.json](evidence/focused-review.json).

## Qué se conserva sin repetir

Del checkpoint anterior: integridad privada de E_oc/E_ocb91884d5, modelos3/4,28 BCK,18975 segmentos,182 diagnósticos y cotas401/494/501; soporte/geometría de31 prismas, paredes645.858/742.278 y ARC externos; G2/censo/owners, Digpl/rutas/WRock, SDK/ABI/builds y bloqueo DLL. Los hashes de los tres JSON anteriores se registran, sin recalcular sus resultados.

No se descargó ninguna entrada privada nueva, no se abrió un ARC/BCK/BMD o KCL, no se reconstruyeron joints ni se volvieron a procesar las28 animaciones o31 prismas. Los ZIP originales, game assets y log permanecen privados fuera de Git. Los cinco informes nuevos citan el historial; no se editaron informes antiguos.

## Delta realizado y herramienta

[analysis/focused_review.py](analysis/focused_review.py), stdlib Python, sin código nativo:

1. Busca exclusivamente mensajes de overlays y nombres de carga en el log anonimizado íntegro; verifica su hash de referencia, publica conteo/line70, **sin texto del log**. No vuelve a censar las28 capturas.
2. Lee solamente nuevos campos **RTBL/SCLS** en stage.dzs/room.dzr ya extraídos, verifica su pequeño hash contra inventario previo. Usa stride13 de SCLS oficial; corrige la interpretación futura del metadata antiguo12 sin modificarlo. No es una repetición de integridad ARC/ZIP.
3. Calcula distancias nuevas de Link a sectores ya calculados (16 evaluaciones/98 refinamientos), usando **JSON numérico privado conservado** de capturas. No genera puntos o grids nuevos, ni publica posiciones completas de capturas; solo conteos/mejor mínimo de cribado. No recorre otra vez el censo o log G2.
4. Registra fuentes y hashes de evidencia reutilizada; la cota voluntaria800 es derivación acotada de fuente bajo guardas documentadas, no simulación del engine ni prueba Windows.

Resultado nuevo: overlays de mods aplicados vacíos **PASS_RUNTIME_LOG** durante G2; mecanismos dinámicos conocidos; registros de textura independientes; bytes efectivamente cargados siguen PARTIAL/NOT_VERIFIED, sin convertir esta limitación en el único bloqueo. RTBL demuestra que2/4 retienen3; SCLS tiene3 destinos de stage y7 de room3. Fuente social E_OC no tiene filtro room; globalcenso/sensores/transición/progreso no están en el log actual.

## Reproducción focalizada

Mientras exista el scratch privado anterior, desde el checkout:

```bash
PYTHONDONTWRITEBYTECODE=1 python DEVF/CP01_G4_FINAL_STATIC_REVIEW/analysis/focused_review.py \
  --private-log /workspace/work/devf-g4-eoc-safety/private/DEVF_G2_log_sin_rutas_personales.txt \
  --private-captures /workspace/work/devf-g4-eoc-safety/private/captures-private.json \
  --location-cache /workspace/work/cp01-location \
  --source /workspace/work/dusklight-v203-baseline \
  --output-dir /workspace/work/devf-g4-final-static/reproduced
cmp DEVF/CP01_G4_FINAL_STATIC_REVIEW/evidence/focused-review.json /workspace/work/devf-g4-final-static/reproduced/focused-review.json
```

Este comando reproduce solo el incremento, no decodificadores/modelos/KCL. Si se pierde el entorno, los resultados se recuperan del tag sin solicitar originales por rutina. Reproducir el delta requiere log privado, JSON numérico privado y DZS/DZR del cache; si falta alguno, declarar la parte no reproducible, conservar los resultados publicados y no usar extractos para demostrar ausencia de mensajes en el log completo. No se publica ni reconstruye aquí el log.

## Validación y publicación

Validaciones específicas documentadas en [offline-validation.json](evidence/offline-validation.json): empaquetado13 y campos de SCLS, sentinel de layer15→-1, room firmado, rechazo de stride truncado; RTBL/retención3 consistente; overlay único0 anterior a capturas; coherencia de derivación voluntaria acotada (sin ejecución nativa); JSON/AST/enlaces/alcance y hashes anteriores intactos. No tests G1/G2 o suites antiguas repetidos.

Se revisa el diff: únicamente este directorio nuevo, archivos textuales propios, sin ARC/modelos/animaciones/EXE/DLL/ROM/saves/logs. Fuente oficial y archivos históricos intactos, branch deriva exactamente de la base. Workflows anteriores no corresponden a estos paths y no se hace dispatch. Publicación branch/tag/PR draft seguida de fetch en Git independiente, comparación de blobs/parent y checks de refs anteriores; no merge.

## Siguiente paso mínimo

Leer [G4_GATE_DECISION](G4_GATE_DECISION.md) y [POSITION_CONTEXT_REVIEW](POSITION_CONTEXT_REVIEW.md). **No pedir de nuevo ARC o confirmación general de overlays**: el servicio aplicado durante G2 está cerrado. Usar solo evidencia existente que identifique progreso/Twilight/entrada/override, sensores/Link y censo E_oc global relevante, y secuencia natural de retirada/recreación de room3. Si falta, documentar observación baseline futura pendiente de autorización separada; no crear módulo ni ejecutar el juego por este checkpoint. No se necesita reabrir SDK, animaciones, KCL completo, Dawnlight o descarga DLL. La tarea se detiene en G4.
