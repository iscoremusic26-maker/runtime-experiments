# SDK público exacto y contrato del primer servicio

Revisión fija [Dusklight40457c6adb381928e4b5fef6ed459ed291edd5e2](https://github.com/TwilitRealm/dusklight/tree/40457c6adb381928e4b5fef6ed459ed291edd5e2), sólo lectura:
- sdk/include/mods/api.h: ServiceHeader, ModContext opaco y contrato de manifest import REQUIRED: proveedor inicializado antes de importer; deferred resuelve tras publish; major incompatible no coincide. No dependencia JSON inventada: el manifest nativo es metadata.modmeta generado por SDK.
- sdk/include/mods/service.hpp: EXPORT_DEFERRED_SERVICE produce ModMetaExport flag1/service=null; IMPORT_SERVICE produce ModMetaImport REQUIRED flag0. Proveedor usa Host.publish_service en mod_initialize después de instalar watch, con header1.0 y funciones no nulas.
- src/dusk/mods/svc/host.cpp35–43 delega publicación;125–179 watch/unwatch/detach: ctx del watcher proveedor, subject consumidor sólo válido durante callback; borrar estado antes de retorno.
- src/dusk/mods/svc/registry.cpp publish_deferred_service exige export declarado del mismo proveedor, header/versiones exactas; no publicación duplicada. resolve_service_imports falla required ausente/major distinto antes de mod_initialize.
- src/dusk/mods/loader/loader.cpp398–440 ordena dependencias y activa todo el lote antes de terminar init;1237–1266 tick itera el mismo orden;1268–1274 shutdown en orden inverso. Por REQUIRED, primer update proveedor cierra admisión antes de update consumidor. No mirar layout privado ni flags de LoadedMod desde el .dusk.

## API y propiedad
Header C ABI compartido80(request)/24(receipt)/24(service), comprobado en MSVC C11 y C++20. Funciones request_placement y remove_placement; struct_size, major/minor y funciones verificados. No STL/referencias C++ cruzando DLL, no punteros de actor ni ActorId.
Caller usa SU ModContext; Host.mod_id confirma atribución conocida. Contexto es el contrato SDK de mods nativos cooperativos, no autenticación/sandbox contra falsificación deliberada. No obtener owner por posición, ordinal o campos del juego.
Broker copia ID y conserva sólo contexto del consumidor mientras esté vivo + ticket + handle propio de StageService. Stage recibe contexto proveedor, no caller. Watch sólo compara subject y borra puntero/token incluso si cleanup falla. Residuo conserva handle sin owner y bloquea nuevas altas hasta detach proveedor.
Durante Add se detecta cancelación/reentrancia adversarial sin aceptar owner desprendido; backend alias de handle queda en fallo sin borrar registros existentes. Fuera de ventana se devuelve UNAVAILABLE. No macros privadas/offsets, register_edit ni hooks.
Ventana de bootstrap antes del primer update, no introspección de call stack ni detección pública de arranque global. Hot enable/reload queda fuera de contrato; sólo arranques fríos. Release permite retirar edición, no actor vivo.
Probe shutdown consulta servicio actual con Host.get_service antes de usarlo, evitando llamada a un export retirado; no usa lookup dinámico para inicialización/dependencia.

## Aislamiento del editor y del juego
10archivos core/IO/UI/tests se copian byte por byte de CP07.1; contadores/render/config siguen intactos. Core JSON y registros externos son autoridades separadas dentro del mismo proveedor; un único servicio Stage crea las ediciones. Máscara/capacidad2 y conflictos impiden doble mismo sitio.
El editor no serializa ni modifica entradas API. Guardar JSON para siguiente reinicio no cambia ediciones actuales. Nativos sin salud/color/IA personalizados. No host/SDK/Aurora/Borealis/importlib/ROM/saves modificados ni rebuild del ejecutable.
Contrato y laboratorio +PE permiten QA, no PASS de aparición humana ni loader ejecutado en CI.
