# Contratos reutilizados y único servicio nuevo

Fuente host/SDK exacta: [40457c6adb381928e4b5fef6ed459ed291edd5e2](https://github.com/TwilitRealm/dusklight/tree/40457c6adb381928e4b5fef6ed459ed291edd5e2), sin cambios.

- sdk/include/mods/svc/host.h, HostService2.2: data_dir(ctx,const char**) persistente hasta shutdown. src/dusk/mods/svc/host.cpp77–109, blob edc647fc4d918900fffc17f94db0f7756e7f3902: ConfigPath/mod_data/mod->metadata.id, crea carpeta y devuelve ubicación.
- src/m_Do/m_Do_main.cpp630–631, blob58a1f3bfbd5b0b2e59e1b55bc72cfa9e3c860c2f: ConfigPath=dataPaths.userPath; --mods no es autoridad para data_dir.
- src/dusk/data.cpp (blob0ddd957e6eb32bb7dbd7feda415472f9707b95a6) delega en borealis::data::Manager. src/dusk/app_info.hpp8–9 fija TwilitRealm/Dusklight.
- Borealis exacto4ac5e7052a8c49a122f8d57f626b5c75c5ca6968, src/data.cpp418–426 (blob c9e7007b02bb97d0aa054b1d136095f1a0b6af34): SDL_GetPrefPath;630–646/649–659/724–751 distinguen predeterminado, portable, personalizado y --user-dir. Windows normal usa %APPDATA%/TwilitRealm/Dusklight. Si el usuario eligió otra carpeta, data_dir sigue la carpeta activa sin hardcodearla.
- sdk/include/mods/svc/file.h1.0: join(ctx,dir,"placements.json",&location); open READ; size/read/close síncronos en hilo del juego. join devuelve ubicación opaca válida hasta próxima join/create_child: no se conserva fuera del scope, no se concatena, no se escribe ni usa picker. Cierre verificado antes de parse/registro.
- StageService1.0 add_actor/remove_actor_edit reutilizados de QA B. Registro copia bytes; StageActorHandle es edición, NO ActorId. remove elimina edición propia, NO enemigo vivo.

Nuevo flujo: validar servicios -> cargar y cerrar archivo <=16KiB -> parse/validación completa a draft -> máscara0..2 -> mismos records BE -> registro propio con rollback. Un solo propietario de cada handle; sin punteros a actor, callbacks, dependencias de host nuevas o Token/setID improvisado. Versiones de servicio verificadas en runtime y metadatos PE.

No reapertura de register_edit, SYMGEN, recursos ARC/KCL/render, ubicaciones ni personalización. No modificación de SDK/host ni propuesta de otro ejecutable. La carpeta normal del nuevo ID es mod_data/dev.devf.cp06_native_config_dual. No escritura automática de ejemplos ni hot reload.
