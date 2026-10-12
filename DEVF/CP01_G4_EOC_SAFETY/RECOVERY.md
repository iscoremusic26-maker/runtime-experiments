# Recuperación del checkpoint G4

Estado final: **G4_BLOCKED_WITH_EXACT_NEXT_INPUT**, **NO_SAFE_POSITION_VERIFIED**, `DISARMED_NO_REGISTRATION`, G5/CP02 NO-GO. Ninguna implementación o compilación nueva, ni ejecución del juego, cambios de host, StageService, perfiles, saves, flags o recursos originales.

## Identidad y alcance

Repositorio privado `iscoremusic26-maker/Mods-Duskligh`. Rama nueva `review/devf-cp01-g4-eoc-safety`, base exacta `1990f3137553c0f2aec43f66eeda55746fc8cc2e`, tag base `DEVF_CP01_G2_READONLY_PACKAGE`. Checkpoint previo `2124adddae1e4433f7523e777cf0a773b2119bb2`/`DEVF_CP01_A1_PREFLIGHT_G0_G4`. Código G2 compilado `b3ed281cbcb5934b7a8bd7d78b5adcef19b09ad2`, intacto.

Nuevo tag de recuperación: **`DEVF_CP01_G4_EOC_SAFETY_REVIEW`**. Su commit exacto se obtiene con `git rev-parse DEVF_CP01_G4_EOC_SAFETY_REVIEW^{commit}`; el tag representa revisión BLOCKED, no PASS. El commit y enlace del PR draft se entregan al usuario tras publicar/verificar. No se mueven tags previos ni se modifica el PR7; no merge. PR nuevo contra `package/devf-cp01-g2-readonly` para mostrar solamente el incremento G4.

Fuente original consultada: `TwilitRealm/dusklight@40457c6adb381928e4b5fef6ed459ed291edd5e2`, checkout limpio e independiente `work/dusklight-v203-baseline`; Aurora3227d76. No se utilizó el checkout experimental parcheado. Hashes de funciones consultadas en [g4-aggregates.json](evidence/g4-aggregates.json).

## Evidencia conservada y nuevas herramientas

- Informes de selección/ubicación/gates en `CP01_A1_PREFLIGHT`, geometría/colisiones/rutas/Digpl en `CP01/evidence`, arquitectura A1 en `CP01_DAWNLIGHT_AUDIT/SCENE_OWNERSHIP.md`, build/seguridad del observador en `CP01_G2_READONLY_PACKAGE`. Se citan sin editar el historial ni repetir sus suites.
- Adjuntado anonimizado privado:183907 bytes,2182 líneas, SHA256 `d19f2760e695f48f4df59706b791de121ffe77806bdafde8a7539b2cdc2b78b4`. Conservado completo en scratch privado, incluidas28 capturas. El hash del original distinto es solo reportado, no verificado. **No publicar log completo ni su reconstrucción**, aunque sea anonimizado.
- Inputs privados main9f95a34; ZIP originales y ARC anteriores permanecen en ese repositorio/scratch, nunca añadidos a este cambio. No E_OC/E_ocb disponibles.
- Herramienta nueva [analysis/review_g4.py](analysis/review_g4.py): stdlib Python, lee el log privado, exige hash/tamaño/28 capturas/contextos/196 registros, calcula solo agregados muestreados; inventaría nombres ZIP/nested `.dusk` y registra hashes del fuente y evidencias anteriores. No decodifica de nuevo KCL/ARC ni ejecuta código nativo. No modifica entradas.
- Única evidencia JSON nueva: agregados sanitizados, conteos, líneas de referencia, inventario y hashes. No posiciones completas de las28 capturas, texto del log, recursos binarios o direcciones de memoria.

## Reproducción offline

Conservar localmente los insumos privados; si el entorno temporal desaparece, recuperar los **resultados derivados** desde el tag. El log no está en Git y requerirá una copia privada de exactamente el adjunto anonimizado para reproducir sus agregados; no sustituirlo por el original con otro hash. No repetir SDK/CP00, Dawnlight o pruebas47 del observador.

Desde el checkout del proyecto, adaptando exclusivamente ubicaciones locales de lectura:

```bash
python DEVF/CP01_G4_EOC_SAFETY/analysis/review_g4.py \
  --log /workspace/work/devf-g4-eoc-safety/private/DEVF_G2_log_sin_rutas_personales.txt \
  --inputs /workspace/codex-cp00-inputs \
  --source /workspace/work/dusklight-v203-baseline \
  --output /workspace/work/devf-g4-eoc-safety/reproduced-aggregates.json
cmp DEVF/CP01_G4_EOC_SAFETY/evidence/g4-aggregates.json \
  /workspace/work/devf-g4-eoc-safety/reproduced-aggregates.json
```

Comprobación incremental ejecutada: **PASS_OFFLINE**, hash/tamaño/líneas,28 capturas completas,196 registros válidos, capas y parámetros coherentes, advertencias/severidad, inventarios, fuente original y hashes de evidencia reutilizada. Rechazo de una copia alterada del log: PASS_OFFLINE de fallo cerrado, sin generar salida. Son validaciones de evidencia, no de render/colisión/creación ni pruebas del juego.

Controles del cambio: solo este directorio nuevo; sin EXE/DLL/ARC/ROM/saves/log añadido; antiguos archivos idénticos a la base; árbol fuente oficial intacto. Workflows históricos filtrados por otras rutas, sin dispatch ni compilaciones nuevas. Validación de enlaces locales/documentos, JSON, sintaxis Python y whitespace; publicación seguida de fetch en repositorio independiente para comprobar commit/tag recuperables. Comprobar la disponibilidad remota al reanudar:

```bash
git fetch origin refs/heads/review/devf-cp01-g4-eoc-safety refs/tags/DEVF_CP01_G4_EOC_SAFETY_REVIEW
git rev-parse DEVF_CP01_G4_EOC_SAFETY_REVIEW^{commit}
git merge-base --is-ancestor 1990f3137553c0f2aec43f66eeda55746fc8cc2e DEVF_CP01_G4_EOC_SAFETY_REVIEW
git diff --name-status 1990f3137553c0f2aec43f66eeda55746fc8cc2e DEVF_CP01_G4_EOC_SAFETY_REVIEW
```

## Continuación mínima, sin reiniciar el estudio

Leer [G4_GATE_DECISION](G4_GATE_DECISION.md) y pedir/recibir solamente los dos ARC y manifiesto privado conforme [EOC_RESOURCE_VERIFICATION](EOC_RESOURCE_VERIFICATION.md). Verificar nuevos bytes/SHA/CRC/estructura, reutilizar decodificadores propios y estudiar modelo/arma/BCK/joints. No repetir integridad ARC antiguos, geometría WRock/Digpl, auditoría DLL o observación G2 histórica. Continuar comparación incremental de envolvente/terreno una vez exista una cota fundamentada. No asumir que obtener los archivos completa G4.

El punto anterior sigue sin aprobación para E_OC; no fabricar coordenadas. Entrada/salida natural, progresión, aislamiento, nueva identidad/propiedad/render/colisión/cleanup requieren revisión específica y, para ejecución, autorización posterior. Bloqueo independiente de descarga DLL conserva su estado previo. Detenerse al concluir esta revisión: no G5, G6 o CP02.
