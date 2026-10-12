# Recomendación: A1 primero, A2 con propietario explícito después

**Mantener A1 como primera ruta a validar para colocaciones persistentes de enemigos originales. Mantener A2 como base futura de variantes con identidad individual, con un gate nuevo de propiedad de escena. No adoptar el spawner completo ni los hooks de Dawnlight. CP02 NO-GO; DISARMED_NO_REGISTRATION.**

Autoridad: arquitectura `.dusk` sobre Dusklight oficial e intacto 2.0.3 Windows x64 DX12. Base `545b2d1418bfcae11dd4585c1a9bdcbc526b6a2d`. Referencias exactas D/S y commits en [COMPARATIVE_AUDIT](COMPARATIVE_AUDIT.md). Esta decisión documental amplía los requisitos del checkpoint anterior; no cambia su código ni borra sus resultados.

## Qué cambia con esta referencia

| Decisión | Justificación / evidencia / estado |
|---|---|
| Preferir el reloader nativo para A1 | S10 ROOM_SCENE→S8 context de nodo→S9 Stage helper→S3/S5 request owner. **PASS_STATIC**: capa de sala en el flujo normal para perfiles CURRENT. No depende de entrar desde UI ni de un setter de capa dentro de DEVF. |
| Rechazar A2 desde un caller arbitrario sin owner verificado | S1/S2/S3 capturan current layer, no room ownership. D1/D2 documentan el fallo de raíz. **PASS_STATIC** de la diferencia; frecuencia de fallo Windows de DEVF NOT_VERIFIED. |
| Separar owner play de owner room | S10 cleanup recorre capa de sala; S11 teardown de escena recorre sus descendientes. Seleccionar capa de Link/PLAY puede evitar root y todavía conservar actores durante cambios de room. **PARTIAL**: debe elegirse el dueño que satisfaga el lifetime buscado y observar migraciones propias del enemigo. |
| Conservar vía A2 sin hooks | S7 y S13 respaldan selección/restauración de capa mediante ABI; imports/exports comprobados. **PASS_STATIC** de disponibilidad, **NOT_VERIFIED** de uso seguro concreto. No declarar A2 imposible ni listo. |
| No confundir presets con bypass de admisión | D1/D6 usan hooks, mientras S17 aplica FILI aparte del parámetro propio. **INCOMPATIBLE** adoptar ese bypass; respetar contexto nativo es la alternativa compatible. |
| Mantener tipos antes de allocation y tracking temprano | D4:246–274/S6:138–163, D1:334–336. **PASS_STATIC** como invariantes para solicitudes propias; no interceptar/reemplazar actores vanilla o sus descendientes. |

## Primera aparición futura A1, alcance acotado

Una configuración propia proporciona nombre canónico, parámetros específicos, transform y stage/room/layer lógico verificados. Se registra solo Add antes de la carga natural de la room. **No invocar el reloader manualmente**, no patch/delete de enemigos originales y no activar simultáneamente A2 para la misma entrada. El perfil debe ser nativo, CURRENT, con admission y recursos compatibles y sin modo de migración/evento no estudiado. No se elige automáticamente E_SB/E_RD/Darknut ni se habilita aquí un paquete.

La prueba futura debe observar owner, fase completa, conteo de nuevas instancias, render y cleanup bajo la transición real. A1 no devuelve ActorId: cualquier asociación de los actores observados con la entrada de prueba exige un caso controlado y evidencias de baseline/censo, parámetros y contexto, sin ambigüedad con actores vanilla. No usar primer match por perfil como ownership ni comenzar a escribir stats de esos matches. Si no se puede distinguir, detener ese ensayo y revisar el método de observación.

Persistencia significa reconstituir una **definición** en sesiones/cargas compatibles mediante datos propios. No significa actor eterno, continuidad de ID, recuperación de HP tras save, exactamente una instancia por recarga o eliminación instantánea al desactivar. Retirar el edit solo impide creaciones futuras; cierre de proceso antes de reenable/hot reload sigue siendo la política conservadora inicial. S14 y los informes anteriores justifican estos límites.

## Evolución A2 hacia variantes individuales

Una entrada que requiera ActorId propio usará una solicitud A2 exclusiva para esa colocación, después de validar su owner y contexto. Elegir capa de sala viva para lifetime de room o una capa de escena demostrada para otro lifetime; no derivarlo de room_num ni asumir siempre que la capa de Link sea la deseada. Con el ABI oficial puede investigarse un scope de selección/restauración sin hooks; requerirá pruebas de nesting/error y de transiciones. La alternativa fpcSCtRq_Request(layer,...) también está públicamente declarada/exportada, pero exige responsabilidades de append/error adicionales: no se implementa ni se aprueba todavía.

Registrar ActorId al retorno y diferenciar solicitado, visible-en-create, listo, fallido/cancelado y retirado. La cancelación ABI por la base pública se conserva como posibilidad **B / NOT_VERIFIED**, no como solución demostrada. No acceder a standard_create_request_class privada ni enganchar phase_Load/fpcBs_Create. Al cambio de contexto, descartar punteros prestados y validar cualquier ID nuevamente. Los descendientes creados por métodos nativos normalmente capturan su capa, pero parent ID no fija dueño ni cubre requests desde otra API/otro contexto; revisar por enemigo antes de prometer cleanup de su familia.

Se mantienen todos los objetivos de DEVF: vida/daño/defensa/tamaño/velocidad/IA/ataques por instancia, apariencia independiente, efectos/recompensas, colocaciones persistentes, editor y Cave/Dungeon Framework futuros. La matriz anterior sigue distinguiendo parámetros/ABI por tipo de funciones universales. Este audit no demuestra stats/IA arbitrarios ni reduce el producto a vanilla placements.

## Lecciones Cave compatibles y alternativas fundamentadas

| Técnica | Aplicación posible / límite |
|---|---|
| Validar suelo finito y room | D4:204–217/D5:15–34, S20 y exports. Herramientas **PASS_STATIC**; una política preflight de solicitudes propias es **B / NOT_VERIFIED**. No reutilizar lowest-floor/+120 de Cave como coordenada segura universal. |
| Definir tipo/params antes de solicitar | D4:246–274/S6. Aplicable a registros propios A1 o solicitudes propias A2 (**A**), manteniendo room/layer/parent adecuados. No sustituir un actor ya reservado ni un hijo de coordinador que espera su tipo. |
| Espera acotada sin alterar recursos originales | D4:220–244 contiene un hook incompatible. Para un controlador propio A2 se puede investigar una espera **antes de crear**, con timeout y ningún actor solicitado si falla. No prometer pausar el reloader del host mediante servicios que no ofrecen ese contrato. |
| Plan de salas/framework propio | Configuración propia y APIs de creación son oportunidades compatibles (**B**) si el futuro framework declara escenario/owner/recursos/slots y lifetime. No existe aún un contrato de Cave/Dungeon Framework que permita PASS de integración. |
| Reemplazar enemigos vanilla preservando IDs/slots | Cave intercepta requests y cambia profile antes de allocation. **C / INCOMPATIBLE** de ese mecanismo para DEVF. StageService tiene edits públicos, pero no se implementa sustitución ni se presume que replique identidad, timing o cleared-room semantics. |
| Enemigos fuera de su horario/medio/owner | Hooks y cambios scoped de daytime o Execute quedan **INCOMPATIBLE**. Respetar condiciones nativas o escoger un perfil/preset/contexto demostrado; no ofrecer la variante imposible como si estuviera implementada. |

## Riesgos y cierre

El bloqueo de DLL/perfiles propios del checkpoint anterior permanece **BLOCKED** e independiente. No se reaudita el parche ni se transfiere su defecto de reentrancia al host original. Elegir perfiles nativos y callback NULL evita esa dependencia en el ciclo de vida del enemigo, pero no borra los riesgos de requests, escena, reenable o recursos propios de futuras variantes.

La auditoría justifica avanzar después a **observación y validación dirigida**, no a una aparición aprobada ni CP02. El siguiente paso mínimo está secuenciado en [NEXT_VALIDATION_GATES](NEXT_VALIDATION_GATES.md): comprobar en la instalación contexto/admisión/recursos y owner; después, con autorización separada, un único ensayo A1. A2 necesita sus gates adicionales antes de usarse para variantes.
