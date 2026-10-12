# Decisión de arquitectura DEVF

**Ruta recomendada: `.dusk` sobre Dusklight oficial 2.0.3, backend nativo sin callbacks de actor pertenecientes a DEVF y adaptadores por enemigo sujetos a gates independientes. CP02 permanece NO-GO.**

El checkpoint de host parcheado se conserva como investigación. No es una dependencia del producto, no se aplica ni se continúa corrigiendo. El baseline original ya compilado tampoco se recompila en esta tarea. La implementación previa `DEVF/CP01` conserva `DISARMED_NO_REGISTRATION` sin cambios.

La capacidad de definir colocaciones nativas está acreditada estáticamente; 26 comprobaciones nuevas de codificación/desarmado y una comprobación de tipos del ABI pasaron con MSVC/Windows SDK. Aparición, render, suelo, colisión, eliminación y DX12 real permanecen **NOT_VERIFIED**. La evaluación no acredita que todas las variantes avanzadas sean realizables ni las descarta por ausencia de setters universales.

## Componentes propuestos, sin implementar CP02

| Componente | Responsabilidad y gate |
|---|---|
| Modelo de configuración propio | IDs estables de colocación/variante; stage/room/layer explícitos, transform, tipo nativo, parámetros específicos y capacidades solicitadas. Guardar exclusivamente en data_dir del mod; recursos propios en res. No persistir ActorIds/pointers entre sesiones. |
| Backend A1 pasivo | Serializar ACTR/TGSC y registrar solo Add por StageService. Reaplicar configuración en cada activación. Retirar ediciones futuras al detener; documentar supervivencia de instancias. Apropiado para colocaciones vanilla, sin presentar el handle como ID de actor. |
| Backend A2 gestionado | Propuesta para variantes que necesitan identidad: solicitud nativa por perfil verificado, callback NULL, ActorId por colocación, máquina de estados de readiness/contexto. No usar A1 simultáneamente para esa entrada. Persistencia se obtiene de la configuración y del controlador, no de un ID guardado. Requiere experimentos pendientes de transición/cancelación. |
| Adaptadores por tipo | Declarar capabilities y limitaciones por enemigo. Empezar por un único campo con consumidor claro después de confirmar readiness. Solo datos públicos de instancias validadas y funciones oficiales; no offsets privados, globals HIO/KREG, execute/vtable replacement o código parcheado. Si un campo se sobrescribe, estudiar su semántica antes de mantenerlo a fuerza cada tick. |
| Apariencia/efectos | Recursos/objetos propiedad del mod y servicios oficiales Texture/Gfx/ABI. Acreditar aislamiento por instancia y cleanup. No insertar callbacks ni pointers DLL en objetos nativos. Gfx propio es una posibilidad legal para representación adicional; no equivale automáticamente a skin que sustituya todo el modelo vanilla. |
| UI/editor futuro | UI oficial con handles y retirada de callbacks, configuración propia, undo y validación antes de publicar cambios. La edición de una definición no puede prometer cambiar/eliminar su instancia si no hay binding demostrado. |
| Puente Cave/Dungeon futuro | Servicio/versionado explícito de contexto, ownership, IDs y transiciones, una vez que existan esos contratos. Invalidar caches al detach del proveedor. Compatibilidad aún NOT_VERIFIED. |

La política A1 puede evitar el bloqueo específico de callbacks de perfiles DEVF: solo conserva datos copiados y usa perfiles nativos. La política A2 requiere mayor control de requests/contexto aunque sus métodos de actor sigan siendo originales. No es necesario trasladar la DLL de DEVF al ciclo de vida del enemigo para solicitarlo; tampoco se obtiene automáticamente una garantía de borrado al descargar el mod.

## Objetivo completo y condiciones GO/NO-GO

Se mantienen variantes por instancia, atributos configurables, apariencias independientes, IA configurable, colocaciones persistentes, editor y compatibilidad futura. La matriz explica qué subfunciones están disponibles, cuáles requieren pruebas y qué métodos quedan excluidos. Las alternativas son propuestas, no implementaciones ni recortes aceptados del objetivo.

| Gate | Estado actual | Requisito concreto |
|---|---|---|
| Host oficial intacto/SDK exacto | **PASS** estático y compilación incremental propia. | Conservar root 40457c6, servicio ABI correcto y límites de arquitectura. |
| Definición nativa y cierre del prototipo | **PASS** estático/laboratorio. | Registros 32/35 bytes; callback NULL; ningún registro/actor activado. |
| Enemy/placement real | **BLOCKED** para autorizar aparición. | Validar ubicación y recursos **del enemigo elegido** bajo flags/capa/escena de una instalación. Los resultados anteriores de WRock/F_SP121 se conservan y no se extrapolan a E_SB. |
| Requests, readiness y transiciones A1/A2 | **NOT_VERIFIED**. | Experimento oficial controlado, sin ambigüedad de IDs ni duplicados, con evidencia de carga/fallo/cambio de sala. |
| Variantes independientes | **PARTIAL / NOT_VERIFIED** por feature. | Adaptador específico, aislamiento frente a una instancia vanilla simultánea, sin escritura compartida ni callbacks DLL retenidos. |
| Perfil personalizado anterior y descarga DLL | **BLOCKED**, independiente. | Contrato oficial suficiente para garantizar finalización/cancelación y retirada de callbacks antes de unload. No se resuelve con esta ruta ni se ignora shutdown fallido. |
| Runtime Windows x64 DX12 | **NOT_VERIFIED**; ejecución **NOT_TESTED**. | Logs/evidencia real del juego; este laboratorio no acredita render, colisión ni limpieza runtime. |
| CP02 | **NO-GO**. | Cumplir gates aplicables y autorización de la etapa posterior. Esta evaluación no la inicia. |

## Experimento mínimo futuro, requiere nueva autorización

Antes de una aparición: una fase de observación sin registros, en la instalación oficial, que identifique versión/build_id, stage/room/layer efectivos, flags relevantes de aparición y archivo nativo disponible. Elegir una ubicación fundamentada **para ese enemigo**, reutilizando evidencia previa solo donde sea pertinente. `E_SB` es aquí una demostración del formato, no una selección aprobada para Hyrule Field.

Con esa evidencia y una autorización específica, preparar un paquete separado de prueba de una sola colocación original y parámetros revisados, sin nuevo perfil ni callback post-create. Primera prueba A1: iniciar proceso limpio, registrar una definición antes de la recarga prevista, entrar una vez a la sala/capa verificadas y observar cantidad, fase de creación, recursos y transform. Retirar la edición debe demostrar ausencia en una **carga posterior**, sin exigir desaparición inmediata del enemigo actual. Para revertir, cerrar el juego sin guardar cambios de progreso y retirar únicamente el paquete de prueba antes de abrir de nuevo. No activar hot reload/reenable durante esta primera prueba. Este procedimiento es un plan; no se ha producido el paquete activo ni ejecutado ninguno de sus pasos.

Antes de atributos avanzados, un experimento A2 adicional deberá demostrar ID propio, que `fpcM_IsCreating` deja de indicar request en curso y que el actor concreto completó recursos/componentes, desaparición/cambio de contexto y qué ocurre al desactivar durante creación pendiente. Solo después se estudia **un** campo por instancia, con otra instancia vanilla como control. No identificar Stage instances por el primer match del perfil; no usar desaparición como evento universal de muerte para recompensas.

El siguiente paso mínimo es obtener esa evidencia de contexto/recursos de un enemigo y acordar el experimento futuro; no corregir el parche ni iniciar CP02.
