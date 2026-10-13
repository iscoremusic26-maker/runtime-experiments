# Adaptador nativo experimental, solo offline

Base exacta `09a682f0338d24928b3ea1abca0df6972004a596`, SDK oficial `40457c6adb381928e4b5fef6ed459ed291edd5e2`. Se implementa una ruta real distinta de los observadores READ_ONLY. No existe `.dusk` activo ni DLL entregable.

## Camino real

`mod_update` → `devf_first_request_link_anchor` → `Controller::attempt` → comprobación de Admission → dos preflights frescos → latch irreversible → `LayerScope::select(child)` → tercer preflight → `NativeBackend::request` → **una llamada** `svc_actor->create_actor(ctx_, ProfileName(0x1fe), &native, &id)` → restauración RAII de previous → observación escalar → polls limitados.

El único sitio del servicio está en `src/native_backend.cpp`; el core tiene un solo sitio `b.request(preset)`. Ambos existen en el target MSVC. El anchor `/INCLUDE` y la separación del proveedor de admisión, sin LTO (`/GL-`), impiden sustituir la prueba de enlace por un archivo que solo mide structs. ActorService1.0 se importa realmente en `modmeta`; sus funciones son indirectas, no imports `fopAcM_create` ficticios.

`src/admission.cpp` devuelve siempre `{}`: ubicación y sesión no admitidas. No hay configuración, setter, export o UI para cambiarlo. El core devuelve BLOCKED antes de cualquier lectura o escritura nativa. Solo los fakes conceden admisión. Una versión futura exige un cambio de fuente y revisión/autorización independientes; este binario experimental no se distribuye ni carga.

El preset conserva profile0x1FE, parameters0xFFFFFFFF, argument−1, room3, ángulos(−236,0,0), escala(1,1,1), callbackNULL y C exacto convertido a float32 con comprobación de finitud/rango. `setID=0xFFFF` lo fija la implementación oficial, sin una supuesta opción adicional del SDK. No se registra ni sustituye ningún perfil; el perfil nativo E_OC conserva su IA y culling originales.

## Reutilización y separación

La biblioteca STATIC `first_readonly_bridge` compila siete unidades: bridge propio y seis fuentes históricas G4B/G2/A2 sin cambios. Solo ese target usa las guardas históricas. El módulo experimental compila sus cuatro fuentes más `sdk/src/game_feature.cpp`; no se le asignan `DEVF_A2_DISARMED` ni `DEVF_READ_ONLY`. Su única guarda es `DEVF_FIRST_OFFLINE=1`, que describe el alcance del target, no prueba ausencia de creación.

La proyección copia los treinta campos de Owner. Se reutilizan resolver y consultas G4B previos; únicamente el pequeño predicado A2 se adapta al namespace nuevo, con comparación de fixtures contra el código histórico real. El monitor tiene una lectura propia mínima: el resolver histórico rechaza cualquier contador create, por lo que no puede seguir una solicitud propia pendiente. No se duplican el censo completo G2 ni las consultas geométricas.

El latch se consume antes del primer setter. Errores del servicio, excepciones, restauración fallida, timeout, shutdown o reentrada nunca lo reinician. STOP es terminal incluso antes de consumirlo. No existe cancelación, eliminación, cleanup de actores, retry ni callbacks diferidos propios.
