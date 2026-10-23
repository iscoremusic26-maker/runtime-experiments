# Auditoría semántica enfocada — CP-R96

Base remota CP-R95 `8e4a5492a0b31e3104a75b71c8632c0302fc9d0f`; fuente única `40457c6adb381928e4b5fef6ed459ed291edd5e2`. Resuelve V1-C01 de [readiness](V1_READINESS.md). Es una revisión de afirmaciones con riesgo de selección equivocada, no una nueva auditoría de todos los símbolos ni de los 209 slots.

## Correcciones trazables

| Registro afectado | Proposición anterior / ajuste | Contraste y efecto |
| --- | --- | --- |
| `dusk::mods::svc::item_gives_tick`, WORLD-021 | OFFICIAL_SERVICE → POTENTIAL_REQUIRES_VERIFICATION | [item_gives_tick](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/mods/item_gives.cpp#L367-L396) es un helper interno; [tabla ItemService](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/sdk/include/mods/svc/item.h#L71-L109) declara give_item y observe_gives como entradas del servicio. Se preservan claim/nivel de WORLD-021: enqueue no confirma grant ni durabilidad. No se retiró una API pública. |
| `stage_tgsc_data_class`, WORLD-033/038/039/040 | OFFICIAL_SERVICE → POTENTIAL_REQUIRES_VERIFICATION | [declaración TGSC](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/include/d/d_stage.h#L221-L228) declara estructura del juego; [StageService](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/sdk/include/mods/svc/stage.h#L20-L40) expone operaciones con bytes/tamaño. [constantes de tamaño](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/mods/svc/stage.cpp#L23-L24) fija 0x20/0x23 aceptados. Conservar la rectificación CP-R22: stride de struct, bytes del CRC y payload admitido son unidades distintas; sizeof/offset Windows sin medir. |

Las condiciones antiguas ya advertían helper interno y tamaño no medido, pero la etiqueta oficial contradecía esa explicación. Se corrige la etiqueta y se añaden notas en WORLD-021/033, sin borrar IDs ni cambiar niveles. 452 registros permanecen:87 OFFICIAL_SERVICE,360 POTENTIAL_REQUIRES_VERIFICATION y5 TYPED_HOOK;delta de clasificación -2/+2/0 respecto CP-R95. Esos87 incluyen servicios/tipos y ranuras;no representan87 slots auditados a fondo.

## Cinco TYPED_HOOK: procedencia conservada

| Registro | Sustento releído | Conclusión y frontera |
| --- | --- | --- |
| `mods::HookImpl<Tag,R,A...>::trampoline` | [trampoline](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/sdk/include/mods/svc/hook.hpp#L53-L90), HOOK-004 | Args/retval locales de la llamada;no retener referencias después. El tipo del helper no prueba el ABI de un target. |
| `mods::hook::install<Entry>` | [install](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/sdk/include/mods/svc/hook.hpp#L169-L186), HOOK-003 | Comprueba servicio/target y obtiene original;puede fallar. No acredita resolución o interceptación efectiva Windows. |
| `mods::hook::uninstall<Entry>` | [uninstall](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/sdk/include/mods/svc/hook.hpp#L240-L255), HOOK-007 | Exige slot disponible y target;éxito limpia estado local. No restaura efectos game-side ni demuestra callback drenado. |
| `daAlink_c::posMove` y `daAlink_c::execute` | [ejemplos tipados](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/docs/modding.md#L1315-L1345), [gate FEATURES](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/sdk/include/mods/svc/hook.hpp#L1-L5), PLAYER-034 | Ejemplos explícitos DEFINE_HOOK y FEATURES game justifican ruta tipada documentada. No se promovieron otros métodos por tener cuerpo C++;símbolo, firma binaria, coexistencia y unload siguen pendientes. |

## Otros puntos de alto impacto contrastados

- **Versiones/imports:** [service_import](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/src/dusk/mods/svc/registry.cpp#L362-L392) valida import y busca id/major/minor;optional ausente no equivale a backend implementado y un import válido no prueba cada operación. HOOK-002 conserva ese alcance.
- **UiService:** [versión UI](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/sdk/include/mods/svc/ui.h#L11-L13) y [tabla UI](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/sdk/include/mods/svc/ui.h#L354-L370) corresponden a major2/minor3 y al tipo `UiService`. El candidato histórico v1 del host no cambia el nombre del tipo SDK actual ni vuelve J2D una UIhost. CALLBACK-032..034/047..049 conservados.
- **GameService:** [GameService](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/sdk/include/mods/svc/game.h#L1-L26) declara época2.0 y solo ServiceHeader. No es una API de control arbitrario del juego ni comprobación de todos los layouts C++. HOOK-027 conservado.
- **SaveService:** [contrato Save](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/sdk/include/mods/svc/save.h#L31-L62) declara set_blob y observe_saves;`save_slot_written` continúa POTENTIAL, helper interno, no nuevo slot. Copia/dirty, notificación vanilla y durabilidad sidecar no son equivalentes;WORLD-011/012/034..037 conservados.
- **Luau:** [familias de bundle](https://github.com/TwilitRealm/dusklight/blob/40457c6adb381928e4b5fef6ed459ed291edd5e2/docs/modding.md#L4-L14) documenta runtime de script limitado a servicios expuestos. SCRIPT_API sigue DOC_CONTRACT;no acredita acceso C++ arbitrario, conjunto completo de bindings o proveedor externo disponible. HOOK-024 conservado.
- **Ownership/error:** la revisión anterior de callbacks, heaps, packets, overlays y saves mantiene sus condiciones;ningún unregister se convierte aquí en drenaje, ningún Delete en GPU idle, ningún MOD_OK en persistencia. Véanse [riesgos](RISK_REGISTER.md) y [preguntas](OPEN_QUESTIONS.md). No se reauditaron todas esas cadenas.

## Método, alcance y deuda no bloqueante

Se filtraron los89 registros OFFICIAL_SERVICE previos:87 apuntaban a sdk/ y los dos corregidos a fuente del juego/host. Los identificadores de esos87 se encontraron en sus cabeceras SDK del pin;esto es comprobación de nombre/procedencia, no de semántica completa ni versión de todos los slots. Se leyeron las declaraciones y consumidores necesarios para las correcciones y las rutas tipadas/versiones indicadas arriba. El validador protegido añade estructura/IDs/relaciones/rangos;no sustituye esta comparación semántica.

132 objetos source carecían de url opcional al comenzar esta revisión. Se añadieron cuatro permalinks de los registros tratados, quedando128;repo/commit/path/rangos y evidence_ids ya permitían trazarlos por el ledger. No se migraron índices por estética. Esa deuda opcional no impide navegación ni prueba ABI.

Sin nuevos IDs, símbolos, fichas o niveles de cobertura. Nuevo documento complementario;las citas de esta auditoría incrementan ocurrencias/rangos según cálculo del validador, no conocimiento ejecutado. No se afirman fallos observados. Cuatro gitlinks, Android excepcional, DLL/ABI/exports Windows y0 runtime permanecen límites. V1-C02/03 siguen pendientes;este documento por sí solo no declara V1_READY_STATIC_ONLY.
