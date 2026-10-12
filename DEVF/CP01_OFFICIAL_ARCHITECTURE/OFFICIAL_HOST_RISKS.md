# Seguridad del host original y límites de la ruta nativa

Se reutiliza `DEVF/CP01/LIFECYCLE_AUDIT.md`; no se repite la auditoría de actores/cBg ni los tests anteriores. Esta revisión determina qué contratos afectan a la arquitectura nueva. Todo código citado procede del árbol **original limpio** 40457c6, no de la integración parcheada.

| Situación | Conclusión delimitada |
|---|---|
| Native Stage placement, bytes temporales del mod | **PASS estático:** Stage los copia; dStage copia al append del host. No retiene vector ni callback de DEVF en el actor/request. |
| Native Actor request con callback NULL | **PASS estático condicionado:** copia datos y usa métodos del perfil original. No requiere DLL de DEVF para ciclo de vida del enemigo; por nombre se debe excluir override de otro mod. |
| Request pendiente al desactivar | **PARTIAL:** puede sobrevivir porque no se cancela por dueño nativo. No es por sí solo un callback a DEVF; sí impide prometer ausencia de apariciones posteriores o limpieza inmediata. Transición/resource failure **NOT_VERIFIED runtime**. |
| Actor visible en primera fase | **PASS estático** sobre el orden observado: entra en g_fopAcTg_Queue antes de completar Create. **BLOCKED** cualquier escritura avanzada que lo considere listo solo por encontrar el ID. |
| Stage edit retirado/detach | **PASS estático** para borrar futuros registros; destrucción de instancias existentes **no está implementada por ese contrato**. No se conserva LoadedMod* en los bytes del actor por esta ruta. |
| Hot reload/reenable | **NOT_VERIFIED:** viejo actor puede seguir vivo y nueva definición volver a ejecutarse. Stage handles no permiten reconciliar IDs. No afirmar exactly-once ni eliminar el primer match por perfil. |
| Transiciones de room/stage/layer | **NOT_VERIFIED** para un caso real. Invalidar tracking del contexto y no reutilizar IDs/pointers de sesión anterior; verificar tanto pendientes como terminados. No intentar controlar lifecycle con parche al host. |
| Delete nativo individual | **PARTIAL:** request de eliminación visible; no confirmación sin observación posterior. MOD_OK si no encontrado no prueba cancelación pre-create. Dos solicitudes o desaparición temprana no autorizan doble liberación: el mod nunca hace free/delete al actor nativo. |
| Recursos nativos | **PARTIAL:** resLoad/resDelete, heap, animación y colisión son del perfil original. La copia de datos evita buffers DEVF dependientes. Disponibilidad y fallos parciales en una instalación **NOT_VERIFIED**; reutilizar APIs no acredita aptitud de una escena. |
| Recursos y trabajo propios de futuras variantes | **BLOCKED** si un actor retiene callbacks/pointers/objetos cuyo destructor dependa de la DLL tras detach. No asignar callbacks de colisión/J3D, vtables, punteros al estado de DEVF ni liberar memoria del heap del actor. Datos/objetos propios han de retirarse mediante sus servicios oficiales. |

## Desactivación original, no política de veto

`ModLoader::deactivate_mod`: modules_mod_deactivating → mod_shutdown → remove exported services → modules_mod_detached → unload_native → active=false. Un shutdown fallido se registra y el flujo continúa. `unload_native` difiere el cierre de la librería al drain de retired natives para proteger código en la pila del tick; **no es un pin hasta que terminen actores o recursos asíncronos**. Ningún resultado del prototipo acredita lo contrario.

ActorService.modDeactivating recopila únicamente **perfiles registrados por ese mod**. No destruye automáticamente instancias de perfiles nativos creadas por él. StageService.modDetached borra todos sus edits. ResourceService libera buffers propios al detach; los enemigos originales cargan sus archivos con la infraestructura nativa, no con esos buffers. Por eso la ruta A pura puede evitar la dependencia de callbacks que bloquea el perfil personalizado anterior, aunque persistan requests/actores nativos.

Los otros servicios requieren contratos independientes: Ui invalida slots y comprueba slot_live antes de callbacks capturados; File anula owner/callback del picker al detach; Gfx retira tipos y llama aurora::gfx::synchronize durante deactivación cuando existen registros. Son barreras estáticas pertinentes para editor/render futuros, **no una prueba general de seguridad de cualquier callback introducido por DEVF**. El prototipo no registra ninguna de estas operaciones.

## Separación de la investigación experimental

La compilación del host parcheado y las 17 expectativas del diagnóstico dirigido se conservan en `CP01_HOST_INTEGRATION`. La evidencia se obtuvo sobre el parche exacto, headers/TUs reales y adaptadores explícitos; no ejecutó el juego ni una liberación real de memoria en el caso reentrante. No se aplica el parche, no se corrige aquí y no se distribuye un EXE.

`actor_drain_mod` y sus snapshots sin revalidar son una adición experimental; ese defecto no se atribuye al original. El diagnóstico de recorrido cached-next no se presenta como un fallo runtime del ejecutable oficial. El original contiene un recorrido análogo en su ruta de desregistro personalizado; la semejanza estática no sustituye un experimento del host original con su flujo completo. La arquitectura A **no registra perfiles**, por lo que no necesita usar ese destructor de perfiles DEVF.

El bloqueo original independiente sigue siendo: los contratos públicos no garantizan retención de la DLL/cancelación completa cuando perfiles o callbacks DEVF siguen pendientes. Ni una eventual corrección del experimento ni dejar desarmado un prototipo demostraría descarga dinámica del perfil CP01 original. Este bloqueo permanece **BLOCKED** para la ruta personalizada, y no se usa para descartar indiscriminadamente los perfiles nativos.

## Política recomendada para una ruta A futura

Solo perfiles originales, callback de solicitud NULL, configuración copiada, ninguna referencia de la DLL en actor/request. Desactivar retira definiciones futuras; las instancias nativas existentes continúan bajo ownership del motor. No ofrecer borrado inmediato hasta probar binding y cancelación. No hot reload durante el experimento inicial; terminar el proceso antes de reenable para evitar duplicados. El mod no puede forzar al host a respetar esta precaución mediante un return de shutdown; es una condición operativa explícita, no una barrera implementada.

Actualmente no hay actores, edits, trabajo asíncrono ni recursos registrados por el prototipo. Su cierre de compilación es **DISARMED_NO_REGISTRATION** y no existe un archivo de configuración que pueda abrirlo.
