# Riesgos transversales y rollback

Riesgos derivados del commit fijado. No son fallos observados durante ejecución; se distingue contrato, fuente e inferencia en el [ledger](EVIDENCE_LEDGER.json). La mitigación es una condición para estudiar una futura integración .dusk, sin implementar un mod en esta campaña.

| ID | Riesgo y disparador | Evidencia | Mitigación / límite del rollback |
| --- | --- | --- | --- |
| R-01 | Usar offsets/tamaño GameCube o un STATIC_ASSERT histórico como ABI Windows | PLAYER-009 y HOOK-001/027; WORLD-033 | Verificar tipos/época/target exactos. No asumir padding, PMF ni vtables por comentarios. |
| R-02 | Init parcial cambia estado y devuelve error esperando shutdown | HOOK-016 | Revertir pasos propios antes de devolver fallo; shutdown solo corre si initialized quedó true. |
| R-03 | Replace takeover destruye el ganador previo; uninstall no lo restaura | HOOK-005/007 | Política de conflicto explícita; no prometer pila ni rollback al replace anterior. |
| R-04 | Actor propio no termina destrucción y mantiene callbacks mientras se retira DLL | SDK-001, HOOK-029 | Demostrar fin de instancias/callbacks; cleanup que registra un fallo no es barrera. No certificada estrategia universal de hot unload. |
| R-05 | Retirar observer libera userdata que un snapshot aún conserva | CALLBACK-001..004 y CALLBACK-007 | Separar retirada, fin de dispatch y liberación; no extrapolar cancelación Host/Camera a Save. |
| R-06 | Guardado vanilla confirmado pero sidecar falla o queda dirty | WORLD-011/012 | Datos propios versionados e idempotentes; tratar los errores de cada archivo, sin prometer transacción CARD+mods. |
| R-07 | Cambio de room/layer/escena invalida puntero de actor/path/model/archive | WORLD-003, PLAYER-025, PRES-004/006 | Revalidar identidad y contexto; limpiar caches; ownership del heap/archive define vigencia. |
| R-08 | Overlay retirado deja consumidor ya cargado con estado anterior | PRES-002..006 | Retirar registro propio y recargar consumidor cuando proceda; no borrar buffers ajenos ni prometer reversión instantánea. |
| R-09 | Tipo de registro TGSC/padding no coincide con tamaño aceptado por servicio | WORLD-033 | Usar contrato de bytes real y comprobar tamaño concreto del caller; sizeof Windows no medido aquí. |
| R-10 | Ejecutar servicio o usar GPU prestada fuera de callback/fase/hilo | PRES-010..013, HOOK-030 | Respetar game thread/render worker, no liberar device/queue prestados; detener trabajo propio antes de unload. |
| R-11 | Liberar con allocator/CRT incorrecto o mantener puntero al destruir solid heap | ROOT-001..006 y PRES-037/038/039 | Usar la pareja de ownership; JKR token/fallback no justifica liberar memoria de otro servicio. |
| R-12 | Booleano de ResourceService se interpreta como validación de argumentos | SDK-019, PRES-035 | Validar parámetros antes; retorno enum=5 se vuelve true en ramas inválidas. Solo discrepancia estática, sin fix productivo. |
| R-13 | Símbolo/target solo declarado se presenta como hook operativo | HOOK-010..012/026/028 | Verificar manifest, firma, dirección, aliases y entrada parcheable en la imagen concreta. Ningún target nuevo probado aquí. |
| R-14 | Singleton no nulo se confunde con recursos/audio listos | HIST-005/007/011 | Comprobar fase y recursos reales; informes históricos no certifican todos los estados ni observación audible actual. |
| R-15 | Actualización “por frame” usa tiempo de presentación para política de actor | ARCH-001, ROOT-007, HOOK-018 | Separar tick de simulación, execute de actor y presentación; pausa/captura/errores alteran rutas. |

Un rollback de registros no deshace mutaciones arbitrarias de inventario, flags, posiciones, archivos o servicios externos. Restaurar únicamente estado propio y aún compatible con el contexto; reingreso/reinicio puede ser necesario cuando un consumidor conserva objetos. No se propone modificar host, SDK, EXE, ROM ni saves como mecanismo de implementación .dusk.

R-16 — Persistencia interna del port no debe confundirse con SaveService: AchievementSystem fija loaded antes de IO, captura errores y tick limpia dirty después de save. No interpretar snapshot UI o toast como confirmación durable. PORT-004/005; sin fallo reproducido ni acceso a archivos del usuario.
