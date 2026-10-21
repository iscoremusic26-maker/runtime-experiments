# Continuidad — CP-R12

Rama research/dusklight-203-dusk-atlas de iscoremusic26-maker/Mods-Duskligh; solo DUSKLIGHT_RESEARCH. Fuente 40457c6adb381928e4b5fef6ed459ed291edd5e2,tree e4b79b565b2842f711f7c9f2390f56ef11063157; Windows x64/DX12/GZ2E01 USA. Padre verificado CP-R11 b90b9ebef217c8fd21510e152819e0570271d92d; consultar HEAD para SHA propio.

CP-R10 completo: file-select→PLAY en systems/runtime_and_lifecycle.md, ARCH-002..007. Aceptación booleana distinta de request_id/creating_id/existencia/ejecución; caller ignora retorno; delete-before-create destruye UI/fileSel/heap y limpia vista. Creación por fases/overlap pausa destino; ReRequest solo antes de creating_id y cancelación no reconstruye escena. No todos los errores/gates auditados. Totales207 evidencias,221 símbolos,20 fichas,47 archivos; +6/+6/+0 desde CP-R09. Estados canónicos18 CROSSCHECKED selectivos,6 READ,4 INVENTARIED sin cambio. Inventario R00 intacto.

CP-R11 completo: models_animations_materials AutoMata→morf/BCK/BTK→execute/draw→resDelete/heap. PRES-044..047. Instancias y recursos tienen ownership distinto; setAnm falla después de mutar BCK si BTK falta; remove BTK no restaura pila anterior. Totales211 evidencias,225 símbolos,20 fichas,47 archivos. Neto desde CP-R09:+10/+10/+0 en dos cadenas representativas; niveles canónicos sin cambio.

CP-R12 completo: MessageService en callback_ownership_and_cancellation, CALLBACK-009..013. Candidatos copiados sin revalidar handle/active; copia de texto tras callback y retención shared_ptr por binding. Remove/detach no libera texto ya seleccionado ni prueba fin de callback/userData/DLL; reset/destructores de control/processor liberan bindings. Totales216 evidencias,229 símbolos,20 fichas,47 archivos. Neto CP-R09:+15/+14/+0,tres cadenas nuevas. Estado canónico sin cambio.

Próxima acción exacta CP-R13: alternar Q-13 soporte interno speedrun/LiveSplit. Leer port_achievements/índice para no duplicar; localizar src/dusk/livesplit.cpp y su caller real. Seguir generación/evento→estado/conexión→envío/error/cierre sin abrir datos del jugador ni conectar a LiveSplit. Si hay bloqueo elegir Q-12 puzzle/minijuego con fuente disponible. No tratar soporte interno como servicio SDK. Después alternar Q-12 o Q-11 otro controlador ambiental; no repetir Item/Message/fonts/time.

Q-01 parcial para otros dispatchers; Q-02 contrato explícito de reentrancia pendiente. Q-09 fallos/otras escenas y Q-10 formatos/LOD/skin permanecen parciales.

Rutas efímeras work/source/dusklight-2.0.3 (certificada) y work/atlas/DUSKLIGHT_RESEARCH solo si existen. No repetir inventario/hashes. Revisar validador antes de ejecutarlo contra fuente; fallo bloquea publicación. HEAD/tree/padre actuales,expected_sha sin force; verificar ref y documentos remotos tras cada commit, reconciliar cambios concurrentes. Checkpoints breves antes de lecturas extensas. Submódulos4 y diferencia Android permanecen; ningún ABI/export/runtime Windows certificado.

Solo documentos/índices. Sin tocar producción,fuente,SDK,assets,saves,configuración,PR80/81,CI65/66 ni otra rama. Sin PR,merge,release,tag,force; no subir prompts ni fuente completa. NO MOD IMPLEMENTED / NO GAME RUNTIME CLAIMED / NO PRODUCTION MODIFIED. Sin tarea de fondo.
