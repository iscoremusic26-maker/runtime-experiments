# Decisión para un primer E_OC nativo

**Recomendación estratégica: RECOMMEND_A2**, sin hooks, mediante ActorService y scope de **capa hija de ROOM_SCENE**, no raíz ni owner de Link por defecto. Es autorización propuesta de diseño, no GO de aparición ni PASS de seguridad runtime. No se modifican la recomendación histórica A1 para colocaciones persistentes ni sus resultados.

Estamos **parcialmente sobrecomplicando** el primer ensayo: exigir navegación universal, censo social exhaustivo de todo el juego o destrucción/recreación natural previa de room3 para cualquier ruta aumenta el camino crítico sin demostrar mejor ownership. Siguen siendo esenciales el owner válido, enlace correcto, admisión nativa, un punto local justificable y un cierre de sesión conservador. La existencia de Dawnlight no satisface esos controles automáticamente.

## Comparación limitada a una instancia, una sesión y ninguna variante

| Aspecto | A1: Add + carga natural | A2: solicitud individual con owner validado |
|---|---|---|
| 1. Implementación | Encoder/Add sencillo; coordinación de consumo e identificación más costosa. | Scope y guardas adicionales; controlador one-shot e ID explícito. |
| 2. Dependencias runtime | ROOM_SCENE debe consumir edit compatible. | Sala ya viva, caller game-thread y contexto validado en el tick. |
| 3. Recarga | Imprescindible tras registrar; RTBL2/4 retiene3. | No exige retirada/recreación de sala. |
| 4. Propiedad | PASS_STATIC del call path natural, CURRENT. | PASS_STATIC de captura; política de selección propia aún NOT_VERIFIED. |
| 5. Aislamiento | Edición del conjunto de creación de sala, sin tocar originales. | Una cola de request nativa; setter temporal de contexto global, sin patch. |
| 6. FILI/progreso | No elimina restricciones. | Tampoco; no copiar bypass Dawnlight. FILI bitSwFF existente cubre el filtro concreto en ambas. |
| 7. Identidad | Handle de edit no es ActorId; necesita atribución sin ambigüedad. | ID devuelto se asocia a intento propio; validar ID/perfil/room/owner y lifetime. |
| 8. Asincronía | Create asíncrono y no ID directo. | Requested/pending/ready/failure distintos; false IsCreating no basta. |
| 9. Recursos | Reloader prepara bancos; Create carga recursos propios. | Respetar carga ya disponible/phase nativa; registro no prueba carga. No callbacks propios. |
| 10. Errores | Retirar edit no revierte instancia. | Error no justifica retry; pending tardío no tiene rollback universal. |
| 11. Duplicación | Edit puede consumirse otra vez hasta retirarlo. | Latch consumido antes del único intento, sin rearm/auto-retry. |
| 12. Transiciones | Hay que coordinar carga y retiro; salida visual no implica teardown. | Rechazar transición antes de solicitar; después cambio de contexto termina ensayo, sin nuevos requests. |
| 13. Limpieza/persistencia | Edición persistente e instancia con lifetime diferente. | Sin definición Stage persistente; actor/pendiente nativos permanecen hasta cleanup/cierre, no unload del mod. |
| 14. SDK | StageService y flujo nativo acreditados. | ActorService + funciones exportadas de capa acreditadas; combinación específica debe enlazarse después. |
| 15. Detener | Retirar edit impide futuros consumos, no mata actor. | Desarmar impide nuevas solicitudes, no cancela la existente; cierre completo es fallback. |
| 16. Observaciones nuevas | Llegada/retirada/reentrada node, consumo, identidad y render. | Owner resuelto antes/después, readiness y render; no ciclo natural previo requerido. |
| 17. Windows/DX12 | Nueva creación/render/cleanup NOT_VERIFIED. | Igual; evita ruta root si cumple contrato, no acredita renderer real. |
| 18. Reutilización futura | Colocaciones persistentes declarativas. | Identidad individual y lifecycle observacional útiles para variantes; atributos futuros sin aprobar. |

## Contrato que permite preferir A2

Desde **mod_update en game thread**, una intención manual futura se procesa únicamente en ese contexto. UI solo transmite intención; no llama al servicio. `fapGm_Execute:824–832` hace tick antes de `fpcM_Management`: la solicitud normal encola, no ejecuta Create ni callbacks de actor sincrónicamente. Es un fundamento estático de scope corto, no lock global ni garantía frente a otros mods con hooks/reentrada.

La sala se resuelve con el camino público ya usado por G2: `getStatusProcID(room)` → `fopScnM_SearchByID` → perfil ROOM_SCENE/ID/inicialización → `room->base.layer` registrada. Se comprueba el vínculo público process_node y padre de escena; IDs/punteros de G2 no se reutilizan. Link puede tener owner5 mientras el hijo de sala es6: no exigir igualdad. La capa padre PLAY_SCENE prolongaría lifetime a otras salas y amplía el ensayo; **no es la opción principal**.

Scope: caller previo registrado; owner local registrado, no-root, node completo y sin creaciones/eliminaciones pendientes; contexto, estado de sala/transición y pertenencia a escena revalidados antes de la llamada. Seleccionar owner, pedir E_OC CURRENT con callbackNULL, registrar ID escalar y restaurar caller. `fpcM_Create` captura current; fases posteriores seleccionan el request.layer. Cambiar room_num o mover owner después no sustituye este contrato.

`IsDeletingMesg` solo lee delete_count. Los demás guards de identidad, node, estado y nextStage son necesarios; tampoco forman una reserva vitalicia. Punteros prestados solo locales, sin yield, workers, llamadas a UI, operaciones de escena ni callbacks propios dentro del scope. Restauración LIFO/error no deshace una solicitud; exception después de aceptación incierta consume el intento y obliga a cierre, sin retry. Fallo de memoria/SEH no se presenta como recuperación garantizada.

## Riesgos mitigables y bloqueos concretos

| Ruta | Sabemos / mitigable | Impide runtime mientras falte |
|---|---|---|
| A1 | Owner natural; edición propia retirable. Duplicación mitigable coordinando consumo/retiro. | No hay ciclo natural de consumo acreditado ni identidad directa; punto sin admitir. No elegir A1 solo por recomendación anterior. |
| A2 | Mecanismo oficial de scope, nodo público observador, tracking ID y latch únicos; cierre sin callbacks DLL en actor. | Consumidor específico sin revisión/link/lab; owner real en instante de solicitud, punto y guardas sin acreditar. No elegir por test Dawnlight solamente. |

Estos bloqueos permiten preparar un **controlador desarmado** en una tarea autorizada; no exigen NO_TEST_ROUTE_YET. No se ha aprobado preparar módulo activo. La cancelación ABI no probada no se añade al camino crítico de una sesión sin transiciones ni unload: no se utiliza y se declara cierre de proceso como salida. Si se exigiera cancelar inmediatamente manteniendo el juego abierto, ese contrato seguiría BLOCKED.

`fpcSCtRq_Request(layer,...)` es otra función oficial acreditada, pero desplaza allocation/append/error ownership al consumidor. No reduce complejidad ni ofrece rollback mejor; no iniciar un tercer sistema. A1 permanece como alternativa si falla el contrato del scope A2: cambiar ruta requiere evidencia concreta, no ejecutar ambas.

## Escenario y decisión final

Mantener **F_SP121 / room3 / logical6 como escenario de evaluación**, porque ya tiene E_OC naturales, FILIbitSwFF, recursos y geometría local estudiados. No hay otra ubicación aprobada en la evidencia revisada. Ni punto antiguo ni posiciones de enemigos originales se adoptan como defaults.

Una sala nativa más simple y sin eventos sería una alternativa para evaluación posterior si el terreno local no permite admitir un punto; requiere solo sala/capa real, FILI, recursos E_OC/E_ocb efectivos, superficie/clearance local y owner vivo, sin barrido del juego. La arena Dawnlight requiere hooks de admisión: no es alternativa ya acreditada.

El beneficio decisivo de A2 es eliminar recarga/edición/reconsumo e identidad inferida **a cambio de validar un scope de owner acotado**. Recomendación final: **RECOMMEND_A2** para el primer ensayo; G4 y G5 permanecen bloqueados hasta sus gates específicos.
