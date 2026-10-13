# Resolver A2: revisión de las guardas nuevas

**OWNER_STATIC_SUFFICIENT_FOR_TEST_DESIGN**, condicionado al caller original y listas sanas; **A2_RUNTIME_OWNER_NOT_VERIFIED**. No se encontró un defecto demostrado que justifique modificar código. Son correctas como preflight conservador las comprobaciones añadidas a G2; no constituyen reserva de lifetime ni monitor nativo de requests pendientes.

Base b342a8dfdf47fa503f02cb91c470d66e646334c5. Fuente oficial exacta40457c6adb381928e4b5fef6ed459ed291edd5e2; checkout limpio. Revisado únicamente `capture_owner` y sus predicados nuevos. Laboratorio/MSVC/binario históricos permanecen PASS y no se ejecutaron otra vez.

## Referencias oficiales focalizadas

Todos los enlaces están fijados al commit oficial:

- O1 [d_stage.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/d/d_stage.cpp):251–267 setStay/next,279–292 createRoomScene,315–365 flags de residencia.
- O2 [d_s_room.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/d/d_s_room.cpp):198–285 objectSetCheck/Execute;365–370 registra ID en phase0;474–505 finaliza Create;514–524 perfil CURRENT.
- O3 [f_op_scene.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/f_op/f_op_scene.cpp):44–64 añade tag temprano y copia append a parameters. [Scene lookup](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/f_op/f_op_scene_mng.cpp):13–15 busca en lista de escenas.
- O4 [f_pc_executor.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/f_pc/f_pc_executor.cpp):40–81 init2 al entrar en cola de ejecución; retiro→init3. [create_req](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/f_pc/f_pc_create_req.cpp):18–33 lookup pending por ID,104–118 fin/fallo.
- O5 [d_s_play.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/d/d_s_play.cpp):1161–1165 phase1 asigna mProcID. [d_stage.h](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/include/d/d_stage.h):1140–1145 getters stay/next/proc;1161–1164 checkStatusFlag;1215–1218 room ID.
- O6 [f_pc_node.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/f_pc/f_pc_node.cpp):45–61 scope de node Execute;107–124 crea layer interna con el node. [f_pc_layer.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/f_pc/f_pc_layer.cpp):43–81 contadores;95–118 registro/current/search;135–170 retiro/creación y process_node. Tipos públicos `include/f_pc/f_pc_node.h`, `f_pc_layer.h`, `include/f_op/f_op_scene.h`.
- O7 [f_pc_node_req.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/f_pc/f_pc_node_req.cpp):285–310 captura current/parent para node nuevo. Se verifica el vínculo real; no se deduce por room_num.
- O8 [door_shutter](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/d/actor/d_a_door_shutter.cpp):1788–1797 anticipa next y cambios de status; [door_spiral](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/d/actor/d_a_door_spiral.cpp):341–350 prepara next antes de cambiar stay.
- O9 [f_ap_game.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/f_ap/f_ap_game.cpp):811–832 tick antes de management, contraste ya acreditado. No nueva auditoría del loader/motor.

## Matriz de guardas añadidas

FR=falso rechazo; AI=aceptación indebida posible bajo límites indicados. PASS_LAB histórico prueba predicados sobre datos sintéticos, no lecturas reales del resolver.

| Condición | Fuente | Demuestra | No demuestra | FR | AI/límite | Estático | Runtime exacto |
|---|---|---|---|---|---|---|---|
| ID status→scene + perfil ROOM_SCENE | O2/O3/O5 | Objeto de escena con ID y tipo buscados | Ready por mera presencia | ID temprano/stale→rechazo | Lookup no pin | PASS_STATIC | ID/tipo encontrado en instante de preflight |
| room.parameters == room | O1/O3 | Entero room del append copiado, no encoding ACTR | Estado de todos sus hijos | Formas no nativas rechazadas | Caller/source fuera del contrato | PASS_STATIC | Parámetro coincide con room3 |
| init_state2 y !IsCreating(node) | O2/O4 | Create finalizó y pasó a ejecución, fuera de request queue | Recursos de una nueva adición o futuro teardown | Init1/3 rechazados deliberadamente | No cubre una intención futura de borrar | PASS_STATIC + PASS_LAB | Valores del node real y cola en ese tick |
| getProcID→PLAY_SCENE, ID/init/capa registrada | O5/O6 | Identidad global asignada al PLAY en phase1 y node completo | mProcID por sí solo prueba escena actual viva | Stale/transición/incompleto rechazados | No reserva del objeto | PASS_STATIC | Play encontrado, completo y vínculo observado |
| room.layer_tag.layer == &play.layer | O6/O7 | ROOM pertenece directamente al árbol del PLAY validado | Igualdad con owner de Link, cualquier escena anidada | Room de otro árbol legítimo se rechaza | No inferir vínculo por dos números solos | CONDITIONALLY_SUPPORTED | Comparación de punteros en capture; guardar solo resultado/IDs |
| child.process_node==room.base; play análogo | O6 | Backlinks exactos creados por fpcLy_Create | Vida persistente de los punteros | Otro modelo de node se rechaza | Listas/memoria corruptas fuera de premisas | PASS_STATIC | Booleans de backlink durante captura local |
| child registrado y ID coincide con G2 | O6/G2 Registry | Identidad dentro del registro vivo del tick | Generación/refcount o validez en tick posterior | Registro incompleto/ciclo/límite rechaza | ABA/otro tick no cubierto | PASS_STATIC, lector G2 histórico | Root/previous/child/parent registrados, no IDs fijos |
| child != root y != parent; parent==play_layer | O6 + core | Selección del hijo, no root/capa del padre | Scene lifetime o equivalencia con logical6 | Contextos distintos al contrato rechazados | Premisa binding ya validada | PASS_STATIC + PASS_LAB | IDs y bindings efectivos; Link owner solo informativo |
| root/current/previous cotejados con G2 | O6/G2 | Caller previo localizado; discrepancia se rechaza | Previous inmortal ni identidad por entero aislado | Cambios durante captura rechazan | Reentrada destructiva no soportada | CONDITIONALLY_SUPPORTED | Previous válido en momento de uso; root puede ser previous |
| status &0x2e ==0 | O1/O2/O5 | Sin bits2/4/8/0x20 que anuncian setup/retirada/limpieza | Ausencia de toda transición/evento | Limpieza selectiva o preparación con node vivo rechaza | Señales externas/futuras no cubiertas | PASS_STATIC | Estado/máscara del room actual |
| stay3, next==stay, !nextStage | O1/O8 | Sin destino de room anticipado ni nextStage marcado | Next distinto significa node ya muerto | Puerta puede mantener room estable mientras next difiere | Intención no reflejada aún en getters | PASS_STATIC, conservadora | next/stay/nextStage en tick de intento |
| contadores hijo/padre ==0; !IsDeleting | O6 | Sin trabajo contado en esas capas antes del intento | Lock, todas las colas o toda descendencia | Trabajo de sala vecina/otro hijo rechaza | No cubre pendientes de otro subsistema | CONDITIONALLY_SUPPORTED + PASS_LAB | Counts exactos; ausencia de delete_count>0 |
| IDs stage/room/play/logical recotejados al final | O1/O5 + resolver | Detecta cambio observable durante captura | Snapshot atómico frente a concurrencia | Cambio normal en ventana rechaza | Cambio sin señales/ABA no detectado | CONDITIONALLY_SUPPORTED | Contexto efectivo coherente antes del futuro scope |
| host_verified/update_context del caller | O9/lifecycle | Sitio previsto del loader y headers/version/epoch | OS thread ID, ausencia absoluta de reentrada o pin | Otro caller debe rechazarse | true manual fuera del contrato no valida hilo | CONDITIONALLY_SUPPORTED | Caller normal; adaptation aún RUNTIME_NOT_VERIFIED |

## Carga, estabilidad y retirada

`getStatusProcID` se escribe en phase0 **antes** de terminar Create. `fopScn_Create` también pone la escena en la lista temprano. Por eso profile/lookup no bastan; init2 y ausencia de request completan el criterio. Parámetro de room se copia del entero creado por createRoomScene; no hay bits superiores que deban enmascararse en este flujo. Los backlinks comparados son los tipos reales del host, sin offsets de comentarios32-bit.

Durante estabilidad, setStayNo deja next==stay. Una puerta puede cambiar next mientras stay y ROOM_SCENE permanecen vivos: **el resolver rechaza más que nodos destruidos**, de forma intencionada para un ensayo sin transiciones. Counts del padre pueden reflejar otra sala residente; también es veto conservador. Máscara0x2e incluye estado2 anterior al primer Execute y0x20 limpieza selectiva aunque room sobreviva. No retirar estas restricciones para conseguir PASS.

Al retirar node, init3/counters/flags y retiro de tag/registry aportan rechazos; los IDs globales pueden persistir pero lookup ya no encuentra objeto. Hay intervalos de intención pendiente sin toda señal aplicada: ninguna combinación es lock. Dentro del tick original, los getters/list walks nuevos no ejecutan Create/Delete ni ceden hilo, y no introducen una operación incompatible con tick→management. No hay pointer que salga de capture_owner.

## Límite específico: preflight, no monitor pending

El resolver comienza con `capture_native` G2, que rechaza creates/deletes/censo incompleto. **No puede usarse sin adaptación como lector de owner durante nuestro futuro request pendiente**, aunque el monitor abstracto del core tolere create_count1. Esa es una separación de contratos ya declarada, no un error del módulo desarmado que nunca crea. El futuro monitor necesitará resolución escalar de contexto/ID coherente con pending; no fingir readiness ni devolver PASS rellenando booleans. No se implementa aquí.

## Decisión de observación

Los vínculos y falsos rechazos están suficientemente fundamentados para diseñar el ensayo: **no exigir otra campaña G2/A2 solo para volver a probar este contrato estático**. Sí hay que verificar el owner mediante estas guardas en la sesión futura, inmediatamente antes del scope; nunca adoptar node102/child6/parent5 históricos. Esto conserva RUNTIME_NOT_VERIFIED.

La evidencia local que falta para el punto puede necesitar una captura desarmada futura. Se puede incluir el Owner escalar en **esa misma captura**, sin imponer un segundo observador ni un ciclo de recarga A1. [EXACT_REMAINING_EVIDENCE](EXACT_REMAINING_EVIDENCE.md) delimita la captura; no se autoriza ni se implementa ahora.
