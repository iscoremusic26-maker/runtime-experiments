# DEVF_NATIVE_API_PAIR_HUMAN_RUNTIME_OBSERVED_PASS

Cierre posterior al build0.7.1, limitado a F_SP121/sala3/capa6 y dos arranques Windows/DX12 reportados. Procedencia: **confirmación humana + extractos comunicados por el usuario**; Codex no recibió ni leyó bytes de logs completos, no inspeccionó píxeles ni recalculó hashes.

| Sesión comunicada | Configuración | Evidencia y observación |
| --- | --- | --- |
| dusklight-20261015-140237.log | Proveedor0.7.1+probe0.1.0, JSON NONE | Usuario observó un Bokoblin nativo adicional en FIELD. API_PUBLISHED_BOOTSTRAP_OPEN; REQUEST_ACCEPTED owner=dev.devf.native_api_probe site=0 result=0 token=1; PROBE_REQUEST_ACCEPTED_EDIT_ONLY;2/2mods activos. Apagado: REMOVE_RESULT result=0, PROBE_OWN_EDIT_REMOVED, all mods unloaded. Recuento aproximado comunicado:10E_OC frente a9retail; no identifica placement con PID. |
| dusklight-20261015-140350.log | Sólo proveedor0.7.1, JSON NONE | Usuario confirmó ausencia del adicional. CONFIG_ACCEPTED_STAGE_EDITS_REGISTERED configured=0 edits=0;1/1mod activo;all mods unloaded al salir. |

**PASS HUMAN_REPORTED** para la secuencia par+NONE→un FIELD y proveedor solo+NONE→ninguno. No evidencia de hot unload, FPS, universalidad, ActorId↔placement ni otros escenarios. Los logs embebidos HUMAN_PENDING permanecen inmutables; este dictamen es posterior.

Build histórico38787691561 y descarga38788164065 permanecen SUCCESS; fuente compilada ae4fa410e4543c032fccfe761b2a817ae17479b2. Checkpoint anterior c72ba3909b618f555c07cbeabd95e2fd1f4d4efa. No recompilación/reempaquetado del par0.7.1 para este cierre, no QA histórica repetida ni rawlogs publicados. CP07.2A es un artefacto posterior con QA humana independiente pendiente.
