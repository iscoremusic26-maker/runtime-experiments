# DEVF CP01 — contraste focalizado de Dawnlight

**Resultado: A1 tiene un contexto nativo de sala acreditado estáticamente; A2 necesita seleccionar y validar explícitamente su propietario cuando se invoca fuera del proceso de un actor. Hay funciones oficiales exportadas para investigar esa selección sin hooks. Ninguna ruta obtiene PASS runtime Windows/DX12 en esta auditoría. CP02 NO-GO.**

Base DEVF: `545b2d1418bfcae11dd4585c1a9bdcbc526b6a2d`, tag `DEVF_CP01_OFFICIAL_SDK_ARCHITECTURE`. Dawnlight: `9bb214d47617c9bc295d22facf36c35d17661e5a`, tag `v4.0.3`. Dusklight oficial: `40457c6adb381928e4b5fef6ed459ed291edd5e2`, versión 2.0.3. Solo documentación: no código funcional, port, hooks, compilación, ejecución, paquete ni instalación.

Se reutilizaron ARCHITECTURE_DECISION, FEASIBILITY_MATRIX, ROUTES_AND_CONTRACTS, OFFICIAL_HOST_RISKS, SOURCE_REVIEW y TEST_RESULTS del checkpoint base. Continúan válidos: copia ACTR32/TGSC35, handle de edición ≠ ActorId, retirar Stage edits ≠ borrar instancias, request ≠ actor listo, almacenamiento propio, variantes por tipo pendientes y bloqueo independiente del perfil DLL personalizado. Las 26 expectativas MSVC anteriores no se repitieron ni se reinterpretaron como pruebas del motor.

## Clasificación

A: técnica compatible mediante servicios/ABI oficiales con contrato estático acreditado. B: adaptación fundamentada que necesita comprobar requisitos. C: mecanismo dependiente de hooks, supuestos privados o modificaciones excluidas. Estado separado: `PASS_STATIC`, `PARTIAL`, `NOT_VERIFIED`, `BLOCKED`, `INCOMPATIBLE`. Un export acredita disponibilidad, no seguridad semántica ni ejecución.

| Mecanismo / aprendizaje | Dawnlight: archivo, función, líneas | Contraste oficial 2.0.3 / limitación | Clase y estado |
|---|---|---|---|
| Propiedad de escena distinta del room | D1, create_test_actor_in_player_layer, 211–230; D2, 8–42 | S1→S2→S3→S4/S5 capturan la capa al encolar. room solo es un dato del append. | A / PASS_STATIC del contrato; comportamiento DEVF NOT_VERIFIED. |
| Selección temporal de capa y restauración | D1, helper 213–229 | S7 ofrece setter/getter; S13 ya usa selección de play layer en el host original. Disponibilidad PE/implib comprobada abajo. Precisa mismo hilo, capa viva, contexto estable y nesting LIFO. | A / PASS_STATIC para mecanismo; B / NOT_VERIFIED para política completa A2. |
| Registro de ID inmediatamente tras solicitar | D1, 263–269, 334–336 | ActorService devuelve ID de request. Puede observarse más tarde sin post-callback DLL. No es prueba de readiness ni ownership de descendientes. | A / PASS_STATIC de ID; B / PARTIAL de tracking. |
| Detectar/eliminar descendants del spawner | D1, after_create_child 142–151; before_process 154–188; install_test_hooks 232–258 | Los hooks de createChild/process no se adoptan. parent ID no fuerza layer; hay creación sin parent ID. Las APIs de lectura podrían identificar algunos hijos después, sin cubrir su admisión previa a Create. | C / INCOMPATIBLE para hooks; B / NOT_VERIFIED para observación sin hooks. |
| Aislar consultas de admisión por proceso | D1, process stack 129–188; D6, hooks de switch/dungeon bit 719–751 | Dawnlight mantiene la arena nativa como cleared mediante respuestas alteradas y deja consultas vanilla a IDs tracked. No basta con parámetros individuales para eliminar el gate FILI de S17. | C / INCOMPATIBLE. Alternativa A: escena/flags que admitan naturalmente el perfil; ninguna escritura de saves o bypass. |
| Standalone Staltroop / agua / lava | D1, before_process 167–179, appear/wait 191–208 | Timers/estados se fuerzan desde hooks, incluso skip de wait. No son parámetros universales ni compatibilidad ambiental demostrada en 2.0.3. | C / INCOMPATIBLE del mecanismo. B: escoger enemigo/entorno nativos compatibles. |
| Presets específicos | D1, tablas 27–119; spawn params 321–331 | E_SB se conserva como referencia anterior y no está en esas tablas. E_RD y Darknut se contrastan con S16/S18; no auditar las 43 opciones ni convertir el catálogo en whitelist. | A / PARTIAL de semántica seleccionada; runtime NOT_VERIFIED. |
| Elegir perfil antes de reservar memoria | D4, before_allocate 246–275 | S6 reserva profile.process_size. La lección de elegir tipo antes de crear es válida; reescribir args de fpcBs_Create por hook no lo es. | A / PASS_STATIC para configurar una solicitud propia; C / INCOMPATIBLE para sustituir requests vanilla interceptadas. |
| Conservar room, parent, setID y request/layer | D4, after_request 183–201 y before_allocate 265–274 | Cave conserva el request original y el contexto roomReLoader. No captura mágicamente el contexto de UI ni puede transferirse la seguridad por copiar un room. | A / PARTIAL como invariantes de diseño; C para interceptación. |
| Esperar suelo / fallback tras 120 intentos | D4, find_ground 204–217, before_load 220–244; D5, 15–34 | Consultar suelo está respaldado por ABI/export. Suspender phase_Load mediante hook requiere función sin declaración SDK, y está excluido. Alternativa B: validar suelo antes de una solicitud propia; no hay garantía de pausar el reloader nativo con Stage.add_actor. | A / PASS_STATIC de herramientas; B / NOT_VERIFIED de política de suelo; C / INCOMPATIBLE del hook. |
| Superficies de la misma sala | D5, find_ground 15–34; test 9–38 | Evita aceptar un piso de otra sala cargada, NaN y probes ascendentes. Elegir el piso más bajo de Cave es una política específica: no garantiza suelo seguro para Field, pendientes, agua, eventos o envolvente del enemigo. | A / PARTIAL; adaptación de ubicación B / NOT_VERIFIED. |
| Excluir generadores/coordinadores | D4, after_request 194–199 | Wolfos pack espera hijos del mismo tipo; sustituirlos por otro tamaño/tipo puede invalidar casts. Elegir solo solicitudes propias conocidas evita esa sustitución. | A / PASS_STATIC de límite de diseño; la exclusión concreta se respalda aquí en el código/comentario Dawnlight, no en una nueva auditoría Wolfos 2.0.3. |
| Stalhound diurno forzado | D4, before/after_stalhound_process 128–160 | Cambia daytime global y usa hooks, aunque restaure y trate nesting. No es atributo independiente de una instancia. | C / INCOMPATIBLE. Alternativa: respetar horario y condiciones nativas, pendiente por enemigo. |
| Limpieza de pendientes del randomizer | D4, update/shutdown 279–304 | Borrar s_pending es olvidar metadatos, no cancelar requests del host. Uninstall tampoco destruye actores. No adoptar una garantía de limpieza por ese código. | A / PASS_STATIC de esa distinción; garantía general BLOCKED. |

## Versiones, ABI y disponibilidad real

Dawnlight **4.0.3** es versión del mod. Su CMake D7:4–12 elige Dusklight **v2.0.0** por defecto. D8:35–59 permite un DUSKLIGHT_DIR existente o una versión sobrescrita: el default **no demuestra** qué host/ABI usó cada build o prueba de dispositivo. No se compiló Dawnlight ni se investigaron dependencias 2.0.0. Cada contrato transferido se contrastó de nuevo con el **ámbito pertinente** de 2.0.3; no se importaron offsets 32-bit de comentarios como layouts Windows x64.

El SDK objetivo expone esos headers mediante GameABIConfig y `FEATURES game`, con **GameService major 2** como epoch. Un `.dusk` futuro que use estas funciones debe importar ese feature/ABI y enlazar la import library exacta, además de comprobar versión. El objeto ABI anterior no enlazó estos símbolos específicos; no se presenta como validación de la futura combinación.

Comprobación nueva, read-only y focalizada: la import library local ya recuperada por CP00 tiene 9400986 bytes y SHA256 `4dc4a511d761e6eb52541733fa31919a2234ed9cd5b2f16f8fea91c468f30ca4`, idéntico al miembro acreditado en `DEVF/evidence/input_verification.json`. Se leyeron sus short import objects seleccionados: **AMD64, destino dusklight.exe**, y se cotejaron con los registros conservados de exports PE de CP00. Se reutiliza la equivalencia previa de los 30042 imports/exports; no se revalidaron ZIP, ARC o fuentes completas ni se distribuyeron binarios. Suficiente para **PASS_STATIC de presencia**, no para PASS de link/ejecución nuevo.

| Función ABI / símbolo MSVC seleccionado | Contrato examinado |
|---|---|
| `fpcLy_CurrentLayer` / `?fpcLy_CurrentLayer@@YAPEAUlayer_class@@XZ` | Getter actual, S7:105–106. |
| `fpcLy_SetCurrentLayer` / `?fpcLy_SetCurrentLayer@@YAXPEAUlayer_class@@@Z` | Asignación de contexto, sin retención/pin/lock, S7:101–103. |
| `fpcLy_RootLayer` / `?fpcLy_RootLayer@@YAPEAUlayer_class@@XZ` | Comparar raíz, S7:95–97. |
| `fpcLy_IsDeletingMesg` / `?fpcLy_IsDeletingMesg@@YAHPEAUlayer_class@@@Z` | Consulta delete_count, no un flag universal de escena, S7:43–51. |
| `fpcLy_Search` / `?fpcLy_Search@@YAPEAUlayer_class@@I@Z` | Lookup por layer ID, no ownership/refcount, S7:109–118. |
| `fpcSCtRq_Request` / `?fpcSCtRq_Request@@YAIPEAUlayer_class@@FP6AHPEAX1@Z11@Z` | Solicitud explícita de layer con append/post-method, S4:140–177. Posibilidad B; no API automática de rollback. |
| `fpcCtIt_Judge`, `fpcCtRq_Cancel`, `fpcCtRq_IsDoing` | Headers públicos/exports presentes, S5/S19. Permiten investigar lookup/cancel con base pública; contrato de fallo parcial y duración exige pruebas. No modificar requests ni copiar standard_create_request_class privada. |
| `fpcM_IsCreating` | Consulta pertenencia a cola, S3/S5. False no prueba éxito, modelo o render. |
| `dComIfGp_getPlayer`, `dComIfGp_isEnableNextStage` | Public wrappers/export presentes; puntero prestado y transición indicada, no reserva de escena. |
| `cBgS::GroundCross`, `dBgS::GetRoomId`, `cBgS_GndChk::SetPos(cXyz const*)` | Headers y exports presentes, S20. Resultado de suelo no acredita toda la ubicación. |
| `dBgS_GndChk` ctor/dtor, `g_dComIfG_gameInfo` | Disponibilidad de construcción/base y dato game-info. El dato exige declaración oficial dllimport; no offset privado. |

Los doce símbolos de capa/request/contexto y los seis de suelo/datos anteriores se verificaron por objetos de importación, no solo por buscar texto en headers. No se realizó un nuevo link ni ejecución: **NOT_VERIFIED** para su uso concreto en DEVF.

## Evidencia separada

- **Dawnlight, prueba simulada:** D3 extrae solo el helper y define ActorService/layer/render/cleanup con stubs. Inspección estática en esta tarea, sin ejecutar el script ni compilarlo. Lo que sus assertions cubren y omiten está en SCENE_OWNERSHIP.
- **Dawnlight, funcionamiento reportado:** D2:3–6,28–34 cita confirmación del usuario del revision `bd7347d` y build #342; logs/dispositivo descritos allí. Se registra como reporte externo, sin raw logs nuevos, build efectivo/renderer/versión de host acreditados aquí. No es evidencia propia Windows/DX12 de DEVF.
- **DEVF previo:** Windows/MSVC run38277234930 y 26 expectativas de codificación/desarmado/types se conservan con su alcance. No ejercitaron la captura de escena del host.
- **Esta auditoría:** únicamente lectura de código, contraste de exports/implib, hashes focalizados y preservación de árboles. **PASS_STATIC** donde procede; ejecución/render/limpieza DEVF **NOT_VERIFIED**. No se ejecutó una suite ni laboratorio nuevo.

## Referencias reproducibles

Los identificadores D y S de los seis informes remiten a estos commits, funciones y rangos. Las líneas se contaron sobre sus fuentes exactas; EOL no cambia las referencias.

| ID | Origen fijado, archivo y líneas de interés |
|---|---|
| D1 | [Dawnlight enemy_spawner.cpp](https://github.com/BeZide93/dawnlight/blob/9bb214d47617c9bc295d22facf36c35d17661e5a/src/enemy_spawner.cpp): tablas27–119, tracking142–188, adaptations191–208, helper211–230, hooks232–258, entry263–269/287–337. |
| D2 | [Dawnlight darknut-arena-spawner.md](https://github.com/BeZide93/dawnlight/blob/9bb214d47617c9bc295d22facf36c35d17661e5a/docs/darknut-arena-spawner.md): reporte3–6/28–34, mecanismo8–58, hijos90–100, pruebas132–147. |
| D3 | [Dawnlight enemy_spawner_scene_test.py](https://github.com/BeZide93/dawnlight/blob/9bb214d47617c9bc295d22facf36c35d17661e5a/tests/enemy_spawner_scene_test.py): extracción6–16, stubs18–78, assertions80–129, g++133–140. |
| D4 | [Dawnlight cave_randomizer.cpp](https://github.com/BeZide93/dawnlight/blob/9bb214d47617c9bc295d22facf36c35d17661e5a/src/cave_randomizer.cpp): hooks21–32, catálogo45–78, tiempo128–160, requests183–201, suelo/load204–244, allocation246–275, cleanup279–304. |
| D5 | [Dawnlight cave_randomizer_ground.hpp](https://github.com/BeZide93/dawnlight/blob/9bb214d47617c9bc295d22facf36c35d17661e5a/src/cave_randomizer_ground.hpp): find_ground15–34; [test cpp](https://github.com/BeZide93/dawnlight/blob/9bb214d47617c9bc295d22facf36c35d17661e5a/tests/cave_randomizer_ground_test.cpp):9–38. |
| D6 | [Dawnlight new_save_modes.cpp](https://github.com/BeZide93/dawnlight/blob/9bb214d47617c9bc295d22facf36c35d17661e5a/src/new_save_modes.cpp): on_bossrush_area_dungeon_bit_pre719–734 y on_bossrush_area_switch_pre736–751. No revisión del resto de modos. |
| D7/D8 | [Dawnlight CMakeLists.txt](https://github.com/BeZide93/dawnlight/blob/9bb214d47617c9bc295d22facf36c35d17661e5a/CMakeLists.txt):4–12,47–48; [FetchDusklight](https://github.com/BeZide93/dawnlight/blob/9bb214d47617c9bc295d22facf36c35d17661e5a/cmake/FetchDusklight.cmake):35–59. |
| D9 | [Dawnlight enemy_spawner.hpp](https://github.com/BeZide93/dawnlight/blob/9bb214d47617c9bc295d22facf36c35d17661e5a/src/enemy_spawner.hpp):labels11–20, entradas públicas22–27. |
| S1 | [Dusklight actor service](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/mods/svc/actor.cpp):create220–250, child253–287, get/delete288–320. |
| S2 | [Dusklight f_op_actor_mng.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/f_op/f_op_actor_mng.cpp): layer136–149, append176–239, create258–313. |
| S3 | [Dusklight f_pc_manager.h](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/include/f_pc/f_pc_manager.h):fpcM_Create45–48; [cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/f_pc/f_pc_manager.cpp): DrawIterater36–38, IsCreating48–50. |
| S4 | [Dusklight f_pc_stdcreate_req.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/f_pc/f_pc_stdcreate_req.cpp): private struct21–31, phase allocation49–64/subcreate67–85, Request140–177. |
| S5 | [Dusklight f_pc_create_req.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/f_pc/f_pc_create_req.cpp): IsCreating18–33, ToCreateQ41–44, Cancel61–74, Do84–120, Create132–148; [public header](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/include/f_pc/f_pc_create_req.h):23–44. |
| S6 | [Dusklight f_pc_base.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/f_pc/f_pc_base.cpp): Execute59–81, Create133–170; [layer_tag](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/f_pc/f_pc_layer_tag.cpp):Init61–76. |
| S7 | [Dusklight f_pc_layer.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/f_pc/f_pc_layer.cpp):IsDeleting43–52, context95–128, Cancel145–147; [header](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/include/f_pc/f_pc_layer.h):14–44. |
| S8 | [Dusklight f_pc_node.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/f_pc/f_pc_node.cpp): Execute45–61, delete timing66–104, Create107–124. |
| S9 | [Dusklight d_stage.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/d/d_stage.cpp): name table907–926/990–991/1064, actorCreate1635–1662, layer assertion2298–2300, Stage helper2611–2633, roomReLoader2816–2835. |
| S10 | [Dusklight d_s_room.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/d/d_s_room.cpp): filters125–164, objectSetCheck198–264, Execute267–288, Create474–505, profile514–524. |
| S11 | [Dusklight f_pc_deletor.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/f_pc/f_pc_deletor.cpp):ToDeleteQ63–105, Delete107–135. |
| S12 | [Dusklight d_s_play.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/d/d_s_play.cpp): draw659–662; [J3DDrawBuffer.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/libs/JSystem/src/J3DGraphBase/J3DDrawBuffer.cpp):entryImm202–208. |
| S13 | [Dusklight commands.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/commands.cpp):403–410; [ImGuiActorSpawner.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/imgui/ImGuiActorSpawner.cpp):97–121. Se consulta como precedente, no se invoca código interno UI. |
| S14 | [Dusklight stage service](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/mods/svc/stage.cpp): create139–155, edits158–219. |
| S15 | [Dusklight E_SB](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/d/actor/d_a_e_sb.cpp):Create1097–1155, profile1171–1186; revisión anterior reutilizada. |
| S16 | [Dusklight E_RD](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/d/actor/d_a_e_rd.cpp):weapon208–209, migration2196–2209, children4963/6909/7140, Create7316–7495, profile7636–7651. |
| S17 | [Dusklight f_op_actor.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/f_op/f_op_actor.cpp):Create443–565, FILI517–536. |
| S18 | [Dusklight Darknut](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/d/actor/d_a_b_tn.cpp):Ending4179–4223/Zako4359–4429, dispatch4526–4531, Create5030–5164, profile5177–5192; [save query](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/d/d_save.cpp):isSwitch1621–1641. |
| S19 | [Dusklight f_pc_create_iter.cpp](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/f_pc/f_pc_create_iter.cpp):Judge19–24, filtro26–41; header f_pc_create_iter.h28–31. |
| S20 | [Dusklight ground header](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/include/d/d_bg_s_gnd_chk.h):7–23; d_bg_s.h43/214/247–249; c_bg_s_gnd_chk.h8–12. |
| S21 | [Dusklight ModLoader](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/mods/loader/loader.cpp):tick1237–1264, deactivate296–338; [f_ap_game](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/f_ap/f_ap_game.cpp):duskExecute748–807/fapGm_Execute811–824. |

Conclusiones y gates específicos: [SCENE_OWNERSHIP](SCENE_OWNERSHIP.md), [ENEMY_PARAMETERS](ENEMY_PARAMETERS.md), [ARCHITECTURE_RECOMMENDATION](ARCHITECTURE_RECOMMENDATION.md), [NEXT_VALIDATION_GATES](NEXT_VALIDATION_GATES.md), [RECOVERY](RECOVERY.md).
