# QA humana dirigida — protocolo histórico
**Estado posterior, 15-10-2026:** CP07_2C_FIX_RUNTIME_PASS_USER_OBSERVED_WINDOWS_DX12, acotado a las dos sesiones A_ONLY/BOTH y la declaración del usuario. Ver [acta humana del 15-10-2026](HUMAN_RUNTIME_RESULTS_2026-10-15.md). No repetir este protocolo para cerrar la incidencia. Los pasos siguientes se conservan como referencia del plan previo; no acreditan mediciones ni todos sus subcasos.

## Protocolo conservado del build
1. Respaldar saves y JSON. Cerrar Dusklight por completo. DX12 / 2.0.3.
2. Sustituir únicamente proveedor 0.7.3 por 0.7.4. Reutilizar el MISMO Bokoblin Expansion 0.1.0 probado; retirar otros proveedores/probe. Conservar qa.json y placements.json (legacy NONE).
3. A_ONLY: localizar A, atraerlo con seguridad más allá del límite previo nominal de 600; explorar 1000–1500 o más sólo si se dispone de distancia fiable y terreno seguro. No informar medidas a ojo como medición.
4. Observar persecución y retirada prematura; después perder contacto y observar regreso. El retorno de executeWalk/home sigue permitido. Anotar visualmente y conservar log: los eventos de registro no identifican el estado de IA ni prueban píxeles.
5. Si A falla, parar y hacer rollback frío. Si es estable, BOTH: A+B, combate nativo, duplicados y reacción de grupo si se aproximan naturalmente. No inferir cooperación universal.
6. Cerrar, enviar observación y log para evaluar FIX_RUNTIME_PASS. Codex no ejecutó el juego. No repetir las pruebas históricas de aparición/retirada como requisito.
Rollback: cerrar, retirar 0.7.4, restaurar proveedor original 0.7.3 y JSON respaldados; conservar consumidor original 0.1.0. No hot unload: remove_actor_edit no destruye actores vivos.
