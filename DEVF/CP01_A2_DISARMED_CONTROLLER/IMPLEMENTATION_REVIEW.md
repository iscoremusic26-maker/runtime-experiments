# Controlador A2 desarmado: implementación y reutilización

Base exacta `2911af67bde2dc1e6376ed7c989cdc862b79126d`; estrategia aprobada RECOMMEND_A2. Host de referencia oficial `40457c6adb381928e4b5fef6ed459ed291edd5e2`, SDK/ABI2.0.3. Ningún código de Dawnlight se copia. Este checkpoint implementa controlador y simulación; no implementa un adaptador de solicitudes nativas.

## Componentes reales

| Archivo | Función implementada |
|---|---|
| `src/controller_core.hpp/.cpp` | Estados explícitos, validación combinada, contexto escalar, latch consumido antes de solicitud simulada, ID propio, monitor pending/readiness/error/timeout y terminales sin reset. |
| `src/room_owner_resolver.hpp/.cpp` | Adaptación del lector G2: vínculo público ROOM_SCENE→child→PLAY_SCENE vigente, ID/profil/init, estado de sala, contadores y revalidación de datos. Solo devuelve valores propios. |
| `src/disarmed_mod.cpp` | Lifecycle oficial Host2.2/Log1.0/Game2, host2.0.3, guardia de reentrada update, diagnóstico de solo lectura acotado16 líneas/120updates y `Controller.disarm`. No ruta de solicitud. |
| `tests/simulation.hpp` | Scope genérico sobre FakeEngine, selección/restauración y revalidación, intento único, aceptación incierta. Compilación exclusivamente LAB_ONLY; no se incluye en DLL del módulo. |
| `tests/fake_engine.hpp`, `controller_lab.cpp` | Layers/nodo/IDs/request y errores sintéticos. No es ejecución del motor. |
| `tests/adapter_lab.cpp` | Ejecuta el lifecycle real nuevo contra servicios y resolver falsos; desarme y reentrada, rechazos, límite de lecturas y reactivación. |
| `tests/abi_link_probe.cpp` | DLL offline con direcciones de funciones oficiales para verificar imports de scope y tipo de ActorSpawnParams; no invoca funciones ni se instala. |
| `ci/` | Pipeline MSVC, seis mutantes temporales, compile guards, auditoría PE/código/grafo e informes textuales. |

## Reutilización concreta de G2, sin modificar sus archivos

CMake compila directamente los históricos `CP01_G2_READONLY_PACKAGE/src/core.cpp` y `native_reader.cpp`; el resolver incluye su `core.hpp`. Reutiliza `capture_native`, `Registry`, validación de stage/room/logical, presencia de Link en cola antes de dereferenciarlo, perfil/init/INIT/IsCreating, búsqueda pública de ROOM_SCENE, IDs y capas registradas. No reescribe lectores/censo ni repite sus pruebas históricas. La auditoría coteja su ledger revisado de hashes LF.

La carencia específica G2 era el vínculo con la **escena vigente**, no la enumeración. La adaptación vuelve a resolver el node y `getProcID` de PLAY_SCENE en el mismo tick, coteja perfiles/init, `layer.process_node`, parent layer y child registrado. ROOM_SCENE es propietario del hijo; Link owner no determina ese hijo. La enumeración adicional usa el mismo `Registry` para validar los vínculos nuevos; no introduce otro registro de capas.

Se añaden getters públicos `getNextStayNo`, `getProcID`, `roomControl_checkStatusFlag` y `IsDeletingMesg`. Máscara de rechazo0x2e: bit2 prepara node,4 solicita retirada,8 limpia contenidos,20 borra selectivamente; fuente focalizada `d_s_room.cpp:198–280`. `d_s_play.cpp:1162` asigna getProcID; `d_stage.cpp:251–267` alinea next con stay al entrar. No se escriben estos datos. init2 y ausencia de IsCreating, contadores de hijo/padre y nextStage son señales combinadas; no pin ni reserva vitalicia.

## Máquina de estados y seguimiento

DISARMED/VALIDATION_REJECTED no envían solicitudes. ATTEMPT_CONSUMED se fija antes de FakeEngine.request; no hay reset o segundo backend. REQUESTED→PENDING exige distinguir cola/proceso incompleto. READY_OBSERVED requiere ID/perfil/room/owner, actor visible, init/INIT y recursos conjuntamente. Phase failure, desaparición ambigua, owner/ID ajeno, reuse informado, destrucción, contexto cambiado o timeout llevan a FAILED/STOP_SESSION; no retry/delete/cancel. READY seguido de desaparición o regresión termina la sesión.

El monitor no rechaza automáticamente create_count1 causado por su propio pending. En laboratorio la identidad y pending se aportan como valores abstractos; no hay lector nativo de readiness/request implementado en este checkpoint. La señal `reused` es un hecho suministrado por el fake, **no un detector de generación del ABI**. Un ID nativo con igual perfil/room/owner reutilizado no sería distinguible solo con esos datos: futura tarea deberá declarar contexto/continuidad y parar ante ambigüedad; no afirmar que ese contrato runtime ya está resuelto.

Preset constante conservado E_OC0x1FE, parametersFFFFFFFF, argument−1, XFF14, yaw/z0, escala1, setIDFFFF/callbackNULL en el contrato futuro. No contiene XYZ: `NO_ASIGNADO`. Coordenadas de WRock no se incorporan. Los fixtures modelan IDs/capas sintéticos; no se asigna posición real. La ausencia de posición aprobada produce rechazo en simulación.

## Contrato de hilo y errores

El resolver se invoca exclusivamente desde el update original del loader, en el tick del juego; no crea threads/tareas. `update_context` representa ese sitio de llamada, **no un detector OS del hilo ni autorización para llamar desde otro caller**. La guardia updating bloquea reentrada del lifecycle y el driver fake tiene guardia busy. Esta premisa de caller/version/listas sanas continúa runtime NOT_VERIFIED para la adaptación.

Scope solo en fakes; IDs se seleccionan/revalidan y previous se coteja antes de entrar. Restauración normal/error/C++throw y nesting LIFO probados bajo ese contrato. Previous conocido muerto se rechaza sin restaurarlo, lo que termina sesión; RAII no recupera SEH/concurrencia/memoria corrupta. Revalidación/error incierto consume o mantiene parada; desarmar no borra un terminal previo al intento.

No hay interfaz nativa request, arming/config/UI/env switch, hot reload o paquete generado. `begin_simulation` es lógica escalar de core, no export de la DLL ni llamada del lifecycle; aun invocada no contiene creación. Implementar otro adaptador nativo y admitir ubicación requerirán tareas/autorizaciones posteriores, no cambiar una bandera.
