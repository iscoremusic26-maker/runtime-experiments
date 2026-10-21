# Cobertura — CP-R01

R00 conserva 19367 rutas inventariadas; no se recalcularon hashes ni se rehízo el inventario en esta continuación. Se recuperaron borradores técnicos y se contrastaron init fallida, teardown y replace contra el código fijado.

**CROSSCHECKED selectivo:** contrato/implementación de HookService y loader, orden de tick y ownership. Matriz de 25 contratos SDK con límites de implementación seleccionados; 26 candidatos de módulo, no 26 servicios necesariamente disponibles en un build. 209 ranuras públicas localizadas, sin afirmar auditoría individual de todas.

56 evidencias y 68 entradas de símbolos con referencias y firmas. Los niveles son los de cada registro. Ningún símbolo nuevo tiene resolución binaria ni ejecución Windows observada.

Borradores recuperados aún no incorporados en este checkpoint: mundos/guardado, jugador/física/actores, presentación/recursos, histórico y memoria. No cuentan todavía como cobertura publicada. El índice SYSTEM_INDEX describe solo las fronteras ya documentadas, no comprensión completa de esas áreas.

Pendientes: pruebas de disponibilidad binaria, callbacks reentrantes, teardown de actores propios que rechazan borrado, submódulos ausentes, bootstrap completo y semántica de áreas restantes.
