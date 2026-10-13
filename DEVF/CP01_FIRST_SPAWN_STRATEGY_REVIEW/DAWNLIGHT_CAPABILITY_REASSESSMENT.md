# Dawnlight: capacidades y evidencia reutilizable

Revisión estratégica desde `4276a0562eb156d04569be38b5cc2dc987cd074a`. Dawnlight exacto: `9bb214d47617c9bc295d22facf36c35d17661e5a` / v4.0.3. Host objetivo: Dusklight oficial `40457c6adb381928e4b5fef6ed459ed291edd5e2` / 2.0.3, Windows x64/DX12. La versión de Dawnlight no acredita la versión de su host: CMake usa 2.0.0 por defecto, sobrescribible. No se compiló ni ejecutó ningún proyecto.

## Qué acredita cada clase de evidencia

| Clase | Resultado reutilizado | Límite |
|---|---|---|
| A: capacidades en código / PASS_STATIC | Spawner con 43 etiquetas, E_OC, parámetros por perfil, GroundCross, ActorService, scope de capa y tracking temprano. Cave conserva datos de requests originales y cambia perfil antes de allocation. | Catálogo no es whitelist de 43 enemigos seguros; spawner y Cave completos usan hooks. |
| B: pruebas simuladas | `enemy_spawner_scene_test.py` extrae el helper: restaura contexto en éxito/error/throw, rechaza root/deleting/nextStage y simula draw/cleanup. Ground helper tiene test separado. | Engine, fases, render y colas son stubs; vacía pending antes del teardown simulado. No acredita cancelación, reentrada real o DX12. No se volvió a ejecutar. |
| C: funcionamiento reportado | `darknut-arena-spawner.md:3–34`: confirmación de usuario en bd7347d, build #342, problemas de Link invisible/duplicación de draws y retorno al hub corregidos mediante selección de owner. | Evidencia externa favorable y técnicamente coherente; no identifica aquí host/renderer de cada distribución ni valida DEVF. |
| D: traslado al SDK oficial | ActorService y ABI de capa/request/suelo acreditados en auditoría anterior; perfil E_OC CURRENT. | Consumidor A2 específico, lifecycle y render DEVF aún NOT_VERIFIED. |
| E: incompatibilidades | Hooks de admisión, proceso/descendientes, phase_Load/allocation, correcciones de estado y daytime global. | NO REUTILIZABLE bajo las restricciones; no se introducen bypasses aunque no escriban saves. |

## Clasificación de mecanismos

| Mecanismo | Clasificación | Aplicación y límite |
|---|---|---|
| Seleccionar perfil/argumento/preset antes de solicitar | REUTILIZABLE DIRECTAMENTE EN CONCEPTO | E_OC nativo conocido; no modificar actor ya reservado ni actores originales. |
| ActorService como solicitud individual | REUTILIZABLE CON ADAPTACIÓN | Guardas, owner de ROOM_SCENE y un único intento. No copiar `create_standalone_actor`, que instala hooks. |
| Selección temporal de capa y RAII | REUTILIZABLE CON ADAPTACIÓN | Funciones oficiales; propietario de sala validado en el mismo tick, no adoptar ciegamente owner de Link. RAII restaura contexto, no revierte request ni protege punteros destruidos. |
| Registro de solicitudes | REUTILIZABLE DIRECTAMENTE EN CONCEPTO | Guardar ID escalar inmediatamente, slot propio previamente reservado; request ≠ listo y ID no es handle con generación. |
| GroundCross / finite / room | REUTILIZABLE CON ADAPTACIÓN | Ground helper de Cave rechaza NaN, suelo ascendente y otra sala; su elección de piso más bajo y offsets no son regla general para Field. |
| Parámetros por enemigo | REUTILIZABLE DIRECTAMENTE EN CONCEPTO | Reutilizar semántica, conservar el preset DEVF; tabla Dawnlight no determina inocuidad. |
| Error y restauración | REUTILIZABLE CON ADAPTACIÓN | Sin retries tras intento incierto, sin excepción/alloc propia después de encolar; no asumir rollback transaccional. |
| Descendientes mediante hooks | NO REUTILIZABLE BAJO NUESTRAS RESTRICCIONES | No interceptar createChild ni process. Ownership nativo común fundamenta teardown, no tracking exhaustivo por parentID. |
| Limpieza | REUTILIZABLE CON ADAPTACIÓN | Ciclo de escena y cierre completo del proceso; borrar metadatos/uninstall no cancela pendientes ni destruye actores. No hot reload. |
| Cave Randomizer completo | NO REUTILIZABLE BAJO NUESTRAS RESTRICCIONES | Intercepta cargas/requests/allocation y reemplaza originales. Solo transferir conceptos de contexto, tipo previo y suelo. |
| Admisión mediante hooks | NO REUTILIZABLE BAJO NUESTRAS RESTRICCIONES | Respetar FILI y estado real; sin falsificar consultas, parchear flags o HIO. |

## E_OC: diferencia exacta de presets

Fuente focalizada: `src/d/actor/d_a_e_oc.cpp:2704–2747,349–370,2848–2870` del host exacto. Tabla de spawner Dawnlight y Cave usa `0x00FF0000`. DEVF conserva `0xFFFFFFFF`, angle.x `-236 = 0xFF14`, yaw0, z0, escala1, argumento−1; XYZ no admitido.

| Campo | DEVF FFFFFFFF | Dawnlight 00FF0000 | Consecuencia |
|---|---|---|---|
| Byte bajo: modo | FF normalizado a0 | 0 | Mismo modo normal; no puente2 ni demo3/4. |
| Byte8–15: búsqueda | FF → S | 0 → S | Ambos radio S1200 por defecto, no M5000 (que exige byte1). No inmunidad a detección/aliados. |
| Byte16–23: derrota | FF | FF | Ambos desactivan consultas/escrituras guardadas del switch de derrota. |
| Byte24–31: switch secundario | FF | 0 | Diferencia real. `searchPlayer2` lo escribe en modo2; no activa esa rama en modo0. No convertir 0 en garantía de ausencia de todos los efectos. |
| Modelo y rango: **angle.x**, no parameters | FF14 → E_OC normal, rango2000 | Spawner angle.x0 → E_OC normal, rango0; Cave también pone X0 | Mismos recursos normales, distinta política de retorno. Rango0 no inmoviliza y no es confinamiento. |

Ninguna diferencia simplifica el ensayo de forma acreditada. FFFFFFFF conserva los dos sentinels y el rango autorado investigado; cambiarlo o poner X0 perdería parte de la correspondencia con la evidencia existente. Recursos: E_OC + E_ocb, modelo y arma nativos; no E_OC2. WAIT puede pasar a WALK sin input y Create ejecuta una vez antes de la siguiente observación. No se promete inmovilidad ni ausencia absoluta de escrituras del juego.

## La heurística delante de Link

Spawner: 300 unidades delante, probe Y+500, un GroundCross y rechazo exclusivo del sentinel −1e9. Acredita un intento de colocar el origen en una superficie bajo ese probe. No comprueba finitud allí, pertenencia a room, pendiente, agua, techo, paredes, clearance de cuerpo/arma, overlap de actores, eventos o navegación posterior; tampoco fija owner. Acercarlo a Link puede favorecer detección normal inmediata. No trasladar 300 como distancia segura.

La mejora Cave finite/room sigue sin certificar esos aspectos. Para DEVF, el punto debe admitirse por separado con evidencia local reutilizada y comprobaciones dirigidas; no generar coordenadas nuevas mediante esa heurística ni aprobar el antiguo candidato.

Referencias y procedencia completas, sin repetir la auditoría: [COMPARATIVE_AUDIT](../CP01_DAWNLIGHT_AUDIT/COMPARATIVE_AUDIT.md), [SCENE_OWNERSHIP](../CP01_DAWNLIGHT_AUDIT/SCENE_OWNERSHIP.md), [RECOVERY previo](../CP01_DAWNLIGHT_AUDIT/RECOVERY.md). Los seis archivos Dawnlight solicitados se consultaron focalizadamente; no se investigó todo el proyecto.
