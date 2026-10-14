# Camino A — decisión focalizada

**BLOCKED_WITH_EVIDENCE.** A0 (callback nula) reduce el riesgo de descarga de DLL, pero no acredita el momento inicial de HP 150 antes de combate ni la limpieza de toda solicitud propia al desactivar/reload. A1 (callback de DLL) sigue sin un contrato de retención/revocación hasta completar o cancelar la solicitud. No se autoriza un prototipo con estas lagunas.

Esta tarea solo autoriza investigación y evaluación conceptual de una escritura tipada sobre la instancia demostrablemente propia. No se ejecutó ninguna escritura, juego, DLL, compilación, instalación ni empaquetado. Base documental `08433c6cb338637ec4191bdcc454cbc9537ad7df`; informes de PR22 y checkpoints CP01/CP02 intactos. CI no cambia.

## Qué aporta esta revisión

1. **A0 sí evita la callback colgante:** `create_function=nullptr` hace que PostMethod no invoque código del mod. El actor usa el perfil nativo. Un actor pendiente o vivo tras descargar el mod no implica por sí mismo un use-after-free de DLL; sí puede quedar un enemigo de prueba sin propietario que lo retire.
2. **Identidad útil:** la solicitud y el proceso utilizan el mismo ID. La búsqueda simple de ActorService puede encontrar actores todavía en creación: el wrapper añade el actor a su cola antes de native create. Solo obtener un pointer o una room no acredita readiness.
3. **Timing nuevo:** `mod_update` precede `fpcCt_Handler`, que precede execute/draw. Cuando E_OC2 completa create asigna 220 y ejecuta su primera acción; puede entrar además en la ejecución/dibujo ordinarios antes del siguiente update del mod. No se afirma que reciba un golpe en esa ventana; tampoco hay una garantía de que no lo haga. Aplicar 150 después de daño podría restaurar salud, contradiciendo el objetivo.
4. **Permiso técnico distinto de autorización:** docs/modding.md 126–127 permite a mods nativos llamar funciones públicas y leer/escribir campos del juego. No hay una imposibilidad general de acceso tipado a `health`. Esa documentación no otorga al encargo permiso de escritura real ni demuestra ownership/contexto/lifetime; sigue faltando una excepción explícita para la próxima tarea.
5. **Dos precisiones al informe previo:** `delete_actor` no es cancelación general por ID, pero puede alcanzar un actor parcialmente creado y activar el abort del engine si ya existe en la cola; no siempre es un no-op mientras se crea. `unload_native` retira la imagen y la descarga físicamente en el próximo drenaje, no necesariamente al instante. Ese retraso no espera a solicitudes de actores.

## G1–G8

| Gate | Estado | Evidencia / límite |
|---|---|---|
| G1 identidad exclusiva | PASS_SOURCE | Mismo ID solicitud→proceso, sin búsqueda por perfil/proximidad. Es un ID de proceso, no un token de ownership/generación permanente. C01–C03; [IDENTITY_AND_TIMING](IDENTITY_AND_TIMING.md). |
| G2 stage/room/layer y fase | NOT_VERIFIED | Hay getters tipados, pero room 3 no equivale a layer 6 ni a sala lista. ActorService hereda la capa de procesos actual, distinta de la capa de datos 6. No se demuestra un gate atómico de contexto y disponibilidad de recursos. C09. |
| G3 inicialización efectiva 150 antes de combate | BLOCKED | A0 solo observa terminación en un update posterior a native create/execute/draw; la ventana 220 existe. No hay punto público de mod_update entre fin de create y primer execute. A1 tiene mejor punto de aplicación pero bloquea G5. C04–C05. |
| G4 acceso tipado y semántica | CONDITIONAL | NEEDS-RULE_EXCEPTION: escritura única a health de la instancia propia, tras readiness/ownership y antes de daño; sin offset ni global ni field_0x560. Lectura de este último solo acredita inicialización conjunta, no HP máximo. C06. |
| G5 ningún código del mod pendiente tras unload | PASS_SOURCE para A0; BLOCKED para A1 | A0 no registra callback; A1 retiene dirección mientras la solicitud persiste y el loader no espera ni acepta veto de shutdown. C07–C08; [LIFECYCLE_SAFETY](LIFECYCLE_SAFETY.md). |
| G6 errores, cambio de sala, muerte, reload y cleanup | BLOCKED | No hay ownership de solicitudes nativas por ModContext ni cancelación pública total por ID. Falta cobertura antes de crear el actor y ante rechazo de delete; reload puede pedir otro actor mientras el anterior permanece. C03/C07/C08. |
| G7 ABI/enlace/compatibilidad | CONDITIONAL | SOURCE-VERIFIED soporte GameABI 2 y llamadas públicas; imports concretos de una DLL futura NOT_VERIFIED. Requiere ampliar la auditoría StageService-only de CP02, sin copiar su PASS ni modificar SDK/lib. C10. |
| G8 observabilidad | CONDITIONAL | DESIGN-PROPOSAL de telemetría ligada al ID propio y valores leídos, no MOD_OK=HP. Sin medición runtime ni prototipo actual. C11. |

Los IDs C01–C11 corresponden a [evidence/source-references.json](evidence/source-references.json): commit fijo, hashes, rutas y rangos reales. PASS_SOURCE significa lectura de fuente, nunca build o runtime.

## Decisión posterior mínima

Una excepción de escritura por sí sola no cierra G3/G6. Dentro del contrato actual no se propone un `.dusk`. El mínimo contrato upstream necesario está en [LIFECYCLE_SAFETY](LIFECYCLE_SAFETY.md): solicitud nativa poseída por ModContext, estado/cancelación por token y override inicial copiado por host antes de primera acción/combate, sin callback de DLL. Es una propuesta que exigiría cambiar host/SDK/versionado y el requisito de 2.0.3 intacto; no se implementa ni se solicita aprobación de un cambio concreto al host ahora.

CP01 y CP02 siguen utilizables con los PASS humanos reportados de aparición/comportamiento/retirada; 220 HP y daño no se midieron. No se entrega `IMPLEMENTATION_PLAN_IF_GO.md` porque el gate no habilita implementación. No CP04.
