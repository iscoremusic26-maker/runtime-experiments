# Gates siguientes — plan, no ejecución ni autorización de TEST

**Estado actual: documentación terminada; DISARMED_NO_REGISTRATION; CP02 NO-GO. No existe paquete activo de esta auditoría.** Referencias D/S y versiones exactas en COMPARATIVE_AUDIT. Los gates siguientes no se han ejecutado dentro del juego ni autorizan continuar automáticamente.

## Evidencia reutilizable y datos que no se vuelven a pedir

- DEVF base545b2d1, fuentes oficiales40457c6, SDK/import library/EXE 2.0.3 ya verificados CP00; baseline host Windows y laboratorios CP01 anteriores. No volver a descargar los ZIP, compilar host o repetir sus suites.
- Datos ya observados: F_SP121, room3, layer efectivo6, entry-4, posición original(-4056.7346,-6717.1538,65135.8281), angle s16-24697. Candidato **de análisis anterior** (-4806.7346,-6729.480961460304,65135.8281), yaw0, scale1. No pedir de nuevo esos números ni tratarlos como ubicación aprobada de un enemigo.
- ARC/colisiones/WRock/rutas/Digpl y sus límites se conservan en CP01; no rehacerlos por rutina. Su caja no es la de E_SB/E_RD/Darknut. La aprobación de un enemigo requiere solo los datos **nuevos y específicos** que no cubra esa evidencia.
- Auditoría actual: contratos de captura de capa, call path A1 de sala, 18 imports/exports seleccionados de escena/request/suelo/contexto, params seleccionados y límites de las pruebas simuladas Dawnlight. **PASS_STATIC**, no readiness/render/cleanup real.

## Secuencia mínima

| Gate | Evidencia faltante / comprobación dirigida | Criterio de aprobación o bloqueo |
|---|---|---|
| G0 — expediente del enemigo y escena | Elegir explícitamente un único enemigo/preset; resource names, admission FILI, switches específicos, flags/eventos del contexto, medio/hora y descendientes/modos que se usen. Reutilizar fuente/evidencia disponible antes de pedir nada. | Contrato nativo admitido sin falsificar consultas, escribir flags o modificar recursos. Si necesita un hook/global bypass: **BLOCKED**, cambiar el caso con fundamento. |
| G1 — consumidor Windows desarmado/observador | Solo si se prepara nuevo código autorizado: compilar/enlazar los imports ABI realmente usados contra SDK/lib exactos y GameService epoch2; observar identidad de host y contextos. No host build ni Dawnlight port. | Version/build/API compatibles, código disarmado y sin registro/creación. Exports presentes son premisa, no sustituyen este link específico. No repetir 26 tests no afectados. |
| G2 — observación oficial, sin spawn | Nueva autorización para cargar/ejecutar un observador. Host.version/build_id, Windows x64, DX12 confirmado, mods activos, stage/room/layer lógico, current layer, owner de Link y del nodo de room vivo, transición y delete_count. Recursos requeridos y admission del caso, disponibles mediante evidencia de instalación. | Distinguir layer lógico del motor; propietario correcto, válido y estable. No necesitar offsets privados ni alterar estado para admitir el perfil. Falta de evidencia implica **NOT_VERIFIED/NO-GO** para aparición. |
| G3 — laboratorio adicional, únicamente para A2 elegida | Captura/restore del scope, nested calls LIFO, retorno de error/exception, guards de capa, owner capturado antes/después. Si se usa cancel ABI: lookup/base pública, is_doing, cancel/fallo parcial y no reutilizar pointer liberado. Usar código original pertinente o declarar los adapters, no presentar stubs como engine proof. | Expectativas dirigidas PASS con límites documentados; consumo de headers/imports validado en Windows. No reutilizar los 17 tests del parche como prueba del original. **No es prerrequisito de implementar A1**, donde no se añade setter de capa propio. |
| G4 — ubicación específica y recursos | Para enemigo seleccionado: soporte/pendiente/altura, techo/pared/agua si aplica, envolvente/render/colliders, actores/eventos/triggers, recursos/animaciones/armas necesarias. Inferir únicamente de datos disponibles y de observación dirigida de instalación; no inventar coordenadas. | Punto y room/layer fundamentados para ese enemigo, sin reemplazar originales ni depender de un switch/story change. Recursos instalados acreditados. Si falta un archivo, identificar solo el recurso concreto requerido; no solicitar de nuevo ARC ya publicados. |
| G5 — ensayo A1 único | Autorización nueva del usuario, paquete TEST separado y revisado, una sola entrada Add registrada antes de la **recarga natural** de la sala verificada. Sin A2 paralela, sin nuevos perfiles/post-callbacks/hooks. | Actor esperado completa Create; owner de room observado y no-root; cantidad/identidad discernibles; render de Link/enemigo/colisión probados con evidencia real. La prueba no se ejecuta por el mero hecho de aprobar el informe. |
| G6 — retiro y transiciones reales | Retirar definición; comprobar efecto en carga posterior, cambio de room/stage, pending request y descendientes del modo elegido. No asumir aparición inmediata ni kill instantáneo al retirar edit. | Cleanup nativo observado y sin duplicados/huérfanos en secuencia definida. Si la room sigue cargada, no exigir destrucción que ese contexto no promete; registrar su lifetime hasta salida real. Errores, ID ambiguo, migración no controlada o bloqueo de carga mantienen **NO-GO** de esa garantía. |
| G7 — variantes A2 individuales | Tras cumplir G0–G4 y su gate de laboratorio, autorización separada para una sola solicitud ID propia con owner verificado; readiness/componente específico antes de cualquier atributo. Una instancia vanilla de control cuando se estudie un campo. | Identidad/readiness/lifetime acreditados por caso, sin callbacks DLL en enemigo ni escritura compartida. Solo después estudiar una feature por tipo, sin avanzar aquí a CP02. |

G1/G2/G4 pueden resolver sus datos nuevos sin activar enemigos. G3 se requiere al elegir un nuevo mecanismo A2, no como investigación general que retrase A1. La primera aparición mínima candidata es **G5 A1**, después de sus requisitos específicos y autorización; no los 43 perfiles, no una Cave completa y no una arena cuyo admission solo funciona mediante hooks Dawnlight.

## Cómo observar sin inventar propiedad/identidad

Un plan de logs futuro debe usar funciones y datos públicos del ABI exacto; pointers se resuelven y validan en el tick, no se almacenan como ownership duradero. Registrar etapa, host/build/renderer, instante/contexto, ActorId cuando exista, perfil, room, layer lógico, layer_id/owner observado, estado de creación y resultado. Publicar solo logs propios sin recursos originales o datos personales.

A1 no entrega IDs. Usar un ensayo controlado con censo baseline, los registros/actores originales ya conocidos y parámetros/transform/contexto de la única adición. **No basta el primer actor de ese perfil ni una coincidencia de posición.** Si el método de observación no distingue la entrada de un spawn vanilla/evento, queda pendiente y se detiene el ensayo; no aplicar stats/delete a ese match. A2 entrega el ID de solicitud, pero el registro puede representar creación pendiente, actor visible no inicializado, fallo o desaparición. fpcM_IsCreating por sí sola no acredita readiness ni muerte; este último matiz evita recompensas duplicadas por unload/fallo.

Dawnlight device reports son una hipótesis contrastada útil, no un gate superado de DEVF. D3/D5 son tests simulados inspeccionados, no nuevas pruebas ejecutadas. Ningún futuro run C++ lab sustituye Windows/DX12 runtime; cada fila runtime debe conservar NOT_VERIFIED hasta disponer de su evidencia.

## GO/NO-GO y parada

| Decisión | Condición objetiva |
|---|---|
| Auditoría documental completada | Los seis informes, referencias exactas y checkpoint recuperable; no implica GO de aparición. |
| Listo para solicitar autorización de TEST A1 | G0/G1/G2/G4 resueltos para un caso, identidad observacional no ambigua, paquete separado revisado y rollback claro. Hoy **BLOCKED** por evidencia runtime/contexto/recursos/ubicación del enemigo pendiente; no hay paquete preparado. |
| PASS de aparición/limpieza | Solo G5/G6 ejecutados en host oficial Windows x64 DX12 con logs y evidencia real. Hoy **NOT_VERIFIED**. |
| Garantías A2 | G3 y G7 más requisitos de contexto específicos; exports o test Dawnlight no los satisfacen. Hoy **NOT_VERIFIED**. |
| Descarga DLL de perfiles personalizados | Bloqueo original independiente conservado, sin adoptar parche. **BLOCKED**. No se exige ni se proclama resuelto por un enemigo nativo. |
| CP02 | **NO-GO**. Esta tarea no la inicia ni satisface las garantías del producto completo. |

La autorización de un ensayo específico no autoriza hot reload, reenable, más perfiles, stats o cambios de entorno. Parar ante Link invisible, dobles draws, errores/ciclos de render, scene owner incorrecto, pending que no termina, recurso/actor ambiguo o cambios de progreso inesperados; conservar logs y no ampliar el caso para enmascararlos.

## Recuperación y reversión futuras

Para cualquier prueba autorizada después: verificar ejecutable oficial y checkpoints antes de iniciar; conservar los originales y archivos privados fuera de publicaciones. Instalar manualmente solo el paquete de prueba autorizado, sin reemplazar EXE/ROM/saves. Sesión controlada sin guardar cambios de progreso; cerrar el proceso para revertir estado volátil y retirar únicamente el `.dusk` de prueba antes de relanzar. No fiarse de un shutdown failure para impedir unload ni del retiro de Stage edit para eliminar al enemigo actual. No realizar hot reload/reenable durante la primera secuencia.

No se realizó instalación o modificación de partidas en esta auditoría y no hay reversión runtime pendiente. La recuperación documental se detalla en [RECOVERY](RECOVERY.md); retomar esa referencia no arma los prototipos ni autoriza CP02.
