# Recuperación — continuación G4 de recursos

Resultado: **G4_RESOURCE_VERIFIED_POSITION_BLOCKED / NO_SAFE_POSITION_VERIFIED**. Sin ejecución del juego, compilación nativa, mod/host modificado, perfiles, StageService, spawner o `.dusk` activo. No saves, flags, layers o recursos originales alterados. G5/CP02 NO-GO y bloqueo DLL independiente conservados.

## Checkpoints y fuentes

Base exacta `3e0792e90b6ebc764b421e56ab63a36df3157893`, tag `DEVF_CP01_G4_EOC_SAFETY_REVIEW`, PR8 draft sin merge. Rama independiente nueva **`review/devf-cp01-g4-eoc-resource-continuation`** en el repositorio privado `iscoremusic26-maker/Mods-Duskligh`. Nuevo tag **`DEVF_CP01_G4_EOC_RESOURCE_CONTINUATION`** identifica esta revisión BLOCKED, no un PASS. El commit se resuelve por el tag; el hash exacto/PR nuevo se entregan tras publicación y fetch independiente. PR contra rama G4 anterior para mostrar solo este incremento; no se mueve ningún checkpoint histórico.

Inputs privados: `codex-cp00-inputs`, rama `inputs/devf-cp01-g4-eoc-resources`, commit91884d5932377e15a96a9f1c8df48348751f37a5. Tres archivos en `DEVF/CP01_G4_EOC_RESOURCE_INPUTS/`, leídos mediante git show a scratch privado fuera del repositorio de código. No LFS pointers, no LFS pull necesario. Hashes/tamaños/manifiesto en [RESOURCE_INTEGRITY](RESOURCE_INTEGRITY.md); originales intactos, no publicados en código/PR/artefactos.

Fuente oficial limpia `TwilitRealm/dusklight@40457c6adb381928e4b5fef6ed459ed291edd5e2` en checkout baseline sin parche. Consultas focalizadas a loaders J3D, calc Maya/morph, interpolación Hermite, JNT/SHP/EVP y uso de modelos/arma/colliders E_OC. Hashes del fuente en evidencia nueva. A1, SDK, ABI, Dawnlight, G2, KCL/WRock/Digpl y unload previos conservados, sin repetir sus auditorías o pruebas.

## Scripts/evidencia nueva y reproducción offline

Dos herramientas propias stdlib Python, sin llamada nativa. [eoc_resources.py](analysis/eoc_resources.py) reutiliza Yaz0/RARC/VTX1 previos y añade solo decodificación/validación de skeleton, skin/palettes, curvas, cotas y diagnósticos necesarios. [reassess_position.py](analysis/reassess_position.py) consulta octree espacial limitado a501 y31 prismas, reutilizando soporte/half-planes/triángulo-caja; no reconstruye todo el KCL.

JSON derivados: [resources-envelope.json](evidence/resources-envelope.json), [position-query.json](evidence/position-query.json). Sin vértices, matrices bind completas, curvas, texturas, archivos originales o log publicado. El hash del JSON G2 reutilizado se conserva para demostrar el baseline de28 capturas; el log privado completo permanece intacto en su scratch previo y no se requiere para esta continuación.

Recuperar **solo los tres archivos nuevos** desde el commit privado (las credenciales Cloud/Git existentes funcionaron). Si fueran punteros LFS en una entrega posterior, resolver exclusivamente esos paths antes de verificar hashes. No descargar ZIP/SDK/ROM antiguos por rutina. Mantener las copias de análisis en carpeta privada fuera de Git; no modificar archivos fuente para hacer pasar lecturas.

Desde el proyecto, con inputs ya recuperados y cache geométrico anterior existente:

```bash
PYTHONDONTWRITEBYTECODE=1 python DEVF/CP01_G4_EOC_RESOURCE_CONTINUATION/analysis/eoc_resources.py \
  --inputs /workspace/work/devf-g4-eoc-resources/private \
  --source /workspace/work/dusklight-v203-baseline \
  --private-work /workspace/work/devf-g4-eoc-resources/private \
  --output /workspace/work/devf-g4-eoc-resources/resources-reproduced.json
PYTHONDONTWRITEBYTECODE=1 python DEVF/CP01_G4_EOC_RESOURCE_CONTINUATION/analysis/reassess_position.py \
  --location-cache /workspace/work/cp01-location \
  --envelope /workspace/work/devf-g4-eoc-resources/resources-reproduced.json \
  --output /workspace/work/devf-g4-eoc-resources/position-reproduced.json
cmp DEVF/CP01_G4_EOC_RESOURCE_CONTINUATION/evidence/resources-envelope.json /workspace/work/devf-g4-eoc-resources/resources-reproduced.json
cmp DEVF/CP01_G4_EOC_RESOURCE_CONTINUATION/evidence/position-query.json /workspace/work/devf-g4-eoc-resources/position-reproduced.json
```

Si el cache se perdió, recuperar la extracción privada previa R03_00.arc para la consulta **solo de la nueva región**, con el decodificador existente; no reejecutar CP00, WRock/Digpl o toda la auditoría KCL. Los resultados nuevos pueden recuperarse desde Git sin los bytes privados; recalcularlos exige esos inputs. No recrear ni sustituir los originales mediante headers.

## Validación específica de esta revisión

PASS_OFFLINE: SHA/tamaños/manifiesto, Yaz0/RARC/índices, dos BMD/28 BCK y skeleton compatibles;18975 segmentos continuos incluidos;55 matrices del cuerpo y1 del arma resueltas para las posiciones realmente usadas;182 poses diagnósticas dentro de las cotas. Geometría local31 prismas/19 celdas, cobertura Acch100 y circunscrito501, distancias de pared/techo y reutilización de colisiones/G2/Digpl con límites explícitos.

Comprobaciones específicas: curva sintética con extremos iguales y tangentes que producen un máximo interior (ambos tipos), rechazo de SSC con escala padre que atraviesa0, y rechazo de ARC alterado sin producir JSON. Ninguna equivale a PASS de render/colisión/spawn o del SDK. Reporte de resultados en `evidence/offline-validation.json`.

Antes de publicar se verifican JSON/sintaxis/enlaces/whitespace, alcance nuevo exclusivamente textual, hashes de recursos sin cambios y árboles anteriores idénticos. Sin suites históricas o workflows disparados manualmente; paths nuevos no corresponden a filtros de builds anteriores. Publicación de branch/tag/PR draft seguida de fetch en repositorio Git independiente y comprobación de parent, contenido y refs históricos; sin merge.

## Continuar sin repetir

### Recuperación durante esta misma tarea

La instrucción posterior de recuperación encontró el entorno y todos los resultados presentes: HEAD3e0792e, rama independiente ya preparada,9 archivos propios sin seguimiento, sin cambios staged o tracked; ninguna continuación publicada todavía. Se guardó una instantánea privada de nombres/tamaños/hashes antes de tocar los informes. Los dos scripts, los dos JSON, los cinco informes y el inventario/extracciones privados siguen disponibles. No hubo pérdida ni fallo de código demostrado; no se hizo reset/clean/force push.

Se revisaron las derivaciones, coordenadas, escala única HIO, matrices jerárquicas/arma y supuestos de morph/rotación. Se conservaron las cotas401/494/501 **en su dominio matemático condicionado**, no como límites del engine o del movimiento. Se recuperaron también el polígono501 cubierto y las distancias geométricas a4714/4734 ya calculadas después del aviso inicial de AABB; no se repitió esa consulta. Única corrección documental: el total de poses era182 (1 bind+1 WAIT+85 ATTACK_B+95 ATTACK_C), no185. No cambió ningún cálculo de recursos o KCL.

La recuperación valida archivos/hashes propios y fixtures focalizados sin reprocesar las28 BCK, volver a descargar ARC ni reconstruir los5326 prismas. Los comandos de reproducción anteriores son instrucciones para recuperación futura; no se ejecutaron por rutina tras esta instrucción de continuación.

Leer [G4_GATE_DECISION](G4_GATE_DECISION.md). No pedir de nuevo E_oc/E_ocb. La disponibilidad está cerrada; faltan recursos efectivos/override, condiciones de progreso/carga/acceso y dominio de movimiento que permita admitir una ubicación. La cota501 es relativa al origen en aritmética matemática, no un límite mundial ni certificado FP/runtime. Confirmar información existente y delimitar únicamente una revisión offline condicionada, según [POSITION_REASSESSMENT](POSITION_REASSESSMENT.md). No abrir el juego ni instalar/hacer aparecer nada mediante este checkpoint. Detenerse aquí.
