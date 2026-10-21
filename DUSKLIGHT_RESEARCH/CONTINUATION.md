# Continuidad — CP-R26

Rama research/dusklight-203-dusk-atlas en iscoremusic26-maker/Mods-Duskligh; escritura solo DUSKLIGHT_RESEARCH. Upstream 40457c6adb381928e4b5fef6ed459ed291edd5e2,árbol e4b79b565b2842f711f7c9f2390f56ef11063157; Windows x64/DX12/GZ2E01 USA. Padre verificado 4f45eafa7c96f828ce9f71cefde42346fca07716; consultar HEAD para SHA propio.

## Resultado y alcance

PORT-010..013 y nueva ficha port_presence: configuración/UI, init, mainloop/15s, payload y shutdown. bool/local log no es ACK; Borealis faltante impide certificar ownership/reconexión. Sin conexión de presencia, cuenta ni configuración personal consultada.

Baseline de esta continuación CP-R22 105ea48f71ea29909c0700a7376b88f2d6da548f:260 evidencias,263 símbolos,21 fichas,48 archivos. Actual:277 evidencias,276 símbolos,22 fichas,49 archivos. Neto:+17 evidencias,+13 símbolos,+1 documento. Checkpoints de esta continuación:CP-R23, CP-R24, CP-R25, CP-R26. No repetir campañas anteriores:CP-R10 escenas,11 AutoMata,12 Message,13 LiveSplit; seguir CHANGELOG y evidencias.

28 entradas canónicas:18 CROSSCHECKED selectivas,6 READ,4 INVENTARIED. Las cadenas nuevas son muestras,ninguna promoción global. Inventario R00 y siete erratas intactos. Cuatro submódulos ausentes,diferencia Android y falta de ABI/export/runtime Windows mantienen límites. Duración N/D,no sumar sesiones/pausas ni CPU ficticia.

## Primera acción exacta siguiente

CP-R27: alternar a Q-10 localización. Leer hud_ui_text y PRES-021/036..039/056..059; elegir carga BMG por idioma y su consumidor de grupo, sin repetir font/TextBoxEx/Message callbacks. Empezar por src/dusk/language.cpp y caller de active language; si ya cubierto, escoger skin/LOD con fuente disponible.

Antes de nueva función: consultar ficha,ledger y símbolo actuales. OPEN_QUESTIONS tiene prioridad. Si ya cubierto en nuevo HEAD,saltar a otro hueco; no repetir inventario/scheduler/fonts/AutoMata/Item/Message/LiveSplit ni implementar mods.

## Reproducibilidad y operación

Rutas efímeras:work/source/dusklight-2.0.3 certificada y work/atlas/DUSKLIGHT_RESEARCH solo si existen. Leer SOURCE_PIN/AGENTS/HEAD remoto. Comando revisado: `python work/atlas/DUSKLIGHT_RESEARCH/tools/validate_atlas.py work/source/dusklight-2.0.3`. Solo escribe VALIDATION_REPORT en atlas; fallo bloquea publicación. Valida JSON,IDs,relaciones,enlaces y rangos; no semántica,ABI,exports,build o runtime.

Diff exclusivo DUSKLIGHT_RESEARCH; HEAD/tree/padre actuales,expected_sha sin force,verificar ref y archivos remotos. Reconciliar concurrencia antes de escribir. No subir INVENTORY_SUMMARY/tools/inventory.py locales divergentes de R00. Checkpoint breve antes de otra lectura extensa.

Sin fuente/SDK/EXE/ROM/assets/saves/configuración ni producción/otros proyectos. Sin PR80/81,CI65/66,PR nuevo,issue,merge,release,tag o force. No prompts,fuentes completas ni datos personales en commits. NO MOD IMPLEMENTED / NO BUILD PERFORMED / NO GAME RUNTIME CLAIMED / NO PRODUCTION MODIFIED. Sin trabajo de fondo.

## Resumen de esta ejecución

| CP | Commit remoto anterior verificado / evidencia | Cadena y límite |
| --- | --- | --- |
| R23 | 24bc5eda073dffddfd7079c11a62874694770316 · PLAYER-046..051 | Tag→tipo1→FIRST_TALK→retirada. Tipo2/3 separados; assets/resultado final no probados. |
| R24 | b568395f73122d467fae22d6b3b923713174c428 · ARCH-008..011 | Logo stage-request y fallo task/destino; exclusión/cancelación no equivalen a rollback. |
| R25 | 4f45eafa7c96f828ce9f71cefde42346fca07716 · PRES-065..067 | JKR fetch frente a cache dRes tras retirar ganador; selector Aurora pendiente. |
| R26 | Este árbol; consultar ref para SHA propio · PORT-010..013 | Presencia host, gates/UI, payload y cierre; backend/ACK sin prueba. |

Baseline editorial CP-R22:2271 ocurrencias,1109 rangos únicos,226 fuentes citadas; actual CP-R26:2502/1213/238, deltas+231/+104/+12. Atlas49 archivos y22 fichas; +1 ficha port_presence real frente a48/21. +17 evidencias y+13 localizadores netos; no hooks operativos. 45 MD/JSON validados, sin promoción global18/6/4. Publicar con lease y verificar el árbol; ninguna edición de inventario/pin autorizada. Los bloques R23..26 anteriores quedan en CHANGELOG y sus fichas; no repetirlos.

Ninguna contradicción borrada: límites previos de readiness, snapshots, sizeof y backing siguen vigentes. Q-09/Q-12/Q-13 siguen parciales; Q-14 ahora PARCIAL por política/consumidor de overlay. Cuatro gitlinks ausentes y Android mantienen alcance; ausencia de Borealis bloquea únicamente garantías internas concretas. Primera consulta pequeña siguiente: localizar callers de language::active_language sin reauditar la tabla regional PRES-021, y decidir si hay consumidor BMG/carga aún nuevo antes de asignar CP-R27.
