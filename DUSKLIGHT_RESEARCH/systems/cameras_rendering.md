# Cámaras, render y backend

Fuente: `TwilitRealm/dusklight@40457c6adb381928e4b5fef6ed459ed291edd5e2`. Objetivo: Dusklight 2.0.3, Windows x64, DX12, GZ2E01. Esta ficha registra inspección estática; no se ejecutó el juego ni un mod. Los símbolos del juego que aparecen aquí no tienen disponibilidad de enlace ni hook demostrada por su mera existencia.

## Cámara y ciclo de vida

`CameraService.get_camera` recibe una vista del juego viva, valida frustum/perspectiva y devuelve matrices column-major compatibles con WebGPU, incluyendo reversed-Z consultado a Aurora. No determina que un `void*` cualquiera sea válido. `register_camera_operator` copia callback, prioridad y user_data a un slot owned. Al ejecutar solo acepta cámara principal: ordena prioridad descendente, secuencia ascendente y aplica el primer callback que devuelve true mediante `dCamera_c::Reset`; cada candidato parte del estado inicial, no del estado producido por el anterior. Unregister/detach retira slots. **PRES-007/008**: [src/dusk/mods/svc/camera.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/mods/svc/camera.cpp#L55-L128); [src/dusk/mods/svc/camera.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/mods/svc/camera.cpp#L142-L243).

El call site está al comienzo de `dCamera_c::Run`, después de `ResetView`; detached y debug fly camera preceden al operador. Si este gana, aumenta frame/ticks y retorna antes del seguimiento normal. Esto impide asumir que un operador agrega una transformación a cualquier cutscene o cámara secundaria. **SOURCE_OBSERVED, PRES-009**: [src/d/d_camera.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/d/d_camera.cpp#L1058-L1075).

## Contrato gráfico y fases reales

`GfxService` usa la API C WebGPU. `get_device_info` entrega device/queue/adapter/instance prestados, formatos y reversed-Z. Un objetivo DX12 no convierte estas interfaces en `ID3D12Device*`: aquí no hay tal contrato. Servicios y callbacks de etapa se llaman desde game thread; draw/compute corren en render worker y solo pueden usar contexto y llamadas wgpu, sin otros servicios. Contextos viven durante callback y targets resueltos durante frame; objetos GPU creados por el mod son responsabilidad del mod. **STATIC_CROSSCHECKED, PRES-010**: [sdk/include/mods/svc/gfx.h](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/sdk/include/mods/svc/gfx.h#L16-L39); [src/dusk/mods/svc/gfx.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/mods/svc/gfx.cpp#L1061-L1118).

| Fase oficial | Call site en `m_Do_graphic.cpp` | Uso observado |
|---|---|---|
| `GFX_STAGE_SCENE_BEGIN` | [src/m_Do/m_Do_graphic.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/m_Do/m_Do_graphic.cpp#L2331-L2338) | Contexto de cámara/viewport de escena |
| `GFX_STAGE_SCENE_AFTER_TERRAIN` | [src/m_Do/m_Do_graphic.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/m_Do/m_Do_graphic.cpp#L2363-L2370) | Inserción posterior al terreno |
| `GFX_STAGE_SCENE_AFTER_OPAQUE` | [src/m_Do/m_Do_graphic.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/m_Do/m_Do_graphic.cpp#L2392-L2399) | Inserción posterior al opaco |
| `GFX_STAGE_FRAME_BEFORE_HUD` | [src/m_Do/m_Do_graphic.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/m_Do/m_Do_graphic.cpp#L2756-L2762) | Inserción de frame antes de HUD |
| `GFX_STAGE_FRAME_AFTER_HUD` | [src/m_Do/m_Do_graphic.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/m_Do/m_Do_graphic.cpp#L2817-L2823) | Inserción de frame posterior al HUD |

La validación del servicio acepta exactamente esas etapas y structs suficientes. `resolve_pass` conserva compatibilidad con tamaños antiguos para attachments. El propio host usa `AuroraGXSync` como workaround de sincronización; no declarar seguridad universal de concurrencia por la presencia de mutex. **PRES-011/013**: [src/dusk/mods/svc/gfx.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/mods/svc/gfx.cpp#L31-L33); [src/dusk/mods/svc/gfx.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/mods/svc/gfx.cpp#L1304-L1328); [src/dusk/mods/svc/gfx.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/mods/svc/gfx.cpp#L1339-L1389).

## Retirada y alcance Windows/DX12

Desactivación retira tipos Aurora bajo ownership y llama synchronize si retiró IDs draw/task; esta fase ocurre antes de mod_shutdown, sin implicar que detenga hilos propios del mod; detach además libera claims de ventanas/desconfigura superficies. El mod debe desregistrar sus callbacks y liberar sus objetos GPU, nunca conservar targets de un frame previo ni liberar handles prestados. **PRES-012**: [src/dusk/mods/svc/gfx.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/mods/svc/gfx.cpp#L176-L186); [src/dusk/mods/svc/gfx.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/mods/svc/gfx.cpp#L1013-L1032).

Clasificación: cámara/Gfx `OFFICIAL_SERVICE`; interceptar la cámara o render original a mano sigue `POTENTIAL_REQUIRES_VERIFICATION`. Dependencias: [modelos](models_animations_materials.md), [HUD](hud_ui_text.md), [lifecycle](runtime_and_lifecycle.md), WindowService y Aurora. **BLOCKED**: backend interno extern/aurora `3227d76c60e1e782ca576610bce61c9e7744d8be` no descargado. Compilación shader, precisión/profundidad, surface loss y coste de sincronización en Windows DX12 son **NOT_VERIFIED**. No inferir Vulkan ni paridad de GPU.

Cobertura: READ/CROSSCHECKED selectiva según SYSTEM_INDEX y los niveles de cada evidencia; ninguna ruta constituye prueba runtime Windows/DX12.
