# Preguntas abiertas y siguiente comprobación mínima

Todas se refieren al SHA fijado. Se evita repetir lo ya respondido; cada pregunta tiene una acción limitada. El atlas sigue siendo estático y la existencia de una pregunta no autoriza implementar ni compilar un mod.

| ID / estado | Qué falta y por qué importa | Próximo paso mínimo |
| --- | --- | --- |
| Q-01 · PARCIAL | Item y Message contrastados en CALLBACK-005..013; otros dispatchers pendientes | Elegir otro dispatcher con hueco concreto; no repetir Save/Host/Camera/Item/Message ni inferir barrera universal. |
| Q-02 · PARCIAL | Item exige side-effect-free; Message copia sin revalidar handle/active y conserva texto separado de callback; sin garantía general de reentrancia | Contrastar encabezado y bucle concreto de un servicio; documentar límites de colección y vigencia. |
| Q-03 · NOT_VERIFIED | Perfil propio cuyo unregister falla durante teardown | Seguir actor_remove_mod/loader y rutas de creación pendientes; determinar exactamente qué estado queda, sin afirmar crash ni solución SDK. |
| Q-04 · NOT_VERIFIED | Símbolos exportados/resolubles y layouts en imagen Windows x64 concreta | Consultar evidencia histórica exacta o manifest/import library ya disponible sin recompilar; si no existe, mantener límite binario. |
| Q-05 · BLOCKED local | Aurora/Borealis internos, incluidos DX12, DVD/CARD y garantías externas de unregister | Consultar solo archivo necesario al SHA del gitlink si hay acceso; no instalar ni auditar todo el tercero antes de avanzar en fuente principal. |
| Q-06 · PARCIAL | Retry por save-written/copy/erase y vida de dirty/caché contrastados en WORLD-034..037; backend,crash consistency y migración completos pendientes | Revisar atomic_replace exacto de Borealis si disponible; si falta,conservar bloqueo local y no inventar ACK/garantía de reinicio. |
| Q-07 · NOT_VERIFIED | TGSC: bytes significativos, stride/padding y tamaño del caller Windows | Comparar consumidor/serialización y evidencia de tipos de la revisión exacta; no convertir STATIC_ASSERT histórico en medida. |
| Q-08 · NOT_VERIFIED | BST frame_end consulta dirty pero llama sync WSYS | Buscar call sites de sync BST y lifecycle antes de inferir qué edición quedaría diferida; no afirmar reproducción audible. |
| Q-09 · PARCIAL | File-select→PLAY contrastado en ARCH-002..007; quedan logo/direct-load, opening/reset y recuperación tras error/overlap, captura y separatePresentation completos | Seguir un fallo concreto de overlap/creación sin repetir ruta ordinaria; el caller no comprueba ChangeReq ni restaura menú. |
| Q-10 · READ parcial | Fuentes y cadena AutoMata morf/BCK/BTK contrastadas (PRES-036..039,044..047); quedan formatos/LOD/skin,otros morf,TextBoxEx y localización | Elegir una ruta transversal de adquisición→uso→liberación; conservar resto como muestreo. |
| Q-11 · READ parcial | Avance normal/KYTAG11 y salida save/audio contrastados (PRES-040..043); KYTAG06 tipo11→paletas/fog/partículas contrastado (PRES-048..051); agua,otras variantes/escritores y orden entre perfiles pendientes | Seguir un controlador y consumidores de sus datos; no diseñar un mod climático. |
| Q-12 · READ parcial | Swpush contacto/debounce/switch/cleanup contrastado (PLAYER-035..039); resto de NPC,bosses,puzzles,pesca/minijuegos conserva profundidad selectiva | Alternar familias y mecanismos comunes; la ficha other_systems localiza rutas, no estudia exhaustivamente cada actor. |
| Q-13 · READ parcial | Logros y cadena speedrun/LiveSplit contrastados en PORT-001..009; backend/ACK/timeouts/reset completos,presence,diagnostics y configuración pendientes | Alternar familia; backend Borealis puntual si disponible o presence/diagnostics. No conectar LiveSplit ni tratar contador UI/tick como tiempo real medido. |
| Q-14 · NOT_VERIFIED | Resolución de conflictos reales entre varios mods/overlays/hook candidates | Contrastar desempate y cleanup de un mecanismo; coexistencia runtime sigue sin demostrarse. |

Bloqueos que no impiden continuar: submódulos ausentes y falta de runtime Windows. Git/gh no fueron la vía operativa; el conector GitHub permite continuar documentación con HEAD comprobado y lease. No hay tarea programada ni promesa de trabajo desatendido.
