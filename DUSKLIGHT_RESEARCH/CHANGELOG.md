# Checkpoints documentales

## CP-R00 — auditoría e inventario

Campaña iniciada el 20 de octubre de 2026 (zona del usuario: America/Panama; registros de herramientas en UTC del día 21). Se verificaron repositorios, rama base privada, commit/tag upstream y bytes de los árboles locales. Se creó una rama aislada desde CP00 y se inventariaron 19367 archivos sin modificar fuente. Se identificaron cuatro submódulos ausentes y una discrepancia Android explícitamente excluida de afirmaciones técnicas. Los informes profundos se incorporarán en checkpoints posteriores, conservando sus niveles de evidencia.

No se ejecutaron compilaciones, CI nuevas ni el juego. No se creó un mod, tag, release ni merge. El prompt no forma parte de estos documentos.

## CP-R01 — recuperación y primer contenido técnico (21 de octubre de 2026)

Continuación desde HEAD remoto CP-R00 verificado. Recuperados informes de hooks/loader y SDK, contrastados y publicados con evidencia y símbolos. Se precisó la métrica: 26 candidatos de módulo, sujetos a disponibilidad; 25 contratos C y 209 ranuras públicas actuales. Se documentan rollback de init fallida, replace de slot único, orden de ticks y límite de cleanup de actores propios. Sin repetir inventario, compilar ni ejecutar juego; sin PR nuevo.

## CP-R02 — escenas, guardado, bancos de estado y narrativa

Integrados borradores recuperados tras revisión de SaveService/StageService y consumidores. Cinco fichas, 33 evidencias nuevas y símbolos; correcciones sobre TGSC (assert histórico inactivo PC) y rangos acumulados de switches. No se equipara callback de guardado con durabilidad de sidecars ni retirada de edición con borrado de actor vivo.

CP-R02a: validación de relaciones detectó sistema de física no declarado para un símbolo KCL; índice corregido y referencias,IDs y rangos comprobados. Se consolidó el handoff acumulado.
