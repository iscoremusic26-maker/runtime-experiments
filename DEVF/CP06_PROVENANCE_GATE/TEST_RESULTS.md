# Gates y pruebas efectivamente ejecutadas

| Gate | Dictamen binario | Prueba / límite |
| --- | --- | --- |
| P0 SRC_PROVENANCE | PASS | stage.cpp exacto blob4dfd265…; trayecto antes/después y referencias fijadas, sin nuevo análisis de mapa/render. |
| P1 ABI_AND_SYMBOL | PASS | **Estático binario**: EXE SHA exacto, RSDS/manifiesto concordantes, alias fuente unívoco, sin flags inline/multiname/dupname para register_edit; intervalo .pdata y argumentos/outHandle/retorno medidos. Hook instalado/runtime NOT_TESTED. |
| P2 OWNER_TO_ACTOR_BRIDGE | NO_GO | El primer eslabón handle→buffer almacenado falta bajo la prohibición de leer layout privado. No traza A/B a request/ActorId ni afirmación de imposibilidad universal. |
| P3 CORE_ISOLATION | NOT_RUN | P2 no pasó: no implementación genérica, callbacks nuevos, dos owners/actores o simulación que suplante host. |
| P4 SITE2 | NOT_RUN en esta tarea / SITE2_PENDING heredado | Estudio norte/sur del checkpoint anterior conservado; no whitelist nueva. |
| P5 PACKAGE/HUMAN_TEST | NOT_RUN | No mod compilado/paquetizado, ni descarga de TEST nuevo ni gameplay. |

## Ejecuciones nuevas

| Run real privado | Fuente realmente checkout | Resultado |
| --- | --- | --- |
| [38749242238](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38749242238) | 586ef29ec87698fad12210486b72c31bffec187c | SUCCESS, medición inicial de símbolos/demangling. Campo ci_sha del primer JSON tomó GITHUB_SHA=e397ed4d0ed2115583f988b458b783a2dfbf167f (merge temporal de evento), no fuente. Se corrigió después separando ambos campos. No reatribuir ese JSON a una fuente compilada. |
| [38749796088](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38749796088) | 16984c96e7d6cb87a17c99729dfc586ee058640b | FAILURE, NO_FOCAL_INSTRUCTIONS por regex/escapes del script nuevo. No demuestra ausencia de función; no se instaló ningún hook. Corrección en commit siguiente, sin amend/force. |
| [38749877215](https://github.com/iscoremusic26-maker/codex-cp00-inputs/actions/runs/38749877215) | 9b4930b3bab0a6437b17ce99e3f232f724823a5f | SUCCESS, job116473164418. Símbolos + desensamblado de un único límite + compilación/ejecución fixture propio MSVC. Inicio14:16:10Z/final14:17:36Z,86s de run según API. |

Se leyeron realmente los logs de estos jobs por conector GitHub. Evidencia derivada seleccionada en evidence/symbol-abi-result.json, sin rawlog de usuario, EXE/DLL/PDB/SDK ni bytes originales.
El fixture prueba sólo pointer8/ModResult4/Header72/Entry24 con api.h original; no ActorEditRecord/LoadedMod, dos Add, callbacks asincrónicos, muerte/ID reciclado/epoch. No etiquetar ese fixture como P2/P3, ni como BUILD_PASS de un mod.

## Preservación y no ejecución
Sin código funcional CP01–06, CMake, .dusk, JSON config/max1/whitelist, workflows históricos ni recursos modificados. Todos los archivos del baseline d9a7765… deben coincidir por path/blob/mode/type (readback final en PR40). Sólo archivos NUEVOS de esta etapa bajo CP06_PROVENANCE_GATE; CI nuevo y separado en inputs. Originales de inputs preservados por mismo control.
Tag humano existente5b9f2847…→3ab8ff2… y seis tags previos se revalidan, no retag. PR37/38/39 siguen draft/open/unmerged sin modificaciones.
Los cinco PASS humanos CP06 parcial siguen sus categorías originales; no se heredan a multiinstancia, reentrada, FPS, hardware/terceros o modelo retail idéntico. No nuevas pruebas solicitadas al usuario. **NO PROBAR NADA.**
