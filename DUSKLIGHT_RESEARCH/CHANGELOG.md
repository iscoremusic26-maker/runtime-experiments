# Checkpoints documentales

## CP-R00 — auditoría e inventario

Campaña iniciada el 20 de octubre de 2026 (zona del usuario: America/Panama; registros de herramientas en UTC del día 21). Se verificaron repositorios, rama base privada, commit/tag upstream y bytes de los árboles locales. Se creó una rama aislada desde CP00 y se inventariaron 19367 archivos sin modificar fuente. Se identificaron cuatro submódulos ausentes y una discrepancia Android explícitamente excluida de afirmaciones técnicas. Los informes profundos se incorporarán en checkpoints posteriores, conservando sus niveles de evidencia.

No se ejecutaron compilaciones, CI nuevas ni el juego. No se creó un mod, tag, release ni merge. El prompt no forma parte de estos documentos.

## CP-R01 — recuperación y primer contenido técnico (21 de octubre de 2026)

Continuación desde HEAD remoto CP-R00 verificado. Recuperados informes de hooks/loader y SDK, contrastados y publicados con evidencia y símbolos. Se precisó la métrica: 26 candidatos de módulo, sujetos a disponibilidad; 25 contratos C y 209 ranuras públicas actuales. Se documentan rollback de init fallida, replace de slot único, orden de ticks y límite de cleanup de actores propios. Sin repetir inventario, compilar ni ejecutar juego; sin PR nuevo.

## CP-R02 — escenas, guardado, bancos de estado y narrativa

Integrados borradores recuperados tras revisión de SaveService/StageService y consumidores. Cinco fichas, 33 evidencias nuevas y símbolos; correcciones sobre TGSC (assert histórico inactivo PC) y rangos acumulados de switches. No se equipara callback de guardado con durabilidad de sidecars ni retirada de edición con borrado de actor vivo.

CP-R02a: validación de relaciones detectó sistema de física no declarado para un símbolo KCL; índice corregido y referencias,IDs y rangos comprobados. Se consolidó el handoff acumulado.

## CP-R03 — recuperación de fichas y síntesis de integración

Integrados13 informes recuperados de jugador/actores/presentación/memoria/histórico y matriz .dusk. Revisadas invalidaciones ARC,expectativas externas de texturas,sincronización Gfx condicionada y punteros de viento. Se conserva profundidad selectiva; no se promueve CI a runtime.

## CP-R04 — cancelación de callbacks y precisión de citas

Nueva lectura transversal: Save copia registros completos, Host revalida handles y Camera revalida handle+owner activo. Se documenta inferencia condicionada de userdata vencida sin afirmar fallo runtime. Cuatro evidencias y dos slots nuevos; corregido anclaje histórico CP00 de L15 a L12 tras consultar archivo exacto.

## CP-R05 — síntesis, dependencias y handoff

Añadidos ARCHITECTURE, SYSTEM_DEPENDENCIES, RISK_REGISTER, OPEN_QUESTIONS y métricas. ARCH-001 contrasta el orden del scheduler con sus gates. SYSTEM_INDEX incluye rutas, dependencias y estados; soporte inventariado se mantiene separado de áreas leídas. Siete erratas nominales corrigen branding/MemCard sin duplicar FILE_INVENTORY. Se precisa la diferencia entre ocurrencias y rangos únicos de referencias, y la fila AudioRes no afirma sync BST por frame frente a PRES-024. Índice maestro y handoff reescritos alrededor del estado publicado.

Esta continuación tuvo checkpoints cortos R01, R02/R02a, R03, R04 y R05, sin crear PR ni modificar producción. El intervalo inactivo entre sesiones no cuenta como investigación. Ver RESEARCH_METRICS para tiempo de sesión observado y límites de medición.

## CP-R06 — Item resolvers, snapshots y consumidor cofre

Contrastados contrato 2.3, registro/retirada, copia PendingResolve sin handle, orden por mod/vector, active-check y efectos de detach. Consumidor TARGET_PC daTbox_c::create1st enlaza la resolución a parámetros del cofre. Cuatro evidencias y tres símbolos nuevos. La cancelación tardía es inferencia condicionada; el contrato exige ausencia de efectos secundarios y no se promete reentrancia. Sin runtime, builds ni mod.
