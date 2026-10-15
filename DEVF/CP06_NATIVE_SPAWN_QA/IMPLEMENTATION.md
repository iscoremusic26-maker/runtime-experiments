# Implementación mínima de dos paquetes nativos

## Registros y build
`native_records.hpp` serializa explícitamente la estructura ACTR de32bytes BE: name[8]=E_oc, parametersFFFF0100, XYZ float32, ángulos0106/0000/0000 y setIDFFFF. No se añade un ID a campos de guardado. Los bytes completos de ambos records se contrastaron en Windows con `struct.pack(">8sIfffhhhH",...)`, independiente del constructor C++.
El perfil510, recurso E_OC2/preset220 nativo proceden de la resolución ya comprobada de ese record; el QA no registra perfiles ni mide/escribe salud. No cambio de recursos.
A y B son targets DLL/manifest independientes que comparten el core. Compile-time DEVF_QA_MODE=1/2 determina uno norte o dos (sitio1,norte); no configuración oculta. El macro DEVF_SOURCE_SHA lleva el commit realmente compilado.
No FEATURES game: el SDK oficial permite módulos sólo servicios. Host2.2/Log1.0/Stage1.0, ABI1; cero HookService/ActorService/FileService, cero imports de dusklight.exe. No se enlazó importlib ni se recompiló host/SDK/Aurora; se usó add_mod/package oficial sin modificarlo.

## Alta y fallo
Registros fijos/finitos y contextos ya validados se construyen sin asignación de memoria en el mod. Antes de la primera alta se validan contexto/API. `attempted` impide reintentos durante la misma carga de DLL. Se conserva sólo cada StageActorHandle de la llamada propia; no actor pointers/IDs/allocations del host.
Si una alta falla, arroja excepción, devuelve0 o duplica handle, se retiran los handles propios recibidos en orden inverso. También se captura un handle escrito antes de una excepción. Cleanup fallido se conserva para reintentar en shutdown; nunca se busca/borran registros ajenos.
Retorno MOD_ERROR de initialize provoca detach del mod por host, que retira sus ediciones como fallback según StageService1.0. Esto es rollback de ediciones, **no garantía de borrar un actor ya vivo**. Sólo arranque/cierre frío autorizado, no hot reload.
`mod_update` devuelve MOD_OK sin registrar ni crear nada. Reaparición al cargar sala depende de la creación nativa/ediciones de StageService, no de un loop del mod. No se afirma ausencia runtime de duplicados/reentrada hasta prueba humana.
Shutdown retira sólo sus handles e informa resultado. El host conserva propiedad de los actores y su destrucción nativa; no callback del mod queda en ellos.

## Telemetría y límites
Log acotado inicial/final: id/version/source/mode/escenario/room/layer/count/handles/posición norte/retorno/cleanup. `STAGE_EDIT_REGISTERED` demuestra registro y **NO** nacimiento. Sin logs por frame, rutas personales, census/HP/identidad de retail o render.
B añade1200 unidades Z respecto de sitio1; no confinamiento de movimiento. Los dos pueden moverse por IA nativa. Personalización por instancia sigue PENDIENTE y no bloquea estas altas nativas. No se implementó otra estrategia de hooks.
