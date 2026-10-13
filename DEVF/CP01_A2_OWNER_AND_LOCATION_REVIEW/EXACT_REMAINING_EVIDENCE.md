# Evidencia pendiente exacta y captura mínima propuesta

**No falta el SDK, los ARC, la arquitectura ni otro cálculo de navegación universal.** Falta vincular el medio y la ocupación del punto al contexto real de una sesión. Ningún archivo original o log completo se solicita en esta entrega.

## Datos indispensables para decidir sobre el punto

| Dato exacto | Por qué importa / propiedad obtenida | Evidencia actual y carencia | Fuente/método mínimo | Offline o runtime | Gate |
|---|---|---|---|---|---|
| Medio efectivo en C: GroundCross pertinente, room del soporte, superficie especial/agua sobre soporte y BG dinámico que intersecte el volumen inicial | Excluir vacío/suelo incorrecto, agua y una intersección inicial grave; no confundir suelo con ausencia de agua | KCL2174/ground0 y cobertura100/501 acreditados; el JSON declara expresamente que no prueba no-water/dynamicBG. Modelos autorados no contienen registro BG actual | Captura de solo lectura en la instalación: consulta de suelo/agua con los tipos/filtros públicos usados por el nativo y comparación con soporte existente; resultados numéricos/IDs/estado de BG relevantes, no recursos. Alcance en el punto/envolvente inicial, no toda room | No se deduce la composición dinámica actual offline. Requeriría captura futura autorizada; validar sólo los imports nuevos si se implementa | Medio/clearance inicial del candidato |
| Posición/volumen de Link y ocupantes físicos relevantes alrededor de C en el instante de evaluación | Excluir overlap inicial con Link/actores originales, conservando sus instancias | G2 llega a488.5791XZ; siete E_OC room3 alejados en28muestras. No son estado presente ni censo de colliders/BG cargados | Reutilizar iteración pública G2 para copiar IDs/perfil/room/owner y posiciones relevantes locales; validar volúmenes/colliders públicos pertinentes cuando exista contrato. No usar cull box o distancia de centro como prueba. No segunda enumeración global ni escribir a actores | Captura futura de solo lectura. Si un volumen no puede acreditarse por API pública/evidencia, registrar NOT_VERIFIED: no offsets ni bounding inventado | No solapamiento inicial del candidato |
| Contexto actual sin evento/puerta/coach/escolta/transición incompatible, layer6 efectiva y recursos nativos accesibles | Evitar ensayo dentro de evento/progreso/carga ya en curso y vincular evidencia con escena real | G2 layer6 y recursos registered; no estado de evento/nextRoom/play binding nuevo ni sesión aislada. ARC e integridad ya resueltos | En la misma captura: contexto escalar del resolver, señal pública de evento activo y estado local pertinente/observación sanitizada; disponibilidad E_OC/E_ocb del flujo nativo. No flags editados, no historia completa ni hashes de buffers runtime | Datos actuales requieren runtime; contratos, presets/FILI y recursos están acreditados offline. Carga final del nuevo actor sólo será observable durante futuro ensayo | Contexto de ubicación; autorización futura distinta de aprobar geometría |

C significa exclusivamente (-4806.7346,-6729.480961460304,65135.8281), F_SP121/R3/logical6. Los datos son **requisitos definidos**, no lecturas realizadas. El bloqueo es FIRST_TEST_LOCATION_BLOCKED_EXACT_EVIDENCE; no se usa el desconocimiento como prueba de agua/actor/evento presente.

## Owner: suficiente para diseño, comprobación obligatoria antes de actuar

**OWNER_STATIC_SUFFICIENT_FOR_TEST_DESIGN.** No hace falta una campaña adicional del resolver solo para confirmar otra vez las reglas del código. La guarda debe pasar en el instante de una futura solicitud y el owner de la instancia debe observarse después; ambas garantías runtime siguen pendientes.

Si la captura local requerida para C se autoriza posteriormente, aprovechar `capture_owner` existente y su presupuesto **máximo16 registros/cadencia120updates**, sin reimplementar G2. Payload mínimo correlacionado con las lecturas locales:

- stage/room/logical, stay/next y nextStage; previous/root registrados.
- node ID, parámetro room/profile/init/completo fuera de request; child ID registrado y backlink correcto.
- play ID/profile/init, play_layer y parent del room, boolean de vínculo directo; Link owner informativo, sin igualdad requerida.
- counts hijo/padre, status &0x2e, IsDeleting y reason de validación final; sin pointers persistidos ni valores5/6 constantes.
- suelo/agua/BG/ocupación/evento de C en el mismo contexto, o NOT_VERIFIED explícito si la lectura no está disponible.

El `Owner` ya contiene casi todos los valores/booleans; el diagnóstico actual imprime solo reason/node/child/play/previous. La captura más detallada sería una **adaptación futura de logging/lecturas focalizadas**, no una corrección que se haga ahora ni otra implementación del observer. Status mask/perfiles/init pueden requerir exponer el dato que ya se comprueba localmente, sin guardar puntero. Un snapshot válido basta para acreditar lo observado en ese momento; más registros solo si ayudan a explicar un rechazo, sin repetir28 capturas. No demuestra estabilidad perpetua ni ejecuta el setter de capa.

La consulta de medio/colliders deberá usar únicamente interfaces oficiales cuyo contrato sea verificable. Esta revisión no presupone una API universal de overlap que no se ha acreditado. Si falta acceso público a un dato indispensable, conservar su NOT_VERIFIED y delimitar el recurso/observación local específico; no sustituirlo por offsets/hook ni diseñar otra auditoría del motor.

## Qué no forma parte del camino crítico

No pedir de nuevo ARC/ZIP/ROM/SDK/EXE/save/log G2 completo; no reestudiar models/BCK/Hermite/501/KCL/overlays. No exigir recarga natural/RTBL/SCLS para A2 ni censo social de todas las salas o confinamiento800/2000/2300. No exigir label68,0x1E08,0x0C01 o switchE3 a priori cuando el contexto efectivo/sesión sin evento basta para este caso. M_RGate00 no es un input automático por contener event_list R03_gate.

Preflight in-game, revisión del futuro adapter request/readiness/identidad, binario/paquete, backups/autosave y autorización manual son gates posteriores de activación; no se implementan aquí. La generación/reutilización de IDs y cleanupG6 no están resueltos por los fakes. Sus contratos deben conservar límites, pero no se abre una investigación general ahora.

## Siguiente operación mínima

Revisión/autorización separada para **una captura local desarmada del punto C** con medio/BG/ocupación/evento, incluyendo el Owner escalar existente. Después decidir admisión con esos datos, sin nuevos XYZ, barridos o spawn. No se solicita al usuario ejecutarla en esta entrega, no hay `.dusk` ni instrucciones de instalación/runtime.
