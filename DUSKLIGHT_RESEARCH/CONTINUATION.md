# Continuidad — CP-R04

Fuente fijada: `40457c6adb381928e4b5fef6ed459ed291edd5e2`; árbol `e4b79b565b2842f711f7c9f2390f56ef11063157`. Objetivo: Windows x64 / DirectX 12 / GZ2E01 USA. Rama `research/dusklight-203-dusk-atlas`; padre remoto verificado CP-R03 `b2278941d931d71463a3410d2c7668da1e297d19`. El HEAD del commit que contiene este handoff se consulta en GitHub.

Publicados acumulados: matriz SDK, hooks/ABI, matriz de integración, 19 fichas (18 áreas previas más callbacks), histórico, 183 evidencias y 202 símbolos. CP-R04 añade contraste de cancelación Save/Host/Camera: Save retira de la lista viva pero mantiene snapshot ya copiado; no liberar userdata por asumir cancelación inmediata. Es análisis estático, no una prueba de fallo ni de concurrencia.

Primera acción siguiente: comprobar HEAD, leer cobertura y crear síntesis ARCHITECTURE, SYSTEM_DEPENDENCIES, RISK_REGISTER y OPEN_QUESTIONS a partir de las evidencias existentes; no repetir inventario o hashes. Después profundizar un hueco concreto, por ejemplo Item/Message y fin de callbacks. Todos los borradores técnicos recuperados ya están publicados; ningún mensaje de subagente se cuenta por sí solo como artefacto.

Límites vigentes: cuatro submódulos ausentes; layouts TARGET_PC sin medición Windows; ningún hook nuevo resolvió en el binario; ningún juego ejecutado. Modelos, HUD, clima y minijuegos conservan profundidad muestreada, indicada por ficha.

Persistir cada 3–5 minutos activos; no iniciar otra lectura sin salvar el bloque anterior. Máximo 2–3 estudios paralelos tras checkpoint seguro. Solo commits bajo DUSKLIGHT_RESEARCH; sin nuevos PR, merge, tags, releases o force. Usar conector GitHub con HEAD comprobado y expected_sha; verificar ref, diff y archivo remoto. No tocar producción, SDK, upstream, PR #80/#81 o CI #65/#66.

NO MOD IMPLEMENTED / NO GAME RUNTIME CLAIMED / NO PRODUCTION MODIFIED. No hay ejecución de fondo.
