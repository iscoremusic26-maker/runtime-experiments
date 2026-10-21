# Continuidad — CP-R05

Fuente upstream `40457c6adb381928e4b5fef6ed459ed291edd5e2`, árbol `e4b79b565b2842f711f7c9f2390f56ef11063157`. Objetivo: Dusklight 2.0.3, Windows x64, DirectX 12, GZ2E01 USA. Repositorio privado `iscoremusic26-maker/Mods-Duskligh`; continuar la rama exacta `research/dusklight-203-dusk-atlas`.

Padre remoto comprobado de este checkpoint: CP-R04 `201a2880d667cbf1d02fe5bc9ba53fcf24ac4f2a`. El SHA que contiene este handoff se consulta en el HEAD/historial; no se fabrica autorreferencia. R01 `f163cfc605ff92757aef3c5f7b492a1e63ef7459` publicó SDK/hooks/loader; R02/R02a incorporó world/save y corrigió una referencia de sistema; R03 `b2278941d931d71463a3410d2c7668da1e297d19` recuperó los demás informes; R04 contrastó cancelación de callbacks.

## Qué está publicado

19 fichas de sistemas, arquitectura, contratos SDK, hooks/ABI, integración, dependencias, riesgos, preguntas y evidencia histórica. Totales: 184 evidencias, 202 registros de símbolos; 28 entradas canónicas incluyen soporte e histórico y no son 28 sistemas gameplay comprendidos. R00 conserva sus 19367 archivos / 488 directorios; INVENTORY_ERRATA aporta siete correcciones sin duplicar el índice.

R05 añade síntesis y una comprobación del scheduler: en el camino normal las colas de borrado/prioridad/creación preceden execute/draw; gates de captura/error y separatePresentation impiden generalizar a todo frame. R04 distingue snapshot Save de revalidación de handles Host/Camera; no garantiza cancelación inmediata ni autoriza liberar userdata por analogía. Save callback antecede al flush de sidecars; StageService retira registros sin borrar actores ya vivos. ABI Windows, disponibilidad de símbolos y runtime siguen sin certificar.

## Primera acción exacta de la próxima sesión

1. Consultar HEAD remoto actual y leer README, AGENTS, este handoff y RESEARCH_COVERAGE. No asumir el SHA anterior ni sobrescribir una punta nueva.
2. Leer la ficha `systems/callback_ownership_and_cancellation.md` y las evidencias CALLBACK-001..004. Estudiar **una** ruta adicional de ItemService o MessageService: registro, snapshot/lookup, callback, cancelación y detach; incluir un consumidor del juego y sus límites. No repetir Save/Host/Camera ni todo el inventario.
3. Documentar solo la conclusión sustentada, actualizar ledger/índices/preguntas/cobertura y publicar CP-R06 de inmediato. Mantener los rangos del SHA fijado y verificar archivo remoto y diff antes de ampliar otra lectura.
4. Después alternar huecos de OPEN_QUESTIONS: bootstrap/title y gates, modelos/HUD/fonts, ambiente, NPC/puzzles/minijuegos o soporte del port. No convertir un actor histórico en el centro de la campaña.

## Herramientas y persistencia

La copia certificada de esta sesión está en `work/source/dusklight-2.0.3`; el atlas de trabajo en `work/atlas/DUSKLIGHT_RESEARCH`. Son rutas efímeras, no requisitos del atlas. Los borradores recuperados ya están publicados. Cambios locales experimentales de clasificación de inventario de la sesión anterior no sustituyen los archivos remotos R00: usar el TSV remoto más INVENTORY_ERRATA; no republicar esos borradores ni rehash masivo.

Validación: `python DUSKLIGHT_RESEARCH/tools/validate_atlas.py RUTA_FUENTE_CERTIFICADA`. El script escribe VALIDATION_REPORT en su propia carpeta y no muta la fuente. Comprobar salida exitosa antes de cualquier escritura remota; una validación fallida impide publicar hasta reconciliar referencias.

Git/gh no fueron la vía operativa; usar conector GitHub. Releer HEAD, crear árbol sobre su tree SHA, commit con ese padre, actualizar ref sin force y con expected_sha. Si cambia el HEAD, releer y reconciliar. Solo escribir bajo DUSKLIGHT_RESEARCH. No crear PR nuevo, merge, tag o release; no tocar upstream, SDK, producción, PR #80/#81, CI #65/#66 ni otras ramas. No subir prompts, fuentes completas, secretos ni assets originales.

Persistir una contribución útil cada 3–5 minutos de trabajo activo, antes de tareas costosas. Limitar a 2–3 lecturas paralelas cuando ya haya checkpoint seguro y publicar sus archivos antes de abrir nuevas subtareas. El límite de sesión no es una autorización para declarar completo lo que no quedó versionado.

## Límites permanentes de esta campaña

Cuatro submódulos ausentes (SOURCE_PIN), byte mismatch Android excluido, TARGET_PC cambia estructuras y no hay medición ABI Windows nueva. No se ejecutó el juego ni un mod. Modelos/HUD/clima/minijuegos y otras áreas mantienen muestreo indicado en SYSTEM_INDEX. Las observaciones CI históricas conservan SHA/alcance y no se promueven a runtime.

NO MOD IMPLEMENTED / NO GAME RUNTIME CLAIMED / NO PRODUCTION MODIFIED. No hay tarea en segundo plano ni continuación programada.

Texto para reanudar: «Continúa el atlas desde el HEAD actual de research/dusklight-203-dusk-atlas. Lee DUSKLIGHT_RESEARCH/CONTINUATION.md y ejecuta su primer flujo pendiente, con checkpoint breve; no repitas R00 ni implementes mods».
