# A1 — condiciones preparatorias, sin implementación

**G5 NO-GO.** Este documento no autoriza un ensayo, no contiene spawner y no entrega un `.dusk`. Preset y ruta A1 se conservan; A2, hooks, setters de layer y parche experimental están fuera de alcance.

## Contrato estático focalizado

Fuente oficial intacta `40457c6adb381928e4b5fef6ed459ed291edd5e2`; se reutiliza [SCENE_OWNERSHIP](../CP01_DAWNLIGHT_AUDIT/SCENE_OWNERSHIP.md) y se contrastaron únicamente estas funciones:

| Ruta fuente | Resultado PASS_STATIC condicionado |
|---|---|
| `src/dusk/mods/svc/stage.cpp:189–205,269…` | add_actor valida/copia un registro y entrega handle de edición; no crea actor. remove_actor_edit elimina la edición, no una instancia viva |
| Mismo archivo:57–77,139–155 | Selecciona stage actual y ediciones Add de mod activo, room exacta y layer lógico coincidente; llama al createFn del host |
| `src/d/d_stage.cpp:2611–2634` | Helper sincrónico copia registro, prepara append con room del stage y llama al constructor nativo; ACTR conserva escala implícita |
| `src/d/d_stage.cpp:1635–1662,2816–2835` | Resolución de nombre/perfil/argumento nativo; roomReLoader decodifica común, consume Add y después carga registros del layer |
| `src/d/d_s_room.cpp:198–240,267…` | objectSetCheck prepara recursos/BG/event manager y llama roomReLoader durante creación/ejecución natural de ROOM_SCENE |
| `src/f_pc/f_pc_node.cpp:45–61,107–124` | Submétodos de Execute/Create del nodo establecen temporalmente su **layer hija** y restauran el contexto después |
| `include/f_pc/f_pc_manager.h:45`, `src/f_pc/f_pc_stdcreate_req.cpp:49,67` | Request captura current del contexto natural; fases posteriores restablecen la layer capturada |
| `src/d/actor/d_a_e_oc.cpp:2848…` | Perfil E_OC nativo CURRENT ya acreditado; no se registra otro perfil |

En esa cadena natural la futura solicitud proviene del contexto del nodo ROOM_SCENE: su CURRENT es la layer **hija**, no la root del mod_update ni la owner padre del nodo. G2 observó originales con owner6 y child6 de room3, padre5 y current0 del lector; **no observó una Add**. Es PASS_STATIC de esa ruta, no PASS runtime de una adición. Los números de layers/nodos/ActorIds dependen de la sesión.

No invocar roomReLoader, forzar logical6 ni usar current0 desde mod_update como prueba de propiedad correcta. Registrar una edición cuando room3 ya está residente no garantiza consumo inmediato. Cambiar de sala visible tampoco garantiza destruir/cargar el nodo. La futura prueba requiere demostrar un intervalo natural descargada→cargada antes de consumir una única edición, sin setters, teleport, flags o manipulación de cola.

## Preset que se mantiene

StageF_SP121, room3, logical6 exacto; nombre `E_oc`, perfil `fpcNm_E_OC_e=0x1FE`, argumento-1. `parameters=0xFFFFFFFF`, angle.x=-236/0xFF14, yaw0, angle.z0, setIDFFFF, ACTR escala implícita(1,1,1). Normal modo0, rango2000, búsqueda S por HIO, switchesFF. No wildcard de layer, ajuste HIO/escala ni reemplazo de original. **XYZ de nueva instancia: NOT_VERIFIED; no se reutiliza la Y de WRock.**

FILI room3 bitSwFF evita el filtro genérico concreto y EnemyAppear1Flag=false, como ya documentado. No se certifican todas las condiciones de admisión, carga o progreso a partir de esos sentinels.

## Una eventual adición y prevención de duplicados

Tras otra autorización, recursos/ubicación acreditados y baseline aislado, una prueba debería registrar como máximo **una** edición. Mantener un solo handle y estado por contexto; no Add por tick ni rearmar automáticamente al reentrar. Recarga natural puede materializar nuevamente una edición persistente. Retirarla tras el primer consumo confirmado impediría futuros consumos, pero no mata una instancia ni revoca requests ya emitidos; esta secuencia aún no está implementada ni probada.

El handle **no es ActorId**. IDs158…172 pertenecen a una sesión pasada y no identifican otra. Futuro censo previo/posterior debe distinguir una sola entrada adicional por diferencia de IDs, perfil nativo, room/owner, preset y colocación inicial propia; después revalidar fase/vida y contexto. Un lookup por perfil o la mera presencia en cola no acredita readiness. Si otros eventos/actores aparecen simultáneamente, la atribución puede ser ambigua y el ensayo debe detenerse, sin borrar un actor cuyo origen no está demostrado. No hay aquí un mecanismo runtime certificado para esa correlación.

La retirada de Add y la destrucción por transición son garantías distintas. Las solicitudes, fallos parciales, permanencia de sala y destrucción nativa necesitan evidencia futura. No asumir desaparición al desactivar el mod; no hot reload ni descarga durante solicitudes/actores activos. La descarga normal del observador G2 no resuelve el bloqueo independiente de perfiles personalizados.

## Aislamiento reversible y requisitos de ensayo posterior

No se cambia nada ahora. Una futura sesión autorizada debería: cerrar el juego antes de preparar configuración; conservar copias de configuración/lista de mods; deshabilitar reversiblemente Randomizer y reemplazos de textura mediante opciones/configuración documentadas, sin borrar archivos; conservar solo componentes oficiales imprescindibles y el módulo expresamente aprobado. Documentar overrides efectivos de E_OC/E_ocb y confirmar host/DX12/contexto/progreso sin editarlo. Luau solo si el paquete futuro realmente lo requiere.

El nuevo baseline aislado no puede presumirse idéntico a G2: censo, mods, comportamiento y recursos efectivos se confirmarían en esa futura sesión. No se solicita repetir G2 ahora. Antes del ensayo debe existir un procedimiento revisado de instalación/reversión, límite de una adición, observación y salida sin persistir cambios. No hay paquete activo preparado ni instrucciones para instalarlo en esta tarea.

Detener G5 si falta autorización, envolvente/punto/suelo, identidad host/backend, recursos efectivos, carga natural demostrada, logical6/room3, owner hijo correcto, phase/readiness, atribución única, controles contra reconsumo, o si aparecen anomalías visuales/colisión/eventos/transición. No corregir una desviación con capas globales, hooks, flags o borrado de actores desconocidos.

**NOT_VERIFIED / NOT_TESTED runtime:** creación real adicional, render DX12, cuerpo/arma/Acch, navegación/agua/ataques, ausencia de interferencia, fallos parciales, una sola instancia, transición/destrucción/recursos y reversión. G6 y CP02 siguen cerrados. Ningún contrato de fuente se eleva a PASS de estas pruebas.
