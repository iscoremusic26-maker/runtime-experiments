# Diseño futuro: A2 one-shot, sin código activo

**DOCUMENT_ONLY / DISARMED_NO_REGISTRATION.** Una sola instancia E_OC normal; ningún StageService edit, perfil nuevo, post-callback, hook, patch, cambio HIO o modificación del ejecutable. No se crea `.dusk`, DLL ni spawner en esta revisión.

Escenario de evaluación: F_SP121 / room3 / logical6. Preset conservado: perfil `fpcNm_E_OC_e=0x1FE`, nombre canónico `E_oc`, parametersFFFFFFFF, argumento−1, angle.x−236/FF14, yaw0, z0, escala(1,1,1), setIDFFFF mediante ActorService, callbackNULL. Recursos nativos E_OC y E_ocb. **XYZ = UNASSIGNED_UNTIL_ADMITTED**; el punto anterior no es un default. Aprobación del escenario no aprueba el punto.

## Contratos e interfaces conceptuales

`Intent`: una acción manual explícita pendiente, sin llamada nativa desde UI. `Snapshot`: valores propios de host/contexto/node/child layer y ubicación admitida; nunca pointers persistentes. `Attempt`: slot preasignado, latch de sesión, ID escalar, epoch/node/layer de contexto y estado. `ResolveOwnerNow`: punteros públicos prestados exclusivamente en el tick. Son especificaciones, no interfaces implementadas.

Estados: DISARMED → intent validado → ATTEMPT_CONSUMED → REQUESTED/PENDING → READY_OBSERVED → STOP_SESSION. Rechazo previo no crea nada; después de ATTEMPT_CONSUMED no se rearma ni se reintenta, incluso si devuelve error. No seleccionar otra ruta como fallback automático. Una nueva sesión y nueva autorización serían necesarias para otra prueba.

## Flujo de solicitud (pseudocódigo no ejecutable)

```text
En mod_update, en game thread y sin ejecución anidada:
  si no existe autorización/intent manual y punto admitido: permanecer desarmado
  resolver de nuevo host, stage, room, logical, Link, PLAY_SCENE y ROOM_SCENE
  verificar registro/identidad/perfil/init de node y capa hija, estado de sala,
    contadores sin pending, no nextStage/teardown/evento incompatible
  comprobar contexto y condiciones locales del punto admitido
  resolver caller previous y owner room-child; ambos registrados, owner != root
  consumir latch y preparar Attempt; no allocations propias después de este punto
  en scope local de restauración:
    seleccionar room-child, comprobar current == owner
    solicitar exactamente E_OC nativo con callback NULL
    conservar resultado y ID en slot propio; restaurar previous al salir
  validar restauración y resultado; incertidumbre/throw -> STOP_SESSION, sin retry
En siguientes ticks:
  resolver contexto y actor por ID nuevamente, sin reutilizar pointer del tick anterior
  si contexto cambió, error, timeout o identidad inconsistente -> STOP_SESSION
  si pendiente: observar, no modificar/delete ni solicitar de nuevo
  si actor completo + identidad/owner coherentes: READY_OBSERVED
  observar intervalo autorizado; parada -> cierre completo, nunca hot reload
```

No retener ningún pointer de player, escena, layer, actor o create_request. La validación del player parte de cola pública/identidad antes de dereferenciarlo, como G2; room node mediante búsqueda en lista de escenas. LayerId se resuelve por búsqueda y se coteja con vínculo público node, no se toma6 como constante. Verificar que parent scene realmente corresponde al PLAY_SCENE vigente. Ni nombre de room ni owner no-root aislado satisfacen el contrato.

## Guardas y límites de ownership

- Solicitud solo en update del juego, scope sin yield/worker/render/UI callbacks, sin llamadas de escena ni setters de progreso. Una guardia de reentrada rechaza intento anidado.
- Usar root/current/search/set de ABI oficial; headers exactos, sin offsets de comentarios32-bit. Previous puede ser root como contexto del caller que se restaura: **solo owner target se prohíbe root**.
- Node identificado y completo, hijo registrado y vinculado, contadores create/delete0 antes de encolar; estado de sala sin retiro/recarga pendiente y no transición. `IsDeletingMesg` es dato parcial, no pin/lock.
- Guardas runtime posteriores no exigen create_count0 del owner mientras nuestro request está pendiente: sería rechazar el efecto de la propia solicitud. Separar precondiciones de creación del monitor pending.
- Captura de request ocurre en `fpcM_Create` y fases usan request.layer. Owner correcto evita **estáticamente bajo ese contrato** el camino root+global draw; verificación real de owner/render queda pendiente. No reparar paquetes ni mover propietario después.
- Scope RAII restaura en retorno/error/C++throw ordinario; no deshace aceptación, no salva una escena destruida por reentrada ni recupera SEH/memoria corrupta. Ambiente sin mods que alteren esos contratos y revisión del código son requisitos del experimento.

## Identidad, recursos y asincronía

El ID al retorno pertenece al intento; no adoptar el primer E_OC ni `get_actor_id(profile)`. En cada tick resolver ID, comprobar proceso/perfil0x1FE, room3, owner del node esperado, estado init completo, fuera de cola de creación y condición actor INIT; componentes de modelo/animación nativos requeridos antes de declarar visual-ready. No inspeccionar componentes derivados durante Create ni deducir éxito porque IsCreating seafalse.

G2 tiene procedimientos de lectura/rechazo reutilizables, pero no certifica readiness de una adición. Si actor no está visible aún, mantener pending hasta criterio combinado/error/timeout, sin cancelar a ciegas. Si sale del contexto, retirar asociación y detener; un ID escalar no posee generación ni autoriza actuar sobre un posible reemplazo. No escribir stats ni aplicar delete en este ensayo.

Los bytes ARC y contrato Create ya están acreditados. No invocar hooks de load/heap ni callbacks DLL: Create carga E_OC/E_ocb y sus métodos nativos. Preferir una sala con recursos ya naturalmente presentes; comprobar disponibilidad pertinente antes del intento, sin igualar registered aloaded. Fallo de fase/heap o modelo faltante es resultado negativo y parada, no razón para modificar recursos o repetir solicitud.

Un request que termina tarde puede seguir produciendo actor nativo mientras la escena exista. Latch permanece consumido; no retry, cancel ABI o unload. El host no recibe referencias a código/datos privados de DEVF desde parámetros/append/post-method; los datos de ActorSpawnParams se copian por ActorService. Esto reduce riesgo de callback DLL pendiente, sin probar limpieza total de la escena.

## Ubicación e intervalo operativo

Usar evidencia local existente y admitir un punto específico antes de armar. Revisar clearance inicial/suelo/material/agua/paredes/techo, overlap de originales y eventos/triggers pertinentes. Las cotas401/494/501 son condicionadas de recurso; no contienen movimiento. No adoptar300 delante de Link, WALK≤800 ni radio2000 como garantía.

La prueba empieza con Link sin combate/acción deliberada y sin transición/evento incompatible. La búsqueda social es global; observar actores próximos relevantes, no pretender inexistencia mundial de aliados. Una reacción nativa es evidencia de comportamiento, pero combate, salida del área vigilada o interacción inesperada termina el ensayo. No exigir demostrar todas las trayectorias posibles antes del primer request.

Presupuesto finito de pending y observación debe fijarse y justificarse en la revisión del futuro paquete; hoy no hay duración aprobada. Timeout no congela/destruye actor. Create ejecuta una vez dentro de creación: no existe pausa garantizada para validar al enemigo antes de que actúe. Si el riesgo local no puede aceptarse con esas condiciones, no activar, aunque el ensayo sea corto.

## Evidencia, parada y retirada

| Momento | Evidencia futura mínima |
|---|---|
| Antes | Host intacto/versión/ABI/DX12; mods/config; stage/room/logical; node/child/caller y estado; recursos; punto admitido y condiciones locales; baseline originales. |
| Solicitud | Un intento, perfil/params/transform/callbackNULL, owner elegido/current durante llamada/previous restaurado, retorno e ID propio. |
| Completion | ID propio resuelto, perfil/room/owner, pending→init/componente listo, timestamps y errores. |
| Render/comportamiento | Clip/fotos+logs correlacionados: Link y E_OC visibles, movimiento inicial, sin error/ciclo/draw duplicado. No declarar PASS de daño/colisión/cleanup no ejercitados. |
| Fin | Razón de parada, request/actor estado último, proceso completamente cerrado y paquete retirado antes de nuevo inicio. Terminación del proceso no demuestra G6. |

Parar ante owner incorrecto/no registrado, Link ausente/invisible, packet/cycle/staging/DX12 error, múltiples intentos/IDs inesperados, fase fallida, pending excedido, transición/cambio de identidad, salida del ámbito observado, combate/progreso/guardado inesperado o host que no responde. No intentar reparar escena, forzar unload o cancelar un request parcialmente conocido. Cierre normal si responde; si cuelga, terminar el proceso mediante Windows y conservar evidencia. Esto limita la sesión, no promete ausencia de crash ni reversión de escrituras ya realizadas.

Instalación futura separada y reversible solo con autorización expresa, revisión independiente y backups de saves/config. Verificar autosave y prevenirlo por configuración oficial reversible si existe; ninguna escritura deliberada de progreso. No atribuir aislamiento a G2 con Randomizer/texturas. Desarmar controlador bloquea nuevas solicitudes, **no** elimina enemigo/pending. Mantener módulo hasta cierre completo; retirar solamente paquete TEST tras confirmar fin del proceso. No confiar en shutdown como veto de unload.

G6 posterior exige ensayo separado de transición natural con instancia viva, pending y descendientes, desaparición de IDs/capas y ausencia de huérfanos/duplicados, con logs reales. No es efecto demostrado del cierre. Descarga personalizada sigue BLOCKED y CP02 NO-GO.
