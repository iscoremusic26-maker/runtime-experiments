# Memoria, heaps y vigencia de objetos

Fuente fijada: `40457c6adb381928e4b5fef6ed459ed291edd5e2`. Inspección estática selectiva de JKernel, actor manager y adaptaciones PC; sin ejecución Windows/DX12. No existe aquí una certificación de allocator intercambiable entre juego y cualquier DLL.

El heap actual se mantiene por hilo en PC; cambiarlo devuelve el anterior. Esto describe selección de memoria, no permiso de concurrencia para tocar el mundo o actores. Un worker nace con su propio contexto TLS. El adaptador OSThread usa std::thread y side tables, así que no se presupone el modelo de scheduling de GameCube.

**ROOT-001 · SOURCE_OBSERVED** — [libs/JSystem/src/JKernel/JKRHeap.cpp L40-L53](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/libs/JSystem/src/JKernel/JKRHeap.cpp#L40-L53); [libs/JSystem/src/JKernel/JKRHeap.cpp L200-L204](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/libs/JSystem/src/JKernel/JKRHeap.cpp#L200-L204).

El port evita confundir el allocator general con JKR mediante JKRHeapToken y macros JKR_NEW/JKR_DELETE. Para una futura DLL debe conservarse la pareja allocator/liberador del contrato que entregó cada objeto; no sustituir una llamada ResourceService.free por delete o JKRHeap.free.

**ROOT-002 · SOURCE_OBSERVED** — [libs/JSystem/include/JSystem/JKernel/JKRHeap.h L236-L278](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/libs/JSystem/include/JSystem/JKernel/JKRHeap.h#L236-L278).

La familia JKR PC puede salir del heap y hacer fallback a memoria aligned del sistema. En Windows usa _aligned_malloc; la sobrecarga de delete con token comprueba findFromRoot y, si no encuentra heap, utiliza _aligned_free. Un puntero no encontrado en el árbol JKR no prueba que pertenezca a este fallback: podría venir de otro servicio o CRT.

**ROOT-003 · SOURCE_OBSERVED** — [libs/JSystem/src/JKernel/JKRHeap.cpp L521-L595](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/libs/JSystem/src/JKernel/JKRHeap.cpp#L521-L595); [libs/JSystem/src/JKernel/JKRHeap.cpp L627-L640](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/libs/JSystem/src/JKernel/JKRHeap.cpp#L627-L640).

El actor manager ejecuta heapCallbackFunc con un heap actual temporal y luego repone el anterior. Este wrapper hace la restauración al retorno normal, sin guard de excepción visible. DeleteHeap destruye el heap y pone actor->heap a NULL; los punteros a modelos, animaciones o buffers allí asignados deben considerarse vencidos aunque su valor numérico permanezca en otra tabla.

**ROOT-004 · SOURCE_OBSERVED** — [src/f_op/f_op_actor_mng.cpp L372-L385](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/f_op/f_op_actor_mng.cpp#L372-L385).

La construcción del solid heap puede volver a llamar al callback cuando intenta un heap ajustado: no asumir que es una notificación única para escribir efectos externos irreversibles. El wrapper elimina bits de flags del tamaño y duplica la estimación en TARGET_PC; eso es política de capacidad, no evidencia de que cada clase tenga exactamente doble tamaño.

**ROOT-005 · SOURCE_OBSERVED** — [src/f_op/f_op_actor_mng.cpp L625-L670](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/f_op/f_op_actor_mng.cpp#L625-L670); [src/f_op/f_op_actor_mng.cpp L717-L753](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/f_op/f_op_actor_mng.cpp#L717-L753).

La variante cómoda mDoExt_createSolidHeapToCurrent guarda el heap anterior en un único slot estático, con asserts de hilo principal y no anidamiento. La selección del heap JKR sea TLS no vuelve reentrante ese slot. La restauración lo pone a NULL. Mantener estas invariantes aunque un build desactive asserts.

**ROOT-006 · SOURCE_OBSERVED** — [src/m_Do/m_Do_ext.cpp L986-L1009](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/m_Do/m_Do_ext.cpp#L986-L1009); [src/m_Do/m_Do_ext.cpp L1118-L1127](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/m_Do/m_Do_ext.cpp#L1118-L1127).

## Integración y rollback

El mecanismo de memoria no se expone como un servicio genérico de asignación en el inventario de SDK. Para bytes de recursos, archivos, red o savedata se prefiere la pareja de operaciones del servicio correspondiente; para perfiles propios se sigue ActorService y su lifecycle. La llamada C++ a estos helpers queda **POTENTIAL_REQUIRES_VERIFICATION**: firma/source visible no garantiza export, resolución ni seguridad del target Windows. Consultar [SDK](../SDK_AND_SERVICES.md), [ABI](../HOOKING_AND_ABI.md), [actores](actors_ai_npcs.md) y [recursos](resources_archives_overlays.md).

Rollback: cancelar trabajo propio, retirar callbacks antes de descargar código, liberar cada recurso con su propietario y limpiar caches de IDs/punteros al borrar actor o cambiar escena. Destruir un heap no deshace cambios de flags/save ni restaura recursos ajenos. Estas son obligaciones de diseño deducidas del ownership observado, no pruebas runtime.

## Cobertura pendiente

Se siguieron selección/restauración, fallback PC y construcción/destrucción de heap de actor. Quedan PENDING el árbol completo de disposers, reciclaje de todas las clases JKR, fallos de workers, comportamiento en shutdown y cross-CRT Windows. No se propone modificar SDK, allocator del host ni ejecutable.

Cobertura: READ/CROSSCHECKED selectiva según SYSTEM_INDEX y los niveles de cada evidencia; ninguna ruta constituye prueba runtime Windows/DX12.
