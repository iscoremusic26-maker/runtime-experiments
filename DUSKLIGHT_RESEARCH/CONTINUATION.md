# Continuidad — CP-R13

Rama research/dusklight-203-dusk-atlas en iscoremusic26-maker/Mods-Duskligh; solo DUSKLIGHT_RESEARCH. Fuente40457c6adb381928e4b5fef6ed459ed291edd5e2,tree e4b79b565b2842f711f7c9f2390f56ef11063157; Windows x64/DX12/GZ2E01 USA. Padre CP-R12 verificado893106a330b128d4743f51de54e03d7cb84f8f4c; consultar HEAD para SHA propio.

## Checkpoints de esta continuación

- CP-R10 e44139795c4e0beb1e1bf608bd894d0656a06c4b: runtime_and_lifecycle,ARCH-002..007. File-select→PLAY,aceptación distinta de ejecución,delete-before-create,destructor de UI/fileSel/heap,overlap/pausa y cancelación/ReRequest. Caller ignora retorno; no rollback demostrado.
- CP-R11 b90b9ebef217c8fd21510e152819e0570271d92d: models_animations_materials,PRES-044..047. AutoMata→morf/BCK/BTK→execute/draw→cleanup. Recursos prestados e instancias de heap distintos; setAnm puede mutar BCK antes de fallar BTK; remove no restaura animator previo.
- CP-R12 893106a330b128d4743f51de54e03d7cb84f8f4c: callback_ownership_and_cancellation,CALLBACK-009..013. Message copia candidatos sin revalidar handle/active; texto se copia después de callback y vive en bindings; remove/detach no drena callback ni libera bytes ya seleccionados. Reset/destructores de control/processor liberan bindings.
- CP-R13: port_speedrun_livesplit,PORT-006..009. SaveLoaded→modo/tick/contador y UI→red son rutas separadas. Contador/30 no es tiempo real medido; send no comprueba resultado ni ACK,Connected no rearma startPending. Borealis ausente limita copias/cierre/entrega. Sin conexión externa realizada.

Totales220 evidencias,232 símbolos,21 fichas,48 archivos. Neto frente a HEAD inicial CP-R09 03f2a405fbab7f8d2caed286bffd37728eaf07d4:+19 evidencias,+17 símbolos,+1 documento real; cuatro cadenas representativas,sin pretender familias completas. 28 entradas canónicas:18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED. Inventario R00 intacto. Duración de esta continuación N/D,no sumar pausa ni sesión previa. Todos los checkpoints pasan validador editorial contra fuente certificada; no certifica semántica,ABI,export ni juego.

## Primera acción exacta CP-R14

Alternar Q-12 puzzles/minijuegos. Leer systems/other_systems.md,actors_ai_npcs y ledger antes de elegir. Archivo existente src/d/actor/d_a_obj_swpush.cpp: localizar Mthd_Create/Mthd_Execute/Mthd_Delete,ride callback y acción de switch; verificar símbolos con rg y seguir condición de activación→estado→switch/colisión→desregistro/heap con un consumidor real. No repetir carga de modelos de CP-R11 ni tratar un puzzle como regla de todos los NPC/bosses. Si ya cubierto en nuevo HEAD,saltar a otro hueco Q-12/Q-11.

Q-09 parcial: fallos de overlap/creación,logo/direct-load,opening/reset y todos los gates captura/presentación. Q-10 conserva formatos/LOD/skin/otros morf/TextBoxEx. Q-01 otros dispatchers,Q-02 contrato de reentrancia,Q-03 teardown con instancias pendientes; Q-13 backend/ACK de LiveSplit,presence/diagnostics y configuración completa. Ningún ABI/runtime Windows nuevo;4 submódulos ausentes y diferencia Android mantienen límites.

## Operación

Rutas efímeras work/source/dusklight-2.0.3 (certificada) y work/atlas/DUSKLIGHT_RESEARCH solo si existen. Leer SOURCE_PIN/AGENTS y HEAD actual,no repetir inventario/hashes. Validador revisado: source como argumento,escribe solo VALIDATION_REPORT del atlas; fallo bloquea publicación. Diff solo DUSKLIGHT_RESEARCH; HEAD/tree/padre actual,expected_sha sin force; verificar ref y contenido remoto después,reconciliar si hay concurrencia. No subir local INVENTORY_SUMMARY/tools/inventory.py divergentes de R00. Checkpoints cortos antes de lectura extensa.

Solo documentos e índices. Sin fuente,SDK,assets,saves,configuración,producción,PR80/81,CI65/66 ni otra rama. Sin build,mod,.dusk,PR nuevo,merge,release,tag o force. No prompts/fuentes completas/secretos en commits. NO MOD IMPLEMENTED / NO GAME RUNTIME CLAIMED / NO PRODUCTION MODIFIED. Sin ejecución de fondo ni tarea programada.
