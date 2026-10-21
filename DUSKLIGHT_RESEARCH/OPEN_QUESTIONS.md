# Preguntas abiertas y siguiente comprobación mínima

Todas se refieren al SHA fijado. Se evita repetir lo ya respondido; cada pregunta tiene una acción limitada. El atlas sigue siendo estático y la existencia de una pregunta no autoriza implementar ni compilar un mod.

| ID / estado | Qué falta y por qué importa | Próximo paso mínimo |
| --- | --- | --- |
| Q-01 · PARCIAL | Item resolvers contrastados en CALLBACK-005..008; Message y otros dispatchers siguen pendientes | Leer una implementación y un consumidor, comparar snapshot/lookup/ownership con CALLBACK-001..004; no generalizar desde nombres. |
| Q-02 · PARCIAL | Item copia defensivamente pero su contrato exige resolver sin efectos secundarios; no hay garantía general de reentrancia | Contrastar encabezado y bucle concreto de un servicio; documentar límites de colección y vigencia. |
| Q-03 · NOT_VERIFIED | Perfil propio cuyo unregister falla durante teardown | Seguir actor_remove_mod/loader y rutas de creación pendientes; determinar exactamente qué estado queda, sin afirmar crash ni solución SDK. |
| Q-04 · NOT_VERIFIED | Símbolos exportados/resolubles y layouts en imagen Windows x64 concreta | Consultar evidencia histórica exacta o manifest/import library ya disponible sin recompilar; si no existe, mantener límite binario. |
| Q-05 · BLOCKED local | Aurora/Borealis internos, incluidos DX12, DVD/CARD y garantías externas de unregister | Consultar solo archivo necesario al SHA del gitlink si hay acceso; no instalar ni auditar todo el tercero antes de avanzar en fuente principal. |
| Q-06 · NOT_VERIFIED | Qué ocurre ante fallo de sidecar tras éxito de CARD, incluidos intentos posteriores | Seguir dirtyMods/error paths y auxiliares de almacenamiento; no deducir durabilidad a partir del callback/toast. |
| Q-07 · NOT_VERIFIED | TGSC: bytes significativos, stride/padding y tamaño del caller Windows | Comparar consumidor/serialización y evidencia de tipos de la revisión exacta; no convertir STATIC_ASSERT histórico en medida. |
| Q-08 · NOT_VERIFIED | BST frame_end consulta dirty pero llama sync WSYS | Buscar call sites de sync BST y lifecycle antes de inferir qué edición quedaría diferida; no afirmar reproducción audible. |
| Q-09 · READ | Bootstrap main/title/slots y gates completos de pausa, captura, errors y separatePresentation | Seguir una transición concreta y sus callbacks; ARCH-001 solo cubre el camino normal del scheduler. |
| Q-10 · READ parcial | Cadena font JUTResFont/file-info contrastada (PRES-036..039); quedan modelos/skins/LOD, TextBoxEx, cache-font y charset/localización | Elegir una ruta transversal de adquisición→uso→liberación; conservar resto como muestreo. |
| Q-11 · READ | Calendarios, agua, iluminación por layer y weather tags | Seguir un controlador y consumidores de sus datos; no diseñar un mod climático. |
| Q-12 · READ | Todos los NPC, bosses, puzzles, pesca y minijuegos | Alternar familias y mecanismos comunes; la ficha other_systems localiza rutas, no estudia exhaustivamente cada actor. |
| Q-13 · READ parcial | Logros internos contrastados en PORT-001..005; speedrun/LiveSplit, presence, diagnostics y configuración pendientes | Localizar propietario del estado y consumidor relevante de una familia; no abrir datos del usuario ni tratar comentario AchievementService como API presente. |
| Q-14 · NOT_VERIFIED | Resolución de conflictos reales entre varios mods/overlays/hook candidates | Contrastar desempate y cleanup de un mecanismo; coexistencia runtime sigue sin demostrarse. |

Bloqueos que no impiden continuar: submódulos ausentes y falta de runtime Windows. Git/gh no fueron la vía operativa; el conector GitHub permite continuar documentación con HEAD comprobado y lease. No hay tarea programada ni promesa de trabajo desatendido.
