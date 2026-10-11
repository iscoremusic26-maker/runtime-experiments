# Implementación y límites de CP01

## Base y actor
Fuente única: dusklight-2.0.3.zip ya verificado en CP00. Adaptación de mods/custom_actor_demo/src/m_a_obj_wrock.hpp y .cpp, no una copia de objetos, perfiles/vtables ni ABI antiguo. El nombre exclusivo dvfrock no aparece en el árbol retail 2.0.3. ActorService rechaza un conflicto con otro perfil custom. No registra wrock ni un nombre retail.

Rock conserva fopAcM_ct, archive Wrock, índices BMD=4/DZB=7 oficiales, heap del demo, creación mDoExt_J3DModel__create, dBgW, corrección de suelo/sala, transformación por instancia, registro/movimiento de colisión y el par setListBG/setList. No empaqueta recursos retail ni reemplaza texturas/materiales. La iluminación estándar del demo sigue usando el pipeline del juego; aislamiento visual real no acreditado.

ResourceLifecycle es compartido con el laboratorio: mantiene fase pendiente, no declara listo un actor solicitado, inicializa heap/colisión una sola vez, hace terminales los errores y retira colisión registrada antes de liberar la solicitud de archivo. Limpieza idempotente de su estado y referencias; la memoria solid heap sigue perteneciendo al motor. Punteros del actor limitados a su propia instancia, sin registro global de punteros ni offsets retail. Contadores saturados de create/ready/execute/draw/delete permiten diagnóstico posterior con log acotado al cierre.

Las llamadas nativas reales se compilan/enlazan, pero no se ejecutaron en el juego. El laboratorio no acredita constructores/heap/J3D/Bgsp reales, colisión física ni dibujo.

## ActorService y StageService
Controller usa tablas de servicios SDK, registro propio y handles separados. start valida perfil/nombre y, si hay placement, requiere evidencia externa explícita, stage no vacío <=8, sala específica, capa y registro ACTR de 32 bytes con nombre correcto. No existe placement de producción en este checkpoint. Los bytes/campos completos de un futuro registro deberán construirse mediante stage_actor_data_class 2.0.3; el laboratorio usa exclusivamente una fixture sintética LABONLY, nunca el juego.

Stage add_actor registra datos para la carga posterior de escenario/sala/capa; no activa instantáneamente la sala cargada. Se ha comprobado la ruta stage_create_new_actors del host y su integración en d_stage.cpp. remove_actor_edit retira futuras apariciones, no borra por sí mismo una instancia ya creada. Para limpiar instancias propias se utiliza unregister_actor del perfil.

request_runtime usa ActorService::create_actor con escala positiva/finita, posición finita y sala válida. Es una autoridad alternativa: se rechaza si existe registro Stage o una solicitud runtime previa en la activación. No se guarda ActorId efímero ni se borra un actor con ID posiblemente reutilizado. Ninguna llamada runtime se expone o activa automáticamente en el mod entregado.

Rollback explícito: fallo de stage add retira perfil; stop retira primero registro Stage, luego perfil. Fallos conservan handles y bloquean un segundo start. No se informa éxito de limpieza ante MOD_UNAVAILABLE.

## Orden de desactivación del host exacto
loader.cpp::deactivate_mod llama modules_mod_deactivating ANTES de mod_shutdown. ActorService registra actor_remove_mod en modDeactivating; StageService borra registros en modDetached DESPUÉS de mod_shutdown. Por eso stop(true) en el callback de shutdown admite MOD_INVALID_ARGUMENT solo al retirar el perfil ya consumido por el pre-hook nativo; no lo admite en cleanup/rollback ordinario ni en retirada Stage. MOD_UNAVAILABLE conserva el fallo. La discrepancia entre actores construidos y destruidos también devuelve fallo.

Bloqueo comprobado: el loader continúa a unload_native aunque shutdown falle, y actor_remove_mod registra error pero no impide unload. El barrido de unregister_actor considera colas activas/deletion; no se ha demostrado que cubra solicitudes de creación aún pendientes. Un retorno de error del mod no retiene la DLL. No se introduce un parche al EXE, un hook global o una DLL auxiliar para cambiarlo. La falta de prueba real de este cierre impide aprobar TEST con actores activos.

## Ubicación y política de seguridad
El demo oficial aporta F_SP108/sala 0 y coordenadas, pero el handoff CP00 ya las clasificaba como referencia sin certificación. No hay ROM/escena en ejecución, suelo/resources/eventos verificados ni log de usuario que acrediten un lugar seguro. No se inventa uno.

El módulo carga por ResourceService el res/safety-policy.txt propio, exige NO_AUTOMATIC_SPAWNS y libera el buffer. Alterar esa política provoca rechazo antes de registrar. Solo registra el perfil; no crea actores ni registra un placement. No hay forma de convertir un cambio del .txt en coordenadas activas. Stage y runtime están implementados en el controlador y probados con tablas simuladas, pendientes de integrarse con una ubicación real verificada dentro de CP01.

Windows x64 y host 2.0.3 se restringen en build/import/guardas. DX12 es el único backend objetivo de pruebas; el mod no cambia renderer ni afirma comprobar el backend mediante una API inexistente. No hay funcionalidad CP02, enemigo retail ni editor.
